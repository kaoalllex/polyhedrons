# Experiment log

Append-only. Each entry: date, track, question, command, seeds, runtime, outcome.
Negative results are kept.

## 2026-10-29 Setup (PI)

* Environment: 4 CPU cores, 15 GB RAM, Python 3.13.17, numpy 2.5.3; installed scipy 1.18.1,
  sympy 1.14.0, networkx 3.7, z3-solver, python-sat (CaDiCaL 1.9.5, Kissat 4.0.4, Glucose),
  ortools 9.15, numba 0.68.1. gcc 13.3.
* Claude Code 2.1.312. Main session model `claude-opus-5-5`, effort `xhigh`.

## 2026-10-29 Track 2: enumeration of neighborly genus-6 12-vertex triangulations (combinatorial-topology)

Question: independent enumeration of all orientable triangular embeddings of K12 (genus 6) up to
combinatorial isomorphism; machine-readable data. No seeds (all runs deterministic). All runs
single-core, at most 2 concurrent processes, `timeout` on every long run. Binaries built in the
session scratchpad with `gcc -O2 -Wall` (gcc 13.3).

1. `enum_k12 first_only` -> first solution after 394 nodes, 0.001 s; written (canonically
   relabelled) to `data/k12_first.json`; `check_triangulations.py` OK. (= id 2 of the full list.)
2. `timeout 3000 enum_k12 > data/enum_k12_raw_output.txt`: 12,455,137 nodes, 12,144 labelled
   solutions, **59 classes**, 18.86 s CPU (19.1 s wall), orbit-stabiliser failures 0.
   No checkpointing needed at this runtime.
3. `build_json.py` -> `data/k12_triangulations.json` (Python re-derivation of the canonical form
   agrees with the C canonical form for all 59; 0.8 s).
4. `check_triangulations.py data/k12_triangulations.json` first run: FAIL on entry 39
   (aut_orient_preserving_order). Cause: BUG IN THE CHECKER (orientation test compared directed
   edges, but every edge occurs in both directions); fixed to compare cyclically normalised
   oriented triangles. Rerun: all OK (4.3 s); with `--selftest` 4.7 s.
   Negative controls: flipped triangle / duplicated (relabelled) type / wrong aut_order /
   broken edge -> all rejected.
5. `enum2_k12 orient print` first version: OVERCOUNTED (21,988 solutions after 31 s, run
   killed). Cause: when the branching edge lies in no triangle, its two triangles were chosen in
   both orders (each such solution produced twice). Fixed by choosing an unordered pair c1<c2.
   Rerun: 214,073,339 nodes, **12,144** labelled orientable solutions, 64.6 s CPU (66.0 s wall).
6. `classify_enum2.py` on the 12,144 enum2 solutions: each matched to exactly one of the 59
   entries (invariant lookup + brute-force isomorphism); every entry hit exactly 264/|Aut| times;
   no duplicate labelled solutions. 25.8 s.
7. `compare_literature.py` (run with `python3 -I`; external files only parsed):
   HackerPoet `topologies.txt` 59 -> bijection with our 59; Lutz-format `k12_g6_lutz.txt`
   59 -> bijection with our 59. Mapping in `data/k12_literature_map.json`. External
   `automorphisms.json` (size, pres) agrees with our (|Aut|, |Aut+|) for 59/59. 2.0 s.
8. `k12_invariants.py` -> `data/k12_invariants.json` (groups, orbits, fixed structures), 0.2 s.
   Cross-check with the canonical-form automorphisms of `k12_tools.py`: element types over all
   59 types: 59 identities, 27 involutions (+), 14 order-3 (+), 12 order-4 (−); no
   orientation-reversing involution; every nontrivial automorphism fixed-point-free on vertices.
9. Side check (not needed for R^3): `timeout 1200 enum2_k12 all` (no orientability pruning),
   stopped manually (not finished): last progress line `  nodes=1048576000 sols=2193334 (or 418, nonor 2192916) t=257.3s`.
   So >= 2,192,916 labelled non-orientable neighborly 12-vertex triangulations (chi=-10) with
   link(0) = the cycle 1-...-11, hence >= 2,192,916/264 > 8,300 non-orientable isomorphism types
   [N, lower bound; the exact count was not computed]. Negative/incomplete result kept for the record.

## 2026-10-29 PI experiment E-PI-1: exact single-plane relocation from near-misses

**Question.** Are the best known asymmetric near-misses (5 violations, HackerPoet topology 33
and 36) local minima with respect to moving ONE plane anywhere in space (not just locally)?
If a single-plane global move lowers the count, the prior optimizers were trapped by locality.

**Method.** `code/relocate.py`: with 11 planes fixed, the count is constant on the cells of an
arrangement of 220 hyperplanes in the 4D space of plane vectors (165 fixed triple points + 55
fixed line directions). Probe the 8 cells around (a 1/stride sample of) the 1.75M vertices,
take the best cell, re-centre it by LP. `code/reloc_descent.py` cycles over planes in random
order, accepting moves with count <= current. Float arithmetic (fastviol), so any improvement
must be re-verified exactly.

**Calibration.** topology_37 seed (4 violations, symmetric map), stride 200: no plane can be
moved to reach < 4 (all 8 planes tested before a numerical exception that has since been
guarded). 10 µs per evaluation; a full scan (stride 1) costs ~140 s per plane on one core.

Run: `reloc_descent.py hp_seeds_ranked.json topology_33/shape_c5_i0_1154.obj t33.json 40 3 1 1`
(stride 3, 1 thread, seed 1, 40 minutes). Result: pending.

## 2026-10-29 Track 3 (OM-SAT)

* **Model check (§4–§5).** Re-derived independently: side(abc;d)=χ(abcd)χ(abc∞) exactly;
  with u_XY := spatial part of *(h_X∧h_Y∧h_∞) = −(n_X×n_Y), t_W−t_Z = det(XYZW)/(det(XYZ∞)det(XYW∞)),
  so σ_XY=+1 in that convention; E-predicate, §5.2 IN (boundary terms, transversal crossings, run rule)
  and Lemma 5.1 (both directions) all check out. No error found. Remarks: (1) the +ray and −ray
  parities agree *combinatorially* (side bits are vertex functions, so total crossings of L_XY ≡ 0),
  hence reorienting ∞ preserves IN; (2) IN[X;·] depends only on the rank-3 contraction χ/X, so
  "IN along L_XY = IN along L_XZ" is already implied by GP (pseudoline topology) — redundant;
  (3) Szilassi's index.html planes are NOT in general position (χ(0,1,5,∞)=χ(2,3,5,∞)=χ(4,5,6,∞)=0;
  three normal triples coplanar), so positive controls use a ±1 perturbation of 1000×planes.
* **Code.** `code/omsat.py` (encoder; one set of predicate formulas with a CNF/Tseitin backend and an
  Eval backend), `code/omsat_geom.py` (exact direct geometry, Fractions, 2D charts),
  `code/omsat_validate.py`, `code/omsat_sym.py` (Lutz maps, own Aut computation, symmetric instances),
  `code/omsat_crosscheck_track4.py`, `code/rup_check.py`. Outputs in `experiments/omsat/`.
* **Validation** (`python3 omsat_validate.py 300 100 8`, seed 20261029, 168 s): 693 uniform configs
  (Szilassi control, 292 perturbed Szilassi of which 93 embedded, 300 random n=7, 100 random n=12 on
  type id 0). Formula vs direct geometry: IN 180,318 / REFLEX 76,212 / RTURN 38,106 / E 256,530 /
  line order 1,686,120 / side 281,020 evaluations, **0 mismatches**; Lemma 5.1 (triples) ⇔ direct
  embeddedness (pairwise F_X∩F_Y=e_XY + simplicity): 693/693 agree; POC geometric check on 11,114 corners
  of simple polygons: 0 failures; all 94 embedded configs satisfy every clause family; GP holds on all.
  CNF backend: 17 configs with χ fixed by units — 0 mismatches between Tseitin literals and Eval values
  (252 resp. 1452 named predicates each); full instance SAT iff Eval reports no violation (17/17;
  non-embedded ones UNSAT with assumption cores of 8–42 χ literals).
* **Cross-check with Track 4** (`planes.check_embedding`, imported only by the cross-check script):
  149 configs (120 perturbed Szilassi, 29 random n=12), 22,872 IN values, 0 mismatches; embeddedness
  agrees on 149/149 (32 embedded).
* **n=7 free χ** (Szilassi triangulation): SAT in ≤0.07 s for every option combination, with and
  without reorientation/mirror normalisation; the models satisfy all families.
* **Numbering.** All 59 Lutz maps matched to our `k12_triangulations.json` ids by canonical form
  (`experiments/omsat/lutz_to_ourid.json`; e.g. Lutz #25 = our id 0, #54 = id 58, #3 = id 32, #48 = id 26).
* **Symmetric instances (independent reproduction of Hashirama1337s/szilassi-12 Part B).** Own Aut
  computation (|Aut(#54)|=12, all orientation-preserving, T; |Aut(#3)|=|Aut(#48)|=6, D3). Encoding:
  GP + 176 triple clauses + χ(gS)=ε(g)χ(S) + orbit-flip and mirror normalisation. Controls per instance:
  free action, no forced-zero quadruple, explicit rational ρ:G→O(3) with det ρ=ε found and random
  ρ-symmetric configs uniform, instance without triples SAT, explicit normalised symmetric χ SAT.
  Results (cadical195 via PySAT): **#54 T UNSAT 1.3 s** (278 conflicts; also UNSAT without normalisation
  3.9 s, kissat404 3.3 s, glucose4 1.3 s); **#3 D3 UNSAT 9.3 s**; **#48 D3 UNSAT 10.6 s**.
  DRAT proof for #54 T: `experiments/omsat/sym_54_T.drat` (1282 lines, sha256 52497b88…ba23f), CNF
  `sym_54_T.cnf.gz` (sha256 of uncompressed ac71c316…be407). Check: `drat-trim sym_54_T.cnf sym_54_T.drat`
  (building drat-trim here was refused by the sandbox permission system); own minimal forward RUP checker
  `code/rup_check.py`: 1034 lemmas all RUP, empty clause derived, VERIFIED.
  #48 C2 (plain and with reflex+poc) launched with 30-min limits; see Track 3 results for outcome.
* **#48 C2** (6 orbits of size 2, half-turn; same controls as above, all passed): with F4 REFLEX1 + F6 POC
  (reflex corners are part of the encoding): **UNSAT in 298.2 s** (cadical195, 409,355 conflicts; 19,635 vars,
  483,166 clauses). Plain (GP+triples only): no result after ~320 s, stopped by me at the PI's wrap-up
  request (so this only shows that it took longer than 320 s). No proof was written for the C2 run.
  The prior work reports 188 s for #48 C2 with their orient encoding.

## 2026-10-29 Track 4 (geometry-first SAT)

Code: `code/planes.py` (exact geometry + DIRECT embedding checker + violation_profile), `code/geomsat.py` (SAT/MaxSAT/CP-SAT encoder for
fixed planes, §6(B)), `code/track4_common.py`, `code/unit_test_in.py`, `code/szilassi.py`, `code/szil_test.py`, `code/exp_n7.py`,
`code/exp_n12.py`, `code/anneal.py`. Bulk logs (not in repo): session scratchpad. All geometry is exact (Python ints / Fractions);
random planes are integers (scale 1e4, 1e5 in the annealer), general position checked exactly (all 4x4 dets among planes + h_inf != 0).
Encoding: 220 vars t_XYZ + Tseitin aux (n=12: ~7.0k vars, ~50k clauses incl. exactly-two per pair and all 3- and 4-cycles in links; 5+6
split links removed by lazy cuts; CP-SAT variant adds 5-cycles statically so the link constraint is complete). IN uses §5.2 verbatim,
with E/prefix-XOR/suffix-XOR chains shared along each line; the "run" term uses flip_{X,Y} = XOR_C [t_XYC and OR_{C' : side(XCC';Y)>0} t_XCC'].

**Mapping of MaxSAT scores to edge-face / self-crossing counts.** One violated non-triangle triple {X,Y,Z} = a point P=P_XYZ in F_X,F_Y,F_Z.
Let k = number of the 3 edges e_XY,e_XZ,e_YZ passing through P in their relative interior (computed directly, exactly):
k=0: V0 face-face-face interior point; k=1: V1 = one edge pierces the interior of the third face = 1 edge-face intersection;
k=2: V2 = two edges of one polygon cross in its plane = 1 polygon self-crossing (this also implies 2 edge-face contacts by Lemma 3.1, not counted
twice); k=3: V3 = three edges concurrent = 3 self-crossings. Reported V = V0+V1+V2+V3 (number of violated triples), and the benchmark-comparable
B = V0+V1+V2+3*V3 (= #self-crossings + #edge-face piercings, +V0). CP-SAT optimises B (weights 1, +2 for k=3 triples); the
plain MaxSAT/RC2 objective is V. Caveat: HackerPoet's/Moki-Julio's exact counting rules are not known to me; B is my best equivalent.

### E1 (3a) Is the encoded IN predicate (§5.2) equal to exact point-in-polygon?
`cd code; python3 unit_test_in.py 200 60` (seeds 101 (n=7), 202 (n=12); distributions cycled over sphere_unif,tangent,gauss,pts3,near_tangent,small_off).
Random planes, torus (n=7, relabelled) / random one of the 59 types from `data/k12_triangulations.json` with random labelling; IN evaluated by solving the
definitional CNF with t fixed; 4 ray variants (line L_XY or L_XZ, both directions). Result: n=7: 84,000 (face,point) comparisons, 0 mismatches;
n=12: 158,400 comparisons, 0 mismatches; violated-triple sets (encoding vs direct PIP) identical in all 1040 evaluations. In all these random trials
the polygons were non-simple, so this tests the even-odd rule incl. self-crossing rays. Runtime 7 s + 23 s. PASS.

### E2 (3b) Positive control: Szilassi
`python3 szilassi.py; python3 szil_test.py`. index.html MODELS.szilassi: all 7 faces exactly planar (rational check). Planes (ints):
(0,-20,5,-6),(0,20,5,-6),(50,-50,70,21),(-50,50,70,21),(-10,0,-5,-6),(0,0,5,-1),(10,0,-5,-6). They are NOT in general position (3 triple points
at infinity: planes {0,1,5},{2,3,5},{4,5,6}); their dual triangulation is a valid 14-triangle 7-vertex torus. After a random integer perturbation
(relative 1e-6..1e-3) general position holds, the direct checker passes with the Szilassi triangulation (ok_triples and ok_pairs True, profile all 0)
and the SAT encoder returns SAT (~10 ms), the model being exactly the Szilassi triangulation, direct checker PASS. 
Cross-validation of SAT vs brute force over all 120 labelled copies of the unique torus (`exp_n7.py cvp 25`, seed 17): 25 perturbed-Szilassi
arrangements (rel 0.02..0.5), 3000 (arrangement,labelling) pairs: direct ok_triples == ok_pairs in all (validates Lemma 5.1 on these), encoding == direct in all,
SAT == (some labelling embeds) in all 25; 5 SAT arrangements, each with exactly 1 valid labelling. (`exp_n7.py cv 3` on 18 pure random arrangements: 0 positives, 0 disagreements.)
Torus: 14 triangles {i,i+1,i+3},{i,i+2,i+3} mod 7: every pair in 2 triangles, all links 6-cycles, 120 distinct labelled copies (checked); orientability not separately checked
(K7 does not triangulate the Klein bottle, Franklin).
Robustness (`exp_n7.py rob 300`, seed 13; scale planes to 1e6, add uniform integer noise of relative size rel to all 4 coefficients): SAT fraction
rel 1e-4,1e-3,1e-2: 300/300; 0.03: 291/300; 0.1: 115/300; 0.2: 22/300; 0.3: 5/300; 0.5: 0/300. SAT count == count where the original
Szilassi triangulation stays valid at every level (no other torus ever appeared).
Random 7-plane arrangements admitting a torus (`exp_n7.py frac 3000`, seed 11, SAT verified by direct checker, 0 disagreements): sphere_unif 1/3000, tangent 1/3000,
near_tangent 0/3000, gauss 1/3000, pts3 0/3000, small_off 1/3000 => 4/18000 = 2.2e-4 (95% CI roughly 0.6e-4..5.7e-4). Solutions are rare but not absent; timing ~11 ms/arrangement.

### E3 (3c) n=12, random arrangements: SAT?
`python3 exp_n12.py sat 5 90 1001 1` (6 distributions x 5 arrangements, cadical195, timeout 90 s, 1 process). Result: 30/30 UNSAT, 0 timeouts,
time 5.3-27.8 s (median 11.8 s). Proven by the solver for those fixed planes: NO triangulation of any of the 59 types / any labelling embeds the polyhedron.
(Soundness rests on the encoding; the encoding was validated in E1/E2 only on fixed triangulations and n=7 SAT; no n=12 UNSAT was cross-checked independently.)

### E4 (3c) n=12 distance to a solution
RC2 (g4, stratification options adapt/exhaust/minz) on one sphere_unif arrangement: TIMEOUT at 250 s (core-guided approach does not scale; abandoned).
Replaced with CP-SAT (ortools, 1 worker, 36 s limit, objective B above): `python3 exp_n12.py cpsat 4 45 2002 1` (6 dists x 4). All 24 solved to FEASIBLE,
lower bound 0 (no optimality proof), so these are UPPER bounds on the minimum. B (edge-face + self-crossings): min 23, median 31, max 39; V (violated triples)
min 17, median 29, max 39. Per distribution (B): sphere_unif 39,31,27,37; tangent 32,32,34,32; near_tangent 30,28,31,27; gauss 31,24,36,29; pts3 35,28,35,28; small_off 30,23,33,38.
Typical profile: 4-17 pierced faces + 13-20 self-crossings, 8-12 of 12 polygons non-simple.

### E5 (4) Annealing, asymmetric random start
`python3 anneal.py 1 sphere_unif 9` (9 min, 1 process): SA on integer plane coefficients (move: perturb one plane by relative 6e-4..0.1) with T fixed, objective B (exact),
every 250 evals CP-SAT (25 s, warm start) re-optimises T. 2250 evaluations. B: 33 (initial CP-SAT) -> 24 (V=24, 1 face-face-face point, 4 edge-face, 19 self-crossings, 8 non-simple faces).
Saved: `experiments/track4_anneal_sphere_unif_1.json` (planes + triangulation, exact). No candidate (B=0 never close). Not extended (resource limit).

## 2026-10-29 PI: E-PI-1 result and fixed-normals method (E1)

* E-PI-1 (single-plane exact relocation, stride 3) from HackerPoet topology_33 seed (5
  violations, trivial-automorphism map): 33 relocation steps, every step found only count-5
  cells (plateau moves, some moving a plane far); no count < 5 reached. Stopped manually.
* E1 `code/fixed_normals.py`: with integer normals fixed, existence of offsets is exact
  SMT(LRA) in z3. A first version with float cofactors was WRONG (z3 exploited rounding with
  offsets ~1e16); fixed by exact integer cofactors and bounded offsets. Szilassi control (n=7):
  normals perturbed by sigma 0, 0.05, 0.10, 0.15 -> SAT and the independent exact checker
  (planes.check_embedding) confirms embedding; sigma 0.20, 0.25 -> UNSAT. n=12 seed
  topology_33: no answer within 300 s (smoke test: UNKNOWN at 20 s).
* Overnight package `overnight/run_overnight.py` (jobs normals/sym/cube/ils) smoke-tested:
  normals s0 UNKNOWN at 20 s; ils seed 0: 4 -> 4; sym Lutz #54 C3 class 0: UNSAT in 23 s
  (unverified, no proof tools here); cube map #1: cubes time out at 12 s and split as designed.
  PySAT's cadical195 ignores interrupt() during long solves, so cubes run in killable child
  processes.

## 2026-10-29 Cross-field round 2 + night-2 pdefect candidate

* **Night-2 `pdefect` candidate pd10_0 (type 10, defect 14.6 -> 0, 127 iterations): FALSE POSITIVE.**
  Reconstructed (closure MILP with phi = 0, `torus_defect(..., return_L='full')`): edge lengths
  |a| in [1, 100] (hits the bound A = 100), planes recovered exactly (coplanarity 6e-14). Exact
  check (`planes.check_embedding`, integer planes at 1e6 and 1e8): only 1 of 12 faces simple,
  51 violated triples, 33 bad pairs; local: 52 face self-crossings, 10 multi-reflex vertices.
  With simple faces imposed (`torus_simple`, R^3, phi = 0) the same normals are INFEASIBLE
  (13 s). Lesson: zero period defect is only a necessary condition (as in the T^3 runs); the
  `pdefect` job must check `torus_simple` before raising a candidate (fixed in the job).
* Q16 screw-orbit planes: KILL (best 27 / 28, random 23-39).
* Q17 winding-number classifier (`code/q17_winding.py`): exact octant test at all 220 triple
  points; 45 of 1005 imported seeds bound a solid (w in {0,1}); Monte Carlo misses thin defects.
* Q18 GWAS on imported seeds (`code/q18_gwas.py`): no universal defect position; hotspots in
  symmetric types (type 56: two 4-vertex orbits at 83-85 %, others <= 13 %).
* **Own path, ladder (Y1, `code/ladder.py`)**: closed polyhedra with n mutually adjacent faces;
  maps generated by annealing over rotation systems of K_n (no external data), doubled
  adjacencies via diagonals; numba triple-point energy (71 us per evaluation) for annealing,
  independent pair-based check at the end. Calibration n = 7 (Szilassi must be found), then
  n = 8 on genus 2. Results below as they come.

### Queue for the user's next night script (from `cross-field-ideas.md`)
| Idea | What to run | Needs |
|---|---|---|
| Y2 difference map (RRR) | divide-and-concur over plane coefficients, per type, 30 min | implementation (not yet written) |
| Y3 rare-event levels | subset simulation on violation levels 20 -> 0 per type | implementation |
| Y6 local-search SAT | probSAT / yalsat / ddfw on the asymmetric immersion CNFs (from `immersion` job) | solvers installed locally |
| Y5 CEGAR | abstract immersion models -> exact check -> blocking clauses | incremental CaDiCaL |
| Y8 symmetry breaking by irreps | annealing in one irrep subspace at a time | group representation code |
| Y1 ladder n = 9, 10, 11 | `ladder.py fast N G ...` with G = 3, 4, 5 | ready once n = 8 is understood |
| X5 planarization flow | smooth genus-6 surface with the map -> planar faces | implementation |

### Ladder (Y1) results, 2026-10-29 (own pipeline, no external data)
* Exact verifier `code/ladder_exact.py` (rational arithmetic; map checks, distinct points, simple
  faces incl. collinear touching, exact pair intersections on each line X cap Y). Agrees with the
  independent `planes.check_embedding` on n = 7 controls (positive and perturbed negative, identical
  bad-pair and simple-face counts).
* **n = 7 (K7, torus): Szilassi-type polyhedra found from random planes in seconds, 5 / 5 runs,
  all EMBEDDED by both exact checkers.** The pipeline works end to end.
* n = 8 (K8 on genus 2, two doubled adjacencies), first runs: the annealer found float "zeros" that
  the exact verifier rejected — two loopholes, both closed:
  1. collinear doubled edges merged (the two shared segments of a doubled pair overlap); the strict
     float crossing test and the triple criterion do not see it -> explicit disjointness penalty;
  2. an overlap of faces X, Y in the GAP between their two shared edges starts and ends at corners,
     so the triple-point criterion (Lemma 5.1 analogue) is blind to it -> annealing now uses
     `pair_energy` (numba twin of the exact pair verifier, 154 us).
  With the honest energy: best 2 on the first 3 maps (the remaining defect sits at the doubled
  adjacency: 6 of 8 faces simple). Runs continue (3 x 15 maps x 4 min).
  Observation for theory: X contains the gap next to the corner v2 = end of e1 iff X is reflex at
  v2; same for Y; both faces are of the same "side type" at e1 and e2 (orientation argument), so the
  local geometry at e1 and e2 is identical. Whether a doubled adjacency can be embedded at all is
  open — a clean small question.
