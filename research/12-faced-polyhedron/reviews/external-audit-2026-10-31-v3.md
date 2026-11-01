> English translation of the external audit v3 (2026-10-31), originally written in Russian. Section numbers are unchanged.

# Scientific audit of the Polyhedrons project

**Audit date:** 31 October 2026  
**Subject:** `polyhedrons.bundle`, all Git refs present in the bundle.  
**Goal:** to assess mathematical progress, the quality of the evidence base, the research strategy, the publication potential and the next steps.

---

## 0. Summary for the research lead

### Main conclusion

**The project has advanced substantially. It has not solved the original problem, but it is no longer at the stage of blind enumeration and is not marking time.** Over a short series of iterations it has produced:

1. an independently reproduced complete classification of the 59 combinatorial types;
2. a formal reduction of the geometric problem to finite exact predicates on signs of determinants;
3. five exact embedded genus-3 surfaces with 12 planar faces of one combinatorial type, and one more exact genus-3 surface of another type;
4. a computer-certified exclusion of symmetric solutions;
5. a new geometric diagnostic tool based on the degree of the Gauss map, which explained why the earlier genus 3 → 4 ladder systematically broke;
6. a positive control on an independent published eight-faced object from 2026.

This is real research progress. At the same time, **there is as yet no proof of existence or of impossibility of the sought genus-6 object**.

### My recommendation

**It is worth continuing, but the success criterion of the next computational cycles should change.** Do not run still more hours of the same optimizers. First learn to discard quickly not only bad geometry but also normal classes that are clearly unsuitable; then solve the exact problem of plane offsets; in parallel strengthen the proof and software base.

The three most promising branches now are:

- Gauss-gated / normals-first search over several combinatorial chains;
- a local obstruction theory for immersion, not only for full embedding;
- independent verification and/or collaboration with the current SAT project `polyhedraproof`.

**The strongest result already obtained that could stand as a scientific result in its own right** is the theorem on the impossibility of a symmetric realization (and, potentially, the stronger statement on the impossibility of a symmetric polygonal immersion), together with the exhaustive treatment of the 25 symmetry classes and the verified DRAT certificates. But before positioning this as a separate publication, the formulation must be reconciled with the independent Moki–Julio work of 2026, and the certificates themselves must be made available.

---

## 1. What exactly the problem is

The strict target configuration is a closed orientable polygonal surface embedded in \(\mathbb R^3\) with the following properties:

- exactly 12 planar faces;
- each face is a simple polygon;
- each pair of faces has exactly one common edge;
- each edge belongs to exactly two faces;
- exactly three faces meet at each vertex.

It follows that:

\[
F=12,\qquad E=\binom{12}{2}=66,\qquad V=44,
\]

\[
\chi=V-E+F=-10=2-2g,\qquad g=6.
\]

In the dual triangulation this is an orientable triangulation of the genus-6 surface with 12 vertices and complete 1-skeleton \(K_{12}\). Each face of the original object has exactly 11 edges, one for each other face.

**It is critically important not to confuse the strict formulation with the relaxed one:** "every pair of faces touches along at least one edge" allows pairs with two edges. Such objects do not solve the original problem. For example, the two new eight-faced genus-3 objects of 2026 have 20 pairs with one common edge and 8 pairs with two; they are useful control examples, but not solutions of the 12-face problem.

The condition "exactly three faces at a vertex" should be kept in the explicit formulation. It does not follow from the statement of pairwise adjacency of faces alone.

---

## 2. Git state and project organization

Three branches were found in the bundle:

| Branch | HEAD | Role |
|---|---|---|
| `main` | `d4dce69` | site / interactive 3D visualizer |
| `claude/wonderful-carson-saxyck` | `6e5aaad` | early large research branch, numerical and combinatorial experiments |
| `claude/practical-archimedes-e5p1fi` | `1458825` | the most recent research branch, Gauss gate, normals-first, Q1 |

The research branches contain about 150–170 commits; the last branch contains roughly 2,264 added/changed lines relative to the previous research branch and a series of new theoretical and computational directions.

### Important organizational remark

`main` contains only the user-facing part of the project and practically no research material. Therefore a person opening GitHub on the default branch will not see the experiment log, the proofs, the data or the research programme. This explains why one could wrongly conclude from `main` alone that there is almost no research.

**Recommendation:** explicitly declare the research branch the main one for scientific work, or put the research directory in a separate permanent branch/release. It is not necessary to merge it with the site right away, but a clear entry point is needed: `RESEARCH.md`, a list of branches and a stable tag with the frozen state of the experiments.

---

## 3. What can already be considered a reliable foundation

Below I use four levels of evidentiary strength:

- **Theorem / proved:** there is a mathematical argument that can be checked independently.
- **Certified computation:** a mathematical reduction plus a checkable SAT/DRAT/LRAT certificate.
- **Exact witness:** a stored rationalized geometric configuration verified in exact arithmetic.
- **Numerical observation:** useful for the direction of the search, but not a proof.

### 3.1. Classification of the 59 combinatorial types: the foundation is complete

Two different implementations of the enumeration obtained 12,144 labelled orientable solutions and 59 classes up to combinatorial isomorphism. An independent validator then checks each object as a triangulation:

- 44 triangles;
- the complete edge graph \(K_{12}\);
- each edge belongs to two triangles;
- the link of each vertex is a single 11-cycle;
- orientability and \(\chi=-10\);
- the 59 types are pairwise non-isomorphic.

A comparison with two external lists also gives a bijection. In the present audit `check_triangulations.py --selftest` was re-run: all 59 records passed the checks, all 1,711 pairs of classes are distinct, and the tests of random relabelling and mirror reversal passed.

**Status:** a reliable basis for all further research. The combinatorial search is essentially closed; there is no longer any need to "search for topologies" again — what is needed is to decide the geometric realizability of specific types.

Limitation: the classification itself is already known from the literature (Altshuler–Bokowski–Schuchert, 1996). The project's novelty here is independent reproduction, audit, machine-checkable data and a convenient computational base, not the discovery of the number 59.

### 3.2. Face-plane reduction: the central mathematical reduction

For each face \(X\) a plane is given:

\[
H_X=\{p:n_X\cdot p=d_X\}.
\]

The vertex corresponding to a triangle \(XYZ\) of the dual triangulation is the intersection of three planes. The edge between two faces lies on the line of intersection of these planes.

Consequences:

- planarity of the faces holds automatically;
- only the 12 planes are unknown;
- for a fixed combinatorial type the geometric constraints become strict inequalities;
- the space of realizations is open in the parameter space (after removing degenerate configurations);
- therefore the existence of a realization implies the existence of a rational certificate, and after scaling an integer one.

This is a very strong formulation of the problem: instead of optimizing the coordinates of 44 vertices with a large number of equalities, the project optimizes the normals and offsets of 12 planes.

### 3.3. Lemma on forbidden triple intersections: a strong basis for OM-SAT

The project has derived and independently checked a lemma that allows embeddedness to be expressed through 176 triples of faces that are not vertices of the dual triangulation. The idea: three planes meet at a critical point; if this point simultaneously falls in the regions of the three corresponding faces, the surface violates the required pairwise intersection.

The adversarial review accepted the proof of Lemma 5.1 and the predicate `IN` after checking the intermediate cases. An exact comparison with a direct geometric check was carried out, including the case of unsimplified polygonal curves. The log records more than 2.5 million predicate checks with zero discrepancies in the test sample; an independent geometric implementation, Track 4, also showed zero discrepancies on 149 configurations.

**Status:** a strong mathematical and computational basis. For publication I would still move the proof into a separate, carefully written text and ask an external specialist in oriented matroids / polygonal surfaces to check it in full.

### 3.4. Exact geometry verifier: a strong engineering asset

`ladder_exact.py` checks in rational arithmetic the simplicity of the faces, the consistency of the edges, and that the intersection of each pair of faces coincides exactly with the prescribed common edges. `verify_solid.py` extracts the map from a solid-first configuration and carries out this check.

In this audit the following were re-run directly:

- the self-test of the classification of the 59 types;
- the check of the solid-first genus-3 object;
- the independent positive control from the published Röst–Vígh 2026 construction;
- the exact check of the five stored genus-3 realizations of type 0;
- the exact check of the two best genus-4 attempts.

Implementation caveat: the geometric coefficients from the JSON are rounded to integers after scaling by \(10^9\) (in the Gauss module the normals are rounded at \(10^6\)). Hence the certificate is exact for the rationalized configuration that the code actually checks, not for the unbounded original floating-point number. This is a normal and useful scheme, but it must be described explicitly in the paper.

### 3.5. Positive control on the eight-faced object: an important independent check

From the published planes and face cycles of Röst–Vígh the project reconstructed the object and checked it with its own tools:

- \(F=8,V=24,E=36,\chi=-4,g=3\);
- 20 pairs of faces have one common edge each, 8 pairs have two;
- all 8 faces are simple;
- all additional intersections are absent;
- the discrete degree of the Gauss map is \(-2=1-g\);
- the rotation eigenvalues of the faces are equal to +1;
- 20 saddle vertices against a lower bound of 7.

This substantially increases trust in the geometric validator and the Gauss tools on a non-trivial external example. However, it does not confirm the whole OM-SAT encoding and does not settle the 12-face case.

---

## 4. Constructive results: what has actually been built

### 4.1. Five exact genus-3 realizations of type 0

All five stored JSON configurations were checked in exact arithmetic:

| Invariant | Value |
|---|---:|
| Faces | 12 |
| Vertices | 32 |
| Edges | 48 |
| Euler characteristic | −4 |
| Genus | 3 |
| Adjacent pairs of faces | 48 of 66 |
| Simple faces | 12 of 12 |
| Extra intersections | 0 |

These are genuine embedded closed polygonal surfaces of genus 3, not pictures or numerical near-misses.

They have one more useful feature: their combinatorial maps admit a further *topological* attachment of handles towards all 66 pairs. In the project documentation this is denoted by the word `extendable`.

**But `extendable` does not mean that the geometry found can be continuously extended to genus 6.** It only means that the combinatorial chain potentially exists. A geometric extension has not been found yet.

### 4.2. One more genus-3 object of a different combinatorial type

The solid-first search independently found one more exact surface with 12 faces, 32 vertices, 48 edges and 48 adjacent pairs. Its sequence of vertex degrees of the dual graph differs from the type-0 ladder objects, so the maps are not isomorphic.

Thus the repository contains **at least two distinct combinatorial types of exactly embedded 12-faced genus-3 surfaces**; for one type five geometric realizations have been found.

The dual of the regular map R3.2, already known in the literature, has the same numerical parameters \((F,V,E)=(12,32,48)\), but all its faces are octagons; your maps have different degree sequences. This is an argument for their difference from that particular known object, but not a full check of historical novelty.

### 4.3. Genus 4: not found yet

The two best genus-4 attempts were re-checked exactly:

| Candidate | Simple faces | Non-simple faces | Bad face pairs | Embedding |
|---|---:|---:|---:|---|
| `4viol` | 8/12 | 4 | 4 | no |
| `degenerate` | 10/12 | 2 | 2 | no |

This is an important correction to the search statistics: the internal energy counter and the exact verifier count different things. The name `4viol` must not be read as "exactly four geometric defects": the exact check shows four non-simple faces and four pairs with an incorrect intersection.

Genus 4 is not simply genus 3 "pressed a little less far". The cause of the plateau is apparently structural; see the Gauss degree below.

---

## 5. The most important theoretical shift: the Gauss map

For an oriented closed surface the degree of the Gauss map equals

\[
\deg G=\frac{\chi}{2}=1-g.
\]

For a discrete surface the project uses the face normals and the oriented triangles of the dual map. Each handle in the genus ladder must change the required degree class by −1.

The project also uses a necessary condition for covering the sphere by positive spherical triangles: for every generic direction there must exist a positive local normal configuration. From an integral argument over areas a lower bound on the number of saddle triangles follows:

\[
s\ge 2g+1.
\]

An important distinction:

- the degree in a chosen rational generic direction is checked by exact signs of determinants;
- the number of saddle triangles is also computed exactly;
- the covering of the sphere in `gauss_gate.py` is currently checked on a finite set of directions (64 plus an additional confirmation sample), not proved for the whole sphere.

Therefore the current `covering=True` is a strong numerical filter, but by itself **is not an exact proof of global covering**. For that one needs an exact check of a spherical marking/partition or a separate combinatorial argument.

### 5.1. Why genus 3 → 4 broke

For the five stored type-0 realizations the Gauss degree itself equals −2, as it should be for genus 3. For the next genus level 4, −3 is needed. The analysis of each next handle showed that the handle being added gives, in these fixed configurations, the contribution \(k_\tau=0\), although −1 is required.

Consequently, for these seed configurations the passage to the next level is impossible if the normals are kept in the same admissible class and no degeneration is passed through. Attempts at local improvement of the geometry with an unchanged set of normals cannot repair a wrong degree.

This explains why SA, CMA-ES, LNS, degeneracy penalties and drift in the offsets all ran into similar defects. They optimized inside a region from which the next level is unreachable without changing the normal class.

**Scope of applicability:** this is not a proof of the impossibility of genus 4 for type 0 in general, still less a proof of the impossibility of genus 6. It excludes a specific continuation path from the genus-3 seeds found, under the stated normal/continuity constraints.

### 5.2. The new experiment Q1

For type 58 the search found, in 447 seconds, one system of 12 normals for which all seven levels of the chain lie in the required degree classes:

\[
(1,0,-1,-2,-3,-4,-5).
\]

All seven class-checks passed the exact check. But then the exact SMT problem for the plane offsets of the lowest level, the genus-0 sphere, turned out to be `UNSAT` in 32.7 seconds.

This is a good result, because it separates two conditions:

1. the normals can lie in the right Gauss class along the whole ladder;
2. this still does not guarantee that plane offsets exist that close up simple faces even at the lowest level.

The `UNSAT` applies only to the set of normals found, the chosen gauge and the given subgraph. It **does not exclude** other normal systems for type 58.

### 5.3. General assessment of the Gauss approach

This is the most promising new tool of the project. It explains the structural causes of the failures of the old searches and creates a cheap prefilter before the expensive exact SMT.

But the current implementation has a rigor boundary: the degree and the saddle count are exact, global covering is not. The next step must strengthen this part, not disguise a sampled check as a proof.

---

## 6. What is excluded, what remains open

### 6.1. Symmetric realizations are excluded

The project went through 25 possible classes of non-trivial symmetry (21 cases with an involution of type C2 and 4 cases with symmetry of order 3). The overnight computation logs record `UNSAT-VERIFIED` for all cases: CaDiCaL built a DRAT proof, and `drat-trim` checked the certificates. The external Moki–Julio work of 2026 states the same conclusion: a 12-faced object cannot have non-trivial symmetry; the asymmetric case remains open.

The project has an even stronger computational result: the exclusion of a symmetric polygonal immersion (without the global conditions of full embedding), by the local conditions of simplicity of faces, a bound on the number of reflex angles, and orientational consistency. If the mathematical premises of the encoding are correct, this is stronger than a simple prohibition of a symmetric embedding.

However, the chain of evidence must be recorded carefully:

- DRAT proves UNSAT of a specific CNF;
- the passage from the CNF to the geometric statement requires a separate proof of correctness of the encoding;
- the logs contain `cnf_sha256`, `proof_sha256` and `DRAT-VERIFIED` lines;
- large `.drat` files are excluded from Git via `.gitignore` and are absent from the attached bundle.

Therefore on the basis of the bundle one can check the reporting, the hashes and the status, but cannot re-run the check of all the raw certificates without access to the results archive / the machine where they are stored. For publication the certificates or a long-term proof archive must be published together with the CNF hashes and a reproduction instruction.

### 6.2. The asymmetric case remains open

This is now the central part of the problem. The full OM-SAT for asymmetric maps is not yet closed. The logs contain timeouts, for example the first 8 asymmetric types were not solved in 2.17 hours each. This is not `UNSAT` and not evidence of impossibility; it is only insufficient computing power / a weak encoding at this stage.

The project does not yet have a proof that none of the 59 maps is realizable. There is also no genus-6 candidate.

### 6.3. Summary of statuses

| Direction | Status | What can be claimed |
|---|---|---|
| Classification of topologies | <strong>Closed</strong> | 59 types reproduced and verified |
| Face-plane reduction | <strong>Strong basis</strong> | correct reduction, needs a final external proof review |
| Lemma 5.1 and `IN` | <strong>Verified</strong> | proof accepted by adversarial review, exact tests found no counterexamples |
| Exact geometric validator | <strong>Working foundation</strong> | several independent objects pass exact verification |
| Symmetric case | <strong>Certified UNSAT</strong> | no non-trivially symmetric solution within the proved coverage of cases |
| Asymmetric immersion | <strong>Open</strong> | timeouts are not an answer |
| Full genus 6 | <strong>Open</strong> | neither a construction nor a proof of impossibility exists |
| Genus 3, 12 faces | <strong>Exact witnesses exist</strong> | at least two combinatorial types, 48/66 adjacencies |
| Transition type 0, g=3 → 4 | <strong>Locally blocked by the Gauss class</strong> | the specific seeds/normals do not continue directly |
| Type 58 normals-first Q1 | <strong>Partial success</strong> | the right chain of degrees was found, but the fixed normals do not give even a sphere |
| Torus period defect | <strong>Not promising now</strong> | a zero period was found, but the surfaces are not simple; the full problem is not solved |

---

## 7. Comparison with current world work

### 7.1. Classical base

- Altshuler, Bokowski, Schuchert (1996): 59 orientable neighborly triangulations of genus 6 with 12 vertices.
- Schewe (2010): proved the impossibility of a geometric realization of the *vertex dual problem* (12 vertices, all pairs joined by an edge) using oriented matroids and SAT.

**Do not transfer Schewe's theorem to your problem by duality.** Embeddedness of spatial polygonal surfaces is not preserved under the simple dual passage: the face-plane problem and the vertex realization impose different conditions.

### 7.2. Bokowski–H. (2025): a numerical search over all 59 types

In the paper *Polyhedral Embeddings of Triangular Regular Maps of Genus g, 2 ≤ g ≤ 14, and Neighborly Spatial Polyhedra* the authors apply optimization to polyhedral embeddings and to dual objects. For 12 hendecagonal faces they report that they found an embedding for none of the 59 types. This is an independent negative numerical result, but not a proof of impossibility.

Their numerical approach is close in spirit to the early branches of the project: random/cluster starts, optimization of intersections, then improvement of the geometric quality and distances. They also note that the examples they managed to find often had symmetry. This explains why symmetric Ansätze were a natural first target, but after their exclusion one must search systematically in the asymmetric setting.

### 7.3. Moki–Julio (2026): the symmetry prohibition

Their public repository describes a computer-assisted theorem with 36 SAT instances and checkable DRAT certificates: there is no symmetric 12-faced object; the asymmetric case is not solved.

Your project independently reproduces the symmetric exclusion with its own encoding. This is valuable, especially if it can be proved/shown that the local exclusion of immersion is indeed stronger than the geometric prohibition of embedding. But for publication one must distinguish the genuinely new mathematical part from an independent replication of an already published computer-assisted result.

### 7.4. Pirozhkov: the most important current computational peer project

`pirozhkov-andrei/polyhedraproof` is another current project on exactly the problem of 12 pairwise adjacent faces. It translates the problem into 59 Boolean formulas and builds a pipeline for independently checkable refutations via cube-and-conquer and LRAT.

As of the published status:

- each formula has 5,257 variables and 52,177 constraints;
- proof checking is performed by a separate `cake_lpr`;
- there are two independent certifiers, hash control, containers with pinned tool versions, CI, tests and logging;
- a pilot on two formulas closed 31,187 leaves with checked LRAT proofs in 648.5 core-hours;
- the full campaign over all 59 formulas has not been carried out; the estimate of the order of 19,000 core-hours is an extrapolation from two formulas, not an actual measurement of the full problem.

This is a very useful benchmark for the level of engineering of provable computation. I would not advise blindly duplicating their full 19k-core-hour cube-and-conquer run. It is better to compare the mathematical reductions and encodings, find independent control theorems/strengthenings, and propose a cross-check or a joint audit. One cannot assume that their formula is equivalent to your OM-SAT without matching the exact variables, premises and soundness clauses.

### 7.5. New eight-faced objects of 2026

Ruslan Mizhaev (15 September 2026) and Gergely Röst–Viktor Vígh (26 September 2026) published two combinatorially different genus-3 objects with eight simple planar nonagonal faces. In each case all pairs of faces are adjacent, but eight pairs have two common edges, so these examples are not strict pairwise-one-edge objects.

Their value for you:

- they are fresh exact geometric positive controls;
- they show that new polyhedral surfaces of genus 3 are still being found;
- Röst–Vígh describe a computational geometric search and demonstrate the recovery of the object from planes;
- your `control_rost_vigh.py` has already successfully verified the published object.

This is a good path to testing the ladder with multiple adjacencies, but before transferring the Gauss gate and SAT there, the code must explicitly account for repeated edges of a pair of faces. The current `gauss_degree`/`gauss_gate` part in a number of functions assumes a simple dual map; in the literature TODO this gap is already noted.

---

## 8. Which results can already be shown to colleagues

### Can be shown with confidence now

**A. Two exactly embedded genus-3 types with 12 faces.**  
This is a vivid and checkable result. But before claiming novelty, a full comparison with the catalogues of known polyhedral maps and with the published R3.2 construction must be carried out.

**B. An independent exact realization of the known Röst–Vígh object.**  
Not an independent discovery of the geometry, but a good evidence package confirming that the verification core works on a genuinely new object with multiple adjacencies.

**C. An independent full check of the 59 combinatorial types.**  
More a computational artifact / replication of a known classification than a new mathematical result. But it is an important foundation and can be useful as an open dataset and test set.

**D. A Gauss-degree explanation of the genus 3 → 4 barrier for the stored type-0 seeds.**  
This is possibly the most interesting internal theoretical story: the specific failures of the optimizer turned out to be a consequence of a wrong topological class of normals. To make this a publishable result, one must formulate an exact theorem with its conditions and a proof of invariance, and then extend the analysis beyond the five seeds.

### A potentially strong result after minimal further work

**E. The prohibition of a symmetric polygonal immersion.**  
If the proof of the local constraints and the completeness of the symmetry enumeration are written up rigorously, this can become a separate statement stronger than "there is no symmetric embedding". One must check whether this result is already covered by the stronger formulation of Moki–Julio, then obtain the raw DRAT certificates and an external review.

### What cannot be claimed yet

- "We proved that the 12-faced polyhedron does not exist": no.
- "We have almost found genus 6": no; genus 3 with 48/66 is not an "almost finished" object, since the missing pairs are not a small local cosmetic defect.
- "The right Gauss degree means that a realization exists": no; Q1 showed the opposite directly.
- "Covering of the sphere is proved by the exact Gauss gate": no; covering is currently tested on a finite set of directions.
- "None of the 59 types is realizable": no, the asymmetric case remains open.

---

## 9. Critique of the research process: strengths and gaps

### What is organized well

1. **Parallel research tracks.** Combinatorics, geometry, oriented matroids/SAT, theory, literature and adversarial verification are not mixed into one opaque task.
2. **Hypotheses are fixed explicitly.** There are a sprint board, a stop list, an experiment log, review prompts and decisions on which directions to stop.
3. **There are control objects.** The Szilassi polyhedron is used as a positive control for n=7; the new Röst–Vígh object as an independent control for eight faces and double adjacencies.
4. **An exact internal verification loop.** A candidate is not considered an achievement by a single float-energy metric.
5. **Adversarial review.** A separate agent checked the lemmas and predicates, and did not only generate code.
6. **Negative results are preserved.** The project has a stop list, logs of failed runs and an explanation of why some approaches should no longer be scaled up.

This corresponds to the spirit of modern reproducible computational research practices: code and data must allow a third party to verify the conclusion independently, and the environment, versions and provenance must be part of the result. See The Turing Way and the Computing Handbook of the Kempner Institute.

### What needs improvement

**1. There is no fixed computational environment.**  
The bundle has no `pyproject.toml`, dependency lockfile, Dockerfile, Makefile or CI workflow. `HOW_TO_RUN_OVERNIGHT.md` suggests installing `numpy scipy numba python-sat z3-solver sympy`, but the versions are not pinned. For a scientific computation this is a serious gap: solver/version drift can change performance, behaviour and, in rare cases, reproducibility.

**2. There is no universal end-to-end reproduction command.**  
There are scripts for individual tasks, but no single command that checks the data, runs short positive/negative controls, checks the hashes, recomputes the key tables and assembles the final evidence report.

**3. The raw proof certificates are not in the bundle.**  
The JSONL contains their SHA-256 and verification marks, but not the `.drat` files themselves. For a long-term scientific result the certificates must be stored in Zenodo/another archive or in a repository release with control hashes.

**4. Run provenance is incomplete and non-uniform.**  
For each run a single minimum must be recorded: commit SHA, source hash, canonical map ID, seed, all parameters, objective-function version, versions of solvers and libraries, OS/CPU, wall time, core time, exit status, input/output hash, exact verifier result, and the reason for stopping.

**5. Inconsistency of documentation.**  
`literature-review.md` still says that the primary papers were not read and that sites were blocked; the later `TODO_world_research_2026.md` says that arXiv was already available and the new materials were read. These documents must be merged into a single current literature matrix with the date, the primary source, the reading status and the accuracy of the claims.

**6. The terminology of defects needs normalization.**  
Currently there are violation events, local defects, nonsimple faces, bad face pairs, class defects and exact embedding errors. They cannot be folded into a single `violations` counter. A formal schema for each metric is needed.

**7. Minor technical failures of interfaces.**  
`ladder_exact.py` in its CLI reads a list of records and indexes it, while some stored genus-ladder examples are single JSON objects with `planes`/`triangles`. One can call the API by hand after obtaining the links, but the public CLI is not universal. A single `verify_candidate.py` is needed that accepts a normalized JSON of any supported type.

**8. LLMs/subagents do not replace independent expertise.**  
The roles "generator, critic, adversarial verifier" are useful for covering the space of ideas. However, three agents working on the same source code and with similar premises are not three independent scientific referees. Before a theorem-level publication a human mathematical review outside the current chain of agents is needed, especially for Lemma 5.1, the global Gauss criteria and SAT soundness.

---

## 10. What to stop and what to keep

### Stop or sharply limit

- New large runs of black-box SA/CMA/GA on the old violation function without a structural filter. It is already known that the best near-miss seeds do not pass the Gauss prefilter and are locally far even from an immersion.
- Attempts to continue precisely the five old type-0 genus-3 configurations towards genus 4 with the same normals. The Gauss class already shows why this path is blocked.
- Torus-period relaxation as the main route. A zero period defect was obtained on configurations with non-simple faces; after adding simplicity the problem turned out to be infeasible for the examples checked.
- Increasing weights/thresholds/iterations on the old objective function if the experiment does not change the mathematical hypothesis or the admissible space.

### Continue

- Generate new systems of normals under the Gauss degree on several different combinatorial ladders, not only around one old seed.
- After each set of normals, immediately solve exact offset feasibility, starting from the lowest level; do not spend time lifting the chain if M0 is not realizable.
- Use the local immersion model. If for some type it is proved that even an immersion with simple faces is impossible, embeddedness is excluded automatically. This may give cheaper UNSAT instances.
- Continue the analysis of handle-local invariants: \(k_\tau\), admissible gauges, saddle count, turning numbers, hemisphere margin. Record each of them separately.
- Keep solid-first as a source of new partial embeddings and independent genus-3 topologies, but assess it as a separate generator, not as a direct route to genus 6.

---

## 11. Recommended programme of next experiments

### Phase 0. Freeze the formal statement

Create a single `SPEC.md` with:

- the strict target and all local conditions;
- a separate description of the relaxed formulations with multiple common edges;
- allowed/forbidden degeneracies;
- a convention on orientability, face simplicity and general position;
- definitions of all counters and evidentiary statuses.

**Result of the phase:** no ambiguity about what exactly counts as a solution.

### Phase 1. Strengthen reproducibility

Minimal plan:

- `pyproject.toml` or a lockfile with exact versions of the Python libraries;
- a Docker/Apptainer image with pinned SAT/SMT solvers and checkers;
- CI: selftest of 59 maps, Szilassi positive control, Röst–Vígh positive control, genus-3 exact witnesses, negative mutants;
- one command `make verify-all` / `python -m polyhedrons.verify_all`;
- a manifest for each result with hashes, commit SHA, seed, parameters and versions;
- publication of the DRAT files and/or LRAT, if size allows, or a link to an archive with hashes.

This is not bureaucracy: it will reduce the risk of repeating expensive computations and make the result fit for third-party audit.

### Phase 2. Normals first, offsets right after

The current Q1 must be developed into a mass experiment:

1. For several types (58, 0, 11, then the types with the best combinatorial chain properties) generate many diverse chain-consistent normal sets.
2. For each set check the exact degrees by level and the exact saddle counts.
3. For now mark global covering as sampled unless/until an exact proof exists.
4. Immediately after generation solve the M0 exact offsets SMT.
5. If M0 is SAT, save the exact surface and go to M1; if UNSAT, record the first impossible level.
6. Repeat many times on different normals to obtain statistics, not a single case.

**The main new signal:** not only "did we find admissible normals", but "what fraction of Gauss-admissible normal sets manage to pass the exact offset stage, and where does the first UNSAT most often appear".

An important recommendation: add the conditions of sphere closure / period equations and face simplicity to the outer-normal search, so as not to generate normals that are already known to be incompatible with M0.

### Phase 3. Work out the local immersion theory

This direction can potentially turn computational observations into short theorems.

- Formalize the constraint "at most one reflex corner per vertex" and prove it for a polygonal immersion with degree-3 vertices.
- Derive local consequences for each 11-gon and for pairs of adjacent faces.
- Investigate parity/crossing-count constraints; do not call them theorems until there is a complete proof.
- Collect minimal UNSAT cores for the symmetric instances; look for human-readable geometric lemmas explaining the conflict.
- Try a face-by-face decomposition by rank-3 contractions, as sketched in the proof roadmap.

If asymmetric immersion is UNSAT for even a significant part of the types, this may considerably narrow the global problem.

### Phase 4. Compare the SAT approaches and agree on independent verification

Contact the authors of `polyhedraproof` with a concrete proposal:

- compare the reduction to 59 formulas with your 715-sign OM-SAT and the face-plane chirotope encoding;
- check which of your local clauses/lemmas are already included in their formulas;
- provide one or two independently cross-checked reference map instances;
- exchange soundness checks, not only runtimes;
- jointly define a small challenge set: a pair of symmetric UNSAT cases, one asymmetric hard instance, the Szilassi positive control and the Röst–Vígh doubled-edge control.

Do not launch hundreds of core-hours until it is clear what specifically new data this run will give compared with the already published pilot.

### Phase 5. Control experiments on 8 faces

The eight-faced genus-3 objects give a good intermediate benchmark, but double adjacencies must be supported as a separate combinatorial type: the dual map is a multigraph, not a simple graph.

Before transferring the Gauss machinery to this setting one needs to:

- implement corner-based orientation with repeated neighbours;
- check degree = −2 on both published eight-faced examples;
- include Mizhaev as a second positive control;
- check the genus-2 rung of your n=8 search and determine whether its plateau is caused by a wrong Gauss class.

---

## 12. A possible publication strategy

I would not try to pack all results into one paper on the "discovery of a 12-faced polyhedron". That has not been achieved yet.

Two independent lines are more realistic:

### Line A: computational geometry / reproducibility note

Possible content:

- the exact face-plane formulation;
- Lemma 5.1 and the chirotope predicates;
- a checkable enumeration of the 59 maps;
- the exact verifier and the test corpus;
- exact genus-3 constructions and the control on Röst–Vígh;
- Gauss-degree diagnostics for the genus ladder.

It makes sense to submit this paper after an external review and a thorough novelty check of the genus-3 maps.

### Line B: computer-assisted theorem on symmetry / immersion

Possible content:

- a complete classification of admissible symmetry groups;
- the reduction to 25 cases;
- local geometric conditions of immersion;
- an independent SAT encoding;
- complete DRAT certificates and an independent checker;
- human-readable minimal cores, if they can be obtained.

Here the overlap with Moki–Julio 2026 must be checked especially carefully, separating the own stronger result from replication.

### What must precede publication

1. An external mathematical review of the lemmas and of all passages from geometry to SAT.
2. Availability of the raw certificates and complete reproduction instructions.
3. A systematic priority search through the known genus-3 maps.
4. An explicit boundary of the claims: computer-assisted theorem vs numerical evidence vs exact witness.

---

## 13. Overall assessment of progress

| Dimension | Assessment | Comment |
|---|---|---|
| Statement and combinatorial reduction | Very good | the problem is clearly reduced to 59 topologies |
| Mathematical theory | Good progress | there is a strong face-plane/OM reduction and a new Gauss diagnostic; external checking is needed |
| Geometric constructions | Good | exact genus-3 objects obtained, but target genus 6 is far away |
| Computational methods | Greatly improved | the transition from black-box optimization to exact filters and SMT is right |
| Proof infrastructure | Average | DRAT statuses exist, but the certificates are not included; no pinned environment and no CI |
| Literature integration | Average | new works found, but documents are partly outdated; a single literature ledger is needed |
| Publication readiness | Partial | there is material for a technical/preprint result, but an external review and a systematic novelty check are needed |
| Chance of solving the original problem | Not estimated | there is no honest quantitative estimate of the probability at present |

### Final verdict

**Continue: yes. Continue in the same way: no.**

The project already has substantive results that do not disappear even if a genus-6 object does not exist. The most important achievement of recent days is the understanding that the previous genus-4 plateau was not just a lack of computing power: the search scheme was falling into a wrong class of normals. This is a qualitative scientific shift.

But now the discipline of the next level is required: every large experiment must test a specific hypothesis, have a success/refutation criterion formulated in advance, and end with an exact witness or a correctly bounded negative conclusion.

I would allocate the nearest research budget not to yet another long "genus-6 search", but to:

1. closing the reproducibility gaps;
2. a mass Q1 normals-first + exact offsets with several types and many seeds;
3. local immersion obstructions and minimal UNSAT cores;
4. an independent comparison with `polyhedraproof` and an external mathematical review.

After these stages one can make a meaningful decision: go for a cluster SAT-proof campaign, change the class of geometric Ansätze, or publish a separate intermediate result.

---

## 14. External sources and reference points

1. A. Altshuler, J. Bokowski, P. Schuchert, *Neighborly 2-manifolds with 12 vertices*, J. Combin. Theory Ser. A 75 (1996), 148–162.
2. L. Schewe, *Nonrealizable Minimal Vertex Triangulations of Surfaces*, Discrete & Computational Geometry 43 (2010); arXiv:0801.2582.
3. J. Bokowski, Kevin H., *Polyhedral Embeddings of Triangular Regular Maps of Genus g, 2 ≤ g ≤ 14, and Neighborly Spatial Polyhedra*, Symmetry 17(4) (2025), 622. https://doi.org/10.3390/sym17040622
4. Moki & Julio, *Szilassi polyhedra: two computer-assisted theorems*, project repository and certificates (2026): https://github.com/Hashirama1337s/szilassi-12 ; DOI: https://doi.org/10.5281/zenodo.23003257
5. A. Pirozhkov, *Twelve pairwise adjacent faces: a reduction to 59 SAT formulas and a pipeline for independently checkable refutations*: https://github.com/pirozhkov-andrei/polyhedraproof
6. R. Mizhaev, *Integer Realization of an Equivelar Octahedron of Genus 3*, arXiv:2609.17700 (2026): https://arxiv.org/abs/2609.17700
7. G. Röst, V. Vígh, *A second eight-faced polyhedron in which every two faces share an edge* (2026): https://zenodo.org/records/23027039
8. The Turing Way, *Guide for Reproducible Research* and *Reproducible Environments*: https://book.the-turing-way.org/reproducible-research/reproducible-research/ ; https://book.the-turing-way.org/reproducible-research/renv/
9. Kempner Institute, Harvard, *Reproducible Research*: https://handbook.eng.kempnerinstitute.harvard.edu/s2_swe_for_research/reproducible_research.html



---

# Addendum to the audit after discussion with the project author

**Date of the addendum:** 31 October 2026  
**Purpose:** to clarify the interpretation of the genus-3 constructions, to fix the Q1 conclusion, to record a research strategy prioritizing a mathematically meaningful search, and to design the computational infrastructure on GitHub Actions.

## 15. Are the genus-3 surfaces found new objects of Mizhaev type?

### 15.1. No: in their current form these are not Mizhaev polyhedra

Ruslan Mizhaev's work describes a genus-3 surface with **8** simple planar nonagonal faces. Every pair of the eight faces has at least one common edge: 20 pairs have one edge each, and 8 pairs have two collinear edges. This is precisely an eight-faced pairwise-adjacent object (with the caveat about multiple adjacencies), and not merely a genus-3 surface with several adjacent faces. The work: https://arxiv.org/abs/2609.17700.

The Polyhedrons project has a different construction:

- 12 faces, not 8;
- 32 vertices and 48 edges;
- 48 of the 66 possible pairs of faces have a common edge;
- 18 pairs of faces are not yet adjacent.

Therefore these objects cannot be called new "Mizhaev polyhedra", new 12-faced neighborly polyhedra, or solutions of the original problem. For the strict target property 18 adjacencies are missing.

### 15.2. But `type0_genus3_extendable` is not a random intermediate object

It is important here to distinguish two families that were merged too generally in the early summary.

**Family A: `genus_ladder/type0_genus3_extendable*.json`.** These are exact embeddings of one and the same combinatorial type of genus 3. For it the routine `reach()` finds reachability of all 66 adjacency pairs by a sequence of three handle additions. In other words, its abstract map is a genuine intermediate level of one of the combinatorial chains leading to the genus-6 target map. In the project log this is noted separately as the first genus-3 object that is not a combinatorial dead end.

This is substantially stronger than "found a beautiful surface with 48 adjacencies": a geometrically correct realization has been built of precisely the map that can be topologically continued to the target combinatorial map.

**However, the geometric continuation has not been found.** The combinatorial addition of three handles does not prove that the specific embedding in `R^3` can be continued while preserving face simplicity and the absence of intersections. Moreover, the Gauss-degree analysis found shows an obstruction to the direct continuation of the stored configurations with fixed normals.

The five stored JSON files are five geometric configurations/variants of one and the same abstract map, not five new combinatorial types. The polished version is also a variant of the original realization; the number of files must not be passed off as the number of provably inequivalent geometric objects.

**Family B: `solid_first/genus3_12faces_48pairs*.json`.** This is a separate exactly verified embedding of genus 3, with a different combinatorial map. But `handle_add.py`/`reach()` classes such solid-first maps as dead ends: for this object the reachable number of adjacencies does not reach 66 (the overnight report gives a maximum of 54 for genus-3 solid-first maps). Therefore its value for a direct solution of the original problem is lower. It is still useful as an independent test object for the geometric validator, the solid-first search and the analysis of obstructions.

### 15.3. Independent value of these objects

Family A has four concrete uses:

1. **A geometric anchor point for the target combinatorics.** This is an exact embedded base case known to the project on the way to genus 6. The question can now be formulated not as a search from scratch but as a search for an admissible geometric transition through the next handle.
2. **A positive benchmark.** The configurations test the face-plane construction, exact arithmetic, face simplicity, the absence of extra intersections, the computation of the Gauss degree and the extraction of the map.
3. **A laboratory of the realization space.** Several geometric variants of one map provide material for studying chirotope chambers, degeneracies, the connectivity of the realization space and possible transitions between chambers.
4. **A control problem for new methods.** Any new search system must be able to re-obtain, or at least exactly verify, this object before being applied to the much harder genus-6 case.

For Family B the main usefulness at present is methodological: a positive exact-embedding test and an example of how a geometrically correct object can turn out to be a combinatorial dead end relative to a specific target property.

**Novelty:** the current check shows that these maps differ from the specific known regular map, the Dyck map `{8,3}` (which has 12 octagonal faces), and from the published eight-faced objects of Mizhaev and Röst–Vígh. But this does not yet mean that they are new combinatorial maps or the first geometric realizations of this kind. The literature also contains other abstract genus-3 maps with 12 octagonal faces, including irregular variants. A separate check of the map catalogues and of the geometric realizations is needed before claiming priority.

## 16. Q1: the fixed scientific conclusion

The Q1 experiment should be regarded as one of the central results of the last research cycle, not simply as a failed solver run.

For type 58 a system of 12 normals was found that passes the exact checks of the required sequence of Gauss-map degrees at all levels:

\[
(D_0,D_1,\ldots,D_6)=(1,0,-1,-2,-3,-4,-5).
\]

But after fixing this system of normals the exact SMT problem for the plane offsets of the lowest level, the genus-0 sphere, turned out to be `UNSAT`.

### 16.1. What the experiment actually established

It refutes the stronger hypothesis:

> "If a set of normals passes all Gauss-degree checks, then plane offsets can be chosen that realize the required surface."

This hypothesis is false: passing the Gauss-degree gate does not guarantee even the existence of the base spherical geometry for the chosen set of normals.

It follows that the Gauss degree is a necessary filter but not a sufficient condition. Between the normals and the offsets there is a further compatibility layer, which must take into account at least the closing of faces, the existence of correct face regions, the simplicity of the polygons and the absence of unwanted intersections.

### 16.2. What the experiment did not establish

The `UNSAT` applies to one system of normals found for type 58, a specific gauge and a specific encoded offset problem. It does not prove:

- the impossibility of all systems of normals of type 58;
- the impossibility of a genus-0 base realization for all maps;
- the impossibility of genus 6;
- the insufficiency of the Gauss map as a mathematical method in general.

Before further scaling of Q1 one must obtain a minimal UNSAT core (if the solver supports it for this formula), verify it independently, and try to translate the conflict into a geometric condition understandable without Z3.

### 16.3. The next right question

Not "how many more normals must be generated at random?", but:

> What additional invariants of a normal configuration, besides the degree of the Gauss map, are necessary for the existence of a compatible system of offsets already on the sphere?

This is the substantive scientific output of Q1. The next experiment must either reveal a compact additional condition or show that offset feasibility depends strongly on the specific chamber of the normals. A large random enumeration without analysis of the UNSAT cause is not a priority.

## 17. Updated strategy: search informative regions, not the whole space

The project author explicitly chooses a resource-conscious research strategy: one laptop cannot exhaustively enumerate the whole space of geometric variants, so the project's advantage must lie not in the number of CPU-hours but in the choice of rare, mathematically motivated search regions.

This becomes the main principle of the further programme:

**First theory and a cheap filter → then an experiment with high discriminating power → then an exact solver → then generalization of the result into a lemma.**

Every expensive run must be justified by the fact that its outcome discriminates between competing hypotheses. Before the run the following are fixed:

- the mathematical hypothesis;
- which results will confirm or refute it;
- why this particular type / chamber of normals / class of configurations was chosen;
- a minimal pilot that can quickly expose an error in the idea;
- a stopping criterion;
- what will be extracted from `SAT`, `UNSAT`, a timeout and a near-miss found.

A timeout must not be recorded as a negative mathematical result; an `UNSAT` must not be generalized beyond its exact formula; a beautiful near-miss does not count as progress without a check of degeneracies.

### 17.1. Transfer of methods from neighbouring fields

I propose not to spread thin over dozens of exotic ideas, but to test four interdisciplinary transfers.

**A. Configuration-space planning from robotics.**

The space of geometric realizations can be regarded as a configuration space: admissible configurations form the free region, while zero edge length, touching/intersection of faces and loss of simplicity are obstacles/boundaries. Instead of a local descent on a single energy function one can study the structure of the admissible regions and the transitions between them by the methods of motion planning, roadmaps and continuation. The question becomes: do genus-3 and potential genus-4 realizations lie in one component of the admissible space, or does the transition require crossing the discriminant set?

The check should be small at first: build a path/roadmap only in the realization space of one genus-3 map and see which geometric properties are preserved. One should not assume in advance that RRT/PRM will automatically solve the problem: this is a candidate method for studying connectivity, not a ready solution.

**B. Oriented matroids and arrangement chambers.**

The normals/coefficients of the planes divide the space into chambers in which the set of signs of the determinants (the chirotope) is constant. The five variants found of one type-0 map are material for studying which chambers actually realize this map. Instead of uniform random sampling of coordinates one can look for neighbouring chambers, transitions across a single degenerate hypersurface, and invariants that forbid entire families of chambers.

**C. Proof mining from UNSAT cores and SAT certificates.**

Use SAT/SMT not only as an "answer machine" but as a tool for discovering lemmas. Extract minimal or small conflicting sets of constraints, translate them into geometric statements, look for a common cause for several maps and then prove this cause independently of the solver. The goal is to replace thousands of specific enumerated variants by one compact lemma.

**D. Rigidity theory / stress methods.**

Study the constraint matrices and ranks for the system of planes, vertices and closure conditions. A possible path is to detect an unavoidable linear dependence ("stress") or rank deficiency that prevents closure, orientation and simplicity from holding simultaneously. This is a potential way to derive a fast necessary condition before running the nonlinear SMT.

These transfers are ranked by closeness to the available data: first B and C (since the project already has chirotope/SAT/SMT artifacts), then A and D as newer theoretical-algorithmic directions.

### 17.2. How to choose experiments

It is proposed to score each next experiment on five criteria from 0 to 2:

1. **Theoretical motivation:** is there a derivation from a lemma/invariant, and not only intuition?
2. **Discriminating power:** do different outcomes really change the research programme?
3. **Cheap falsification test:** can the idea be quickly refuted on a small example?
4. **Generalization potential:** can the result become a lemma for many types?
5. **Reproducibility:** will the result be exact, archivable and repeatable?

Do not run an expensive experiment with a low score on theoretical motivation and discriminating power, even if it is easy to parallelize.

## 18. One priority result for the first AI-assisted research note

As the first compact result for deep analysis with the help of AI I choose neither the symmetric UNSAT (it already has a close independent publication) nor the single Q1 `UNSAT` (by itself it is still too narrow), but:

> **An exact genus-3 realization of type `type0`, combinatorially extendable to one of the target neighborly genus-6 maps.**

This is the clearest positive result: there is a geometric witness, an exact verifier, a known combinatorial map and a checkable sequence of handles that brings it to 66 adjacencies.

### 18.1. Preliminary formulation of the result

There exists a closed orientable polygonal surface of genus 3 in \(\mathbb R^3\), consisting of 12 simple planar faces, with 32 vertices and 48 edges, in which 48 pairs of faces have exactly one common edge each. Its combinatorial map admits an extension by three handle attachments to the target genus-6 map with 66 adjacencies.

This is **not** yet a statement about geometric continuation and **not** a claim of a new Mizhaev polyhedron. The term "new" can be used only after checking the novelty of the map and of the geometric realization against the catalogues and the literature.

### 18.2. Why this result is suitable for the first AI audit

- It has a bounded, self-contained set of source files.
- The mathematical statement is positive and does not depend on the interpretation of long optimization runs.
- An independent checker can be built without relying on a single author script.
- The combinatorial part can be checked by canonicalizing the map and an explicit list of the three handles added.
- Novelty can be investigated separately from correctness: first prove the object, then compare with the known maps.

### 18.3. Task for the AI agent

1. Take `type0_genus3_extendable.json` and its four variants; do not read only the overview READMEs.
2. Independently reconstruct the cyclic traversals of the 12 faces and the exact rational coordinates of all vertices from the rationalized planes.
3. With a second implementation check closedness, orientability, simplicity of all faces, exactly the prescribed pairwise intersections, absence of self-intersections and \(\chi=-4\).
4. Canonicalize the abstract map; check that all stored variants belong to one map type, and do not present them as different combinatorial types.
5. Independently check `reach=66` and write out exactly the three handle attachments leading to the target map.
6. Compare the map with known genus-3 maps, including the Dyck map `{8,3}` and irregular maps from catalogues; separately look for known geometric realizations in \(\mathbb R^3\).
7. Produce a short referee-style dossier: the exact theorem, the complete set of certificates, a novelty assessment, the limitations of the claim and a list of questions for an external mathematician.

**Success criterion:** not "the AI wrote a paper", but an independent, compact and checkable package has been obtained, on the basis of which a mathematician can assess correctness and novelty in a short time.

## 19. GitHub Actions as a computational laboratory

The idea of running each experiment in a separate branch as a computational workflow is technically feasible. GitHub Actions does not restrict a workflow to tests only: `run:` can launch Python, C++, SAT/SMT solvers and any other permitted computational programs.

For a public repository the standard GitHub-hosted runners are free; the current GitHub documentation states that for public repositories standard runners are available free of charge and without a monthly minutes limit. For the public `ubuntu-latest` a runner with 4 CPUs, 16 GB RAM and 14 GB SSD is currently declared. This can give noticeably more parallel CPU than one laptop, although it is not an HPC cluster and the resources of a single job are limited.

### 19.1. Practical limits as of 31 October 2026

| Limit | Current value | Meaning for the project |
|---|---:|---|
| Maximum duration of one GitHub-hosted job | 6 hours | A long search must be done with checkpoint/resume or split into stages |
| Maximum duration of a workflow run | 35 days | Several jobs can form a long experiment pipeline, but each job is still limited to 6 hours |
| Matrix | 256 jobs per workflow run | Convenient for parallelizing seeds / types / configurations |
| Concurrently running standard jobs on GitHub Free | 20 | Ideally up to 20 parallel independent tasks; Pro: 40, per the current GitHub table |
| Maximum retention for a public repository | 90 days | Artifacts and logs cannot be considered a permanent archive of proofs |
| Size of the standard public Ubuntu runner | 4 CPU, 16 GB RAM, 14 GB SSD | A suitable baseline for CPU-bound Python/SAT tasks; little disk for large proof archives |
| Maximum matrix size | 256 jobs | For a larger number of seeds, batched workflow runs are needed |

The stated limits are changeable by GitHub; as the project grows, the current Actions limits page should be consulted.

### 19.2. How to launch computations from separate branches

For `push`, GitHub can run a workflow that is present in the pushed branch even if the workflow file has not yet been merged into the default branch. Therefore the experimental branch `experiment/q1-offsets` can contain its own `.github/workflows/run-experiment.yml` and be launched on push.

But it is more convenient to maintain **one common runner workflow** in the default branch, and to describe each experiment by a separate branch and configuration:

- `experiment/q1-type58-offsets`: the config, hypothesis, parameters and code of a specific experiment;
- `experiment/gauss-chambers-type0`: another hypothesis;
- the workflow is launched on `push` for `experiment/**` branches or manually via `workflow_dispatch`;
- for the `Run workflow` button the workflow file must be in the default branch; after that the branch to run on can be selected.

This reduces copying of YAML but keeps the result fully tied to the commit SHA of the experiment. A separate workflow file inside the branch is also possible if a fully autonomous run is needed.

### 19.3. Minimal template

Below is an example of a common workflow. In a production version third-party Actions must be pinned by full commit SHA, not only by floating tags. The experiment parameters should be stored in a version-controlled config file in the corresponding branch.

```yaml
name: Research experiment

on:
  push:
    branches: ["experiment/**"]
    paths:
      - "research/**"
      - ".github/workflows/research-experiment.yml"
  workflow_dispatch:
    inputs:
      experiment:
        description: "Experiment/config id"
        required: true
        type: string

permissions:
  contents: read

jobs:
  compute:
    runs-on: ubuntu-24.04
    timeout-minutes: 350
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.ref }}

      - name: Record provenance
        run: |
          mkdir -p artifacts
          git rev-parse HEAD > artifacts/commit.txt
          python --version > artifacts/python-version.txt
          lscpu > artifacts/cpu.txt
          free -h > artifacts/memory.txt

      - name: Run experiment
        run: |
          python research/12-faced-polyhedron/code/run_experiment.py \
            --config research/12-faced-polyhedron/configs/${{ inputs.experiment }}.yaml \
            --output artifacts/result.json

      - name: Upload result
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: ${{ github.ref_name }}-${{ github.run_id }}
          path: artifacts/
          retention-days: 90
```

The path/CLI in the example must be adapted to the project's real runner script; this is an architectural template, not ready to run without such an entry point.

### 19.4. What must be saved

Each run must leave a self-describing result package:

- the commit SHA and the branch name;
- the experiment config, all parameters and the random seed;
- versions of Python, libraries, SAT/SMT solvers, the container/image digest;
- the CPU/RAM of the runner;
- stdout/stderr and exit code;
- checkpoints and models/candidates found;
- the exact verifier output;
- hashes of the inputs, results and certificates;
- a short `CONCLUSION.md`: what the hypothesis predicted, what happened and what this outcome allows one to claim.

Large proof files should be moved to a versioned long-term archive (GitHub Release/Zenodo/another durable storage) and in Git one should leave the URL, size and SHA-256. Actions artifacts in a public repository have a maximum retention of 90 days under the current policy.

### 19.5. Proposed scheme of experiments

Do not create a new copy of the workflow for each random seed. It is better:

- one branch per scientific hypothesis/experiment;
- one config file per condition;
- a GitHub Actions matrix for independent subtasks (different seeds, maps, normal chambers);
- one job is one reproducible portion of computation with a hard timeout and a checkpoint;
- a separate artifact for each job and a final aggregator that assembles the results table.

Use `concurrency` so that accidental consecutive pushes do not create endless queues. For heavy tasks, save a checkpoint regularly and start the next batch from it. Do not give the workflow `contents: write` permission if it is not needed; do not run potentially untrusted pull-request code with secrets. GitHub separately states that the use of Actions must comply with the GitHub Terms of Service and Additional Product Terms.

**Conclusion:** GitHub Actions is a reasonable way to turn the repository into a small distributed computational laboratory: to run many independent, bounded and reproducible experiments on cloud runners. But it is not a substitute for the mathematical selection of hypotheses. Priority remains with experiments that test one strong idea, not with the maximum number of random starts.

## 20. Updated main conclusion of the audit

The project should continue the research, but measure progress by the number of new evidentiary constraints, not by CPU-hours and the number of runs.

At the nearest stage the most valuable are:

1. to analyse Q1 through the UNSAT core and try to obtain a human geometric lemma on the incompatibility of normals and offsets;
2. to use `type0_genus3_extendable` as the main exact positive control and to investigate the geometric possibility of a transition from it to the next genus;
3. to study the space of chirotope chambers and look for transitions/obstructions not in raw coordinates but at the level of chambers;
4. to turn small computational conflicts into compact geometric lemmas;
5. to use GitHub Actions for reproducible and parallel experiments, each of which tests a pre-formulated hypothesis.

**New criterion of research success:** one good experiment must either find an exact witness, or give an independent certificate of impossibility, or reveal a short cause of failure that can be turned into a general statement. If it merely increases the number of configurations examined, its priority is low.

---

## Additional sources for the addendum

- R. Mizhaev, *Integer Realization of an Equivelar Octahedron of Genus 3*, arXiv:2609.17700: https://arxiv.org/abs/2609.17700
- G. Röst, V. Vígh, *A second eight-faced polyhedron in which every two faces share an edge*, Zenodo (2026): https://zenodo.org/records/23027039
- N. S. Wedd, *The Genus-3 Regular map {8,3}* (including an irregular 12-octagon map): https://www.weddslist.com/groups/genus/3/8-3/8-3.php
- GitHub Docs, *Billing and usage*: https://docs.github.com/en/actions/concepts/billing-and-usage
- GitHub Docs, *Actions limits*: https://docs.github.com/en/actions/reference/limits
- GitHub Docs, *Events that trigger workflows*: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- GitHub Docs, *Choosing the runner for a job*: https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job
- GitHub Changelog, *Actions retention now covers checks, runs, and statuses* (1 October 2026): https://github.blog/changelog/2026-10-01-actions-retention-now-covers-checks-runs-and-statuses/

---

# Addendum of 31 October 2026: clarifications after discussion with the author

## 21. Clarification: are the genus-3 constructions found new objects of Mizhaev type?

No, they cannot be called Mizhaev polyhedra or new realizations of his eight-faced object.

The work of R. Mizhaev (arXiv:2609.17700, 15 September 2026) gives a genus-3 object with 8 simple planar nonagonal faces, 24 vertices and 36 edges. Every pair of faces is adjacent; 20 pairs have one common edge, 8 pairs have two collinear common edges. In Polyhedrons other objects were built: 12 faces, 32 vertices, 48 edges, genus 3 and 48 adjacent pairs out of 66.

Both `solid-first` realizations were re-checked with `verification/verify_solid.py`: `EXACT_EMBEDDED=True`, 12 simple faces, `chi=-4`, `genus=3`, `V=32`, `E=48`, 48/66 adjacent pairs and an empty list of extra intersections. All five files `type0_genus3_extendable*.json` again passed `ladder_exact.verify`.

The distributions of the number of sides of the faces (which are also the degrees of the vertices of the dual face-adjacency graph) differ:

- type0: `6, 6, 6, 6, 8, 8, 9, 9, 9, 9, 10, 10`;
- solid-first: `5, 6, 7, 7, 8, 8, 8, 8, 9, 9, 10, 11`.

Consequently these two maps are different. Both also differ from the specific regular Dyck map `{8,3}` / dual R3.2, for which all 12 faces are octagonal. However, this is not yet a proof of international novelty: one must check the full catalogues of genus-3 maps, canonicalize the maps taking into account permutations of faces and mirror reversal, and search for known spatial realizations. Until this check is completed, the correct formulation is "constructions that are new to the project and exactly verified", not "first in the world".

Their independent value:

1. exact positive benchmark objects for plane-arrangement/solid-first generators and geometric validators;
2. examples of different genus-3 maps with the same f-vector `(V,E,F)=(32,48,12)`;
3. material for studying the space of geometric realizations: the log records several chirotope-distinguished realizations of one type0 map;
4. for type0, a concretely geometrically realized lowest level of one combinatorial chain leading to the genus-6 target map.

The five JSON files must not be regarded as five different abstract maps. They are five geometric realizations of one type0 combinatorial map. Differing chirotope/sign-patterns may be interesting for studying the chambers of the realization space, but by themselves do not yet prove distinct ambient-isotopy classes.

## 22. Refined Q1 result: chain-consistent normals do not solve the offset problem

The experiment `chain_normals.py` gave an important partial positive result. For type 58 and chain seed 3 one set of 12 normals was found that simultaneously passes the exact checks of the required Gauss classes at all seven levels:

`M0, M1, ..., M6`: degrees `+1, 0, -1, -2, -3, -4, -5`.

Then, with these normals fixed, the exact Z3/SAT model for the plane offsets of the lowest level `M0` (the sphere) returned `UNSAT` in 33 seconds.

**Correct interpretation:** Gauss-degree admissibility is a necessary filter, but for this system of normals found it is not a sufficient condition for the existence of a geometric realization. Separately one must ensure the compatibility of offsets/periods, the closing of faces, correct combinatorics and the simplicity of polygons. Q1 has thereby pointed out which layer of conditions is missing in the current normals-first filter.

**Boundary of the conclusion:** this `UNSAT` applies to a specific set of normals, gauge, bounds/margins and the current formalization of offset feasibility. It does not prove that no other suitable system of normals exists for type 58, does not refute the normals-first strategy, and still less proves the impossibility of the original genus-6 object. No saved SMT2/proof/UNSAT core for this specific run was found in the bundle; the result is so far an exact answer of the solver to the fixed model, but not an independent evidentiary certificate.

The next scientific step is not to enumerate new normals seeds en masse, but to extract a small contradiction core for the seed found, translate it into an understandable geometric statement, and check exactly which relation between normals and offsets is violated. Then the prefilter should be changed so that offset/period feasibility is checked cheaply earlier than the more expensive stages.

## 23. A new checkable artifact: an explicit genus 3 → genus 6 chain at the combinatorial level

In the course of the repeated check of `type0_genus3_extendable.json` not only was the record `reach=66` confirmed, but a concrete sequence of three handle attachments was also extracted. Each operation removes two disjoint triangular faces of the dual triangulation and adds a six-triangle annulus strip, introducing six new edges (that is, six new pairs of adjacent original faces).

The explicit pairs of removed triangles:

1. `(1,2,10)` and `(4,7,9)`;
2. `(0,5,8)` and `(2,6,7)`;
3. `(0,9,11)` and `(3,5,10)`.

The full list of the six inserted triangles and six new adjacencies at each step is stored in the file `polyhedrons_type0_handle_completion_certificate.json`. The levels were checked by exact discrete invariants:

| Level | Dual triangles | Edges / face adjacencies | Euler characteristic | Genus |
|---|---:|---:|---:|---:|
| M3 | 32 | 48 | −4 | 3 |
| M4 | 36 | 54 | −6 | 4 |
| M5 | 40 | 60 | −8 | 5 |
| M6 | 44 | 66 | −10 | 6 |

For all four maps it was checked that: every dual triangular face has three distinct vertices; every edge belongs to exactly two triangles; the dual graph is connected; the link of every vertex is a single cycle; a consistent orientation exists. The final map under the current vertex numbering coincides with the record `id=0` in `data/k12_triangulations.json`.

The reproducible independent checking script is `verify_type0_handle_completion.py`. Its successful output confirms only the **combinatorial** continuation. No geometric realization of the levels genus 4, 5 or 6 is claimed by this certificate.

This extracted witness makes the type0 result noticeably stronger and more convenient for external review: now instead of the statement "reach reports 66" one can provide a finite object, three operations and a check of each intermediate level.

## 24. Priority result for the first AI-assisted research dossier

One result is chosen:

> **An exact genus-3 spatial realization of a type0 map for which an explicit combinatorial chain of three handle attachments to one of the 59 target genus-6 triangulations is provided.**

Why it is preferable for the first AI review:

- a positive and mathematically concrete result, not the interpretation of a large array of failed runs;
- a small data set: 12 rationalizable planes, 32 triangles of the dual map, 3 surgeries and 4 final maps;
- the genus-3 geometric part is checked by exact arithmetic;
- the combinatorial continuation can be checked independently by a short script;
- correctness and novelty can be investigated separately.

The AI task must be limited to a referee-style check: (i) independent verification of the rationalized genus-3 geometry, (ii) canonicalization of the initial map, (iii) verification of each of the three handle surgeries, (iv) comparison of the final map with the catalogue of 59, (v) a novelty search over genus-3 maps and polyhedral embeddings, (vi) an exact formulation of what is proved and what is not. Do not ask the AI to "write a paper" right away.

Q1 should be singled out as a separate next research task, proof mining from the offset-UNSAT, but should not be chosen as the first external result until there is a saved formula and an explainable contradiction core.

## 25. Refined research philosophy: not exhaustive enumeration, but search with high information yield

The author's strategic stance becomes an explicit principle of the project:

**Do not try to enumerate the whole space of variants. Look for mathematically motivated, non-obvious subspaces and methods in which a small experiment can exclude a whole class of configurations or reveal a new constraint.**

Each new idea must pass a short decision protocol:

1. **Mathematical source:** which known property, invariant, lemma or structure suggests the direction?
2. **Transfer of method:** is there a useful analogy from another discipline?
3. **Discriminating experiment:** which different hypotheses are separated by the outcomes of the test?
4. **Cheap refutation:** can the idea first be tested on a small configuration or one seed?
5. **Path to a lemma:** if the test works/does not work, can a generalizable statement, a certificate or a short explanation be obtained?

Ideas for transfer, with priority given to those connected with the current data:

- **Proof mining / SAT-core analysis:** use small UNSAT cores not only as a solver result but as a source of geometric lemmas; identify repeating minimal conflicts for whole families.
- **Theory of oriented-matroid chambers and arrangement geometry:** investigate the adjacency of chambers/chirotopes, the boundaries of degeneration and possible transitions between realizations, instead of uniform sampling of the space of normals.
- **Motion planning from robotics:** regard the set of admissible embeddings as a configuration space, and the degeneracies (zero edges, touchings, self-intersections, loss of simplicity) as an obstructing discriminant. Build a small roadmap of the genus-3 realization space and find out whether one can get into a region where the next handle is realizable without crossing the forbidden boundary.
- **Rigidity theory / stress matrices:** study the rank of the Jacobian of the closure and planarity conditions, infinitesimal motions and self-stresses. A possible success is an early rank obstruction that excludes a family of offset systems before launching the nonlinear search.
- **Active learning / experimental design:** choose the next experiment by expected information value: how much will each possible outcome change the strategy? First maximize discriminating power, not the number of seeds/CPU-hours.
- **Homotopy continuation and algebraic geometry:** when passing between levels, try to track the solution branches of a parametrized system and catch the point of entry into the discriminant, instead of independent restarts of the optimizer.

These ideas are not claims that the corresponding tools will automatically solve the problem. They are concrete interdisciplinary hypotheses, each of which must be tested by a cheap test and have a clear success criterion.

## 26. GitHub Actions: refined architecture and verified limits

The author's idea is technically correct: GitHub Actions can perform full scientific computations, not only unit tests. A workflow can run Python/C++, SAT/SMT, CP-SAT, exact verifiers and analysis scripts. A `push` event can launch a workflow defined directly in the experimental branch; GitHub uses the workflow files present in the commit/ref of the corresponding event. `workflow_dispatch` has a separate rule: the workflow file must be present in the default branch for the manual trigger to be available.

As of 31 October 2026 the official GitHub documentation states:

- the standard Linux runner `ubuntu-24.04`/`ubuntu-latest` for a public repository: 4 CPU, 16 GB RAM, 14 GB SSD; standard GitHub-hosted runner usage for a public repo is free with no minutes limit;
- maximum concurrency of standard hosted jobs: GitHub Free 20, Pro 40 (an account plan limit, not per branch);
- each hosted job: at most 6 hours;
- a whole workflow run: at most 35 days;
- matrix: at most 256 jobs per workflow run;
- for public repositories the retention of checks/runs/artifacts/logs is limited to 90 days; starting from 1 October 2026 the retention setting also covers check runs/workflow runs/statuses.

These resources are convenient for independent CPU tasks: for example, different map types, normal chambers or seeds after theoretically justified selection. They do not turn several runners into one big shared-memory machine: a single job remains limited to 4 CPUs and 16 GB RAM, and local state between jobs is not preserved automatically.

Recommended scheme:

- one branch `experiment/<hypothesis-id>` per scientific hypothesis;
- in the branch: the statement of the hypothesis, the config, the code and the commit SHA;
- one common workflow for all `experiment/**` branches (or a separate file in each branch if a full experimental capsule is needed);
- a job matrix only for genuinely independent subtasks;
- each job is limited by `timeout-minutes: 350` and writes a checkpoint;
- save the config, seed, commit SHA, solver versions, runner specs, stdout/stderr, exit status, candidates, the exact verifier report and SHA-256;
- use Actions artifacts for intermediate exchange, but move long-term proof artifacts to a GitHub Release/Zenodo/long-term archive, since retention is not permanent;
- `GITHUB_TOKEN` with minimal permissions, do not run untrusted PR code with secrets, do not grant `contents: write` if the workflow need not commit results.

Do not run a heavy search on every push by default. It is better for a push to launch a quick smoke/preflight, and for long experiments to be launched manually or only for an explicit experimental branch/config. For long computations split the work into checkpointable jobs shorter than six hours. For independent jobs one can limit `strategy.max-parallel` and use `concurrency` so as not to accumulate a useless queue.

The previous YAML example in the main report should be regarded as an architectural sketch, not a ready workflow: there `inputs.experiment` is used for `push`, where there is no such input. It is more practical to keep a fixed config file in each experiment branch (for example `research/12-faced-polyhedron/experiment.yaml`) or to compute the config path explicitly from the branch name.

An example of a more consistent template (the `run_experiment.py` command here is nominal; it needs to be implemented as the project's single entry point):

```yaml
name: Research experiment

on:
  push:
    branches: ["experiment/**"]
    paths:
      - "research/12-faced-polyhedron/**"
      - ".github/workflows/research-experiment.yml"
  workflow_dispatch:

permissions:
  contents: read

jobs:
  compute:
    runs-on: ubuntu-24.04
    timeout-minutes: 350
    strategy:
      fail-fast: false
      max-parallel: 4
      matrix:
        seed: [11, 12, 13, 14]
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.sha }}

      - name: Capture provenance
        run: |
          mkdir -p artifacts
          echo "$GITHUB_SHA" > artifacts/commit.txt
          echo "${{ github.ref }}" > artifacts/ref.txt
          echo "${{ matrix.seed }}" > artifacts/seed.txt
          python --version > artifacts/python-version.txt
          lscpu > artifacts/cpu.txt
          free -h > artifacts/memory.txt

      - name: Run one bounded experiment
        run: |
          python research/12-faced-polyhedron/code/run_experiment.py \
            --config research/12-faced-polyhedron/experiment.yaml \
            --seed "${{ matrix.seed }}" \
            --output artifacts/result.json

      - name: Upload result package
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: ${{ github.ref_name }}-${{ matrix.seed }}-${{ github.run_id }}
          path: artifacts/
          retention-days: 90
```

For `push` the workflow can live in the experiment branch and run before the merge. For a manual `workflow_dispatch` the same workflow file must also exist in the default branch; the desired branch is selected in the UI. One job is one seed/subtask, and `max-parallel` limits concurrent execution within one matrix. For long work a checkpoint must be written periodically: one cannot count on a job killed at the 6-hour limit managing to execute the last upload step.

**Updated main conclusion:** the computing power of GitHub Actions can help with parallel independent checks, but the project's strategy must remain theory-led. Cloud CPUs should be spent after the mathematical selection of hypotheses, not instead of such selection.

---

## Additional current sources

- GitHub Docs, Actions limits: https://docs.github.com/en/enterprise-cloud@latest/actions/reference/limits
- GitHub Docs, runner selection and public/private specifications: https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job
- GitHub Docs, workflow files and refs: https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows
- GitHub Docs, workflow_dispatch default-branch requirement: https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow
- GitHub Docs, artifact and check/run retention: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository
- GitHub Changelog, retention policy effective 1 October 2026: https://github.blog/changelog/2026-10-01-actions-retention-now-covers-checks-runs-and-statuses/
- R. Mizhaev, *Integer Realization of an Equivelar Octahedron of Genus 3*: https://arxiv.org/abs/2609.17700
- J. Bokowski and K. H., *Polyhedral Embeddings of Triangular Regular Maps of Genus g, 2 ≤ g ≤ 14, and Neighborly Spatial Polyhedra*: https://doi.org/10.26083/tuprints-00030025
