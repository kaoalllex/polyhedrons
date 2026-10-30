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
