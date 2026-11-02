# Roadmap: the experiment queue

As of 2026-11-02. Principle: **theory and a cheap filter first -> a discriminating experiment -> an exact
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
* `verification/verify_all.py` (one command, 14 checks) and `verify_candidate.py` (any file format, `--target S0` = the solution check); CI on every push.
* `requirements.txt` pinned; hard-coded `/home/user` paths removed.
* Experiment template and GitHub Actions runner (`experiments/_template/`, `.github/workflows/experiment.yml`).
* DRAT certificates of `sym` / `symimm`: the night runs had deleted them after checking (no `--keep-proofs`).
  Regenerated 2026-11-01 with `--keep-proofs --keep-cnf`: all 50 CNFs and all 50 proofs are bit-identical to the
  SHA-256 recorded in the `results/{sym,symimm}/results.jsonl` of E-261029-13 and E-261029-15, 50/50 re-VERIFIED by drat-trim. Packed as
  `symmetric-{sym,symimm}-drat.tar.xz` (422 MB, 438 MB) and published on the GitHub release `state-2026-11-01`;
  hashes, versions and how to check: `verification/certificates/symmetric_drat/`. TODO (owner): Zenodo DOI via
  the GitHub-Zenodo integration before any write-up.
* TODO (owner): e-mail to the author of `pirozhkov-andrei/polyhedraproof` (E-261101-11). Why: he reduced exactly
  our problem to 59 SAT formulas independently and asks for collaborators; two encoders that agree predicate by
  predicate on random exact configurations are the cheapest strong evidence for the soundness of FD2/FD4 (today
  PROVED-1 by AI sessions); his two refuted formulas, if their certificates are shared, exclude two types for us at
  no cost; a shared campaign halves the ~19,000 core-h; otherwise the impossibility side may be settled without
  us. Content: three shared symmetric instances with CNF hashes, the predicate-equality harness
  (`code/omsat_validate.py`), one question. Second contact: Roest and Vigh (Szeged), who found the 8-face objects
  with an AI-assisted search and say the 12-face case is open.
* Tag `state-2026-11-01` = `main` after merging this restructure; witnesses and site lab models (`witnesses/`).
* Research graph: one file per idea / hypothesis / experiment with dated IDs (`PROTOCOL.md` §4), past work
  reconstructed as experiments with their data, `verification/trace.py` (in `verify_all`), interactive `map/`.
* TODO (infrastructure, from the 2026-11-01 process audit; each passes the infrastructure filter of `PROTOCOL.md` §3):
  * `lint_docs.py` in `verify_all`: STATUS levels are SPEC labels, ROADMAP rows have T + D >= 3, every backticked
    path in the control documents exists; `experiment.yml` accepts only `E-YYMMDD-NN` ids.
  * `verify_all` runs the verifier's mutation tests (`verification/test_mutants.py`) and re-encodes 2-3 symmetric
    instances to compare their CNF SHA-256 with the certificate records (proves HEAD still builds the certified
    formulas).
  * READMEs link to `STATUS.md` instead of repeating numbers.
  * Pilot the GitHub Actions runner on E-261101-16 or E-261101-18 (small matrix) before relying on it.
  * `lint_docs.py` also checks that every new `PLAN.md` has the counter-calibration and scenario-move lines (template
    changed 2026-11-01 after `reviews/strategy-review-2026-11-01.md`).

## Queue

Order rule (revised 2026-11-01, evening, after the strategy review and its follow-up): first the two cheap
experiments that are decisive on both branches at the combinatorial level (E-261101-23 k-face sub-instances, which
are monotone in the faces, and E-261101-06 rank-3), with the theory session that sharpens both (E-261101-21) and the
primary reads that could change everything (E-261101-22); then the certified-core mining and the encoder agreement
(E-261101-18, -09, -11); then the three tests of whether the constructive plateau is geometry or artefact
(E-261101-16, -24, -19, -17); then the exact campaign pilot (E-261101-15), the write-up and the hygiene; the
constructive side line last. IDs are permanent. Every row is a `planned` experiment folder (its README header holds
origin, hypotheses and links; the map shows them). State: `open` / `running` / `done` / `killed` / `blocked`;
`experiment-conclude` updates the State here and the `status` in the folder. Each folder's README has a starting
point written for execution by a smaller model; the `PLAN.md` (counter calibration and scenario move included) is
filled and committed before any compute.

| ID | State | Tests | Question | T D F G R | Budget | Stop rule |
|---|---|---|---|---|---|---|
| [E-261101-26](experiments/E-261101-26-engine-benchmark-ladder/) | open | H-261101-17, H-261101-10 | First scope done 2026-11-02 (chirotope-first scored on all 80 units, frontier R4 / R5: STATUS 3b); next: the other engines on the same `tasks.json`. Engine benchmark ladder: Szilassi from random, the 8-face objects from their planes and from random symmetric planes, a genus-3 witness from random and from its parent, k-face sub-instances; every construction engine scored here before the target (I-261101-22) | 1 2 2 2 2 | 1-2 days harness, one night per engine | all engines scored, or the first rung where every engine fails |
| [E-261102-03](experiments/E-261102-03-chirotope-alt-cap-or-wall/) | running | H-261101-17 | Chirotope-first on R4 / R5 / R6k k = 8, 9 with the alternation cap lifted, so the time budget binds: is the full-map frontier of E-261101-26 a cap or a wall? Grid over the budget per seed (40, 120 min) | 1 2 2 1 2 | day pilot ~1 h (1 seed); night ~45 core-h | the grid, or the first R4 / R5 success (`candidate-check`); decides E-261102-02 |
| [E-261102-04](experiments/E-261102-04-genus-ladder-engine-score/) | open | H-261101-10 | The genus-ladder search (`genus_ladder.search`, the engine of the 94 archived genus-3 realizations) scored on the same ladder tasks (R1, R4, R5): a second row of the engine-score table | 1 2 2 1 2 | ~2 h harness option + day pilot; night shared with E-261102-03 (~30 core-h) | all units of R1, R4, R5 |
| [E-261102-01](experiments/E-261102-01-kface-sweep-completion/) | done | H-261101-15, H-261101-02, H-261101-12 | Completion of the k-face sweep of E-261101-23 (night 6 hung in the final-polynomial LP): the 32 types not reached at k = 8, 9 on the greedy face set, with the LP time limit and stored final-polynomial certificates; k = 10 only with a longer timeout; a second face set per type if k = 9 is SAT | 2 2 2 2 2 | laptop, daytime, 8 shards (~1.5 h) | all 32 types at k = 8, 9, or the first UNSAT (drat-trim, hashes, the same face set on every type) |
| [E-261102-02](experiments/E-261102-02-chirotope-first-night2/) | blocked | H-261101-17, H-261101-12, H-261101-01 | Blocked until E-261102-03 decides: in E-261101-26 every seed stopped at the 20-alternation cap, so this night would end in ~2.5 h with a predictable k = 7 outcome. Night run 2 of the chirotope-first engine (E-261101-25 night 6 was cut by the LP hang and `--rounds 12`): LP time limit, `--rounds 40`, a cap inside each step, all 10 seed slices, certificates stored; launched only after E-261101-26 has scored the engine (PROTOCOL 8a) | 2 2 2 2 2 | one laptop night, 10 shards | the night, or the first realized 12-face model (`candidate-check`), or 20 seeds ending ROUNDS at 40 rounds |
| [E-261101-06](experiments/E-261101-06-rank3-sat-per-type/) | open | H-261101-02, H-261101-03, DR9 | Rank-3 (normals-only) SAT per type with degree, exact covering on the chambers of the 66 great circles, saddle and face-winding clauses; model counts; the 44 vertex-type patterns as the cube basis | 2 2 2 2 2 | 1 day coding, minutes per type | per type: UNSAT (proof!) or a model count estimate; stop after 3 types if every one is SAT with no pruning |
| [E-261101-21](experiments/E-261101-21-fold-locus-controls/) | open | H-261101-14 | The Gauss map as a fold map: the identity on the controls and the archive, its proof, and its clause form for E-261101-06 and the cubes of E-261101-15 | 1 2 2 2 2 | 1 session | an identity with proof and clause form, or a written "already implied" |
| [E-261101-22](experiments/E-261101-22-equivelar-literature/) | open | - | Step 0 done 2026-11-01 (`literature/primary-reads-2026-11-01.md`: the "empty set" sentence is the vertex version; the face version is open in print; both 8-face objects have 4 convex vertices). Remaining: equivelar {p,3} polyhedra (McMullen-Schulz-Wills, Brehm-Wills, Schulte-Wills 1985 and 2012), Bokowski-Schewe 2002, Arseneva et al. 2024 | 1 2 2 1 1 | 1 literature session | the sources read with exact statements, or two sessions |
| [E-261101-18](experiments/E-261101-18-face-grouped-mus-symmetric/) | open | H-261101-11, H-261101-02 | Face-grouped minimal unsatisfiable cores of the 50 certified symmetric instances; recurring small cores feed E-261101-23 | 2 2 2 2 2 | ~30 core-h (one night) after a one-session pilot | all 50 cores, or 10 cores with no pattern below 10 faces |
| [E-261101-09](experiments/E-261101-09-encoding-comparison/) | open | H-261101-06, DR8 | Encoding comparison with `pirozhkov-andrei/polyhedraproof`: predicate equality on random exact configurations first, timings second; map their two refuted formulas to our types | 1 2 1 1 2 | 1 day | predicate agreement or a named disagreement (which stops campaign work until resolved); time per instance for both |
| [E-261101-11](experiments/E-261101-11-external-human-review/) | open | FD5, FD6, E-261101-03 | External human review: first e-mail to the `polyhedraproof` author (three shared symmetric instances with CNF hashes, one question), then Bokowski / Brehm with FD5, FD6, Lemma A and the dossier | 2 2 1 1 2 | owner's e-mail, no compute | a reply, or 4 weeks without one -> next reviewer |
| [E-261101-16](experiments/E-261101-16-arrangement-first-chamber-sat/) | open | H-261101-08, H-261101-10 | Arrangement first: exact chamber-SAT (disk condition encoded exactly) on G-symmetric arrangements with asymmetric solids allowed, on the 247 archived arrangements, on the 1005 near-miss arrangements and on normals realized from E-261101-06 / -23 models | 2 2 2 1 2 | one night (~20 core-h) | the night ends, or the first solid with >= 54 pairs (then `candidate-check`) |
| [E-261101-24](experiments/E-261101-24-farkas-descent-pilot/) | open | H-261101-16, H-261101-09 | Farkas-certificate descent: the exact dual gradient of offset infeasibility moves the normals (what is different from DR2/DR4: guided, not annealed); pilot on the 80 radius-0 seeds and a perturbed witness | 2 2 2 1 2 | 1 day coding, ~5 core-h | 50 steps per seed, or the first exact S3 object at a level where sampling found none; positive control first |
| [E-261101-19](experiments/E-261101-19-barrier-continuation-genus3-handle/) | open | H-261101-10, H-261101-03 | Barrier continuation inside the genus-3 realization space towards an in-class handle, with a measure that can go negative (replaces E-261101-07) | 2 2 1 2 2 | 1 core-h pilot, then one night (40 realizations) | all extendable arms of 40 realizations, or the first exact genus-4 object |
| [E-261101-17](experiments/E-261101-17-realization-space-geometry/) | open | H-261101-09, H-261101-10 | Geometry of the realization spaces: chord widths by hit-and-run, offsets and normals separately, shrinkage per handle, connectivity of the type-15 archive | 1 2 2 1 2 | ~10 core-h | 10 realizations x 2,000 steps and the pairwise segment tests |
| [E-261101-15](experiments/E-261101-15-cube-and-conquer-pilot/) | open | H-261101-06, H-261101-01, H-261101-12 | Cube-and-conquer pilot on one trivial-Aut type as an Actions matrix, cubes on the 44 vertex-type bits pruned by E-261101-21, LRAT checked on the fly (after E-261101-09 agreement) | 2 2 1 1 2 | ~300 core-h of Actions | one type decided, or the matrix exhausted; report refuted fraction per core-hour and proof-handling cost |
| [E-261101-10](experiments/E-261101-10-write-up-symmetric-immersion/) | open | FD6, H-261101-13 | Write-up: no symmetric immersion (second encoder, soundness proofs, archived certificates, Lemma A for improper isometries reviewed or the statement restricted to rotations) | 2 1 1 1 2 | 2-3 sessions | arXiv-ready draft reviewed by `adversarial-verifier` (a filter) and one human |
| [E-261101-03](experiments/E-261101-03-type0-dossier/) | open | H-261101-05, FD10 | Type-0 genus-3 dossier: the owner's independent second verifier first, then canonical form, certificate re-run, novelty search | 1 2 2 1 2 | 1-2 sessions, no compute | stop after the 5 steps or 2 sessions; any verifier mismatch -> fix FD10 first |
| [E-261101-20](experiments/E-261101-20-incremental-sat-across-types/) | open | H-261101-06 | One incremental SAT session for the 25 symmetric instances with selector literals: do shared GP lemmas cut the total time? | 1 2 2 1 2 | a few core-h | two orders; below 1.5x closes it, above 2x makes it the campaign default |
| [E-261101-08](experiments/E-261101-08-relaxed-s1-twelve-faces/) | open | H-261101-07, DR12 | Relaxed S1 target, a goal in itself: 12 faces, three doubled pairs as one C3 orbit (genus 7, the smallest S1 case), after Roest-Vigh calibration | 1 2 2 1 2 | 2 nights max, <= 25 % of compute | calibration fails -> fix engine, do not run n = 12 |
| [E-261101-12](experiments/E-261101-12-maximal-face-neighbourly/) | open | H-261101-07, DR12, DR15 | Side line: maximal face-neighbourly cubic polyhedra per genus, (F, g) = (8, 2), (9, 3), (10, 4), (11, 5) with 2, 3, 3, 2 doubled pairs; start with (8, 2) and a two-orbit symmetric ansatz (black-box engines were underpowered there) | 1 2 2 2 2 | literature 1 session; then 1 night per case | stop at the first case that is UNSAT for every map tried with a written power statement, or after (9, 3) |

Done or merged this cycle: [E-261101-23](experiments/E-261101-23-k-face-subinstances-face-cegar/) and [E-261101-25](experiments/E-261101-25-chirotope-first/) (done 2026-11-02, night 6, both UNDERPOWERED: a final-polynomial LP without a time limit hung 9 of 10 shards; follow-ups E-261102-01, -02); [E-261102-01](experiments/E-261102-01-kface-sweep-completion/) (done 2026-11-02, LOW-YIELD@4.2 core-h for exclusion on the greedy face set at k <= 9, UNDERPOWERED for realization); [E-261101-07](experiments/E-261101-07-pinned-hemisphere-margin/) (done, verdict ARTEFACT:
the "pinned margin" was a floor of `gauss_gate.hemisphere_margin`; its real question is E-261101-19);
[E-261101-13](experiments/E-261101-13-exact-covering/) (killed: merged into E-261101-06, exact covering on chambers).

Below the gate (T + D < 3; run only after re-scoring with a written reason):

| ID | Question | T D F G R | Why below |
|---|---|---|---|
| [E-261101-04](experiments/E-261101-04-normals-first-power-study/) | Power of normals-first: how often is the *control* SAT at radius r? | 1 1 2 1 2 | re-scored 2026-11-01: the Wendel estimate (`reviews/fresh-eyes-review.md` 2.3) predicts the answer; run a 2 core-h check only if E-261101-17 finds widths comparable across genus |
| [E-261101-14](experiments/E-261101-14-chirotope-chambers/) | Chirotope chambers of the 247 archive realizations | 1 1 2 1 2 | descriptive; E-261101-17 measures the same spaces with a decision attached |

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

Three scenarios with explicit credences (idea I-261101-17; all CONJECTURE, set 2026-11-01 by the strategy review,
updated by `experiment-conclude` from the "scenario move" line of each `PLAN.md`):

| Scenario | Credence | What raises it | What lowers it |
|---|---|---|---|
| A: a realization exists | 0.20 | any S3 object of genus >= 4 (E-261101-16, -19); a realizable OM model | per-type OM-UNSAT (E-261101-15); H-261101-10 supported |
| B: all 59 types are OM-UNSAT (as in the vertex version) | 0.55 | a rank-3 UNSAT (E-261101-06); a decided type (E-261101-15); small recurring cores (E-261101-18) | any OM-SAT model |
| C: some types are OM-SAT with only non-realizable models | 0.25 | an OM-SAT model that fails the realizability audit (I-261029-57) | per-type OM-UNSAT |

Exploration quota (I-261101-22): one run in four is drawn from the mutation pool (a parked method with one stated
change, a re-scored below-gate row, or a new idea), logged as "explore". No construction engine runs on the target
before it is scored on the benchmark ladder (E-261101-26).

Rules. After E-261101-06, -18, -16, -19 and -17: if B >= 0.7, run the certified campaign (E-261101-15 scaled to all
types, with `polyhedraproof` if they agree on predicates); if A >= 0.35, put the constructive items first (the
arrangement or the path that raised it); if C >= 0.4, build the realizability stage before more SAT; otherwise
publish the shareable results (`STATUS.md` section 5) and re-plan. Decide from the table, not from sunk cost.
