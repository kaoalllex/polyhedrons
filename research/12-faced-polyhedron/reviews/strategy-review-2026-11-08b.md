# Strategy review, 2026-11-08 (b): unit (a) run out of order, run cores, evidence retention

Interim lead review, the same day as `reviews/strategy-review-2026-11-08.md` (the main review of the week). Evidence
cut: `abe8db1` on `lab/2026-11-07` plus the uncommitted `results/item1a/`. Questions: the owner's (conclusions from
unit (a), which ran out of order; all runs on 8-10 cores; is CNF/DRAT retention worth it). This report advises and
changes no ledger file. Labels are `SPEC.md` §5; **Recommendation** and **Untested** mark judgments and proposals.
One check was run (seconds): three item-1a CNFs rebuilt under two `PYTHONHASHSEED` values, compared with the recorded
SHA-256 (§4.2).

## 1. Verdict in ten lines

1. **Recommendation:** strategy unchanged; credences unchanged (no scenario moves by 0.1).
2. **EXACT (formula scope):** unit (a), 13 unattempted 11-gon (9,3) maps: 9 UNSAT-VERIFIED, 4 TIMEOUT at 60 s
   (174, 176, 181, 200), 0 SAT. Prediction (>= 10/13) missed by one; the drop rule of item 3 (< 7/13) is not met.
3. **NUMERICAL:** the concentrated classes split. Patterns (1,2,3) (an 11-gon face) and (2,2,2) (a triangle of doubled pairs) are 13 of 13 UNSAT-VERIFIED; pattern
   (1,1,1,3) is 9 of 14, with all 5 undecided maps (74, 174, 176, 181, 200) in it.
4. **NUMERICAL:** the 9 solves of (a) took 32-59 s of solver time (cadical process time 36.5-59.2 s); map 199 finished
   at 59.3 s of a 60 s cap. The cap sits inside the distribution, so the 5 timeouts are probably cap artefacts (untested).
5. **Recommendation:** add the 5 (1,1,1,3) timeouts to the long-cap launch, outside the (b) counts (map 74 already
   is). Expected cost under 1 core-h; it decides "every 11-gon (9,3) plain formula is UNSAT", which feeds item 3
   and the (10,4) pruning count. It passes the follow-up rule (`STRATEGY.md` §2).
6. The out-of-order run itself was cheap and useful: its prep (cap parameters, custom queue) was needed for (b) anyway.
   Its one avoidable cost is that it ran on one shard: 822 s wall instead of about 2 minutes on 8-10 shards.
7. **Recommendation (owner's point 1):** every run whose units can be split uses 8-10 shards, day runs and lab test
   runs included (§3). Next launch: 10 shards.
8. **Recommendation (owner's point 2):** check proofs during the run, keep hashes and checker logs, delete the
   files; never store CNFs; archive proofs only when a claim goes into a note (§4). The status UNSAT-VERIFIED and
   the CERTIFIED path stay intact.
9. **Audit:** about 324 MB of `.cnf.gz` / `.drat.gz` (361 files, largest 81 MB) are tracked on `lab/2026-11-07`. They are
   not on `main` yet and the branch is not pushed. Decide before the week's PR (§6 A1).
10. **First item:** the prep session for the long-cap launch (queue (b) + 5 maps + control (c), the evidence
    change if approved, 10 shards), then the owner launches it.

## 2. Week plan: replacement text for item 1 in `ROADMAP.md`

Items 2-5 stay as approved. Two edits: the laptop line under the heading and item 1.

```
Laptop: at most 10 cores in total, and every splittable run uses 8-10 shards (owner, 2026-11-08), day and lab
test runs included; item 1's launch uses 10 shards, so nothing runs beside it (items 2-3 run before or after it).

1. **E-261103-03 stratified long-cap pilot** (exploit). Question: do the slow (9,3) plain formulas finish
   with longer caps, and does the pattern stratification hold?
   * DONE 2026-11-08 (owner's order, out of sequence): unit (a), 13 unattempted 11-gon maps at 60/120 s:
     9 UNSAT-VERIFIED (94, 100, 102, 111, 123, 171, 177, 184, 199), 4 TIMEOUT (174, 176, 181, 200), 0 SAT;
     (1,2,3) 2/2, (1,1,1,3) 7/11. Prediction (>= 10/13) missed; item 3 is kept (>= 7/13).
   * NEXT, one prep session, then one owner launch: queue `queue_item1b.json` with (b) 12 unresolved maps,
     the lowest indices of each class: 5 of (1^6), 5 of (1^4,2), 2 of (1,1,2,2)/(2,3); plus, outside the (b)
     counts, the 5 (1,1,1,3) timeouts 74, 174, 176, 181, 200; plus (c) the **positive control at F = 9**:
     one E-261107-01 Phase B solid (exact check first), its own map through the `submap=True` path with its
     planes pinned: SAT required. Solver 1800 s, checker at most 2700 s; time to solve recorded as cadical
     process time (`solver.log`). 10 shards; worst case 17 x 4500 s = 21 core-h, 2.5 h wall; expected far
     less. The bounded startup check of PROTOCOL §8 uses the same shard count. If the owner approves the
     evidence change (review 2026-11-08b §4) it lands in this prep session, before the launch.
   * Predictions: the 5 (1,1,1,3) maps: at least 4/5 UNSAT-VERIFIED within 300 s solver time; (b) has none,
     it measures.
   * Kill: control (c) fails -> stop, escalate (the 0-SAT record would be void). Follow-up tree:
     * any SAT -> stop dispatch; check the model exactly, run the saved-OM realizer (E-261103-04 path),
       `verify_candidate.py --target S5`, `candidate-check`; if it does not realize: one final-polynomial
       attempt (at most 1 session);
     * (b) >= 8/12 decided -> item 5a; 3-7/12 -> item 5a for the classes with >= 3/5 decided, item 5b for the
       rest; <= 2/12 -> item 5b only;
     * all 5 (1,1,1,3) maps UNSAT-VERIFIED -> "every 11-gon (9,3) plain formula is UNSAT-VERIFIED" (EXACT,
       formula scope; geometric reading conditional on the encoder argument and on control (c)); item 3 uses
       all 24 maps. Any of them still TIMEOUT at 1800 s -> item 3 uses (1,2,3) and (2,2,2) only.
```

## 3. Cores (owner's point 1)

* Why one core: `run.sh` and `run_overnight.py s5` run one solver per shard (`--workers 1`); parallelism is the shard
  count. Unit (a) was launched as one shard. `PROTOCOL.md:132` ("CORES default 10, fewer by day") allowed that, and
  `run.sh:19` accepts at most 8 shards.
* **Recommendation** (applied by a working session after approval):
  * `PROTOCOL.md` §6: replace "CORES default 10, fewer by day" with "CORES 8-10 for every run whose units can be
    split, day runs and lab test runs included (owner, 2026-11-08); one shard only for a single unit".
  * `run.sh:19`: accept 1-10 shards.
  * Timing under load: the laptop is an M4 Pro, 10 performance + 4 efficiency cores (EXACT, `sysctl`). Ten shards
    fit the performance cores, but wall-clock caps shift under full load. Compare runs by cadical's process time,
    which `solver.log` already records. A short cap that cut a distribution (60 s here) is raised rather than reused.

## 4. CNF and DRAT retention (owner's point 2)

### 4.1 What each file protects against

* The claim "map X is unrealizable" has three links: the encoding is sound (formula UNSAT => no geometric
  realization), the formula is UNSAT, and the CNF on disk is the formula the encoder meant. DRAT covers only the
  second link. The real risk is the first link, and controls plus the encoder argument cover it; no stored file does.
* A false UNSAT from cadical is rare. drat-trim catches it **at run time**, and that check is what UNSAT-VERIFIED
  means. `SPEC.md:93` (CERTIFIED) asks for a checked certificate and recorded hashes, not a retained file.
* Keeping the file helps only if drat-trim itself is later found faulty. Then any re-check would use another checker
  (cake_lpr on LRAT) on a fresh solve, so the old DRAT is not needed. A new proof of the same CNF (same SHA-256)
  certifies the same statement, so "the same proof file is not guaranteed" does not matter.
* A stored CNF adds nothing over its recorded SHA-256 when the build is deterministic. EXACT check (this review):
  maps 94, 174, 200 rebuilt from the current encoder under `PYTHONHASHSEED` 1 and 777 give byte-identical CNFs (SHA-256
  equal to `results.jsonl`). The existing evidence tests already rebuild CNFs (`test_pilot.py:178,234`).
* Partial proofs of TIMEOUT runs have no evidential value; item 1a keeps four of them (64-67 MB each).
* Cost: (a) produced about 45 MB of gzipped proof per 40 s of solving. At 1800 s caps that is about 2 GB per slow map
  (NUMERICAL, a linear extrapolation). Checking cost 212 of 810 s in (a).

### 4.2 Options

| Option | Run cost | Storage | Label of an UNSAT | Final claim needs |
|---|---|---|---|---|
| A. Check at run time, delete the files (**recommended**) | + checker (~0.6x the solve) | hashes + logs (KB) | UNSAT-VERIFIED | a replay night, only if the claim goes into a note and needs an archived certificate |
| B. Trust cadical, no proof | lowest | none | UNSAT-UNCHECKED | a full re-solve with proofs (1x the solve, more than A's check) |
| C. Current practice | + checker + gzip | 0.6 GB per 13 maps; GBs per slow map | UNSAT-VERIFIED | nothing |

* **Recommendation: A.** B looks cheaper but is not: the UNSAT verdicts are the product of E-261103-03, so a later
  replay costs a full solve, while the runtime check costs about 0.6 of one, and it runs in parallel anyway. So the
  owner's intuition ("re-run when something matters") is right for the files, not for the check.
* A in practice: CNF and proof are written to a scratch directory and deleted after the check. Records keep
  `cnf_sha256`, `proof_sha256`, the checker transcript and the tool hashes. TIMEOUT proofs are deleted at once. SAT
  models (small) are kept. A note-level claim (for example "all (9,3) maps are UNSAT") gets one replay night with
  archived proofs on Zenodo or a release, as `PROTOCOL.md:125` already says.
* Code (prep session, about 30 lines plus tests): `pilot.solve` (scratch dir, delete after check); `tranche.pending`
  (`tranche.py:156-160` fails closed on a missing file: accept the recorded hashes and a completed checker
  instead, for new runs); the evidence tests (`test_pilot.py` EvidenceTests, `test_tranche.py:289-332`) compare
  rebuilt CNFs with the recorded hash instead of the stored file. The `.gitignore` edit in the working tree is then moot.
* Rule text (owner's decision; `CLAUDE.md:59`, `AGENTS.md:59`, `PROTOCOL.md:125`): replace "SAT runs keep their proofs and
  CNFs" with "SAT runs record the SHA-256 of every CNF and proof and keep the checker transcript; proofs are checked
  during the run and then deleted, CNFs are rebuilt from the committed encoder and hash-checked; SAT models are kept.
  Proofs are archived (Zenodo or a release, not git) only for a claim that goes into a note."
* Existing files: about 7.5 GB locally (gitignored, no value beyond the records; delete whenever) and the 324 MB in
  git (§6 A1).

## 5. Scores and queue

Re-scored against the morning review's §5.1. Changes only:

| ID | Candidate | T D F G R | J | Kill cost | Disposition |
|---|---|---|---|---|---|
| E-261103-03 item 1 | long-cap launch, (b) + 5 (1,1,1,3) maps + control (c) | 2 2 2 1 2 | 2 | prep 1s + <= 21 h worst, 10 shards | **first** |
| new item 3 input | concentrated-multiplicity cores | 2 1 2 2 2 | - | 1s + 1h | unchanged; its map set depends on the 5 maps |

The queue order of the morning review (§6) stands: 1, 2, 3, 4, 5, then 6-8. No new ideas: the morning's list is
untouched and nothing since adds one. Credences (§9 of the morning review) stay: (a) moved no scenario.

## 6. Audit

* **A1 (high, git).** `lab/2026-11-07` tracks 361 `.cnf.gz` / `.drat.gz` files, about 324 MB, the largest 81 MB (two above
  GitHub's 50 MB warning). They came in with the evidence commits (for example `a005673`); `main` has none, and the branch has
  no remote. A merge would put them into the history of the public Pages repo for good, against
  `PROTOCOL.md:125` (large proofs go to a release or Zenodo). Options, owner's call (a Git write): (i) untrack them before
  the PR and squash-merge (the blobs reach GitHub with the branch push but stay off `main`); (ii) rewrite the unpushed
  branch to drop them (clean, rewrites 61 commits). Either needs the test change of §4.2 first, because the
  evidence tests read these files.
* **A2 (medium).** TIMEOUT partial proofs are kept (`results/item1a/0/attempt_*/map{174,176,181,200}/*.drat.gz`).
* **A3 (medium).** One shard for a 13-unit run (`CONTINUE_PROMPT.md`, "822 s wall, one core"); see §3.
* **A4 (low, wording).** The lab's note to the owner overstates the risk: "without DRAT the conclusion is weaker". It is
  not: the label rests on the run-time check and the recorded hashes (§4.1).
* **A5 (low).** The 60 s cap of the earlier tranche probably also cut (1,1,1,3)-like maps (map 74). The 5-map follow-up
  tests this, so no other re-run is needed.
* Process cost of the deviation: one compact commit (`abe8db1`, 110 lines including code), no amendment chain. Fine.

## 7. The three things to do first

1. Owner: decide the evidence option (A recommended) and A1 (i) or (ii); approve the cores rule.
2. Prep session: `queue_item1b.json` (12 + 5 maps), control (c), the evidence change if approved, `run.sh` up to
   10 shards, startup check on 10 shards; record unit (a) in STATUS and the ledger (`experiment-conclude`, light).
3. Owner launch on 10 shards (<= 2.5 h wall worst case); then item 2 (literature) and item 3 while nothing else runs.

## 8. Owner's decisions (2026-11-08) and the order of work

Approved: evidence option A (§4.2); A1 (ii), rewrite the unpushed branch without the proof files; the cores rule
(§3). Item 1 of §2 replaces the ROADMAP item 1. One prep session does the following, in this order:

1. `experiment-conclude` (light) for unit (a): commit `results/item1a/` records (no `.cnf` / `.drat`), STATUS, ledger.
2. Rules text: `CLAUDE.md:59` and `AGENTS.md:59` get the §4.2 wording; `PROTOCOL.md` §5 (proof storage) and §6
   (cores) likewise; ROADMAP: the §2 laptop line and item 1.
3. Code, option A: `pilot.solve` writes CNF and proof to a scratch directory and deletes them after the check (TIMEOUT
   proofs at once); `tranche.pending` accepts recorded `cnf_sha256` (+ `proof_sha256` and a completed checker for
   UNSAT-VERIFIED) instead of files; `test_pilot.py` EvidenceTests and `test_tranche.py:289-332` compare rebuilt CNFs
   with the recorded hash and check the saved checker transcript instead of reading stored files; the same for
   `E-261103-04/audit.py:164-166,209,317-319` (not in `verify_all`); `run.sh:19` accepts 1-10 shards; revert the
   working-tree `.gitignore` edit. Run the affected tests, then `verify_all.py --quick` once.
4. History rewrite, only after step 3 passes. Scope: the 377 `.cnf` / `.drat` (`.gz`) paths that appear in
   `main..lab/2026-11-07` and not in the `main` tree (361 of E-261103-03, 16 of E-261103-04, about 320 MB at HEAD).
   The 25 proof files already on `main` (E-261103-02, E-261029-04) stay: `main` is pushed. Commands: a clean
   tree; `git branch backup/lab-2026-11-07` (deleted after the check below); build the path list as
   `comm -23 <(proof paths in main..lab) <(proof paths in main)`; `git filter-repo --force --refs main..lab/2026-11-07
   --invert-paths --paths-from-file LIST`. Check: `git ls-files` lists none of them; `git rev-list --objects
   main..lab/2026-11-07` names none; the affected tests pass again; `main` is unchanged (same SHA). The rewrite
   deletes these files from the working tree as well, as option A intends. Local gitignored proofs (about 7 GB) may be
   deleted with them.
5. Prep for the item 1 launch (§2), startup check on 10 shards, hand the launch command to the owner.

Done the same day: steps 1-4 (commits from "E-261103-03 unit (a): record ..." on). The rewrite removed the 377 paths and
nothing else (`main` unchanged); it changed the SHA of 65 commits, so SHAs recorded earlier map through
`reviews/strategy-review-2026-11-08b-commit-map.txt`. The affected tests passed on the rewritten tree (simulated
before the rewrite: 34 OK; `REPLAY_DRAT=1` fresh replay of the (8,2) pilot evidence OK; `verify_all.py --quick` all
pass except two checks that need a git checkout and were not affected).
