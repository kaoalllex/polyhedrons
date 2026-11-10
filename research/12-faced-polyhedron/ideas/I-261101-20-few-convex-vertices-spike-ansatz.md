---
id: I-261101-20
title: Few convex vertices - both known 8-face objects have exactly 4, the covering minimum; search and encode that first
date: 2026-11-01
status: open
direction: [DR9, DR18, DR12]
origin: [L:roestvigh2026, L:mizhaev2026, FD7, I-261101-14]
---

## Idea

Roest-Vigh's and Mizhaev's polyhedra have 20 reflex corners each, one per saddle, hence 20 saddle vertices and only
4 convex vertices, which are the 4 vertices of their tetrahedral convex hull at the ends of long spikes
(`literature/primary-reads-2026-11-01.md`). Four is the minimum compatible with covering (FD7). Szilassi has 6 of 14.
Prior for Szilassi-12: few convex vertices (c = 4 to 8), 36-40 saddles, a tetrahedral or near-tetrahedral hull,
spikes. Use it in three places:

1. E-261101-06: run the rank-3 instance with exactly 4 positive triangles first (their four normal cones must cover
   the sphere like a tetrahedron's), then c <= 8; the instances are far smaller and a c = 4 UNSAT for a type is a
   readable statement.
2. E-261101-16: weight the catalogue towards D2 and S4 arrangements with four far vertices (spikes), as in both
   known objects.
3. E-261101-08: start the C3 doubled-pair ansatz from a spiky tetrahedral core.

## Why it might help

Two independent objects, found by different people with different symmetry groups, share this feature; it is the
kind of empirical regularity a search should exploit before anything else. Lemma B (I-261101-14) explains part of
it: convex tiles cannot tile the sphere exactly, so extra convex vertices cost total absolute curvature; the known
objects spend the minimum.

## Cheapest test

Count convex vertices on the 247 archived genus-2/3 realizations (exact, minutes) and on Szilassi: if the
realizations with the fewest convex vertices are the ones the ladder could extend furthest, the prior is supported;
then the c = 4 rank-3 instance for three types.

## Evidence from our own realizations (2026-11-03, NUMERICAL)

`code/vertex_types.py` (float vertex classification; controls: every convex-hull vertex is a convex corner, the
saddle count equals `gauss_gate.saddles` in the own gauge; both held on every record). Lower bounds: saddles
s >= 2g + 1, convex corners >= 4 (hull vertices).

| Objects | V | convex corners | concave corners | saddles | hull vertices |
|---|---|---|---|---|---|
| Szilassi, 20 ladder R1 realizations (g = 1) | 14 | 6 (all) | 0 | 8 | 4 |
| archive genus 2, 12 faces, 153 realizations | 28 | 6-13 (mostly 8-10) | 0-3 | 15-21 | 4-9 |
| archive genus 3, 12 faces, 94 realizations | 32 | 7-13 (mostly 7 or 10) | 0-2 | 18-24 | 4-9 |
| night-7 R5 realizations (g = 3, type 15) | 32 | 9-10 | 0 | 22-23 | 5-6 |
| Roest-Vigh, Mizhaev 8 faces (literature) | 24 | 4 | 0 | 20 | 4 |

None of our 255 realizations has c = 4; the minimum is 6 at genus 2 and 7 at genus 3, and the convex count does not
fall from genus 2 to 3. The saddle share rises with genus (57 %, ~64 %, ~69 %; the 8-face objects 83 %). Caveats:
our realizations come from parent-seeded engines and are far from face-neighbourly (48 of 66 adjacent pairs at
genus 3), so the c = 4 regularity of the two face-neighbourly 8-face objects is neither confirmed nor refuted for
face-neighbourly polyhedra. Consequence for E-261101-06: c = 4 stays the cheapest first sub-case (smallest instance,
readable UNSAT), but our data give it no extra prior; the PLAN should not call it the most likely case.

## Source

Primary reads 2026-11-01 (Roest-Vigh Theorem 1 item 3, Mizhaev face data, our exact re-check).

## 2026-11-10: the edge-level view (NUMERICAL, session computation, not in the repository)

The same three objects classified by edges (`reviews/HANDOFF_PROMPT_2026-11-10-wedges.md` §2): convex + reflex edges
are 16 + 5 (Szilassi), 20 + 16 (Roest-Vigh), 22 + 14 (Mizhaev); the vertex counts above are reproduced; every saddle
has mixed edge signs. The sharpest convex edges form disjoint face pairs, but a null model puts that near chance. The
follow-ups are separate files: I-261110-01 (wedge-plate ansatz), I-261110-07 (edge bits as a cube basis), and
E-261110-01, which recomputes all of this exactly from committed code.
