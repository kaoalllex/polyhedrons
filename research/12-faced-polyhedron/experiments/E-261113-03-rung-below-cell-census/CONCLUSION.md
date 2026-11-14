# E-261113-03: conclusion

2026-11-14. Pilot (PLAN amendment 1) and one owner day run (`launch.sh 261113-03 start`, 2026-11-13 22:29:57 to
2026-11-14 00:05:57 local), 10 shards, same results directory; the day run skipped the 50 pilot units.

* **Runs**: day run at commit `0da5ebae` in every shard manifest (`manifest-20261113T192958Z.json`; dirty files: only
  the ten pilot `night.log` files of this run, no code), pilot at `9080665e`; `exit_status 0` for both starts in all
  ten `manifest.txt`. `manifest.txt` carries no core-hours; they come from the unit records (`census.py --summary
  results`): units 15.919 core-h + controls 192.2 s = **15.97 core-h** (budget 20), every unit `ended_by: completed`.
  Day-run wall 1 h 36 min; per shard 5,727-5,766 of 7,200 core-s, matching the wall of a single-thread shard, so no
  sleep gap. `units_sha256` `9cda089c...15da` in every manifest.
* **Controls**: 80/80 records pass (two starts x 10 shards x C0, C2, P0, P4): C0 Roest-Vigh SOLID, C2 tetrahedron
  INFEASIBLE, the planted cells P0 (`d0_c08712`) and P4 (`d4_c04592`) SOLID through their LP representatives with
  Roest-Vigh's map (`41ed92cc4a913726`, genus 3, V E F chi 24 36 8 -4) in every shard. The same two cells are SOLID with
  the same map as census units. The classifier tests (Roest-Vigh vs Mizhaev, relabelling invariance, count gate) passed
  at pre-registration (`test_census.py` 4/4); code unchanged since.
* **Results** (`census.py --summary results`): 25,531 / 25,531 cells recorded, 0 open. 25,527 INFEASIBLE
  (UNSAT-SOLVER), **4 SOLID**, 0 UNKNOWN / HARD-TIMEOUT / ERROR. Wall per unit mean 2.24 s, median 2.20, max 5.19
  (<= 0.09 of the 60 s cap). One map class: all 4 SOLID cells (and all 60 SOLID control records) give Roest-Vigh's map,
  genus 3, all 28 pairs, V E F chi 24 36 8 -4, 36 edge runs:

  | unit | deletion | planted | signs differing from the planted cell (of 56) |
  |---|---:|---|---:|
  | `d0_c08712` | 0 | yes | 0 |
  | `d0_c03925` | 0 | no | 35 |
  | `d4_c04592` | 4 | yes | 0 |
  | `d4_c09730` | 4 | no | 21 |

  So each deletion has two cells, far apart in the arrangement, whose eighth plane gives a solid with the source map;
  no cell gives another map (Mizhaev's included).
* **Prediction vs outcome**: P1 (mean <= 2.8 s, ~40 %): **holds** (2.24 s, 15.97 core-h). P2 (a second map, ~35 %):
  **failed**. P3 (no SOLID among the 50 pilot cells, ~70 %): **holds**. H0 (every SOLID cell gives Roest-Vigh's map)
  holds; H1 rejected at this model.
* **Exact verification**: each SOLID is verified in the worker by the exact check (`ladder_exact.verify`: embedded,
  all pairs, V E F chi). No NEW-MAP unit, so no candidate file, no `verify_candidate.py --all-pairs` run and no
  `candidate-check` (the PLAN routes only other maps there); no object here touches a focus target (eight faces).
  No proofs (owner rule): every INFEASIBLE is UNSAT-SOLVER.
* **What may be claimed**:
  * EXACT, instance scope (AI computation, unreviewed): the four listed cells, over the seven planes left after deleting
    plane 0 or 4 of Roest-Vigh, each contain an embedded eight-face all-pairs solid with Roest-Vigh's map (genus 3).
  * NUMERICAL, instance scope: with the frozen Stage A model at eight faces (28 pairs, <= 3 runs per pair, edge runs
    >= 30, genus free, CP-SAT, 60 s cap), the other 25,527 certified generic cells are UNSAT-SOLVER; the cell method
    recovers the known object unaided at this rung (2 / 2 planted cells, plus one non-planted cell per deletion), at
    4 / 25,531 SOLID cells.
* **What may NOT be claimed**: that no other eight-face map lives in these cell families (UNSAT-SOLVER is per exact
  formula; one solid per cell, so the classes are a lower bound; pairs with more than 3 runs not modelled); anything
  about walls (non-generic planes), other deletions' sources, Mizhaev's arrangement, nine planes, or the existence of a
  nine-face S1 object; that the non-planted cells hold new objects beyond another arrangement for the same map.
* **Hypotheses**: H-261112-01: no status change (open); evidence line added: its gate gives the source map only, so
  Stage B is parked at this budget. I-261113-03 -> `tried`.
* **Verdict for the direction**: DR7 / DR18 cell method at the rung below: **discovery power measured, map family rigid
  at this rung: OPEN@15.97 core-h** (25,531 cells, one map class). Not a refutation of Stage B or of H-261112-01.
* **Next step**: by the registered tree, Stage B (E-261112-02) is **parked at this budget**; the enumerator
  (`cells.local_cells`, `census.py`) stays for the thin-wedge replay (I-261110-01) and any later Stage B. The week plan
  is done; the lead review decides the next item.
* **Rows updated**: `STATUS.md` 3ak, header and "As of"; `ROADMAP.md` week item 5, E-261113-03 (done), E-261112-02
  (parked); `experiment-log.md` (2026-11-14); `hypotheses/H-261112-01`; `ideas/I-261113-03`; READMEs of E-261113-03 and
  E-261112-02.
