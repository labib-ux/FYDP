# 08 — Colab v1 Repro Run (live status; update after every session)

## Objective
Reproduce the v1 98% claim twice (Arm A naive stratified-random 80/20 vs
Arm B honest manifest split), same seeds/epochs, on a Colab T4 GPU.
Prove the old number was inflated: expect positive `accuracy_drop`.

## Canonical command (HANDOFF §7, amended — see deviations)
```
pip install -q ultralytics scikit-learn
git clone https://github.com/labib-ux/FYDP.git /content/FYDP
python3 /content/FYDP/scripts/reproduce_v1.py \
  --dataset-root "/content/data/Fabric Defects Dataset" \
  --split /content/FYDP/data/split.json \
  --base-weights /content/drive/MyDrive/fydp/yolo11n-cls.pt \
  --epochs 50 --link-mode copy \
  --work /content/repro --out /content/drive/MyDrive/fydp/repro.json
```
`--link-mode copy` is mandatory (Drive FUSE rejects symlinks).

## Staging spec (fresh VM, ~10 min)
1. T4 GPU runtime (`Runtime → Change runtime type`); verify:
   `nvidia-smi` → Tesla T4, `torch.cuda.is_available()` True.
2. Mount Drive (`drive.mount`, needs interactive auth in browser).
3. Unzip `MyDrive/Fabric Defects Dataset.zip` (2.0 GB) → `/content/data/`
   (yields `/content/data/Fabric Defects Dataset/` + `__MACOSX/`).
4. Weights in `MyDrive/fydp/`: `yolo11n.pt` (5.4 MB,
   sha256 `0ebbc80d…7644ee1`, = official ultralytics release, = local
   `~/Downloads/yolo11n.pt`) and `yolo11n-cls.pt` (5.6 MB,
   sha256 `c62d41bf…82502bd7`).
5. Clone repo to `/content/FYDP` (must be ≥ `f274e73`).
6. Launch DETACHED so kernel interrupts can't kill training:
   `setsid nohup python3 … > /content/repro_run.log 2>&1 < /dev/null &`
   (plain `nohup … &` holds the kernel pipe; never put `sleep` in the
   launch cell — MCP calls time out past ~60 s).

## Known deviations from HANDOFF §7 (do NOT "fix" without owner)
- D1 — `--base-weights` uses **`yolo11n-cls.pt`, not `yolo11n.pt`**.
  `yolo11n.pt` is a *detection* model; the script materializes a
  classification folder dataset → `RuntimeError: No YAML file found`.
  Verified `YOLO('yolo11n-cls.pt').task == 'classify'`. v1's own
  `config.py` says `yolo11n.pt`, but that cannot train this script.
- D2 — `--split` passed as absolute `/content/FYDP/data/split.json`
  (CWD-independent; equivalent to `data/split.json` from `/content/FYDP`).

## Run history
- Attempt 1 (spec weights `yolo11n.pt`): failed fast, detection/classification
  task mismatch (log tail in session notes). Nothing trained.
- Attempt 2 (`-cls`, plain `nohup &`): trained, killed by KeyboardInterrupt
  (kernel interrupt propagated to child). `/content/repro` reached 3.7 GB.
- Attempt 3 (`-cls`, `setsid`-detached, PID 15763): naive arm reached
  **epoch 26/50**, then **Colab free T4 quota exhausted** → runtime reclaimed.
  `repro.json` never written (script saves only at end). Partial weights lost
  (ephemeral disk). Drive artifacts intact (zip + both weights).

## Current state (2026-09-18/19)
- Colab runtime: dead (quota). MCP Colab cell tools withdrawn from agent
  session; re-pair + restage required before any new run.
- Local repo: clean, `main` = `origin/main` (`457e52a`).
- Quota typically resets ~24 h. Alternative: Kaggle free GPU (30 h/week, needs
  2 GB dataset upload) or local M1 overnight run (dataset already in
  `~/Downloads`; needs torch-MPS + ultralytics venv).

## Resume procedure (when GPU returns)
1. Fresh pair + staging spec above.
2. Add Drive checkpoint sync alongside training (10-min `cp` loop of
   `/content/repro/*/train*/weights/*.pt` → Drive) so the next interruption
   costs minutes, not hours. No repo changes needed.
3. Relaunch canonical command; poll log with short cells (no `sleep` > 45 s).
4. On completion: verify `MyDrive/fydp/repro.json`, report naive-vs-honest
   accuracy table + per-class P/R/F1 + `accuracy_drop`. Do NOT start Track 2
   (`src/v1_baseline/` untouched) until owner confirms the numbers.
