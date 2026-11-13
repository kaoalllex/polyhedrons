# E-261113-03: rung-below cell census over seven planes of Roest-Vigh

Pre-registration, 2026-11-13, week item 5 (prep only this week; the census run needs the owner). Committed before the
pilot; the list and the code below are part of this commit.

* **ROADMAP row / scores**: T 2 D 2 F 2 G 1 R 2, T + D = 4; explore, control (the discovery-power control of the cell
  method, gate of Stage B, E-261112-02).
* **Question**: when one plane of Roest-Vigh is deleted, how many generic cells of an eighth plane over the remaining
  seven contain an eight-face all-pairs solid under the Stage A model, does the planted cell (the deleted plane's own
  cell) yield one unaided, and which maps (canonical, with genus) appear?
* **Hypotheses moved**: H-261112-01 (a ninth-plane cell of a fixed source holds a nine-face S1 object) only through
  its gate: a second map here is the reason for Stage B; the source map alone parks Stage B at this budget.
* **H1 / H0**: H1: the SOLID cells of the census show at least one map other than Roest-Vigh's. H0: every SOLID cell
  found gives Roest-Vigh's map (the cell family is rigid at this rung).
* **Why**: Stage A has no positive control at nine planes, so its 2,004 UNSAT-SOLVER verdicts carry no discovery-power
  statement (E-261112-01 CONCLUSION); one rung below, an answer is known (I-261113-03, review 2026-11-13 N3).
* **Method**: `census.py`. Source Roest-Vigh; its four symmetries split the planes into {0..3} and {4..7}; deleted
  planes 0 and 4 (every deletion up to symmetry); stabiliser of the deleted plane trivial (checked), so every cell is
  one unit. List: D = 56 dual vectors of the triples of seven planes + INF; cells = union over the vertices X of D of
  X + eps * b, b a local region (`cells.local_cells`, the Stage A algorithm, refactored out of `near_copy_cells`; the
  Stage A list regenerates byte-identical, `units.json` SHA-256 `ef132bc7...`). Representative per cell: max-margin LP
  rounded to 1e-9, checked exactly (`cells.representative`). Decision: the frozen Stage A worker unchanged
  (`stage_a.worker`: `best_solid(target_edges=30, edges_at_least=True, max_runs=3)`: 28 pairs, <= 3 runs per pair,
  connected disk faces, edge runs >= 30, genus free), planes = the seven + the representative, cap 60 s, hard limit
  cap + 30 s, one worker. Every SOLID is verified exactly in the worker (`ladder_exact.verify`, all pairs, V E F chi)
  and classed by `map_canon` (minimum breadth-first code over all roots; mirror images equal) and genus.
* **List certificate (done, `list/certificate.json`)**: per vertex, local regions = Zaslavsky 2 (1 + c2); union =
  m + c3, the rank-4 Zaslavsky count from the flats: delete 0: 12,767 = 12,767 (9,318 vertices), delete 4: 12,764 =
  12,764 (9,309); 5,000 random integer planes per deletion all in the union; planted cell in the union for both; all
  25,531 representatives LP points. `list/units.json.gz`, JSON SHA-256 `9cda089c...15da`, pinned in `census.py`. Queue:
  hash order per deletion, blocks of 10 interleaved, so every shard holds both deletions.
* **Target / counters**: S1 at eight faces (28 pairs, genus free), a rung with known objects; no focus-target result
  is possible. Per unit: SOLID / UNSAT-SOLVER (INFEASIBLE) / UNKNOWN / HARD-TIMEOUT / ERROR; per SOLID: EMBEDDED,
  adjacent pairs, V E F chi, edge runs, genus, map class.
* **Controls**: positive: C0 Roest-Vigh unseeded at K = 30 SOLID; P0, P4 the planted cells through their own list
  units (LP point, not the deleted plane) SOLID with all pairs at eight faces (the discovery-power control proper).
  Negative: C2 tetrahedron at K = 7 INFEASIBLE; the classifier separates Roest-Vigh's and Mizhaev's maps (same V E F)
  and is invariant under 10 random relabellings; the count gate fails on a truncated vertex list (`test_census.py`).
  All controls run first at every start; any failure stops the shard.
* **Pilot**: `PILOT=1` through `overnight/launch.sh`, 10 shards, the first five units of each (50 cells in hash order,
  30 from delete 0, 20 from delete 4), <= 0.5 core-h with controls, charged to the total. Exposes the cost per cell,
  the SOLID rate and any classifier or record error.
* **Pilot gate**: the binding limit must be the 20 core-h budget, not the 60 s cap: report per unit `ended_by` and the
  budget fraction. Projected cost = recorded walls + mean pilot wall x remaining units + controls per start. Projected
  <= 20 core-h, all controls pass, 0 ERROR -> the day run is proposed to the owner unchanged. Projected above 20 core-h
  -> no run; the owner gets priced options (one deletion only; a lower cap with the timeouts left open; a larger budget).
* **Predictions** (CONJECTURE): P1 (about 40 %): the mean cell costs <= 2.8 s, so the census fits 20 core-h. P2 (about
  35 %): the full census shows a map other than Roest-Vigh's. P3 (about 70 %): the pilot's 50 cells hold no SOLID.
* **Grid**: one cap (60 s) suffices for a finite list; a cap-bound pilot is escalated, not re-capped silently.
* **Budget**: <= 20 core-h total (pilot and controls included), 10 shards, at most 10 single-thread workers, owner's
  laptop on AC under caffeinate; stop/resume by records without redoing accepted units.
* **Power**: exhaustive over the certified generic cells of the two deletions if every unit ends; each cell gets one
  CP-SAT solve, which returns one solid, so the distinct maps are a lower bound on the maps the cells hold. Not
  covered: walls (non-generic planes), other sources, more than one solid per cell, pairs with more than 3 runs.
* **Proofs**: none (owner rule); INFEASIBLE is UNSAT-SOLVER for the exact model and never a family negative.
* **Counter calibration**: no float diagnostic decides a verdict; exact signs, counts and the exact geometry check do.
  The LP margin only chooses a representative that is then checked exactly; time prices the run and proves nothing.
* **Scenario move**: none numeric. A second map raises the working weight of a hit inside the ninth-plane families
  (review 2026-11-13 §8, 0.03) for the lead; the source map only leaves it and parks Stage B at this budget.
* **Outcomes**:
  * SOLID with Roest-Vigh's map: the method recovers the source (discovery power at this rung, counted per cell).
  * SOLID with another map (Mizhaev's included): written as a candidate file, `verification/verify_candidate.py FILE
    --all-pairs` with eight faces, then `candidate-check`; escalate; Stage B proposed to the owner. The census goes on.
  * INFEASIBLE: UNSAT-SOLVER for that cell's exact model only.
  * UNKNOWN / HARD-TIMEOUT: the cell stays open; no information; listed by ID.
  * near-miss: not used; only exact SOLID counts.
* **Follow-up tree**: pilot gate pass -> owner launches the day run (`bash research/12-faced-polyhedron/overnight/
  launch.sh 261113-03 start`); fail -> priced options to the owner. After the run: a second map -> Stage B PLAN
  proposed; the source map only -> Stage B parked at this budget; the enumerator is reused by Stage B and the thin-wedge
  replay either way.
* **Stop rule**: a failed control, count or hash check (stop, diagnose), all units recorded, or the budget.
* **STATUS / ROADMAP**: the census numbers (cells, SOLID cells, maps by genus, open cells, core-h) go to STATUS in the
  conclusion commit; ROADMAP E-261113-03 -> done; E-261112-02 -> proposed or parked by the reading above.

## Amendments

**Amendment 1 (pilot, 2026-11-13, lab session; nothing in the plan changes).** `PILOT=1 bash overnight/launch.sh
261113-03 start`, 10 shards, commit `9080665e` in every manifest, clean tree. Controls 40/40 pass: C0, P0 (`d0_c08712`),
P4 (`d4_c04592`) SOLID in every shard with Roest-Vigh's map (`41ed92cc4a913726`, genus 3, V E F chi 24 36 8 -4), C2
INFEASIBLE; so the planted cells give the source object unaided through their LP representatives. Pilot units: 50/50
INFEASIBLE (UNSAT-SOLVER), `ended_by: completed`, 0 SOLID / UNKNOWN / ERROR; wall 1.80-3.53 s (mean 2.34, median 2.30;
delete 0: 2.38, delete 4: 2.29), at most 0.059 of the 60 s cap; controls 97.5 s per start of 10 shards. Gate: the
binding limit is the budget, not the cap; projected total 16.6 core-h (recorded + 2.34 s x 25,481 units + one control
round; another start adds about 0.03 core-h) <= 20 core-h -> **pass**; about 1.7 h wall on 10 cores. P1 so far holds
(2.34 <= 2.8 s), P3 holds (no SOLID in 50); P2 is open, so T + D = 4 stands. The day run uses the same results
directory, skips the 50 recorded units and is the owner's launch.
