# HANDOFF — FYDP v2 session context (read this first in a new session)

Date: 2026-09-18. Prior session did topic research + repo setup + Track 1 audit.
Next agent: verify state with the commands at the bottom before acting.

## 1. Project
Final Year Design Project (vision + image processing), team of 5–6, 1 year,
good GPU access. Continuation of ML course project (UIU, Jun 2026):
"Unified Fabric Defect Detection & Lead Time Prediction" (YOLO classifier +
Defect Density Score + RandomForest lead-time). Course report + slides exist
in Downloads (`Unified Fabric Defect Detection & Lead Time Prediction final.pdf/.pptx`).

## 2. Repos and paths (macOS, user nafizimtiazlabib)
- Old/source (read-only reference): `https://github.com/oyon79/Fabric-Defect-Detection_And_Lead-Time-Prediction`
  (code only; weights + dataset on Google Drive, NOT downloaded except below).
- Work repo: `https://github.com/labib-ux/FYDP.git`, local clone at
  `/Users/nafizimtiazlabib/FYDP/FYDP` — **all work happens here**.
- Dataset (stays out of git): `/Users/nafizimtiazlabib/Downloads/Fabric Defects Dataset` (2.0 GB).
- Weights on disk: `/Users/nafizimtiazlabib/Downloads/yolo11n.pt` ONLY.
  `best.pt` was never downloaded (Spotlight + find confirmed) — retrain path chosen instead.
- Local python3.9 has NO numpy/torch/ultralytics: all audit scripts are stdlib-only
  by design; GPU/Colab runs need `pip install -r requirements.txt`.

## 3. Commits in labib-ux/FYDP (oldest → newest)
1. `a8dd187` setup: README, .gitignore, requirements, src/config.py, folder skeleton.
2. `dd74931` v1 baseline vendored byte-for-byte to `src/v1_baseline/` (DO NOT EDIT)
   + `docs/AUDIT_V1.md` (blockers with file:line refs).
3. `ea393d7` Track 1 tools: `scripts/inventory_dataset.py`,
   `scripts/resplit_by_roll.py`, `src/metrics.py`, `docs/TRACK1.md`.
4. `f896ff3` real audit: `docs/datasheet.json` + `data/split.json` (first manifest).
5. `4b08940` (teammate) `scripts/compare_labels.py`.
6. `fe9b6a8` (teammate) `scripts/find_near_duplicates.py` + `scratch/` thumbnails.
7. `1d72795` (me) `scratch/` untracked+ignored; `scripts/reproduce_v1.py`.
8. `42edf44` (me) `data/quarantine.json` + exclusion-aware re-split.
9. `734dda6` (me) `--link-mode copy` in reproduce script (Drive/Colab compat).
Push status at handoff time was PENDING (user runs `git push -u origin main`
from `/Users/nafizimtiazlabib/FYDP/FYDP`) — verify with `git status -sb`.

## 4. v1 audit conclusions (see docs/AUDIT_V1.md)
Blockers: (1) fake localization — bbox is a centered square sized from
confidence (`v1_baseline/defect_detection.py:370-390`), never at the defect;
(2) circular lead-time labels (`Lead=(qty/speed)*0.1*(1+2*Ds)`, RF learns its
own formula, "92% MAE gain" vacuous); (3) train/test integrity (report
Fig 3.3/3.4 look identical, split undocumented). Also: preprocessing applied
at inference by default (random, degrades inputs), disambiguation thresholds
on degraded frame, single-defect-per-frame, crash without best.pt.

## 5. Dataset facts (docs/datasheet.json, data/split.json + data/quarantine.json)
- 2578 images: defect free 1505 / stain 398 / hole 281 / lines 157 /
  horizontal 136 / Vertical 101. Imbalance noted for v2 (class weights).
- 17 exact byte-dupes removed (`- Copy`, `(1)` files).
- Processed families `N_processed (k).jpg` (hole/horizontal/Vertical) are
  near-duplicate groups → kept together by group patterns in resplit script.
- QUARANTINE (12 files, team visually verified, enshrined in data/quarantine.json):
  9× `hole/line_2018-10-11*` + 3× `lines/line_2018-10-10*` counterparts —
  identical swatches cross-labeled hole vs lines, some defect-free (NOISY verdict).
- `hole/20180531*` vs `lines/20180531*` verified CLEAN (different defects, keep).
- Current manifest: 2549 imgs (2561−12), train 2087 / test 468, overlap 0,
  quarantined-in-split 0. NOT fully roll-disjoint (1994 files lack group ids:
  all of stain, hash-named pools) — honest PARTIAL flag in manifest.
- Open: row-review the 152-file `lines/line_2018-10-10` batch (clean swatches
  reportedly carry defect labels → likely second quarantine).

## 6. Upgrade roadmap (agreed, 6 tracks in README + docs/UPGRADE_PLAN.md)
T1 dataset audit (tooling DONE, quarantine DONE, repro PENDING) → T2 YOLOv11-seg
+ mask-Ds + OBB for Horizontal↔Hole 7–8% confusion → T3 PatchCore/AnomalyDINO
(train on good only) → T4 real lead-time logs + Ds ablation (RF vs XGB vs MLP)
→ T5 4-point grading (pixel-to-inch) + Jetson TensorRT demo → T6 thesis/paper
tables (mAP, AUROC, MAE/RMSE/R², ablations).

## 7. Reproduction experiment (NEXT ACTION at handoff)
`scripts/reproduce_v1.py`: Arm A stratified random 80/20 vs Arm B manifest;
same seeds/epochs; prints accuracy + per-class P/R/F1 + drop into docs/repro.json.
Colab T4 recipe (dataset zip + yolo11n.pt on Drive first):
```
pip install -q ultralytics scikit-learn
git clone https://github.com/labib-ux/FYDP.git
python3 scripts/reproduce_v1.py --dataset-root "/content/data/Fabric Defects Dataset" \
  --split data/split.json --base-weights /content/drive/MyDrive/fydp/yolo11n.pt \
  --epochs 50 --link-mode copy --work /content/repro --out <drive>/repro.json
```
(`--link-mode copy` required: Drive FUSE rejects symlinks.) `--eval-only` mode
exists if best.pt ever appears. Expected: positive accuracy drop (old claim inflated).

## 8. Conventions established this session
- Tell-before-do for repo changes; user runs `push` and GPU/Colab steps.
- `src/v1_baseline/` frozen; v2 code fresh. Manifests (`split.json`,
  `quarantine.json`, `datasheet.json`) ARE committed as audit proof.
- `scratch/`, `*.bmp`, `*.pt`, `runs/`, raw data stay out of git.
- Scripts must run on bare stdlib where possible; heavy deps guarded with
  clear pip messages; every script compile-checked before commit.

## 9. MCP/Colab note (diagnosed, not solved here)
colab-mcp server binary healthy (handshake OK, `ColabMCP 2.14.5`, log shows
`enabling session proxy tools`); this prior session had zero live MCP servers,
so Colab was unreachable from it. If tools still don't appear in the new
session: restart the client after config load, confirm server connected in its
MCP panel, then pair the browser Colab notebook (proxy tools appear on pairing).

## 10. Verify-first commands for the new agent
```
cd /Users/nafizimtiazlabib/FYDP/FYDP
git log --oneline -9 && git status -sb
python3 src/metrics.py --self-test
python3 scripts/resplit_by_roll.py --root "/Users/nafizimtiazlabib/Downloads/Fabric Defects Dataset" --seed 42 --quarantine data/quarantine.json --out /tmp/split_check.json
```
Deterministic manifest: re-run must print `images=2549 ... train=2081 test=468`.
