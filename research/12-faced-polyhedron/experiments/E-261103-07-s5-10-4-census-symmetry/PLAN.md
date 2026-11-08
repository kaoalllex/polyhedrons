# E-261103-07: (10,4) cost probe for the exact plain route

Pre-registration (`PROTOCOL.md` §2), owner-approved design of 2026-11-08 (10 maps, slow patterns at 1800 s).

* **ROADMAP row / scores**: T 1 D 2 F 2 G 2 R 2 (`reviews/strategy-review-2026-11-08c.md` §6); follow-up of ROADMAP week item 5a,
  branch "5a decides every map UNSAT".
* **Question**: what does the E-261103-03 plain encoder cost per (10,4) map, by pattern, and so for all 1117 admissible maps?
* **Hypotheses moved**: H-261101-07 only by a realized SAT model (genus 4 case); UNSAT and TIMEOUT results move nothing (10
  of 1117 maps). The probe is a cost measurement, not a decision of (10,4).
* **H1**: the (10,4)/(9,3) time ratio F (below) is at most 10, so the route costs at most a campaign of nights. **H0**: F > 10 or
  most fast maps TIMEOUT at 300 s; the route needs a speed-up first.
* **Why**: E-261103-03 decided all 203 (9,3) formulas; the next case adds one element (11 instead of 10, 330 bases), the
  formulas double (about 157,000 clauses against 78,000). The pattern census (README) gives counts per pattern; only the
  growth factor is unknown.
* **Method**: the E-261103-03 runner (`tranche.py`, `run_overnight.py s5 --s5-queue`), extended on 2026-11-08 by a census case
  `(10, 4)`, a control file and per-map caps in the queue (defaults unchanged for (9,3); 37 unit tests OK). Queue
  `queue_probe.json` from `make_queue.py` (seed 2611080701, random within the pattern): fast patterns one map each,
  solver/checker 300/450 s: 690 `(1,1,2,2)/(2,2,2)`, 1104 `(1,1,2,2)/(2,3)`, 78 `(1,1,1,3)`, 845 `(1,2,3)`, 146
  `(2,2,2)/(2,2,2)`, 57 `(3,3)/(4)`; slow patterns two each at 1800/2700 s: 96, 926 `(1^4,2)`; 85, 852 `1^6`. Target S5 at
  (10,4), plain uniform formula (`ALL_OPTS`), counters `SAT / UNSAT-VERIFIED / TIMEOUT` (SPEC §4). CNF and proof deleted
  after the check, hashes and transcripts kept (PROTOCOL §5). First SAT stops dispatch globally.
* **Controls**: `pilot.py --controls-only` per shard (as in 5a); positive `control-f10-sK` (convex simple 10-face polyhedron,
  `control_f9.py --faces 10`, V 16, planes pinned, submap formula) must be SAT; negative `control-f10-neg-sK` (same planes,
  the map of a second polyhedron) must be UNSAT-VERIFIED; both in every shard before its map, caps 60/120 s. They are genus 0;
  they test the n = 10 encoder-solver-checker path and the case switch, not genus-4 behaviour.
* **Pilot**: the bounded startup check through `launch.sh` on 10 shards with test caps (as for 5a): controls pass, maps start
  with the (10,4) census record, `stop` and resume work. Test results are deleted; nothing from it is a result.
* **Pilot gate**: the binding limit is the per-map solver cap; the run starts if all 20 controls pass in the check.
* **(9,3) reference** (median solver seconds over the decided plain records of E-261103-03, NUMERICAL): `(1,1,2,2)/(2,2,2)` 90,
  `(1,1,2,2)/(2,3)` 90, `(1,1,1,3)` 58, `(1,2,3)` 36, `(2,2,2)/(2,2,2)` 27, `(1^4,2)` 213, `1^6` 497; `(3,3)/(4)` has none.
* **Growth factor**: F_p = (10,4) solver seconds / (9,3) reference of its pattern, per decided map with a reference;
  F = median of F_p (fast and slow maps). A TIMEOUT gives F_p > cap / reference (a lower bound).
* **Projection**: P = sum over patterns of count x reference x F x 1.71 / 3600 core-h (1.71 = 1 + checker/solver of item 5a;
  `(3,3)/(4)` taken at 90 s). At F = 1, P = 122 core-h.
* **Predictions**: (1) >= 5/6 fast maps decided at 300 s (about 60 %); (2) F between 2 and 10 (about 50 %); (3) >= 2/4 slow maps
  decided within 1800 s (about 40 %); (4) 0 SAT (about 85 %); (5) controls pass in every shard.
* **Grid**: one setting; the caps are set per pattern from the (9,3) times, the probe measures and does not tune.
* **Budget**: 10 shards on the laptop (AC power), one shard per map; reservation 58,200 s (10 equal shares of 5820 s: two
  controls at 180 s, one slow map at 4500 s, 960 s overhead); the caps bound actual use at about 6.5 core-h (4 x 4500 + 6 x 750
  + controls); expected 2-4 core-h; wall <= 1.3 h; `--hours 2`.
* **Power statement**: one map per fast pattern measures F to within the spread of (9,3) times in that pattern (up to about
  3x either way at (9,3)); it cannot give a per-pattern distribution, and two slow maps per pattern cannot exclude a slow tail.
* **Counter calibration**: no float diagnostic in the verdict; times are recorded cadical process times; F and P are
  arithmetic on them.
* **Scenario move**: none for credences ((10,4) row unchanged); only "cannot tell" for (10,4) may be revised by the lead review.
* **Outcomes and their meaning**:
  * SAT: first-SAT stop; the runner's model check, realizers, final polynomial, then `candidate-check` (stages are
    untested at n = 10: if one errors, the model stays saved and is processed in a session);
  * UNSAT-VERIFIED: that exact plain (10,4) formula, nothing beyond it;
  * TIMEOUT: no information about the map; a lower bound for F_p;
  * a control fails: stop, escalate, no verdict.
* **Verdict rule (decided now)**: P <= 160 core-h -> "one week" (two 80-core-h nights); 160 < P <= 800 -> "campaign" (up to 10
  nights); P > 800, or >= 3 of 6 fast maps TIMEOUT, or all 4 slow maps TIMEOUT -> "needs a speed-up first" (item 5b-type
  benchmark before any full run).
* **Follow-up tree**: none beyond recording; the verdict goes to the lead review (review 2026-11-08c §4, option 2).
* **Stop rule**: every queued unit decided or timed out, a first SAT, a control failure, or the 2 h deadline.
* **What changes**: STATUS gets a (10,4) cost line (NUMERICAL); ROADMAP row E-261103-07 `done`; no hypothesis status changes
  without a SAT.

## Amendments
