# docs/report/ — FYDP submitted report

## What lives here
- `FYDP_REPORT.md` — the full report, regenerated from the submitted PDF
  (`262_034_Report.pdf`, 40pp, 27 September 2026). This file is the source of
  truth; it was reconciled against the PDF, not the other way round.
- `figures/*.mmd` — one standalone Mermaid source per figure:
  - `fig31_context.mmd` — Figure 3.1 context diagram
  - `fig32_system.mmd` — Figure 3.2 proposed system diagram
  - `fig33_workflow.mmd` — Figure 3.5 system workflow
  - `fig34_bridge.mmd` — Figure 3.6 metadata bridge
  - `fig35_pipeline.mmd` — Figure 3.7 ML pipeline
  - `fig36_fourpoint.mmd` — Figure 3.8 four-point grading
  - `fig39_gantt.mmd` — Figure 3.9 project task allocation Gantt

## Instructions for any AI agent asked for the figures
1. Hand the user the matching `figures/*.mmd` file content (or the embedded block
   from `FYDP_REPORT.md`) for the figure number they ask about.
2. Tell them to paste it into the Mermaid Live Editor (https://mermaid.live).
3. Export steps: top bar Theme → Base, then Export → PNG at 2x–3x scale with a
   white background (print-ready). Save as `figNN_name.png` next to the sources.
4. For the Word/PDF submission, insert the exported PNGs as figures — pasting
   raw markdown into Word will NOT render diagrams.

## Notes
- Figure and table numbering follows the submitted PDF exactly. Chapter 3 uses
  Figures 3.1–3.9 (3.1 context, 3.2 system, 3.3 architectural, 3.4 use case,
  3.5 workflow, 3.6 metadata bridge, 3.7 ML pipeline, 3.8 four-point,
  3.9 Gantt). Do not renumber.
- Chapter 4 is intentionally empty in the submitted PDF — it carries the template
  note "Must be present in Final Report." Results are not yet written.
- `slides/FYDP-I_Defect-to-Delivery.pptx` is aligned to this report.
