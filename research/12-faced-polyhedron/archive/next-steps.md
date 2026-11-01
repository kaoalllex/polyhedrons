# Next steps

## Cycle 1 (in progress, 2026-10-29)
Literature (done), enumeration (done: 59 confirmed), OM-SAT encoder with controls and
independent reproduction of 2-3 claimed symmetric UNSAT results, geometry-first SAT with
controls, theory notes, adversarial verification of the foundations, PI experiment E-PI-1
(exact single-plane relocation from near-misses).

## Cycle 2 candidates (ranked by expected value)

1. **j-plane OM-SAT neighbourhoods ("SAT-LNS").** Take a near-miss configuration, fix the
   chirotope on all quadruples of the 13 elements that avoid a chosen set J of j free planes
   (exact signs from the configuration), and let SAT decide whether ANY chirotope extending
   this partial one satisfies all embedding clauses.
   * j = 1 is exactly the single-plane relocation problem (realizable answers = cells of a
     220-hyperplane arrangement), so it cross-checks E-PI-1.
   * UNSAT for j planes = a certificate that no modification of those j planes (even at the
     oriented-matroid level) repairs the near-miss: a rigorous local-optimality statement.
   * SAT = a candidate oriented matroid close to a realizable configuration; realize it by
     placing the j planes cell by cell (LP feasibility per single-element extension, with
     Farkas-certificate cuts fed back to SAT in a CEGAR loop).
   * Measuring how solve time grows with j tells how far the "local" structure determines the
     global problem (prior work: full j = 12 instances need ~300 core-hours per map).
2. **Iterated local search** = exact relocation + random kicks of other planes, over the ~60
   asymmetric seeds with <= 7 violations; 2 cores.
3. **Geometry-first MaxSAT on near-miss arrangements**: does any OTHER labeled triangulation
   fit a near-miss arrangement better than its own?

## Night 5 candidates (2026-10-30; decide after nights 3-4)
1. Resume night 4 (`./run_night4.sh` again continues the archive) if it is still improving.
2. Flip arms in `archive_climb`: when an arm stalls at a fixed violation pattern that vanishes only in
   a degenerate limit, try the 2-2 flips of the dual map at the collapsing edges (valid ones only) as
   new targets.
3. More chains per type (`glad --reps 4`) for the types that realized genus 2: different sub-map
   sequences give different genus-3 maps (chain choice decided type 0's genus 3).
4. Exact local obstruction test of a stuck pattern (OM-SAT / LP on the planes involved): if it is
   UNSAT, that handle on that realization family is impossible and can be pruned.
