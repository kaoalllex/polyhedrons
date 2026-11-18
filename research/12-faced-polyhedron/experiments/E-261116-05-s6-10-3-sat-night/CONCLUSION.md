# E-261116-05: normalised S6 SAT-oriented owner night

## Owner run conclusion (2026-11-16)

* **Verdict: ALL-20-DECIDED-UNSAT-SOLVER@7.269 worker-h** (18 fresh, Lutz #1/#2 reused from
  E-261116-02). NUMERICAL, SPEC §4 instance scope: the twenty normalised uniform S6 embedding
  formulas (`submap=True`, symbreak, mirror) only. No candidate, no checked proof.
* **Prediction vs outcome:** H1 holds: all eighteen remaining maps decided, each by one
  monolithic `kissat --sat` solve; 0 SAT, 0 TIMEOUT, 0 ERROR, no stop or SAT latch.
* **Runs:** one owner launch at 16:53:56 local, commit `c41203f9` (dirty: the uncommitted
  ROADMAP row only; all 16 queue inputs hash-match). Ten shards, two maps each, one start, no
  restart; longest shard 3720.45 s against the 8 h shard cap; production 7.269 worker-h,
  7.239 CPU-h against 79 worker-h; endpoint clock gaps <= 0.07 s, no continuous sleep audit.
  Solver time per map 762.9-2734.1 s (median 1277.0 s, total 26154.9 s), at most 20 % of
  the 13800 s cap. All ten JSON manifests present; preparation is in `results/preparation-cost.json`.
* **Controls / checks:** each shard revalidated the inherited invariance, positive and negative
  gates and the Python, dependency and solver identity before solving (same hashes as
  `results/run/identity.json`). The all-UNSAT outcome is constant, so the other sign rests on the
  preparation controls through this launcher/queue path (small positive SAT with checked clauses,
  negative UNSAT-SOLVER) and the reused known-SAT `--sat` model; these do not measure discovery
  power at (10,3). Fresh audit (`results/run-audit.json`): all 18 CNFs rebuilt from the committed
  encoder with matching SHA-256, variables and clauses; 20 distinct CNF hashes with the reused rows;
  every solver log ends `s UNSATISFIABLE`/exit 20; coverage, checkpoints, provenance and budget
  reconcile: PASS. No solve or proof replay; the preparation quick PASS is reused (no code change).
* **Claims:** each of the twenty formulas is UNSAT-SOLVER (NUMERICAL, instance scope). Must not be
  claimed: UNSAT or UNSAT-VERIFIED, that no S6 (10,3) polyhedron exists, any family or theorem
  scope, anything about non-uniform (non-general-position) or non-cubic objects, (11,4) or S0.
  A formula-scope exclusion needs a checked replay of exactly these twenty CNFs (owner's word;
  idea I-261116-05) and stays conditional on the PROVED-1 normalisation soundness, encoder
  soundness and census coverage. Not run: proofs, a second encoder, non-uniform formulas.
* **Hypotheses:** H-261110-03 stays open; its (10,3) part has solver-level support for the rival
  in planning only. Status and S0 A/B/C credences unchanged, as pre-registered.
* **Next:** the registered follow-up has no undecided map to park: S6 (10,3) by the normalised
  formulas is exhausted at solver level, no further long-cap campaign. Week item 5
  (E-261116-04) next; the lead decides the next S6 step and whether to price the replay.

## Preparation (2026-11-16)

* **Verdict: READY**, NUMERICAL control/startup scope (SPEC §4); not a target result.
  PLAN pre-registered in `da9a862a`. H-261110-03 and S0 A/B/C unchanged.
* Frozen queue and inherited decisions validate (`results/validation.json`); both reused
  pilot CNF hashes rebuild exactly with the S6 submap constructor. No new census or replay.
* Run the remaining catalogue maps using `kissat --sat`, ten shards; the PLAN reserves
  preparation time separately from production. Caps and stop rules are unchanged.
* Controls: inherited invariance/positive/negative gates reused after environment/source/
  solver validation; small positive SAT and negative UNSAT-SOLVER pass through the same
  launcher/queue path. Positive clauses checked, model preserved, no bridge or witness claim.
* Startup: `launch.sh 16-05 start/status/stop/start`, scratch output, fifteen-second caps;
  active stop preserves ten records, restart completes all eighteen without duplication.
  SAT stops dispatch and preserves its checked model; thirty-model bridge remains subsequent.
  Evidence: `results/startup-check.json`. Production output is absent, pointer restored.
* Changes: existing runner supports S6 topology, SAT-oriented options and a first-SAT latch;
  launcher checks PID ownership before counting/killing it. No new execution framework.
* Checks: five runner tests PASS; shell/compile PASS; `verify_all.py --quick` ALL PASS,
  archive skipped. Trace zero errors, diff/metadata review PASS; logs in `results/`.
* Failures retained: temporary-path alias test fixed; initial detached startup killed;
  initial S6 startup rejected a non-neighbourly map before the constructor fix; short stop
  tests finished too early, so the active-stop check above replaced them. No hidden target run.
* Accounting: `results/preparation-cost.json` sums available worker/CPU manifests;
  initial killed-start overhead is unmeasured. No solver proof or geometry replay.
* Owner next, on AC: `bash research/12-faced-polyhedron/overnight/launch.sh 16-05 start`;
  the same command with `status` or `stop`. The launcher supplies caffeinate; keep lid open.
