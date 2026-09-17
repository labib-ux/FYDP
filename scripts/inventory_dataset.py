"""Dataset inventory + train/test leakage detector (stdlib only).

Covers the v1 report gap (Fig 3.3 vs 3.4 look identical, no split manifest):
  - per-class counts, bytes, md5 for every image
  - exact-duplicate detection inside one root
  - cross-split overlap check (hash intersection of --train vs --test)

Usage:
  python3 scripts/inventory_dataset.py --root data/pilot --out docs/datasheet.json
  python3 scripts/inventory_dataset.py --root data/pilot \\
      --train data/pilot/train --test data/pilot/test --out docs/datasheet.json
"""
import argparse
import hashlib
import json
from pathlib import Path

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}


def md5_of(path, chunk=1 << 20):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def scan(root):
    """Return (classes, hashmap, filelist) for class-subfolder layout."""
    root = Path(root)
    classes, hashmap, files = {}, {}, []
    if not root.exists():
        return classes, hashmap, files
    for sub in sorted(p for p in root.iterdir() if p.is_dir()):
        recs = []
        for p in sorted(sub.iterdir()):
            if not (p.is_file() and p.suffix.lower() in IMG_EXTS):
                continue
            rel = str(p.relative_to(root))
            h = md5_of(p)
            recs.append({"path": rel, "md5": h, "bytes": p.stat().st_size})
            hashmap.setdefault(h, []).append(rel)
            files.append(rel)
        if recs:
            classes[sub.name] = recs
    return classes, hashmap, files


def main():
    ap = argparse.ArgumentParser(description="Inventory a fabric dataset, detect duplicates/leakage.")
    ap.add_argument("--root", required=True, help="Dataset root with <class>/ subfolders")
    ap.add_argument("--train", default=None, help="Train split root (same layout) for overlap check")
    ap.add_argument("--test", default=None, help="Test split root (same layout) for overlap check")
    ap.add_argument("--out", default="docs/datasheet.json", help="JSON report path")
    args = ap.parse_args()

    classes, hashmap, files = scan(args.root)
    duplicates = {h: paths for h, paths in hashmap.items() if len(paths) > 1}

    report = {
        "root": args.root,
        "total_images": len(files),
        "per_class": {c: len(r) for c, r in classes.items()},
        "total_bytes": sum(r["bytes"] for rs in classes.values() for r in rs),
        "exact_duplicate_groups": len(duplicates),
        "exact_duplicate_files": sum(len(v) for v in duplicates.values()),
    }

    if args.train and args.test:
        _, train_hashes, _ = scan(args.train)
        _, test_hashes, _ = scan(args.test)
        overlap = set(train_hashes) & set(test_hashes)
        report["train_test_overlap_hashes"] = len(overlap)
        report["train_test_overlap_files"] = sorted(
            p for h in overlap for p in train_hashes[h]
        ) + sorted(p for h in overlap for p in test_hashes[h])
        report["leakage_verdict"] = (
            "LEAK: identical files in train and test — re-split required"
            if overlap else "OK: no identical files shared between train and test"
        )
    else:
        report["leakage_verdict"] = "not checked (pass --train and --test)"

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2))
    print(json.dumps({k: v for k, v in report.items()
                      if k != "train_test_overlap_files"}, indent=2))
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
