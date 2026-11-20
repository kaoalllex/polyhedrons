---
id: E-261119-02
title: Symmetric nine-face census - C3 3+3+3 and C2 4 x 2 + 1 maps by lifting the C3 exact cover, then per-map symmetric formulas
date: 2026-11-19
status: running
direction: [DR19, DR18]
origin: [I-261030-18, I-261119-01, I-261118-02, E-261103-01, E-261118-03]
tests: [H-261101-07]
produces: []
preregistered: true
---

> Planned, week item 2, the main investment (`reviews/strategy-review-2026-11-19.md` §1, owner-approved 2026-11-19;
> reconciled with the Codex second opinion, `reviews/strategy-review-2026-11-19-reconcile.md`, owner-approved the same
> day), explore, jump 2. Scores T D F G R: 2 2 1 2 2 | budget: stage A one session, <= 1 core-h shared by C3 and C2;
> stage B <= 10 core-h owner run, 10 shards. Before any compute: `PLAN.md` (skill `experiment-start`) with its unit tests
> run in that commit. No proofs.

## Goal

Stage A: generalise `E-261103-01/c3_crosscheck.py` to (9, 4) (three pair orbits, 0 or 3 fixed triangles, pair
multiplicity <= 3, 18 C3 extra-edge demand classes (reconcile check); the code asserts <= 2 now; deadline inside gluing;
covers, gluings, codes and time per stratum and the fixed-cell count b per map recorded), plus a C2 analogue with one
fixed face. Controls: (9, 3) gives exactly the census's 8 admissible free-C3 classes and its fixed-face involution
classes; (7, 1) gives Szilassi's map; free C2 at (8, 3) gives both known maps. Gate per family in a shared 1 core-h, C3
first: a complete family that passes its controls goes to stage B even if the other times out. Stage B, after one map
per multiplicity stratum is priced: kissat, cap 600 s; C3 by omsat's C3 clauses in the standard chart (as for the 8 C3
(9, 3) maps), C2 4 x 2 + 1 plane-only in a moved chart (the E-261118-03 runner, `build_sym` gauge, the action inherited
on canonical darts). Rung: both known maps SAT on the free-C2 (8, 3) list, every (9, 3) symmetric formula UNSAT (agrees
with 3d); controls: generic moved nine-plane signs pinned on the symmetry + gauge subformula, a realizable nine-face
fixed-face positive, a wrong pairing, a wrong action. E-261119-01's U1 is compared with this rung only on common
decoded maps.

## Stage A results (2026-11-20)

Owner launch 2026-11-20 10:01Z on `1b80fe52` (after the 0 s defective launch, PLAN amendment 1): unit tests OK in shard 0,
then all 807 units complete (the unit list has 807, not the 808 that amendment 1 states) in 88 s wall, 0.24 core-h by the
manifests (655.8 core-s inside units); with the defective launch 0.30 core-h of the 1 core-h cap. Gate: C3 and C2 both pass,
every control exact (`results/stageA/summary-brief.json`). The lists: STATUS 3be. Prediction vs outcome: P1-P4 held; P3
(C2 completes, 0.45) held with room (617 core-s); P5 held as maps only (the free-C2 (8, 3) list has 788 classes besides the
two known ones; maps are not polyhedra). Session re-check: every (9, 4) and free-C2 (8, 3) class rebuilt from its
canonical code passes `review.check`, `census.admissible` and re-canonicalises to itself; per stratum: C3 b0 m222 76,
b0 m32 10, b3 m222 27, b3 m32 5; C2 m22222 6152, m32222 2224, m222222 1848, m3222 1524, m3322 344, m322222 176, m33222 176.
Raw claims markers, the full `summary.json` (25 MB, rebuilt by `symcensus.py summary results/stageA`) and the defective
launch are in `../polyhedrons-data/<same path>`. Label: EXACT computation, coverage PROVED-1; no realization is claimed.

For stage B: at the row's 10 core-h the C2 list leaves under 3 s per map (12444 maps), against a 600 s cap; the C3 list
(118) fits. Pricing one map per stratum (four C3, seven C2) decides the stage-B amendment; a C2 subset or a larger
budget goes to the owner.

## Next

SAT -> bridge, `--all-pairs` nine faces, `candidate-check`, escalate. A complete family all UNSAT-SOLVER -> genus 5
(E = 51) for that family, priced the same way. Neither family advances -> E-261117-04 (P6). A control failure -> repair. Lab: Opus, high / Codex gpt-6-astra, high.
