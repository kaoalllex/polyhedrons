# E-261110-04: owner night, symmetric families at nine planes (amended 2026-11-17, week item 5)

Pre-registration. Do not edit after the run starts; add dated amendments at the end instead.

* **ROADMAP row / scores**: T 1 D 2 F 1 G 1 R 2 (T + D = 3). Week item 5; `reviews/dialogue-2026-11-16-strategy.md`
  §2 row 5 and Appendix A7 (owner-approved).
* **Question**: does the frozen engine of E-261103-05 find a nine-face all-pairs solid (S1, genus free) in random
  C3 3+3+3 or C2 4 x 2 + 1 arrangements at E in {45, 51}, and does a geometric coefficient box change the eight-plane
  D2 2 x 4 hit rate of K13?
* **Hypotheses moved**: none in `tests`. A verified nine-face hit would be new (nothing in print for nine, CLAIMED)
  and sends E-261101-08 to the lead; zero hits parks the distribution and cap of that arm only.
* **H1**: at least one arm has a nine-face hit rate p >= 3 / (its decided units). **H0**: every arm's rate is below.
* **Why**: symmetric families cut the plane parameters and raise the eight- and seven-plane rung rates (K13: D2 2 x 4
  7.1 %; N2: C2 3 x 2 + 1 at 12 x its asymmetric baseline, STATUS 3av). A face fixed by a rotation lies in a plane
  perpendicular to its axis, so C3 on nine all-pairs planes is 3+3+3 (A7, PROVED-1). E = 45, 51 are genus 4, 5
  (E = 3F mod 6; chi = F - E / 3); E = 39 (genus 3) is the parked (9, 3) sweep and is not run.
* **What differs from the parked runs** (E-261107-01, E-261108-01: E = 39, asymmetric or "8-plane winner" families):
  E free in {45, 51}; symmetric families with a measured unit cost (K14: C3, E = 45, median 13.5 s, 70 INFEASIBLE /
  10 UNKNOWN of 80); the C2 arm in a moved chart (E-261117-02 gate passed); no E-261110-03 gate (closed).
* **Method**: `night.py` (reuses `n2.engine`, `n2.chart`, `n2.plane_only`, `n2.verify_candidate`; frozen engine
  unchanged: `best_solid`, hard disk model, one disk face per plane, 1-3 runs per pair, one CP-SAT worker; the solid
  need not be invariant). Unit i of each arm draws one arrangement deterministically from ('E-261110-04', arm, i):
  * c3: three integer planes (coefficients in [-8, 8] without 0, d in [-8, -1]; K14's box) and their images under
    (x, y, z) -> (y, z, x); standard chart; decided at E = 45 and at E = 51 (paired), cap 20 s each.
  * c2: plane (0, 0, +-1, d) and four pairs (a, b, c, d), (-a, -b, c, d), box [-8, 8] without 0; plane-only uniform;
    first far plane of `n2.NORMALS` with a uniform ten-plane chirotope as infinity; E = 45 and 51, cap 20 s each.
  * geo2 / geo3: K13's D2 2 x 4 sampler with every coefficient s q^w (s = +-1, w uniform in {0, ..., 3}; d = -q^w),
    q = 2 (magnitudes 1-8, inside K13's box) and q = 3 (1-27); E = 36, cap 15 s; i < 3000 per q.
  * Rejected draws are counted per unit. Target S1 at nine faces; counters (SPEC §4): units, decided (INFEASIBLE +
    hits), UNKNOWN (cap), REJECTED_BY_ENGINE, ENGINE_ERROR, hits, hits verified.
* **Controls** (stage A, `bash run.sh stage_a`, must PASS before any shard runs; `run.sh` refuses otherwise):
  positive: P1 the moved Szilassi planes (E-261117-02 K3) at E = 21 give an EMBEDDED all-pairs solid with
  `verify_candidate --all-pairs` PASS; P2 K13 seed 4 at E = 36 gives (24, 36, 8, -4), PASS; tetrahedron at E = 6
  OPTIMAL. Negative: K13 seeds 0-3 INFEASIBLE; tetrahedron at E = 7 INFEASIBLE; the unmoved c2 draw rejected
  ("nonuniform triple of normals"); P2's links with two entries swapped fail `verify_candidate`. Exact draw checks on
  units 0-9: c3 orbits, c2 half-turn on plane vectors, moved chirotope uniform with plane-only signs kept, far plane
  beyond every finite triple point, geo coefficients in the declared box. No nine-face positive control exists (no
  nine-face object is known); a nine-face hit is trusted only through `verify_candidate` and `candidate-check`.
* **Pilot**: shard 0 of 1, `DEADLINE=300 SHARDS=1 OUTDIR=pilot bash run.sh 0` (5 min, one core): per arm and E the
  status counts, median and max seconds, UNKNOWN fraction, rejected draws; exposes a c2 chart failure at nine
  planes, an E = 51 cost blow-up or engine errors.
* **Pilot gate**: the binding limit must be the shard deadline, not the per-unit cap: UNKNOWN fraction <= 0.5 in each
  nine-plane (arm, E), no ENGINE_ERROR, REJECTED_BY_ENGINE = 0 in c2. Otherwise amend (drop that (arm, E), or a cap
  change through the lead) before the night.
* **Predictions**: Q1 c3 E = 45 UNKNOWN fraction <= 0.2 in the night (K14 0.125 of 80; ~60 %; fails -> the cap binds,
  UNDERPOWERED for that cell, no cap raise without the lead). Q2 median seconds at E = 51 above E = 45 in c3 (~60 %;
  decides which E a follow-up keeps). Q3 c2 median <= c3 median at E = 45 (~50 %; prices the C2 family at nine
  planes). Q4 geo2 rate outside K13's Wilson interval [0.045, 0.111] (~40 %; inside -> the coefficient distribution
  does not matter at this rung, geo arm parked). Q5 a verified nine-face hit in any cell (~5 %).
* **Grid**: E in {45, 51} (the genus is the parameter the outcome may depend on); q in {2, 3}. Caps fixed by A7.
* **Budget**: one owner night, 10 shards x DEADLINE 27000 s = 75 core-h (<= 80), laptop on AC under
  `overnight/launch.sh 10-04 start` (`caffeinate -dimsu`, `nice`). Pilot <= 0.1 core-h, stage A < 0.1.
* **Power statement**: units are interleaved over the arms, so the deadline cut keeps them balanced. At K14's cost
  (about 27 s per c3 unit for both E) and similar c2 cost, each nine-plane (arm, E) gets about 4,500 units; zero hits
  in n decided units rejects p >= 3.0 / n (about 7e-4) for that family, box, cap and E only (95 %). It cannot exclude
  rarer hits, other boxes or caps, symmetric solids missed by the cap (UNKNOWN), or any other family. geo: 3000 draws
  per q give a Wilson half-width of about 0.01 near 7 %; the baseline K13 (240 draws, archived, not rerun) is the
  weak side of the comparison.
* **Proofs**: none. INFEASIBLE is a CP-SAT status for one arrangement and E (`UNSAT-SOLVER` level), no negative claim.
* **Counter calibration**: no float diagnostic enters the verdict; hits are decided by exact `verify`/`verify_candidate`.
* **Scenario move**: A (exists) +small on a verified nine-face hit (it is not a 12-face object); B, C unchanged in
  every outcome (nine faces at genus >= 4 do not bear on the (12, 6) chirotopes).
* **Outcomes**: hit = an EMBEDDED all-pairs nine-face solid with `verify_candidate --all-pairs` PASS (run inline;
  it stops the night); reported as an S1 object with its genus and multiplicities, never S5 or S0, only after
  `candidate-check`. INFEASIBLE = no solid with that E in that arrangement (solver level). UNKNOWN = no information.
  Near-misses do not count. ENGINE_ERROR = a failed control: stop, diagnose, no verdict from that night.
* **Follow-up tree**: SOLID -> `candidate-check`, `--all-pairs` nine faces, escalate; E-261101-08 to the lead. Zero
  hits -> that (family, box, cap, E) parked with its p bound. geo rate outside K13's interval -> a note for the lead
  (link to P4 only if C1 recovers a hit's chirotope); inside -> geo arm parked.
* **Stop rule**: the first verified nine-face hit (all shards stop after their unit), a failed control, or the deadline.
* **STATUS / ROADMAP**: a new STATUS section with the table per (arm, E); ROADMAP row done (or a SOLID escalation).

## Amendments
