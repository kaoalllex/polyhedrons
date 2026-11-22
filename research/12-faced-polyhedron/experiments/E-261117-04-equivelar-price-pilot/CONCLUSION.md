# E-261117-04: conclusion

**EQUIVELAR-9-4-PLAIN-ALL-UNSAT-SOLVER (formula scope)**: the plain sub-map formula of every one of the 1071 admissible
equivelar (9, 4) classes, in its code's orientation, is UNSAT-SOLVER (no proof): planning evidence, never a negative
result. This conclusion covers stage C (PLAN amendment 2, week item 4); stages A and B are in the README and STATUS
3bk, 3bl.

* **Runs** (lab-run after the owner's one-line permission, 10 cores, <= 50 min; `run.sh`, 10 shards, lean, kissat
  4.0.4 seed 0, cap 60 s, no proofs): chunk 0 (`Q=stageC_c0`, 91 maps) 2026-11-22 20:14:08Z-20:16:10Z, 887 core-s;
  chunk 1 (`Q=stageC_c1`, 980 maps) 20:17:35Z-20:38:53Z, 11479 core-s. **3.43 core-h, ~23.5 min wall** (the shards'
  `budget.json` ledgers, controls included). Every shard `exit_status: 0` (`results/stageC_c*/*/manifest.txt`). The
  laptop was on battery at the start (the owner allowed it) and on AC by the end, under `caffeinate -dimsu`; the
  shards' wall matches their ledgers, so no sleep gap is visible.
* **Audit** (session): 1071 of 1071 planned maps have exactly one record, every one `UNSAT-SOLVER`, `ended_by:
  completed`, scope `sub-map embedding formula (submap=True)` (no generator), canonical SHA-256 equal to the maps file.
  0 SAT, 0 TIMEOUT, 0 ERROR, so no 600 s pass and no model queue. Solver time per map: mean 11.0 s, median 9.2 s, max
  54.9 s (27 above 30 s, 3 above 45 s: the cap was close to binding on pattern 9 and 5+4). Per pattern (maps, mean s):
  9 (624, 12.3), 5+4 (168, 13.1), 7+2 (108, 8.4), 6+3 (65, 5.4), 5+2+2 (58, 7.8), 4+3+2 (36, 5.5), 3+2+2+2 (10, 4.6),
  3+3+3 (2, 1.4). The 111 symmetric classes average 9.1 s, the 960 others 11.3 s.
* **Controls** (all passed): build controls (`p6.py build-c`: census complete with its controls, the ten K2 maps
  distinct and admissible, chunks partition the admissible set, every pattern in chunk 0, f9 violations 0 / > 0); the
  pinned f9 pair in every shard of both queues (20 positive SAT, model checked; 20 negative UNSAT-SOLVER); the
  runner's convex controls `CONTROLS-PASS` in all 20 shard runs. Consistency: the ten K2 maps UNSAT-SOLVER again
  (1.5-26.7 s; K2 had 1.4-23.4 s at cap 120 s).
* **Price** (NUMERICAL): chunk 0 projected chunk 1 at 13753 core-s and 34 min wall (x 1.5 margin); actual 11479 core-s
  and 21.3 min. The review's 5-31 core-h for the pass was high by about 2x (actual 3.4).
* **Prediction vs outcome**: P9 (controls and K2, 0.9) held; P10 (every unit within 60 s, 0.8) held, max 54.9 s;
  P11 (no SAT, 0.85) held; P12 (<= 5 core-h and a lab run, 0.75) held.
* **What may be claimed**: every admissible equivelar (9, 4) map has an UNSAT-SOLVER plain sub-map formula in its
  code's orientation (10 elements, kissat 4.0.4, cap 60 s, seed 0). With stage A: on the equivelar slice the pipeline
  recovers both known (8, 3) solids and finds nothing at (9, 4). Planning use only.
* **What may NOT be claimed**: that any equivelar (9, 4) map is non-realizable (no checked proof; a replay with
  proofs would be needed for a note); anything about the mirror orientation's formulas beyond the soundness argument of
  the PLAN, about non-equivelar (9, 4) maps (S1 at nine faces allows them), other genera, or nine-face S1 objects in
  general.
* **Hypotheses**: H-261101-07 stays open; evidence line added (equivelar slice at genus 4, formula scope). No credence
  move (week plan: the lead re-plans).
* **Verdict**: **UNSAT-SOLVER on 1071 of 1071, 0 SAT@3.43 core-h** (stage C; the experiment as a whole 6.7 core-h:
  A 0.18, B 3.1, C 3.43). Not LOW-YIELD: a complete pass over its slice at formula scope, every unit decided.
* **Next step**: none from this experiment. The week plan's tree sends the all-UNSAT-SOLVER outcome to the lead
  review, which re-plans the nine-face line.
* **Rows updated**: `STATUS.md` 3bn and header, `ROADMAP.md` (item 4, E-261117-04 row), `experiment-log.md`,
  `paper/OUTLINE.md` B9, `hypotheses/H-261101-07*.md`, the README.
