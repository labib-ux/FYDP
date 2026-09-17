# FYDP v2 upgrade plan (6 tracks)

From v1 audit (ML course report, June 2026):
- Fix train/test leakage (Fig 3.3 vs 3.4 identical), add mAP50/mAP50-95/P/R/F1/IoU
- Replace bbox-Ds with mask-Ds (YOLOv11-seg), fix Horizontal↔Hole 7-8% confusion
- Replace synthetic `Lead = Qty/Speed*(1+2*Ds)` loop with factory logs + time-split eval
- Add PatchCore/AnomalyDINO branch (train on good only)
- Add 4-point grading (pixel-to-inch) + Jetson TensorRT demo
- Baselines: YOLOv8 vs v11 vs Fab-ASLKS/Fab-ME vs RT-DETR; RF vs XGBoost vs MLP

Tracks:
1. Dataset v2 (disjoint rolls, 2 fabrics, external tests)
2. Detector v2 + true Ds
3. Anomaly branch
4. Real planning model
5. 4-point + edge
6. Thesis/paper tables + ablations

Start: audit + re-split. Do not train v2 until split is disjoint.
