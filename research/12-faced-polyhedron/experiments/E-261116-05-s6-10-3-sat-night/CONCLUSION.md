# E-261116-05: normalised S6 SAT-oriented owner night

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
