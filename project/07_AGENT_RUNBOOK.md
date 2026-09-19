# 07 — Agent Runbook (AI agents: obey this)

## Session start (do not skip)
```
cd /Users/nafizimtiazlabib/FYDP/FYDP
git pull
git log --oneline -9 && git status -sb
python3 src/metrics.py --self-test
python3 scripts/resplit_by_roll.py --root "/Users/nafizimtiazlabib/Downloads/Fabric Defects Dataset" --seed 42 --quarantine data/quarantine.json --out /tmp/split_check.json
```
Must print `images=2549 ... train=2081 test=468`. If not, stop and report.
Note: the resplit needs the EXTRACTED dataset folder. If only
`~/Downloads/Fabric Defects Dataset.zip` exists, unzip it first
(weights/dataset zips are never in git — see 09 §0; GitHub caps files at
100 MB). The committed `data/split.json` manifest is unaffected.

## Frozen / forbidden
- `src/v1_baseline/` — frozen audit reference. Never edit.
- No Track 2 training until the human confirms repro numbers.
- Never commit: `*.pt`, datasets, `scratch/`, `runs/`, `*.bmp`.
- Owner runs `git push` and all GPU/Colab steps unless they explicitly say otherwise.

## Conventions
- Tell-before-do for repo changes; feature branches per track.
- Manifests (`split.json`, `quarantine.json`, `datasheet.json`) ARE committed.
- stdlib-first scripts; heavy deps guarded with pip messages.
- Colab runs: T4 GPU, `--link-mode copy` (Drive rejects symlinks), save
  `repro.json` back to Drive, report naive-vs-honest table + per-class
  P/R/F1 + `accuracy_drop`.
- If Colab pairing/staging/training fails: report the exact failed step,
  never improvise around it.
