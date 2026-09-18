"""Reproduce the v1 98% claim twice: naive random 80/20 vs group-aware split.

Arm A (naive):  stratified random 80/20 by file, seed 42  -> expected: high
Arm B (honest): data/split.json manifest (dupes removed, processed
                families kept together)          -> expected: visible drop

Needs ultralytics + torch on a GPU machine:
  pip install -r requirements.txt
  python3 scripts/reproduce_v1.py --dataset-root "/path/to/Fabric Defects Dataset" \\
      --split data/split.json --base-weights ~/Downloads/yolo11n.pt \\
      --epochs 50 --work runs/repro --out docs/repro.json

Eval-only mode (no training, needs a trained classify *.pt):
  python3 scripts/reproduce_v1.py --eval-only --weights /path/to/best.pt \\
      --dataset-root ... --split data/split.json --out docs/repro.json
"""
import argparse
import json
import os
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from metrics import confusion_prf  # noqa: E402  (stdlib core)


def sanitize(name):
    return name.replace(" ", "_")


def load_manifest(split_path, dataset_root):
    m = json.loads(Path(split_path).read_text())
    root = Path(dataset_root or m["root"])
    return root, m["train"], m["test"]


def stratified_random(pool, test_frac, seed):
    """pool: list of (cls, rel). Returns (train, test) as {cls: [rel]}."""
    by_cls = {}
    for cls, rel in pool:
        by_cls.setdefault(cls, []).append(rel)
    rng = random.Random(seed)
    train, test = {}, {}
    for cls, rels in sorted(by_cls.items()):
        rels = sorted(rels)
        rng.shuffle(rels)
        n_test = max(1, round(len(rels) * test_frac))
        test[cls] = rels[:n_test]
        train[cls] = rels[n_test:]
    return train, test


def manifest_split(train_rels, test_rels):
    train, test = {}, {}
    for rel in train_rels:
        cls = rel.split("/", 1)[0]
        train.setdefault(cls, []).append(rel)
    for rel in test_rels:
        cls = rel.split("/", 1)[0]
        test.setdefault(cls, []).append(rel)
    return train, test


def materialize(split, dataset_root, dest, link_mode="symlink"):
    """Place split {cls: [rel]} under dest/<side>/<sanitized_cls>/.

    link_mode='symlink' (fast, needs POSIX fs) or 'copy' (Colab/Drive,
    where the FUSE mount rejects symlinks).
    """
    import shutil
    mapping = {}
    for side, groups in split.items():
        for cls, rels in groups.items():
            safe = sanitize(cls)
            mapping[safe] = cls
            d = dest / side / safe
            d.mkdir(parents=True, exist_ok=True)
            for rel in rels:
                src = (dataset_root / rel).resolve()
                dst = d / Path(rel).name
                if dst.exists() or dst.is_symlink() or not src.exists():
                    continue
                if link_mode == "copy":
                    shutil.copy2(src, dst)
                else:
                    os.symlink(src, dst)
    (dest / "class_map.json").write_text(json.dumps(mapping, indent=2))
    return mapping


def evaluate_predictor(predict_fn, test_groups, dataset_root):
    """predict_fn(path) -> predicted class dir name. Returns metrics dict."""
    y_true, y_pred = [], []
    for cls, rels in sorted(test_groups.items()):
        for rel in sorted(rels):
            p = dataset_root / rel
            if not p.exists():
                continue
            y_true.append(sanitize(cls))
            y_pred.append(predict_fn(str(p)))
    prf = confusion_prf(y_true, y_pred)
    return {"n": len(y_true), "accuracy": prf.pop("_accuracy"),
            "per_class": prf}


def main():
    ap = argparse.ArgumentParser(description="v1 claim reproduction: naive vs honest split.")
    ap.add_argument("--dataset-root", default=None)
    ap.add_argument("--split", default="data/split.json")
    ap.add_argument("--base-weights", default="yolo11n.pt")
    ap.add_argument("--epochs", type=int, default=50)
    ap.add_argument("--imgsz", type=int, default=640)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--work", default="runs/repro")
    ap.add_argument("--out", default="docs/repro.json")
    ap.add_argument("--eval-only", default=None,
                    help="path to trained classify best.pt: skip training, eval on honest test")
    ap.add_argument("--link-mode", default="symlink", choices=["symlink", "copy"],
                    help="copy = for Google Drive/Colab (no symlink support)")
    args = ap.parse_args()

    try:
        from ultralytics import YOLO
    except ImportError:
        sys.exit("ultralytics not installed — run: pip install -r requirements.txt")

    dataset_root, m_train, m_test = load_manifest(args.split, args.dataset_root)
    if not dataset_root.exists():
        sys.exit(f"dataset root missing: {dataset_root} (pass --dataset-root)")
    report = {"seed": args.seed, "epochs": args.epochs, "imgsz": args.imgsz}

    def run_arm(arm_name, train_groups, test_groups, weights):
        arm_dir = Path(args.work) / arm_name
        train_dir = arm_dir / "train"
        materialize({"train": train_groups, "test": test_groups},
                    dataset_root, arm_dir, link_mode=args.link_mode)
        model = YOLO(args.eval_only or weights)
        if not args.eval_only:
            model.train(data=str(train_dir), epochs=args.epochs,
                        imgsz=args.imgsz, seed=args.seed,
                        project=str(arm_dir), name="train", verbose=False)
        names = model.names  # idx -> folder name

        def predict_fn(path):
            r = model.predict(path, verbose=False)[0]
            return names[int(r.probs.top1)]

        res = evaluate_predictor(predict_fn, test_groups, dataset_root)
        print(f"[{arm_name}] n={res['n']} acc={res['accuracy']:.3f}")
        for cls, v in sorted(res["per_class"].items()):
            print(f"    {cls:12s} P={v['precision']:.2f} R={v['recall']:.2f} F1={v['f1']:.2f}")
        return res

    if args.eval_only:
        test_groups = manifest_split(m_train, m_test)[1]
        report["eval_only_weights"] = args.eval_only
        report["honest_test"] = run_arm("honest", {}, test_groups, None)
    else:
        pool = ([(r.split("/", 1)[0], r) for r in m_train]
                + [(r.split("/", 1)[0], r) for r in m_test])
        naive_train, naive_test = stratified_random(pool, 0.2, args.seed)
        honest_train, honest_test = manifest_split(m_train, m_test)
        report["naive_random_split"] = run_arm("naive", naive_train, naive_test,
                                               args.base_weights)
        report["honest_manifest_split"] = run_arm("honest", honest_train,
                                                  honest_test, args.base_weights)
        a = report["naive_random_split"]["accuracy"]
        b = report["honest_manifest_split"]["accuracy"]
        report["accuracy_drop"] = a - b
        print(f"\nnaive={a:.3f} honest={b:.3f} drop={a - b:+.3f} "
              f"(positive drop = old claim was inflated)")

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
