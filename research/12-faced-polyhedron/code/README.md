# Code registry

Flat module directory (scripts import each other by name; run from this folder or put it on `sys.path`).
Environment: `../requirements.txt`. Every module's docstring has its usage line. Status: **CORE** = trusted,
tested library (changes need `verify_all.py` green and a note in `experiment-log.md`); **TOOL** = maintained
analysis / control script; **ENGINE** = search engine, with its verdict from `../STATUS.md`; **ONE-OFF** =
script of one sprint-board test, kept for reproducibility, not maintained.

## Core library

| Module | Role |
|---|---|
| `planes.py` | exact face-plane geometry, `check_embedding` (Track 4) |
| `ladder_exact.py` | exact rational verifier for planes + links (doubled adjacencies supported) - the success criterion |
| `ladder4_exact.py` | same for 8-face rungs with 4-valent vertices |
| `verify_solid.py` | exact check of solid-first results (map extraction + `ladder_exact`) |
| `gauss_degree.py` | Gauss-map degree, covering (sampled), saddles; `coherent_triangles`, `links_from` |
| `gauss_gate.py` | Gauss gate T1 per handle (k_tau, admissible gauges, turning numbers, hemisphere margin) |
| `omsat.py`, `omsat_geom.py`, `omsat_sym.py`, `omsat_gauss.py` | OM-SAT encoder, exact evaluator, symmetric instances, Gauss clauses |
| `fixed_normals.py`, `fixed_normals_gauge.py` | exact offset SMT at fixed normals (sub-maps supported) |
| `period_defect.py` | period / closure LP-MILP at fixed normals, `torus_simple` |
| `k12_tools.py`, `check_triangulations.py`, `k12_invariants.py` | 59-type data helpers, independent checker, invariants |
| `handle_add.py`, `tubes.py` | handle attachment, `reach`, tube decomposition of neighbourly maps |
| `ladder.py` | smaller-analogue maps, `pair_energy`, `degeneracy` |
| `solid_first.py`, `solid_fast.py`, `solid_cpsat.py` | solid-first state, numba evaluator, exact CP-SAT inner solver |
| `fastviol.py`, `local_viol.py`, `relocate.py` | float violation counters, exact single-plane relocation |
| `rup_check.py` | minimal RUP proof checker |

## Tools and controls

| Module | Role |
|---|---|
| `control_rost_vigh.py` | positive control: Roest-Vigh 8-face genus-3 polyhedron (in `verify_all`) |
| `nf_control.py` | positive control of normals-first on a realized map (see ROADMAP E02) |
| `omsat_validate.py`, `omsat_crosscheck_track4.py`, `submap_validate.py`, `unit_test_in.py` | encoder / predicate validation |
| `enum_k12.c`, `enum2_k12.c`, `build_json.py`, `classify_enum2.py`, `compare_literature.py` | enumeration of the 59 types and literature cross-check |
| `import_hackerpoet.py` | import of the 1005 HackerPoet near-misses |
| `gate_vs_glad.py` | night-3 analysis (gate vs branching outcomes) |
| `beauty.py`, `polish_solid.py`, `render_solid.py`, `render_defect.py`, `research_map.py`, `see_through.py` | presentation and figures |
| `fresh_eyes/` | scripts of the fresh-eyes review (closure, parity, winding lemma, T^3, Penrose LP) |

## Engines (verdicts: `../STATUS.md` section 3)

| Module | Direction | Verdict |
|---|---|---|
| `genus_ladder.py`, `beam_ladder.py`, `archive_climb.py`, `level_search.py`, `seed_search.py`, `lns_handle.py`, `ladder_solid.py`, `drift_search.py`, `repair_search.py` | DR1 genus ladder family | DEAD@budget for S0 |
| `normals_first.py`, `kdrift.py`, `chain_normals.py` | DR2 normals first / k-drift; DR14 Q1 | DEAD@budget as climbers; reusable for E02-E03 |
| `solid_exact_search.py`, `solid_search.py`, `solid_search_fast.py` | DR7 solid-first | OPEN-LOW (generator) |
| `period_anneal.py`, `gauss_search.py`, `offset_anneal.py`, `joint_anneal.py` | DR4 closure-first, normal annealers | DEAD |
| `ladder_cma.py`, `ladder_ga.py`, `ladder_ils.py`, `ladder_ng.py`, `ladder_reloc.py`, `ladder4.py`, `anneal.py`, `reloc_descent.py` | DR6 black-box engines, DR15 n = 8 | DEAD |
| `immersion_sat.py`, `immersion_anneal.py` | DR8 / DR11 immersion | OPEN (needs cubing) |
| `geomsat.py`, `exp_n7.py`, `exp_n12.py`, `track4_common.py` | Track-4 geometry-first SAT | historical |

## One-off tests (sprint board ids, `../archive/sprint-board.md`)

`q4_polar.py`, `q5_admissible_all.py`, `q10_core.py`, `q13_tube_planes.py`, `q15_symmetric_planes.py`,
`q16_screw_planes.py`, `q17_winding.py`, `q18_gwas.py`, `szilassi.py`, `szil_test.py`, `szilassi_faceplane_check.py`.
`q10_core.py` is the starting point for ROADMAP E03 (UNSAT cores).

New code: put library functions in an existing CORE module where they belong; put an experiment's own script in
its `experiments/E##-slug/` folder unless it becomes a reusable tool.
