# TODO: who is working on "the next polyhedron after Szilassi" (to study)

Owner's question (2026-10-30): what is going on in the world right now on finding the next polyhedron after
Szilassi; is there anything useful for this project? Study the materials below (primary sources, not
summaries), extract methods, exact statements, coordinates usable as positive controls, and anything that
changes our plan. Status: NOT STARTED (waiting for the owner's go after the night-4 script is settled).

Materials named by the owner (from a chat-assistant summary that is itself unverified; check every claim):
* R. Mizhaev, "Integer Realization of an Equivelar Octahedron of Genus 3", arXiv:2609.17700 (Sept. 2026):
  8 nonagonal faces, 24 vertices, 36 edges, genus 3; 20 pairs share one edge, 8 pairs share two collinear
  edges (so not a pairwise-one-edge object). Integer coordinates, CAD-assisted.
* G. Röst, V. Vígh, "A second eight-faced ..." arXiv:2609.32998 (Sept. 2026): combinatorially different
  octahedron with the same characteristics, verified by exact rational arithmetic.
* J. Bokowski, Kevin H., "Polyhedral Embeddings of Triangular Regular Maps of Genus g, 2 <= g <= 14, and
  Neighborly Spatial Polyhedra", Symmetry 17(4) (2025) 622, https://www.mdpi.com/2073-8994/17/4/622
  (already summarized from secondary sources in literature-review.md sec. 6; Sec. 4 and 8.3 still unread).
* Solid Modeling Symposium, Seattle 2003 slides,
  https://www.slideserve.com/yeva/solid-modeling-symposium-seattle-2003 (probably C. Séquin's talk on
  Szilassi/Császár-type models; check relevance).
* People named: L. Schewe (oriented matroids + SAT; vertex version, see literature-review.md sec. 5),
  R. Mizhaev, G. Röst, V. Vígh.

Questions to answer:
1. Search methods of Mizhaev and Röst-Vígh (how did they find the 8-face genus-3 objects; CAD, numerical
   optimization, exhaustive combinatorics?), and whether they address 12 faces at all.
2. Their exact coordinates as POSITIVE CONTROLS for `code/ladder_exact.py` (doubled collinear adjacencies)
   and for the Gauss gate (`code/gauss_gate.py`, degree 1 - g = -2 with doubled edges?).
3. Relation to our ladder: their objects are an n = 8 rung with 8 doubled adjacencies at genus 3; our
   n = 8 rung (genus 2, two doubled adjacencies) stalls at 1 violation. Does more doubling / higher genus
   make realization easier (as the genus-ladder data suggest)?
4. Anything on obstructions for the 12-face case.

## Status 2026-10-30 evening (session 5, out of budget)

* STARTED with the owner's priority (question 2/3: positive control for the n = 8 rung). Blocked: arxiv.org
  is not in the cloud session's allowed network domains (DNS fails); the owner has to allow `arxiv.org`
  (environment settings -> Network access -> Allowed domains), or put the PDFs / coordinate files into
  `literature/`.
* Found while preparing the control (no network needed, do these first next session):
  1. `gauss_gate` / `gauss_degree.coherent_triangles` assume a SIMPLE map: with doubled adjacencies (two
     edges between faces X, Y, as in the 8-face genus-3 objects and our n = 8 rung) an edge key {X, Y} has 4
     triangles and the BFS orientation breaks. Needed: a links-based variant (oriented corners (X, L[i],
     L[i+1]) from the rotation system with repetitions, degree and covering from those corners; target
     chi/2 = 1 - g: -1 for our genus-2 rung, -2 for the genus-3 octahedra).
  2. `ladder_exact.verify` already takes links with repetitions (doubled adjacencies) -> it can check their
     coordinates directly once the face cycles are known.
  3. No n = 8 attempt is saved in the repository (the ladder runs of 2026-10-29 kept only logs): rerun
     `code/ladder.py` / `ladder_ga.py` on n = 8 for a few minutes, save the best attempts (planes + links),
     then run the links-based T1 (target -1) and turning numbers on them (review 2.3: is the n = 8 plateau at
     1 violation a class defect like type-0 genus 4, or an in-class defect?).
  4. Then normals first + exact offsets for n = 8 needs `omsat.Triangulation` with doubled adjacencies
     (partners per edge occurrence, not per face pair) - not supported yet.

## 2026-10-30 late: arxiv reachable (curl); first results

* Abstracts read (full texts downloaded to the session scratchpad only, not committed):
  * Mizhaev, arXiv:2609.17700: integer coordinates, face walks and plane equations given in the paper;
    exact verification; C4 (rotoreflection) symmetry; "based on an earlier construction".
  * Röst-Vígh, arXiv:2609.32998: faces A1: 3x-4y-2z=5, B1: -2x+5y-5z=3 and their images under the
    half-turns about the axes (symmetry D2, chiral); found by "a computational geometric search"; exact
    rational verification; combinatorially different from Mizhaev's; they say their construction procedure
    applied to Mizhaev's planes reproduces his polyhedron (integer vertices in [-300, 300]^3).
* **POSITIVE CONTROL PASSED** (`code/control_rost_vigh.py`, rebuilt from their Table 1 planes and face
  cycles only): our exact verifier `ladder_exact.verify` (doubled collinear adjacencies as repeated link
  entries): EMBEDDED, V/E/F = 24/36/8, 20 single + 8 double pairs, all faces simple; Gauss gate: own
  degree -2 = chi/2, turning +1 on all 8 faces, own gauge admissible (2256 directions), 20 saddles
  (>= 2g+1 = 7). So the degree theorem and our exact tools hold on an independent, published polyhedron
  with doubled adjacencies.
* Next: Mizhaev's coordinates (his tables) as a second control; read Röst-Vígh's "computational geometric
  search" section for the method (symmetric two-orbit plane ansatz: 2 free planes + a symmetry group =
  8 planes; the analogue for 12 faces is excluded for symmetric 12-face polyhedra by our certified UNSAT,
  but a symmetric ansatz for LADDER rungs / genus-ladder levels is not); compare their n = 8, genus 3 with
  our n = 8, genus 2 rung (1 violation plateau).
* Röst-Vígh method (their Sec. 4, verbatim gist): "found by a computational geometric search, using
  significant computational resources ... developed, optimized, implemented in Python, and verified through
  a highly autonomous AI framework. The method rediscovered the Szilassi polyhedron and Mizhaev's example as
  well"; details deferred to a later paper. Their "construction procedure" builds the polyhedron from the
  planes alone (like our solid-first `code/solid_cpsat.py`): applied to Mizhaev's planes it reproduces his
  polyhedron. Mizhaev's planes are given in their Sec. 3 in a +- form (two orbits under the rotoreflection
  T(x,y,z) = (y,-x,-z)). Neither paper claims anything about 12 faces.
* Lesson for us: both 8-face examples are SYMMETRIC (D2, C4 rotoreflection) two-orbit plane sets, i.e. a
  2-plane (8-parameter) search space. For 12 faces every symmetric polyhedron is excluded (our certified
  25/25 UNSAT), but symmetric ansaetze remain open for intermediate objects (ladder rungs with doubled
  adjacencies, genus-ladder levels) and as seeds that are then perturbed asymmetrically.
