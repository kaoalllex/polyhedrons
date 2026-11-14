> **Status: UNREVIEWED (filed 2026-11-14).** An AI-written literature addendum from outside the lab sessions, supplied
> by the owner as a supplement to the realization-space proposal (`../ideas/I-261114-05-realization-space-geometry.md`).
> No project session has read the cited sources for this file or checked its bibliographic data: every statement
> about a paper is CLAIMED at most (`SPEC.md` §5), every proposed transfer is an untested proposal. Do not cite it as
> evidence; a source enters `README.md` (the literature matrix) only after its own read. Overlaps: `schewe2010`,
> `bokowski2025` and ideas I-261029-41, -45, -46. Lead review 2026-11-14 (`../reviews/strategy-review-2026-11-14.md`
> §3) scheduled none of its work items.

# Scientific Literature Addendum: Realizability Obstructions, Oriented Matroids, and the Geometry of Polyhedral Realization Spaces

**Project:** https://github.com/kaoalllex/polyhedrons  
**Date:** November 13, 2026  
**Document type:** Supplement to the scientific review "Geometry of Polyhedral Realization Spaces as a Research Strategy"  
**Purpose:** Identify established mathematical results, evaluate their relevance to the project, and formulate concrete opportunities for transferring existing methods into the search for new face-neighbourly polyhedra.

**Strategic recommendation:** Prioritize the transfer and strengthening of mathematical realizability obstructions over building a general-purpose geometric meta-space.

---

# 1. Executive Summary

## 1.1 Main finding

The idea of studying entire regions of geometric configurations, rather than searching directly for individual coordinate solutions, is well established in discrete geometry.

A substantial body of research already addresses:

- Realization spaces of polytopes and oriented matroids.
- Geometric non-realizability of combinatorial structures.
- Algebraic certificates proving that configurations cannot exist.
- SAT-based exclusion of entire classes of geometric realizations.
- Topological and combinatorial obstructions to embedding surfaces.
- The structure and connectivity of realization spaces.

These results provide a rigorous foundation for the proposed research direction.

However, they also demonstrate that the broad idea itself is not new.

The opportunity for original research lies in adapting and combining these methods for the project's particular setting:

**Closed orientable polyhedral surfaces embedded in R³, with planar simple polygonal faces and exactly three faces incident to every vertex.**

The strongest unresolved target is the 12-face, genus-6, pairwise single-adjacency polyhedron.

The project has an unusual advantage: the 59 combinatorial triangulations dual to this target have already been studied extensively, and their direct simplicial realizations have been proved impossible.

Nevertheless, this does not imply that their dual 12-face polyhedral realizations are impossible.

This distinction creates a potentially valuable research opportunity.

## 1.2 Central research question

The most important question suggested by the literature is:

> Can the oriented-matroid, algebraic, topological, or SAT-based obstructions that prove non-realizability of simplicial triangulations be transformed into new necessary conditions for their combinatorial duals, represented geometrically by face planes?

A successful result would not necessarily settle the 12-face problem.

It could instead provide:

1. New necessary conditions on face-plane arrangements.
2. Stronger SAT/SMT constraints.
3. Algebraic certificates excluding classes of chirotopes.
4. Restrictions on geometric handle-attachment operations.
5. Improved methods for determining whether abstract sign assignments have actual geometric realizations.
6. Explanations for why particular families of configurations cannot produce the desired surface.

These would be meaningful mathematical results even without constructing the target polyhedron.

## 1.3 Initial ranking of the literature

| Priority | Research source | Potential contribution | Transfer difficulty |
|---|---|---|---|
| 1 | Schewe (2010) | SAT-based non-realizability of the same 59 combinatorial triangulations | High |
| 2 | Bokowski, Richter, Sturmfels (1990) | Algebraic certificates of non-realizability | Medium–high |
| 3 | Gouveia, Macchia, Wiebe (2023) | LP-assisted discovery of algebraic certificates | High |
| 4 | Bokowski & Kevin H. (2025) | Direct evidence about the 59 dual polyhedra | Low for analysis, high for new results |
| 5 | Timmreck (2007) | Topological and integer-feasibility obstructions | High |
| 6 | Gouveia, Macchia, Wiebe (2023), realization-space models | Combining complementary representations | Medium–high |
| 7 | Tsukamoto (2013) | Disconnected realization spaces | Low for theory, uncertain computational value |
| 8 | Richter-Gebert & Ziegler (1995) | Universality and complexity of realization spaces | Primarily theoretical |
| 9 | Hougardy, Lutz, Zelke (2010) | Geometric realization heuristics and calibration | Medium |

These rankings concern expected usefulness to the current project, not the mathematical importance of the original publications.

---

# 2. Essential Distinction: Primal and Dual Realizability

Before examining individual papers, one mathematical distinction must be made explicit.

## 2.1 The original simplicial problem

Let K be one of the 59 neighbourly orientable genus-6 triangulations with 12 vertices.

A geometric simplicial realization assigns points

\[
p_1,\ldots,p_{12}\in\mathbb R^3
\]

to the vertices of K.

Every abstract triangle \(\{i,j,k\}\) becomes the ordinary flat geometric triangle

\[
\operatorname{conv}(p_i,p_j,p_k).
\]

The resulting collection of triangles must form an embedded surface without forbidden intersections.

Schewe proved that none of the 59 triangulations admits such a realization.

## 2.2 The project's dual problem

The project's target is different.

The 12 vertices of K correspond to 12 polygonal faces of the desired polyhedron.

Each face lies in a plane

\[
H_i=\{x:n_i\cdot x=d_i\}.
\]

Each triangle \(\{i,j,k\}\) of K corresponds to a vertex of the desired polyhedron:

\[
v_{ijk}=H_i\cap H_j\cap H_k.
\]

Each original vertex i corresponds to a polygonal face whose boundary is determined by the cyclic link of i in K.

Thus, K specifies the combinatorics of the dual polyhedron, but its vertices are not required to become the vertices of a straight-triangle realization of K.

## 2.3 Why the known impossibility theorem does not settle the dual problem

A geometric duality transformation does not generally preserve realizability for non-convex polyhedral surfaces of positive genus.

In particular:

- The original simplicial embedding uses 12 points in R³.
- The desired dual embedding uses 12 planes in R³.
- The 44 vertices of the dual surface arise as triple-plane intersections.
- The polygons of the dual surface may be non-convex.
- The supporting planes do not automatically define an embedded straight-triangle realization of K.

The existence of a valid face-plane realization therefore does not automatically contradict Schewe's theorem.

This is one of the most important facts for the entire research strategy.

**Any proposed transfer of non-realizability results must explicitly prove that its constraints are necessary for the face-plane problem.**

A combinatorial correspondence alone is insufficient.

---

# 3. Lars Schewe (2010): SAT-Based Non-Realizability of the 59 Triangulations

## 3.1 Reference

**Lars Schewe**

*Nonrealizable Minimal Vertex Triangulations of Surfaces: Showing Nonrealizability Using Oriented Matroids and Satisfiability Solvers*

Discrete & Computational Geometry, 43, 289–302 (2010).

- arXiv: https://arxiv.org/abs/0801.2582
- DOI: https://doi.org/10.1007/s00454-009-9222-y

## 3.2 Established result

Schewe proves that none of the vertex-minimal triangulations of the orientable genus-6 surface admits a polyhedral embedding in R³.

In particular, this includes the 59 triangulations with 12 vertices and complete edge graph K12.

The work also provides non-realizability results for certain genus-5 triangulations and develops constructions of infinite families of non-realizable triangulated surfaces.

The primary methodological achievement is the conversion of geometric non-realizability into a satisfiability problem involving oriented matroids.

## 3.3 Mathematical mechanism

A geometric point configuration in R³ induces a rank-4 oriented matroid.

Its chirotope records determinant signs:

\[
\chi(i,j,k,l)
=
\operatorname{sgn}
\det
\begin{pmatrix}
p_i & 1\\
p_j & 1\\
p_k & 1\\
p_l & 1
\end{pmatrix}.
\]

The oriented-matroid axioms impose consistency conditions on these signs.

Additional constraints arise from forbidden geometric intersections.

For example, two simplices that are disjoint in the abstract triangulation must not intersect geometrically.

Using oriented-matroid circuits, these intersection restrictions can be converted into Boolean constraints.

The overall procedure is:

1. Encode the oriented-matroid axioms.
2. Encode geometric compatibility with the combinatorial triangulation.
3. Translate the resulting system into SAT.
4. Determine whether any compatible abstract oriented matroid exists.

If the formula is UNSAT and all encodings are necessary for an embedding, no geometric embedding can exist.

The method can prove non-realizability without searching through continuous vertex coordinates.

## 3.4 Why this is relevant

The current project already follows a related philosophy through OM-SAT.

However, its geometric variables are face planes rather than vertices of a straight-triangle embedding.

This creates an opportunity for a systematic comparison.

The key question is not whether Schewe's theorem can simply be reused.

It cannot be assumed to transfer.

Instead:

**Which structural ingredients of Schewe's obstruction machinery have valid analogues in the face-plane model?**

Potential candidates include:

- Oriented-matroid consistency.
- Circuit-based incidence restrictions.
- Exclusion of forbidden intersections.
- Symmetry reduction.
- Combinatorial simplification of geometric constraints.
- Extraction of minimal contradictory constraint sets.
- Computer-checkable non-realizability certificates.

## 3.5 Proposed transfer investigation

### Task S1: Predicate correspondence audit

Compare Schewe's necessary constraints with the project's `code/omsat.py` and `theory/mathematical-model.md`.

For each relevant constraint:

1. Identify its geometric meaning in Schewe's vertex model.
2. Identify the corresponding objects in the face-plane model.
3. Determine whether a direct analogue exists.
4. Prove its necessity for embedded polygonal faces.
5. Check whether the condition is already implied by the project's existing clauses.
6. Construct a small counterexample if the proposed analogue is false.

The main objective is to identify genuinely new constraints, not to duplicate existing ones.

### Task S2: Search for transferable contradiction patterns

Study whether Schewe's non-realizability arguments contain recurring small collections of incompatible sign relations.

Investigate whether an analogous contradiction can be formulated using face-plane chirotopes.

Important distinction:

A contradiction among primal vertex-orientation signs does not automatically imply a contradiction among dual face-plane signs.

The transfer requires a separate proof.

### Task S3: Investigate proof compression

Determine whether small contradictory subsystems can explain specific negative results more clearly than large SAT certificates.

This could be useful for converting computer-assisted results into short mathematical lemmas.

## 3.6 Expected benefit

Potentially high mathematical impact.

A successful transfer could yield exact constraints for many combinatorial types.

However, the most likely immediate outcome is a structural comparison and the identification of missing assumptions.

## 3.7 Main risk

The primal and dual geometric predicates may be fundamentally different.

Schewe's most powerful forbidden-intersection constraints might not impose any new restrictions on the face-plane problem.

## 3.8 Recommendation

**Highest priority for mathematical analysis, but not for expensive computation.**

Perform a focused predicate-level audit first.

Do not start by reproducing the entire genus-6 SAT computation.

---

# 4. Bokowski and Guedes de Oliveira (2000): Early Non-Realizability Through Oriented Matroid Generation

## 4.1 Reference

**Jürgen Bokowski and António Guedes de Oliveira**

*On the Generation of Oriented Matroids*

Discrete & Computational Geometry, 24, 197–208 (2000).

- DOI: https://doi.org/10.1007/s004540010027

## 4.2 Established result

The authors developed an algorithm for generating oriented matroids and used it to prove the non-realizability of a particular orientable genus-6 triangulated surface.

This provided a counterexample to Grünbaum's conjecture that every closed orientable triangulated surface admits a geometric embedding in R³.

The work also claimed broader non-realizability families.

The later paper by Schewe explicitly reports correcting an error in the earlier literature concerning infinite-family constructions. Therefore, the older claims about infinite families should not be reused without checking the corrected proofs.

## 4.3 Relevance to the project

The most useful aspect is the historical development of exact symbolic exclusions.

The work demonstrates that the following can be a successful mathematical strategy:

1. Start from combinatorics.
2. Derive necessary oriented-matroid conditions.
3. Show that no consistent geometric sign structure exists.
4. Conclude non-realizability without finding coordinates.

This is conceptually aligned with the project's current research direction.

## 4.4 Possible practical application

Review the original oriented-matroid generation and pruning techniques.

Compare them with:

- The current OM-SAT formulation.
- Its symmetry-breaking rules.
- Chirotope consistency checks.
- Existing combinatorial-map enumeration.

The likely benefit is methodological rather than a direct new theorem.

## 4.5 Recommendation

**Secondary reference supporting the Schewe investigation.**

Useful for understanding the historical progression of non-realizability algorithms.

Not recommended as a standalone new research track.

---

# 5. Bokowski, Richter, and Sturmfels (1990): Final Polynomials and Algebraic Impossibility Certificates

## 5.1 Reference

**Jürgen Bokowski, Jürgen Richter, and Bernd Sturmfels**

*Nonrealizability Proofs in Computational Geometry*

Discrete & Computational Geometry, 5, 333–350 (1990).

- DOI: https://doi.org/10.1007/BF02187794
- Related author publication record: https://www.mis.mpg.de/people/bernd-sturmfels/publications

## 5.2 Central idea

Rather than searching for geometric coordinates, derive an algebraic contradiction from determinant relations that every realization must satisfy.

Plücker coordinates and Grassmann–Plücker relations impose polynomial identities on determinants of realizable configurations.

An abstract chirotope specifies signs of those determinants.

A final polynomial provides an algebraic incompatibility certificate.

Conceptually, it shows that the required signs cannot coexist with the polynomial identities governing actual geometric configurations.

This distinction is important:

An abstract oriented matroid may satisfy combinatorial axioms without corresponding to an actual real vector configuration.

Final-polynomial methods address that realizability gap.

## 5.3 Relevance to the face-plane model

The project represents each face plane by a homogeneous vector

\[
h_i\in\mathbb R^4.
\]

The determinants of quadruples of these vectors are natural Plücker-type quantities.

For 12 face planes and the plane at infinity, the project already uses 715 determinant signs.

Therefore, the existing representation is directly suitable for studying algebraic compatibility conditions on those determinants.

The potential research objective is:

**Find compact algebraic certificates excluding particular face-plane sign assignments or families of assignments.**

## 5.4 Important distinction

A final polynomial excluding one chirotope does not necessarily exclude an entire combinatorial type.

A combinatorial type may admit many abstract chirotopes satisfying the embedding predicates.

To prove that the entire type is non-realizable, one must cover all admissible possibilities or derive a type-wide contradiction.

The project must distinguish:

- A certificate excluding one abstract sign assignment.
- A certificate excluding a family of sign assignments.
- A proof excluding an entire combinatorial type.

These have very different mathematical strength.

## 5.5 Proposed transfer experiment

Use the project's existing final-polynomial infrastructure.

Start with a known SAT chirotope model that has already been shown non-realizable.

Then:

1. Extract its determinant-sign constraints.
2. Reconstruct the algebraic incompatibility certificate.
3. Verify the polynomial identity independently.
4. Identify which sign assumptions are actually used.
5. Remove irrelevant sign assumptions where possible.
6. Test whether the remaining certificate excludes additional candidate models.

The main quantity of interest is not merely certificate size.

It is **certificate generality**.

A certificate that excludes many configurations is more valuable than one that describes a single failed model.

## 5.6 Potential mathematical payoff

The strongest possible result would be a compact algebraic lemma of the form:

> No realizable arrangement of face planes can satisfy this particular collection of determinant-sign conditions.

If those conditions are forced by a combinatorial family, the lemma would exclude that entire family.

## 5.7 Main risks

- Certificates may be highly specific.
- Algebraic elimination may be expensive.
- Small certificates may not exist in the chosen representation.
- A contradiction might rely on dozens or hundreds of determinant signs.
- Generalizing a certificate may be harder than finding it.

## 5.8 Recommendation

**High priority as a proof-oriented research direction.**

Especially promising because the project already has partial infrastructure and previous experience with exact final-polynomial exclusions.

---

# 6. Gouveia, Macchia, and Wiebe (2023): Discovering Non-Realizability Certificates Using Linear Programming

## 6.1 Reference

**João Gouveia, Antonio Macchia, and Amy Wiebe**

*General Non-Realizability Certificates for Spheres with Linear Programming*

Journal of Symbolic Computation, 114, 172–192 (2023).

- arXiv: https://arxiv.org/abs/2109.15247
- DOI: https://doi.org/10.1016/j.jsc.2022.04.013
- Authors' implementation and certificates: https://bitbucket.org/macchia/nonrealizability

## 6.2 Established contribution

The authors develop a method for constructing algebraic non-realizability certificates using linear programming.

The central idea is to reformulate realizability as the existence of a positive real point satisfying certain polynomial equations.

One then searches for a polynomial belonging to the corresponding ideal whose coefficients are positive in an appropriate monomial representation.

Such a polynomial cannot vanish at a strictly positive point.

Therefore, the existence of the certificate proves that the required positive realization is impossible.

The authors use a reduced slack-ideal representation and linear programming to search for certificates.

They demonstrate the method on combinatorial spheres and related polytope-realizability problems.

## 6.3 Why the approach is interesting

The method separates two tasks:

### Discovery

Use optimization to find a candidate algebraic identity.

### Verification

Check the resulting identity exactly.

This is especially attractive for a research project operating on a single laptop.

The expensive reasoning can be converted into a finite certificate, and the final mathematical claim does not depend on trusting floating-point optimization.

## 6.4 Applicability limitations

The published method concerns polytopes and combinatorial spheres.

The project's target surfaces have positive genus and may be highly non-convex.

Consequently:

- The standard slack-matrix formulation for convex polytopes does not directly describe these surfaces.
- Facet inequalities for convex bodies cannot simply be reused.
- A new suitable algebraic representation may be needed.
- Positivity assumptions must be independently justified.

The correct transfer is methodological, not a direct import of the paper's theorem.

## 6.5 Proposed adaptation

Investigate an analogous certificate search based on the project's face-plane determinants.

Let

\[
\Delta_{ijkl}
=
\det(h_i,h_j,h_k,h_l).
\]

For a particular candidate sign pattern, introduce positive variables corresponding to signed determinant magnitudes.

Use the polynomial identities satisfied by realizable determinant arrays.

Then investigate whether the resulting equations admit an algebraic positivity certificate of infeasibility.

A possible pipeline:

1. Choose a small non-realizable abstract chirotope.
2. Translate its signs into positivity requirements.
3. Construct a restricted polynomial system from Grassmann–Plücker relations.
4. Search a small monomial support for a positive polynomial identity.
5. Use LP to find candidate coefficients.
6. Rationalize coefficients.
7. Verify the identity exactly.
8. Minimize the set of sign assumptions involved.

This pipeline should first reproduce an existing certified negative example.

## 6.6 Best initial application

Do not begin with all 59 genus-6 types.

Start with one of the project's existing non-realizable SAT models for which a final-polynomial certificate is available.

The goal is to determine whether an LP-assisted method can recover a comparable or smaller certificate at low computational cost.

## 6.7 Success criterion

The method becomes strategically interesting if it can:

- Reproduce known certificates.
- Find smaller certificates.
- Discover certificates with fewer sign assumptions.
- Exclude multiple candidate models with one identity.
- Avoid expensive direct nonlinear realizability searches.

## 6.8 Recommendation

**High-priority experimental method, conditional on a small positive-control demonstration.**

This may be one of the strongest practical opportunities for transferring a method from contemporary algebraic geometry into the project.

---

# 7. Dagmar Timmreck (2007): Topological Obstructions and Integer Feasibility

## 7.1 Reference

**Dagmar Timmreck**

*Necessary Conditions for Geometric Realizability of Simplicial Complexes*

- arXiv: https://arxiv.org/abs/0705.1912

## 7.2 Established result

Timmreck associates a system of linear equations and inequalities with a simplicial complex.

If the complex admits a simplicial embedding in the specified Euclidean space, the corresponding system must admit an integer solution.

The method extends earlier work by Isabella Novik and uses ideas from obstruction theory, deformation cochains, intersection numbers, and linking numbers.

This provides a potential route to non-realizability proofs through integer programming.

## 7.3 Why this is conceptually important

The method translates geometric existence into a discrete necessary condition.

Instead of constructing coordinates, one studies algebraic-topological quantities that any geometric realization would have to satisfy.

The general reasoning pattern is:

\[
\text{Geometric realization}
\Longrightarrow
\text{Integer-feasible obstruction system}.
\]

Therefore,

\[
\text{Integer infeasibility}
\Longrightarrow
\text{No geometric realization}.
\]

This is exactly the sort of mathematical reasoning that could eliminate families of candidates.

## 7.4 Important limitation from the paper itself

The paper explicitly reports that certain studied subsystems for genus-5 and genus-6 examples remain feasible.

Thus, the published constraints do not automatically reproduce Schewe's impossibility theorem for the 59 triangulations.

This is critical.

The paper provides a potentially transferable framework, not an established solution to the project's genus-6 dual problem.

Furthermore, its original setting is simplicial complexes, whereas the project uses general polygonal faces.

## 7.5 Proposed research question

Can topological intersection and linking constraints be expressed directly for face-plane realizations?

A possible approach is:

1. Select a combinatorial polyhedral surface K.
2. Identify disjoint cycles, face boundaries, and relevant subcomplexes.
3. Derive topological intersection restrictions for an embedded surface.
4. Determine whether the restrictions can be expressed using the project's exact geometric predicates.
5. Translate the resulting conditions into integer or SAT constraints.
6. Test whether they provide information not already implied by existing embedding clauses.

One possible alternative is to triangulate the polygonal surface.

However, this requires care.

For a non-convex polygon, not every diagonal is contained inside the face.

A valid triangulation may depend on the actual geometric realization.

Therefore, choosing an arbitrary triangulation of the abstract polygonal faces may exclude valid solutions.

Any use of auxiliary triangulations must preserve completeness or explicitly limit the scope of the conclusion.

## 7.6 Potential payoff

A genuinely new topological condition could be more powerful than another local intersection predicate.

It might constrain all possible realizations of a combinatorial family.

## 7.7 Main risk

The necessary conditions may be too weak.

Additionally, some conditions may already follow from the project's existing global embedding requirements.

## 7.8 Recommendation

**Mathematically interesting, but lower immediate priority than final-polynomial and SAT-based obstruction mining.**

First perform a focused applicability audit.

Do not build a large integer-programming engine without evidence that the resulting constraints discriminate among relevant examples.

---

# 8. Bokowski and Kevin H. (2025): Direct Investigation of the 59 Dual Polyhedra

## 8.1 Reference

**Jürgen Bokowski and Kevin H.**

*Polyhedral Embeddings of Triangular Regular Maps of Genus g, 2 ≤ g ≤ 14, and Neighborly Spatial Polyhedra*

Symmetry, 17(4), 622 (2025).

- Article: https://www.mdpi.com/2073-8994/17/4/622
- DOI: https://doi.org/10.3390/sym17040622

## 8.2 Established findings

The paper surveys and investigates polyhedral embeddings of regular maps and neighbourly spatial polyhedra.

It explicitly discusses the 59 genus-6 triangulations with 12 vertices and their combinatorial duals.

The authors report that their numerical methods did not find embeddings of the corresponding dual polyhedra with:

- 12 polygonal faces.
- Eleven edges per face.
- 44 vertices.

The paper also presents a self-intersecting model for one dual combinatorial structure, with a small number of polygon intersections.

This is important because the authors distinguish the impossible direct triangular embeddings from the unsuccessfully searched dual embeddings.

## 8.3 What the paper does not prove

The failure to find dual embeddings is not a mathematical proof that none exist.

In particular, the paper does not establish a general non-realizability theorem for all 59 dual face-plane structures.

The project's target therefore remains mathematically open on the basis of these results.

## 8.4 Research opportunity

The self-intersecting construction deserves a targeted geometric analysis.

Instead of treating it merely as a failed solution, investigate whether its intersections reveal a small set of critical geometric constraints.

Potential questions:

1. Which face pairs intersect improperly?
2. Which determinant signs control these intersections?
3. Can the intersections be removed by a deformation preserving the relevant combinatorial map?
4. Does the candidate satisfy necessary Gauss-map conditions?
5. Are there local geometric obstructions preventing a repair?
6. Can the configuration be classified within the project's existing chirotope framework?

This is closely aligned with the proposed obstruction-guided exploration.

## 8.5 Important caution

Repairing one specific self-intersecting model is not equivalent to resolving the entire combinatorial type.

Even if one model cannot be repaired within its nearby geometric region, another disconnected region might contain a valid realization.

The result of a local repair investigation must therefore be stated with its precise scope.

## 8.6 Recommended work item

**Reconstruct and classify the published self-intersecting dual model using the project's exact verifier.**

Prerequisites:

- Obtain trustworthy coordinates or reconstruct the model from the published data.
- Confirm its combinatorial map.
- Verify its intersections independently.
- Record the complete face-plane chirotope if applicable.
- Identify any degeneracies or violations of the project's general-position assumptions.

Then use it as a controlled negative example for evaluating obstruction-guided methods.

## 8.7 Recommendation

**High relevance as experimental evidence and a potential benchmark.**

A better starting point than generating large numbers of random near-misses.

---

# 9. Richter-Gebert and Ziegler (1995): Universality of Realization Spaces

## 9.1 Reference

**Jürgen Richter-Gebert and Günter M. Ziegler**

*Realization Spaces of 4-Polytopes Are Universal*

Bulletin of the American Mathematical Society, 32, 403–412 (1995).

- arXiv: https://arxiv.org/abs/math/9510217

## 9.2 Established result

The authors explain a universality theorem for realization spaces of four-dimensional convex polytopes.

These spaces can exhibit the complexity of arbitrary primary semialgebraic sets in the relevant stable-equivalence sense.

In particular, realization spaces can have complicated topology and arithmetic structure.

This shows that geometric realization spaces are not necessarily simple connected regions.

## 9.3 Relevance to the project

The result supports the general scientific legitimacy of studying realization spaces.

It also warns against simplistic assumptions.

In particular:

- A realization space may be disconnected.
- It may have nontrivial topology.
- Local numerical optimization may explore only a limited region.
- A finite collection of samples may provide little information about global structure.

## 9.4 What cannot be concluded

The theorem concerns four-dimensional convex polytopes.

It does not prove that the realization spaces of the project's particular non-convex polyhedral surfaces are equally complicated.

It also does not establish that the current optimization plateaus are caused by disconnected components.

The theorem is a warning about possible complexity, not an explanation of specific failed experiments.

## 9.5 Recommendation

**Use as theoretical background and as a reason to avoid constructing a complete global realization-space atlas.**

Do not treat universality as evidence that a particular target region exists.

---

# 10. Yasuyuki Tsukamoto (2013): Disconnected Spaces with Fixed Oriented Matroids

## 10.1 Reference

**Yasuyuki Tsukamoto**

*New Examples of Oriented Matroids with Disconnected Realization Spaces*

Discrete & Computational Geometry (2013).

- arXiv: https://arxiv.org/abs/1201.2560
- DOI: https://doi.org/10.1007/s00454-012-9456-y

## 10.2 Established result

Tsukamoto constructs rank-3 oriented matroids on 13 elements whose realization spaces are disconnected.

Thus, even when the oriented matroid is fixed, its geometric realizations may occupy multiple connected components.

This is directly relevant to the proposed chirotope-chamber atlas.

## 10.3 Consequence for the project

The following identification is not generally valid:

\[
\text{One chirotope}
=
\text{One connected geometric chamber}.
\]

A fixed chirotope can correspond to multiple connected realization components.

Therefore, a graph whose nodes are chirotopes is not necessarily a graph of connected components.

This affects:

- Reachability analysis.
- Chamber transition graphs.
- Distance-to-solution metrics.
- Connectivity experiments.
- Interpretation of archived realizations.

## 10.4 Practical recommendation

Use chirotopes primarily as discrete geometric signatures.

Do not infer connectivity from sign equality alone.

For any claimed transition between geometric realizations, require an explicit verified path or an applicable connectivity theorem.

## 10.5 Research value

Primarily methodological.

This work identifies an important failure mode in the original meta-space proposal.

It does not immediately provide a new way to construct or exclude the project's target polyhedron.

---

# 11. Gouveia, Macchia, and Wiebe (2023): Combining Different Realization-Space Models

## 11.1 Reference

**João Gouveia, Antonio Macchia, and Amy Wiebe**

*Combining Realization Space Models of Polytopes*

Discrete & Computational Geometry, 69, 505–542 (2023).

- arXiv: https://arxiv.org/abs/2001.11999
- DOI: https://doi.org/10.1007/s00454-022-00379-8

## 11.2 Established contribution

The paper studies several representations of polytope realization spaces:

- Classical vertex-coordinate representations.
- Grassmannian representations.
- Gale-transform representations.
- Slack-matrix representations.

The authors investigate explicit relationships between these models and show how combining their strengths can simplify difficult computations.

A central lesson is:

**No single representation is necessarily best for every aspect of a realizability problem.**

## 11.3 Relevance to the project

The project already has several complementary formulations:

- Face-plane coordinates.
- Chirotope signs.
- SAT/SMT constraints.
- Fixed-normal feasibility.
- Gauss-map conditions.
- Combinatorial maps.
- Exact embedding predicates.

The literature supports treating these as complementary mathematical views rather than forcing them into one feature space.

## 11.4 Possible transfer

Investigate which questions become simpler in which representation.

For example:

| Research question | Potentially useful representation |
|---|---|
| Does a concrete object exist? | Exact face planes and combinatorial map |
| Is a sign assignment combinatorially consistent? | Oriented matroid / SAT |
| Are offsets feasible for fixed normals? | Linear constraints |
| Are global geometric conditions satisfied? | Exact embedding predicates |
| Is a particular chirotope realizable? | Determinantal polynomial constraints |
| Why is a configuration infeasible? | UNSAT cores and algebraic certificates |
| Can a family be excluded? | Symbolic inequalities or transferable certificates |

This could lead to a cleaner research architecture in which solvers exchange mathematically meaningful certificates.

## 11.5 Limitation

The paper's slack-matrix theory concerns convex polytopes and cannot be transplanted directly into the positive-genus setting.

Any new algebraic representation for the project's non-convex surfaces would require an independent correctness argument.

## 11.6 Recommendation

**Useful as a conceptual guide for combining existing models.**

Potentially valuable for designing a better SAT-to-geometry bridge and stronger non-realizability certificates.

---

# 12. Hougardy, Lutz, and Zelke (2010): Surface Realization Through Geometric Optimization

## 12.1 Reference

**Stefan Hougardy, Frank H. Lutz, and Mariano Zelke**

*Surface Realization with the Intersection Edge Functional*

Experimental Mathematics, 19(1), 79–92 (2010).

- arXiv: https://arxiv.org/abs/math/0608538

## 12.2 Established contribution

The authors develop a geometric optimization heuristic based on an intersection-edge functional.

They use it to realize many difficult simplicial surface triangulations.

Their results include geometric realizations for vertex-minimal triangulations of orientable surfaces of genus 3 and 4, as well as examples of genus-5 simplicial polyhedra with 12 vertices.

## 12.3 Relevance

This work provides an important contrast to pure non-realizability methods.

It demonstrates the value of:

- Geometrically meaningful objective functions.
- Exact combinatorial structure.
- Carefully chosen positive controls.
- Optimization methods tailored to intersections rather than generic coordinate distance.

The connection to the current project is methodological.

## 12.4 Possible application

Compare the project's existing violation objectives with intersection-based geometric functionals.

A useful question is whether such functionals provide better information near the boundaries of valid face-plane regions.

However, the method was developed for simplicial surfaces and should not be assumed to transfer unchanged to non-convex polygonal faces.

## 12.5 Recommendation

**Use primarily as a benchmark and methodological reference.**

Do not launch a new optimization campaign unless a small experiment demonstrates an improvement over existing project methods.

---

# 13. What Is Already Known, and What May Still Be New?

The literature suggests the following classification.

| Research proposition | Status |
|---|---|
| Study geometric realization spaces instead of individual coordinate solutions | Established mathematics |
| Use oriented matroids to encode geometry | Established mathematics |
| Prove geometric non-realizability using SAT | Established technique |
| Prove all 59 direct genus-6 triangulations non-realizable | Established result |
| Derive algebraic non-realizability certificates | Established technique |
| Search for such certificates using LP | Established for relevant polytope-realizability settings |
| Characterize arbitrary realization spaces through semialgebraic geometry | Established theoretical framework |
| Automatically transfer Schewe's theorem to the 59 dual polyhedra | Not justified |
| Prove all 59 dual face-plane configurations non-realizable | Not established by the reviewed sources |
| Derive new dual-specific necessary conditions from primal obstruction methods | Open research opportunity |
| Transfer algebraic certificates across families of face-plane chirotopes | Proposed research opportunity |
| Establish geometric restrictions on genus-changing transformations | Proposed research opportunity |
| Use critical sign changes to guide exact search between face-plane regions | Proposed research opportunity |

The key scientific distinction is between reusing established mathematics and producing a new mathematical statement about the project's particular objects.

The latter is where original research may emerge.

---

# 14. Recommended Research Program

The following program is designed for a single-laptop research project with limited computational resources.

It deliberately prioritizes mathematical leverage over large-scale experimentation.

## Phase 1: Transferability Audit

### Objective

Determine which existing non-realizability techniques are mathematically compatible with the project's face-plane setting.

### Primary literature

- Schewe (2010).
- Bokowski, Richter, Sturmfels (1990).
- Timmreck (2007).
- Gouveia, Macchia, Wiebe (2023).

### Required work

For each candidate technique, identify:

1. The exact theorem or constraint.
2. Its required geometric assumptions.
3. Whether it concerns vertices, supporting planes, simplices, or general polygons.
4. Whether convexity is required.
5. Whether the method permits positive genus.
6. Whether it assumes simplicial faces.
7. What changes are needed for a face-plane interpretation.
8. Whether the resulting condition is already contained in the project's exact embedding model.

### Deliverable

A transferability matrix with statuses:

- DIRECTLY APPLICABLE.
- APPLICABLE AFTER PROVED REDUCTION.
- POTENTIALLY ADAPTABLE.
- NOT APPLICABLE.
- ALREADY IMPLEMENTED.
- UNRESOLVED.

### Stop criterion

If no genuinely new necessary condition or promising certificate mechanism survives the audit, do not initiate a new solver campaign.

---

## Phase 2: Algebraic Certificate Pilot

### Objective

Test whether the project's existing non-realizable SAT models admit compact, reusable algebraic certificates.

### Method

Use the existing final-polynomial infrastructure.

Adapt the LP-assisted certificate-search ideas of Gouveia, Macchia, and Wiebe if the representation supports them.

### Positive control

Reproduce an existing exactly checked final-polynomial contradiction.

### Experimental question

Can the certificate be simplified or generalized?

### Measurements

- Number of determinant signs involved.
- Polynomial degree.
- Number of monomials.
- Rational coefficient complexity.
- Time required to discover the certificate.
- Time required to verify it.
- Number of additional abstract models excluded by the same certificate.

### Success criterion

At least one certificate must either:

1. Exclude additional previously unexcluded sign assignments.
2. Depend on fewer assumptions than the original certificate.
3. Produce a reusable mathematical restriction.
4. Substantially reduce verification or discovery cost on an independent example.

Merely reproducing a known certificate is a correctness control, not evidence of improved discovery power.

### Recommended budget

A small, capped pilot.

Do not attempt a full genus-6 classification.

---

## Phase 3: Obstruction Transfer Between Nearby Configurations

### Objective

Determine whether mathematical obstructions remain valid across nearby realizable chirotopes or regions of normal space.

### Main hypothesis

An infeasibility certificate derived for one configuration may remain valid under a mathematically describable family of geometric changes.

### Possible approaches

- Dependency analysis of exact predicates.
- Minimal UNSAT cores.
- Parametric linear feasibility.
- Farkas-type dual certificates.
- Restricted determinant-sign systems.
- Algebraic identities with small sign support.

### Required validation

Every generalized exclusion must be proved for the entire stated family.

Sampling multiple excluded examples does not establish a family-wide theorem.

### Potential payoff

A method for excluding many geometric configurations using one exact certificate.

This is one of the strongest possible outcomes of the realization-space perspective.

---

## Phase 4: Application to the Current Constructive Targets

Only after the earlier phases establish useful results should the method be integrated into the current target searches.

### Nine mutually adjacent faces

Potential contribution:

- Eliminate cells through exact necessary conditions.
- Reuse constraints between nearby ninth-plane cells.
- Reduce expensive solver calls.
- Preserve certified coverage.

### S6 (10,3)

Potential contribution:

- Strengthen oriented-matroid constraints.
- Improve the SAT-to-coordinates bridge.
- Exclude incompatible sign assignments earlier.
- Explain fixed-normal infeasibility.

### S5 (10,4)

Potential contribution:

- Detect higher-genus obstructions.
- Derive constraints on admissible geometry.
- Improve the selection of structured arrangements.

### S0 (12,6)

Do not restart large-scale search automatically.

Return to S0 if a mathematical result transfers to the 59 combinatorial types or meaningfully improves their exact realizability analysis.

---

# 15. Specific Research Questions for a Scientific Agent

The following questions are suitable for a dedicated mathematical research agent.

## Question 1: Transfer of Schewe's obstructions

Can any circuit, chirotope, or forbidden-intersection argument from Schewe's proof be transformed into a necessary condition for the face-plane realization of the combinatorial dual?

Required output:

- A precise proposed statement.
- A proof or counterexample.
- Comparison with existing OM-SAT clauses.
- Explanation of which dual combinatorial maps it constrains.

## Question 2: Generalizing final-polynomial certificates

Can existing non-realizable face-plane chirotopes be grouped into families excluded by a common algebraic identity?

Required output:

- A verified polynomial identity.
- Explicit sign assumptions.
- The family of excluded assignments.
- A proof of exclusion.
- Reproduction using the project's exact arithmetic.

## Question 3: Parametric offset infeasibility

For fixed normals, the offset feasibility conditions within a prescribed full chirotope are linear.

Can an infeasibility certificate for one normal configuration be extended to a neighbourhood or an explicitly defined semialgebraic region of normal configurations?

Required output:

- A parameterized certificate.
- Its domain of validity.
- An exact proof.
- A small positive control and a negative control.

## Question 4: Geometrically meaningful chamber boundaries

Which determinant-sign changes can actually alter the validity of a particular polyhedral embedding?

Can one identify a proper subset of critical sign changes sufficient to describe all changes in the embedding predicates?

Required output:

- A precise definition of critical signs.
- A sound dependency or transition rule.
- A proof that excluded transitions cannot repair the violated constraints.
- Comparison with naive Hamming-distance exploration.

## Question 5: Restrictions on handle attachment

For a specified combinatorial handle-attachment operation that raises the genus of a cubic surface, can one derive necessary conditions on the associated face-plane arrangement?

Required output:

- Exact definition of the operation.
- Necessary incidence relations.
- Resulting determinant-sign conditions.
- Proof or counterexample.
- Applicability to the 12-face genus ladder.

---

# 16. Scientific Integrity Requirements

Any follow-up research must observe the following rules.

## Distinguish the different realization problems

Never confuse:

1. Realizability of an abstract triangulation by flat triangles.
2. Realizability of its combinatorial dual by flat polygonal faces.
3. Existence of an abstract oriented matroid satisfying some constraints.
4. Realizability of that oriented matroid over the real numbers.
5. Existence of an immersed surface.
6. Existence of an embedded surface.

These are not equivalent.

## Treat solver conclusions with the correct scope

- SAT does not imply geometric realizability.
- UNSAT excludes only the precisely encoded family, assuming soundness.
- A solver timeout is not a negative result.
- A final polynomial excluding one chirotope does not automatically exclude a combinatorial type.
- An infeasible fixed-normal problem does not exclude all possible normals.
- A failed geometric deformation does not prove that another valid realization is unreachable.

## Do not claim novelty without literature comparison

For every proposed new lemma:

1. Search for established equivalents.
2. Identify the exact difference from prior results.
3. Provide a complete proof.
4. Test small counterexamples.
5. Obtain independent mathematical review.

## Keep numerical experiments separate from mathematical proof

Numerical experiments may suggest patterns, but cannot establish:

- Non-realizability of an entire type.
- Disconnectedness of realization space.
- Absence of geometric transitions.
- Completeness of a search family.
- The existence of a universal obstruction.

Claims of these kinds require mathematical arguments or exact, soundly scoped computational certificates.

---

# 17. Final Assessment and Strategic Recommendation

## What the literature establishes

There is extensive prior research on geometric realization spaces and non-realizability.

The fundamental concepts behind the original proposal are established mathematics.

However, the published results also demonstrate that strong mathematical impossibility theorems can be obtained without searching over continuous coordinates.

Schewe's proof for the 59 genus-6 triangulations is a particularly striking example.

The project's face-plane dual problem remains distinct from the simplicial problem solved by Schewe.

That distinction is both a limitation and an opportunity.

## The strongest opportunity

The most promising research program is to combine:

**Oriented-matroid constraints + algebraic non-realizability certificates + exact face-plane geometry + transferable obstructions.**

This could turn the project's current negative computational evidence into mathematical statements excluding entire classes of geometric configurations.

## What should receive priority

### First

Investigate whether Schewe's obstruction machinery contains structural ideas that survive passage to the face-plane formulation.

### Second

Investigate whether the project's existing final-polynomial certificates can be generalized using algebraic methods and LP-assisted certificate discovery.

### Third

Study whether exact infeasibility certificates can be transferred between neighbouring geometric regions, especially across fixed-normal fibres and critical chirotope boundaries.

### Fourth

Only if these methods prove useful, incorporate them into the existing constructive searches for nine and ten faces.

## What should not receive priority

- Generic numerical clustering.
- e-means integration.
- A complete realization-space atlas.
- Large random searches through sign patterns.
- Full enumeration of abstract oriented matroids without a clear feasibility argument.
- Unverified transitions between combinatorial types.
- Broad machine-learning experiments lacking a precise mathematical hypothesis.

## Final strategic verdict

**PILOT — with priority given to mathematical obstruction discovery, not geometric clustering.**

The proposed idea becomes substantially stronger when reformulated as:

> Study the geometry and algebra of polyhedral realization spaces to identify necessary conditions, critical transitions, and transferable certificates of non-realizability.

The ultimate scientific objective should be:

**Develop a mathematically rigorous method that can exclude infinite families or large combinatorial classes of impossible geometric configurations through compact, independently verifiable arguments.**

Even one useful new theorem of this kind could have lasting value beyond the immediate search for the next Szilassi-type polyhedron.

---

# 18. Bibliography

1. Schewe, L. (2010). *Nonrealizable Minimal Vertex Triangulations of Surfaces: Showing Nonrealizability Using Oriented Matroids and Satisfiability Solvers.* Discrete & Computational Geometry, 43, 289–302.  
   https://arxiv.org/abs/0801.2582  
   https://doi.org/10.1007/s00454-009-9222-y

2. Bokowski, J., & Guedes de Oliveira, A. (2000). *On the Generation of Oriented Matroids.* Discrete & Computational Geometry, 24, 197–208.  
   https://doi.org/10.1007/s004540010027

3. Bokowski, J., Richter, J., & Sturmfels, B. (1990). *Nonrealizability Proofs in Computational Geometry.* Discrete & Computational Geometry, 5, 333–350.  
   https://doi.org/10.1007/BF02187794

4. Gouveia, J., Macchia, A., & Wiebe, A. (2023). *General Non-Realizability Certificates for Spheres with Linear Programming.* Journal of Symbolic Computation, 114, 172–192.  
   https://arxiv.org/abs/2109.15247  
   https://doi.org/10.1016/j.jsc.2022.04.013

5. Timmreck, D. (2007). *Necessary Conditions for Geometric Realizability of Simplicial Complexes.*  
   https://arxiv.org/abs/0705.1912

6. Bokowski, J., & Kevin H. (2025). *Polyhedral Embeddings of Triangular Regular Maps of Genus g, 2 ≤ g ≤ 14, and Neighborly Spatial Polyhedra.* Symmetry, 17(4), 622.  
   https://doi.org/10.3390/sym17040622

7. Richter-Gebert, J., & Ziegler, G. M. (1995). *Realization Spaces of 4-Polytopes Are Universal.* Bulletin of the American Mathematical Society, 32, 403–412.  
   https://arxiv.org/abs/math/9510217

8. Tsukamoto, Y. (2013). *New Examples of Oriented Matroids with Disconnected Realization Spaces.* Discrete & Computational Geometry.  
   https://arxiv.org/abs/1201.2560  
   https://doi.org/10.1007/s00454-012-9456-y

9. Gouveia, J., Macchia, A., & Wiebe, A. (2023). *Combining Realization Space Models of Polytopes.* Discrete & Computational Geometry, 69, 505–542.  
   https://arxiv.org/abs/2001.11999  
   https://doi.org/10.1007/s00454-022-00379-8

10. Hougardy, S., Lutz, F. H., & Zelke, M. (2010). *Surface Realization with the Intersection Edge Functional.* Experimental Mathematics, 19(1), 79–92.  
    https://arxiv.org/abs/math/0608538

---

# 19. Scope and Limitations of This Addendum

This document supplements the original realization-space strategy review.

The cited papers and their main stated results were checked against available publication records, abstracts, or online full text.

The proposed applications to the polyhedrons project are research hypotheses unless explicitly described as established consequences.

No new mathematical theorem has been proved in this addendum.

No computation was performed against the project's current data.

No new polyhedral realization was constructed.

No complete proof-transfer audit or exhaustive novelty search was performed.

In particular, the absence of a directly applicable theorem in the reviewed sources must not be interpreted as proof that no such theorem exists elsewhere in the literature.

Before claiming an original mathematical result, the project should perform a more comprehensive literature and proof audit.

**Final recommendation: Focus the next mathematical investigation on the Schewe-to-dual transfer problem and the generalization of algebraic non-realizability certificates.**

**The goal is not to create another search engine. It is to discover mathematical constraints that make large parts of the search unnecessary.**