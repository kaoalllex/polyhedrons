# Addendum to the lead review 2026-11-09: the owner's ideas

Date: 2026-11-09. Owner's request after the lead review: assess six ideas that change the representation of the
problem. This addendum advises only; it changes no ledger file and no week plan. Every recommendation below is an
untested proposal, not evidence.

## 1. Considered and not taken

The reason is recorded so that an idea is reopened only with a new argument, not re-litigated.

| Idea | Verdict | Reason |
|---|---|---|
| Polyhedron as vectors | Already the representation | Each face is a plane, a vector (n, d) in R^4; the chirotope is the sign vector of its 4x4 determinants (FD1, FD2, FD4). It is minimal: 30 parameters, about 18 after the affine group. Other vector views are filed: normals only (DR9), Maxwell-Cremona (I-261029-01). Gale duality goes from rank 4 on 11 elements to rank 7, which is worse. |
| Weyl's equidistribution criterion | Not taken | The degree-1 analogue for a closed surface is Minkowski's condition, sum of area x normal = 0. As a filter on normals it says only "not in an open hemisphere", which the covering condition of FD7 already implies. Its other use, low-discrepancy (Sobol, Halton) starts and coverage measures for random samplers, improves sampling, which the strategy deprioritises, and cannot exclude a solution region of small measure. |
| Discrepancy theory, Spencer's six-deviations method | Not taken | The constraints are sign consistency (Grassmann-Pluecker, forbidden triples), not balance. Only the Bansal / Lovett-Meka rounding walk transfers, as a cousin of I-261029-20. A heuristic that only finds models does not speed up UNSAT maps, and every (8, 2) and (9, 3) map was UNSAT (STATUS 3d, EXACT, formula scope); kissat already decides a map exactly. |
| Vertices as points of the complex plane / solving over C | Not taken | In the face-plane formulation there are no equations: vertices are intersections of plane triples, and the whole problem is strict sign inequalities (FD1: open realization space). C has no order, so the complexified problem keeps none of the difficulty and is trivially feasible; a point of R^3 does not fit in C anyway. The legitimate uses of C are filed: complex homotopy detours (I-261029-19), unit-phase relaxation (I-261029-20); the Riemann-sphere view of the Gauss map restates FD7. |

## 2. The "radar" (Littlewood polynomials, matched filtering)

A matched filter needs a known template. There is no positive S5 example at our sizes: every admissible (8, 2) and
(9, 3) formula is UNSAT (STATUS 3d, EXACT, formula scope), so a radar of "where to go" cannot be calibrated. Its
sound form is a radar of "where not to go": local obstructions as the signal, used to prune and order the (10, 4)
maps. Analogy (not evidence): the odd-length Barker-sequence question, a +-1 search like ours, was closed by a parity
argument; for even lengths the work is exhaustive structured search plus number-theoretic obstructions, the shape
of our SAT sweep plus obstruction mining.

What already exists:

* E-261108-02 (EXACT per sub-formula, NUMERICAL as a census): 0 of 24 admissible 11-gon (9, 3) maps have an UNSAT
  face-support sub-formula on <= 6 faces, 0 at 7 faces. In that grouping the obstructions are not local, so an
  ordering by "known local obstructions" has no signal today.
* I-261108-06, the face-contraction sieve (the rank-3 contraction at one face), is a different clause subset that
  E-261108-02 did not test. The lead review 2026-11-09 scored it below the gate (D 2 -> 1): one kissat solve per map
  costs about what the sieve's power test risks.
* N2 of the lead review 2026-11-09 (empirical hardness model for queue order) is the "ordering" half of the radar
  and is already queued after week item 1.

Break-even, a scenario from recorded numbers, not a measurement: the mean full solve is about 475 / 1117 = 0.43
core-h per (10, 4) map (STATUS 3x, scenario); the sieve costs at most 10 faces x 20 s = 0.056 core-h per map at its
cap. If no map is SAT, so that the sweep runs to the end, the sieve pays for itself when it kills more than about
13 % of the maps (less if its sub-formulas finish well under the cap). The idea's own kill rule (>= 20 of 203 (9, 3)
maps, about 10 %) is close to that line.

**Proposal for the next lead review (filed at the owner's request; no run approved):** one explore item, "obstruction
radar": the power test of I-261108-06 on the 203 known-UNSAT (9, 3) maps (<= 1 core-h, 8-10 shards, day run).
Kill: < 20 of 203 -> park the sieve with its measured kill rate. >= 27 of 203 (about 13 %) -> sieve the (10, 4) maps
of strata A and B before their nights and feed the result into N2's ordering. In between -> record the rate; the
lead decides. It does not displace week items 1-3.

## 3. Witnesses: how they were found and why progress stopped

For the owner's question; this repeats the ledger (STATUS 2, DR1, DR3) and adds nothing to it.

* `lab_solid_genus3` (E-261030-02): annealing over 12 random planes with an exact CP-SAT inner step that selects the
  best solid of the arrangement. Plateau at 48 of 66 pairs; dead-end map (handles reach at most 54).
* `lab_type0_genus3` (E-261030-03): genus ladder inside the type-0 target map, from the sphere upwards one handle
  at a time, extendable by construction (3-handle completion certificate, E-261101-02).
* Genus 4 was never reached (DR1). The Gauss gate explains it for type 0: all 21 arms (7 realizations x 3 arms) have
  k_tau = 0, while each handle must lower the Gauss degree by one (FD7, DR3). This is the origin of "jump, do not
  climb" (`STRATEGY.md` §2) and of the exact per-map route.

## 4. Result (added 2026-11-09)

The owner asked for the power test at once: E-261109-05, 0 of 203 maps killed, controls pass; the proposal of §2 is
closed and I-261108-06 is parked (STATUS 3ac).
