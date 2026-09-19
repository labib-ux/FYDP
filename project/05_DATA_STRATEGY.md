# 05 — Data Strategy (critical path)

Factory logs are the #1 risk. Pursue rungs in order; record the rung in the
thesis. Minimal schema: order_id, qty, machine_speed, defect_summary,
actual_hours.

1. **Real order logs + rework/DHU records** from a partner factory (alumni,
   BUTEX / Isl-Knit author contacts — local and published).
2. **Paired dataset**: their defect counts + our vision-measured Ds on the
   same rolls (creating this pairing is itself a contribution).
3. **Calibrated queuing simulation** (documented parameters from measured Ds
   distributions) — labelled synthetic, validates planning *machinery* only,
   never accuracy claims. This is the line v1 crossed; we don't.

Never: generate labels from the formula under test (circular); train on
external test-only sets; quote the void 98% as ours.
