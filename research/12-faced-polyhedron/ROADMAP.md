# Roadmap: the experiment queue

**Focus since 2026-11-19** (`STRATEGY.md`, owner-approved `reviews/strategy-review-2026-11-19.md`): nine mutually
adjacent faces (S1, genus free) first, on the two uniform symmetric families C3 3+3+3 and C2 4 x 2 + 1: the P3-sym
power ladder on known answers (E-261119-01, with the symmetric (8, 3) slice) first, a symmetric nine-face census with
per-map symmetric formulas (E-261119-02) the main investment; P6 (E-261117-04) the fallback. No nine-plane sampling
night without a measured rate one rung below (E-261110-04: no hit, STATUS 3ay). Mirror families are outside every
uniform formula. (11, 5): closed for the laptop (E-261118-03). S6 parked after (10, 3), its replay deferred with the
note (E-261116-08); one lemma session (E-261116-09). (10, 4): all 1117 admissible maps UNSAT-SOLVER, replay parked
(I-261116-02). The S0 price probe is withdrawn. The significance filter excludes (11, 3); S6 (10,2) is a control, not a
headline. The note is deferred.

As of 2026-11-19. Compute is laptop-only, no Actions or rented compute. Prefer a certified finite cell list
when enumeration and decisions fit the budget. Sampled misses need a measured discovery-power statement;
solver answers without checked proofs are not family negatives. Current evidence: `STATUS.md`; run rules:
`PROTOCOL.md`.

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
* Declined by the owner on 2026-11-07 (kept for the record): e-mail to the author of `pirozhkov-andrei/polyhedraproof` (E-261101-11). Why: he reduced exactly
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
  * Pilot the GitHub Actions runner before relying on it. Owner approved an Actions trial on 2026-11-08: the
    calibration wave on known (9,3) maps (I-261108-07, lead review 2026-11-08d queue item 6). **Parked by the owner on
    2026-11-10** (laptop-only compute).
  * `lint_docs.py` also checks that every new `PLAN.md` has the counter-calibration and scenario-move lines (template
    changed 2026-11-01 after `reviews/strategy-review-2026-11-01.md`).
* **Harness changes approved by the owner on 2026-11-10** (`reviews/HANDOFF_PROMPT_2026-11-10-wedges.md` §11; less
  owner time, same control; each passes the infrastructure filter of `PROTOCOL.md` §3). One lab session each, in this
  order, before or between week items, never during a night. Acceptance check of every item: the control-surface test
  (`start` -> `status` / `board` -> `stop` -> `start` in a scratch directory), `verify_all.py --quick` green, no change
  to any recorded result.
  1. **Permissions and hooks** (`.claude/settings.json`, half a session). Allowlist the read-only commands of lab
     sessions (git status / log / diff / show, ls, `trace.py --check`, `launch.sh status`, the test files of
     `verify_all`); run the `fewer-permission-prompts` skill once; a `PostToolUse` hook on edits under `ideas/`,
     `hypotheses/`, `experiments/*/README.md` and `ROADMAP.md` runs `trace.py --check`; a `Stop` hook warns when the
     tree is dirty without a handover. Never in the allowlist: push, `sudo`, `launch.sh start`. The allowlist is one
     commit the owner reviews.
  2. **Experiment contract and `lint_docs.py`** (it absorbs the two `lint_docs.py` bullets above). Every night
     experiment ships `queue.json` or a unit list, `progress.sh`, `summary.py` / `verdict.json`, and a `run.sh` that
     verifies candidates in the run. `lint_docs.py` in `verify_all --quick`: PLAN committed before any `results/`,
     T + D >= 3 on every open row, STATUS "As of" equals the latest CONCLUSION date, README `status` equals the ROADMAP
     State, every backticked path exists, the text budgets of `PROTOCOL.md` §8b.
  3. **`launch.sh post` and `board`** (extend `launch.sh`, no new launcher). `post` runs when the last shard of a queue
     ends: `summary.py` writes `results/SUMMARY.md` and `verdict.json` (the PLAN's registered rules, machine-readable),
     every CANDIDATE goes through `verify_candidate.py`, results are committed on the lab branch, a macOS notification
     reports the verdict line. `board` (`verification/board.py`) prints one screen: branch and dirty flag, running
     shards, last verdict, next week item, open approvals, the credence table; `board.py --handover` writes the
     mechanical handover lines; `trace.py` generates the STATUS §3 experiment table from the README headers
     (hand-written STATUS keeps §0-§2 and §4-§7). Optional: `arm HH:MM` (refuses off AC power, on a dirty tree or
     without a committed PLAN) and `session N`. `start` / `arm` stays the owner's approval of a night.
  4. **Compute accounting** (15 minutes). Record CPU seconds (`resource.getrusage(RUSAGE_CHILDREN)` in
     `run_overnight.py`, or `/usr/bin/time -l` in `run.sh`): `core_hours = wall x WORKERS` overstates (lead review
     2026-11-09, audit A2), and the pricing of the (10, 4) nights depends on it.

  The tools of the new targets (`code/edge_types.py`, a generic `solid` job in `run_overnight.py`,
  `code/lutz_import.py`, `verify_candidate.py --target S6` once the SPEC entry is approved, benchmark-ladder rows for
  wedge-seeded engines) are built inside the preps of E-261110-01, -02 and -03. A headless morning session
  (`launch.sh morning`: `experiment-conclude` with a restricted tool set, a `DRAFT` commit on the lab branch, never a
  push or a merge) is built only after two manual mornings went well. Already applied as wording on 2026-11-10: no
  night report, one commit per stage, the lead review's size and owner digest, chained lab items (`PROTOCOL.md` §8b).

## Week plan (owner-approved lead review 2026-11-19; replaces the 2026-11-18 plan)

Source: `reviews/strategy-review-2026-11-19.md` §1, approved by the owner on 2026-11-19. Lab sessions take items in
order and may chain steps needing neither a night nor an approval. Outside-tree questions go to "For the lead". At most
10 cores, 8-10 shards per splittable run, laptop on AC under caffeinate; the owner launches every run. Each experiment
needs its `PLAN.md` committed before compute (skill `experiment-start`), with its unit tests run in that commit. Pilots
go through `run.sh` with a manifest and stop once their projection exceeds the item budget (audit 4 of the review). No
proofs; every UNSAT or INFEASIBLE is UNSAT-SOLVER. The previous week (2026-11-18) is done: STATUS 3az, 3ba, 3bb, 3bc;
E-261116-08 deferred by the owner.

1. **P3-sym power ladder and the symmetric (8, 3) slice** ([E-261119-01](experiments/E-261119-01-p3sym-power-ladder/), explore, J 0; follow-up of E-261118-02; I-261119-02; reconciled with the Codex second opinion, `reviews/strategy-review-2026-11-19-reconcile.md`).
   * P3-sym unpinned, 5 workers, one seed. U1 free C2 4 x 2 at (8, 36), cap 1.5 h (66 quad orbits, both known objects
     inside): on each model decode, census code, bridge, `--all-pairs`, then block that map by its complete paired runs
     (one predicate per run on line ij with end triples ijk, ijl; the negated conjunction of its E runs and every image
     under the normaliser of the action, 384 for free C2) and continue; a map whose bridge fails stays open. U2 free C2
     at (8, 30), cap 1 h, predicted INFEASIBLE ((8, 2) negative, STATUS 3d). U3 C3 3+3+3 at (9, 39), cap 1 h, predicted
     INFEASIBLE ((9, 3) negative, 3d); 3d's checked proofs are for the map CNFs, not for P3. U4 D2 and S4 at (8, 36)
     with blocking, 15 min each, run first. Hard aggregate <= 20 core-h including controls and bridges, one owner evening.
   * Controls: those of E-261118-02, plus both known objects pinned under free C2 (orbit-size-2 gauge reachable).
     Blocking controls: a synthetic unit test (same end triples, different pairing); each known object pinned with its
     own map blocked INFEASIBLE, with the other map blocked SAT; unpinned, with Roest-Vigh's map blocked U1 still
     returns Mizhaev's, and the reverse.
   * Kill and tree: a failed control -> repair. U2 or U3 SAT -> stop: decode, GP, Euler, darts, census code, action;
     transport chi into the 3d map CNF and evaluate its clause families; bridge; a PASS -> `--target S5`,
     `candidate-check`, escalate. U1 UNKNOWN -> P3-sym parked for nine faces (no power at 66 orbits). Otherwise record
     each unit and go to item 2 (C3 at nine faces per map there). No C3 night from this item: one needs a changed
     nine-plane discovery test (e.g. the planted control of the Codex review §5) and the owner's word. A new
     (8, 3) map realized, `--all-pairs` PASS -> `candidate-check`, escalate (meets E-261112-02's reopening condition).
     Blocking ends INFEASIBLE -> "this P3-sym free-C2 formula with these blocks is INFEASIBLE", UNSAT-SOLVER (planning);
     no claim on maps whose bridge failed.
   * Lab: Opus, high / Codex gpt-6-astra, high (blocking soundness decides the claim; a new eight-face object is possible).
2. **Symmetric nine-face census with per-map symmetric formulas** ([E-261119-02](experiments/E-261119-02-symmetric-nine-face-census/), explore, J 2; the main investment; I-261030-18, I-261119-01).
   * Stage A, one session, <= 1 core-h: generalise `E-261103-01/c3_crosscheck.py` to (9, 4) (three pair orbits, 0 or 3
     fixed triangles, pair multiplicity <= 3, 18 C3 extra-edge demand classes; the code asserts <= 2 now; deadline
     inside gluing; covers, gluings, codes and time per stratum and the fixed-cell count b per map recorded), plus a C2
     analogue with one fixed face. Controls: (9, 3) gives exactly the census's 8 free-C3 classes and its fixed-face
     involution classes; (7, 1) gives Szilassi's map; free C2 at (8, 3) gives both known maps. Gate per family in a
     shared 1 core-h, C3 first: a complete family that passes its controls goes to stage B even if the other times out.
   * Stage B, owner run <= 10 core-h, 10 shards, kissat, cap 600 s, after one map per multiplicity stratum is priced:
     C3 by omsat's C3 clauses (standard chart), C2 4 x 2 + 1 plane-only (moved chart, the E-261118-03 runner, `build_sym`
     gauge, the action inherited on canonical darts). Rung: both known maps SAT on the free-C2 (8, 3) list, every (9, 3)
     symmetric formula UNSAT (agrees with 3d); controls: generic moved nine-plane signs pinned on the symmetry + gauge
     subformula, a realizable nine-face fixed-face positive, a wrong pairing, a wrong action. Item 1's U1 is compared
     with this rung only on common decoded maps.
   * Tree: SAT -> bridge, `--all-pairs` nine faces, `candidate-check`, escalate. A complete family all UNSAT-SOLVER ->
     genus 5 (E = 51) for that family, priced the same way. Neither family advances -> item 3.
   * Lab: Opus, high / Codex gpt-6-astra, high (a new enumerator; its controls are the result).
3. **P6 equivelar price pilot, stage A** ([E-261117-04](experiments/E-261117-04-equivelar-price-pilot/), explore, J 2), only if neither census family of item 2 advances.
   * Roest-Vigh's equivelar {9, 3} map must appear at (8, 3); costs per stage; no night before a price.
   * Lab: Opus, medium / Codex gpt-6.1-sol, high.
4. **Uniformity and perturbation lemmas** ([E-261116-09](experiments/E-261116-09-uniformity-perturbation-lemmas/), audit, no compute), extended by I-261118-02 and the two lemmas of the review's §2 (owner 5: symmetric eight-face solids have a free half-turn; lead 4: the (11, 5) improper slice is non-uniform). They carry the scope sentences of items 1-2. Input: the Codex review §4 (every group element, powers included; the stabiliser test is not a full dependency test).
   * Lab: Opus, high / Codex gpt-6-astra, high (proofs; at most PROVED-1).
5. **Optional: face-transitive nine-face maps at genus 7** ([E-261119-03](experiments/E-261119-03-cayley-nine-faces-genus-7/), explore, J 2; owner's idea, I-261119-03).
   * N1's two enumerators at valence 14 (Z9, Z3 x Z3), the plain formula at 10 elements on any admissible class; <= 1
     session. Kill: no admissible class -> the face-transitive nine-face slice closed at genus 4 and 7.
   * Lab: Opus, medium / Codex gpt-6.1-sol, medium; SAT: Opus, high / gpt-6-astra, high.

Deferred: E-261116-08 (owner, returns with the note), P4, every nine-plane sampling arm, N3, Stage B (E-261112-02;
reopens on a new (8, 3) map), the asymmetric (8, 3) sweep, the curved-face encoder and the full deletion sieve
(I-261118-04 parked), E-261101-08, the (10, 4) replay, wedges, the full 865, S6 (11, 4). Parked: N4 (I-261117-04).
Closed for the laptop: (11, 5) (E-261118-03; its improper slice has no uniform formula). Not recommended: longer
P3-sym C3 caps before item 1. None is refuted. Previous plans and their results remain in the dated reviews and STATUS.

## Queue: constructive targets on the laptop (owner-approved 2026-11-12, reordered 2026-11-19)

A queue row is not a launch: commit its PLAN and pass its gates before compute. "J" = jump (2 reaches the target
genus directly).

| ID | State | Tests | Question | T D F G R | Budget | Stop rule |
|---|---|---|---|---|---|---|
| [E-261119-01](experiments/E-261119-01-p3sym-power-ladder/) | running (week item 1; PLAN 2026-11-19) | H-261101-07 | **Explore, J 0.** P3-sym power on known answers: free C2 at (8, 36) finds a model (66 orbits), free C2 at (8, 30) and C3 at (9, 39) predicted INFEASIBLE (3d); the symmetric (8, 3) slice by paired-run map blocking | 2 1 2 1 2 | 1 session + <= 20 core-h, one owner evening | failed control or blocking control, all units at their caps, a contradiction with 3d, or first verified candidate |
| [E-261119-02](experiments/E-261119-02-symmetric-nine-face-census/) | planned (week item 2, the main investment) | H-261101-07 | **Explore, J 2.** Symmetric nine-face census (C3 3+3+3, C2 4 x 2 + 1) by lifting the C3 exact cover, then per-map symmetric formulas at 10 elements | 2 2 1 2 2 | stage A 1 session, <= 1 core-h shared by C3 and C2; stage B <= 10 core-h owner run | census control failure, (9, 4) census over 1 core-h per family, all formulas recorded or first verified candidate |
| [E-261119-03](experiments/E-261119-03-cayley-nine-faces-genus-7/) | planned (week item 5, optional) | H-261101-07 | **Explore, J 2.** Face-transitive (Cayley) nine-face maps at genus 7 (Z9, Z3 x Z3, valence 14), plain formula on any admissible class (owner's idea) | 1 1 2 1 2 | <= 1 session | no admissible class, all formulas recorded or first verified candidate |
| [E-261118-04](experiments/E-261118-04-one-face-deletion-sieve-9-3/) | done (OPEN-LOW, pilot; owner) | H-261101-07 | **Explore, J 0.** (9, 3) one-face deletion sieve: 203 maps x 9 deleted faces at 9 elements; quasi-polyhedra with one curved face (owner's idea) | 1 2 2 1 2 | 1 session, <= 1 core-h, 10 shards | failed control, all 1827 formulas recorded or cap |
| [E-261118-01](experiments/E-261118-01-face-transitive-8-3-formulas/) | done 2026-11-18 (classes 1-5 all UNSAT-SOLVER, Roest-Vigh's realized; STATUS 3ba) | H-261101-07 | **Exploit, J 0.** N1b: the five unrealized face-transitive (8, 3) classes by the plain and normalised formulas at 9 elements | 2 1 2 1 2 | <= 0.2 core-h, 10 shards | Roest-Vigh's class not SAT (bug), all ten formulas recorded or first verified candidate |
| [E-261118-02](experiments/E-261118-02-equivariant-census-free-formula/) | done 2026-11-19 (rung passed; nine faces UNDERPOWERED@17.0 core-h, C3 3+3+3 UNKNOWN at 1 h; STATUS 3bb; to the lead) | H-261101-07 | **Explore, J 2.** P3-sym: equivariant census-free formula; D2 / S4 eight-face rung, then C3 3+3+3 at nine faces | 2 2 2 2 2 | 2 sessions, <= 6 core-h; nine faces <= 40 core-h owner run | failed control, no rung model at 30 min, first verified candidate or cap |
| [E-261118-03](experiments/E-261118-03-s5-11-5-plane-only-price-probe/) | done 2026-11-19 (gate NIGHT; all 20 Aut+ = 2 maps UNSAT-SOLVER x 4 seeds @1.0 core-h; STATUS 3bc; (11, 5) closed for the laptop) | H-261101-07 | **Explore, J 2.** (11, 5) plane-only C2 formula on two Aut+ = 2 maps against the 12-element median | 1 2 2 1 2 | 1 session, <= 4 core-h, 8 shards | failed N2 control, both maps priced, first verified candidate or cap |
| [E-261117-01](experiments/E-261117-01-cayley-census-9-4/) | done 2026-11-17: NO-ADMISSIBLE-CAYLEY-9-4 (STATUS 3au) | H-261101-07 | **Exploit, J 2.** N1: face-transitive cubic maps, order-8 rung at (8, 3), then Z9 and Z3 x Z3 at (9, 4), each map by the plain and free-C3 formulas | 2 2 2 1 2 | 1 session, <= 1 core-h joint cap, 10 shards | Roest-Vigh's map missing (bug), all maps recorded, first verified candidate or cap |
| [E-261117-02](experiments/E-261117-02-moved-chart-plane-symmetry/) | done 2026-11-17: GATE PASSED (STATUS 3av) | - | **Explore, gate.** N2: plane-only symmetry in a moved chart; Szilassi control chain, then the seven-plane C2 3 x 2 + 1 rung | 2 2 2 2 2 | 1 session, <= 1 core-h | failed control (cause told apart), rung recovered or cap |
| [E-261116-07](experiments/E-261116-07-census-free-s1-ladder/) | done 2026-11-17: UNDERPOWERED@5.5 core-h, no model, parked (STATUS 3aw) | H-261101-07 | **Explore, J 2.** P3 v2: census-free formula with validity-gated cells and eager connectivity; unit tests, L0-L3, bridge gate at eight faces | 2 2 1 2 2 | 2 sessions, <= 6 core-h, 10 shards | decision tree of the week item; first verified candidate or cap |
| [E-261117-03](experiments/E-261117-03-patchwork-chirotope-probe/) | done 2026-11-17: Szilassi patchwork at K = 32, C2 S5 by construction; n >= 9 UNDERPOWERED@0.87 core-h (STATUS 3ax) | - | **Explore.** P4: step 0 candidate-check of the 16 S6 (10, 2) files; C0 certificate, C1 control coverage per K, C2 Szilassi's map formula AND P4 | 1 2 1 2 2 | 1 session, <= 1 core-h; sampler <= 6 core-h gated | no control in the box, C2 UNSAT-SOLVER in the box, or cap |
| [E-261110-04](experiments/E-261110-04-genus-free-9-10-faces-sweep/) | done (2026-11-18; LOW-YIELD@63.8 core-h, STATUS 3ay) | - | **Explore, J 2.** Owner-approved night: C3 3+3+3 at nine planes, E in {45, 51}; C2 4 x 2 + 1 arm (E-261117-02 passed); geometric-box arm | 1 2 1 1 2 | one owner night <= 80 core-h, 10 shards | first verified candidate, failed control or cap; zero verified hits parks that distribution and cap |
| [E-261117-04](experiments/E-261117-04-equivelar-price-pilot/) | planned (week item 3, only if neither E-261119-02 census family advances) | H-261101-07 | **Explore.** P6 price pilot: equivelar slice, stage A at (8, 3), costs per stage | 1 2 1 1 2 | 1 session, 1 core-h; no night before a price | control map absent, pinned control UNSAT or cap |
| [E-261116-08](experiments/E-261116-08-s6-10-3-replay-pricing/) | planned, deferred by the owner 2026-11-19 (returns with the note; proofs approved for paper item D3; budget to re-price, estimate 5-8 core-h) | H-261110-03 | **Audit.** Proof size, check time and memory on two of the twenty S6 (10, 3) CNFs; gate of a one-night replay | 1 2 2 1 2 | 1 session, <= 2 core-h | both CNFs priced or a hash mismatch |
| [E-261116-09](experiments/E-261116-09-uniformity-perturbation-lemmas/) | planned (week item 4; extended 2026-11-17: N2 perturbation step, P3 proof obligations; 2026-11-18: I-261118-02; 2026-11-19: the eight-face free half-turn and (11, 5) improper lemmas) | H-261101-07 | **Audit.** Uniformity lemma for cubic embedded objects; perturbation lemma I-261108-09 by its universal local check | 2 1 2 2 2 | 1 session | proof or counterexample |
| [E-261116-06](experiments/E-261116-06-s5-11-5-symmetric-slice/) | parked (withdrawn 2026-11-17: registered free-action domain empty; not run) | H-261101-07 | **Exploit, J 2.** Free-C2 / free-C3 uniform formulas of the 24 symmetric admissible (11, 5) maps | 1 2 2 1 2 | 1 session + <= 2 core-h, 10 shards | all formulas recorded, first verified candidate or failed control |
| [E-261116-01](experiments/E-261116-01-s5-11-5-census-cost-probe/) | done (NO-SWEEP-SYMMETRIC-SLICE; STATUS 3aq) | H-261101-07 | **Exploit, J 2.** (11, 5) census rerun with manifest, ten normalised formulas at 3600 s; price of the 3986 admissible maps and of S0 by the element curve | 2 2 2 2 2 | 1 prep session + <= 10 core-h, 10 shards | ten maps recorded, first verified candidate, failed control, census mismatch or cap |
| [E-261116-02](experiments/E-261116-02-s6-10-3-cube-pilot/) | done (STATUS 3ar; follow-up E-261116-05 done) | H-261110-03 | **Exploit, J 2.** march_cu cubes and `kissat --sat` on normalised Lutz #1, #2 | 1 2 2 1 2 | 1 prep session + <= 8 core-h, 10 shards | both maps decided or all cubes / units recorded, failed cover control or cap; neither decided -> park S6 (10, 3) |
| [E-261116-05](experiments/E-261116-05-s6-10-3-sat-night/) | done (ALL-20-DECIDED-UNSAT-SOLVER; STATUS 3as) | H-261110-03 | **Exploit, J 2.** Normalised monolithic `kissat --sat` on remaining Lutz maps; pilot decisions reused | 1 2 2 1 2 | <=80 core-h, 10 shards, one owner night | first SAT, failed control, owner stop, all units or cap; SAT -> thirty-model bridge, otherwise park unresolved maps |
| [E-261116-03](experiments/E-261116-03-s0-price-probe/) | parked (withdrawn 2026-11-16b: E-261116-01 median gate not met; not run) | H-261101-06, H-261101-01 | **Exploit, J 2.** Ten asymmetric S0 embedding formulas at 4 h | 2 2 2 2 2 | 1 prep session + <= 40 core-h, 10 shards | ten types recorded, failed control, first SAT (realizability stage) or cap |
| [E-261116-04](experiments/E-261116-04-polar-transfer-10-3/) | done (NO-CHART-EMBEDDED, STATUS 3at) | H-261110-03 | **Explore, J 2.** Polar planes of 17 vertex realizations in every affine chart, `--target S6` | 1 2 2 1 2 | 1 session, seconds | all charts tested, failed control or a PASS |
| [E-261114-01](experiments/E-261114-01-normalised-s6-10-3/) | done (NO-DAY-RUN; pilot gate failed, STATUS 3am) | H-261110-03 | **Exploit, J 2.** The twenty `submap=True` (10, 3) formulas with the reorientation and mirror units, behind the invariance test and re-gauged positive controls; no proofs | 2 2 2 2 2 | 1 prep session + <= 20 core-h day run, 10 shards | all twenty recorded, first verified candidate, failed control or cap; both pilot units TIMEOUT -> no day run |
| [E-261114-02](experiments/E-261114-02-bridge-recovery-control/) | done (bridge ADEQUATE; CONCLUSION, STATUS 3al) | H-261110-03 | **Explore, control.** Does the frozen bridge recover the exact chirotopes of the 16 realized (10, 2) objects; 30 seeds on five unrealized maps | 1 2 2 2 2 | < 1 core-h, chained with the prep of E-261114-01 | all units recorded or cap |
| [E-261114-03](experiments/E-261114-03-hull-vertex-chart-pilot/) | done (UNRESOLVED; small-pilot gate closed, STATUS 3an) | H-261101-06 | **Explore.** Chart normalisation at a hull vertex: lemma, exact re-charting controls, one cube per vertex on the two slowest normalised maps | 2 2 2 2 2 | 1 session + <= 3 core-h, 10 shards | failed control; summed cube time >= 0.7x monolithic on both maps; censored baseline -> unresolved (PLAN) |
| [E-261114-04](experiments/E-261114-04-immersion-core-8-2/) | done 2026-11-14 (park; CONCLUSION / STATUS 3ap) | H-261101-15, H-261029-06 | **Explore.** Face-grouped minimal cores of the immersion-only formula on (8, 2) #0, #1 | 2 1 2 2 2 | 1 session, <= 1 core-h | both maps mined; no core on <= 6 faces -> park |
| [E-261113-01](experiments/E-261113-01-symmetric-s6-10-3/) | done (2026-11-13: (a) 0 EMBEDDED; (b) 10/10 UNSAT-SOLVER, 0 SAT, 0.034 core-h; OPEN, STATUS 3ag) | H-261110-03 | **Exploit, J 2.** Symmetric S6 (10, 3): the one-parameter tetrahedral family of Lutz #15 by exact arrangement cells, then ten symmetric `submap=True` formulas (C3 on six maps, free C2 on three), no proofs | 2 2 2 2 2 | 1 prep session + <= 10 core-h day run, 10 shards | all units recorded, first verified candidate, failed control or cap |
| [E-261113-02](experiments/E-261113-02-s6-10-2-calibration-rung/) | done (2026-11-13: 153/153 SAT, median 0.83 s; bridge 16/153; LIGHT, CHEAP; STATUS 3ah) | H-261110-03 | **Explore, calibration.** (10, 2) rung: time to SAT over seeds and bridge realization rate on 50 of Lutz's 865 maps | 1 2 2 2 2 | 1 prep session + <= 3 core-h, 10 shards | 50 maps recorded, importer control failure or cap |
| [E-261113-03](experiments/E-261113-03-rung-below-cell-census/) | done (2026-11-14: 25,531/25,531 recorded, 4 SOLID all with Roest-Vigh's map, 25,527 UNSAT-SOLVER, 15.97 core-h; OPEN, Stage B parked; STATUS 3ak) | H-261112-01 | **Explore, control.** All generic eighth-plane cells over seven planes of Roest-Vigh; the enumerator must find the known object unaided; distinct dual maps among SOLID cells; gate of Stage B | 2 2 2 1 2 | 1 prep session, then an owner day run <= 20 core-h, 10 shards | count mismatch, planted cell missed, all cells recorded or cap |
| [E-261112-01](experiments/E-261112-01-ninth-plane-stage-a/) | done (2026-11-13: 2,004/2,004 UNSAT-SOLVER, 0 SAT, 8.01 core-h; OPEN, STATUS 3ae) | H-261112-01 | **Explore, J 2.** Exact near-copy ninth-plane cells over both sources; all pairs, edge runs >= 39, genus free; recovery and deleted-plane reinsertion controls | 2 2 2 1 2 | 1 prep session + <= 12 core-h (owner, amendment 2), 10 shards | first candidate, failed control/count/orbit check, completed list or cap |
| [E-261112-02](experiments/E-261112-02-ninth-plane-stage-b/) | parked (2026-11-14: E-261113-03 found only the source map; no PLAN; a new lead decision reopens it) | H-261112-01 | **Explore, J 2.** All generic cells, Roest-Vigh first; independent rank-4 count, actual orbits, 50-cell timing gate; no night earned by an A miss; proposed only if the rung-below census finds a second map | 2 1 1 1 2 | 1 prep session, then 1 owner night/source, <= 80 core-h/night, 10 shards | count/control failure, first candidate or cap; cost > 1 night/source -> owner decision |
| [E-261110-02](experiments/E-261110-02-face-minimal-10-3-decision/) | done (2026-11-13: OPEN@20.03 core-h, solver-limited: 20/20 TIMEOUT at 3600 s, controls pass; escalated, STATUS 3af) | H-261110-03, H-261110-01 | **Exploit, J 2.** Twenty plain `submap=True` formulas, no proofs (owner, 2026-11-13); S6 (10,2) formula and foreign-model realization controls before the (10,3) night | 2 2 2 2 2 | 1 prep session + <= 80 core-h owner night, 10 shards | all twenty recorded, failed control or cap |
| [E-261110-05](experiments/E-261110-05-immersion-only-s5-formulas/) | done (2026-11-13: V2 8/8 UNSAT-SOLVER; V1 (9,3) 5 SAT; H-261110-01 weakened; STATUS 3ai) | H-261110-01 | **Explore.** V2 first on two (8,2) maps, then the unchanged V1/V2 tree on two (8,2) and six (9,3) maps; no proofs (owner rule 2026-11-13, PLAN) | 2 2 2 2 2 | <= 3 core-h, 8-10 shards | 16 units ended, hash/control failure or cap |
| [E-261113-04](experiments/E-261113-04-cube-and-conquer-pilot-10-4/) | done (2026-11-13: PARK, r >= 1.07 on 96 and >= 0.92 on 85, 0 SAT, 1.08 core-h; STATUS 3aj) | H-261101-06 | **Explore, gate of E-261110-06.** Segment-order cubes (9 order literals of the 3 doubled pairs, 512 cubes) on (10,4) maps 96 and 85 vs monolithic kissat; map 845 speed calibration | 1 2 2 2 2 | 1 prep session + <= 3 core-h, 10 shards | all units recorded, failed control, cube cap 0.1x or arm cap 0.7x monolithic |
| [E-261110-06](experiments/E-261110-06-s5-10-4-strata-ab-remainder/) | done (COMPLETE-UNSAT-SOLVER; owner run concluded, STATUS 3ao) | H-261101-07 | **Exploit, J 2.** (10,4) strata A + B, 757 maps, formulas with the reorientation and mirror units after the controls of E-261114-01; priced on the 10 maps of E-261103-07; no proofs | 2 2 2 2 2 | 1 prep session + one owner night <= 80 core-h, 10 shards | all maps recorded, first verified candidate, failed control or cap; price above one night -> fastest patterns first, the rest to the lead |
| [E-261110-01](experiments/E-261110-01-edge-types-wedge-census/) | deferred (PLAN retained; thin wedges only if needed) | - | **Calibration.** Edge types / wedge covariate; no longer a prerequisite for a random-family night | 1 2 2 1 2 | existing 1-session tool budget | all input/null rows or failed control |
| [E-261110-03](experiments/E-261110-03-arrangement-family-scoring-8-planes/) | parked (closed as a gate 2026-11-17: the D2 gate tests nothing, K13; not run) | - | **Explore, gate.** All-pairs solids at 8 planes, E free: D2 2x4, isotropic, (10, 2)-deleted-plane families; p per family | 2 2 2 1 2 | 1 prep session + <= 3 core-h, 10 shards | all units, failed control or cap |
| [E-261101-08](experiments/E-261101-08-relaxed-s1-twelve-faces/) | deferred (outside this week) | H-261101-07 | Relaxed S1 at twelve faces; original plan retained, no active scoring gate or night | 2 2 2 2 2 | no current allocation | return through a future approved week plan |

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
| [E-261103-03](experiments/E-261103-03-s5-exact-decision-8-2-9-3/) | done (2026-11-08: all 203 admissible (9,3) plain formulas UNSAT-VERIFIED, STATUS 3d) | H-261103-03, H-261103-02, H-261101-07 | (8,2) stage completed (see CONCLUSION; exact formula decisions, geometric scope PROVED-1). Paired (9,3) pilot completed (CONCLUSION / STATUS 3e); wider plain coverage unresolved. Autonomous 60/300-second grid completed (CONCLUSION / STATUS 3f); new-map tranche activated and same-path pilot concluded (STATUS 3h); owner-run tranche concluded (STATUS 3i), LOW-YIELD; broader census goal incomplete, no automatic expansion. Exact decision per map: the 2 (8, 2) maps (9 elements, plain and C2), the 8 C3 (9, 3) maps with C3 clauses, the 24 C2 maps via asymmetric formulas unless a nonuniform symmetry extension is supplied (fixed-face C2/D3 uniform UNSAT is not a geometric exclusion), then all 203 admissible (9, 3) maps; realizers and final polynomials on every model; CNF + DRAT kept; a realized model goes to `candidate-check` and `--target S5` | 2 2 2 2 2 | hours for (8, 2); one night for (9, 3) | every map decided (UNSAT-VERIFIED / realized / NONREALIZABLE-EXACT / listed timeout), or median SAT time above ~1 h per (9, 3) map |
| [E-261103-04](experiments/E-261103-04-s5-genus-ladder-9-faces/) | done | H-261101-07, H-261103-02 | **Explore.** Legacy representation gate failed (STATUS 3j); replacement dart-preserving surgery gate passed (CONCLUSION / STATUS 3k, PROVED-1). Geometric recovery pilot concluded UNDERPOWERED (CONCLUSION / STATUS 3l). Conditional grid concluded UNDERPOWERED (STATUS 3n). Intermediate-map audit completed (STATUS 3o): Roest-Vigh g1 OM-SAT, Mizhaev g2 formula UNSAT-VERIFIED (geometric interpretation PROVED-1). Alternative first-removal audit completed (STATUS 3p): an OM-SAT alternative found and finite queue exhausted. Descendant audit completed CHAIN-PASS (STATUS 3q), combinatorial/OM route only. Saved-OM realization: Roest-Vigh g1 and Mizhaev g1/g2 auxiliaries accepted (STATUS 3r, 3s). **Concluded 2026-11-07**: hinge ladder parked (fails both controls); OM-first realization of intermediates works but adds no (9,3) power. Genus ladder on 9 faces: every admissible (9, 3) map from its sphere down (`tubes`) and up again with `genus_ladder.search`, exact verifier per level, `--target S5` at the top; controls R1 and the two (8, 3) maps through the same ladder; what is different from DR1: a genus-3 target below the ravine, 9 faces, all pairs adjacent | 1 2 2 1 2 | one night, 10 cores, many seeds x short budgets | the night, or the first S5 PASS |
| [E-261103-05](experiments/E-261103-05-s5-symmetric-solid-first/) | done | H-261103-02, H-261101-07 | **Explore pilot completed**, BENCHMARK-PASS (CONCLUSION / STATUS 3g); R2/R3 achieved, target/night not activated. Broader proposal: symmetric solid-first (the Roest-Vigh route): C3 / D3 / C2 arrangements of 9 planes, the CP-SAT inner solver extended to 1-3 edge runs per pair; gates R2 (the known planes give the known objects) and R3 (rediscover an (8, 3) object from random D2 / S4 planes in a session) | 2 2 2 1 2 | 1 session; one night only if R3 passes | R2, R3, then the night or the first 36-pair solid |
| [E-261103-06](experiments/E-261103-06-embedded-first-pilot/) | parked | H-261101-07 | **Explore.** Embedded first, planar later (I-261103-01): R1 Szilassi from a torus, then an (8, 3) object from a smooth genus-3 surface; **R1 pilot 2026-11-07**: 4 valid starts blocked by the barrier at energy 84-118, UNDERPOWERED, parked (CONCLUSION / STATUS 3u); kill: the planarity energy plateaus above zero on R1 with the barrier active | 1 2 2 2 1 | 1-2 sessions | R1 and R2' converge (then a pre-registered (9, 3) night), or R1 fails |
| [E-261107-01](experiments/E-261107-01-s5-nine-plane-solid-first-pilot/) | done | H-261103-02, H-261101-07 | **Explore.** Week plan item 1: nine-plane solid-first target pilot, the E-261103-05 engine on 30 uniform 9-plane arrangements (c3 / d2p1 / random), 36 pairs, E = 39, cap 180 s; **Concluded 2026-11-07**: all 30 INFEASIBLE at 0.38 core-h (CONCLUSION / STATUS 3t); LOW-YIELD inference withdrawn 2026-11-12, discovery power unmeasured | 2 2 2 1 2 | <= 2 core-h, one shard | 30 units decided or 2 core-h |
| [E-261108-01](experiments/E-261108-01-s5-arrangement-source-sweep/) | done | H-261103-02, H-261101-07 | **Explore.** Week plan item 4: arrangement-source sweep for solid-first, the E-261107-01 engine unchanged on 300 nine-plane arrangements (100 Roest-Vigh + random ninth plane, 100 Mizhaev + ninth, 100 random C2-invariant), 36 pairs, E = 39, cap 60 s, 10 shards; **Concluded 2026-11-08**: all 300 INFEASIBLE, 0 SOLID at 1.33 core-h (CONCLUSION / STATUS 3v); LOW-YIELD inference withdrawn 2026-11-12, discovery power unmeasured | 2 2 2 1 2 | <= 2 core-h, 10 shards | 300 units decided or 2 core-h |
| [E-261101-11](experiments/E-261101-11-external-human-review/) | parked | FD5, FD6 | **Owner declined the letters on 2026-11-07.** Owner's e-mails (zero compute): the S5 letter to Roest-Vigh and Mizhaev (have they tried (8, 2) or (9, 3); their method; an offer of the map census), and the S0 letters as before | 2 2 1 1 2 | 0 | a reply, or 4 weeks |
| [E-261103-07](experiments/E-261103-07-s5-10-4-census-symmetry/) | done 2026-11-08 (cost probe: 10/10 TIMEOUT, needs a speed-up first; STATUS 3w) | H-261101-07 | Symmetric stretch preparation from the completed (10, 4) census of E-261103-01 (STATUS 3c; do not repeat its enumeration); preparation of the stretch, no geometry before (9, 3) is decided; since 2026-11-08 a (10, 4) cost probe (10 mixed-pattern maps at 300 s), a follow-up of week item 5a only | 1 2 2 2 2 | <= 6.5 core-h by the caps, expected 2-4 (owner 2026-11-08: slow maps at 1800 s) | the 10 maps decided or timed out |
| [E-261109-01](experiments/E-261109-01-grooved-box-multiplicity-control/) | done 2026-11-09 (all pass; STATUS 3y) | H-261101-07 | **Audit.** Week plan item 1: grooved box with k = 2, 3 notches (top/front pair shares 3, 4 segments), pinned positive SAT / swapped-pairing negative UNSAT-VERIFIED through `submap=True`, unpinned k = 2 | 2 2 2 2 2 | < 0.1 core-h, 1 shard | all 5 units ended or a failed pinned positive |
| [E-261109-02](experiments/E-261109-02-independent-census/) | done 2026-11-09 (agreement; STATUS 3z) | H-261101-07 | **Audit.** Week plan item 3: independent growth enumerator vs E-261103-01 at (7,1), (8,2), (9,3) | 2 2 2 2 2 | seconds | classes, |Aut+|, reflexibility equal or a listed difference |
| [E-261109-03](experiments/E-261109-03-second-encoder-six-9-3-maps/) | done 2026-11-09 (all agree; STATUS 3aa) | H-261101-07 | **Audit.** Week plan item 4: independently written encoder `enc2.py` (Lemma 5.1 + line-interval parity, no INCONS/RFCONS/REFLEX1/POC) vs the first encoder on maps 40, 43, 10, 30, 48, 5 and the pinned controls | 2 2 2 2 2 | <= 1 core-h, 8 shards | six targets and controls ended, a disagreement, or 2 sessions |
| [E-261109-04](experiments/E-261109-04-union-of-matched-solids/) | done 2026-11-09 (0 of 256 samples; LOW-YIELD@0.03 core-h; STATUS 3ab) | H-261103-02 | **Explore.** Week plan item 5 (I-261108-11 stage 1): union of two projectively matched exact solids, Szilassi + Szilassi (k = 4) and Szilassi + tetrahedron (k = 1), 128 frozen samples each, exact union boundary from the plane-arrangement cells; control: identical copies return Szilassi | 1 2 2 2 2 | < 1 core-h, 8 shards | both sources sampled or a failed control |
| [E-261109-05](experiments/E-261109-05-face-contraction-sieve/) | done 2026-11-09 (0 of 203 killed; I-261108-06 parked; STATUS 3ac) | H-261101-07, H-261101-11 | **Explore.** Owner request 2026-11-09 (lead review addendum `reviews/strategy-review-2026-11-09-owner-ideas.md` §2; not a week item): I-261108-06 power test, the rank-3 contraction at one face of each of the 203 known-UNSAT (9,3) plain formulas, cap 20 s, controls C0 (none) / C1 (planted, exactly {4,5,6}) | 1 2 2 2 2 | <= 2 core-h, 10 shards | all 203 maps or a failed control |
| [E-261109-06](experiments/E-261109-06-s5-10-4-stratum-c-sweep/) | done 2026-11-10 (360/360 UNSAT-SOLVER, 0 SAT; A + B = 6.06 nights -> Actions route; STATUS 3ad) | H-261101-07 | **Exploit.** Week plan item 1: (10,4) first-witness sweep, stratum C, the 358 admissible maps of the six fastest patterns (146, 845 reuse E-261108-03), kissat rel-4.0.4, no DRAT, cap 3600 s, frozen `queue.json`, pinned controls in every shard, first-SAT stop; 0 SAT prices strata A and B | 2 2 2 1 2 | <= 80 core-h, <= 10 h, 10 shards, one owner night | all units, first SAT, a failed control, or the cap (< 300 decided -> escalate) |
| [E-261108-03](experiments/E-261108-03-s5-10-4-speedup-benchmark/) | done 2026-11-09 (kissat wins, P(4) = 475 core-h, no 10x; STATUS 3x) | H-261101-07 | **Exploit.** Week plan item 2: (10,4) speed-up benchmark, V1 kissat rel-4.0.4, V2 CaDiCaL `--unsat` (owner 2026-11-08 21:30); Phase A six known (9,3) maps + controls, Phase B (10,4) maps 96, 85, 146, 845 at 14400 s solver cap without DRAT (amendment 2), default-CaDiCaL baseline on 96, 85; censored projection P(lambda), winner rule of item 2 | 1 2 2 2 2 | <= 47 core-h, 10 shards, one owner launch <= 5.1 h | all 22 units ended, stop, or first SAT |

S0 items kept alive at low cost while the focus has no result: E-261101-10
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
origin, hypotheses and links; the map shows them). State: `open` / `running` / `done` / `killed` / `parked` (stopped UNDERPOWERED, not refuted) / `blocked`;
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
| [E-261101-11](experiments/E-261101-11-external-human-review/) | parked | FD5, FD6, E-261101-03 | **Owner declined the letters on 2026-11-07.** External human review: first e-mail to the `polyhedraproof` author (three shared symmetric instances with CNF hashes, one question), then Bokowski / Brehm with FD5, FD6, Lemma A and the dossier; since 2026-11-03 also the S5 letter to Roest-Vigh and Mizhaev (S5 queue above) | 2 2 1 1 2 | owner's e-mail, no compute | a reply, or 4 weeks without one -> next reviewer |
| [E-261101-16](experiments/E-261101-16-arrangement-first-chamber-sat/) | open | H-261101-08, H-261101-10 | The S5 form is E-261103-05 (2026-11-03); this row keeps the S0 form (a symmetric arrangement with an asymmetric solid), parked. Arrangement first: exact chamber-SAT (disk condition encoded exactly) on G-symmetric arrangements with asymmetric solids allowed, on the 247 archived arrangements, on the 1005 near-miss arrangements and on normals realized from E-261101-06 / -23 models | 2 2 2 1 2 | one night (~20 core-h) | the night ends, or the first solid with >= 54 pairs (then `candidate-check`) |
| [E-261101-24](experiments/E-261101-24-farkas-descent-pilot/) | open | H-261101-16, H-261101-09 | Farkas-certificate descent: the exact dual gradient of offset infeasibility moves the normals (what is different from DR2/DR4: guided, not annealed); pilot on the 80 radius-0 seeds and a perturbed witness | 2 2 2 1 2 | 1 day coding, ~5 core-h | 50 steps per seed, or the first exact S3 object at a level where sampling found none; positive control first |
| [E-261101-19](experiments/E-261101-19-barrier-continuation-genus3-handle/) | open | H-261101-10, H-261101-03 | Barrier continuation inside the genus-3 realization space towards an in-class handle, with a measure that can go negative (replaces E-261101-07) | 2 2 1 2 2 | 1 core-h pilot, then one night (40 realizations) | all extendable arms of 40 realizations, or the first exact genus-4 object |
| [E-261101-17](experiments/E-261101-17-realization-space-geometry/) | open | H-261101-09, H-261101-10 | Geometry of the realization spaces: chord widths by hit-and-run, offsets and normals separately, shrinkage per handle, connectivity of the type-15 archive | 1 2 2 1 2 | ~10 core-h | 10 realizations x 2,000 steps and the pairwise segment tests |
| [E-261101-15](experiments/E-261101-15-cube-and-conquer-pilot/) | open | H-261101-06, H-261101-01, H-261101-12 | Cube-and-conquer pilot on one trivial-Aut type as an Actions matrix, cubes on the 44 vertex-type bits pruned by E-261101-21 (or the 66 edge-convexity bits, I-261110-07, if E-261110-01 confirms them), LRAT checked on the fly (after E-261101-09 agreement) | 2 2 1 1 2 | ~300 core-h of Actions | one type decided, or the matrix exhausted; report refuted fraction per core-hour and proof-handling cost |
| [E-261101-10](experiments/E-261101-10-write-up-symmetric-immersion/) | open | FD6, H-261101-13 | Write-up: no symmetric immersion (second encoder, soundness proofs, archived certificates, Lemma A for improper isometries reviewed or the statement restricted to rotations) | 2 1 1 1 2 | 2-3 sessions | arXiv-ready draft reviewed by `adversarial-verifier` (a filter) and one human |
| [E-261101-03](experiments/E-261101-03-type0-dossier/) | open | H-261101-05, FD10 | Type-0 genus-3 dossier: the owner's independent second verifier first, then canonical form, certificate re-run, novelty search | 1 2 2 1 2 | 1-2 sessions, no compute | stop after the 5 steps or 2 sessions; any verifier mismatch -> fix FD10 first |
| [E-261101-20](experiments/E-261101-20-incremental-sat-across-types/) | open | H-261101-06 | One incremental SAT session for the 25 symmetric instances with selector literals: do shared GP lemmas cut the total time? | 1 2 2 1 2 | a few core-h | two orders; below 1.5x closes it, above 2x makes it the campaign default |
| [E-261101-08](experiments/E-261101-08-relaxed-s1-twelve-faces/) | open | H-261101-07, DR12 | Relaxed S1 target, a goal in itself: 12 faces, six extra segments (genus 7, the smallest S1 case; corrected 2026-11-10, this row said "three doubled pairs"), after Roest-Vigh calibration (done, STATUS 3g); deferred 2026-11-12 in the constructive queue above | 2 2 2 2 2 | one night per family | calibration fails -> fix engine, do not run n = 12 |
| [E-261101-12](experiments/E-261101-12-maximal-face-neighbourly/) | open | H-261101-07, DR12, DR15 | Umbrella row of the focus, split on 2026-11-03 into E-261103-01 to -07 (S5 queue above). **Focus target since 2026-11-03 (`STRATEGY.md`): (9, 3) first, stretch (10, 4)** (SPEC S5, `--target S5`); the strategy review splits this row into experiments. Maximal face-neighbourly cubic polyhedra per genus, (F, g) = (8, 2), (9, 3), (10, 4), (11, 5) with 2, 3, 3, 2 doubled pairs; (8, 2) only as a warm-up if it calibrates the (9, 3) method; symmetric ansatzes first (black-box engines were underpowered there) | 1 2 2 2 2 | literature 1 session; then 1 night per case | (9, 3): an S5 PASS (`candidate-check`), or every map tried UNSAT with a written power statement; then (10, 4) under the same rule |

Done or merged this cycle: [E-261102-03](experiments/E-261102-03-chirotope-alt-cap-or-wall/) (done 2026-11-03, night 7: full-map frontier unchanged with the cap lifted, 0/12 at 120 min, R6k k = 8, 9 4/4 each) and [E-261102-04](experiments/E-261102-04-genus-ladder-engine-score/) (done 2026-11-03, night 7: genus-ladder search, R4 0/14, R5 5/10 at 6 min); [E-261102-02](experiments/E-261102-02-chirotope-first-night2/) (killed 2026-11-03 before any run, by the pre-registered rule of E-261102-03); [E-261101-23](experiments/E-261101-23-k-face-subinstances-face-cegar/) and [E-261101-25](experiments/E-261101-25-chirotope-first/) (done 2026-11-02, night 6, both UNDERPOWERED: a final-polynomial LP without a time limit hung 9 of 10 shards; follow-ups E-261102-01, -02); [E-261102-01](experiments/E-261102-01-kface-sweep-completion/) (done 2026-11-02, LOW-YIELD@4.2 core-h for exclusion on the greedy face set at k <= 9, UNDERPOWERED for realization); [E-261101-07](experiments/E-261101-07-pinned-hemisphere-margin/) (done, verdict ARTEFACT:
the "pinned margin" was a floor of `gauss_gate.hemisphere_margin`; its real question is E-261101-19);
[E-261101-13](experiments/E-261101-13-exact-covering/) (killed: merged into E-261101-06, exact covering on chambers).

Below the gate (T + D < 3; run only after re-scoring with a written reason):

| ID | Question | T D F G R | Why below |
|---|---|---|---|
| [E-261101-04](experiments/E-261101-04-normals-first-power-study/) | Power of normals-first: how often is the *control* SAT at radius r? | 1 1 2 1 2 | re-scored 2026-11-01: the Wendel estimate (`reviews/fresh-eyes-review.md` 2.3) predicts the answer; run a 2 core-h check only if E-261101-17 finds widths comparable across genus |
| [E-261101-14](experiments/E-261101-14-chirotope-chambers/) | Chirotope chambers of the 247 archive realizations | 1 1 2 1 2 | descriptive; E-261101-17 measures the same spaces with a decision attached |

## Parked methods (budget or power limits, not refuted)

The historical measurements in `STATUS.md` §3 remain. The 2026-11-12 owner decision withdraws the
LOW-YIELD inference for E-261107-01 and E-261108-01: recovery controls did not measure discovery power.
Archive face descent, cyclic arrangements and native (10,3) sampling are demoted at this budget. None is refuted. A new run needs a `PLAN.md` that says what is different this time (objective, ansatz, power, scale)
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
| Census-free formula P3 v2 (DR19; E-261116-07) | (7, 21) in 8 s; 48/48 eight- and nine-face cubes UNKNOWN at 225-560 s, no model even in the cube holding Roest-Vigh and Mizhaev | a changed search measured first on that cube (solution hint or partial pinning, more workers, a longer cap) and its time to a model |
| Nine-plane symmetric sampling, frozen engine (E-261110-04) | 0 hits: C3 3+3+3 and C2 4 x 2 + 1, E = 45, 51, p >= ~9e-4 rejected per decided arrangement (10-19 % censored at 20 s); +-q^w boxes 0 / 551, 0 / 557 classes at eight planes | a family with a measured rate >= 1e-2 at a rung with a known answer and a stated transfer reason; keep the uniform box |

## Decision point

Three scenarios with explicit credences (idea I-261101-17; all CONJECTURE, set 2026-11-01 by the strategy review,
updated by `experiment-conclude` from the "scenario move" line of each `PLAN.md`):

S0 table (unchanged 2026-11-03: no S0 evidence since 2026-11-01):

| Scenario | Credence | What raises it | What lowers it |
|---|---|---|---|
| A: a realization exists | 0.20 | any S3 object of genus >= 4 (E-261101-16, -19); a realizable OM model | per-type OM-UNSAT (E-261101-15); H-261101-10 supported |
| B: all 59 types are OM-UNSAT (as in the vertex version) | 0.55 | a rank-3 UNSAT (E-261101-06); a decided type (E-261101-15); small recurring cores (E-261101-18) | any OM-SAT model |
| C: some types are OM-SAT with only non-realizable models | 0.25 | an OM-SAT model that fails the realizability audit (I-261029-57) | per-type OM-UNSAT |

S5 table (set 2026-11-03 by the strategy review; all rows set 2026-11-08 by `reviews/strategy-review-2026-11-08d.md` §8 and again 2026-11-09 by `reviews/strategy-review-2026-11-09.md` §8, owner-approved; all CONJECTURE; "cannot tell" = not decided within the strategy's
horizon by our tools; moved by the "scenario move" lines of the E-261103 PLANs):

| Case | exists | does not exist | cannot tell | Evidence in one line |
|---|---|---|---|---|
| (9, 3) | 0.03 | 0.97 | 0 | E-261103-03: all 203 admissible plain formulas UNSAT-VERIFIED (EXACT); m = 3, 4 control passed, census reproduced by a second enumerator, two encoders agree on six maps (E-261109-01..03); still PROVED-1, no human review (lead review 2026-11-09 §8) |
| (8, 2) | 0.02 | 0.98 | 0 | E-261103-03: both plain formulas UNSAT-VERIFIED; m = 3, 4 control passed and census reproduced (E-261109-01, -02); conditional PROVED-1, not reviewed (lead review 2026-11-09 §8) |
| (10, 4) | 0.10 | 0.50 | 0.40 | 2026-11-16: all 1117 admissible maps UNSAT-SOLVER (stratum C plain, A + B normalised; STATUS 3ad, 3ao); the review's 0.03 / 0.87 / 0.10 not applied (owner did not ask). 2026-11-10 (owner-approved; was 0.15 / 0.50 / 0.35): stratum C 360/360 UNSAT-SOLVER (E-261109-06) is weak evidence against, laptop-only compute raises "cannot tell". E-261108-03: kissat decides four maps in <= 2749 s (UNSAT-SOLVER), sweep priced at about 424-475 core-h (scenario); four UNSAT-SOLVER maps are no existence evidence; proof checking of long solves does not fit 48 GB (lead review 2026-11-09 §8) |

Targets of 2026-11-10 (`reviews/strategy-review-2026-11-10.md` §4, owner-approved 2026-11-10; all
CONJECTURE: planning weights of one AI session, not evidence; moved by the "scenario move" lines of the E-261110 PLANs):

| Case | exists | Evidence in one line |
|---|---|---|
| (10, 3) face-minimal, single adjacencies (S6) | 0.25 | the vertex version is realizable at genus 3 (CLAIMED); the face version has no data; nothing run |
| nine mutually adjacent faces, genus >= 4 (S1) | 0.45 | 2026-11-18 (owner-approved lead review §7; was 0.55): zero hits in the C3 3+3+3 and C2 4 x 2 + 1 nine-plane families, the face-transitive (9, 4) slice empty (EXACT), Stage A 0 of 2004, the rung-below census only its source; none is a negative result. Eight exist at genus 3 (Mizhaev, Roest-Vigh); (9, 3) excluded at formula scope |
| relaxed Szilassi-12, genus >= 7 (S1) | 0.40 | no data; the engine is calibrated at 8 planes only |
| (10, 4) S5 | 0.10 (the row of the table above) | stratum C 360/360 UNSAT-SOLVER is weak evidence against; laptop-only compute raises "cannot tell" |
| S0 | the S0 table above (A = 0.20) is unchanged (owner, 2026-11-10); the handoff session's weight was 0.05 | no S0 evidence since 2026-11-01 |

Rules for S5: both (8, 2) and (9, 3) decided non-existent -> write the note, focus moves to (10, 4) with E-261103-07
(fired 2026-11-08: owner approved lead review 2026-11-08d; the note is gated by week items 1, 3, 4 and says that no
independent review took place);
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
