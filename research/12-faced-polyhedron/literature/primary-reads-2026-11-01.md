# Primary reads of 2026-11-01

Three sources read in their primary text in the strategy-review follow-up session (reader: an AI session; every
statement below is a paraphrase with a section pointer, not a quotation). Read levels in `README.md` were raised
accordingly. Files: the arXiv PDFs were fetched with curl and read via `pypdf`; the MDPI article was read as its HTML
full text in the built-in browser (figures not seen). Our labels follow `../SPEC.md` section 5.

## 1. Bokowski and Kevin H., Symmetry 17(4) 622 (2025), 58 pages

Authors: Juergen Bokowski (Fachbereich Mathematik, TU Darmstadt) and Kevin H. (independent researcher,
"CodeParade", Los Angeles). Dedicated to J. M. Wills.

What matters for us:

* **The face version is open in print.** Sec. 3: the second author's search of the dual cases found no additional
  embeddings. Sec. 8.3: no embedding of the 59 dual abstract polyhedra (12 eleven-gons, 44 vertices) was found with
  his methods; the best object is a Kepler-Poinsot-style model with two crossed polygons (their Figure 38). Sec. 9
  repeats that they have no neighbourly spatial polyhedron on 12 vertices and only the attempt at a dual embedding.
  No oriented-matroid claim is made for the face version anywhere. Status: CLAIMED (numerical, negative).
* **The "empty set" sentence is the vertex version.** Sec. 7.3 describes Bokowski and Guedes de Oliveira (2000): the
  12-vertex neighbourly oriented matroids not forbidden by edge-face intersections form the empty set after long
  computations. That is the vertex (Csaszar-type) problem, completed by Schewe (2010). This resolves the warning in
  `literature-review.md` Sec. 6: nothing there answers our question, and E-261101-15 is not a replication.
* **Their method (Sec. 4).** For dual (face) problems each search point is a plane; vertices are the triple points
  of the cubic map. Two stages: a large random search ranked by the number of edge-polygon intersections plus
  polygon self-crossings, then a refinement that also optimises aesthetics (edge-length ratios, near intersections,
  skinny polygons) and can truncate to small integer coordinates. A geometric symmetry is imposed by defining the
  other points of a permutation orbit relative to the first. They report that dual problems are slower and harder
  than triangular ones because plane placement is more sensitive. Runtimes: seconds for the smallest regular maps,
  about a day for the largest on a desktop. This is the engine behind the 1005 HackerPoet near-misses (FD11).
* **Their symmetry heuristic (Sec. 4).** Every embedding they found has a non-trivial geometric symmetry, and on
  non-embeddable examples an asymmetric search never beat a symmetric one; they conjecture that an embeddable
  regular map is embeddable with a symmetry. For us this is context, not evidence: their data are regular maps
  with large automorphism groups, while 39 of our 59 types have trivial automorphism group and FD5 excludes every
  symmetric S0 realization. If their heuristic transferred, it would predict non-existence (CONJECTURE).
* **Szilassi's embedding is essentially unique** (Sec. 8.2, citing Bokowski and Schewe, "On Szilassi's torus",
  Symmetry: Culture and Science 13 (2002) 211-240, oriented-matroid techniques). CLAIMED, source not read. If it
  means one realization class, the n = 7 realization space is a single thin component: the natural calibration for
  E-261101-17 and support for H-261101-09.
* Other pointers: a topological K12 embedding of highest symmetry (type 58) by Sequin and Xiao, 2004 ("K12 and the
  genus 6 Tiffany lamp"); all four realizations of the Moebius torus (Bokowski and Eggert 1991, vertex version);
  additional neighbourly pseudo-manifolds on 9, 10, 11 vertices (ABS 1994; Altshuler and Brehm 1992); their data
  at codeparade.net/embeddings (.obj files).

## 2. Roest and Vigh, arXiv:2609.32998 (26 September 2026), 7 pages

Authors: Gergely Roest and Viktor Vigh, Bolyai Institute, University of Szeged (e-mail addresses in the paper).

* **Object P.** 8 faces, 36 edges, 24 vertices, genus 3, equivelar {9,3}; planes A1: 3x - 4y - 2z = 5 and
  B1: -2x + 5y - 5z = 3 with their images under the three half-turns about the coordinate axes (group D2); all
  vertices rational; 20 pairs share one edge, 8 pairs two collinear edges; the A faces have three reflex corners,
  the B faces two. Symmetry group exactly D2 (Theorem 1, with a short proof), so P is chiral; combinatorial
  automorphism group dihedral of order 8, simply transitive on faces, all orientation-preserving, hence every
  realization of this map is chiral. Convex hull: the tetrahedron of four vertices at the ends of four long spikes.
  Already our positive control (`code/control_rost_vigh.py`, in `verify_all`).
* **Structural fact we had not noted.** 4 x 3 + 4 x 2 = 20 reflex corners, one per saddle, so P has exactly 20
  saddle vertices and **4 convex vertices, which are the 4 hull vertices**. Our gate reports 20 saddles for it
  (`TODO_world_research_2026.md`). The minimum number of convex vertices compatible with covering (FD7) is 4.
* **Verification protocol (Sec. 3).** Eight exact checks: general position; simplicity and reflex corners;
  closedness and orientability; vertex links; embedding as interval computations on each pair's line; orientation
  and volume; symmetries by enumerating orthogonal maps permuting the planes; automorphisms by the image of one
  directed edge. This is the same checklist as `ladder_exact.verify` plus `verify_candidate.py`.
* **Comparison with Mizhaev (Sec. 4).** Mizhaev's planes are listed; their "construction procedure" applied to his
  planes alone reproduces his polyhedron, i.e. the polyhedron is recovered from the arrangement (our solid-first /
  chamber selection, FD-level support for E-261101-16). Doubled pairs: two 4-cycles in P, one 8-cycle in M, so the
  two are not combinatorially equivalent (Proposition 2).
* **Method (Sec. 5).** Only a gist: a computational geometric search with significant resources, implemented in
  Python and run through a highly autonomous AI framework (Claude acknowledged), which also rediscovered Szilassi
  and Mizhaev; details deferred to a later paper. They state that the twelve-face case with every pair sharing
  exactly one edge remains open. Reference for the question: Arseneva et al., DCG 71 (2024).

## 3. Mizhaev, arXiv:2609.17700 (15 September 2026), 5 pages

* Integer realization: planes F1: 21x + 3y - 10z = -1440, F2: 21x + 3y + 10z = 1440, F3: 3x + z = 234,
  F4: 3x - z = -234, F5: 3y - z = 234, F6: 3y + z = -234, F7: 3x - 21y + 10z = -1440, F8: 3x - 21y - 10z = 1440;
  24 integer vertices (coordinates within [-300, 300]^2 x [-234, 234]) and 8 face walks (Tables 1-2);
  rotoreflection T(x, y, z) = (y, -x, -z), symmetry group C4 = combinatorial automorphism group; doubled pairs form
  one 8-cycle; earlier OSF preprint 2020 (doi 10.31219/osf.io/hvtey).
* **Our exact check (2026-11-01).** Planes and face walks transcribed into `mizhaev2026-planes.json` (links derived
  from the walks and the exact vertex-plane incidences); `code/ladder_exact.verify`: EMBEDDED, 28 pairs adjacent,
  20 single + 8 doubled, no non-simple face, no bad pair. Reflex corners per face F1..F8 = (2, 2, 3, 3, 3, 3, 2, 2),
  total 20, so **4 convex vertices** as for Roest-Vigh. Label: EXACT (session check, not yet in `verify_all`; adding
  `control_mizhaev.py` is a one-file task, see E-261101-12).
* His references worth a look for E-261101-22: Datta 2005 (k,k-equivelar polyhedral maps); McMullen, Schulz, Wills
  1982; Schulte and Wills 2012 (convex-faced combinatorially regular polyhedra of small genus, Symmetry 4).

## 4. What this changes in the project

1. The ambiguity in `literature-review.md` Sec. 6 is closed: the printed OM-level exclusion concerns the vertex
   version; our question is open in print (Bokowski-H. Sec. 8.3; Roest-Vigh Sec. 5). No ledger claim changes.
2. New structural prior (idea I-261101-20): both known face-neighbourly polyhedra beyond Szilassi have the minimum
   possible number of convex vertices (4), a tetrahedral hull and long spikes. Cheap tests: E-261101-06 with the
   number of convex vertices fixed to 4 (then <= 8) as the first sub-case; E-261101-16 catalogue weighted towards
   D2 / S4 arrangements with four far vertices.
3. Second positive control available (Mizhaev), data in this folder.
4. Contacts for E-261101-11: Roest and Vigh (Szeged, the institute of Szilassi), Bokowski (Darmstadt), Kevin H.
5. Leads: Bokowski-Schewe 2002 (uniqueness of Szilassi), Arseneva et al. 2024 (the question's source), Sequin-Xiao
   2004 (type-58 topological model), Schulte-Wills 2012; rows added to `README.md`.
