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

## Stage B (2026-11-20)

Amendment 2 (owner launch 12:12Z, 31 s wall, < 0.1 core-h; `results/stageB-*`): all controls pass on every shard. Rung:
the 32 (9, 3) symmetric classes UNSAT-SOLVER (agrees with 3d); Roest-Vigh's map SAT under 2 of its 3 free-C2 groups,
Mizhaev's SAT under its 1, all three realized, `--all-pairs` PASS. Pricing: 33 of 33 records UNSAT-SOLVER in <= 0.29 s
(12 C3, 21 C2f, all 11 strata; decided fraction 1.0 by 30 s everywhere). Added formula controls (`controls_b.py`,
`results/controls_b.json`): on every pricing record, generic symmetric planes pinned SAT 165 of 165, planes of a wrong
action UNSAT 165 of 165. Pass 1 (amendment 3; owner launch 2026-11-20 13:53Z, `results/stageB-pass1/`): 10 shards complete, 11 min wall
(649-663 s per shard, no gap), 1.83 core-h by the budget ledger (6598 core-s), against a projection of ~1.8. Every shard
passed the pinned f9 pair and the runner's controls (`CONTROLS-PASS`). All 12562 records UNSAT-SOLVER within the 30 s
cap, every one `completed`: C3 118 (max 0.46 s, 16.6 solver-s), C2f 12444 (max 0.63 s, 2079.9 solver-s), every stratum of
both lists; no SAT, no UNKNOWN, so no pass 2. Replication: the 33 pricing records, matched by canonical code, group and
generator, give the same status and formula hash. Prediction vs outcome: R1 (all decide within 30 s), R2 (no SAT), R3
(<= 3 core-h) held. Reading per the tree: in both families every uniform symmetric (9, 4) formula is UNSAT-SOLVER.
Stage B used < 2 of its 10 core-h. Caveat: one status across all 12562 records; it rests on controls of both signs at
formula level (`controls_b.py`), the (8, 3) rung (map-level SAT, standard chart) and the (7, 1) Szilassi chain (moved
chart, E-261118-03); no realizable nine-face map exists to serve as a map-level positive in the moved chart. Per-map
`result.json` files are in `../polyhedrons-data` (owner, 2026-11-20); git keeps each shard's `results.jsonl` (indexed by
`map_index` into `maps/pass1.json`, rebuilt by `stageb.py`). Label: UNSAT-SOLVER per exact formula (STATUS 3bf); no
negative claim.

## Next

Both families are all UNSAT-SOLVER at (9, 4), so per the tree: genus 5 (E = 51) for both, priced the same way (stage-A
census at (9, 5), then per-stratum pricing; an amendment before any run). SAT -> bridge, `--all-pairs` nine faces,
`candidate-check`, escalate. Neither family advances -> E-261117-04 (P6). A control failure -> repair. Lab: Opus, high / Codex gpt-6-astra, high.
