---
id: E-261119-02
title: Symmetric nine-face census - C3 3+3+3 and C2 4 x 2 + 1 maps by lifting the C3 exact cover, then per-map symmetric formulas
date: 2026-11-19
status: done
concluded: 2026-11-22
verdict: SYMMETRIC-ROUTE-ENDS-AT-GENUS-4-UNSAT-SOLVER
direction: [DR19, DR18]
origin: [I-261030-18, I-261119-01, I-261118-02, E-261103-01, E-261118-03]
tests: []
produces: []
preregistered: true
---

> Concluded 2026-11-22 ([CONCLUSION.md](CONCLUSION.md)): the symmetric route ends at genus 4; the random 10 % of the C2
> (9, 5) list is 97830 of 97830 UNSAT-SOLVER (14.32 core-h); formula scope, planning only.

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

## Genus 5 (amendment 4, 2026-11-20)

C3 3+3+3 at (9, 5), stage A5c3, session run on `8b5bc10e` (10 shards, 13 s wall, ~0.04 core-h; 7.4 core-s inside units):
unit tests OK, the C3 (9, 3) control exact (8 classes), 83 demand classes = the Burnside count, all 498 units complete,
**no exact cover in any unit, so no map** (`results/stageA5c3/summary-brief.json`). Gate passes; the list is empty (G2
held). Consistent with a standard argument (PROVED-1): b = 1 is forced (34 - b = 0 mod 3), and b counts the fixed points
of the rotation on the surface (it fixes no vertex, and an order-3 map cannot fix an edge), but the rotation numbers at
the fixed points of an orientation-preserving Z3 action sum to 0 mod 3, so exactly one fixed point is impossible. Label:
EXACT computation, coverage PROVED-1: no admissible C3 3+3+3 (9, 5) map, so stage B is void for C3 at genus 5. The
claim markers and the full `summary.json` are in `../polyhedrons-data/<same path>`. The C2 4 x 2 + 1 census (A5c2) is the
owner night of amendment 4.

C2 4 x 2 + 1 at (9, 5), stage A5c2, owner launch on `cc0cdac3` (10 shards; the first launch, 2026-11-21 09:06Z, stopped
after 41.6 min with 2586 units recorded, the relaunch at 20:56Z claimed the remaining 9826 in 27.7 min; 12412 claims =
12412 records, no unit repeated or lost; every manifest exit 0; 11.56 core-h shard wall, 11.47 core-h inside units, plus
the ~0.85 core-h pilots: ~12.4 of the 40 core-h cap). Unit tests OK; the four C2 controls hold ((9, 3) 24 classes and
(8, 2) 2 equal the census, (7, 1) is Szilassi's map, (8, 3) holds both known maps among its 790 classes, as in stage A);
12288 demand classes = the Burnside count; every action checks; all 12288 units complete. **978228 admissible C2 4 x 2 + 1
(9, 5) map classes** in 12 of the 16 multiplicity strata (the four with four or more multiplicity-3 pairs have no cover);
per-stratum counts in `results/stageA5c2/summary-brief.json`. Gate passes (G1, G3, G4 held). Label: EXACT computation,
coverage PROVED-1, maps only. The per-unit records (1.4 GB, the stage-B input) are in `../polyhedrons-data/<same path>`,
SHA-256 in `results/stageA5c2/SHA256SUMS`. The full `summary.json` (2.2 GB, derived; peak 21 GB RSS, 109 s) and the claim
markers were deleted (owner, 2026-11-22); its hash stays in `SHA256SUMS` for the record. Since amendment 5 `symcensus.py
summary` streams the records and writes only the brief (rebuilt from the data copy: equal to the committed one, 85 s,
0.75 GB RSS).

## Stage B at genus 5: pricing (amendment 5, 2026-11-22)

Session run on `813c75dc` (`STAGE=B5`, 10 shards, 24 s wall, < 0.03 core-h; `results/stageB5-*`). Every shard's pilot and
pinned f9 controls pass. Lean replication (`queue_pricing_lean.json`, the (9, 4) pricing in the lean mode): 53 of 53
units equal the committed `results/stageB-pricing` records in status, `cnf_sha256`, `formula_sha256`, variables and
clauses; no folder is left for the 33 UNSAT-SOLVER records, the 20 controls keep theirs (S2 held). Formula controls on the
36 (9, 5) records (`results/controls_b_9_5.json`): 180 of 180 symmetric pinned SAT, 180 of 180 wrong-action UNSAT, 36 of
36 unpinned SAT, PASS (S1 held). Pricing (`maps/pricing_9_5.json`, 3 maps in each of the 12 strata, drawn from the
hash-checked data copy): **36 of 36 UNSAT-SOLVER**, max 0.23 s, mean 0.13 s (9.5k variables, 85k clauses; (9, 4): 0.29 s,
0.14 s); the fraction decided by 30, 60, 120 and 600 s is 1.0 in every stratum (S3 held, S4 holds so far). A lean unit
leaves ~1 KB (its `results.jsonl` and `progress.jsonl` lines). Label: UNSAT-SOLVER per exact formula; a price, not a
result about any stratum.

**Pass-1 price** (amendment 6 registers it with the owner's choice): 978228 records. The (9, 4) pass 1 ran at 0.525 core-s
per record under full load (6598 core-s, 12562 records) with the same solver time per record (0.13-0.14 s mean), so
~515k core-s = **~143 core-h, ~14.3 h wall on 10 shards** (two owner nights, resumable). Disk: ~1 GB of lean lines instead
of ~5M files and 20-45 GB. Tail: 36 of 36 decided gives a 95% upper bound of ~8% undecided; a cap of 5 s (20 x the priced
maximum) bounds that tail at ~110 core-h, 30 s at ~650 core-h, so the cap matters only if the bound is approached (at
(9, 4) all 12562 decided < 1 s). Work for amendment 6: one maps file would be ~0.63 GB (647 B per record) and the runner
loads it in every unit, so the maps go in ~100 chunk files and queues, built by streaming; `run_b.sh` invocations last at
most `--hours 2`, so the launch must resume until done.

**Amendment 6 checks** (session, on `1441f778`): (a) the lean (8, 3) rung (`STAGE=B5`, 11 s wall): 4 of 4 units repeat
the recorded `results/stageB-rung_8_3` statuses, `cnf_sha256`, `formula_sha256` and sizes; the 3 SAT units (Roest-Vigh
under 2 groups, Mizhaev) keep their whole folders (model, hinge stages, candidate) with `--all-pairs` PASS; the
UNSAT-SOLVER unit leaves no folder. (b) Smoke of `STAGE=B5p1` on chunk 0 (10 shards, 90 s, then stop; folders deleted):
1621 records UNSAT-SOLVER (max 0.79 s, mean 0.15 s), 1204 units per 60 s on 10 shards = 0.50 core-s per unit under
full load; the 6 units in flight at the stop are SKIPPED-STOP, keep their folders and rerun on the next start; the chunk
loop stops the shard on STOP-REQUESTED. Projection for the 10%: ~14 core-h, ~1.4 h wall; for the rest ~122 core-h.
Owner launch next: `launch.sh 261119-02 start` (`STAGE=B5p1`, chunks 0-9).

**Amendment 6 result** (owner launch 2026-11-22, `results/stageB5-pass1*`, audit `audit_pass1.py` -> `pass1_summary.json`):
chunks 0-9, 97830 of 97830 UNSAT-SOLVER within the 5 s cap (max 2.01 s, mean 0.158 s), controls pass on every
shard-chunk, 14.32 core-h, ~1.4 h wall; both power lines and the scope in CONCLUSION.

## Next

Both families are all UNSAT-SOLVER at (9, 4), so per the tree: genus 5 (E = 51) for both, priced the same way (stage-A
census at (9, 5), then per-stratum pricing; an amendment before any run). Amendment 4 (2026-11-20): C3 (9, 5) census
(498 units) in the session, C2 4 x 2 + 1 (9, 5) census (12288 units, priced ~12 core-h) as an owner night, 40 core-h cap.
C3 is void at (9, 5); the C2 list is complete (978228 classes). Amendment 5 priced it: 36 of 36 UNSAT-SOLVER in <= 0.23 s;
pass 1 ~143 core-h, ~14 h wall, ~1 GB lean. Next: the owner's choice (pass 1 as amendment 6, its cap and budget; no subset
by a guessed predictor without the owner), or first a lemma for the common (9, 4) obstruction (week item 4). SAT -> bridge, `--all-pairs` nine faces,
`candidate-check`, escalate. Neither family advances -> E-261117-04 (P6). A control failure -> repair. Lab: Opus, high / Codex gpt-6-astra, high.

Lead review 2026-11-22, final (owner-approved): the symmetric route ends at genus 4; P6 (E-261117-04) is the main line.
Amendment 6 (the random 10 % of (9, 5) pass 1) finished, 97830 of 97830 UNSAT-SOLVER (owner launch; untracked
`results/stageB5-pass1*`): its conclusion is week item 5; chunks 10-99 postponed by the owner. Amendment 7 (week item 2,
conditional on item 1): the free-C2 (8, 3) symmetric pass on maps item 1 leaves open, with all 862 free half-turns
derived from Aut+ (stage A kept the first action per unit, `symcensus.py`:344: the 822 records miss 40 actions on 23
maps, 14 on 13 maps not conjugate to a tested one; final review K1).

Closed 2026-11-22 (week item 5): see CONCLUSION.md; the C2 (9, 5) chunks 10-99 stay postponed by the owner.
