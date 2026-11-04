# Roadmap: the experiment queue

**Focus since 2026-11-03** (`STRATEGY.md`): the focus target is S5 at (9, 3), stretch (10, 4); S0 is parked, not
abandoned. The S5 queue below was proposed by `reviews/strategy-review-2026-11-03.md` and approved by the owner on
2026-11-03; the S0 queue follows it, parked as it stood.

As of 2026-11-04. Principle: **theory and a cheap filter first -> a discriminating experiment -> an exact
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

## Queue: focus target S5 (approved 2026-11-03)

Proposed by `reviews/strategy-review-2026-11-03.md` (sections 2-3) and approved by the owner on 2026-11-03. Order rule:
the combinatorics first (the candidate maps are the input of every engine), then the exact route (encoder, then the
decision per map: (8, 2) in hours, the symmetric (9, 3) maps, then all admissible ones), with the heuristic engines as
explore runs (one run in two, `STRATEGY.md` section 2) behind pilots with stated kill criteria. Every row is a `planned`
folder; its `PLAN.md` is written and committed before any compute (skill `experiment-start`). Candidate maps, counts
and labels: `STATUS.md` section 3c.

| ID | State | Tests | Question | T D F G R | Budget | Stop rule |
|---|---|---|---|---|---|---|
| [E-261103-01](experiments/E-261103-01-s5-map-census/) | done | H-261103-01, H-261101-07 | **Completed E-261103-01** (EXACT computation, coverage PROVED-1; see CONCLUSION). Census of the candidate maps for (7, 1), (8, 2), (9, 3), (10, 4) (dual triangular maps with multiple edges, underlying K_F) with admissibility (distinct corner triples) and automorphism data, output in `links` format; controls: (7, 1) = 1 class, (12, 6) = 59 types with the FD3 orders, every sampled class of the review contained, the two (8, 3) maps contained if that case finishes | 2 2 2 2 2 | 2 sessions, minutes-hours of CPU | the four censuses with every control, or a written reason why a case does not finish |
| [E-261103-02](experiments/E-261103-02-s5-omsat-multi-adjacency-encoder/) | done | - | Completed E-261103-02 (EXACT controls, soundness PROVED-1; see CONCLUSION). OM-SAT encoder for multiple adjacencies and F != 12 (Lemma 5.1 with m shared segments per pair; symmetric clauses for C3 / C2 / D3); validated on the Roest-Vigh and Mizhaev chirotopes (SAT, 0 predicate mismatches on random perturbations) with both negative controls; `ladder_exact.verify` repeated-corner guard tested. Free C2/C3 calibrated; uniform fixed-face C2/D3 UNSAT is not a geometric exclusion | 2 2 2 2 2 | 1-2 sessions | the controls pass and the first (8, 2) instance is built, or a written obstruction |
| [E-261103-03](experiments/E-261103-03-s5-exact-decision-8-2-9-3/) | running | H-261103-03, H-261103-02, H-261101-07 | (8,2) stage completed (see CONCLUSION; exact formula decisions, geometric scope PROVED-1). Paired (9,3) pilot completed (CONCLUSION / STATUS 3e); wider plain coverage unresolved. Autonomous 60/300-second grid completed (CONCLUSION / STATUS 3f); new-map tranche activated and same-path pilot concluded (STATUS 3h); owner-run tranche concluded (STATUS 3i), LOW-YIELD; broader census goal incomplete, no automatic expansion. Exact decision per map: the 2 (8, 2) maps (9 elements, plain and C2), the 8 C3 (9, 3) maps with C3 clauses, the 24 C2 maps via asymmetric formulas unless a nonuniform symmetry extension is supplied (fixed-face C2/D3 uniform UNSAT is not a geometric exclusion), then all 203 admissible (9, 3) maps; realizers and final polynomials on every model; CNF + DRAT kept; a realized model goes to `candidate-check` and `--target S5` | 2 2 2 2 2 | hours for (8, 2); one night for (9, 3) | every map decided (UNSAT-VERIFIED / realized / NONREALIZABLE-EXACT / listed timeout), or median SAT time above ~1 h per (9, 3) map |
| [E-261103-04](experiments/E-261103-04-s5-genus-ladder-9-faces/) | running | H-261101-07, H-261103-02 | **Explore.** Legacy representation gate failed (STATUS 3j); replacement dart-preserving surgery gate passed (CONCLUSION / STATUS 3k, PROVED-1). Geometric recovery pilot concluded UNDERPOWERED (CONCLUSION / STATUS 3l). Conditional failed-level grid registered and startup-checked (STATUS 3m), awaiting owner authorization; no active optimizer. Focus geometry/night remain gated. Genus ladder on 9 faces: every admissible (9, 3) map from its sphere down (`tubes`) and up again with `genus_ladder.search`, exact verifier per level, `--target S5` at the top; controls R1 and the two (8, 3) maps through the same ladder; what is different from DR1: a genus-3 target below the ravine, 9 faces, all pairs adjacent | 1 2 2 1 2 | one night, 10 cores, many seeds x short budgets | the night, or the first S5 PASS |
| [E-261103-05](experiments/E-261103-05-s5-symmetric-solid-first/) | done | H-261103-02, H-261101-07 | **Explore pilot completed**, BENCHMARK-PASS (CONCLUSION / STATUS 3g); R2/R3 achieved, target/night not activated. Broader proposal: symmetric solid-first (the Roest-Vigh route): C3 / D3 / C2 arrangements of 9 planes, the CP-SAT inner solver extended to 1-3 edge runs per pair; gates R2 (the known planes give the known objects) and R3 (rediscover an (8, 3) object from random D2 / S4 planes in a session) | 2 2 2 1 2 | 1 session; one night only if R3 passes | R2, R3, then the night or the first 36-pair solid |
| [E-261103-06](experiments/E-261103-06-embedded-first-pilot/) | open | H-261101-07 | **Explore.** Embedded first, planar later (I-261103-01): R1 Szilassi from a torus, then an (8, 3) object from a smooth genus-3 surface; kill: the planarity energy plateaus above zero on R1 with the barrier active | 1 2 2 2 1 | 1-2 sessions | R1 and R2' converge (then a pre-registered (9, 3) night), or R1 fails |
| [E-261101-11](experiments/E-261101-11-external-human-review/) | open | FD5, FD6 | Owner's e-mails (zero compute): the S5 letter to Roest-Vigh and Mizhaev (have they tried (8, 2) or (9, 3); their method; an offer of the map census), and the S0 letters as before | 2 2 1 1 2 | 0 | a reply, or 4 weeks |
| [E-261103-07](experiments/E-261103-07-s5-10-4-census-symmetry/) | open | H-261101-07 | Symmetric stretch preparation from the completed (10, 4) census of E-261103-01 (STATUS 3c; do not repeat its enumeration); preparation of the stretch, no geometry before (9, 3) is decided | 1 2 2 2 2 | minutes-hours of CPU | the census, or a written reason |

S0 items kept alive at low cost while the focus has no result: E-261101-11 (the first `polyhedraproof` e-mail), E-261101-10
(the FD6 write-up, one session per two weeks), E-261101-09 step 1 (predicate equality; it also audits the shared predicates
of the S5 encoder), E-261101-06 (rank-3 SAT, built in its 9-element form first as a filter for E-261103-03). Everything
else in the S0 queue is parked, not dropped.

## S0 queue (parked 2026-11-03, not dropped)

Kept as it stood at parking time (`STRATEGY.md` section 1: S0 resumes when the owner says so or when a focus result
transfers). States are maintained; no S0 night run starts without a new strategy decision.

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
| [E-261101-26](experiments/E-261101-26-engine-benchmark-ladder/) | done | H-261101-17, H-261101-10 | Closed for S0 on 2026-11-03 (strategy review: R4 is the wall; the S5 rungs R2 / R3 and the (8, 2) maps are controls inside E-261103-04 and E-261103-05). Two engines scored (STATUS 3b): chirotope-first (2026-11-02, cap lifted 2026-11-03 by E-261102-03) and the genus-ladder search (E-261102-04); both fail R4, only genus-ladder passes R5. R4 is the first rung where every scored engine fails (the stop rule's second branch, reached for the engines scored so far); next: another engine only with a stated reason it could pass R4. Engine benchmark ladder: Szilassi from random, the 8-face objects from their planes and from random symmetric planes, a genus-3 witness from random and from its parent, k-face sub-instances; every construction engine scored here before the target (I-261101-22) | 1 2 2 2 2 | 1-2 days harness, one night per engine | all engines scored, or the first rung where every engine fails |
| [E-261102-03](experiments/E-261102-03-chirotope-alt-cap-or-wall/) | done | H-261101-17 | Chirotope-first on R4 / R5 / R6k k = 8, 9 with the alternation cap lifted, so the time budget binds: is the full-map frontier of E-261101-26 a cap or a wall? Grid over the budget per seed (40, 120 min) | 1 2 2 1 2 | day pilot ~1 h (1 seed); night ~45 core-h | the grid, or the first R4 / R5 success (`candidate-check`); decides E-261102-02 |
| [E-261102-04](experiments/E-261102-04-genus-ladder-engine-score/) | done | H-261101-10 | The genus-ladder search (`genus_ladder.search`, the engine of the 94 archived genus-3 realizations) scored on the same ladder tasks (R1, R4, R5): a second row of the engine-score table | 1 2 2 1 2 | ~2 h harness option + day pilot; night shared with E-261102-03 (~30 core-h) | all units of R1, R4, R5 |
| [E-261102-01](experiments/E-261102-01-kface-sweep-completion/) | done | H-261101-15, H-261101-02, H-261101-12 | Completion of the k-face sweep of E-261101-23 (night 6 hung in the final-polynomial LP): the 32 types not reached at k = 8, 9 on the greedy face set, with the LP time limit and stored final-polynomial certificates; k = 10 only with a longer timeout; a second face set per type if k = 9 is SAT | 2 2 2 2 2 | laptop, daytime, 8 shards (~1.5 h) | all 32 types at k = 8, 9, or the first UNSAT (drat-trim, hashes, the same face set on every type) |
| [E-261102-02](experiments/E-261102-02-chirotope-first-night2/) | killed | H-261101-17, H-261101-12, H-261101-01 | Killed 2026-11-03 before any run (E-261102-03: full map a wall at <= 120 min, k = 7 expected). Was blocked because in E-261101-26 every seed stopped at the 20-alternation cap, so this night would end in ~2.5 h with a predictable k = 7 outcome. Night run 2 of the chirotope-first engine (E-261101-25 night 6 was cut by the LP hang and `--rounds 12`): LP time limit, `--rounds 40`, a cap inside each step, all 10 seed slices, certificates stored; launched only after E-261101-26 has scored the engine (PROTOCOL 8a) | 2 2 2 2 2 | one laptop night, 10 shards | the night, or the first realized 12-face model (`candidate-check`), or 20 seeds ending ROUNDS at 40 rounds |
| [E-261101-06](experiments/E-261101-06-rank3-sat-per-type/) | open | H-261101-02, H-261101-03, DR9 | Rank-3 (normals-only) SAT per type with degree, exact covering on the chambers of the 66 great circles, saddle and face-winding clauses; model counts; the 44 vertex-type patterns as the cube basis | 2 2 2 2 2 | 1 day coding, minutes per type | per type: UNSAT (proof!) or a model count estimate; stop after 3 types if every one is SAT with no pruning |
| [E-261101-21](experiments/E-261101-21-fold-locus-controls/) | open | H-261101-14 | The Gauss map as a fold map: the identity on the controls and the archive, its proof, and its clause form for E-261101-06 and the cubes of E-261101-15 | 1 2 2 2 2 | 1 session | an identity with proof and clause form, or a written "already implied" |
| [E-261101-22](experiments/E-261101-22-equivelar-literature/) | open | - | Demoted 2026-11-03: the S5 objects at (8, 2)-(11, 5) are non-equivelar (2E/F is not an integer), so the equivelar reads cannot contain them; the S5 letter to Roest-Vigh and Mizhaev moved to E-261101-11. Step 0 done 2026-11-01 (`literature/primary-reads-2026-11-01.md`: the "empty set" sentence is the vertex version; the face version is open in print; both 8-face objects have 4 convex vertices). Remaining: equivelar {p,3} polyhedra (McMullen-Schulz-Wills, Brehm-Wills, Schulte-Wills 1985 and 2012), Bokowski-Schewe 2002, Arseneva et al. 2024 | 1 2 2 1 1 | 1 literature session | the sources read with exact statements, or two sessions |
| [E-261101-18](experiments/E-261101-18-face-grouped-mus-symmetric/) | open | H-261101-11, H-261101-02 | Face-grouped minimal unsatisfiable cores of the 50 certified symmetric instances; recurring small cores feed E-261101-23 | 2 2 2 2 2 | ~30 core-h (one night) after a one-session pilot | all 50 cores, or 10 cores with no pattern below 10 faces |
| [E-261101-09](experiments/E-261101-09-encoding-comparison/) | open | H-261101-06, DR8 | Encoding comparison with `pirozhkov-andrei/polyhedraproof`: predicate equality on random exact configurations first, timings second; map their two refuted formulas to our types | 1 2 1 1 2 | 1 day | predicate agreement or a named disagreement (which stops campaign work until resolved); time per instance for both |
| [E-261101-11](experiments/E-261101-11-external-human-review/) | open | FD5, FD6, E-261101-03 | External human review: first e-mail to the `polyhedraproof` author (three shared symmetric instances with CNF hashes, one question), then Bokowski / Brehm with FD5, FD6, Lemma A and the dossier; since 2026-11-03 also the S5 letter to Roest-Vigh and Mizhaev (S5 queue above) | 2 2 1 1 2 | owner's e-mail, no compute | a reply, or 4 weeks without one -> next reviewer |
| [E-261101-16](experiments/E-261101-16-arrangement-first-chamber-sat/) | open | H-261101-08, H-261101-10 | The S5 form is E-261103-05 (2026-11-03); this row keeps the S0 form (a symmetric arrangement with an asymmetric solid), parked. Arrangement first: exact chamber-SAT (disk condition encoded exactly) on G-symmetric arrangements with asymmetric solids allowed, on the 247 archived arrangements, on the 1005 near-miss arrangements and on normals realized from E-261101-06 / -23 models | 2 2 2 1 2 | one night (~20 core-h) | the night ends, or the first solid with >= 54 pairs (then `candidate-check`) |
| [E-261101-24](experiments/E-261101-24-farkas-descent-pilot/) | open | H-261101-16, H-261101-09 | Farkas-certificate descent: the exact dual gradient of offset infeasibility moves the normals (what is different from DR2/DR4: guided, not annealed); pilot on the 80 radius-0 seeds and a perturbed witness | 2 2 2 1 2 | 1 day coding, ~5 core-h | 50 steps per seed, or the first exact S3 object at a level where sampling found none; positive control first |
| [E-261101-19](experiments/E-261101-19-barrier-continuation-genus3-handle/) | open | H-261101-10, H-261101-03 | Barrier continuation inside the genus-3 realization space towards an in-class handle, with a measure that can go negative (replaces E-261101-07) | 2 2 1 2 2 | 1 core-h pilot, then one night (40 realizations) | all extendable arms of 40 realizations, or the first exact genus-4 object |
| [E-261101-17](experiments/E-261101-17-realization-space-geometry/) | open | H-261101-09, H-261101-10 | Geometry of the realization spaces: chord widths by hit-and-run, offsets and normals separately, shrinkage per handle, connectivity of the type-15 archive | 1 2 2 1 2 | ~10 core-h | 10 realizations x 2,000 steps and the pairwise segment tests |
| [E-261101-15](experiments/E-261101-15-cube-and-conquer-pilot/) | open | H-261101-06, H-261101-01, H-261101-12 | Cube-and-conquer pilot on one trivial-Aut type as an Actions matrix, cubes on the 44 vertex-type bits pruned by E-261101-21, LRAT checked on the fly (after E-261101-09 agreement) | 2 2 1 1 2 | ~300 core-h of Actions | one type decided, or the matrix exhausted; report refuted fraction per core-hour and proof-handling cost |
| [E-261101-10](experiments/E-261101-10-write-up-symmetric-immersion/) | open | FD6, H-261101-13 | Write-up: no symmetric immersion (second encoder, soundness proofs, archived certificates, Lemma A for improper isometries reviewed or the statement restricted to rotations) | 2 1 1 1 2 | 2-3 sessions | arXiv-ready draft reviewed by `adversarial-verifier` (a filter) and one human |
| [E-261101-03](experiments/E-261101-03-type0-dossier/) | open | H-261101-05, FD10 | Type-0 genus-3 dossier: the owner's independent second verifier first, then canonical form, certificate re-run, novelty search | 1 2 2 1 2 | 1-2 sessions, no compute | stop after the 5 steps or 2 sessions; any verifier mismatch -> fix FD10 first |
| [E-261101-20](experiments/E-261101-20-incremental-sat-across-types/) | open | H-261101-06 | One incremental SAT session for the 25 symmetric instances with selector literals: do shared GP lemmas cut the total time? | 1 2 2 1 2 | a few core-h | two orders; below 1.5x closes it, above 2x makes it the campaign default |
| [E-261101-08](experiments/E-261101-08-relaxed-s1-twelve-faces/) | open | H-261101-07, DR12 | Relaxed S1 target, a goal in itself: 12 faces, three doubled pairs as one C3 orbit (genus 7, the smallest S1 case), after Roest-Vigh calibration | 1 2 2 1 2 | 2 nights max, <= 25 % of compute | calibration fails -> fix engine, do not run n = 12 |
| [E-261101-12](experiments/E-261101-12-maximal-face-neighbourly/) | open | H-261101-07, DR12, DR15 | Umbrella row of the focus, split on 2026-11-03 into E-261103-01 to -07 (S5 queue above). **Focus target since 2026-11-03 (`STRATEGY.md`): (9, 3) first, stretch (10, 4)** (SPEC S5, `--target S5`); the strategy review splits this row into experiments. Maximal face-neighbourly cubic polyhedra per genus, (F, g) = (8, 2), (9, 3), (10, 4), (11, 5) with 2, 3, 3, 2 doubled pairs; (8, 2) only as a warm-up if it calibrates the (9, 3) method; symmetric ansatzes first (black-box engines were underpowered there) | 1 2 2 2 2 | literature 1 session; then 1 night per case | (9, 3): an S5 PASS (`candidate-check`), or every map tried UNSAT with a written power statement; then (10, 4) under the same rule |

Done or merged this cycle: [E-261102-03](experiments/E-261102-03-chirotope-alt-cap-or-wall/) (done 2026-11-03, night 7: full-map frontier unchanged with the cap lifted, 0/12 at 120 min, R6k k = 8, 9 4/4 each) and [E-261102-04](experiments/E-261102-04-genus-ladder-engine-score/) (done 2026-11-03, night 7: genus-ladder search, R4 0/14, R5 5/10 at 6 min); [E-261102-02](experiments/E-261102-02-chirotope-first-night2/) (killed 2026-11-03 before any run, by the pre-registered rule of E-261102-03); [E-261101-23](experiments/E-261101-23-k-face-subinstances-face-cegar/) and [E-261101-25](experiments/E-261101-25-chirotope-first/) (done 2026-11-02, night 6, both UNDERPOWERED: a final-polynomial LP without a time limit hung 9 of 10 shards; follow-ups E-261102-01, -02); [E-261102-01](experiments/E-261102-01-kface-sweep-completion/) (done 2026-11-02, LOW-YIELD@4.2 core-h for exclusion on the greedy face set at k <= 9, UNDERPOWERED for realization); [E-261101-07](experiments/E-261101-07-pinned-hemisphere-margin/) (done, verdict ARTEFACT:
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
| Genus ladder / arch / glad climbing (DR1) | genus 3 for 4 types, genus 4 never, nights 3-5 | a handle choice that passes the Gauss gate (k_tau = -1), or a new type; or a target below the ravine: the 9-face ladder E-261103-04 (explore, 2026-11-03) |
| Normals-first / k-drift climbing (DR2) | 12,202 UNSAT, 0 SAT, ~150 core-h; low power | E-261101-04 shows the control is SAT often enough |
| Closure-first pdefect / sdefect (DR4) | zero defects only with >= 11 non-simple faces | face simplicity inside the model |
| Black-box engines on the pair energy (DR6) | n = 7 solved; plateau at n = 8 and genus 4 | a different objective (e.g. with Gauss-class terms), not more seeds |
| Near-miss repair (DR5) | all 1005 near-misses in the wrong Gauss class (FD11) | a near-miss in the right class |
| Gauss clauses as a SAT speed-up (DR16) | no speed-up observed | - |
| Asymmetric immersion instances without cubing (DR8) | 8/8 timeouts at 2.2 h | cube-and-conquer (E-261101-15) |

## Decision point

Three scenarios with explicit credences (idea I-261101-17; all CONJECTURE, set 2026-11-01 by the strategy review,
updated by `experiment-conclude` from the "scenario move" line of each `PLAN.md`):

S0 table (unchanged 2026-11-03: no S0 evidence since 2026-11-01):

| Scenario | Credence | What raises it | What lowers it |
|---|---|---|---|
| A: a realization exists | 0.20 | any S3 object of genus >= 4 (E-261101-16, -19); a realizable OM model | per-type OM-UNSAT (E-261101-15); H-261101-10 supported |
| B: all 59 types are OM-UNSAT (as in the vertex version) | 0.55 | a rank-3 UNSAT (E-261101-06); a decided type (E-261101-15); small recurring cores (E-261101-18) | any OM-SAT model |
| C: some types are OM-SAT with only non-realizable models | 0.25 | an OM-SAT model that fails the realizability audit (I-261029-57) | per-type OM-UNSAT |

S5 table (set 2026-11-03 by the strategy review, all CONJECTURE; "cannot tell" = not decided within the strategy's
horizon by our tools; moved by the "scenario move" lines of the E-261103 PLANs):

| Case | exists | does not exist | cannot tell | Evidence in one line |
|---|---|---|---|---|
| (9, 3) | 0.40 | 0.35 | 0.25 | 203 admissible maps (many tickets); at (8, 3) the two known objects are 2 of >= 22,666 maps, so realizable maps may be rare; 10-element OM instances are small, so "cannot tell" is bounded by the realizability stage |
| (8, 2) | 0 | 1 | 0 | E-261103-03: both plain formulas UNSAT-VERIFIED; conditional on PROVED-1 census coverage and encoder soundness, not human-reviewed theorem certainty |
| (10, 4) | 0.30 | 0.30 | 0.40 | several hundred maps, almost no symmetry in the sample, no engine pass at genus 4 |

Rules for S5: both (8, 2) and (9, 3) decided non-existent -> write the note, focus moves to (10, 4) with E-261103-07;
(9, 3) exists -> the stretch starts from the method that found it; E-261103-03 stalls on models that neither realize nor
certify -> build the realizability stage (I-261029-57) before more SAT.

Exploration quota (I-261101-22): while the focus target has no result, one run in two is drawn from the mutation pool
(a parked method with one stated change, a re-scored below-gate row, or a new idea), logged as "explore" (`STRATEGY.md`
section 2; PROTOCOL 8a's default is one in four). No construction engine runs on the target before it is scored on the
benchmark ladder: for S5 the rungs are R2 / R3 (the 8-face objects) and the (8, 2) maps, as controls inside E-261103-04
and E-261103-05.

Rules. After E-261101-06, -18, -16, -19 and -17: if B >= 0.7, run the certified campaign (E-261101-15 scaled to all
types, with `polyhedraproof` if they agree on predicates); if A >= 0.35, put the constructive items first (the
arrangement or the path that raised it); if C >= 0.4, build the realizability stage before more SAT; otherwise
publish the shareable results (`STATUS.md` section 5) and re-plan. Decide from the table, not from sunk cost.
