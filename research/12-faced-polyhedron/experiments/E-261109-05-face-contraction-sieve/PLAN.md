# E-261109-05: face-contraction sieve, power test on the 203 known-UNSAT (9, 3) maps

Pre-registration, 2026-11-09. Focus S5 (10, 4); this run is on (9, 3) formulas with known answers. Label ceiling EXACT per
sub-formula; no geometric claim.

* **ROADMAP row / scores**: T 1 D 2 F 2 G 2 R 2 (T + D = 3). The lead review 2026-11-09 scored D 1 (below gate); the owner
  asked for the run on 2026-11-09 after `reviews/strategy-review-2026-11-09-owner-ideas.md` §2, whose break-even argument
  (the kill rate decides whether strata A and B are sieved before their nights) restores D 2. Not a parked method:
  E-261108-02 grouped clauses by constraint face tuples; this groups them by the contraction at one element.
* **Question**: what fraction of the 203 admissible (9, 3) plain formulas (all UNSAT-VERIFIED, STATUS 3d) is already UNSAT
  on the clauses of the rank-3 contraction at one face?
* **Hypotheses moved**: H-261101-07 (only through the cost of the (10, 4) sweep, not its answer); H-261101-11 (a few-face
  core): a kill shows a one-face obstruction, none weakens it at this grouping.
* **H1 / H0**: H1: >= 27 of 203 maps (about 13 %, the break-even of the addendum) are killed. H0: < 20 of 203.
* **Method** (`sieve.py`): rebuild the plain formula (`pilot.build`, `ALL_OPTS`, `from_links`), compare with every recorded
  `formula_sha256` of E-261103-03. Every variable is a chirotope sign q_S or a Tseitin gate (`omsat.CNF`). For each clause,
  I(clause) = the intersection of the 4-sets S over the signs in its transitive gate support. con(X) = all gate definition
  clauses + every other clause with X in I(clause); asserted to be a clause subset of the formula, so con(X) UNSAT =>
  the formula UNSAT. X = 0..8 (the verdict) and X = INF (descriptive: the normals' arrangement). Each con(X) by `pilot.solve`
  (CaDiCaL + drat-trim, cap 20 s, checker cap 20 s); a map is killed iff some face X gives UNSAT-VERIFIED.
* **Measured before registration (structure only, no solve)**: con(X) has about 10,150 non-definition clauses, of which
  10,080 are the rank-3 GP relations at X; the rest are INCONS, RFCONS, POC and SEGMENT_DISJOINT at X. TRIPLE and REFLEX1
  never enter (each mentions three faces), so the sieve tests only whether face X's polygon is consistent on its own.
* **Controls**: C0 negative (convex 9-face control, full formula SAT within 60 s): every con(X) must be SAT. C1 positive
  (C0 + units q_S and -q_S, S = {4, 5, 6, INF}): con(X) UNSAT-VERIFIED exactly for X in {4, 5, 6, INF}, SAT otherwise.
  C2 (another map with the control's planes pinned, UNSAT-VERIFIED in E-261103-03): descriptive, which X fire.
* **Pilot** (shard-free, minutes): C0, C1, C2, maps 40 and 0. It could expose an empty or constant measurer or slow solves.
* **Pilot gate**: C0 and C1 as stated; median con(X) solve < 2 s; projected total <= 2 core-h. Else escalate.
* **Predictions**: (P1) fewer than 20 of 203 killed (~85 %; TRIPLE is outside every contraction). (P2) con(INF) is SAT on
  all 203 (~80 %). (P3) no con(X) times out (~80 %).
* **Grid**: one cap (20 s). The cap matters only through TIMEOUTs, which are counted and reported, not read as kills.
* **Budget**: <= 2 core-h, one session, 10 shards (`SHARDS=10`, units round-robin), laptop, minutes of wall time.
* **Power statement**: decides, for each of the 203 maps and each face, whether the contraction sub-formula alone is
  UNSAT. It says nothing about pairs or triples of contractions, other groupings, or (10, 4) maps; a TIMEOUT is unknown.
* **Counter calibration**: no float diagnostic. The discrete measure (killed / face set) is calibrated by C0 (none) and C1
  (exactly {4, 5, 6} plus INF); a kill count equal for all maps is not a phenomenon unless C1 moves it.
* **Scenario move**: none of A / B / C (the answers of these maps are known); only the price of the (10, 4) sweep.
* **Outcomes**:
  * >= 27 killed: pass -> follow-up below.
  * < 20 killed: park I-261108-06 with the measured rate, scope "one-face contraction, cap 20 s, the 203 (9,3) maps".
  * 20-26: record the rate; the lead decides.
  * any con(X) SAT on C1 at X in {4, 5, 6}, or UNSAT on C0: measurer bug, stop. A SAT full formula cannot happen here.
* **Follow-up tree**: pass -> a PLAN amendment to sieve the 757 (10, 4) maps of strata A and B (minutes per map, no DRAT
  needed for skipping, UNSAT-SOLVER may skip a map; the owner approves the run); the result feeds the queue order of N2.
* **Stop rule**: 1 session, 2 core-h, then conclude.
* **STATUS / ROADMAP for each outcome**: one STATUS line (3ac) with the kill rate; ROADMAP row done; I-261108-06 status
  `tested` with the verdict.

## Amendments

### Pilot 2026-11-09 (no plan change)

* Scratchpad run of C0, C1, C2, maps 40 and 0 (not recorded as results): C0 full SAT, every con(X) SAT (pass); C1 con(X)
  UNSAT-VERIFIED exactly at 4, 5, 6, INF (pass); C2 fires at face 1 only (descriptive: the measure moves on a non-planted
  contradiction); maps 40 and 0 not killed. Every solve 0.02-0.08 s; projected total about 3 min wall. Gate passed.
