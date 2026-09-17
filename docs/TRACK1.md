# Track 1 runbook — dataset audit before any v2 training

Gate: nothing trains until the manifest below exists and is committed.

## 1. Inventory the pilot set (finds Fig 3.3/3.4-type duplication)
```bash
python3 scripts/inventory_dataset.py --root data/pilot --out docs/datasheet.json
python3 scripts/inventory_dataset.py --root data/pilot \
  --train data/pilot/train --test data/pilot/test --out docs/datasheet.json
```
Read `leakage_verdict` in `docs/datasheet.json`. If it says LEAK, the old
98% number is void — re-split and re-benchmark.

## 2. Roll-disjoint re-split (filenames carry roll ids like `roll03_...`)
```bash
python3 scripts/resplit_by_roll.py --root data/pilot --test-frac 0.2 \
  --roll-regex '^([A-Za-z0-9]+)[-_]' --seed 42 --out data/split.json
```
If output says `roll_disjoint=false`, filenames have no roll ids: rename to
`<roll>_<class>_<n>.jpg` (or keep per-roll folders) and re-run. Commit
`data/split.json`.

## 3. Metric harness smoke test (no deps needed)
```bash
python3 src/metrics.py --self-test
```
With deps (`pip install -r requirements.txt`):
- detection: `detection_map_50_95()` for mAP50 + mAP50-95, or `yolo_val()` wrapper
- classification: `confusion_prf()` per-class P/R/F1 (replaces accuracy-only)
- Ds quality: `mask_iou()` — bbox-Ds vs mask-Ds comparison (Track 2 target)
- planning: `regression_metrics()` with-Ds vs without-Ds ablation (Track 4 target)

## 4. External test-only sets (never train on these)
- Isl-Knit (3375 imgs, 7 knit faults, BUTEX 2024) + FabricSpotDefect
  (1014 imgs, 3288 spots, IUB 2024) under `data/external/`, test only.

## Exit criteria
- [ ] `docs/datasheet.json` committed (counts + bytes + md5s)
- [ ] `data/split.json` committed, roll-disjoint=true, train∩test=∅
- [ ] v1 reproduced on old split, then shown dropping on disjoint split
