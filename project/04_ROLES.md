# 04 — Roles (team of 6)

| Role | Owner focus | Hands off to |
|---|---|---|
| P1 Data & Rigor Lead | Split integrity, datasheet, quarantine v2, external sets, eval harnesses. The defence's immune system. | P2 (clean splits), P3 (protocols) |
| P2 Detector Engineer | YOLOv11-seg + OBB training, mask-Ds, Horizontal↔Hole fix. | P5 (masks for grading), P6 (weights) |
| P3 Anomaly Engineer | PatchCore/AnomalyDINO branch + router policy + open-set test. | P6 (router integration) |
| P4 Planning Modeller | Factory data access (starts week 1), RF/XGB/MLP, time-split eval, Ds-ablation. | P6 (predictor API) |
| P5 Edge & Grading Engineer | Pixel→inch calibration, Auto-4pt module, Jetson TensorRT rig. | P6 (demo panels) |
| P6 Integration & Thesis Lead | Pipeline wiring, demo app, figures/tables, paper drafts. Holds the repo. | Everyone (reviews) |

Rules: one owner per track; cross-track changes via PR + review; P1 can veto
any training run that breaks the manifest gate; P6 resolves conflicts.
