# E-261118-02: P3-sym, the census-free formula on symmetric quotients (D2 / S4 eight-face rung)

Pre-registration (2026-11-18), at most 80 lines. Amendments at the end.

* **ROADMAP row / scores**: T 2 D 2 F 2 G 2 R 2; week item 3, explore, J 2. What differs from the parked E-261116-07:
  a group action on the planes (the parked-methods rule); one formula per group, 5 workers instead of 1.
* **Question**: does the equivariant P3 formula return an eight-face S1 solid unaided within 30 min under D2 or S4?
* **Hypotheses moved**: H-261101-07 (method only: the rung objects are known). I-261118-01: tested by the rung.
  I-261118-02: corrected (deviation 1).
* **H1 / H0**: H1 = a D2 or S4 unit returns a model that the bridge realizes with `--all-pairs` PASS within its cap;
  H0 = no realized model in either unit (UNKNOWN, infeasible or unrealized models only).
* **Why**: both eight-face objects carry a free order-4 group (Roest-Vigh D2, Mizhaev S4, improper); the quads fall
  into 36 (D2) and 34 (S4) orbits of 126, and C3 on nine faces into 72 of 210 (lead review, recomputed EXACT by
  `quad_orbits` here). P3 decided the 70-sign seven-face formula in 8 s and no eight-face cube in 560 s.
* **Method**: `p3sym.py`, `SymFormula` = `p3.Formula` of E-261116-07 (imported, unchanged) plus, per generator
  (perm, det): chi(perm S) = det chi(S) for every quad, x_T = x_gT for every cell, and the implied equalities of
  sigma, tau, facets b and ends (presolve help); orbit gauge (sigma_k(t) = + for the least plane k of each orbit,
  t = 012 or 345 avoiding k); mirror normalisation chi(0, 3, 6, INF) = +. Soundness (PROVED-1, this session, module
  docstring): for an isometry g fixing the origin and outward planes, A = diag(g, 1) is orthogonal, A h_m = lambda
  h_perm(m) with lambda > 0, det A = det g, A h_INF = h_INF; reorientations constant on orbits and the reflection keep
  the equalities, so the gauge and the mirror lose no solid. An action forcing a zero sign raises (out of domain).
  Groups: D2 = <(01)(23)(45)(67), (02)(13)(46)(57)>, det +1; S4 = <(0123)(4567)>, det -1. Target S1 at eight faces,
  E = 36, all pairs adjacent (genus 3; never S5 or S0). Counters (SPEC §4): CP-SAT status per solve, seconds, cap
  fraction, models, decode, GP check, invariance check, bridge status, core-seconds.
* **Units** (laptop, owner launch, `launch.sh 261118-02 start`): shard 0 D2, shard 1 S4 (5 workers each, cap 1800 s,
  concurrent); shard 2 plain cube 5 of E-261116-07 with 8 workers, after both, cap min(900 s, (5.6 core-h - used) / 8),
  skipped below 60 s; shards 3-9 idle (one CP-SAT search per formula; at most 10 cores at any time). Per unit at most
  3 models: each decoded, GP- and invariance-checked independently in Python, then the frozen E-261103-03 bridge
  (<= 240 s) and the saved-file `verify_candidate.py --all-pairs`; the unit stops on the first realized model, else
  blocks that chirotope and goes on.
* **Unit tests (`test_p3sym.py`, run in this commit, 6 OK)**: orbit counts 36 / 34 / 72; group orders and an
  inconsistent det raising; no forced zero for D2, S4, C3, forced zeros for C4, Cs 3 x 2 + 1, C2 3 x 2 + 1 (standard
  chart), Cs 4 x 2 + 1; exact integer check that two mirror pairs are concurrent and a half-turn pair, its fixed face
  and INF are dependent; both normal forms invariant under their group, not the other; Roest-Vigh pinned OPTIMAL,
  EMBEDDED, invariant, (24, 36, 8, -4), and INFEASIBLE under S4.
* **Controls** (`run.sh controls`, session, seconds): positive, Roest-Vigh (D2) and Mizhaev (S4; relabelled by
  (0 6 1 7 2 5 3 4), its rotoreflection (0 6 1 7)(2 5 3 4)) brought into the normal form (orientation, orbit gauge,
  mirror) and pinned: OPTIMAL, decoded, EMBEDDED, invariant (this is gauge reachability); Roest-Vigh in its raw
  orientation with gauge and mirror off: OPTIMAL. Negative: each object pinned under the other group, and Roest-Vigh
  with one equivariant quad orbit flipped (GP broken): INFEASIBLE. In-run positive: the rung itself (both formulas
  contain a known solid, by the gauge-reachability control).
* **Deviations from the row**: (1) The Cs 3 x 2 + 1 control at (7, 21) is dropped: a mirror swapping two pairs of
  planes makes the four concurrent (A = diag(R, 1), det A = -1: det(Ah, h, Ak, k) is both -D and, by two column
  swaps, D = det(h, Ah, k, Ak), so D = 0), so the action forces chi(0123) = 0
  in every chart and the formula is out of P3's uniform domain; INFEASIBLE would test nothing (PROVED-1, exact check
  in the tests). The same excludes Cs 4 x 2 + 1 and Cs 3 x 2 + 3 at nine faces from P3-sym: to the lead. (2) A
  subclass in this folder instead of an edit of `p3.py`: the default and the stage-A regression are unchanged by
  construction (`p3.py` hash in the manifests). (3) The row's caps sum to 7 core-h (2 x 5 x 0.5 + 8 x 0.25) against
  <= 6: the side unit takes what is left (above). (4) The orbit gauge replaces the 012 / 345 gauge; for C3 the two
  coincide under the equalities.
* **Pilot** (session, after this commit): the controls, then shards 0 and 1 together with `PILOT=1` (cap 120 s,
  0.33 core-h). Exposes build or memory faults, a broken unit record, the bridge path on a model.
* **Pilot gate**: controls PASS; both units build, solve and record (status, cap fraction, sizes); the owner run
  then fits 5.6 core-h by construction. A failed control: repair once, then park.
* **Predictions**: (P1) controls pass (0.95); (P2) D2 returns a model within 30 min (0.5); (P3) S4 does (0.45); (P4)
  at least one rung model is realized with `--all-pairs` PASS (0.35); (P5) the plain cube 5 with 8 workers finds no
  model in its cap (0.75).
* **Grid**: one cap per unit (the row's); the question is per group. One seed (0, then 1, 2 after blocking).
* **Budget**: session <= 0.4 core-h (controls, pilot); owner run <= 5.6 core-h, about 45 min wall; total <= 6 core-h.
* **Power**: decides only what CP-SAT finds in 30 min on 5 workers; UNKNOWN carries no information. A rung failure
  says the method fails on this host at this cap on formulas known to be satisfiable, nothing about existence.
* **Proofs**: none. An INFEASIBLE rung unit would contradict the gauge-reachability control: stop and repair.
* **Counter calibration**: no float diagnostic enters the verdict; statuses are CP-SAT's; the invariance check is
  boolean with controls on both sides (normal forms true, wrong group false); bridge `wrong_signs` is an integer.
* **Scenario move**: rung pass: none for existence (known types), P3-sym becomes the nine-face route; rung failure:
  none for existence, the stance question of the lead review §1 item 9 goes to the owner.
* **Outcomes**:
  * model realized, `--all-pairs` PASS: a rung pass (a known type, or a new eight-face type -> `candidate-check`).
  * model not realized: an OM model with a solid, not a polyhedron; listed with `wrong_signs`; not a rung pass.
  * INFEASIBLE: contradicts the controls -> repair. UNKNOWN at the cap: no information.
* **Follow-up tree**: a rung pass -> amendment with the C3 3+3+3 nine-face units (E = 45, 51, 57; cap max(3 x the
  rung time to the realized model, 1 h); <= 40 core-h; one owner run); its SAT -> bridge, `--all-pairs` nine faces,
  `candidate-check`, escalate; its UNSAT-SOLVER -> slice closed for planning (never "no nine-face object"); UNKNOWN
  -> UNDERPOWERED, to the lead. No rung pass -> park P3-sym with the cause, week item 6 (E-261117-04).
* **Kill / stop rule**: a failed control; all three units recorded; or 6 core-h.
* **STATUS / ROADMAP**: row to done with the verdict; one STATUS line (formula scope, host, caps); the Cs exclusion
  and the corrected family list to I-261118-02 and the lead.

## Amendments

### 2026-11-18: amendment 1, the rung passed in the pilot; the nine-face follow-up registered

Controls (`results/controls/`, commit `5cbe026a`): all PASS (orbit counts 36 / 34 / 72; forced zeros as listed; both
normal forms pinned OPTIMAL, EMBEDDED, invariant; three negatives INFEASIBLE). Rung pilot (`results/pilot/0`, `1`;
shards 0, 1, cap 120 s, 5 workers each, about 0.02 core-h): D2 OPTIMAL in 2.3 s, S4 in 5.0 s; each first model
GP-valid, decoded (V 24, E 36), invariant, realized by the bridge (hinge) with `--all-pairs` PASS. Census codes
(`p3sym.py types`, EXACT): the D2 model is Roest-Vigh's map, the S4 model Mizhaev's. Known objects returned unaided:
the rung passes (H1; P2-P4 held). The 30-min rung units are not rerun (their cap never bound; same seeds).
Follow-up (the registered branch): C3 3+3+3 at nine faces, E = 45, 51, 57, cap max(3 x 5.0 s, 1 h) = 1 h, 5 workers
as on the rung, at most 20 models per unit (each checked and bridged; stop at the first realized); E = 45 and 51
together, then 57; then the side unit (plain cube 5, 8 workers, 15 min). <= 17 core-h, <= 2.3 h wall, one owner run
(`launch.sh 261118-02 start`). Cs 4 x 2 + 1 dropped (deviation 1). C3 pilot first (session, shards 0-2, cap 60 s,
`results/pilot-c3/`): gate = all three build and record at nine faces. Any realized nine-face model goes to
`candidate-check` and the owner before anything else. Scope of an INFEASIBLE: UNSAT-SOLVER of that formula (uniform in
the standard chart, cubic, one disk per plane, C3 with orbits 012 / 345 / 678), slice closed for planning only.
