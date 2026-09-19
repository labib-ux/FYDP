# Full Project Brief — start here (human or AI agent)

Final Year Design Project (vision + image processing), team of 5–6, ~8 months
(Oct 2026 → May 2027). Continuation of the ML course project (UIU, Jun 2026):
"Unified Fabric Defect Detection & Lead Time Prediction".

## Thesis in one sentence

> Nobody has built and validated the full loop — camera → true defect
> measurement → 4-point roll grade → lead-time prediction from real factory
> data → edge deployment — with honest, leakage-free evaluation. Every paper
> does one link; this thesis is the chain.

## Doc map

| File | What it tells you |
|---|---|
| `01_OVERVIEW.md` | Project, team, repos/paths, v1 recap, v2 goal |
| `02_NOVELTY_AND_LITERATURE.md` | What's already done (with citations), our gaps, strategy |
| `03_PLAN_8MONTHS.md` | Phases, gates, timeline Oct 2026 → May 2027 |
| `04_ROLES.md` | 6 roles, responsibilities, handoffs |
| `05_DATA_STRATEGY.md` | Factory-data critical path + honest fallback ladder |
| `06_DEFENCE_AND_PUBLICATION.md` | Pre-answered defence questions, paper venues |
| `07_AGENT_RUNBOOK.md` | How an AI agent must work in this repo (read first) |
| `08_COLAB_REPRO_STATUS.md` | Live Colab v1-repro state: staging spec, deviations, run history |

## Related repo docs (source of truth for details)

- `../docs/HANDOFF.md` — session context, verify-first commands (§10)
- `../docs/AUDIT_V1.md` — v1 audit: blockers with file:line refs
- `../docs/TRACK1.md` — Track 1 runbook (dataset audit)
- `../docs/UPGRADE_PLAN.md` — original 6-track split
- `../data/split.json` + `../data/quarantine.json` — committed audit proof

## Non-negotiable rules (see `07_AGENT_RUNBOOK.md`)

1. `src/v1_baseline/` is frozen (v1 audit reference, do not edit).
2. Nothing trains until the manifest gate passes (Track 1 exit checklist).
3. No `*.pt`, datasets, or `scratch/` outputs in git.
4. Every results table carries confidence intervals; no bare point estimates.
5. The v1 98% number is void (leakage proven by us) — never quote it as ours.
