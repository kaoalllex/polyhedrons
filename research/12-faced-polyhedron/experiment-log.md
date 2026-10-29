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
