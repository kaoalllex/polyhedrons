# Roadmap: the experiment queue

As of 2026-11-01. Principle: **theory and a cheap filter first -> a discriminating experiment -> an exact
solver -> a lemma or a certificate**. We do not try to enumerate the search space; we pick small, motivated
regions where one experiment can exclude a whole class or reveal a new constraint. How to run an item:
`PROTOCOL.md`. Current state: `STATUS.md`.

## Scoring (pre-registration)

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
  SHA-256 recorded in the `results/{sym,symimm}/results.jsonl` of E-261029-13 and E-261029-15, 50/50 re-VERIFIED by drat-trim. Packed as
  `symmetric-{sym,symimm}-drat.tar.xz` (422 MB, 438 MB) and published on the GitHub release `state-2026-11-01`;
  hashes, versions and how to check: `verification/certificates/symmetric_drat/`. TODO (owner): Zenodo DOI via
  the GitHub-Zenodo integration before any write-up.
* Tag `state-2026-11-01` = `main` after merging this restructure; witnesses and site lab models (`witnesses/`).

## Queue

Order rule: first the items that validate evidence the project already relies on (E-261101-03 checks the verifier and
the best witness, E-261101-04 checks whether 12,202 UNSATs mean anything); then by score sum, ties by lower cost. IDs are
permanent. Every row is a `planned` experiment folder (its README header holds origin, hypotheses and links; the
map shows them). State: `open` / `running` / `done` / `killed` / `blocked`; `experiment-conclude` updates the State
here and the `status` in the folder. E-261101-10 keeps its working notes in `proof-no-symmetric-immersion/`.
Each folder's README has the starting point; hypotheses and outcome meanings go in its `PLAN.md` before it runs.

| ID | State | Tests | Question | T D F G R | Budget | Stop rule |
|---|---|---|---|---|---|---|
| [E-261101-03](experiments/E-261101-03-type0-dossier/) | open | H-261101-05, FD10 | Type-0 genus-3 dossier: is the best positive result correct and new? | 1 2 2 1 2 | 1-2 sessions, no compute | stop after the 5 steps below or 2 sessions; any verifier mismatch -> fix FD10 first |
| [E-261101-04](experiments/E-261101-04-normals-first-power-study/) | open | H-261101-04, DR2 | Power of normals-first: how often is the *control* SAT at radius r? | 1 2 2 1 2 | ~10 core-h | 30 maps x 3 radii, or earlier if the rate is clear |
| [E-261101-05](experiments/E-261101-05-unsat-core-mining/) | open | H-261101-02, DR10 | Proof mining: what small cores make fixed-normal offset problems UNSAT? | 2 2 2 2 2 | ~5 core-h + theory | a core family explained, or 50 cores with no pattern |
| [E-261101-06](experiments/E-261101-06-rank3-sat-per-type/) | open | H-261101-02, H-261101-03, DR9 | Rank-3 (normals-only) SAT per type with degree / covering / saddle / face-winding clauses | 2 2 2 2 2 | 1 day coding, minutes per type | per type: UNSAT (proof!) or a model count estimate; stop after 3 types if every one is SAT with no pruning |
| [E-261101-07](experiments/E-261101-07-pinned-hemisphere-margin/) | open | H-261101-03, DR3 | Pinned hemisphere margin: why does every class-reaching drift end at margin 0? | 2 2 2 2 1 | 1 session theory + 1 core-h | stop after 1 session + the 1-h test: proof, counterexample, or written reason it is an artefact |
| [E-261101-08](experiments/E-261101-08-relaxed-s1-twelve-faces/) | open | H-261101-07, DR12 | Relaxed S1 target: 12 faces, doubled pairs, symmetric orbit ansatz, after Roest-Vigh calibration | 1 2 2 1 2 | 2 nights max, <= 25 % of compute | calibration fails -> fix engine, do not run n = 12 |
| [E-261101-09](experiments/E-261101-09-encoding-comparison/) | open | H-261101-06, DR8 | Encoding comparison with `pirozhkov-andrei/polyhedraproof` on shared instances | 1 2 1 1 2 | 1 day | conflicts / time per instance measured for both encoders |
| [E-261101-10](experiments/E-261101-10-write-up-symmetric-immersion/) | open | FD6 | Write-up: no symmetric immersion (second encoder, soundness proofs, archived certificates) | 2 1 1 1 2 | 2-3 sessions | arXiv-ready draft reviewed by `adversarial-verifier` (a filter) and one human |
| [E-261101-11](experiments/E-261101-11-external-human-review/) | open | FD5, FD6, E-261101-03 | External human review: send FD5/FD6 (CNF hashes, certificates) and the E-261101-03 dossier to Pirozhkov, Moki & Julio or Bokowski | 2 2 1 1 2 | owner's e-mail, no compute | a reply, or 4 weeks without one -> next reviewer |
| [E-261101-12](experiments/E-261101-12-maximal-face-neighbourly/) | open | H-261101-07, DR12, DR15 | Side line: maximal face-neighbourly cubic polyhedra per genus. All pairs adjacent and E = 3(F + 2g - 2) >= C(F, 2) give the largest F per genus: (F, g) = (8, 2), (9, 3), (10, 4), (11, 5), with 2, 3, 3, 2 extra edges beyond one per pair (doubled pairs); (12, 6) is Szilassi-12 itself. Which of them exist? Start with a literature check and (8, 2) | 1 2 2 2 2 | literature 1 session; then 1 night per case | stop at the first case that is UNSAT for every map tried with a written power statement, or after (9, 3) |

Below the gate (T + D < 3; run only after re-scoring with a written reason):

| ID | Question | T D F G R | Why below |
|---|---|---|---|
| [E-261101-13](experiments/E-261101-13-exact-covering/) | Exact covering: replace sampled covering by an exact check | 1 1 2 1 2 | no planned decision depends on it until E-261101-06 uses covering clauses; re-score then |
| [E-261101-14](experiments/E-261101-14-chirotope-chambers/) | Chirotope chambers of the 247 archive realizations | 1 1 2 1 2 | descriptive; no outcome changes the plan |

Conditional (only after E-261101-06 and E-261101-09): **E-261101-15 cube-and-conquer pilot** on 3 types (type 0, type 58, one trivial-Aut
type), one laptop night or GitHub Actions matrix; metric = refuted fraction per core-hour; campaign only if the
extrapolation is below ~2,000 core-hours per type.

## Parked methods (low measured yield, not refuted)

Tried, with little yield at the budget stated in `STATUS.md` §3 (LOW-YIELD rows). None is refuted, so none is
forbidden. A new run needs a `PLAN.md` that says what is different this time (objective, ansatz, power, scale)
and which outcome would change the estimate. An unchanged re-run at a similar budget is expected to repeat the
result, so it scores D = 0 and does not pass the gate.

| Method | Measured yield | What would make a new run informative |
|---|---|---|
| Genus ladder / arch / glad climbing (DR1) | genus 3 for 4 types, genus 4 never, nights 3-5 | a handle choice that passes the Gauss gate (k_tau = -1), or a new type |
| Normals-first / k-drift climbing (DR2) | 12,202 UNSAT, 0 SAT, ~150 core-h; low power | E-261101-04 shows the control is SAT often enough |
| Closure-first pdefect / sdefect (DR4) | zero defects only with >= 11 non-simple faces | face simplicity inside the model |
| Black-box engines on the pair energy (DR6) | n = 7 solved; plateau at n = 8 and genus 4 | a different objective (e.g. with Gauss-class terms), not more seeds |
| Near-miss repair (DR5) | all 1005 near-misses in the wrong Gauss class (FD11) | a near-miss in the right class |
| Gauss clauses as a SAT speed-up (DR16) | no speed-up observed | - |
| Asymmetric immersion instances without cubing (DR8) | 8/8 timeouts at 2.2 h | cube-and-conquer (E-261101-15) |

## Decision point

After E-261101-03 to E-261101-07: either (a) E-261101-15 then a certified campaign (cloud or Actions matrix), or (b) publish the shareable
results and change the class of geometric ansatz, or (c) stop with a written negative report. Decide from the
evidence, not from sunk cost.
