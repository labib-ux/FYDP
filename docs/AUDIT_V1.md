# v1 audit — baseline vendored from oyon79 repo (Sep 2026)

Source: `https://github.com/oyon79/Fabric-Defect-Detection_And_Lead-Time-Prediction`
Vendored byte-for-byte into `src/v1_baseline/` (config, defect_detection,
metadata_bridge, lead_time_predictor, integration). Weights + dataset live
on Google Drive only, not in git. Do not edit `v1_baseline/` — v2 work goes
in `src/` fresh modules.

## What v1 does (verified from code)
- YOLO **classifier** (`result.probs`, top-1) per frame, 6 classes
  (`defect_detection.py:334-348`). One label per frame, no multi-defect.
- Area is **not measured**: `DefectAreaEstimator` maps class → base size
  (hole 0.06 … lines 0.20) scaled by confidence (`defect_detection.py:141-192`),
  then draws a **centered square** bbox (`defect_detection.py:370-390`).
  Ds is therefore a function of (predicted class, confidence), not of pixels.
- `Ds = sum(bbox)/frame`, clamped [0,1], rolling window 10
  (`metadata_bridge.py:26-76`).
- Lead time labels from fixed formula
  `base=(qty/speed)*0.1`, `×(1+Ds*2)` + N(0,0.5) noise, clipped ≥0.5h
  (`lead_time_predictor.py:131-148`); RF(100 trees) trained on 1000 such rows.
- `LiveStreamProcessor` retrains predictor on synthetic data at init,
  loads `best.pt` at detector init (crashes without weights, even for the
  synthetic-frame demo path) (`integration.py:66-75,341`).

## Issues, ranked
### Blockers (must fix for final-year defence)
1. **Fake localization.** Bbox is centered by construction, never at the
   defect. Any IoU/mAP-seg eval of v1 will be ~0. Ds has ≤6 discrete values.
   Fix: YOLOv11-seg / OBB, pixel-true Ds (Track 2).
2. **Circular lead-time labels.** RF learns the formula it was generated
   from; "92% MAE gain vs mean baseline" is vacuous. Noise σ=0.5 dominates
   small orders; clip at 0.5h distorts the low end. Fix: factory logs +
   time-split eval, report RF vs XGBoost vs MLP with Ds-ablation (Track 4).
3. **Train/test integrity.** Report Fig 3.3 vs 3.4 look identical; dataset
   size/source/split-by-roll undocumented. Fix: re-split by roll, publish
   datasheet with per-class counts (Track 1).

### Major
4. **Preprocessing applied at inference by default** (`detect(...,
   apply_preprocessing=True)`): adds random noise/blur/darkening to real
   frames, non-deterministic per call (random angle/gamma). Meant as train
   augmentation, harmful at test. Default must become False; keep sim only
   for robustness tests.
5. **Disambiguation on degraded frame** with magic thresholds
   (max≥80/std<3 etc., `defect_detection.py:29-66`): tuned to one dataset,
   applied to the preprocessed frame while area uses the original — inconsistent.
6. **Fragile class map** (`FABRIC_CLASSES` index→name): breaks if training
   folder order changes. Save `class_names` from training run instead.
7. **`update()` refits from scratch** — not online learning despite docstring.
8. **Single defect per frame**: overlapping/multi-defect lines + stains
   collapse to one label; Ds undercounts by design.

### Minor
9. Display defaults True (fails headless); machine-specific fallback paths
   (`~/Desktop/sample_images`); hardcoded `CLASSIFIER_PATH`.
10. No seeds for torch/ultralytics, no CV, no mAP/P-R/F1 per class, no FPS
    table, no Jetson validation despite edge claims.

## Strengths to keep
- Clean module split (detect → bridge → predict → integrate) and central
  `config.py`; rolling-window Ds smoothing; honest limitations section in
  report; closed-loop framing matches real MES need (DHU/rework use-case).

## Track 1 exit checklist (before any v2 training)
- [ ] Dataset inventory: counts per class, camera, res, knit vs woven, annotator
- [ ] Re-split by roll; prove train ∩ test = ∅ (hash list in `data/split.json`)
- [ ] External test-only copies: Isl-Knit + FabricSpotDefect (never train)
- [ ] Metric harness: mAP50, mAP50-95, P/R/F1 per class, mask-IoU for Ds
- [ ] Reproduce v1 numbers on old split, then show drop on disjoint split
