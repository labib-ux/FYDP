# data/ — not committed (see .gitignore)

Put datasets here locally, never `git add` them.

Expected layout (v2):
```
data/
  pilot/        # v1 6-class set (disjoint rolls after re-split)
  factory/      # new 2-3k images, 2 fabrics min
  external/     # Isl-Knit + FabricSpotDefect test-only copies
  logs/         # factory lead-time CSVs (qty, speed, Ds/DHU, hours)
```

Split rule: by roll/fabric, never random crops. Train rolls != Test rolls.
Weights (`*.pt`) also stay out of git — use Drive/releases.
