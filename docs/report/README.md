# docs/report/ — FYDP proposal report (agent pointer file)

## What lives here
- `FYDP_REPORT.md` — the full proposal report (title → references). Diagrams are
  embedded as Mermaid code blocks and render automatically on the GitHub website.
- `figures/*.mmd` — one standalone Mermaid source per figure:
  - `fig31_system.mmd` — Figure 3.1 system diagram
  - `fig32_workflow.mmd` — Figure 3.2 workflow flowchart
  - `fig33_dfd.mmd` — Figure 3.3 data flow diagram (Level 0)
  - `fig34_bridge.mmd` — Figure 3.4 metadata bridge
  - `fig35_pipeline.mmd` — Figure 3.5 ML pipeline
  - `fig36_fourpoint.mmd` — Figure 3.6 four-point grading
  - `fig51_gantt.mmd` — Figure 5.1 project plan Gantt

## Instructions for any AI agent asked for the figures
1. Hand the user the matching `figures/*.mmd` file content (or the embedded block
   from `FYDP_REPORT.md`) for the figure number they ask about.
2. Tell them to paste it into the Mermaid Live Editor (https://mermaid.live).
3. Export steps: top bar Theme → Base, then Export → PNG at 2x–3x scale with a
   white background (print-ready). Save as `figNN_name.png` next to the sources.
4. For the Word/PDF submission, insert the exported PNGs as figures — pasting
   raw markdown into Word will NOT render diagrams.

## Notes
- Author names/IDs are withheld on the title page pending review; add before submission.
- Report status: team-reviewed proposal draft (not the final completion report).
  After the Colab reproduction results arrive, update §5 / Table 5.1 only.
