# E-261112-01: conclusion

2026-11-13. One owner laptop launch (`launch.sh 261112-01 start`), 10 shards, root `results/`, commit `c78e16e1`
(amendment 2) in every shard manifest, clean tree, `units_sha256` `ef132bc7...` as pinned, Python 3.14.6, identical
`pip freeze` in all shards (`ortools==9.15.6755`). One start per shard, no restart, no Actions run.

* **Runs**: started 2026-11-12 20:49:38 UTC; every shard `SHARD-DONE`, `exit_status 0`; last shard ended 21:38:47 UTC,
  wall **49 min**. Cost: **8.01 core-h** of the 12 core-h cap (sum of the runner's per-shard spent counters in
  `night.log`, 2,827-2,947 core-s each, single-thread workers; `manifest.txt` records only the exit status; child CPU
  7.75 h). No sleep gap: per shard, wall minus summed unit and control walls is 3 s. Pilot gate passed in all 10 shards
  (measured pilot means 14.4-16.0 s, projected 0.67-0.74 of the shard budget).
* **Controls**: C0 and C1 for both sources SOLID with exactly verified all-pairs geometry (V E F chi 24 36 8 -4) and C2
  INFEASIBLE in all 10 shards (50/50 pass). C1 used an LP representative distinct from the deleted plane (margins
  0.140 Roest-Vigh, 0.0022 Mizhaev). The controls show the worker can return both signs at eight planes through the
  units' cell-to-solver path; no nine-plane positive control exists (no known nine-face object), so discovery power at
  nine planes is unmeasured.
* **Results**: 2,004 of 2,004 units recorded (1,006 Roest-Vigh orbits, 998 Mizhaev orbits, all of orbit size 4, unit set
  equal to `list/units.json`), every one **INFEASIBLE** with `ended_by: completed`, return code 0, 0 SOLID, 0 UNKNOWN,
  0 HARD-TIMEOUT, 0 ERROR; 2,004 distinct model SHA-256 in `results/*/results.jsonl`. Unit wall 5.3-25.3 s (median
  15.4 s Roest-Vigh, 13.0 s Mizhaev), at most 0.42 of the 60 s cap; every unit has 56 bounded cells, the general-position
  count C(8,3) for nine planes. No `results/CANDIDATE`; `raw/` is empty (no SOLID or ERROR unit).
* **Prediction vs outcome**: planning prediction "all cells plus controls fit 7.3 core-h" (CONJECTURE, about 50 %):
  **missed** by 0.71 core-h (8.01); the owner's 12 core-h cap of amendment 2 held. H1 (a Stage A cell contains a
  nine-face all-pairs solid): no support. H0 is consistent with the outcome, but only at UNSAT-SOLVER level for the
  2,004 exact models; it is not established.
* **Exact verification**: no SAT, so no `verify_candidate.py --all-pairs` and no `candidate-check`. No UNSAT is used as
  evidence: every INFEASIBLE is CP-SAT without a proof (UNSAT-SOLVER, SPEC §4); model hashes recorded, model files not kept.
* **What may be claimed**: NUMERICAL, instance scope: for each of the 2,004 certified near-copy cell representatives
  (Stage A list, amendment 1), CP-SAT reports the frozen hard model (`best_solid(target_edges=39, edges_at_least=True,
  max_runs=3)`: 36 pairs, connected disk faces, edge runs >= 39, genus free) INFEASIBLE within 25.3 s. The Stage A list is
  exhausted at this formula; nothing in it is left open.
* **What may NOT be claimed**: that no nine-face S1 object exists in these cells, over these two sources, or at all; any
  family negative or exclusion (no checked proof, encoding soundness PROVED-1 via E-261103-05 only); anything about
  non-generic cells (walls), the rest of the rank-4 cell set (Stage B), other eight-plane sources, non-cubic objects or
  S5; a discovery rate, a density bound or LOW-YIELD (no nine-plane positive control, power unmeasured); that this miss
  earns or rules out a Stage B night.
* **Verdict for the direction** (DR7 / DR18 at nine faces): **OPEN@8.01 core-h** (Stage A list exhausted, 2,004/2,004
  UNSAT-SOLVER, 0 SAT, 0 open; discovery power unmeasured). H-261112-01 stays open.
* **Next step**: no new row. Stage B (E-261112-02) stays a gated queue item: its PLAN, independent rank-4 count, actual
  orbits and 50-cell timing gate come before any compute, and its night needs the owner's budget decision on its own
  merits. Otherwise week item 2 (E-261110-02 prep).
* **Rows updated**: `STATUS.md` header and section 3ae, `ROADMAP.md` E-261112-01 State `done`, `experiment-log.md`
  (2026-11-13), H-261112-01 evidence.
