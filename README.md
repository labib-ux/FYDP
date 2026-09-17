# Unified Fabric Defect Detection & Lead Time Prediction — FYDP v2

Final Year Design Project (vision + image processing).
Continuation of ML course project `oyon79/Fabric-Defect-Detection_And_Lead-Time-Prediction` (YOLO classifier + Ds + RandomForest).

## v1 recap (what we have)
- YOLO classifier, 6 classes: defect-free, hole, horizontal, vertical, lines, stain
- `Ds = sum(bbox areas) / frame area`, rolling window 10
- RandomForest on `[machine_speed, order_qty, Ds]` trained on 1000 synthetic samples
- Reported 98% type accuracy, 92% MAE gain vs static baseline (needs hardening, see docs)

## v2 goal (what we will do)
1. Dataset v2: disjoint rolls + Isl-Knit / FabricSpotDefect external tests
2. Detector v2: YOLOv11-seg + RT-DETR baselines, mask-Ds (not bbox-Ds), fix Horizontal↔Hole confusion
3. Anomaly branch: PatchCore / AnomalyDINO trained only on good fabric for unseen defects
4. Real planning model: replace synthetic formula with factory logs (time-split eval)
5. 4-point grading + Jetson edge demo with TensorRT
6. Thesis + paper tables (mAP, AUROC, MAE/RMSE/R2, ablations)

## Repo layout
```
src/          # detector, bridge, predictor, integration (to be ported from v1)
configs/      # training hyperparams
data/         # NOT committed, see data/README.md
notebooks/    # eval + figures
docs/         # UPGRADE_PLAN.md + audit notes
```

## Setup
```bash
pip install -r requirements.txt
```

## Workflow
- `main` = stable, feature branches per track (`track1-dataset`, `track2-detector`, ...)
- No `*.pt`, no datasets in git. Use releases/drive for weights.
- See `docs/UPGRADE_PLAN.md` for the 6-track task split.
