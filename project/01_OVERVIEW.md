# 01 — Overview

## Project
Final Year Design Project (vision + image processing), team of 5–6, 1 year of
access to good GPUs. Host university: UIU (Bangladesh) — local knit/dyeing
industry access is a core asset (see `05_DATA_STRATEGY.md`).

## Continuation of
ML course project (UIU, Jun 2026): "Unified Fabric Defect Detection & Lead
Time Prediction" — YOLO classifier + Defect Density Score (Ds) + RandomForest
lead-time predictor. Course report + slides exist in the owner's Downloads.
Source repo (read-only reference):
`https://github.com/oyon79/Fabric-Defect-Detection_And_Lead-Time-Prediction`
(code only; weights + dataset on Google Drive).

## Work repo (all work happens here)
- GitHub: `https://github.com/labib-ux/FYDP.git`
- Local clone: `/Users/nafizimtiazlabib/FYDP/FYDP`
- Dataset (stays out of git):
  `/Users/nafizimtiazlabib/Downloads/Fabric Defects Dataset` (2.0 GB, 2578 imgs)
- Weights on disk: `/Users/nafizimtiazlabib/Downloads/yolo11n.pt` only.

## v1 recap (what we have)
- YOLO classifier, 6 classes: defect free (1505), stain (398), hole (281),
  lines (157), horizontal (136), Vertical (101).
- `Ds = sum(bbox areas) / frame area`, rolling window 10.
- RandomForest on `[machine_speed, order_qty, Ds]`, trained on 1000 synthetic rows.
- Reported 98% type accuracy, "92% MAE gain" vs static baseline.
- **Audit verdict (see `../docs/AUDIT_V1.md`):** fake localization (centered
  square bbox from confidence, never at the defect), circular lead-time labels
  (RF learns its own generating formula), undocumented split with evidence of
  train/test duplication. The 98% number is void.

## v2 goal (what we will do)
1. Dataset v2: roll-disjoint manifest + quarantine + external test-only sets.
2. Detector v2: YOLOv11-seg + OBB, pixel-true mask-Ds, fix Horizontal↔Hole confusion.
3. Anomaly branch: PatchCore / AnomalyDINO on defect-free fabric + router policy.
4. Real planning model: factory logs + time-split eval, Ds-ablation (RF vs XGB vs MLP).
5. Auto 4-point grading (ASTM D5430, pixel→inch) + Jetson TensorRT edge demo.
6. Thesis + paper tables (mAP, AUROC, MAE/RMSE/R², ablations, CIs everywhere).

## Current state (Sep 2026)
Track 1 audit done: `data/split.json` (2549 imgs after 17 dupe removals,
train 2081 / test 468, overlap 0), 12-file quarantine
(`data/quarantine.json`), deterministic re-split verified. v1 reproduction
(naive-vs-honest 50-epoch) in progress on Colab T4.
