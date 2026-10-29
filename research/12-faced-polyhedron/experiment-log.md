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
