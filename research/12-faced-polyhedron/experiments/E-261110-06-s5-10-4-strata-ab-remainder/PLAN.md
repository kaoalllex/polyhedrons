# E-261110-06: normalised S5 (10,4), strata A + B

Pre-registration, 2026-11-14; replaces the unexecuted 2026-11-10 cube rule.

* **ROADMAP / scores**: week item 2; exploit, jump 2; T 2 D 2 F 2 G 2 R 2.
* **Question / H1 / H0**: can the normalised A+B formulas fit one 80 core-h laptop night
  (H1), or must only the faster patterns run (H0)?
* **Hypothesis moved**: H-261101-07; only a verified S5 (10,4) witness establishes existence.
* **Method / target**: pilot.CNF / from_links / build with ALL_OPTS plus symbreak=True,
  mirror=True; full multi-adjacency formula, not submap=True. kissat seed 0, no proofs.
  Reuse E-261114-01 soundness (PROVED-1) and successful controls after provenance checks.
* **Controls**: saved invariance and positive gates must PASS; negative gate must PASS.
  Compare current encoder, solver, Python and dependencies against the saved environment;
  validate source hashes and saved summaries. A mismatch blocks reuse and target dispatch.
  No unchanged control or solver is rerun just for this prep.
* **Prep**: the ten integer-index maps of E-261103-07/queue_probe.json, cap 1800 s each,
  ten shards. Reuse #845/#96/#85 from E-261114-01 if formula and environment match;
  these finished below their 1200 s cap. New units append checkpoints and retain logs.
* **Counters / labels**: SPEC §4 SAT, UNSAT-SOLVER, TIMEOUT, ERROR; solver and total seconds;
  EMBEDDED, nonsimple_faces, bad_pairs, adjacent_pairs only from exact geometry checks.
  Runtime projections are NUMERICAL, formula decisions instance scope; no geometric negative.
* **Projection**: P = (520 mean(t96,t926) + 237 mean(t85,t852)) / 3600 core-h;
  report solver-only P and total elapsed P separately (no proof-checker multiplier).
  A TIMEOUT contributes its cap as a lower bound: never claim that bound fits the night.
  The other six patterns are timing comparisons, not extrapolation samples for A/B.
* **Prediction / decision**: P <= 80 core-h; if false or censored, rank A/B by observed
  pattern cost and propose the faster coverage inside one night, remainder to the lead.
  At least one new unit must finish before its cap; all TIMEOUT closes the night gate.
* **Grid / power**: 1800 s prep then 3600 s night; two fixed samples per A/B pattern.
  This estimates cost, not the slow-tail distribution or discovery probability. Saved
  recovery success does not measure target discovery power. A censored P is unresolved.
* **Budget**: prep <= 6 core-h, <= 35 minutes solver wall on ten shards; AC/caffeinate.
  SAT follow-up is separate within remaining prep budget; record any deferred work.
  Night <= 80 core-h and <= 8 h per shard, ten shards, owner launch only.
* **Night gate**: after prep, freeze the selected queue and bounded runner before owner launch.
  No first-SAT stop; bridge on every SAT; stop on first verified candidate or failed control.
  Controls and startup must pass through the actual launcher before handover.
* **SAT follow-up**: keep checked model; generate at least thirty seed models per SAT map,
  bridge with submap=False, --target S5, then candidate-check and escalate. A failed bridge
  excludes neither chirotope nor map. No candidate announcement without owner review.
* **Proofs**: none. Every unchecked UNSAT is UNSAT-SOLVER; no formula or family negative.
* **Calibration**: no float geometric threshold decides the verdict; raw monotonic timings
  are recorded, including the cap and fraction consumed. No clamped diagnostic is used.
* **Scenario move**: verified target establishes A; all UNSAT-SOLVER only suggests proof
  replay to the lead, no numeric credence move; SAT without geometry leaves A/C open;
  TIMEOUT, cost measurements and failed controls leave A/B/C and H-261101-07 unchanged.
* **Outcomes / stops**: prep ends on all records, failed control, ERROR or budget; timeout
  has no negative meaning. Near-miss is only a diagnostic, never target success.
  Night all UNSAT-SOLVER -> lead proposes proof replay and (11,5) probe I-261114-03;
  unfinished night -> lead receives exact remaining queue; no second night by default.
* **Ledger**: prep ready -> running/awaiting owner; failed or censored gate -> record scope
  and escalate; night conclusion -> done. Record counts only in CONCLUSION and STATUS.

## Amendments

### 2026-11-14: night queue and startup

Prep passes; select both strata, excluding the four already decided timing samples.
`queue.json` binds the census, preparation summary and shared formula/solver/bridge sources.
The `s5ab` dispatch in run_overnight calls this experiment's run.py; reuse tranche locks,
reservations and append checkpoints, pilot.solve and tranche.bridge (submap=False).
Thirty seeds per SAT map are processed; fewer than thirty SAT models is explicitly incomplete
and goes to the lead, never a failed realization claim. Interrupted seed models survive.
No first-SAT latch; stop on verified candidate, shared error or cumulative budget.
Actual launcher smoke uses a scratch results path and ten maps capped at 0.01 s;
exercise start/status/stop/start with the same entry point, then restore production paths.
Smoke TIMEOUTs are dispatch tests only, excluded from timing projections and production.

### 2026-11-14: startup fixture environment

The first retained-launcher check dispatched no maps: launch.sh owns the shell variable QUEUE,
so the fixture path was lost and the production 3600 s units did not fit the tiny budget.
Use S5AB_QUEUE for the fixture override; repeat only startup with the corrected environment.
The initial detached attempt was killed by signal 9 before task records; cause unestablished.
No target night or solver decision resulted from these failed startup checks.
