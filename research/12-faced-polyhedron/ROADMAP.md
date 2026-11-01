# Roadmap: the experiment queue

As of 2026-11-01. Principle: **theory and a cheap filter first -> a discriminating experiment -> an exact
solver -> a lemma or a certificate**. We do not try to enumerate the search space; we pick small, motivated
regions where one experiment can exclude a whole class or reveal a new constraint. How to run an item:
`PROTOCOL.md`. Current state: `STATUS.md`.

## Scoring (pre-registration, external audit 17.2)

Each item is scored 0-2 on: **T** theoretical motivation, **D** discriminating power (do different outcomes
change the plan?), **F** cheap falsification test exists, **G** generalisation potential (a lemma for many
types?), **R** reproducibility (exact, archivable). Do not run anything with T + D < 3, however easy to
parallelise. Every item's `PLAN.md` states what SAT / UNSAT / timeout / near-miss would mean **before** it runs.

## Phase 0 - foundations of the workflow (done 2026-11-01 unless marked)

* `SPEC.md` frozen; evidence labels and counters normalised.
* `verification/verify_all.py` (one command, 11 checks) and `verify_candidate.py` (any file format, `--target S0` = the solution check); CI on every push.
* `requirements.txt` pinned; hard-coded `/home/user` paths removed.
* Experiment template and GitHub Actions runner (`experiments/_template/`, `.github/workflows/experiment.yml`).
* DRAT certificates of `sym` / `symimm`: the night runs had deleted them after checking (no `--keep-proofs`).
  Regenerated 2026-11-01 with `--keep-proofs --keep-cnf`: all 50 CNFs and all 50 proofs are bit-identical to the
  SHA-256 recorded in `overnight/results/{sym,symimm}/results.jsonl`, 50/50 re-VERIFIED by drat-trim. Packed as
  `symmetric-{sym,symimm}-drat.tar.xz` (422 MB, 438 MB) and published on the GitHub release `state-2026-11-01`;
  hashes, versions and how to check: `verification/certificates/symmetric_drat/`. TODO (owner): Zenodo DOI via
  the GitHub-Zenodo integration before any write-up.
* Tag `state-2026-11-01` = `main` after merging this restructure; witnesses and site lab models (`witnesses/`).

## Queue

Order rule: first the items that validate evidence the project already relies on (E01 checks the verifier and
the best witness, E02 checks whether 12,202 UNSATs mean anything); then by score sum, ties by lower cost. IDs are
permanent. State: `open` / `running` / `done` / `killed` / `blocked`. Folder `experiments/E##-slug/` once
started (E08 lives in `proof-no-symmetric-immersion/` until its PLAN.md exists). `experiment-conclude` updates
the State. Hypotheses and outcome meanings go in each item's `PLAN.md` before it runs; the sections below are
the starting point.

| ID | State | Tests | Question | T D F G R | Budget | Stop rule |
|---|---|---|---|---|---|---|
| E01 | open | FD10, witness | Type-0 genus-3 dossier: is the best positive result correct and new? | 1 2 2 1 2 | 1-2 sessions, no compute | stop after the 5 steps below or 2 sessions; any verifier mismatch -> fix FD10 first |
| E02 | open | DR2 | Power of normals-first: how often is the *control* SAT at radius r? | 1 2 2 1 2 | ~10 core-h | 30 maps x 3 radii, or earlier if the rate is clear |
| E03 | open | DR10 | Proof mining: what small cores make fixed-normal offset problems UNSAT? | 2 2 2 2 2 | ~5 core-h + theory | a core family explained, or 50 cores with no pattern |
| E06 | open | DR9 | Rank-3 (normals-only) SAT per type with degree / covering / saddle / face-winding clauses | 2 2 2 2 2 | 1 day coding, minutes per type | per type: UNSAT (proof!) or a model count estimate; stop after 3 types if every one is SAT with no pruning |
| E04 | open | DR3 | Pinned hemisphere margin: why does every class-reaching drift end at margin 0? | 2 2 2 2 1 | 1 session theory + 1 core-h | stop after 1 session + the 1-h test: proof, counterexample, or written reason it is an artefact |
| E09 | open | DR12 | Relaxed S1 target: 12 faces, doubled pairs, symmetric orbit ansatz, after Roest-Vigh calibration | 1 2 2 1 2 | 2 nights max, <= 25 % of compute | calibration fails -> fix engine, do not run n = 12 |
| E07 | open | DR8 | Encoding comparison with `pirozhkov-andrei/polyhedraproof` on shared instances | 1 2 1 1 2 | 1 day | conflicts / time per instance measured for both encoders |
| E08 | open | FD6 | Write-up: no symmetric immersion (second encoder, soundness proofs, archived certificates) | 2 1 1 1 2 | 2-3 sessions | arXiv-ready draft reviewed by `adversarial-verifier` (a filter) and one human |
| E12 | open | FD5, FD6, E01 | External human review: send FD5/FD6 (CNF hashes, certificates) and the E01 dossier to Pirozhkov, Moki & Julio or Bokowski | 2 2 1 1 2 | owner's e-mail, no compute | a reply, or 4 weeks without one -> next reviewer |
| E13 | open | DR12, DR15 | Side line: maximal face-neighbourly cubic polyhedra per genus. All pairs adjacent and E = 3(F + 2g - 2) >= C(F, 2) give the largest F per genus: (F, g) = (8, 2), (9, 3), (10, 4), (11, 5), with 2, 3, 3, 2 extra edges beyond one per pair (doubled pairs); (12, 6) is Szilassi-12 itself. Which of them exist? Start with a literature check and (8, 2) | 1 2 2 2 2 | literature 1 session; then 1 night per case | stop at the first case that is UNSAT for every map tried with a written power statement, or after (9, 3) |

Below the gate (T + D < 3; run only after re-scoring with a written reason):

| ID | Question | T D F G R | Why below |
|---|---|---|---|
| E05 | Exact covering: replace sampled covering by an exact check | 1 1 2 1 2 | no planned decision depends on it until E06 uses covering clauses; re-score then |
| E10 | Chirotope chambers of the 247 archive realizations | 1 1 2 1 2 | descriptive; no outcome changes the plan |

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

## Parked methods (low measured yield, not refuted)

Tried, with little yield at the budget stated in `STATUS.md` §3 (LOW-YIELD rows). None is refuted, so none is
forbidden. A new run needs a `PLAN.md` that says what is different this time (objective, ansatz, power, scale)
and which outcome would change the estimate. An unchanged re-run at a similar budget is expected to repeat the
result, so it scores D = 0 and does not pass the gate.

| Method | Measured yield | What would make a new run informative |
|---|---|---|
| Genus ladder / arch / glad climbing (DR1) | genus 3 for 4 types, genus 4 never, nights 3-5 | a handle choice that passes the Gauss gate (k_tau = -1), or a new type |
| Normals-first / k-drift climbing (DR2) | 12,202 UNSAT, 0 SAT, ~150 core-h; low power | E02 shows the control is SAT often enough |
| Closure-first pdefect / sdefect (DR4) | zero defects only with >= 11 non-simple faces | face simplicity inside the model |
| Black-box engines on the pair energy (DR6) | n = 7 solved; plateau at n = 8 and genus 4 | a different objective (e.g. with Gauss-class terms), not more seeds |
| Near-miss repair (DR5) | all 1005 near-misses in the wrong Gauss class (FD11) | a near-miss in the right class |
| Gauss clauses as a SAT speed-up (DR16) | no speed-up observed | - |
| Asymmetric immersion instances without cubing (DR8) | 8/8 timeouts at 2.2 h | cube-and-conquer (E11) |

## Decision point

After E01-E04 and E06: either (a) E11 then a certified campaign (cloud or Actions matrix), or (b) publish the shareable
results and change the class of geometric ansatz, or (c) stop with a written negative report. Decide from the
evidence, not from sunk cost.
