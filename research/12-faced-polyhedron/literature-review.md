# Literature review: the 12-face Szilassi-type problem (Track 1)

Date of review: 2026-10-29. Author: literature-researcher agent.

## 0. Access limits (read this first)

In this sandbox only GitHub raw files (`raw.githubusercontent.com`), PyPI and the GitHub code-search
tool were reachable. **arxiv.org, link.springer.com, sciencedirect.com, mdpi.com, doi.org,
tuprints.ulb.tu-darmstadt.de, page.math.tu-berlin.de, www.math.ucdavis.edu, vanderbilt.edu, researchgate and
Wikipedia were all blocked** (proxy 403 / DNS failure). Consequences:

* I did **not read any of the primary papers** (Bokowski-Pisanski, Schewe, ABS, Bokowski-Kevin H., Sulanke-Lutz,
  Ellingham-Stephens, Grünbaum-Szilassi). No theorem number or page below is from my own reading of those papers.
* Statements about the papers come from three kinds of secondary access, always labelled:
  **[WS]** = summary returned by the WebSearch tool (a model-generated digest of the page; abstracts are usually
  reliable, anything finer is not); **[3P-audit]** = the source-audit file `docs/SOURCES.md` of the third-party repo
  `pirozhkov-andrei/polyhedraproof`, which claims to have read the primary texts (it is itself AI-assisted and unreviewed);
  **[README]** = third-party repository READMEs.
* Everything labelled [3P-audit] must be re-checked against the primary source when network access to
  arxiv.org / mdpi.com / springer is allowed. Hosts that need to be allowed: `arxiv.org`, `www.mdpi.com`,
  `link.springer.com`, `page.math.tu-berlin.de` (or `www3.math.tu-berlin.de`), `math.vanderbilt.edu`.
* Status vocabulary: **proved** / **claimed** / **computational** / **conjectured**.

## 1. Data found (high priority item) — see also `literature/DATA_FOUND.md`

| What | Where (local) | Origin | Notes |
|---|---|---|---|
| The 59 triangulations, hex format `no.01..no.59` | `literature/HackerPoet-NeighborlyPolyhedra/topologies.txt` | https://raw.githubusercontent.com/HackerPoet/NeighborlyPolyhedra/main/topologies.txt, downloaded 2026-10-29, sha256 `cadaa7c7a386015d7aa659bdca677e303d05ff9481c5352046a1a7343f98e356` | 59 lines, 44 triples each. Third party (CodeParade). |
| The 59 triangulations, Lutz format `manifold_lex_d2_n12_o1_g6_#1..#59`, 1-indexed vertices | `literature/Hashirama1337s-szilassi-12/code/k12_g6_lutz.txt` | https://raw.githubusercontent.com/Hashirama1337s/szilassi-12/main/code/k12_g6_lutz.txt, downloaded 2026-10-29, sha256 `55912614618733476d07094ca4ed638df84ab58b42e8dba9eb81730da1a589b7` | Per [3P-audit] (pirozhkov) the file served by Lutz's Manifold Page has exactly this size (25,272 bytes) and this raw sha256, so this is byte-identical to Lutz's file *as reported by an independent third party*; I could not fetch Lutz's page myself. |
| Sage's `GenusSix()` (one triangulation) | `literature/sage-GenusSix/sage_simplicial_complex_examples.py.txt` (sha256 `8464cf90...115e5b`) | sagemath/sage `src/sage/topology/simplicial_complex_examples.py` | Docstring: "number 58 in the classification of Altshuler, Bokowski and Schuchert in [ABS96], where it is the unique surface with the largest symmetry group, of order 12." |
| `SurfOG06.scb` (GAP/simpcomp binary, one genus-6 surface) | `literature/passagemath-simpcomp-data/extracted/` | PyPI `passagemath-gap-pkg-simpcomp-data` 10.8.13, wheel sha256 `217c6cb4...ff4ed85` | Not the 59; wheel deleted after extraction; not otherwise used (format not decoded). |

**Verification I performed** (`literature/verify_59.py`, run as `python3 -I`; computational, exact combinatorics):
both lists have 59 entries; every entry has 44 triangles, 66 edges each in exactly 2 triangles, all 12 vertex links are single
11-cycles, and is orientable; the 59 canonical forms within each list are pairwise non-isomorphic; the **two lists are the same 59
isomorphism classes** (bijection printed by the script). Automorphism group orders (including reflections) are
39 of order 1, 9 of order 2, 1 of order 3, 7 of order 4, 2 of order 6, 1 of order 12. [3P-audit] says Ellingham-Stephens Theorem 4 gives
exactly "39 of order 1, 9 of order 2, 1 of order 3, 7 of order 4, 2 of order 6, 1 of order 12", so this matches.
Sage's GenusSix() is isomorphic to Lutz #54 = HackerPoet no.58.

**Numbering warning.** Three numberings exist and must not be mixed: Lutz #1..#59; HackerPoet `no.NN` (1-indexed in the file, his folders `topology_k` and
README use 0-indexing, so e.g. "topology 42 = Razorcross" is presumably `no.43`, which equals Lutz #58); ABS96's own numbering
(which I could not see). Only the order-12 map is pinned across them (Lutz #54 = HackerPoet no.58 = ABS #58 per Sage). The match of
HackerPoet's `no.NN` with ABS numbering for the other 58 maps is **not established**. Timmreck's introduction [WS] says Bokowski and
Guedes de Oliveira showed "number 54 on Altshuler's list" has no simplicial embedding; this coincides with the Lutz number of the order-12 map,
so that "54" is probably Lutz-style numbering or a coincidence. **Open interpretation question**, left to the PI.

## 2. Altshuler, Bokowski, Schuchert 1996

* A. Altshuler, J. Bokowski, P. Schuchert, "Neighborly 2-manifolds with 12 vertices", J. Combin. Theory Ser. A 75 (1996) 148-162,
  doi:10.1006/jcta.1996.0069. **Not read** (paywalled / blocked).
* **Claimed/computational (classification):** exactly 59 combinatorial types of orientable neighborly triangulations of the genus-6 surface
  with 12 vertices. The count is corroborated by: Sulanke-Lutz, Eur. J. Combin. 30 (2009), Table 4, p. 9 ([3P-audit], arXiv:math/0610022v3);
  Ellingham-Stephens, J. Combin. Des. 13 (2005) 336-344, whose Section 6 re-generated the orientable embeddings and "confirm[s]" ABS
  ([3P-audit], preprint a10.pdf); [WS] on Lutz's enumeration paper ("59 neighborly triangulations"); and my own check that the Lutz file holds 59 pairwise non-isomorphic
  valid triangulations (this shows >= 59 distinct classes in the file, not completeness).
* [3P-audit] states that "the enumeration data [of ABS] were not recovered" by them either.
* Per [README] of HackerPoet: "The paper about 'Neighborly 2-Manifolds' has a table of automorphism groups for the dual graph problem." I cannot confirm.
* Implication: the combinatorial question (model section 1.3) is settled by two independent enumerations (ABS 1996 and Ellingham-Stephens 2003/05,
  plus Sulanke-Lutz 2009) as far as the secondary reports go. We now have the data.

## 3. Bokowski and Pisanski 2007

* J. Bokowski, T. Pisanski, "Oriented matroids and complete-graph embeddings on surfaces", J. Combin. Theory Ser. A 114 (2007) 1-19,
  doi:10.1016/j.jcta.2006.06.012 (dedicated to Ringel). Full text **not read**; only the abstract [WS].
* **Proved (abstract, as relayed):** a function maps simple pseudoline arrangements with an even number of elements to pairs of
  complete-graph embeddings on a surface (the oriented matroid survives in each member); "triangular" arrangements (cells 2-colourable,
  one colour class all triangles) give triangular complete-graph embeddings, so Ringel's results on triangular complete-graph embeddings can be read
  as results on curve arrangements; 2-colourable curve arrangements relate to Petrie dual maps; an orientable surface of genus g admits a complete curve
  arrangement with at most 2g+1 curves (unbounded for non-orientable).
* **What it does not appear to be:** a paper about *polyhedral (geometric) realizability* of the 59 maps or of their duals. The abstract is about *topological* embeddings of K_n and
  oriented matroids of rank 3 (pseudolines). I found **no indication** that it excludes any of the 59 dual face-realizations; your question 1 premise
  ("which of the 59 are excluded") is probably misattributed. Exact theorem statements and page numbers: **not obtainable here**. Needs primary reading.
* Misattribution risk: one WebSearch digest called a "2010 Bokowski-Pisanski DCG paper" the source of the non-embeddability of genus 6; that is a garbling of Schewe 2010 / Bokowski-Guedes de Oliveira 2000.

## 4. Bokowski and Guedes de Oliveira 2000 (the prior vertex-version result)

* J. Bokowski, A. Guedes de Oliveira, "On the generation of oriented matroids", Discrete Comput. Geom. 24 (2000) 197-208, doi:10.1007/s004540010027
  (a copy was indexed at math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Bokowski/10027.pdf, blocked here).
* **Computational/proved (abstract via [WS]):** disproves Grünbaum's conjecture that every closed triangulated orientable 2-manifold embeds geometrically
  (polyhedrally) in R^3; an infinite class of non-embeddable triangulations for each genus g >= 6; the special 12-vertex genus-6 triangulation has no compatible oriented matroid, i.e. is not realizable.
  This is the **vertex** version.

## 5. Schewe 2010 and thesis

* L. Schewe, "Nonrealizable minimal vertex triangulations of surfaces: showing nonrealizability using oriented matroids and satisfiability solvers",
  Discrete Comput. Geom. 43 (2010) 289-302, doi:10.1007/s00454-009-9222-y; arXiv:0801.2582. **Not read directly.**
* **Computational/proved:** Theorem 1.1 (as relayed [WS], [3P-audit]): no minimal vertex triangulation of a closed connected orientable 2-manifold of genus 6 (12 vertices, all 59 types) admits a polyhedral embedding in R^3;
  there are genus-5 examples of non-realizable vertex-minimal triangulations (3 examples [WS]); an infinite family of non-realizable triangulations; this "corrects an earlier error" in the literature [WS].
  Proposition 1.2 ([3P-audit]): concerns *acyclic uniform rank-4 oriented matroids admissible for each triangulation*, not arbitrary oriented matroids on 12 labels. Section 2 (printed p. 6, [3P-audit]) defines admissibility by excluding circuits whose positive and negative supports lie in disjoint simplices; in uniform rank 4 it suffices to exclude intersections between a triangle and a disjoint edge.
* **Encoding** (variables, Grassmann-Plücker clauses, embedding clauses): not obtainable from my sources beyond the above. The 12 points are the elements of a rank-4 chirotope; embedding predicates involve 5 elements (triangle vs disjoint edge). Third-party reproduction: Hashirama1337s reports (README, sec. 4) reproducing "all 59 vertex versions UNSAT, about 4 minutes each" (`results/logs/sat_schewe.log`; not independently checked by me).
* **Dual (face) problem:** [3P-audit] and the pirozhkov README both say Theorem 1.1 settles only the 12-*vertex* problem and "duality does not carry that answer over to faces". I found no remark in Schewe on the 12-face problem; **but I could not search the full text** (a WebSearch for it returned nothing). Needs primary reading of the outlook section.
* Thesis: L. Schewe, "Satisfiability problems in discrete geometry", TU Darmstadt, 2007 (advisors Bokowski, Grünbaum per Mathematics Genealogy [WS]). Not found online by me; no full text read.
* Related (pointers, not read): Timmreck, "Necessary conditions for geometric realizability of simplicial complexes", arXiv:0705.1912 (linking-number conditions; its introduction mentions the 59 maps and one non-embeddable one [WS]); "Non-existence of polyhedral immersions of triangulated surfaces in R^3", arXiv:1606.04848; "Polyhedral embeddings and immersions of many triangulated 2-manifolds with few vertices", arXiv:1603.04877. All concern vertex-type (triangulation) realizability.

## 6. Bokowski and Kevin H. (CodeParade), Symmetry 17(4) (2025) 622 — the key published statement on the *face* version

* J. Bokowski, Kevin H., "Polyhedral Embeddings of Triangular Regular Maps of Genus g, 2 <= g <= 14, and Neighborly Spatial Polyhedra", Symmetry 17(4), 622,
  doi:10.3390/sym17040622 (open access at mdpi.com; **blocked here**; preprint https://www.preprints.org/manuscript/202502.1872/v1; TU Darmstadt tuprints record).
  The coordinator's message names the second author "Hay"; the [3P-audit] says the printed name is **"Kevin H."**, affiliation CodeParade (= HackerPoet, author of the NeighborlyPolyhedra repo). I could not verify the spelling.
* What I can report (all second-hand):
  * Abstract [WS]: an old conjecture of Grünbaum (1967, disproved 2000) motivates the investigation; symmetrical polyhedral embeddings of all triangular regular maps of genus g (2<=g<=14) exist except one undecided case in genus 13; ten new embeddings were found by a numerical optimisation method (credited to the second author); Szilassi's torus is treated as dual of Möbius' torus; the method was "first tried, unsuccessfully, on a dual of one of the 59 closed oriented surfaces whose edge graph is K12".
  * Sec. 4 (numerical method), Sec. 8.3 (pp. 25-26) and Figure 38 [3P-audit]: Sec. 8.3 "reports no embeddings found among the 59 dual types and illustrates an intersecting model", "an adjacent numerical-search result, not a nonexistence proof". It "includes twelve planes carrying 44 vertices". A WebSearch digest [WS] adds: a subsection "The 59 Examples of the Complete Graph with 12 Vertices"; the dual problem "uses nearly the same algorithm" but is "generally slower and harder ... placement of the planes is more sensitive than the vertex positions"; "the investigation of the second author to study the dual cases, which have been investigated by Bokowski, Guedes de Oliveira, and Schewe, did not find additional embeddings"; and a sentence that "the set of possible 12 vertex neighborly oriented matroids that are not forbidden because of edge-face intersections turned out (after long computations) to be the empty set". **That last sentence is ambiguous: it most likely refers to the vertex version (Schewe), not to a face-plane computation. Do not cite it for the face version without reading the paper.**
  * Hashirama1337s README [README] (secondary, unreviewed): Sec. 4 of the paper says every embedding they found had a non-trivial symmetry, and they conjecture an embeddable regular map is also embeddable with a symmetry; the paper's only computer attempt at the face version is numerical.
  * Objective function: [README] of Hashirama says Bokowski-H. minimised "edge-face hits plus face self-crossings"; HackerPoet's repository counts "crossings" (self-intersections of faces) and "intersections" (edge-face hits). Parameterisation: 12 planes (36 reals), from his code `solver.cpp` (not read; planes with symmetry options `make_symmetric_o4/o2/d2`).
  * Data offered: not known. HackerPoet's repo (below) is the data source.
* Status: **computational/heuristic** (numerical search); no certificate of non-existence; **conjectured**: symmetry of embeddings.

### 6.1 HackerPoet/NeighborlyPolyhedra (code + models; unreviewed, untrusted)

* https://github.com/HackerPoet/NeighborlyPolyhedra (README downloaded; stored in `literature/HackerPoet-NeighborlyPolyhedra/`; code not run).
* **Claimed (author's words):** no shape that is "completely intersection-free" was found; the "Razorcross" (topology 42, 0-indexed) is a near miss: either 0 crossings with 4 edge-face intersections, or 4 crossings (self-intersecting faces) with 0 intersections. Similar
  near-misses: topology 6 (0 crossings/8 intersections; or 10/0), 37 (0/8; 4/0), 49 (0/8; 8/0), 55 (0/16; 10/0), 58 (0/10; 4/0). "There is no rigorous proof about the optimality."
* Highly symmetric shapes tend to have the fewest intersections (order-2/order-4 symmetry options).
* Dual (vertex) problem: his `Dual44` has 4 intersections (manifold 44); he notes the vertex version is already impossible by Schewe.
* Importance: these near misses show the *landscape*: minimal violation counts of 4 (not 1), 12 planes.

## 7. Post-2025 computational / SAT work on exactly our problem (third-party, unreviewed, AI-assisted)

### 7.1 Hashirama1337s/szilassi-12 ("Moki & Julio (AI-assisted), 2026"; Zenodo 10.5281/zenodo.23003257)
* Local copy: `literature/Hashirama1337s-szilassi-12/` (README, Lutz data, `omsat.py`, `autos.py`, `automorphisms.json`, `certificates.csv`; none executed).
* **Claimed theorem (computer-assisted, DRAT-certified):** "No polyhedron with 12 faces in which every two faces share an edge has a non-trivial symmetry" (isometry group trivial). Proof: reduce to 25 (map, cyclic group) cases (21 half-turn classes in 19 maps, 4 three-fold cases #3, #45, #48, #54 in Lutz numbering), plus larger groups; 36 SAT instances, all UNSAT, DRAT proofs checked by drat-trim (about 8.4 GB, regenerated on demand), certificates table with CNF sha256.
* **Encoding** (their sec. 3, same as our model sec. 4): 12 planes + plane at infinity, uniform rank-4 chirotope on 13 elements (715 signs), 3-term Grassmann-Plücker clauses (only necessity used); order along line and "point strictly inside edge" via 4-bracket products; (S) faces simple, (X) no edge meets a face it does not belong to; "point inside face" by parity of crossings along a ray; symmetric instances add chi(gB) = det(g) chi(B). A second, independently derived encoding agrees where it finished (half-turn runs unfinished).
  Extra **orientation encoding**: one winding bit W_k per face; a corner is reflex iff its local turn disagrees with W_k; and **at most one reflex corner meets at any polyhedron vertex** (two reflex corners at a degree-3 vertex would make those faces overlap along their common line). Gave 2.7x (3-fold) to 10x (half-turn) speed-ups.
* **Not resolved:** asymmetric realisations ("None was resolved": #1 and #54 ran 5 h + 4 h; others 10 min); estimate "several orders of magnitude beyond one PC". Numerical GPU search: no realisation; symmetric minima as low as 4 violations; unrestricted plateau at 21-24 violations (their count).
* Controls: 7-face (Szilassi) instance SAT; Csaszar instance SAT; Schewe reproduced (59 UNSAT, ~4 min each).
* Status: **claimed**, unreviewed. The README also states Grünbaum-Szilassi's and Bokowski-H.'s results as background. The symmetry theorem does **not** settle existence ("the 59 maps are not regular"; 39 maps have trivial automorphism group).

### 7.2 pirozhkov-andrei/polyhedraproof ("Twelve pairwise adjacent faces", Zenodo 10.5281/zenodo.23434449)
* README and docs `SOURCES.md`, `THEORY_MAP.md` read (raw GitHub); not stored locally (can be re-fetched).
* **Claimed:** under hypotheses (H1)-(H3) (closed embedded polygonal-cell surface, maximal planar faces), such a polyhedron exists only if one of **59 Boolean formulas** is satisfiable, each with **5,257 variables and 52,177 clauses**; layers S, H, A (chirotope axioms in 3-term form), B (non-adjacent edges of a face do not cross), I (face orientation by crossing parity; at most one reflex corner per vertex, Lemma 2.6), plus 13 gauge clauses. Cube-and-conquer with CaDiCaL proofs checked by cake_lpr.
* **Status:** "The computation over the 59 formulas has not been carried out, so the question remains open and no nonexistence result is claimed." Pilot (rehearsal): maps 1 and 2 refuted (their matrix numbering), 31,187 leaves, 648.5 core-hours; full campaign estimated about **19,000 core-hours** (order of magnitude); asks for collaborators.
* [3P-audit] on Grünbaum-Szilassi 2009: the paper "does not contain the residue condition n = 0,3,4,7 (mod 12) or a statement that the twelve-face problem is open, although secondary sources cite it for both". Also: Arseneva et al. (DCG 71(4) 2024, pp. 1429-1455) Sec. 2, p. 1435 asks which complete graphs arise as adjacency graphs of closed polyhedral surfaces; that is the "open question" source.
* Also lists: Szilassi, "Regular toroids", Structural Topology 13 (1986) 69-80, Sec. 4 pp. 75-76 (7 hexagonal faces, 21 edges, 14 vertices, every pair adjacent), accessible at iri.upc.edu (blocked here).

### 7.3 Others (names only; not read, treat as noise)
* 0LuminaX0/GEODE (EGNN gradient-descent attempt for K12, README only seen); spicylemonade/holyhedron (an LLM "planner" literature file, unrelated mostly); arXiv:2609.32998 "A second eight-faced polyhedron in which every two faces share an edge" (title from a WebSearch digest; digest says its authors state the F=12 case remains open; not verified; note an 8-face pairwise-adjacent polyhedron needs not satisfy "exactly one shared edge").

## 8. Mizhaev, arXiv:2609.17700 (linked from the repository README)

* R. Mizhaev, "Integer Realization of an Equivelar Octahedron of Genus 3" (Sept. 2026). Only the abstract/introduction seen via [WS]; not read.
* **Constructed (exact integer coordinates, verified exactly by the author):** closed orientable genus-3 surface with 8 flat nonagonal faces, 24 vertices, 36 edges (the press figure of 26 edges is wrong: 24-36+8 = -4), three faces per vertex, C4 symmetry; it is "variant V2" of the author's earlier construction [11], published as a coordinate certificate.
* **Key difference from our problem:** "every pair of faces shares an edge, with 20 pairs sharing one edge and 8 pairs sharing two" (28 pairs in total). So it is **not** a pairwise-exactly-one-edge polyhedron; it is an equivelar {9,3} map with an 8-face "neighbourly with multiplicities" structure. The dual map is a 8-vertex genus-3 triangulation with double edges, not a simplicial complex.
* Method: from the abstract it is a construction of a specific incidence structure and certification by exact arithmetic; no evidence of a general method (SAT or numerical). I see no way it generalises to F=12 where the dual must be a simplicial neighborly triangulation. Exact method unknown without the full text.

## 9. Other related literature (pointers; not read)

* Hougardy, Lutz, Zelke: "Polyhedra of genus 2 with 10 vertices and minimal coordinates" (arXiv math/0507592), "Polyhedra of genus 3 with 10 vertices and minimal coordinates" (arXiv math/0604017; 17 of the 20 triangulations have general-position realisations in the 5x5x5 cube), "Surface realization with the intersection edge functional" (arXiv math/0608538), "Polyhedral tori with minimal coordinates" (arXiv 0709.2794) [WS]. These are **vertex-version** realisations; the objective is the total length of triangle-triangle intersection segments, minimised by a random local search. No K12 attempt found [WS].
* Bokowski, "On heuristic methods for finding realizations of surfaces", in Discrete Differential Geometry, Oberwolfach Seminars 38 (2008): abstract only [WS]: heuristic realisation of oriented matroids of rank 3 and 4 for spatial embeddability of 2-manifolds. Content on the dual not seen.
* Ziegler, "Polyhedral surfaces of high genus", arXiv math/0412093: geometric genus problem for n vertices (McMullen-Schulz-Wills record g ~ n log n); Schmitt's "Ten Problems in Geometry" says Guedes de Oliveira and Schewe showed none of the 59 types (12 vertices, 66 edges, genus 6) is realizable without self-intersection [WS] (vertex version).
* Brehm 1983 (non-realizable Moebius strip); Bokowski-Eggert 1991 (Moebius torus, all realisations); Szilassi 1986; Grünbaum-Szilassi 2009 (Contributions to Discrete Math 4(1) 21-39): not read here.
* Arseneva et al., "Adjacency graphs of polyhedral surfaces", DCG 71 (2024), arXiv:2103.09803: [WS] abstract: every graph is the adjacency graph of a polyhedral surface with arbitrary polygonal cells, but with *convex* cells K_5 (and K_{5,81}, non-planar 3-trees) are not realisable. [3P-audit]: its model differs from ours (full side or corner contacts; no distinct-plane requirement). Convex cells are therefore excluded in a different setting; our faces are non-convex.
* Sage/GAP: `simplicial_complexes.GenusSix()`; simpcomp data package has only vertex-transitive 2-manifolds and `SurfOG06`, not the 59.
* Wikipedia "Szilassi polyhedron" (pointer only) states the 12-face case as open.

## 10. Known necessary conditions / partial results for planar-faced duals (question 5)

* Nothing found in the literature (within my reach) that gives a nonexistence result for the face version other than the claimed symmetric result in 7.1.
* Facts that do hold (derive from the model; not from literature): E = C(F,2), genus (F-3)(F-4)/12 (the [3P-audit] says Grünbaum-Szilassi does *not* contain this; the pirozhkov article proves it as Prop. 2.5; our `mathematical-model.md` 1.1 proves it too).
* Convexity: for 7 faces, Szilassi's torus has exactly one convex face; the Hashirama repo proves (claimed, SAT/DRAT) that every 7-hexagon torus without overarching faces has exactly one convex face, confirming Grünbaum-Szilassi Conjecture 5.7 in that case. Not proved in the 12-face case.
* Steinitz-type theorems for higher genus: none known to me; realizability of cubic maps of genus >= 1 with planar faces is not characterised (Bokowski's chapters use oriented matroid enumeration + heuristics only).

## 11. Implications for our approach

1. **Data in hand, cross-checked.** We can use `topologies.txt` or the Lutz file for Track 2/4. The 59 classes agree between two files; automorphism-order distribution agrees with Ellingham-Stephens (as relayed). Record the numbering used in every log.
2. **Our SAT reduction (model sec. 4) is exactly the one two independent third parties already implemented.** Hashirama1337s did it symmetric (36 UNSAT instances, DRAT) and found asymmetric instances too hard for 4-5 hour runs; pirozhkov has a cube-and-conquer pipeline and estimates about 19,000 core-hours. So our Track 2 should not hope for a quick global SAT refutation; value is in (a) independent verification of their encodings, (b) stronger clauses.
3. **Add the "at most one reflex corner per vertex" lemma and an orientation bit per face** (both papers; geometric Lemma 2.6 of pirozhkov: two reflex corners at a degree-3 vertex make faces overlap along their common line). Our current model sec. 4 does not state it. It sped Hashirama's solver 2.7x-10x. Needs an adversarial proof check from us.
4. **Add layer B-type clauses** (non-adjacent edges of the same face do not cross) — already implied by our "(face simple)" predicate but encode directly.
5. **Symmetric cases are probably dead** (claimed UNSAT) and the numerical evidence is that every low-violation configuration is symmetric (Bokowski-H. conjecture; HackerPoet near misses). If correct, a hypothetical realisation would be asymmetric on 39 maps or asymmetric on the 20 symmetric ones, a much larger search space. Numerically one should therefore search *without* imposing symmetry, from non-symmetric seeds.
6. **Numerical baselines to beat:** best known violation counts: 4 edge-face intersections with 0 face self-crossings, or 0 intersections with 4 face self-crossings (Razorcross = HackerPoet topology 42), Hashirama: 4 for symmetric, 21-24 for unrestricted GPU search (different counting). A configuration with 0/0 would be a counterexample to all the above.
7. **Validation controls:** Szilassi 7-face instance must be SAT; Csaszar vertex instance SAT; Schewe: the 59 vertex instances UNSAT (~4 min each).
8. The *rational/integer certificate* argument (open realisation space) in model sec. 2 is consistent with Mizhaev's "integer coordinate certificate" style.
9. **Primary-source reading is still needed** for: Bokowski-Pisanski (likely irrelevant), Schewe sec. 2 encoding, Bokowski-Kevin H. secs. 4 and 8.3, ABS tables. Ask for `arxiv.org`, `mdpi.com`, `link.springer.com` to be allowed.

## 12. Misleading analogies

* **Schewe / Bokowski-Guedes de Oliveira are about the vertex version** (12 free points; the 44 triangles are planar automatically and must be pairwise non-crossing). Face-plane duals are a different realisation space (planar faces by construction; polarity does not preserve embeddedness). Do not cite them as evidence for or against the face version.
* **"No symmetric polyhedron" (Hashirama) is not "no polyhedron".** Unreviewed and AI-assisted; also uses a particular encoding for which only necessity is claimed.
* **Numerical failure (Bokowski-Kevin H., HackerPoet, Hashirama GPU search) is not a proof**; the authors say so.
* **Mizhaev's octahedron** has pairs sharing two edges (8 of 28 pairs): not a pairwise-one-edge object; its existence says nothing about F=12.
* **Arseneva et al.'s K_5 nonrealizability** is for *convex* cells; our faces are non-convex 11-gons.
* **The Grünbaum-Szilassi 2009 paper** is often cited for "the 12-face problem is open" and for the residue condition; [3P-audit] says it states neither. Cite Arseneva et al. 2024 Sec. 2 / Bokowski-Kevin H. 2025 Sec. 8.3 instead, after verifying.
* **Bokowski-Pisanski 2007** concerns topological complete-graph embeddings via pseudolines, not polyhedral realisation.
* **Numbering of the 59 maps** (see sec. 1) differs between Lutz, ABS, HackerPoet (0/1-indexed) and third-party matrix numbering (pirozhkov "this project's"). "Map #54" means different things.
* **Neighbouring dimension count:** the 12 vertices of the vertex version are 36 reals (12 points) just as the 12 planes of the face version; but the face version has degree-3 vertices computed as plane triple points, whose positions are far more sensitive (Bokowski-Kevin H. [WS]).
