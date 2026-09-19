# 02 — Novelty & Literature (surveyed Sep 2026)

Rule: cite prior art, don't ignore it. Our contribution is the loop, the
measurement, and the factory data — NOT a new detector architecture.

## Claim-by-claim verdict

| Our claim | Prior art (exists) | Our defensible gap |
|---|---|---|
| YOLO detector for fabric defects | DCFE-YOLO (PLOS ONE 2025); Fab-ASLKS (2025, Tianchi SOTA 60.3 mAP50); SDLS-YOLOv10 (2025); UniDefectNet YOLOv12 (2026); RT-DETR on fabric: MSCA-RTDETR (Jan 2026), RT-DETR-FFD (2025); review YOLOv1→v11 for fabrics (Sensors 2025) | No architecture novelty. Claim *measurement*: pixel-true mask-Ds vs bbox-Ds, roll-disjoint split, published datasheet. Report Ds quality as a metric (mask-IoU, Ds error). |
| Automatic 4-point grading | Isl-Knit (Heliyon 2024, Bangladesh, YOLOv5 + four-point mapping, knit only, box-based) | Segmentation + OBB physical measurement per ASTM D5430, woven + knit, and an **agreement study vs human inspectors** (Cohen's κ — never reported). Extend them, cite them. |
| Anomaly branch (unseen defects) | AnomalyDINO (WACV 2025, training-free, MVTec/VisA only); PatchCore (general industrial) | First systematic few-shot anomaly study on knit + woven with a supervised→anomaly **routing policy**. The router is the contribution, not the backbone. |
| Lead-time prediction | Atik 2021 (textile company data, ML, no vision); flow-time ML (POM 2025); apparel digital twin (2023, simulation) | **Ds-ablation**: does vision-measured quality beat qty/speed-only planning under time-split eval on real logs? Needs both sides of the data — our factory access is the moat. |
| Edge demo | Edge-AI inspection trend (2025); commercial (Infiano Vision: 24 fps, 1 mm) | Not a paper — the **defence weapon**. Jetson + TensorRT + FPS/mAP table is mandatory. |
| Closed loop vision→planning | Only our own course repo (oyon79). Commercial does traceability, not planning feedback. | The framing is genuinely ours — make it the thesis title, defend with the Ds-ablation. |

## Key references to cite
- Isl-Knit: Heliyon 2024, 3375 imgs, 7 knit faults, Bangladesh knit dyeing industry, YOLOv5 + four-point.
- FabricSpotDefect: Mendeley Data 2024, 1014 imgs / 3288 spots.
- Tianchi fabric dataset, ZJU-Leaper (98k), TILDAv2, DPFD-DET — benchmark context.
- TSFabrics (2026, time-series circular-knitting) — motivates rolling-window Ds.
- ASTM D5430 — grading standard (4-pt penalties, 24 pts/100 m² typical pass).
- AnomalyDINO: WACV 2025. PatchCore: CVPR 2022.

## Strategic consequence
Tracks 2/3/5 = engineering + rigorous benchmarking (necessary, not novel).
Tracks 1-quirks (quarantine audit, datasheet), 4 (Ds-ablation on real logs),
and 6 (thesis tables) = where novelty lives. Put the best analyst on 4+6,
not on YOLO hyperparameters. Never chase a novel detector variant — the field
publishes one monthly.
