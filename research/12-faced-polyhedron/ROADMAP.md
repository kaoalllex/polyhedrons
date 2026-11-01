# Roadmap: the experiment queue

As of 2026-11-01. Principle: **theory and a cheap filter first -> a discriminating experiment -> an exact
solver -> a lemma or a certificate**. We do not try to enumerate the search space; we pick small, motivated
regions where one experiment can exclude a whole class or reveal a new constraint. How to run an item:
`PROTOCOL.md`. Current state: `STATUS.md`.

## Scoring (pre-registration, external audit 17.2)

Each item is scored 0-2 on: **T** theoretical motivation, **D** discriminating power (do different outcomes
change the plan?), **F** cheap falsification test exists, **G** generalisation potential (a lemma for many
types?), **R** reproducibility (exact, archivable). Do not run anything with T + D < 3, however easy to
parallelise. Every item states what SAT / UNSAT / timeout / near-miss would mean **before** it runs.

## Phase 0 - foundations of the workflow (done 2026-11-01 unless marked)

* `SPEC.md` frozen; evidence labels and counters normalised.
* `verification/verify_all.py` (one command, 9 checks) and `verify_candidate.py` (any file format); CI on every push.
* `requirements.txt` pinned; hard-coded `/home/user` paths removed.
* Experiment template and GitHub Actions runner (`experiments/_template/`, `.github/workflows/experiment.yml`).
* TODO: archive the raw DRAT certificates of `sym` / `symimm` (GitHub release or Zenodo, SHA-256 in git) - they
  exist only on the owner's machine (`*.drat` is git-ignored).
* TODO: tag the frozen state `state-2026-11-01` after this restructure is merged.

## Queue (in order; IDs are permanent, folders `experiments/E##-slug/` when started)

| ID | Question | T D F G R | Budget | Stop rule |
|---|---|---|---|---|
| E01 | Type-0 genus-3 dossier: is the best positive result correct and new? | 1 2 2 1 2 | 1-2 sessions, no compute | done when a referee-style package exists |
| E02 | Power of normals-first: how often is the *control* SAT at radius r? | 1 2 2 1 2 | ~10 core-h | 30 maps x 3 radii, or earlier if the rate is clear |
| E03 | Proof mining: what small cores make fixed-normal offset problems UNSAT? | 2 2 2 2 2 | ~5 core-h + theory | a core family explained, or 50 cores with no pattern |
| E04 | Pinned hemisphere margin: why does every class-reaching drift end at margin 0? | 2 2 2 2 1 | theory + 1 h | proof, counterexample, or written reason it is an artefact |
| E05 | Exact covering: replace sampled covering by an exact check | 1 1 2 1 2 | 1 session | exact check agrees with sampling on all 232 gated realizations |
| E06 | Rank-3 (normals-only) SAT per type with degree / covering / saddle / face-winding clauses | 2 2 2 2 2 | 1 day coding, minutes per type | per type: UNSAT (proof!) or a model count estimate |
| E07 | Encoding comparison with `pirozhkov-andrei/polyhedraproof` on shared instances | 1 2 1 1 2 | 1 day | conflicts / time per instance measured for both encoders |
| E08 | Write-up: no symmetric immersion (second encoder, soundness proofs, archived certificates) | 2 1 1 1 2 | 2-3 sessions | arXiv-ready draft reviewed by `adversarial-verifier` and one human |
| E09 | Relaxed S1 target: 12 faces, doubled pairs, symmetric orbit ansatz, after Roest-Vigh calibration | 1 2 2 1 2 | 2 nights max, <= 25 % of compute | calibration fails -> fix engine, do not run n = 12 |
| E10 | Chirotope chambers of the 247 archive realizations | 1 1 2 1 2 | 1 session | a description of chamber adjacency for one map, or "no structure" |

Conditional (only after E06 and E07): **E11 cube-and-conquer pilot** on 3 types (type 0, type 58, one trivial-Aut
type), one laptop night or GitHub Actions matrix; metric = refuted fraction per core-hour; campaign only if the
extrapolation is below ~2,000 core-hours per type.

### E01 - type-0 genus-3 dossier (external audit sections 18, 23, 24)

Hypothesis: the five `type0_genus3_extendable*.json` files are exact embeddings of one map that is completable by
the three certified handles to target type 0. Steps: (1) a second, independently written verifier (vertices from
planes, cyclic face order, simplicity, pairwise intersections, chi = -4) that does not import `ladder_exact`;
(2) canonical form of the map (relabelling + mirror), proof that all five variants share it; (3) re-run the
certificate; (4) novelty search: genus-3 maps with 12 faces (Wedd's list, Conder's census), known R^3
realizations; (5) a 2-page dossier: theorem, certificates, limits, questions for a mathematician.
Outcomes: all pass -> shareable result #2 in `STATUS.md`; any mismatch -> a bug in FD10, top priority.

### E02 - power study for normals-first (night report follow-up)

Hypothesis H0: at in-class seeds the offset problem is generically SAT near the realized normals, so 0 SAT in
12,202 means something. Test: `code/nf_control.py` on 30 realized maps (archive, several types) x r in {0.01,
0.02, 0.05}, z3 timeout 600 s. Outcomes: control SAT rate p >= 0.3 at some r -> the night-4/5 UNSATs at that r
are real evidence of an obstruction between levels (then E03 on them); p ~ 0 -> normals-first sampling is
blind, retire the UNSAT counts as evidence; timeouts dominate -> encoding cost problem, not geometry.

### E03 - proof mining from UNSAT cores (external audit 16.3, 17.1 C, 20)

Instances: the Q1 sphere (type 58, `experiments/chain_normals/`) and the 80 r = 0 kdrift seeds
(`overnight/results/n5/attempts/kd_*`, `radius: 0.0`). Save every SMT2 instance; extract minimal cores (z3
`unsat_core` with named assertions, then deletion-based minimisation); classify by which constraint families
they use (closure / periods, simplicity, reflex, orientation). Outcome: a recurring small core -> state it as a
lemma (PROVED-1), test it as a cheap normal-level filter, add it to the gate; no pattern -> record and stop.

### E04 - pinned hemisphere margin

153/153 drifts reached the next class with margin exactly 0. Either a theorem (handle normals of an embedded
polyhedron cannot leave a closed hemisphere in that configuration) or an artefact of the drift's acceptance
rule. First read `kdrift.py`'s acceptance rule and margin definition; then try to prove; then a 1-hour test that
forces the margin positive. Outcome either way is a short note in `theory/theory-notes.md`.

### E06 - rank-3 SAT per type (internal audit E1, review 2026-10-30 dir. 6)

Variables: the 220 signs chi(X, Y, Z, inf) in the gauge, kappa bits, vertex-type bits. Clauses: rank-3 GP,
degree -5 at sampled directions, covering, >= 13 saddles, vertex rule F3/F4, face turning F6, face-winding
identity. Controls: Szilassi normals (n = 7) SAT; the 94 genus-3 realizations' normals SAT for their sub-maps;
random normals mostly UNSAT. Outcome: UNSAT for a type = a short human-checkable exclusion (unlikely, decisive);
SAT = model counts and a split basis for E11.

## Stop list (do not spend compute on these again for S0)

Genus ladder / arch / glad / n5 / kdrift / normals-first *climbing*; pdefect / sdefect; black-box engines on the
pair energy; near-miss repair; Gauss clauses as a SAT speed-up; asymmetric immersion instances without cubing;
more seeds or weights on an unchanged objective. Reopening needs a written reason in `STATUS.md`.

## Decision point

After E01-E06: either (a) E11 then a certified campaign (cloud or Actions matrix), or (b) publish the shareable
results and change the class of geometric ansatz, or (c) stop with a written negative report. Decide from the
evidence, not from sunk cost.
