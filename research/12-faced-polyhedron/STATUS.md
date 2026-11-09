# Status ledger (single source of truth for "where are we")

As of **2026-11-09** (E-261109-01 multiplicity control passed, 3y; E-261108-03 speed-up benchmark recorded in 3x; lead review 2026-11-08d applied: focus moved to (10, 4) by the owner, new week plan and S5
credences in `ROADMAP.md`; before it lead review 2026-11-08 applied: (9, 3) credences moved; sections
3d-3s compacted the same day, wording only, details in each experiment's CONCLUSION; E-261103-03 unit (a), the long-cap launch
and item 5a recorded in 3d the same day; E-261103-03 concluded; E-261103-07 cost probe recorded in 3w). Definitions, counters and
evidence labels: `SPEC.md`. Evidence details: `results.md`; chronology: `experiment-log.md`; what to do next:
`ROADMAP.md`. Update this file in the same commit as any result that changes a row. This file owns the verdicts and
numbers; other files link here.

No active process (item 5a, the E-261103-07 probe and the E-261108-03 benchmark finished). E-261103-03 is concluded (sections 3d-3i): every admissible (9, 3) plain formula is UNSAT-VERIFIED; lead review 2026-11-08d done, next: week item 1 (`ROADMAP.md`). E-261103-04, E-261103-05, E-261103-06
and E-261107-01 are concluded (sections 3g, 3j-3u).

## 0. State in one paragraph

**Focus since 2026-11-08 (`STRATEGY.md`): S5 at (10, 4)**, a maximal face-neighbourly polyhedron with 10 faces and genus
4, gated by a speed-up benchmark (E-261103-07: 10/10 TIMEOUT, section 3w); from 2026-11-03 to 2026-11-08 the focus was
(9, 3), now decided at formula scope (below); its negative result is a side track towards a note marked as not
independently reviewed. No geometric witness is known; the paired exact pilot is complete (section 3e); the candidate-map census is complete (section 3c; EXACT computation, coverage PROVED-1): 240 classes
at (9, 3), 203 admissible, 8 with a free C3, 2 at (8, 2), 1183 at (10, 4), 1117 admissible. The exact route
(OM-SAT per map at 10 elements) has decided every admissible (9, 3) plain formula UNSAT-VERIFIED (EXACT, formula scope; geometric reading conditional PROVED-1, section 3d); its multi-adjacency encoder
passes the bounded controls (E-261103-02, EXACT). Both plain (8,2) warm-up formulas are now
UNSAT-VERIFIED (E-261103-03, section 3d; geometric interpretation conditional PROVED-1). Uniform fixed-face C2/D3 formulas cannot decide those
geometric symmetry families (PROVED-1 scope warning in the experiment). **S0 (Szilassi-12) is parked, not abandoned**: the paragraph below and
every row of this file are its snapshot at parking time and stay valid.

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
| DR7 | Solid-first + exact CP-SAT inner step | S0: genus 3 from random planes, dead-end maps; S5 variant passes known (8,3) and random D2 recovery controls (section 3g) | night 2-3 | OPEN-LOW as a generator of new maps / benchmarks |
| DR8 | Exact asymmetric decision per type (OM-SAT, cube-and-conquer, certificates) | never run to completion; `immersion` 8/8 timeouts at 2.2 h; third-party pilot 2 maps in 648.5 core-h (CLAIMED); night 6: k-face sub-instances on the greedy face set SAT for 27 types at k = 8 and 15 at k = 9, every k = 10 a timeout at 20 min, 0 UNSAT, 0 of 42 models realized (E-261101-23); chirotope-first k = 7 models for 6 of 27 seeds, none realized (E-261101-25); both UNDERPOWERED by a final-polynomial LP hang (see their `CONCLUSION.md`); E-261102-01 completed the sweep: k = 8 SAT for all 59 types, k = 9 SAT for 33, TIMEOUT for 25, 0 UNSAT, 0 realized, 3 exact final polynomials, checked by an independent standard-library checker in `verify_all` (2026-11-03, `verification/certificates/final_polynomial/`, EXACT; each excludes one SAT model, no type) (LOW-YIELD for exclusion on the greedy face set, `CONCLUSION.md`); the chirotope-first engine scored on known answers (section 3b, E-261101-26, E-261102-03): its frontier is the full 12-face genus-3 map, also with the alternation cap lifted (0/12 at 120 min; SAT calls of minutes at k = 10-11); E-261102-02 killed | ~18 core-h + 104 (night 6, ~14 productive) + 4.2 + 6.6 + 35.9 (night 7) | PROMISING, but only after E-261101-06/E-261101-09 show a cost below ~2,000 core-h per type |
| DR9 | Rank-3 (normals-only) SAT per type with degree, covering, saddle, face-winding clauses | proposed (review 2026-10-30 dir. 6), not run | 0 | PROMISING: cheap, outcomes decisive either way |
| DR10 | Proof mining: UNSAT cores of fixed-normal offset problems (Q1 sphere; r = 0 drift seeds) -> geometric lemmas | Q10 found cores empty of global triples (local + period conditions) | ~1 h | PROMISING |
| DR11 | Local immersion theory (one reflex corner per vertex, crossing parity, minimal cores of symmetric instances) | REFLEX1, parity theorem PROVED-1 | - | PROMISING (turns computation into lemmas) |
| DR12 | Relaxed S1 target with a symmetric orbit ansatz (Roest-Vigh style), after calibration on their polyhedron | not started; only known 8-face objects are of this kind | 0 | PROMISING as a side line (<= 25 % of compute) |
| DR13 | Chirotope chambers of the realization spaces (type-0 variants, archive) | 247 chirotopes stored, not analysed | 0 | OPEN (cheap, data exists) |
| DR14 | Chain-consistent normals (Q1), projective ladder (P1), flips through degeneration (Q3), spine-seeded solids | Q1: normals found, sphere UNSAT | ~1 h | OPEN-LOW; Q1 feeds DR10 |
| DR15 | n = 8 genus-2 rung, S5 (8,2) | Both plain census-map formulas UNSAT-VERIFIED in E-261103-03; CNF/DRAT retained, controls pass (section 3d) | pilot 0.009883229479 core-h; recheck separately recorded | FOUNDATION: exact formula decisions; geometric exclusion conditional on PROVED-1 census/encoding |
| DR16 | Gauss clauses as SAT speed-up; kappa-CSP prefilter; symmetric plane sets; screw orbits; tangent planes of smooth surfaces; Szilassi embryo | E-261029-09, E-261029-10 | minutes each | LOW-YIELD@minutes each (small budgets; see the sprint board) |
| DR17 | Configuration-space planning / rigidity (stress matrices) / homotopy continuation between levels | proposed, not tested | 0 | OPEN: E-261101-19 (barrier continuation with a non-saturating measure) and E-261101-17 (geometry of the realization spaces) are its first cheap tests |
| DR18 | Arrangement first: exact chamber-SAT on structured arrangements (a symmetric arrangement with an asymmetric solid is the one loophole FD5 leaves; archived and near-miss arrangements with any solid) | proposed (strategy review 2026-11-01); the inner solver exists (`code/solid_cpsat.best_solid`) | 0 | OPEN: E-261101-16 |
| DR19 | S5 exact pipeline: census of the candidate maps (E-261103-01), OM-SAT per map with multiple adjacencies and symmetry clauses (E-261103-02, -03), realization or final polynomial; the dress rehearsal of the S0 pipeline at 10 elements | E-261103-01 census complete (section 3c); E-261103-02 multi-adjacency encoder controls pass (EXACT), soundness PROVED-1; free C2/C3 calibrated, fixed-face C2/D3 uniformity obstruction documented, both plain (8,2) formulas now UNSAT-VERIFIED in E-261103-03 (section 3d), partial (9,3) decisions (sections 3e-3f) | ~0.4 core-h (sampler) + 0.02273 recorded (census) + 0.058735 recorded (encoder controls) + 0.009883 recorded (decision pilot; control recheck separately manifested) | PROMISING (the queue since 2026-11-03) |

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

R2 / R3 (the 8-face objects) were not expressible in the original OM-SAT encoder and were not run with the
genus-ladder search. E-261103-02 closes the encoder gap (2026-11-03, EXACT controls: own-map Eval / pinned CNF,
predicate comparisons and S0 hashes; `experiments/E-261103-02-s5-omsat-multi-adjacency-encoder/CONCLUSION.md`).
This is validation on supplied planes, not an engine score from random planes. Fixed-face C2/D3 require a
nonuniform encoder for symmetry-preserving geometric decisions (PROVED-1). Other engines (solid-first, normals-first, black-box DR6): not scored yet. **R4 is the first rung
where every scored engine fails**: no construction engine runs on the target until one passes it (PROTOCOL 8a).

## 3c. Focus target S5: candidate-map census (2026-11-03)

E-261103-01 exhausted the four required cases and the K12 control. Evidence and provenance:
`experiments/E-261103-01-s5-map-census/CONCLUSION.md`; datasets `results/maps_F_g.json` in that folder.
**EXACT** computations are checked by `verify_all.py`, including a fresh exhaustive (9,3) run.
**PROVED-1** completeness: the written coverage argument for the enumeration has no human review.
These are abstract dual maps, not geometric S5 witnesses.

A map is loopless, oriented and triangular, with F vertices and E = 3(F + 2g - 2) edges, underlying
simple graph K_F. Mirror images are identified. **Admissible** means every corner triple is distinct;
this is necessary for realization on distinct planes, not sufficient. Dart codes retain parallel-edge
pairings, including on inadmissible maps; `links` alone need not determine them.

| (F, g) | classes | admissible | symmetry of admissible maps | label |
|---|---:|---:|---|---|
| (7, 1) | 1 | 1 | Aut+ = 42, chiral | EXACT; coverage PROVED-1 |
| (8, 2) | 2 | 2 | both have a half-turn, neither is reflexible; Aut+ = 2 and 6 | same |
| **(9, 3)** | **240** | **203** | Aut+ 1:173, 2:22, 3:6, 6:2; **8 with a free C3** (2 with Aut+=6), 24 with an involution, none reflexible | same |
| (10, 4) | 1183 | 1117 | Aut+ 1:1021, 2:83, 3:11, 4:2; 85 with an involution, one reflexible | same |
| (12, 6), S0 control | 59 | 59 | equals all FD3 classes, automorphism orders and reflexibility flags | same |

The (8,2) and (9,3) code sets equal the previous sampled sets, including inadmissible maps. A separate
C3 triangle-orbit exact cover with equivariant edge gluing gives exactly the same eight admissible
free-C3 maps. The two C2 maps at (8,2) and the C3/C2 lists at (9,3) are ready for E-261103-03;
E-261103-02 has validated its encoder (read its fixed-face C2/D3 uniformity restriction). The (9,3) face sizes remain in {8,9,10,11}; 18 admissible maps
have a tripled pair (10 with a doubled pair on a shared face, 8 with it disjoint; EXACT recount, `reviews/strategy-review-2026-11-08.md` M1). Chirality at (8,2) and (9,3) follows at the census' coverage level (PROVED-1).

The (8,3) family is not censused here. The review's >=22,666 sampled classes and its checks of the
Roest-Vigh and Mizhaev maps remain session checks only. Nothing geometric has run on any focus map.

## 3d-3f, 3h-3i. E-261103-03 exact decisions at (8, 2) and (9, 3) (2026-11-04)

* **(8, 2):** both plain formulas and both uniform free-C2 formulas UNSAT-VERIFIED (EXACT; 0.0099 core-h). The geometric
  exclusion is PROVED-1 and conditional on census coverage, encoder soundness and general position; not CERTIFIED.
* **(9, 3) free C3:** all 8 uniform free-C3 formulas UNSAT-VERIFIED (EXACT). A conditional coverage draft for the
  geometric C3 family is in CONCLUSION (PROVED-1, AI review only).
* **(9, 3) plain**, solver cap 60 s unless stated: UNSAT-VERIFIED for 28 maps (5, 6, 30 in the paired pilot; 40, 48 at
  62.5 and 75.7 s in the 60/300-s grid; 19, 20, 29, 31, 43, 52, 58, 59, 60, 66, 67, 75, 83, 90 in the 80-map tranche;
  94, 100, 102, 111, 123, 171, 177, 184, 199 in unit (a); 0-4, 10, 12, 36, 38, 39, 41, 42, 74, 174, 176, 181, 200 in the
  long-cap launch at 1800 s, all 2026-11-08): 45 in total before item 5a; item 5a decided the other 158 (below), so 203 of 203, 0 SAT. Checker time is separate (map 40: 62 s).
* Solve time depends on the multiple-adjacency pattern (NUMERICAL): patterns (1,2,3) and (2,2,2) are 13 of 13
  UNSAT-VERIFIED in 22-76 s; (1,1,1,3) is 14 of 14 (solves 32-215 s; the five that timed out at 60 s, a cap
  inside the solve-time range, finished at 69-215 s); spread-out doubled pairs time out (`reviews/strategy-review-2026-11-08.md` §3.1, `-08b`).
* **Unit (a)** of week item 1 (2026-11-08): the 13 unattempted 11-gon maps at 60/120 s, one shard, 822 s wall
  (0.23 core-h), controls passed; 9 UNSAT-VERIFIED, 4 TIMEOUT. Prediction (>= 10/13) missed; item 3 kept (>= 7/13).
  Scope: these plain formulas at these caps; the TIMEOUTs are no evidence either way.
* **Long-cap launch** (item 1, 2026-11-08, `CONCLUSION` last section): 10 shards, 2.74 core-h, solver 1800 s. Controls passed (`control-f9`
  SAT, `control-f9-neg` UNSAT-VERIFIED; genus-0 submap controls). All 17 maps UNSAT-VERIFIED, 0 TIMEOUT, 0 SAT: the five (1,1,1,3) maps
  (69-215 s) and 12 maps of `1^6` (5, 523-914 s), `(1^4,2)` (5, 127-317 s) and `(1,1,2,2)/(2,3)` (2, 89-136 s; the lowest indices, not
  a sample). **Every 11-gon (9,3) plain formula (24 maps) is UNSAT-VERIFIED** (EXACT, formula scope; geometric reading PROVED-1, conditional).
  Not claimed: anything about the 60 unresolved and 98 unattempted maps, or genus-3 behaviour of the controls.
* **Item 5a** (2026-11-08, `CONCLUSION` last section): 10 shards, 18.51 core-h, longest shard 2.36 h, solver 1800 s. Controls passed in
  every shard. All 158 remaining maps UNSAT-VERIFIED (cadical 31-1239 s, slowest 69 % of the cap), 0 TIMEOUT, 0 SAT; all 158 CNFs rebuild
  to their recorded hashes. **Every admissible (9, 3) plain formula, 203 of 203, is UNSAT-VERIFIED** (EXACT, formula scope). Geometric
  reading: no S5 polyhedron at (9, 3), symmetric or not (PROVED-1, conditional on census coverage, encoder soundness with the uniformity
  reduction, one encoder, no human review). Not claimed: a CERTIFIED or reviewed theorem, archived proofs, a second implementation.
  Untested parts (lead review 2026-11-08d, A1-A2): no positive control has a pair of multiplicity >= 3 (18 of the 203 maps
  and one (8, 2) map have one); the full census has one enumerator. Week items 1, 3, 4 address them.
* **Core study E-261108-02** (week item 3, 2026-11-08, 0.07 core-h wall): PARK. 0 of the 24 11-gon plain formulas have an UNSAT
  sub-formula on <= 6 faces (clause subsets indexed by constraint face tuples, k = 3..6 exhaustive, 0 TIMEOUT; k = 7 also none;
  k = 8 undecided, 94 TIMEOUTs); controls C0/C1/C2 pass, comparators equal. Scope: this grouping and cap 20 s (CONCLUSION).
* Tranche verdict LOW-YIELD@60 s for its frozen queue; no cap above 300 s has been tried (ROADMAP week item 1). All
  manifests total about 2.0 core-h (tranche 1.50 incl. its pilot); itemised sums, hashes and `results/tranche_audit.json`
  in CONCLUSION. Large proofs are local-only with hashes in git; external certificate publication is pending.

## 3g. E-261103-05 solid-first explore controls (2026-11-04)

BENCHMARK-PASS. The disk-aware CP-SAT inner solver (1-3 runs per pair, connected disk faces) recovers both (8, 3)
objects unseeded on their own planes; random D2 seeds 0-3 are INFEASIBLE, seed 4 gives an auxiliary S1 (8, 3) object
isomorphic to Roest-Vigh's map: (24, 36, 8, -4), 28 pairs, 20 single + 8 double, eight simple 9-gons (EXACT, re-solved
by the quick suite; disk-encoding argument PROVED-1). 0.0052 core-h. Engine calibration, not a focus witness.

## 3j-3s. E-261103-04 genus ladder on 9 faces (2026-11-04 to 2026-11-07, concluded)

* The legacy triangle-to-links conversion fails on parallel-edge maps; the dart-preserving surgery gives reversible
  chains to simple spheres for all 203 admissible (9, 3) maps, Szilassi and both (8, 3) controls (PROVED-1).
* Geometric recovery: Szilassi recovered; Roest-Vigh rejected at genus 1 and Mizhaev at genus 2 (non-simple faces),
  also in the 180/600-s grid: hinge ladder UNDERPOWERED, it fails both (8, 3) controls.
* OM audits of the intermediates: Roest-Vigh g1 OM-SAT; Mizhaev g2 formula UNSAT-VERIFIED; an alternative Mizhaev
  first removal is OM-SAT and its descendants give a checked combinatorial/OM chain to a sphere (CHAIN-PASS).
* Saved-OM realization: Roest-Vigh g1 (16, 24, 8, 0) and Mizhaev g1 (16, 24, 8, 0), g2 (20, 30, 8, -2) realized,
  verifier and separate rational checker PASS (PROVED-1, auxiliary, not S5).
* Verdict: hinge ladder parked; OM-first realization of intermediates works (a tool for a future SAT model) but adds no
  (9, 3) power. About 0.47 core-h in all manifests. Details: E-261103-04 CONCLUSION.

## 3t. E-261107-01 nine-plane solid-first pilot (2026-11-07)

30 uniform 9-plane arrangements (c3 / d2p1 / random, 10 each), hard model 36 pairs, E = 39: all 30 INFEASIBLE,
5.9-21 s each (cap 180 s), controls pass (E-261107-01 CONCLUSION). EXACT computation, geometric reading PROVED-1
via the E-261103-05 encoding; no DRAT. Best Phase B pair count 32 (diagnostic only). Verdict LOW-YIELD@0.38
core-h; configuration parked. No hypothesis, credence or witness change.

## 3u. E-261103-06 embedded-first R1 pilot (2026-11-07)

Szilassi map on a 28 x 28 torus mesh, damped block-coordinate flattening with a discrete intersection check: all 4
valid starts BLOCKED after 3-6 steps at energy 84-118 (start 150-191); controls pass. Local folds at mesh ring <= 1
are the rejected steps. EXACT, instance scope; UNDERPOWERED, not a refutation; idea parked, R2' not run
(E-261103-06 CONCLUSION). No hypothesis, credence or witness change.

## 3v. E-261108-01 arrangement-source sweep (2026-11-08)

300 exact 9-plane arrangements (100 Roest-Vigh + random ninth plane, 100 Mizhaev + ninth, 100 random C2-invariant),
hard model 36 pairs, E = 39, cap 60 s, 10 shards: all 300 INFEASIBLE (6-28 s each), 0 SOLID; 40/40 controls pass
(E-261108-01 CONCLUSION). EXACT computation, geometric reading PROVED-1 via the E-261103-05 encoding; no DRAT. Density
bound < 1 % pooled under an i.i.d. assumption. Verdict LOW-YIELD@1.33 core-h; arrangement-first for (9, 3) parked.
No hypothesis, credence or witness change.

## 3w. E-261103-07 (10, 4) cost probe (2026-11-08)

10 (10, 4) admissible maps (one per fast pattern, two per slow pattern), E-261103-03 plain S5 formula, 10 shards, 2.53 core-h
(sum of shard wall times): 20/20 controls pass; 0 SAT, 0 UNSAT, **10/10 TIMEOUT** (fast 300 s, slow 1800 s). NUMERICAL, instance
scope; a timeout is not a result for any map. Pre-registered rule: "needs a speed-up first" before any full (10, 4) run; F is only
bounded below (> 3.3 over all maps, > 11 for `(2,2,2)/(2,2,2)`). No hypothesis, credence or witness change
(E-261103-07 CONCLUSION).

## 3x. E-261108-03 (10, 4) speed-up benchmark (2026-11-08/09)

10 shards, 8.59 core-h (sum of shard wall times), 2.38 h wall, no DRAT (UNSAT-SOLVER), controls pass in every shard. (10, 4) maps
96, 85, 146, 845 (solver s): kissat 1073, 2749, 693, 188; CaDiCaL `--unsat` 3119, 8420, 1415, 367; default CaDiCaL 1970, 6454 (96, 85 only);
0 SAT, three solvers agree. Best measured speed-up 2.35x (kissat on 85), `--unsat` slower than default; the 10x goal is not met.
Winner kissat (sum B 380 against 777 core-h): P(4) = P(16) = 475 core-h without DRAT (n = 1-2 per stratum, a scenario, not a bound).
NUMERICAL, instance scope; UNSAT-SOLVER is not a negative result and (10, 4) UNSATs carry the item 1 caveat. Next by the follow-up tree: Actions
calibration (I-261108-07); no holdout (P(4) > 160). No hypothesis, credence or witness change (E-261108-03 CONCLUSION).

## 3y. E-261109-01 grooved-box multiplicity control (2026-11-09)

Box with k = 2, 3 pyramidal notches across one edge, exact planes, EMBEDDED by `ladder_exact` (F 12 / 15, top/front pair shares
3 / 4 segments). E-261103-02 encoder, `submap=True`: pinned own map SAT (k = 2, 3), same planes with a swapped segment pairing
(valid map, not embedded) UNSAT-VERIFIED, unpinned k = 2 SAT. EXACT, instance scope (other multiple-segment positions, m >= 5,
unpinned k = 3 not run); lifts the item 1 caveat on the (9,3) and (10,4) UNSATs (E-261109-01 CONCLUSION).

## 4. What may and may not be claimed

May: the CERTIFIED and EXACT rows above, with their caveats; "genus-3 exact constructions on 12 faces for
four types, one on a map combinatorially completable to a target map".

May not: "the 12-face polyhedron does not exist"; "we are close to genus 6" (18 missing adjacencies are not a
local defect); "correct Gauss degree implies realizability" (refuted by Q1); "covering is proved" (sampled);
"no type is realizable"; "no symmetric immersion" for mirrors or point reflections until I-261101-16 is reviewed (the certificates cover rotations); anything about the hemisphere wall from the nights-4/5 drift (E-261101-07); any statement from a timeout; any UNSAT beyond its exact formula; that census completeness has an independent human review (the coverage argument is PROVED-1); an unconditional, CERTIFIED or human-reviewed (9, 3) non-existence theorem (single encoder, coverage and soundness PROVED-1, proofs not archived; section 3d), or an unconditional/human-reviewed (8, 2) non-existence theorem (section 3d).

May not (scope, owner's question 2026-11-08): that the (8, 2) or (9, 3) negative covers non-cubic objects. S5 is cubic; at
(8, 2) and (9, 3) the edge count has slack (E <= 30 for 28 pairs, E <= 39 for 36), so counting does not exclude objects with
every pair adjacent and some vertices of degree >= 4 (e.g. (9, 3) with V = 23, E = 36, three 4-valent vertices); no
formula covers them. At (12, 6) there is no slack (E = 66 pairs), so S0 is unaffected. The (8, 2) / (9, 3) note must say "cubic"
unless the perturbation lemma I-261108-09 (untested) reduces these objects to the cubic case.

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

Literature check for S5 (ROADMAP item 2, web search only, 2026-11-08; no compute): arXiv, journal and web searches for (8, 2), (9, 3), (10, 4) found no published or claimed polyhedron and no non-existence result; the only face-neighbourly objects in print remain the tetrahedron, Szilassi and the two (8, 3) objects (Mizhaev, Roest-Vigh). CLAIMED, scope: absence in the sources searched (`literature/review-2026-11-03.md`, `literature/README.md`); MathOverflow not reached by the search tool; the four originals (Altshuler-Brehm 1986 and 1992, ABS 1994, Bokowski-Schewe 2002) were attempted on 2026-11-08 (`literature/primary-reads-2026-11-08.md`): no full text obtainable, none decides or constrains (8, 2), (9, 3), (10, 4); the 1986 genus-2 theorem is a vertex statement for maps without multiple edges.

For the focus target the picture differs (2026-11-03): the combinatorics is small (section 3c) and the exact route is
affordable map by map, so progress is measured by maps decided (UNSAT-VERIFIED, realized, or certified non-realizable), not
by search hours; the heuristic engines are explore runs behind pilots (`ROADMAP.md`, S5 queue).

## 7. Compute ledger

From now on every run records its core-hours in its manifest (`PROTOCOL.md` §5), so this table is exact.

| Period | Core-hours (approx.) | Information gained |
|---|---|---|
| Nights 1-2 (sym, symimm, pdefect, immersion) | not recorded (immersion alone 8 x 2.2 h) | FD5 (certified), FD6 (DRAT-checked); closure-first refuted |
| Night 3 (glad) | not recorded | genus 3 for types 39, 53; class diagnosis of failed levels |
| Nights 4-5 (arch, gate, n5) | ~200 (n5 147.5 measured; arch ~50) | 203 more genus-2/3 realizations; plateau confirmed; 12,202 low-power UNSATs; pinned margin |
| Night 7 (E-261102-03, E-261102-04) | 53.7 measured (35.9 + 17.8; 8.9 of them spent on units that a stop cut short and the restart recomputed) | both scored engines fail R4 (full genus-3 map from random planes, 2 h per seed); genus-ladder wins R5; chirotope-first reaches k = 10 |
| Strategy review 2026-11-03 (flip-walk sampler, single core) | ~0.4 (runs of <= 4 min) | candidate-map counts and symmetric sub-lists of section 3c |
