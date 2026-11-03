# Night report 2026-11-03 (night 7: E-261102-03 and E-261102-04)

* **Wall time vs budget**: launched 2026-11-02T17:19Z (20:19 local, UTC+3) through `overnight/launch.sh`, E-261102-03
  on 10 shards and E-261102-04 on 4, as pre-registered. Both were stopped at 18:12-18:15Z (the exit trap wrote
  `exit_status: 0`; the logs do not record why). E-261102-04 restarted at 18:15Z on 10 shards, E-261102-03 at 18:57Z
  on 8 (shards 8 and 9 of the first segment were not resumed; their units were re-split over shards 0-7). Last shard
  ended at 23:54Z (02:54 local): ~6.6 h wall against the planned 4.5-5.2 h. Manifests: 53.7 core-h (E-261102-03 35.9,
  of which 8.9 in the first segment produced no record because every unit in flight was a 120-min unit;
  E-261102-04 17.8), against ~45 + ~21 budgeted.
* **Sleep gaps**: none seen. The only gap in E-261102-03's logs is the 45-min stop / restart; E-261102-04 logs once per
  unit, and its units used exactly their wall budgets (2400 s, 7200 s).
* **E-261102-03** (chirotope-first, `--alt 100000 --timeout 300`, 20 units x 120 min): R4 type 15 0/4, R4 type 0 0/4,
  R5 0/4; R6k k = 8 4/4, k = 9 4/4 (2/4 and 3/4 at 40 min). Full-map units ended by time (7) or by the 300-s SAT
  timeout at k = 10-11 (5); k = 10 realized in 3 units, k = 11 never. Replay control (R6k k = 9 seed 1) passed.
* **E-261102-04** (genus-ladder search, 49 units): R1 20/20; R5 5/10 at 6 min, 3/5 at 40 min (the same three seeds,
  identical planes); R4 0/10 at 40 min and 0/4 at 120 min, best energy 1-3; every failure by time; 28 float zeros,
  28 judged EMBEDDED.
* **Exact checks**: `verify_candidate.py`: 20 R1 sets PASS `--all-pairs`, 8 R5 sets PASS (EMBEDDED, 32 48 12 -4),
  all 28 fail `--target S0` as expected; 8 R6k successes re-judged in a fresh process, 8/8. No candidate, no UNSAT.
* **Verdict**: E-261102-03: full-map frontier unchanged with the cap lifted (LOW-YIELD@35.9 core-h), E-261102-02
  killed; E-261102-04: frontier at R4 (LOW-YIELD@17.8 core-h), R5 passed. Both scored engines fail R4 (their
  `CONCLUSION.md`).
* **Lesson for the next night**: a stop and restart loses every unit in flight, and with 120-min units that is up to
  2 h per shard; decide the core split before the start, or stop only between units.
