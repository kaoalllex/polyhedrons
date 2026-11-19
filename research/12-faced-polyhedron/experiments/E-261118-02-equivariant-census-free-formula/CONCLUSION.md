# E-261118-02: conclusion

**Rung PASS; nine faces UNDERPOWERED@17.0 core-h (C3 3+3+3, E = 45, 51, 57, 1 h on 5 workers each, one seed)**: the
equivariant P3 formula returned Roest-Vigh's (D2) and Mizhaev's (S4) eight-face maps unaided in seconds, both realized;
the three C3 3+3+3 nine-face formulas ended UNKNOWN at their 1 h caps. No nine-face model, no candidate, no decision.

* **Runs**: pre-registration `5cbe026a` (controls, rung pilot); amendment 1 and C3 pilot at `4ef2fcb6` / `20236abb`;
  owner launch `launch.sh 261118-02 start` at `20236abb`, 2026-11-18 20:30:09-22:45:50 UTC (2 h 15.7 min against
  <= 2.3 h), 10 shards, every `exit_status: 0`; shards 4-9 idle by design (four units). Shards 0 and 1 (E = 45, 51)
  ran together, shard 2 (E = 57) from 21:30:18, shard 3 (plain cube 5, 8 workers) from 22:30:48; at most 10 cores at
  any time, no gap between units. `dirty_files: 10` are the untracked result folders themselves. Core-hours from the
  unit records: 5.00 + 5.00 + 5.00 + 2.00 = 17.01 against <= 17 (process overhead); with the session controls and
  pilots (0.26 core-h) about 17.3 in all. Python 3.14.6, OR-Tools 9.15.6755 in every manifest; the session pilots
  report host Darwin 25.6.0, the owner run Darwin 27.2.0 (the session sandbox's report; same laptop, same Python and
  OR-Tools). No sleep gap: every unit's wall time equals its cap within 1.3 s.
* **Controls** (`results/controls/`, all PASS, amendment 1): orbit counts 36 / 34 / 72; forced zeros as listed; both
  normal forms pinned OPTIMAL, EMBEDDED, invariant (gauge reachability); three negatives INFEASIBLE. In-run positive:
  the rung (pilot, `results/pilot/`): D2 OPTIMAL in 2.3 s, S4 in 5.0 s, each first model decoded, GP-valid,
  invariant, realized by the bridge (hinge) and `--all-pairs` PASS. The nine-face formulas have no in-run positive
  (no nine-face S1 object is known); their power rests on the rung, which has half their orbit count (36 / 34 quad
  orbits against 72).
* **Results** (`results/<shard>/results.jsonl`, `p3sym.py summary results`): C3_9_45, C3_9_51, C3_9_57 (51 283
  variables, 362 265 constraints each): UNKNOWN at 3600 s, no model; plain_cube5_8_36 (21 150 variables, 128 955
  constraints): UNKNOWN at 900 s, no model. No INFEASIBLE, no error.
* **Prediction vs outcome**: P1 (controls) held; P2 (D2 model, 0.5), P3 (S4 model, 0.45) and P4 (a rung model
  realized, 0.35) held, in the pilot; P5 (plain cube 5 with 8 workers no model in its cap, 0.75) held. Amendment 1
  registered no probability for the nine-face units; its outcome is the tree's UNKNOWN branch.
* **Exact verification**: the two rung models: `verify_candidate.py --all-pairs` PASS on the saved
  `results/pilot/{0,1}/*_m0.candidate.json`, census codes EXACT (`p3sym.py types`): the known maps of Roest-Vigh and
  Mizhaev, the registered positive controls, so `candidate-check` does not apply. The owner run produced no model.
  No proofs (none registered).
* **What may be claimed**: the equivariant formula (soundness PROVED-1, module docstring) recovers both known
  eight-face solids from their symmetry alone, D2 in 2.3 s and S4 in 5.0 s on 5 workers (EXACT realizations; method
  scope: one host, one seed). The plain cube 5 has no model within 2.0 core-h on 8 workers (UNKNOWN; instance scope).
* **What may NOT be claimed**: anything about the existence of a C3-symmetric nine-face S1 solid, or of any nine-face
  solid, at E = 45, 51 or 57: a timeout is not a result. Nothing about Cs 4 x 2 + 1 or Cs 3 x 2 + 3 (outside P3-sym,
  deviation 1), C2 4 x 2 + 1 (not run), other caps, seeds or worker counts.
* **Hypotheses**: H-261101-07 unchanged (no new object; the rung objects are known). I-261118-01: the rung test
  passed (the formula works at eight faces); nine faces open. I-261118-02: the Cs families corrected (deviation 1);
  its uniform families left are C3 3+3+3 (standard chart, run here) and C2 4 x 2 + 1 (moved chart, not run).
* **Verdict for the direction**: rung PASS (method, known objects); nine faces UNDERPOWERED@17.0 core-h (three C3
  3+3+3 formulas, 1 h on 5 workers, one seed). The step from eight to nine faces costs more than a factor 700 in time
  to the first model or decision on this host.
* **Next step**: the follow-up tree routes UNKNOWN to the lead: whether a longer C3 run (the registered nine-face
  budget was <= 40 core-h, 17 used), a stronger formula, or P6 (item 6) takes this slot is a strategy decision, not
  a lab improvisation. Week plan: item 4 (E-261118-03). The Cs exclusion and the corrected family list go to the
  lead for `STRATEGY.md` §1.
* **Rows updated**: `STATUS.md` 3bb and header, `ROADMAP.md` State done, `experiment-log.md` (2026-11-19), README,
  I-261118-01, I-261118-02, H-261101-07 note.
