# Night report 2026-11-02 (night 6: E-261101-23 and E-261101-25)

* **Wall time vs budget**: launched 2026-11-01T17:41Z (20:41 local, UTC+3) with `overnight/run_night6.sh`, 10
  single-core processes under `caffeinate -dimsu`; planned ~6-8 h. One shard (E-261101-23 shard 2) finished
  normally after 4.6 h; the other nine ran until the owner's `stop` at 2026-11-02T04:42Z (11.0 h). Manifests: 103.85
  core-h in total (E-23 59.75, E-25 44.10), about 14 of them productive. No sleep gap: shard 2 kept writing records
  until 01:18 local and the hung processes were at 100 % CPU.
* **What hung**: `final_polynomial.py` called `scipy.optimize.linprog(method='highs')` without a time limit; on some
  degenerate LPs (optimum t* = 0) HiGHS did not return. Reproduced in the morning on E-23 type 19 k = 8 (stack dump
  inside `_highs_wrapper`, 100 % CPU), elsewhere inferred from the code path (the last record or progress line of
  every hung shard is followed by that call). One such LP in E-25 shard 3 returned after ~80 minutes. E-25's
  `--seed-minutes 75` is checked between steps, so it could not interrupt the LP. Fixed: `time_limit=120` ->
  status `LP-TIMEOUT`; re-run of the reproduced unit with a 60 s limit completes and writes its record.
* **Log loss**: a start at 07:41:59 local, 15 s before the stop, restarted all ten runners; the launcher redirected
  with `>`, which truncated every `night.log`. Records, manifests and `progress.jsonl` are intact. Now `>>`. The
  restart left partial CNF / DRAT files of the units in flight in five E-23 shards; they are not UNSATs and are not
  committed.
* **E-261101-23** (k-face sub-instances, greedy face set, CaDiCaL + DRAT): 27 types reached; k = 8 SAT 27/27, k = 9
  SAT 15 / TIMEOUT 11, k = 10 TIMEOUT 26/26; 0 UNSAT; 0 of 42 SAT models realized; one exact final polynomial
  (type 0 k = 9) whose multipliers were not stored. Negative control passed in the pilot.
* **E-261101-25** (chirotope-first, k = 7, 4 of 10 seed slices): 27 of 59 scheduled seeds started; 21 ended at the
  first step with the 12 core-guided rounds used up; 6 reached models (42 alternation steps), none realized (best 3
  wrong signs); 19 final polynomials recorded: 13 FEASIBLE, 5 numerical zeros, 1 exact (became a sound cut).
* **Exact checks**: nothing EMBEDDED and no realized k-face model, so `candidate-check` had nothing to verify; no
  UNSAT, so no CNF or proof is evidence.
* **Verdict**: both experiments UNDERPOWERED (numbers and claims in their `CONCLUSION.md`); follow-ups E-261102-01
  (the 32 types not reached) and E-261102-02 (engine night run 2 with `--rounds 40`, after E-261101-26).
