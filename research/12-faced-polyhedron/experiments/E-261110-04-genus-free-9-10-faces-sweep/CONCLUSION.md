# E-261110-04: conclusion

2026-11-18. Owner night on the laptop at `8a24715d` (code clean; dirty files are this run's own output and an
unrelated skill edit), frozen engine of E-261103-05, one CP-SAT worker per unit.

* **Runs**: stage A and pilot as in the PLAN amendment (`results/controls/`, `results/pilot/`; PASS, 0.11 core-h).
  Night `results/0..9/`: a first launch of 10 shards ran 1351-1370 s and was stopped by the owner (`launch.sh stop`,
  shards stopped after their unit); a second launch of 8 shards (shards 0-7) ran 27004-27029 s against the 27000 s
  deadline, so no sleep gap. Shards resume from the shared done set: 21,332 records, no unit decided twice. Manifests
  sum to 229,737 core-s = **63.8 core-h** of the 75 core-h budget (unit time in the records: 63.76 core-h). No
  ENGINE_ERROR, no REJECTED_BY_ENGINE, no hit, no `stop.requested` from a hit. Counts per cell:
  `results/summary.json` (`python3 night.py summary results`).

  | cell | units | INFEASIBLE | UNKNOWN (cap) | UNKNOWN fraction | median s | zero hits reject p >= |
  |---|---|---|---|---|---|---|
  | c3, E = 45 | 3835 | 3437 | 398 | 0.104 | 13.2 | 8.7e-4 |
  | c3, E = 51 | 3835 | 3439 | 396 | 0.103 | 13.3 | 8.7e-4 |
  | c2, E = 45 | 3831 | 3138 | 693 | 0.181 | 15.9 | 9.6e-4 |
  | c2, E = 51 | 3831 | 3109 | 722 | 0.189 | 15.9 | 9.6e-4 |
  | geo2, E = 36 | 3000 | 3000 | 0 | 0 | 1.2 | see diagnostic |
  | geo3, E = 36 | 3000 | 3000 | 0 | 0 | 1.2 | see diagnostic |

* **Controls**: stage A PASS before any shard (P1 moved Szilassi EMBEDDED with `--all-pairs` PASS, P2 K13 seed 4
  (24, 36, 8, -4) PASS, tetrahedron E = 6 / 7, K13 seeds 0-3 INFEASIBLE, swapped links rejected, draw checks). P2 runs
  the same `decide()` call with the same cap as the geo arms, so the geo measuring function returns a solid when one
  exists at this rung. No nine-face positive control exists.
* **Diagnostic (constant geo result)**: every geo unit INFEASIBLE (6000 / 6000) is a constant outcome, so it was
  checked before interpretation (`classes.py`, `results/classes.json`; exact labeled chirotopes of the planes plus
  the plane at infinity, on which the engine's verdict depends). The geo boxes repeat arrangements: 3000 draws give
  **551** (geo2) and **557** (geo3) distinct labeled chirotopes, each with one status; the effective sample is these
  classes (zero hits reject p >= ~7e-3 per arm, Wilson 95 %). None of the 17 archived K13 solids lies in the geo2
  support (all magnitudes in {1, 2, 4, 8}), and none of K13's 240 draws does. The engine gives one status per class in
  every cell (determinism). The nine-plane cells do not repeat: c3 3832 classes of 3835 units, c2 3831 of 3831.
* **Prediction vs outcome**: Q1 (c3 E = 45 UNKNOWN fraction <= 0.2, ~60 %) held: 0.104. Q2 (c3 median at E = 51
  above E = 45, ~60 %) held only formally: 13.28 s vs 13.20 s, no practical difference; E does not decide the cost. Q3
  (c2 median <= c3 median at E = 45, ~50 %) failed: 15.9 s vs 13.2 s, and c2 loses 18-19 % of units to the cap vs
  10 % in c3. Q4 (geo2 rate outside K13's [0.045, 0.111], ~40 %) held, below it: 0 / 551 classes (Wilson upper
  0.007). Q5 (a verified nine-face hit, ~5 %) failed.
* **Exact verification**: no candidate, so nothing for `verify_candidate` or `candidate-check`.
* **What may be claimed** (`SPEC.md` §4 scope: these families, boxes, caps and E only; INFEASIBLE is a CP-SAT status,
  `UNSAT-SOLVER` level, no proofs): NUMERICAL (sampling): zero hits among about 3,100-3,440 decided arrangements per
  nine-plane cell reject a per-arrangement hit rate p >= 8.7e-4 (c3) and p >= 9.6e-4 (c2) for C3 3+3+3 in the
  [-8, 8] box and C2 4 x 2 + 1 in the moved chart, at E = 45 and 51, cap 20 s, the frozen hard-disk engine. At eight
  planes, E = 36, the geometric boxes +-q^w (q = 2, 3, w <= 3) give no solid in 551 / 557 distinct chirotopes, below
  K13's uniform-box rate (17 / 240): the coefficient distribution matters at this rung.
* **What may NOT be claimed**: that no nine-face all-pairs solid exists, in these families or at all; anything about
  the 2,209 UNKNOWN units, other boxes, longer caps, other charts, E = 39 or ten planes (not run); that any single
  arrangement has no solid (no checked proof); that symmetric families are worse than asymmetric ones at nine planes
  (no asymmetric arm at nine planes); for geo, a rate per draw (draws repeat; the bound is per class), or anything
  about boxes other than +-q^w with w <= 3.
* **Hypotheses**: none in `tests`. Scenarios A, B, C unchanged (no hit).
* **Verdict**: **LOW-YIELD@63.8 core-h** (one night, 8-10 shards): no nine-face hit; the C3 and C2 nine-plane cells
  at this box and cap are parked with their p bounds; the geo arm is parked (rate below K13's interval, a note for the
  lead). E-261101-08 is not opened.
* **Next step**: for the lead (week item 5 was the last item of the week plan): the geo result says the uniform box
  carries the eight-plane solids and +-q^w boxes are close to sterile (with heavy rejection: 3.7 / 3.4 rejected draws
  per accepted draw), so a later sampler should not shrink the box toward powers; whether a nine-face arm earns another
  row needs a reason to expect a rate: the night only bounds p below about 1e-3, a rate below that costs more than
  about 4 core-h of C3 units per expected hit, and nothing predicts p.
* **Rows updated**: `STATUS.md` 3ay, `ROADMAP.md` item 5 and row (done), `experiment-log.md` (2026-11-18).
