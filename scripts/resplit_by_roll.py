"""Roll-disjoint re-split manifest generator (stdlib only).

Why: v1 used an undocumented 80/20 split with no roll separation, so the
98% claim is not defensible. This script assigns WHOLE rolls to train or
test so the model is evaluated on unseen fabric, and writes a manifest
instead of moving files (safe, reviewable).

Roll id is taken from the filename via --roll-regex (first group), else
falls back to the parent folder name. If neither separates anything
(single folder, no pattern), output says so honestly instead of faking
roll-disjointness.

Usage:
  python3 scripts/resplit_by_roll.py --root data/pilot --test-frac 0.2 \\
      --roll-regex '^([A-Za-z0-9]+)[-_]' --seed 42 --out data/split.json
  python3 scripts/resplit_by_roll.py --root data/pilot --out data/split.json \\
      --materialize data/v2split   # creates train/<class>/ test/<class>/ symlinks
"""
import argparse
import json
import os
import random
import re
from pathlib import Path

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}


def roll_id_for(path, pattern):
    name = Path(path).name
    if pattern:
        m = re.match(pattern, name)
        if m:
            return m.group(1) if m.groups() else m.group(0)
    return Path(path).parent.name  # fallback: folder = roll


def main():
    ap = argparse.ArgumentParser(description="Generate a roll-disjoint train/test manifest.")
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", default="data/split.json")
    ap.add_argument("--test-frac", type=float, default=0.2)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--roll-regex", default=r"^([A-Za-z0-9]+)[-_]",
                    help="first group = roll id; empty string disables, falls back to folder")
    ap.add_argument("--materialize", default=None,
                    help="optional dir to create train/<class>/ test/<class>/ symlinks")
    args = ap.parse_args()

    root = Path(args.root)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    if not root.exists():
        out.write_text(json.dumps({
            "root": args.root, "error": "root does not exist",
            "train": [], "test": [],
        }, indent=2))
        print(f"root {args.root} does not exist — wrote empty manifest to {out}")
        return
    pattern = args.roll_regex or None
    by_class_roll = {}  # cls -> {roll: [relpath]}
    pattern_hits = 0
    total = 0
    for sub in sorted(p for p in root.iterdir() if p.is_dir()):
        for p in sorted(sub.iterdir()):
            if not (p.is_file() and p.suffix.lower() in IMG_EXTS):
                continue
            total += 1
            if pattern and re.match(pattern, p.name):
                pattern_hits += 1
            rid = roll_id_for(p, pattern)
            by_class_roll.setdefault(sub.name, {}).setdefault(rid, []).append(
                str(p.relative_to(root)))

    rng = random.Random(args.seed)
    train, test, roll_map = [], [], {}
    for cls, rolls in sorted(by_class_roll.items()):
        ids = sorted(rolls)
        rng.shuffle(ids)
        n_test = max(1 if ids else 0, round(len(ids) * args.test_frac))
        test_ids = set(ids[:n_test])
        for rid in ids:
            side = "test" if rid in test_ids else "train"
            roll_map.setdefault(rid, {"class": cls, "side": side})
            (test if side == "test" else train).extend(rolls[rid])

    distinct_rolls = len({r for rolls in by_class_roll.values() for r in rolls})
    guaranteed = pattern_hits > 0 or distinct_rolls > sum(len(r) for r in by_class_roll.values()) == 0
    # Honest flag: true roll-disjointness needs real roll ids with >1 roll per class
    multi_roll = any(len(rolls) > 1 for rolls in by_class_roll.values())
    manifest = {
        "root": args.root,
        "seed": args.seed,
        "test_frac": args.test_frac,
        "roll_regex": args.roll_regex,
        "pattern_matched_files": pattern_hits,
        "total_images": total,
        "distinct_rolls": distinct_rolls,
        "roll_disjoint_guaranteed": bool(multi_roll and (pattern_hits > 0)),
        "note": ("OK: split is roll-disjoint" if (multi_roll and pattern_hits > 0)
                 else "WARNING: no usable roll ids — split is file-level only. "
                      "Collect roll ids (roll_XX in filenames) and re-run."),
        "train": sorted(train),
        "test": sorted(test),
    }
    # train/test must be disjoint by construction; assert before writing
    assert not (set(train) & set(test)), "manifest overlap — bug, do not use"

    out.write_text(json.dumps(manifest, indent=2))

    if args.materialize:
        base = Path(args.materialize)
        for side, items in (("train", train), ("test", test)):
            for rel in items:
                src = root / rel
                dst = base / side / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                if not dst.exists():
                    os.symlink(src.resolve(), dst)

    print(f"images={total} rolls={distinct_rolls} "
          f"train={len(train)} test={len(test)} "
          f"roll_disjoint={manifest['roll_disjoint_guaranteed']}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
