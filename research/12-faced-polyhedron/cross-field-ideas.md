# Cross-field ideas, round 2 (2026-10-29)

Prompt: famous cases where a problem was solved with tools from a distant field; lessons; new
ideas for the 12-face problem, each with a cheap first test. Verdicts and results go to
`sprint-board.md`.

## Historical cases and the lesson each one carries

| Problem (field) | Solved with (field) | Lesson for us |
|---|---|---|
| Poincare conjecture (topology) | Ricci flow, a heat equation for metrics (Hamilton, Perelman) | deform inside the right class instead of searching |
| Fermat's last theorem (number theory) | elliptic curves, modular forms (Wiles) | the obstruction is an invariant from another theory |
| Sphere packing in dim 8 / 24 | modular forms as LP "magic functions" (Viazovska) | an impossibility proof can be one explicit dual certificate |
| Four colour theorem | discharging (charges moved by local rules) + computer | local rules + a global sum give a contradiction |
| Map colour theorem (Ringel-Youngs) | current graphs (Kirchhoff's laws) | build the object from a small "voltage" generator; small cases separately |
| Knot invariants | statistical mechanics, quantum field theory (Jones, Witten) | partition functions are invariants |
| Sensitivity conjecture (30 years) | a 2-page signed-matrix spectral argument (Huang) | short linear-algebra proofs exist when the right matrix is found |
| Cap sets, Kakeya over finite fields | polynomial method (Dvir, Ellenberg-Gijswijt) | encode the configuration in a low-degree polynomial |
| Kelvin's foam problem | physical soap-foam simulation (Weaire-Phelan) | let physics relax the structure |
| Steinitz-type realizations | circle packings (Koebe-Andreev-Thurston) | a canonical geometric representative |
| Lifting frameworks to polyhedra | Maxwell-Cremona graphic statics (19th-century engineering); toroidal version Erickson-Lin 2020 | liftability = self-stresses = linear algebra; periodic version has cohomology conditions |
| Flat torus in R^3 | convex integration (Nash-Kuiper, h-principle) | the "impossible" can become possible in another regularity |
| Kneser conjecture | Borsuk-Ulam (Lovasz) | an equivariant topological map can kill a combinatorial problem |
| Phase problem in crystallography | difference map / RRR (Elser), later sudoku, packings, bit retrieval | a feasibility engine that beats annealing on hard non-convex constraints |
| Real algebraic curves (Hilbert's 16th) | tropical limit / Viro patchworking | glue simple local charts along a subdivision; multi-scale coefficients |
| Software verification | CEGAR (Clarke et al.) | abstract, check, refine with the counterexample |
| Rare failures of structures | subset simulation (Au-Beck), Wang-Landau (statistical physics) | estimate tiny probabilities level by level; the levels are a search engine |
| Impossible figures (perception) | sheaf cohomology (Penrose 1991); LP realizability of line drawings (Sugihara) | our period obstruction is exactly this kind of H^1 class |
| Cap sets, kissing configurations (2023-25) | AI search over generator programs (FunSearch, AlphaEvolve) | search for generators, not objects |

Lessons: (1) the obstruction is usually an invariant borrowed from another theory; (2) short
impossibility proofs are linear-algebraic (one dual certificate, one matrix, one polynomial);
(3) local rules + a global count (discharging) — our obstruction is local, so this fits;
(4) translate into a field that already has a theory (graphic statics, cohomology);
(5) flows instead of search; (6) search for generators; (7) solve smaller analogues first.

## Ideas, round 2a (given first)

| ID | Idea (origin) | First test |
|---|---|---|
| X1 | Maxwell-Cremona for genus g (graphic statics): the period obstruction = obstruction to lifting a framework; reciprocal diagram = Gauss image; Erickson-Lin torus theorem as template | derive the genus-g lifting criterion; compare with our 36 period conditions |
| X2 | Gauss-Bonnet discharging (four colour theorem): sum_X w_X = 12 - s (fresh-eyes identity) with face-local bounds on w_X / reflex corners | bound w_X from the geometry of one 11-gon; check the sum |
| X3 | Huang-style single certificate: one Farkas combination of the 36 period conditions, symmetric under Aut, valid for all admissible normals | LP over certificates for many normal sets at once |
| X4 | Current graphs -> screw-orbit planes (12 planes = orbit of a screw motion, perturbed) | 24 samples, CP-SAT best triangulation (Q16) |
| X5 | Planarization flow with a barrier (Ricci flow / convex integration), start from a smooth embedded genus-6 surface with the map drawn (e.g. Lawson-type surfaces) | Surface-Evolver-style local/global projection |
| X6 | Mini-FunSearch: agents write plane-set generators; scored by Gauss filter + period defect + violations | 20 generators x 1 min |

## Ideas, round 2b

| ID | Idea (origin) | First test | Payoff |
|---|---|---|---|
| Y1 | **Ladder of smaller analogues** n = 8..11 (Polya; Ringel-Youngs small cases): 8 faces pairwise adjacent on genus 2 (cubic forces two pairs to share two edges); 9/g3, 10/g4, 11/g5 similarly. Rank-4 OMs on 9 elements are fully catalogued (Finschi-Fukuda), so n = 8 is completely decidable | K8 genus-2 embeddings by annealing rotation systems; add diagonals; OM-SAT on 9 elements (seconds) | CORRECTION (advisor, 2026-10-29): a closed polyhedron with 8 mutually adjacent faces IS known — Mizhaev's octahedron (arXiv:2609.17700, genus 3, 8 pairs of faces sharing two edges; in this repository's README / index.html; our exact verifier confirms it EMBEDDED). Genus 2 with 8 faces is, to our knowledge, open. Arseneva et al. (SoCG 2021, DCG 2024, 'Adjacency graphs of polyhedral surfaces') realize EVERY graph as the adjacency graph of a polyhedral surface with non-convex cells, but (to be checked in the paper) their surfaces need not be closed - closing the surface is exactly the hard part; their construction is a lead. Calibrates every tool |
| Y2 | **Difference map / RRR** (Elser; X-ray phase retrieval -> sudoku, packings): divide-and-concur with one replica per constraint | implement; 30 min per type vs annealing | a different search engine for the same landscape |
| Y3 | **Rare-event estimation**: subset simulation (structural reliability) / Wang-Landau | levels E <= 20, 15, ..., 0 for a fixed type+labeling with fastviol | "size of the needle"; the level sampler is itself a search |
| Y4 | **Tropical limit / Viro patchworking**: coefficients t^v, combinatorics exact from the valuation matrix; glue local charts | sample integer valuation matrices; CP-SAT cost vs random (23-39) | multi-scale seeds no Gaussian sampler produces |
| Y5 | **CEGAR** (software verification): abstract immersion SAT solution -> exact realizability / embedding check -> refinement clause, incremental CaDiCaL | start from the simple-only SAT model of type 0 (527 s) | turns TIMEOUTs into a learning loop |
| Y6 | **Local-search SAT / survey propagation** (spin glasses): probSAT / yalsat / ddfw on the asymmetric immersion CNF | night run, 8 types | finds SAT models where CDCL times out (if any exist) |
| Y7 | **GWAS on near-misses** (genetics): do defects sit at the same combinatorial positions across seeds? | Q18 | candidate local lemmas |
| Y8 | **Landau symmetry breaking** (physics of frustration): symmetric realizations are impossible; search near the best symmetric near-misses along ONE irreducible representation at a time | anneal in each irrep subspace of the 36-dim plane space | structured low-dimensional search |
| Y9 | **Projective symmetries are covered for free** (convex projective geometry): a finite group of projective maps preserving the bounded polyhedron P preserves conv(P), hence (lift to a sharp cone, average in the dual cone) fixes a hyperplane missing conv(P); in that affine chart it acts affinely, then isometrically after averaging an inner product. So the symmetric theorem extends to projective symmetries | write the paragraph into the proof task | strengthens the theorem at no cost |
| Y10 | **Generalized winding number** (computer graphics, Jacobson et al. 2013): w is constant on the cells of the 12-plane arrangement; embedding => w in {0,1}; transverse crossings => three values | Q17 | exact, cheap test; classifies near-misses |
| Y11 | **Penrose cohomology of impossible figures + Sugihara's LP for line drawings** (perception, computer vision): language for the write-up of the period obstruction; fixed projection + depth labels make non-intersection linear | framing; possibly an LP-based depth-order search | clearer statement of the obstruction |

## Ideas, round 2c: complex numbers (user's question, 2026-10-29)

Direct complexification does not help: over C there is no order, so "simple polygon", "inside",
"faces do not intersect" have no meaning, and every 12-plane configuration in general position
realizes the incidences of any map. The whole difficulty is real (signs / chirotope), so
"converting back" is the entire problem. Meaningful uses of complex numbers:

| ID | Idea (origin) | First test |
|---|---|---|
| Z1 | **Weierstrass representation** (minimal surfaces): a real surface x = Re of an integral of complex data on a Riemann surface; its obstruction is the PERIOD PROBLEM (real parts of periods vanish) = our 36 handle-period conditions. Our surfaces are mostly saddles (27-33 of 44), so the Gauss map is close to an anti-holomorphic 5-sheeted branched cover of the sphere (Riemann-Hurwitz for genus 6: 20 branch points); discrete minimal surfaces with planar faces exist (Bobenko-Hoffmann-Springborn). | build admissible normals from a degree-5 branched-cover model; study how the period problem is solved for genus-g minimal surfaces (symmetry or parameter continuity) |
| Z2 | **Complex detours in homotopy continuation** (numerical algebraic geometry: Bertini, HomotopyContinuation.jl): paths through C avoid the singularities where real paths stall | boundary configurations (some inequalities made equalities), all complex solutions, keep the real ones |
| Z3 | **Signs -> phases relaxation** (phased / complex matroids; Goemans-Williamson-type relaxations): replace +-1 chirotope signs by unit complex phases, optimize continuously, push phases to +-1 | relaxed objective on the ladder (n = 7 / 8) |

## Ideas, round 2d: the science of solving puzzles (user's question, 2026-10-29)

| ID | Puzzle lesson (origin) | Transfer to our problem |
|---|---|---|
| P1 | **Staged subgroups** (Rubik's cube: Thistlethwaite / Kociemba solve in nested stages, each stage keeps what earlier stages fixed) | search in stages that PRESERVE invariants: right Gauss class -> immersion -> closure -> simple faces -> embedding; never leave a class once reached (today our searches jump directly to the last stage) |
| P2 | **Macro-operators** (cube algorithms that change only a few pieces) | learn compound 2-3-plane moves that repair one violation without creating another, from the plateau data (n = 8: one-plane moves are provably stuck) |
| P3 | **Parity invariants** (Loyd's 15-puzzle is unsolvable by a permutation-parity argument) | invariants that prove impossibility: Gauss degree, parity theorem; look for one explaining the n = 8 plateau |
| P4 | **Pattern databases** (Korf: exact costs of sub-puzzles as admissible heuristics) | precompute, for small sets of faces (4-6), all locally feasible configurations; prune / guide with them ("per-face decomposition") |
| P5 | **Constraint propagation + fail-first** (Sudoku, CSP: most constrained variable first; human techniques = derived rules) | branch first on the most constrained faces / vertices; turn recurring local failure patterns into lemmas (clauses) |
| P6 | **Jigsaw: edges first, then clusters, then merge** | solve sub-configurations (5-7 faces) and glue (fragment assembly; Szilassi embryo was one attempt) |
| P7 | **Work backwards / puzzle design** (designers start from the solution) | "solid-first" search: keep an EMBEDDED solid at all times (a union of cells of the 12-plane arrangement; 45 imported seeds are already embedded solids with split faces) and repair the face structure (one simple face per plane, all 66 pairs adjacent); any zero is automatically an embedding |
| P8 | **Lookahead / failed-literal probing** (Nonograms, SAT) | try a decision, propagate, learn from the contradiction |
