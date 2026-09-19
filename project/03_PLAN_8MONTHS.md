# 03 — 8-Month Plan (Oct 2026 → May 2027)

Gates are hard: a phase's gate unmet = next phase doesn't start.

## Phase 0 — Repro & foundations (Month 1, in flight)
- Finish Colab T4 v1 repro (naive-vs-honest, `--link-mode copy`).
- Freeze honest manifest; publish `docs/datasheet.json`.
- P4 sends first factory-visit emails NOW (2–3 month lead time).
- Gate: repro numbers reported, `accuracy_drop > 0` documented.

## Phase 1 — Measurement upgrade (Months 2–3)
- P2: annotate 400–600 segmentation masks (hole/lines/horizontal first),
  train YOLOv11-seg; report mask-Ds vs bbox-Ds error.
- P1: Isl-Knit + FabricSpotDefect + Tianchi-sample as test-only externals
  (hash-verified, never trained on); review 152-file `lines/line_2018-10-10`
  batch (likely quarantine #2).
- P3: PatchCore baseline on defect-free frames.
- P5: pixel→inch calibration rig (checkerboard + known-width tape).
- Gate: mask-Ds error < bbox-Ds error on held-out roll.

## Phase 2 — The two hard novelties (Months 4–5)
- P4: real logs (300–500+ orders) → RF vs XGB vs MLP, with-Ds vs without-Ds,
  time-split eval. This table is the thesis climax.
- P5: Auto-4pt module (penalty points + roll pass/fail at 24 pts/100 m²) +
  human-agreement study (≥2 inspectors, ≥30 rolls, Cohen's κ).
- P3: router policy + open-set test (hold out one defect class; anomaly
  branch must catch what the classifier can't).
- Gate: significant Ds-ablation MAE gain on real data, or honest fallback
  per `05_DATA_STRATEGY.md`.

## Phase 3 — Edge + integration (Month 6)
- P5: Jetson TensorRT FP16 port, FPS/mAP-retention table.
- P6: live loop on one screen: camera → detections → Ds → grade + lead time.
- Gate: live demo ≥15 FPS, all four panels updating.

## Phase 4 — Thesis & paper (Months 7–8)
- Report structured around ablation tables, not the detector.
- Paper 1 (systems/loop): Heliyon (Isl-Knit precedent), Sensors, or ICCA.
- Paper 2 (Auto-4pt agreement): bonus, not a dependency.
- Gate: thesis PDF + defence slides + demo video archived.
