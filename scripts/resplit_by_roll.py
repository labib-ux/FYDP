"""Roll-disjoint re-split manifest generator (stdlib only).

Why: v1 used an undocumented 80/20 split with no roll separation, so the
98% claim is not defensible. This script assigns WHOLE rolls to train or
test so the model is evaluated on unseen fabric, and writes a manifest
instead of moving files (safe, reviewable).

Group keys are tried in order (first match wins):
  1. `^(\d+)_processed` .... processed families (`17_processed (3).jpg`
     + variants come from one source image — splitting them across
     train/test would leak near-duplicates)
  2. `^(\d{4})_` ............ defect-free roll ids (`0015_000_04.png`)
  3. `^((?:hole|line)_\d{4}-\d{2}-\d{2})` .. dated shoots
  4. `^(\d{8})_` ............ dated shoots (`20180531_...`)
Unmatched files become singleton groups (`__file__:<name>`) and are split
randomly within their class — flagged honestly in the manifest.

Usage:
  python3 scripts/resplit_by_roll.py --root "/path/to/Fabric Defects Dataset" \\
      --test-frac 0.2 --seed 42 --out data/split.json
Override patterns with repeatable --roll-regex if filenames change.
"""
import argparse
import hashlib
import json
import os
import random
import re
from pathlib import Path

IMG_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}


def md5_of(path, chunk=1 << 20):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def prefer_key(name):
    """Cleanest filename first: no ' - Copy', no '(n)' suffix, then shorter."""
    low = name.lower()
    return (" - copy" in low, bool(re.search(r"\(\d+\)(?=\.[^.]+$)", name)),
            len(name), name)


DEFAULT_ROLL_PATTERNS = [
    r"^(\d+)_processed",                    # processed families: 17_processed (3).jpg
    r"^(\d{4})_",                           # defect-free roll ids: 0015_000_04.png
    r"^((?:hole|line)_\d{4}-\d{2}-\d{2})",  # dated shoots: hole_2018-10-11 ...
    r"^(\d{8})_",                           # dated shoots: 20180531_135032.jpg
]


def roll_id_for(relpath, patterns):
    """First matching pattern wins; else a per-file singleton group."""
    name = Path(relpath).name
    for pat in patterns:
        m = re.match(pat, name)
        if m:
            return m.group(1) if m.groups() else m.group(0)
    return "__file__:" + name  # no group info: split randomly, flagged


def main():
    ap = argparse.ArgumentParser(description="Generate a roll-disjoint train/test manifest.")
    ap.add_argument("--root", required=True)
    ap.add_argument("--out", default="data/split.json")
    ap.add_argument("--test-frac", type=float, default=0.2)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--roll-regex", action="append", default=None,
                    help="repeatable; tried in order, first match wins. "
                         "Default covers processed-families, roll ids, dated shoots.")
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
    patterns = args.roll_regex or list(DEFAULT_ROLL_PATTERNS)
    rng = random.Random(args.seed)

    # Pass 1: collect + drop exact byte-duplicates (keep cleanest filename).
    seen = {}  # md5 -> (cls, rel, name)
    for sub in sorted(p for p in root.iterdir() if p.is_dir()):
        for p in sorted(sub.iterdir()):
            if not (p.is_file() and p.suffix.lower() in IMG_EXTS):
                continue
            h = md5_of(p)
            rel = str(p.relative_to(root))
            cand = (sub.name, rel, p.name)
            if h not in seen:
                seen[h] = cand
            elif prefer_key(p.name) < prefer_key(seen[h][2]):
                seen[h] = cand
    removed_dupes = []  # recomputed below for the report
    by_hash_paths = {}
    # Re-scan to list which paths were dropped (cheap: reuse md5s via seen).
    for sub in sorted(p for p in root.iterdir() if p.is_dir()):
        for p in sorted(sub.iterdir()):
            if not (p.is_file() and p.suffix.lower() in IMG_EXTS):
                continue
            rel = str(p.relative_to(root))
            keeper = seen[md5_of(p)][1]
            if rel != keeper:
                removed_dupes.append({"dropped": rel, "kept": keeper})
    kept_total = len(seen)

    # Pass 2: group keepers; multi-file groups split by group, singletons pooled.
    by_class_roll = {}  # cls -> {roll: [relpath]}
    pattern_hits = 0
    for cls, rel, name in seen.values():
        if any(re.match(p, name) for p in patterns):
            pattern_hits += 1
        rid = roll_id_for(rel, patterns)
        by_class_roll.setdefault(cls, {}).setdefault(rid, []).append(rel)

    train, test = [], []
    per_class, warnings = {}, []
    for cls, rolls in sorted(by_class_roll.items()):
        grouped = {r: fs for r, fs in rolls.items() if not r.startswith("__file__:")}
        singletons = [f for r, fs in rolls.items()
                      if r.startswith("__file__:") for f in fs]
        gids = sorted(grouped)
        rng.shuffle(gids)
        n_test_groups = max(1 if gids else 0, round(len(gids) * args.test_frac))
        test_groups = set(gids[:n_test_groups])
        n_tr = n_te = 0
        for rid in gids:
            if rid in test_groups:
                test.extend(grouped[rid])
                n_te += len(grouped[rid])
            else:
                train.extend(grouped[rid])
                n_tr += len(grouped[rid])
        rng.shuffle(singletons)
        n_test_s = round(len(singletons) * args.test_frac)
        test.extend(singletons[:n_test_s])
        train.extend(singletons[n_test_s:])
        n_te += n_test_s
        n_tr += len(singletons) - n_test_s
        per_class[cls] = {"method": ("group-disjoint" if not singletons
                                     else "group-disjoint + random singletons"),
                          "n_groups": len(gids), "n_singletons": len(singletons),
                          "n_train": n_tr, "n_test": n_te}
        if singletons:
            warnings.append(f"{cls}: {len(singletons)} files have no group id "
                            f"(hash names / bare numbers) — split randomly, "
                            f"near-duplicate risk remains; collect roll ids")

    # Cross-class naming smell: same shoot prefix living in two classes.
    prefixes = {}
    for cls, rolls in by_class_roll.items():
        for rid in rolls:
            if rid.startswith("__file__:"):
                continue
            prefixes.setdefault(rid, set()).add(cls)
    for rid, clses in sorted(prefixes.items()):
        if len(clses) > 1 and (len(rid) > 3 or "_" in rid or "-" in rid):
            warnings.append(f"prefix {rid!r} appears in classes {sorted(clses)} "
                            f"— verify no near-duplicate leakage across classes")

    distinct_rolls = len({r for rolls in by_class_roll.values() for r in rolls
                          if not r.startswith("__file__:")})
    n_singletons = sum(v["n_singletons"] for v in per_class.values())
    # Honest flag: fully group-disjoint only if every file had a group id.
    manifest = {
        "root": args.root,
        "seed": args.seed,
        "test_frac": args.test_frac,
        "roll_patterns": patterns,
        "pattern_matched_files": pattern_hits,
        "total_images": kept_total,
        "exact_duplicates_removed": len(removed_dupes),
        "removed_duplicates": removed_dupes,
        "distinct_groups": distinct_rolls,
        "ungrouped_singleton_files": n_singletons,
        "per_class": per_class,
        "warnings": warnings,
        "roll_disjoint_guaranteed": bool(distinct_rolls > 0 and n_singletons == 0),
        "note": ("OK: split is group-disjoint"
                 if (distinct_rolls > 0 and n_singletons == 0)
                 else f"PARTIAL: {n_singletons} files lack group ids and were "
                      f"split randomly. Near-duplicate families (processed "
                      f"variants) are kept together; collect roll ids for v2 "
                      f"factory data to reach full disjointness."),
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

    print(f"images={kept_total} rolls={distinct_rolls} "
          f"train={len(train)} test={len(test)} "
          f"roll_disjoint={manifest['roll_disjoint_guaranteed']}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
