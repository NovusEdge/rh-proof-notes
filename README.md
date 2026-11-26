# Notes on the Lean proof of the Riemann hypothesis

Measurements of the Lean source that Levent Alpöge released on 2026-11-20, and
of the shorter rewriting at [lsernau/grh-lean](https://github.com/lsernau/grh-lean),
plus an outline of the argument in [OUTLINE.md](OUTLINE.md).

This repository holds no Lean code from either project. The original archive
carries no licence; the short version is Apache 2.0.

## Build check

The compact edition builds. On 2026-11-26 the workflow in
`.github/workflows/verify.yml` fetched lsernau/grh-lean at commit `72fead1`,
ran `lake build` on `grh-compact` with Lean v4.35.0 and the pinned Mathlib,
and printed the axioms of the five theorems in `src/Main.lean`:

    'riemannHypothesis' depends on axioms: [propext, Classical.choice, Quot.sound]
    'riemannZeta_eq_zero_re' depends on axioms: [propext, Classical.choice, Quot.sound]
    'LFunction_ne_zero_of_half_lt_re' depends on axioms: [propext, Classical.choice, Quot.sound]
    'LFunction_eq_zero_re' depends on axioms: [propext, Classical.choice, Quot.sound]
    'LFunction_eq_zero_re_of_isPrimitive' depends on axioms: [propext, Classical.choice, Quot.sound]

The build took 2 hours 1 minute on a GitHub-hosted runner with 4 cores and
16 GB of memory, with no errors and no `sorry`. Run and full log:
<https://github.com/NovusEdge/rh-proof-notes/actions/runs/45873443122>

This shows that Lean accepts proofs of the stated theorems from its three
standard axioms. It does not show that a person has checked the mathematics,
and it is not the stricter Comparator replay that the proof's own README
describes. The readable edition and the original archive were not built here.

## Size and repetition

Measured on 2026-11-26 from source text, without building.

| | Original | Short, readable | Short, compact |
|---|---|---|---|
| Files | 175,187 | 803 | 796 |
| Lines | 17,374,215 | 477,124 | 112,854 |
| Code lines | 13,372,248 | 285,509 | 70,971 |
| Comment lines | 0 | 132,625 | 18,882 |
| Theorems and lemmas | 818,755 | 18,234 | 7,093 |
| 6-line blocks that repeat exactly | 4.5% | 0.1% | 0.0% |
| Same, with names and numerals erased | 6.5% | 0.1% | |
| Theorems never named again (lower bound) | 2.3% | 0.9% | |

Code lines exclude blanks, comments and `import`/`open`/`namespace` lines.

The original is large because it formalises whole theories, not because it
repeats itself. `Development/AbelianVarietyTheory` alone is 8,142,960 lines,
47% of the tree. The short version proves the same five theorems with 47 times
fewer code lines.

## Limits

- Repetition is textual. Two lemmas that state the same fact differently do
  not match.
- "Never named again" compares the last component of each theorem name
  against every token in the tree. Name collisions hide dead theorems, so the
  true figure is higher.
- Every file is imported by the final theorem, through umbrella imports. Which
  lemmas the proof uses needs a build.

## Reproduce

Each script streams one file at a time and holds only counters.

    python3 -I scripts/dry.py <srcDir> out
    for f in out.lines out.win; do
      LC_ALL=C sort -S 1G "$f" | uniq -c |
        awk '{t+=$1; if($1>1) x+=$1-1} END{printf "%.1f%% removable\n", 100*x/t}'
    done
    python3 -I scripts/reach.py <srcDir> out Main Statements   # then the same pipeline on out.nwin
    python3 -I scripts/unused.py <srcDir>

## Licence

MIT for the scripts and text here.
