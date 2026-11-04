# E-261103-05: bounded disk-aware solid-first explore pilot

Pre-registration, 2026-11-04. Focus S5 (9,3); this pilot calibrates auxiliary (8,3) controls (S1
at eight faces), not a focus witness. Branch inherits 7509f39 and its S5 verification tools;
no main integration, push or PR. ROADMAP scores T D F G R=2 2 2 1 2, T+D=4.

* Tests: H-261103-02 and H-261101-07. H1: the disk-aware chamber solver reproduces both known
  (8,3) controls unseeded, then recovers an (8,3) solid from one of sixteen random D2 arrangements.
  Rival H0: this configuration lacks that recovery power at this budget. Failure moves engine
  allocation, not geometric existence credences. What differs from DR7/DR18: 1-3 edge runs per
  plane pair, all pairs adjacent, hard total-edge count, and hard connected-disk face constraints.
* Reuse solid_cpsat.best_solid and solid_fast.Tables. Preserve the old default one-run API.
  In hard decision mode require every pair, target E=36 for F=8,g=3, max three runs per pair,
  connected selected boundary facets on each plane, chi=1 and no diagonal pinch. Connectedness
  uses rooted integral flow over facet adjacency. A connected bounded planar manifold region
  with chi=1 is a disk. No lazy no-good cuts enter this decision path. The encoding argument is
  PROVED-1; CP-SAT is not an independently checked DRAT certificate.
* Construct chamber sign vectors, bounded cells and line orders from exact rational triple
  points and integer normals. Check the only float signs consumed by existing Tables against
  those exact signs; reject a mismatch or nonuniform arrangement as ERROR, never INFEASIBLE.
  Extract links from boundary edge runs, preserving parallel-edge pairings; do not reconstruct
  a multiple-edge map from its triangle set alone. Verify resulting integer planes/links with
  ladder_exact and verify_candidate --all-pairs. Required control topology: V,E,F,chi=24,36,8,-4.
* Controls before random sampling: unit tetrahedron positive (E=6), disconnected-face flow
  rejection and legacy API regression; saved pilot negative tetrahedron E=7 INFEASIBLE. Then R2:
  Roest-Vigh and Mizhaev own planes, no hints, no pinned occupancy or supplied map constraints.
  Solver cutoff grid 15/60 seconds, at most two calls per control, skipping a completed recovery.
  Require exact EMBEDDED, all 28 pairs, the required topology and matching known cyclic links
  up to rotation/reversal per face. Compare against raw input, not an optimizer diagnostic.
  R2 failure stops R3 and gives UNDERPOWERED, not an exclusion of either geometric family.
* R3 only after both R2 passes: sixteen deterministic D2 two-orbit arrangements, seeds 0..15,
  four proper half-turn images of each of two seed planes. Sample nonzero normal components
  from [-8,8], offset from [-8,-1], with PRNG seed 2611030500+seed; reject exact degeneracies,
  at most 200 draws per seed. D2 normal orbits sum to zero and the uniformity guard excludes
  antipodal pairs. No hemisphere float threshold enters a verdict. Save every accepted input
  and rejection count. S4/C4 arrangements and nine-plane/focus configurations are not run here.
* Use the same 15/60-second solver grid per random arrangement. Skip its 60-second cell after
  a feasible recovery or a completed INFEASIBLE decision. Stop on the first exact (8,3) recovery;
  preserve it and run candidate-check as an auxiliary object, not S5 (9,3). Stop dependent work
  on invalid model, exact/float disagreement, unexpected process error or wrong exact geometry.
  A timeout or a failed random search leaves geometric existence unchanged.
* Prediction: R2 succeeds on both controls by 60 seconds; uncertain R3 prediction: at least one
  of sixteen D2 samples yields an exact (8,3) recovery. No claimed numerical success probability
  is assigned to this uncalibrated catalogue. R3 pass earns a separately pre-registered target
  pilot, not an automatic night. R3 no recovery parks this finite sampler/solver configuration
  with its measured power; the method is not declared dead. Record the limit and used fraction
  for each cell, distinguish solver cutoff from parent/import/build timeout, and assess the
  long-run gates before any later run. No nine-plane random draw is used as a known negative.
* Budget: one worker with numerical/CP-SAT threads pinned to one, 2400-second hard computation
  deadline (under the review's two-core-hour ceiling), plus bounded final hashing/reporting.
  Each worker subprocess has solver cutoff +20 seconds for import/build/validation. Four R2
  calls at most, one five-second negative, up to 32 random calls. Global deadline supersedes
  all unit limits; no multi-hour session run or unattended night. No restart overwrites results.
* Model CP status OPTIMAL/FEASIBLE is only a candidate until the independent exact geometry
  verifier passes; INFEASIBLE refers only to the saved integer CP model for those rational planes,
  target E and max-run bound. UNKNOWN/hard timeout is unresolved. Retain model.pbtxt, input,
  output, logs, source/input/output hashes, dependencies, commit/dirty state and wall/core time.
  All success claims are EXACT only after reproduction in verify_all. No CERTIFIED claim.
* On R2 failure: save its failure output and conclude, do not sample targets. On R3 failure:
  conclude LOW-YIELD at the stated finite budget only if the matched-budget R2 controls pass;
  otherwise UNDERPOWERED. On R3 pass: exact-check auxiliary topology, assess a small separately
  registered nine-plane pilot. This experiment's explore prerequisite for E-261103-03 is concluded
  by either outcome; no E-261103-03 tranche, push, release or PR is part of this pilot.

## Amendments
