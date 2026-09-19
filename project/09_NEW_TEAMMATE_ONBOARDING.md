# 09 — New Teammate Start Here (friend + fresh AI agent)

You got only this repo. That's enough. This page tells you (the human) what
to do, and gives you the exact message to send your AI agent.

## 0. What you need before starting (~15 min)
- [ ] This repo cloned: `git clone https://github.com/labib-ux/FYDP.git`
- [ ] The dataset zip (2.0 GB) + `yolo11n.pt` — get the Drive share link from
      the repo owner and put them in your Google Drive as `MyDrive/fydp/`
      (weights) + `MyDrive/Fabric Defects Dataset.zip` (dataset).
      (`yolo11n-cls.pt` too if shared, else the agent downloads it.)
- [ ] A Google account with Colab access (free tier OK; T4 GPU quota needed —
      if exhausted, see `08_COLAB_REPRO_STATUS.md`, "Current state").
- [ ] Read `project/README.md` (5 min) so the plan makes sense.

## 1. Your job vs the agent's job (actor split)
- **Agent does:** repo verification, Colab pairing, staging commands,
  launching/polling training, reading logs, reporting numbers, writing docs.
- **YOU do (agent cannot):** open the Colab notebook in YOUR browser and keep
  the tab open; `Runtime → Change runtime type → T4 GPU`; run the
  `drive.mount` cell and complete Google auth when asked; `git push`;
  tell the agent when quota/auth steps are done in the browser.

## 2. Exact first message to send your AI agent (copy-paste)
```
Read project/README.md, then project/07_AGENT_RUNBOOK.md and
project/08_COLAB_REPRO_STATUS.md in the repo labib-ux/FYDP
(local clone: <YOUR PATH>/FYDP).

Context: I'm <NAME>, a new teammate. I have the dataset zip + yolo11n.pt
in my Google Drive and a Colab notebook open in my browser.

Job: run the v1 reproduction experiment on my Colab T4 exactly per
08_COLAB_REPRO_STATUS.md (canonical command + staging spec, deviations D1/D2
apply). First run the §10 verify commands from 07_AGENT_RUNBOOK.md adapted
to my machine paths, then pair my Colab session, then stage and train.

Rules: tell me every step you need ME to click in the browser (T4 runtime,
Drive auth) instead of guessing; if anything fails, say exactly which step
(verify / pairing / staging / training). Don't start Track 2 or touch
src/v1_baseline/.
```

## 3. What "done" looks like
- `repro.json` saved to your Drive (`MyDrive/fydp/repro.json`).
- Agent reports: naive-vs-honest accuracy table, per-class P/R/F1,
  `accuracy_drop` number.
- You forward `repro.json` (or its contents) to the repo owner.

## 4. If it breaks
- T4 quota exhausted → wait ~24 h, or use Kaggle free GPU, or ask the owner
  about the local-M1 option (see 08, "Current state").
- Any other failure → paste the agent's exact failure report to the owner.
  Don't delete the Colab notebook — its cells are the debug log.
