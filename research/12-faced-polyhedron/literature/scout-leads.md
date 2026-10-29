# Interdisciplinary scout leads (12-face polyhedron)

Scope: about 25 tool calls, mostly WebSearch; no full PDF reads. Each lead gives the field, the correspondence to our problem (marked ANALOGY where it is only an analogy), sources, and one experiment. Ranked by expected usefulness.

## 1. Non-realizability of 12-vertex genus-6 neighborly triangulations (Schewe; Bokowski-Schewe) [highest priority, check first]
- Field: oriented matroids + SAT, polyhedral embeddings.
- Correspondence: our face-plane model (mathematical-model.md section 2) uses the dual triangulation T of the 59 neighborly genus-6 types. The 2008 paper proves the 59 types of the vertex-version (T as a polyhedral surface with points as vertices) admit no acyclic uniform oriented matroid. Our problem is the dual (planes as faces, triple points as vertices). It is NOT the same OM. ANALOGY, not implication, unless the transfer is proved. Polarity does not preserve nonconvex surfaces in general.
- Sources: https://arxiv.org/pdf/0801.2582 ; SAT 2006 abstract by Schewe (ICMS 2006, via the 2008 bibliography).
- Experiment: write down explicitly the relation between the 12-plane chirotope (on 13 elements, incl. infinity) and any point chirotope on the 12 vertices of T. Decide whether the 2008 UNSAT certificate can be reused, or whether a new UNSAT run on the section-6(A) instance is needed. This decides whether Series 1 is already dead.

## 2. Schewe-style SAT encoding of chirotope axioms (reuse as the core of OM-SAT, section 6(A))
- Field: SAT encoding of uniform oriented matroids.
- Correspondence: exactly our section 6(A) variables (one Boolean per ordered 4-subset of 13 elements; 3-term Grassmann-Plucker relations). The 2008 paper gives 16 clauses of 6 literals per GP relation, total 16 * C(n, r-2) * C(n-r+2, 4), with r = 4, n = 13.
- Sources: https://arxiv.org/pdf/0801.2582 ; https://arxiv.org/pdf/1508.02531 (2015 survey, notes the SAT encoding and an implementation by D. Bremner, plus an IP alternative).
- Experiment: generate the 715-variable GP clause set for n = 13, r = 4 in a script, and check its clause count against the formula above. Then run it on Szilassi's 7 planes (n = 8 incl. infinity) and confirm SAT, as section 6 requires.

## 3. Symmetry breaking for the chirotope SAT (BreakID / satsuma)
- Field: SAT symmetry breaking.
- Correspondence: the reorientation group of the 12 face elements plus the infinity reorientation and global sign (section 4) gives an explicit symmetry group. Lex-leader predicates from generators are the standard fix.
- Sources: https://arxiv.org/pdf/1608.08447 (BreakID) ; https://arxiv.org/pdf/2406.13557 (satsuma) ; https://arxiv.org/pdf/2601.16855 (2026, warns lex-leader blows up proofs; use unit/binary breakers).
- Experiment: add only the unit/binary breakers fixing chi(1,2,k,inf), chi(1,3,4,inf), chi(2,3,4,inf) (section 4), and compare solve time and proof size on the F = 7 control instance.

## 4. Proof certificates for UNSAT: DRAT / PR proofs checked by cake_lpr
- Field: verified SAT proof checking.
- Correspondence: a UNSAT result of OM-SAT (section 6(A)) would otherwise be a claim with no certificate. Final polynomials are an algebraic alternative (lead 5).
- Sources: https://cca.informatik.uni-freiburg.de/papers/PolittFleuryBiere-MBMV23.pdf (PR/LPR proof tooling) ; https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SAT.2023.21 (SAT 2023, proof-related) . No source found that combines oriented matroids with cake_lpr; treat as an untested pipeline.
- Experiment: export the F = 7 control run to DRAT with drat-trim, and check the proof size. Then test whether a PR proof for the GP encoding is produced by a SAT solver that supports it.

## 5. Final polynomials and realizability certificates
- Field: real algebraic geometry of oriented matroids (Bokowski-Sturmfels; Richter-Gebert 1996).
- Correspondence: non-realizability of a uniform oriented matroid is certified by a final polynomial. Richter-Gebert notes that some non-realizable OMs have no biquadratic final polynomial, so this is only a partial method. Relevant to section 6(A) UNSAT if SAT is inconclusive.
- Sources: https://link.springer.com/article/10.1007/BF02187702 (Richter-Gebert, 1996, the abstract is the one retrieved in the search) ; https://arxiv.org/pdf/0801.2582 (uses the final-polynomial criterion).
- Experiment: take a chirotope from lead 2 that is UNSAT on a restricted sub-instance, and try to find a biquadratic final polynomial with a computer algebra system. Record whether it succeeds.

## 6. Numerical realization search via Bokowski-Hay style optimization (2025)
- Field: polyhedral embeddings of regular maps, numerical optimization.
- Correspondence: Bokowski and Hay (2025, Symmetry 17:622) used a numerical optimization method for genus 2 to 14, and report ten new embeddings and their duals. They treat the Szilassi torus as the dual of the Mobius torus. This is the closest published numerical method to our track 4. ANALOGY where the duality is concerned.
- Sources: https://www.mdpi.com/2073-8994/17/4/622 ; https://tuprints.ulb.tu-darmstadt.de/entities/publicationzv/4a6be59e-b2db-4692-9ddf-196ff16ee856
- Experiment: read the optimization objective in the paper (not retrieved here). Port it to our plane parameters (36 real variables, section 2) with the strict inequalities of Lemma 3.1 turned into a hinge penalty, and run it on the F = 7 control.

## 7. Verified small-instance enumeration of realizable OMs (Miyata-Moriyama-Fukuda; Finschi-Fukuda)
- Field: oriented matroid databases.
- Correspondence: rank 4 on 8 elements is classified for realizability. Our 12-plane OM is on 13 elements, so the database does not cover it. Useful for sub-configurations (e.g., 7 or 8 planes) to validate the code.
- Sources: https://arxiv.org/pdf/1204.0645 (complete enumeration of small realizable OMs)
- Experiment: take the 8-element realizable/non-realizable classification as ground truth and test lead 2's encoder on it.

## 8. dReal (delta-complete SMT) for the strict sign conditions
- Field: nonlinear real arithmetic with certificates.
- Correspondence: the 36 plane parameters with strict determinant inequalities (section 2). dReal returns delta-sat or unsat with certificates. ANALOGY-level: the search did not find any source on orientation predicates in dReal.
- Sources: https://arxiv.org/pdf/1310.8278 (Satisfiability modulo ODEs; background on dReal)
- Experiment: encode the 4x4 determinant signs of 3 planes plus infinity for one forbidden triple, then check whether dReal returns delta-sat on a known-good Szilassi configuration.

## 9. Toroidal polyhedra catalogs and Stewart toroids (outside the Szilassi literature)
- Field: polyhedral toroids (Stewart, Hart, Miraheze wiki).
- Correspondence: the 12-face case is not a Stewart toroid (Stewart toroids need regular faces). The catalog is useful only for finding examples of pairwise-adjacent faces in nonconvex toroidal polyhedra. ANALOGY only.
- Sources: https://en.wikipedia.org/wiki/Szilassi_polyhedron ; https://georgehart.com/virtual-polyhedra/toroidal.html ; https://polytope.miraheze.org/wiki/Toroidal_polytope
- Experiment: none recommended beyond checking Hart's list for any entry where every pair of faces shares an edge.

## 10. Realization-space theory (Mnev universality; matroid stratifications)
- Field: algebraic geometry of matroids.
- Correspondence: a universality theorem says realization spaces of OMs can be arbitrarily complicated. This is a warning: even if SAT finds a chirotope, its realization space may be singular or empty. ANALOGY/warning.
- Sources: https://arxiv.org/pdf/2103.16550 (matroid stratifications and realization spaces) ; https://arxiv.org/pdf/1409.3503 (matroid theory for algebraic geometers)
- Experiment: after a chirotope is found, test whether the rational realization from section 2 is reachable by numerical continuation from a random start; a failure suggests a singular component.

## Not found / limits
- No source found for a Sage or polymake oriented-matroid realization routine for rank 4 on 13 elements. TOPCOM is documented only for triangulation enumeration, not for realization.
- No 2015-2020 paper on final polynomials for uniform rank-4 OMs was found in one search.
- Stewart toroid catalog: not checked for pairwise-adjacent faces.
