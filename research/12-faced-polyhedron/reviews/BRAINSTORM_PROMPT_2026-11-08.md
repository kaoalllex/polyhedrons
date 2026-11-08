# Prompt for a creative brainstorm session (2026-11-08)

## How to run

1. Open a **new** session (not the session of review 08e), ideally with a different strong model than the lead's
   for diversity, in the repository `kaoalllex/polyhedrons`, branch `lab/2026-11-08`.
2. Paste everything between the two `-----` lines as the first message.

The session writes `research/12-faced-polyhedron/reviews/brainstorm-<date>.md`, commits it, does not push. The lead
filters the result; nothing enters the queue without the owner.

-----

You are a creative mathematician invited to a brainstorm on an open problem in discrete geometry. Your job is
**divergence**: many bold, varied ideas. Judging comes later and mostly from someone else. Do not read `STATUS.md`,
`ROADMAP.md`, `reviews/`, experiment folders or idea files before Phase 2: they would anchor you to what was already
tried. The brief below is all you need.

**The problem.** Find an embedded closed polyhedral surface in R^3 with 10 planar simple polygonal faces, genus 4,
exactly three faces at every vertex, in which every two faces share an edge (45 pairs; three pairs share two or three
collinear edge segments, so E = 48, V = 32). Known face-neighbourly polyhedra: the tetrahedron (4 faces, genus 0),
Szilassi's polyhedron (7 hexagons, genus 1, a 3D model of the 7-colour map on the torus) and two 8-face genus-3
polyhedra from 2026 (Mizhaev; Roest-Vigh), whose face pairs share up to two edges. The cubic 8-face genus-2 and
9-face genus-3 cases have no solution according to an exact computer search over all candidate maps (conditional,
unreviewed). The grand prize behind it: 12 faces, genus 6, every pair sharing exactly one edge, each face an 11-gon:
a 3D model of the 12-colour map on the genus-6 surface (Heawood bound, Ringel-Youngs); open since the 1970s. A
polyhedron is given by its face planes plus a combinatorial map; vertices are triple points of planes.

**Already tried, do not reinvent** (each failed or stalled at the stated point): numerical optimization of the planes
(annealing, CMA-ES, gradient, ten engines; stuck at genus 3 for 12 faces); ladders that add handles one by one
(a wall between genus 3 and 4); exact SAT over oriented matroids map by map (works at 9 faces, too slow at 10);
choosing cells of a plane arrangement (solid-first); a ninth plane added to the known 8-face objects; symmetric
ansatzes (symmetric 12-face solutions are excluded); normals first, then offsets by LP. Already proposed: the
Boolean union of two projectively matched Szilassi solids (10 planes, genus 1 + 1 + 2 = 4).

**Phase 1, divergent (write it first, no filtering).** 25 ideas, one to three lines each:
* from at least 8 different fields, for example: architecture and freeform facades, origami and rigid folding,
  crystallography and periodic structures, knot theory and 3-manifolds, physics simulation and self-assembly,
  evolutionary design, game-playing search, tropical and real algebraic geometry, number theory and integer
  constructions, art and sculpture (Escher, Szilassi's own way of finding his polyhedron), history of mathematics;
* at least 5 deliberately crazy ideas;
* reframings count as ideas: change the question, the representation, the object you search for, or the order
  of construction;
* the owner's seeds, each taken to its boldest version: an invariant like a determinant that only solutions have;
  solutions as points of one function, recovered by interpolation; matrices and eigenvalues; search for a method of
  search rather than a solution; the map/graph view as in the four colour theorem; proof of non-existence or of
  existence by contradiction; trading a handle for something simpler ("bubbles"), solving, transforming back.
No hedging, no feasibility comments in Phase 1.

**Phase 2, convergent (only after Phase 1 is written).** Now read the titles in `research/12-faced-polyhedron/ideas/`
and mark duplicates. Pick the 5 best non-duplicates by surprise times the chance of a cheap decisive test. For each:
the mechanism (why it might work where the listed approaches stalled), the cheapest test within one session and one
core-hour, and what result would kill it. Small checks of at most ~10 minutes are allowed; nothing longer.

**Rules.** Never fabricate results or citations; a recalled reference is marked "from memory, unchecked". Everything
is an untested proposal. Do not discuss proof audits, encoder soundness, the census, benchmarks, the perturbation
lemma or the research process: other sessions handle them. Write in English; talk to the owner in Russian.

**Output:** `research/12-faced-polyhedron/reviews/brainstorm-<date>.md` with Phase 1 (all 25 ideas, kept even if
duplicates) and Phase 2 (top 5). Commit on the current branch, do not push. Then tell the owner, in Russian, your
three favourite ideas in one sentence each.

-----
