---
id: E-261116-02
title: S6 (10, 3) cube pilot - march_cu cubes and a SAT-oriented kissat configuration on Lutz #1 and #2
date: 2026-11-16
status: done
concluded: 2026-11-16
verdict: BOTH-DECIDED-UNSAT-SOLVER
direction: [DR19, DR8]
origin: [E-261114-01, E-261113-04]
tests: [H-261110-03]
produces: []
preregistered: true
---

> Concluded: both pilot maps decided for planning; no proofs or geometric negative.
> Evidence, costs, checks and method selection: [CONCLUSION.md](CONCLUSION.md).

## Result and next step

The cube and SAT-oriented monolithic arms agree. The registered owner-night gate passes;
select monolithic `kissat --sat`, reusing the pilot decisions. Follow-up preparation is pending;
the pilot launcher has no remaining target work. No candidate, hypothesis-status or credence change.

## Preparation (2026-11-16)

NUMERICAL timing, SPEC section 4 instance scope; no target decision or new candidate.
`results/prep/summary.json`: positive pipeline and target cube-cover gates PASS.
Selected partitions and counts are frozen there; `results/sat-config/result.json`
checks the SAT-oriented option on the same known-SAT control.
`results/startup-check.json`: bounded launcher check, ten shards, no solver units.
`verify_all.py --quick`: ALL PASS (archive skipped); trace: zero errors.
The solver-unit resume path has not been exercised through a stop/restart.
Historical pilot launch on AC: `bash research/12-faced-polyhedron/overnight/launch.sh 16-02 start`;
use the same command with `status` or `stop`. The launcher supplies caffeinate.

The runner reserves the two monolithic allocations before dispatching cube work;
unfinished killed attempts keep their reservations. A budget stop leaves unresolved
cubes OPEN. Target SAT stops dispatch and preserves its checked assignment;
the registered thirty-model bridge is a subsequent stage, before any witness claim.
