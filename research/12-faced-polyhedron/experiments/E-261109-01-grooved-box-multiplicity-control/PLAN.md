# E-261109-01: grooved-box multiplicity control

Pre-registration (`PROTOCOL.md` §2) of `ROADMAP.md` week item 1 (idea I-261108-04), committed before any solver run.

* **ROADMAP row / scores**: T 2 D 2 F 2 G 2 R 2 (lead review 2026-11-08d §7, new idea N1).
* **Question**: does the E-261103-02 encoder (`submap=True`, `ALL_OPTS`) accept a real embedded polyhedron in which one
  face pair shares three (and four) collinear segments?
* **Hypotheses moved**: H-261101-07 only through the caveat of the (8,2)/(9,3) claim and the (10,4) UNSATs (item 1
  follow-up tree); no state change of a hypothesis by itself.
* **H1**: every pinned positive is SAT and every pinned negative is UNSAT-VERIFIED. **H0**: a pinned positive is UNSAT
  or the encoder rejects the map (encoder bug on m >= 3).
* **Object** (`grooved.py`, seeds 2611090102 / 2611090103, exact rationals scaled to integers): a box with
  planes tilted so that no two are parallel, plus k pyramidal notches (3 lateral planes each) across the top/front
  edge. k = 2: F = 12, V = 20, E = 30, top/front share 3 segments; k = 3: F = 15, V = 26, E = 39, 4 segments. Both
  already pass `ladder_exact.verify(require_all_pairs=False)`: EMBEDDED, all faces simple, no bad pair (construction
  check, run before this commit; the controls below are the experiment). Planes in `control_k{2,3}.json`.
* **Negative maps**: the same planes with two link entries exchanged in each of the front and top links (a different
  segment pairing); `grooved.py` keeps only maps with distinct corner triples, consistent edges and chi = 2 on which
  `ladder_exact` says not EMBEDDED, so a loader rejection is not a negative control. First candidate is used.
* **Method**: `control.py`: per k, pinned positive and negative formula (`pilot.build` with `submap=True`, chirotope
  of the planes as unit clauses), CaDiCaL with DRAT checked by drat-trim (default caps 120/120 s); plus the unpinned
  positive formula for k = 2 (12 elements <= 13), solver cap 900 s. Target: S5 encoder control, not a target decision.
* **Controls**: this is the control; the existing convex controls (`control_f9/f10`) are the known-good baseline.
* **Pilot / pilot gate**: none; the whole run is < 0.1 core-h.
* **Predictions**: pinned SAT for k = 2 and 3 (80 %); unpinned k = 2 SAT within 900 s (55 %).
* **Grid**: k in {2, 3} is the parameter (m = k + 1); one seed each.
* **Budget**: < 0.1 core-h, 1 shard, laptop; stop at the first failed pinned positive.
* **Power statement**: tests the multiplicity-3 and -4 clauses on one geometric configuration each (top/front pair
  only); says nothing about other positions of the multiple segments, m >= 5, or maps with several multiple pairs.
* **Counter calibration**: no float diagnostic in the verdict; exactness is rational (`ladder_exact`, planes are
  integers below 2^53 / 1e9 so the float scaling is exact).
* **Scenario move**: pass: no move (removes the A1 residual); fail: stops S5 compute and moves B (all OM-UNSAT)
  down until the encoder is fixed.
* **Outcomes**: pinned positive SAT + negative UNSAT-VERIFIED = pass (record EXACT control). Pinned positive UNSAT =
  failure, stop all S5 compute, escalate (item 1 tree). Negative SAT = the negative is not a control, choose another
  swap and amend. Timeout of the unpinned formula = no information.
* **Follow-up tree**: as week item 1 of `ROADMAP.md`.
* **Stop rule**: all five units done or the first failed pinned positive.
* **STATUS / ROADMAP**: pass -> control recorded in E-261103-02 and STATUS, the item 1 caveat is lifted; fail as the tree.

## Amendments
