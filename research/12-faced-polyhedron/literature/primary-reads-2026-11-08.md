# Primary reads of 2026-11-08 (ROADMAP item 2)

Question: is a maximal face-neighbourly polyhedron of type (F, g) = (8, 2), (9, 3), (10, 4) published, claimed, or
excluded in print? Sources: Altshuler-Brehm 1986 and 1992, Altshuler-Bokowski-Schuchert 1994, Bokowski-Schewe
2002. Reader: an AI session (web only, no downloads kept in `literature/`). Labels follow `../SPEC.md` section 5; a
source's own claim is CLAIMED until reproduced. **Short result: none of the four originals could be obtained in full
text; none decides or constrains (8, 2), (9, 3) or (10, 4). The 1986 genus-2 theorem does not apply to (8, 2),
because it is about polyhedral maps, which by the standard definition have no multiple edges, while every (8, 2)
object has a pair of faces sharing two edges.**

Not run: no full-text read of any of the four papers; no check of the proofs; no search of MathSciNet or zbMATH
beyond the open mirrors listed. Publisher PDFs (ScienceDirect, Springer) returned 403 or a login redirect;
third-party mirrors of the paywalled PDFs (typeset.io / scispace) were not used.

## 0. Definitions fixed from open primary text (used in all sections below)

Source A: U. Brehm, E. Schulte, *Polyhedral maps*, Chapter 20 of *Handbook of Discrete and Computational Geometry*,
3rd ed., CRC Press 2017, pp. 533-548. Full text read (hosted by the editors,
https://csun.edu/~ctoth/Handbook/chap20.pdf; text extracted from the PDF, figures not seen). Read level: full for
Sections 20.1-20.2.
* Glossary, p. 535: "Map on a surface: an embedded finite graph M (without loops or multiple edges) on a compact
  2-manifold S such that [the faces are] closed 2-cells, and each vertex has valency at least 3."
* Same page: "Polyhedral map: a map M on S such that the intersection of any two distinct faces is either empty, a
  common vertex, or a common edge."
* Section 20.2: the unique polyhedral map with 40 edges on the genus-5 orientable surface "is weakly neighborly and
  self-dual" (Theorem 20.2.3 / Brehm 1990 bound on f1 is for polyhedral maps). Section 20.1: "For each g >= 6 there
  are examples of simplicial polyhedral maps that cannot be embedded in R^3 [BO00]"; "Very little is known about
  polyhedral embeddings of orientable polyhedral maps of positive genus."
* Status: CLAIMED (a source statement). It is the Brehm school's definition, the school of Altshuler-Brehm.

Source B: N. Nilakantan, *Nonexistence of a weakly neighbourly polyhedral map of type {6,6}*, Experimental
Mathematics 12(3) (2003) 257-260 (Project Euclid, open; read in full). Intro, p. 257-258:
* "A polyhedral 2-manifold is called a polyhedral map if the intersection of any two faces is empty, a vertex, or an
  edge." Its complexes require "any two cycles have at most one common edge".
* "A polyhedral map is called a weakly neighbourly polyhedral map (wnp map) if any pair of vertices is in a face."
  Counting: d(K) + f1(K) <= C(n,2) for a polyhedral map with n vertices and d diagonals, equality iff wnp. This
  pair count is a polyhedral-map property (a diagonal lies in a unique face); it does not hold when two cells can
  meet in two edges.
* Status: CLAIMED, secondary for the 1986 paper (a later author restating the school's definitions).

So: in this literature "polyhedral map" = no loops, no multiple edges, two faces meet in at most one vertex or one
edge. "Weakly neighbourly" = every two vertices lie on a common face (any face sizes), which is the **vertex**
version; "neighborly" in Altshuler-Brehm 1992 and Lutz = every two vertices joined by an edge (1-skeleton K_n) in a
triangulation, i.e. the same vertex version with simplicial cells. No source here uses the face-sharing-an-edge
condition for a polyhedral surface.

## 1. Altshuler, Brehm, JCTA 42 (1986) 87-103 (genus 2)

Citation: A. Altshuler, U. Brehm, *Nonexistence of weakly neighborly polyhedral maps on the orientable 2-manifold of
genus 2*, J. Combin. Theory Ser. A 42 (1986) 87-103, doi:10.1016/0097-3165(86)90008-7 (pii 0097316586900087;
Semantic Scholar marks a bronze OA link, but ScienceDirect returned 403 to the fetch tool).
* **Obtained:** abstract and a zbMATH review text (via the MaRDI portal record
  https://portal.mardi4nfdi.de/wiki/Item:Q1070581, zbMATH 0585.57004). Full text: **not obtainable** here.
  Read level: **abstract / review only** (secondary).
* Statement (abstract, via BGU CRIS record, MaRDI, and search snippets): a weakly neighborly polyhedral map is "a
  2-dimensional cell-complex which decomposes a closed 2-manifold without boundary, such that for every two
  vertices there is a 2-cell containing them"; the theorem: there is no such map on the orientable surface of
  genus 2; genus 2 seems to be unique in this property. The zbMATH review (as relayed by MaRDI, not re-checked)
  adds: the cells are n-gons for any n >= 3; every cell decomposition of that surface needs at least 10 vertices;
  weak neighborliness gives an upper bound of 12 vertices; the authors "examine every possible p-vector" for a
  hypothetical map and reach a contradiction in each case. Companion 1986 papers cited by later authors: Brehm-
  Altshuler, Israel J. Math. 53 (1986) 137-157 (arbitrary genus); weakly neighborly maps on the torus (five, three
  geometrically realizable) and with chi = -1, -2.
* Definition question (does "polyhedral map" allow two cells sharing 2 edges?): **not read in the paper itself.**
  The Brehm-school definition (Sources A, B) forbids it, and the 10-vertex lower bound quoted by the review is a
  statement about decompositions that are polyhedral maps. CLAIMED.
* **Does it decide (8, 2)?** No, by the following argument.
  1. (8, 2): V = 20, E = 3(F + 2g - 2) = 30, and there are C(8,2) = 28 face pairs. Each edge borders two distinct
     faces, so the shared-edge counts of the 28 pairs sum to 30 and each is >= 1: some pair shares >= 2 edges
     (at a cubic vertex the three edges separate three different face pairs, so two edges shared by one pair are
     disjoint). PROVED-1 (elementary, AI-checked; same arithmetic as `review-2026-11-03.md` note 4).
  2. Hence the primal P is not a polyhedral map (two faces meet in two edges), and its dual P* (8 vertices, 30
     edges, 20 triangles) has a multiple edge, so P* is not a "map" in the sense of Source A. Also P* has 8 < 10
     vertices, below the 10-vertex minimum the review attributes to genus 2. PROVED-1 given the definitions of
     Sources A, B; the dependence on the 1986 paper's own definition is CLAIMED.
  3. The theorem is therefore silent on P*. It does not say that K8 with two doubled pairs cannot sit on genus 2; the
     proof (a case analysis over p-vectors, with the pair count of Source B) uses polyhedrality, so there is no
     reason to expect it to extend. Whether the primal combinatorial (8, 2) maps exist is the project's own
     enumeration, not a literature fact.
* (9, 3), (10, 4): genus 3 and 4, so the genus-2 theorem is irrelevant. The arbitrary-genus paper (Israel J. Math. 53)
  constructs wnp maps, again polyhedral maps without multiple edges.
* **Trap (misleading analogy):** "weakly neighborly polyhedral map" is a vertex statement; the dual statement for the
  primal P is "every two faces of P meet in a vertex", weaker than our "share an edge", and only for polyhedral maps.
* Label: CLAIMED (abstract-level); the inapplicability argument above PROVED-1 modulo the definition in the paper.

## 2. Altshuler, Brehm, DCG 8 (1992) 93-104

Citation: A. Altshuler, U. Brehm, *Neighborly maps with few vertices*, Discrete Comput. Geom. 8 (1992) 93-104.
EuDML https://eudml.org/doc/131211 lists the full text at the Goettingen GDZ (PPN GDZPPN000365408) but
misattributes the author as "T. L. Snyder" (metadata error; keywords "triangulations of closed surfaces, less than 12
vertices, neighborly"). Zbl 0756.52014.
* **Obtained:** abstract and an intro excerpt via search snippets only; the GDZ page is a viewer without a direct PDF
  link and the Springer page needs a login. Read level: **abstract** (secondary).
* Statement (abstract): "We find and describe all the neighborly maps with Euler characteristic chi > -10 (i.e.,
  genus g < 6, if orientable) or, equivalently, all the neighborly maps with V < 12 vertices." Intro excerpt (not
  checked against the PDF): two neighborly maps with 9 vertices (chi = -3) and 14 with 10 vertices (chi = -5), all
  nonorientable; orientable neighborly maps need V = 0, 3, 4, 7 mod 12.
* Definition: triangulations of closed 2-manifolds, neighborly = every two vertices joined by an edge (1-skeleton
  K_V); Lutz (arXiv:math/0506316, read) uses the same wording ("triangulations that have as 1-skeleton the complete
  graph K_n"). A simplicial complex has no multiple edges; our dual maps for (9, 3), (10, 4) have 39 and 48 edges, not
  36 and 45, so they are not in this list.
* **Does it decide (8,2), (9,3), (10,4)?** No. Neighborly orientable triangulations with V < 12 are only the
  tetrahedron (V = 4) and the 7-vertex torus, by the V mod 12 rule, consistent with the abstract. Our duals have V =
  8, 9, 10 and doubled edges, so they are outside the census. This confirms `review-2026-11-03.md` note 2.
* Label: CLAIMED; absence of a census with multiple edges stands (not a proof that none exists).

## 3. Altshuler, Bokowski, Schuchert, Israel J. Math. (1994) and the 10-vertex paper

Citations (checked against Bokowski's bibliography page, https://www.mi.sanu.ac.rs/vismath/visbook/bokowsky/index.html,
and MaRDI):
* A. Altshuler, J. Bokowski, P. Schuchert, *Spatial polyhedra without diagonals*, Israel J. Math. **88** (1994)
  373-396, doi:10.1007/BF02773687, zbMATH 0799.52011. **`README.md` row `abs1994` says volume 86; the volume is 88.**
* Same authors, *Sphere systems and neighborly spatial polyhedra with 10 vertices*, Proc. First Int. Conf. on
  Stochastic Geometry, Convex Bodies and Empirical Measures (Palermo 1993), Rend. Circ. Mat. Palermo (2) Suppl. 35
  (1994) (Bokowski gives Suppl. No. 35; `README.md` says "Suppl. II 2"; unchecked).
* **Obtained:** the zbMATH review (G. M. Ziegler) via https://portal.mardi4nfdi.de/wiki/Item:Q1327516; the 10-vertex
  paper: bibliographic record only. Read level: **review / abstract**.
* Statement (review): the paper studies neighborly simplicial 2-manifolds with 9 vertices, which correspond to
  Mendelsohn triple systems; "all five combinatorial types have straight realizations in R^3"; some topological
  types of embeddings in R^3 are not isotopic to straight realizations; methods: oriented-matroid realizability
  algorithms, final polynomials for non-realizability.
* Reading (CLAIMED): K9 with every pair joined by one directed triple means 36 edges and 24 triangles; per the 2025
  survey (Bokowski-Kevin H., Sec. 7.4, quoted in `review-2026-11-03.md`) these are orientable neighbourly
  2-pseudomanifolds (several circles at a vertex), not closed surfaces. A closed genus-3 surface with 9 vertices and
  K9 would need chi = 9 - 36 + 24 = -3 (odd, not orientable). Our (9, 3) dual has 39 edges and 26 triangles (chi =
  -4). It is a different object. These are VERTEX-version results; duality does not carry embeddedness (Roest-Vigh).
* **Does it decide (8,2), (9,3), (10,4)?** No. Not a seed, not an exclusion. Confirms `review-2026-11-03.md` note 3.
  Mismatch to resolve: the zbMATH review says "simplicial 2-manifolds", the 2025 survey says pseudomanifolds. Only
  the full text can settle which.
* Label: CLAIMED.

## 4. Bokowski, Schewe, "On Szilassi's torus", Symmetry: Culture and Science 13(3-4) (2002) 231-240

* **Obtained:** bibliographic record only (issue page https://journal-scs.symmetry.hu/content-pages/volume-13-numbers-3-4-pages-225-448-2002/:
  pp. 231-240, no abstract, no PDF). Read level: **not read** (citation record).
* What others say it proves, with two different wordings:
  * Bokowski-Kevin H. 2025 Sec. 8.2 (read on 2026-11-01): essentially unique Szilassi embedding, citing the 2002
    issue.
  * L. Szilassi, *On some regular toroids / On three classes of regular toroids* (Hungarian-hosted copy,
    https://www.mi.sanu.ac.rs/vismath/visbook/szilassi/index.html): "In 2004 J. Bokowski and L. Schewe has proved that
    the Szilassi polyhedron had essentially only one axially symmetric version"; reference: "Bokowski, J. and Scewe,
    L. (2004) On Szilassi's Torus, Preprint Technishe Hochschule Darmstadt". Bokowski's own page says both the
    Csaszar and the Szilassi torus "have a geometrical symmetry of order 2. This is optimal, see Bokowski and Eggert
    1991 and Bokowski and Schewe 2004."
  * **So the safest reading of the 2002 paper is: among Szilassi-type embeddings with a symmetry (order 2 optimal),
    essentially one; not "all embeddings of the Heawood map are essentially one" (CLAIMED, unverified).** Anyone who
    cites uniqueness for the calibration E-261101-17 should use the symmetric version until the text is read.
* **Does it decide (8,2), (9,3), (10,4)?** No: genus 1, seven faces; nothing about doubled adjacencies. Its only use
  is calibration at (7, 1). Label: CLAIMED.

## 5. Findings for the matrix and open items

* No source among the four publishes, claims, or excludes a face-neighbourly polyhedron of type (8,2), (9,3) or
  (10,4). Combined with Roest-Vigh and Mizhaev (only (8,3) objects known) the answer to ROADMAP item 2 stays "not found
  in print": CLAIMED, scope = the sources named here plus the searches of 2026-11-03/08 (web only).
* Duality caution restated: the genus-2 theorem and the 1992 census are vertex statements about maps without multiple
  edges. Polarity does not preserve embeddedness, and a doubled adjacency leaves the class of polyhedral maps.
* Corrections suggested for `README.md` (not edited here): `abs1994` volume 86 -> 88 and DOI 10.1007/BF02773687;
  `bokowski-schewe2002` should record "2004 Darmstadt preprint, 'essentially one axially symmetric version'"
  alongside the 2025 survey's "essentially unique"; `altshuler-brehm1992` EuDML record names the wrong author.
* What would raise a read level: the ScienceDirect PDF of the 1986 paper (JCTA articles of that age are in Elsevier's
  open archive; needs a browser session or library proxy by the owner); the Springer PDFs of DCG 8 and Israel J. Math.
  88; the GDZ scan of DCG 8 (https://gdz.sub.uni-goettingen.de, PPN GDZPPN000365408, JS viewer, owner browser). Targeted
  question for the 1986 text: its definition of "polyhedral map" (Section 1) and whether the p-vector argument uses
  the no-multiple-edges property.
* Recommended consequence for the plan (hypothesis, not tested): since nothing in print covers multi-edge dual maps of
  genus 2-4, the own enumeration (cubic maps, K_F underlying graph with 2-3 extra edge copies) is needed and has no
  published control except K12 (59 types).
