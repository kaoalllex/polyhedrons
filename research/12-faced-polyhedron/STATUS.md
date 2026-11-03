# Status ledger (single source of truth for "where are we")

As of **2026-11-03** (after night 7: E-261102-03 and E-261102-04, two engines scored on the ladder; E-261102-02 killed). Definitions, counters and evidence labels: `SPEC.md`. Evidence
details: `results.md`; chronology: `experiment-log.md`; what to do next: `ROADMAP.md`. Update this file in the
same commit as any result that changes a row. This file owns the verdicts and numbers; other files link here.

## 0. State in one paragraph

Combinatorics is finished (59 types). Impossibility side: no symmetric embedding (25/25 cases, CERTIFIED) and
no polyhedral immersion with a rotational symmetry (25/25 DRAT-checked, EXACT; mirrors and point reflections rest on the unreviewed lemma I-261101-16; CERTIFIED after E-261101-10); the asymmetric case is open. Construction side: the best exact object
has genus 3 (48 of 66 adjacent pairs; 94 realizations of 4 types, one of them on a map that is
combinatorially completable to a target map); **genus 4 was never reached** in five nights (ten engines); the nights-4/5 "pinned hemisphere margin" was a measurement artefact (E-261101-07), so the drift evidence about the class wall is void. Every Gauss-admissible normal set tried so far
is exactly UNSAT for the offsets (12,202 decisions in nights 4-5 alone, 0 SAT), but the positive control shows these decisions have low power. No candidate
for genus 6 exists; no type has been excluded. The question is open in both directions.

## 1. Foundations (rely on these)

| # | Statement | Level | Evidence | Caveat |
|---|---|---|---|---|
| FD1 | Face-plane formulation; open realization space; general position WLOG; integer certificates exist | PROVED-1 | `theory/mathematical-model.md` §1-§5; adversarial review ACCEPT (`verification/foundations-report.md`) | reviewers were AI agents (not independent, SPEC §5); PROVED after a human review |
| FD2 | Lemma 5.1: embedding = 176 forbidden-triple conditions on the chirotope of 12 planes + plane at infinity; `IN` predicate | PROVED-1 + EXACT tests | foundations report; 2.5 M predicate evaluations, 0 mismatches; Szilassi check in `verify_all` | same |
| FD3 | Exactly 59 types; automorphism groups (39 trivial) | EXACT | two independent enumerators; bijection with HackerPoet and Lutz lists; `verify_all` check 1 | known since Altshuler-Bokowski-Schuchert 1996 - replication, not discovery |
| FD4 | OM-SAT encoder (GP, triples, REFLEX1, POC, symmetry, normalisations) | EXACT tests | 0 mismatches vs exact geometry; cross-check with Track 4 (`results.md` Track 3) | single encoder; immersion families have no second implementation |
| FD5 | No symmetric embedding (all C2, C3 classes, hence all groups) | CERTIFIED | 25/25 UNSAT-VERIFIED, drat-trim (`experiments/E-261029-13-symmetric-embedding-certificates/results/sym/`) | encoding soundness rests on FD2 (PROVED-1); CNF + DRAT files published (release `state-2026-11-01`, `verification/certificates/symmetric_drat/`); reproduces Moki & Julio 2026 |
| FD6 | **No polyhedral immersion with a non-trivial rotational symmetry** (no global clauses); improper isometries (mirror, point reflection) excluded by the lemma I-261101-16, pending review | EXACT (DRAT-checked) for rotations; PROVED-1 for improper isometries; CERTIFIED after E-261101-10 | 25/25 UNSAT-VERIFIED (`experiments/E-261029-15-symmetric-immersion-certificates/results/symimm/`; CNF + DRAT in release `state-2026-11-01`); plan `proof-no-symmetric-immersion/` | the 25 instances encode det rho = eps = +1 (rotations only, `code/omsat_sym.py`); write-up, soundness proofs of REFLEX1/POC/SIMPLE/SYM, the improper-isometry lemma and a second encoder pending |
| FD7 | Gauss-map degree = 1 - g in the gauge, positive covering, >= 2g+1 saddles; local lemma; face-winding identity; parity theorem; handle decomposition D_{M+tau} = D_M + k_tau | PROVED-1 (classical fact in polyhedral form; the normal-only exact filter is ours) | `theory/theory-notes.md` 2.1 + PI addendum; held on 232/232 realizations (nights 4-5), tetrahedron, cube, Szilassi, Roest-Vigh | covering is checked on sampled directions only (SPEC §4) |
| FD8 | Fixed normals make every condition linear in the offsets; exact SMT decides a normal set in seconds-minutes | PROVED-1 + EXACT | `theory/theory-notes.md` 3.1; `fixed_normals_gauge.py`; positive controls SAT | UNSAT is scoped to that normal set, gauge and bounds |
| FD9 | Fixed-normal obstruction is cohomological (36 handle periods); face simplicity is an independent strong wall | NUMERICAL (~200 normal sets) | `reviews/fresh-eyes-review.md` 2.3; `period_defect.py`; night 2 | observation, not a theorem |
| FD10 | Exact verifiers (`ladder_exact`, `verify_solid`, `planes.check_embedding`) and the one-command suite | EXACT | caught 4 optimizer exploits; `verification/verify_all.py` (14 checks incl. the S0 negative control and the research graph, all PASS 2026-11-01) | rational rounding at 1e-9 (SPEC §3) |
| FD11 | All 1005 known near-misses (HackerPoet) fail the Gauss class (wrong degree, or failed covering for the 12 seeds with degree -5) and none is an immersion (every seed has >= 4 vertices with two reflex corners; min 4, median 14, max 22) | EXACT per instance | `results.md` PI sections; re-check of all 1005 in `reviews/strategy-review-2026-11-01.md` A.2 | the earlier wording ">= 7" held for the first 300 seeds only |

## 2. Exact witnesses (objects, re-checked by `verify_all`)

The ones shown on the site are listed in `witnesses/witnesses.json` (`witnesses/README.md`).

| Object | Target | Files | Value |
|---|---|---|---|
| Type-0 genus-3, 48/66 pairs, **combinatorially extendable** to type 0 (3 explicit handles) | S3 | `experiments/E-261030-03-genus-ladder-type0-genus3/results/type0_genus3_extendable*.json` (5 geometric variants of ONE map); `verification/certificates/type0_handle_completion/` | best positive result; candidate for a referee-style dossier (`ROADMAP.md` E-261101-03) |
| Solid-first genus 3, other map (face sizes 5,6,7,7,8,8,8,8,9,9,10,11), dead end (reach 54) | S3 | `experiments/E-261030-02-solid-first-exact-inner-n12/results/genus3_12faces_48pairs*.json` | benchmark |
| Archive: 247 realizations (153 genus 2, 94 genus 3; types 15: 54, 53: 33, 0: 6, 39: 1) with chirotopes | S3 | `experiments/E-261030-10-realization-archive-climb/results/arch/archive.json` | dataset: chambers of realization spaces |
| Szilassi from random planes without a map; Roest-Vigh 8-face control (degree -2, 20 single + 8 double) | S4 / S1 | `experiments/E-261030-02-solid-first-exact-inner-n12/results/`, `code/control_rost_vigh.py` | positive controls |
| Type-58 chain-consistent normals (all 7 levels in class), sphere level UNSAT | - | `experiments/E-261030-09-chain-consistent-normals-q1/results/` | the Q1 counterexample to "class => realizable" |

Novelty of the genus-3 maps is **not checked** (they differ from the regular Dyck map {8,3} and from the 8-face
objects; catalogues of genus-3 maps not searched). Say "exact constructions new to this project".

## 3. Directions ledger

Verdicts: **FOUNDATION**; **PROMISING** (worth the next compute); **OPEN** / **OPEN-LOW** (not tried enough /
low expected value); **LOW-YIELD@budget** (tried; the measured yield at the stated budget was low; not refuted, so
a run that changes something - objective, ansatz, power, scale - is legitimate; an unchanged re-run is expected to
repeat the result); **REFUTED** (only with a proof, at least PROVED-1, that the method cannot reach the target).
No direction is REFUTED today.

| # | Direction | Evidence | Budget spent | Verdict |
|---|---|---|---|---|
| DR1 | Genus ladder / branching ladder / archive + bandit (`genus_ladder`, `beam_ladder`, `archive_climb`) | genus 3 for 4 types, genus 4 never (best 4.0 events, 11 arms nights 4-5); on the benchmark ladder (E-261102-04, section 3b) the search realizes a genus-3 map from its genus-2 parents in ~1/2 of the seeds, never from random planes | nights 3-5 + 17.8 core-h (night 7) | LOW-YIELD@nights 3-5 for S0 (genus 3 reached, genus 4 never); the Gauss gate (DR3) explains the plateau for type 0; keep the data |
| DR2 | Normals first + exact offsets; k-drift (`normals_first`, `kdrift`, `nf_control`) | 12,202 UNSAT, 0 SAT (nights 4-5); k-drift reached the class 153 times, but the reported "margin exactly 0" was a floor of `gauss_gate.hemisphere_margin` (E-261101-07), so what happens beyond the hemisphere wall is unmeasured | ~150 core-h | LOW-YIELD@150 core-h as a climbing engine; **low-power evidence** (control SAT only at r = 0.05, one trial); E-261101-04 measures the power |
| DR3 | Gauss class as a necessary filter (gate, T1, test 2.2) | explains the type-0 genus-4 plateau (k_tau = 0 on 21/21 = 7 realizations x 3 arms of one map; unchanged in 40 projective charts of one witness, so not a chart artefact) and 93 % of failed ladder levels | cheap | FOUNDATION as a filter; insufficient alone (Q1, DR2) |
| DR4 | Closure-first (`pdefect`, `sdefect`, T^3 relaxation) | 9 zero defects, all with >= 11 non-simple faces | night 2 | LOW-YIELD@night 2: zero defects only with >= 11 non-simple faces; reopen only with simplicity in the model |
| DR5 | Near-miss repair (relocation, ILS, polar duals, dual-mesh planes) | wrong topological class (FD11) | session 1-2 | LOW-YIELD: every known near-miss fails the Gauss class (FD11, EXACT), so none is close in that invariant; not a proof that repair cannot work |
| DR6 | Black-box engines on the unchanged energy (SA, CMA-ES, GA, ILS, NGOpt, DE, LNS, floors) | all solve n = 7; none breaks n = 8 (1-2) or genus 4 | sessions 2-5 | LOW-YIELD@sessions 2-5: solve n = 7, plateau at n = 8 and genus 4; a new objective would make a new run informative, more seeds would not |
| DR7 | Solid-first + exact CP-SAT inner step | genus 3 from random planes, always dead-end maps | night 2-3 | OPEN-LOW as a generator of new maps / benchmarks |
| DR8 | Exact asymmetric decision per type (OM-SAT, cube-and-conquer, certificates) | never run to completion; `immersion` 8/8 timeouts at 2.2 h; third-party pilot 2 maps in 648.5 core-h (CLAIMED); night 6: k-face sub-instances on the greedy face set SAT for 27 types at k = 8 and 15 at k = 9, every k = 10 a timeout at 20 min, 0 UNSAT, 0 of 42 models realized (E-261101-23); chirotope-first k = 7 models for 6 of 27 seeds, none realized (E-261101-25); both UNDERPOWERED by a final-polynomial LP hang (see their `CONCLUSION.md`); E-261102-01 completed the sweep: k = 8 SAT for all 59 types, k = 9 SAT for 33, TIMEOUT for 25, 0 UNSAT, 0 realized, 3 exact final polynomials not independently checked (LOW-YIELD for exclusion on the greedy face set, `CONCLUSION.md`); the chirotope-first engine scored on known answers (section 3b, E-261101-26, E-261102-03): its frontier is the full 12-face genus-3 map, also with the alternation cap lifted (0/12 at 120 min; SAT calls of minutes at k = 10-11); E-261102-02 killed | ~18 core-h + 104 (night 6, ~14 productive) + 4.2 + 6.6 + 35.9 (night 7) | PROMISING, but only after E-261101-06/E-261101-09 show a cost below ~2,000 core-h per type |
| DR9 | Rank-3 (normals-only) SAT per type with degree, covering, saddle, face-winding clauses | proposed (review 2026-10-30 dir. 6), not run | 0 | PROMISING: cheap, outcomes decisive either way |
| DR10 | Proof mining: UNSAT cores of fixed-normal offset problems (Q1 sphere; r = 0 drift seeds) -> geometric lemmas | Q10 found cores empty of global triples (local + period conditions) | ~1 h | PROMISING |
| DR11 | Local immersion theory (one reflex corner per vertex, crossing parity, minimal cores of symmetric instances) | REFLEX1, parity theorem PROVED-1 | - | PROMISING (turns computation into lemmas) |
| DR12 | Relaxed S1 target with a symmetric orbit ansatz (Roest-Vigh style), after calibration on their polyhedron | not started; only known 8-face objects are of this kind | 0 | PROMISING as a side line (<= 25 % of compute) |
| DR13 | Chirotope chambers of the realization spaces (type-0 variants, archive) | 247 chirotopes stored, not analysed | 0 | OPEN (cheap, data exists) |
| DR14 | Chain-consistent normals (Q1), projective ladder (P1), flips through degeneration (Q3), spine-seeded solids | Q1: normals found, sphere UNSAT | ~1 h | OPEN-LOW; Q1 feeds DR10 |
| DR15 | n = 8 genus-2 rung as benchmark | plateau 1-2, poor analogue (advisor) | session 2 | LOW-YIELD as a benchmark; its existence question OPEN-LOW |
| DR16 | Gauss clauses as SAT speed-up; kappa-CSP prefilter; symmetric plane sets; screw orbits; tangent planes of smooth surfaces; Szilassi embryo | E-261029-09, E-261029-10 | minutes each | LOW-YIELD@minutes each (small budgets; see the sprint board) |
| DR17 | Configuration-space planning / rigidity (stress matrices) / homotopy continuation between levels | proposed, not tested | 0 | OPEN: E-261101-19 (barrier continuation with a non-saturating measure) and E-261101-17 (geometry of the realization spaces) are its first cheap tests |
| DR18 | Arrangement first: exact chamber-SAT on structured arrangements (a symmetric arrangement with an asymmetric solid is the one loophole FD5 leaves; archived and near-miss arrangements with any solid) | proposed (strategy review 2026-11-01); the inner solver exists (`code/solid_cpsat.best_solid`) | 0 | OPEN: E-261101-16 |

## 3a. Competing hypotheses

Each hypothesis is a file in `hypotheses/` (statement, rival, evidence, status in the header). The experiments
that test it are listed on the map (`map/index.html`). A hypothesis is never "accepted" by a search that failed.
Standing constraint: any S0 realization is asymmetric (FD5), so symmetric ansatzes are for S1-S4 only.

The competing hypotheses that drive the queue:
- `H-261101-01`: Szilassi-12 exists;
- `-02`: a short structural obstruction kills many types;
- `-03`: the Gauss class is the binding barrier above genus 3;
- `-04`: the normals-first UNSATs are real evidence;
- `-05`: the type-0 witness is correct and new;
- `-06`: a per-type exact decision is affordable;
- `-07`: maximal face-neighbourly polyhedra exist for genus 2-5;
- `-08`: some structured arrangement carries an all-adjacent solid of genus >= 4 (asymmetric solid allowed);
- `-09`: the realization regions are thin and shrink per handle, so sampling has no power at any genus;
- `-10`: handles are the wrong move: no genus-3 realization space reaches an in-class handle;
- `-11`: the symmetric obstructions have cores on <= 6 faces that recur across classes;
- `-12`: some types are OM-SAT with only non-realizable models;
- `-13`: no immersion has a mirror or point-reflection symmetry (lemma, unreviewed);
- `-14`: a fold-map identity constrains the convex region of the Gauss map beyond the known counts;
- `-15`: the obstruction is local in faces: every type has an UNSAT sub-instance on <= 9 faces (the face ladder is
  monotone, the genus ladder is not);
- `-16`: guided by the Farkas certificate, the normals reach offset-feasible configurations that annealing never found.
- `-17`: core-guided SAT under the rank-3 assumptions of a geometric seed reaches embedding models of the full
  12-face instance in minutes (algorithm v2, E-261101-25).
Added 2026-11-01 from `reviews/strategy-review-2026-11-01.md` and its follow-up; H-261101-04 is demoted (its rival is
-09).

## 3b. Engine scores (benchmark ladder, E-261101-26)

Tasks with known answers, exact judge only (`experiments/E-261101-26-engine-benchmark-ladder/`); successes / seeds,
median time to success, budget per seed. No construction engine runs on the target before it has a row here
(PROTOCOL 8a).

| Engine (configuration) | R1 Szilassi, random | R4 type-15 g3, random | R4 type-0 g3, random | R5 type-15 g3, from parents | R6k k = 7 / 8 / 9 (type-15 g3) | Core-h | Frontier |
|---|---|---|---|---|---|---|---|
| chirotope-first, E-261102-02 settings (`--alt 20`, 2026-11-02) | 20/20, 0.2 s, 5 min | 0/10, 40 min | 0/10, 40 min | 0/10, 40 min | 5/10 (2.0 min), 1/10 (0.6 min), 1/10 (1.3 min), 20 min | 6.6 | R4 / R5 (furthest: k = 9 realized, R5); every failure cut by the 20-alternation cap, not by the time (16-36 % of the budget used) |
| chirotope-first, cap lifted (`--alt 100000 --timeout 300`, E-261102-03, 2026-11-03) | - | 0/4 at 40 and 120 min | 0/4 at 40 and 120 min | 0/4 at 40 and 120 min | not run, 4/4 (28.6 min), 4/4 (27.8 min), 120 min; at 40 min 2/4, 3/4 | 35.9 | R4 / R5 (furthest: k = 10 realized in 3 of 12 units, k = 11 never); failures ended by time (7) or the 300-s SAT timeout at k = 10-11 (5) |
| genus-ladder search (`archive_climb` floor, E-261102-04, 2026-11-03) | 20/20, 0.1 min, 5 min | 0/5 at 40 min, 0/2 at 120 min | 0/5 at 40 min, 0/2 at 120 min | 5/10 at 6 min (2.7 min), 3/5 at 40 min (same seeds) | not addressable (takes a full map) | 17.8 | R4 (best energy 1-3, every failure by time); the outcome per seed is decided in ~3 min |

R2 / R3 (the 8-face objects) are not expressible in the OM-SAT encoder (doubled adjacencies) and were not run with the
genus-ladder search. Other engines (solid-first, normals-first, black-box DR6): not scored yet. **R4 is the first rung
where every scored engine fails**: no construction engine runs on the target until one passes it (PROTOCOL 8a).

## 4. What may and may not be claimed

May: the CERTIFIED and EXACT rows above, with their caveats; "genus-3 exact constructions on 12 faces for
four types, one on a map combinatorially completable to a target map".

May not: "the 12-face polyhedron does not exist"; "we are close to genus 6" (18 missing adjacencies are not a
local defect); "correct Gauss degree implies realizability" (refuted by Q1); "covering is proved" (sampled);
"no type is realizable"; "no symmetric immersion" for mirrors or point reflections until I-261101-16 is reviewed (the certificates cover rotations); anything about the hemisphere wall from the nights-4/5 drift (E-261101-07); any statement from a timeout; any UNSAT beyond its exact formula.

## 5. Results worth sharing (ranked, with prerequisites)

1. **No symmetric polyhedral immersion** (FD6; stronger than Moki & Julio's embedding statement, for rotations by
   certificate and for improper isometries by the lemma I-261101-16). Needs: second encoder, written soundness
   proofs, the lemma reviewed, archived certificates, overlap check with Moki & Julio, human review.
2. **Type-0 genus-3 dossier** (section 2 row 1): exact witness + explicit 3-handle completion. Needs: independent
   second verifier, canonical map form, novelty search in genus-3 map catalogues.
3. **Diagnostic note**: known numerical near-misses are topologically far from solutions (FD11) + the exact
   normal-only filter (FD7). Ready to write.
4. **Gauss explanation of the genus-3 -> 4 plateau** (DR3) - needs an exact theorem with hypotheses.
5. Tools and data (verifiers, 59-type data, 247-realization archive) - a release, not a paper.

## 6. Progress or barrier?

Progress is real on understanding and impossibility (FD1-FD11, one certified theorem and one DRAT-checked one awaiting its write-up, a correct diagnosis of
why heuristics plateau). On construction the project has hit a robust barrier at genus 3; more heuristic
search has low expected value. What moves the question now is (a) exact decisions with certificates
(DR8-DR9), (b) turning UNSATs into lemmas (DR10-DR11), (c) a cheap constructive side line on S1 (DR12). Progress
is measured by new exact constraints, certificates or witnesses - not by core-hours or runs.
Primary sources read 2026-11-01 (`literature/primary-reads-2026-11-01.md`): Bokowski-H. 2025 found no embedding of
the 59 duals numerically and their OM-level "empty set" result is the vertex version; Roest-Vigh 2026 call the 12-face
case open. Both known 8-face face-neighbourly polyhedra have exactly 4 convex vertices (I-261101-20).

## 7. Compute ledger

From now on every run records its core-hours in its manifest (`PROTOCOL.md` §5), so this table is exact.

| Period | Core-hours (approx.) | Information gained |
|---|---|---|
| Nights 1-2 (sym, symimm, pdefect, immersion) | not recorded (immersion alone 8 x 2.2 h) | FD5 (certified), FD6 (DRAT-checked); closure-first refuted |
| Night 3 (glad) | not recorded | genus 3 for types 39, 53; class diagnosis of failed levels |
| Nights 4-5 (arch, gate, n5) | ~200 (n5 147.5 measured; arch ~50) | 203 more genus-2/3 realizations; plateau confirmed; 12,202 low-power UNSATs; pinned margin |
| Night 7 (E-261102-03, E-261102-04) | 53.7 measured (35.9 + 17.8; 8.9 of them lost to a stop and restart) | both scored engines fail R4 (full genus-3 map from random planes, 2 h per seed); genus-ladder wins R5; chirotope-first reaches k = 10 |
