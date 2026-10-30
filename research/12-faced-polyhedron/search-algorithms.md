# Search algorithms: what we have tried and what to try later

Test bench: the ladder (`code/ladder*.py`). With 7 faces (Szilassi) every engine has to succeed, and
it does. With 8 faces (genus 2) every engine has so far stopped at 1-2 violations. An engine that
solves 8 faces is the one to point at 12. Every float zero is re-checked with `code/ladder_exact.py`.

## Tried (2026-10-29)

| Engine | n = 7 (Szilassi) | n = 8 best | Notes |
|---|---|---|---|
| simulated annealing, one plane per move (`ladder.py fast`) | seconds, 5/5 exact | 1 (one map), else 2 | 15+ maps, 4-10 min per map |
| exact single-plane relocation (`ladder_reloc.py`) | - | 2 (true local minimum for one-plane moves) | 56-hyperplane arrangement per plane |
| ILS with multi-plane kicks (`ladder_ils.py`) | - | 2 | 379 kicks |
| genetic algorithm, island model (`ladder_ga.py`) | 15 generations, exact | 1 (seeded), 3 (unseeded, 10 min) | crossover by plane = gene |
| CMA-ES with BIPOP-like restarts (`ladder_cma.py`, cma 4.0.0) | 2 restarts, exact | 1 (seeded), 2, 2, 2 | first run found float 'zeros' = scale collapse (all planes nearly concurrent); rejected by the exact check; guard added |

**Reading (2026-10-29):** four different engines all stop at 1-2 violations for 8 faces, while
the same engines solve 7 faces at once. Either the 8-face rung (doubled adjacencies) is obstructed
or much harder; settle it exactly (SAT on 9 elements) or switch the rung (two 4-valent vertices).

## To try later (user's list, 2026-10-29, from another AI, plus our notes)

1. **CMA-ES** as the baseline for comparison (done, see above).
2. **Differential Evolution** (scipy.optimize.differential_evolution, or Nevergrad's DE): a different
   global-search mechanism (difference vectors between population members).
3. **Nevergrad NGOpt** (https://facebookresearch.github.io/nevergrad/): automatic choice among many
   optimizers; cheap to plug in, since the fitness `pair_energy` is a black box.
4. **L-BFGS / nonlinear least squares with gradients** (scipy least_squares, Levenberg-Marquardt).
   Caveat: our conditions are mostly inequalities and combinatorial (simple faces, faces meeting only
   in their shared edges), so the current energy is piecewise constant. To use it we need a SMOOTH
   formulation, e.g. variables = vertex positions + planes, equations = vertices on their three planes
   (F(x) = 0, smooth), inequalities = margins (distance of each forbidden triple point from the
   faces, edge-crossing separations) as smooth penalties or barrier terms, then LM / L-BFGS from
   many starts. For fixed normals the closure equations are already linear (`period_defect.py`).

Our own list of modern "search for the unknown" methods, for the same bench:
5. **Quality-diversity (MAP-Elites) / novelty search**: keep an archive of the best configuration per
   behaviour cell (e.g. number of saddle vertices x which faces carry the defect) instead of one
   population chasing one objective; made for deceptive plateaus like ours.
6. **Cross-entropy method** (as in Wagner 2021, "Constructions in combinatorics via neural networks",
   which found counterexamples to graph-theory conjectures): sample, keep the elite fraction, refit
   the sampling distribution.
7. **Difference map / RRR** (Elser): a feasibility engine, not an optimizer (cross-field-ideas Y2).
8. **Parallel tempering / population annealing / nested sampling** (astronomy): sample the level sets
   E <= k with a population; also estimates how rare a solution is (cross-field-ideas Y3).
9. **Large neighbourhood search with an exact solver**: free 2-3 planes, solve that subproblem
   exactly (OM-SAT or CP-SAT), keep the rest fixed (next-steps.md "SAT-LNS").
10. **Monte Carlo tree search / AlphaZero-style construction**: build the configuration plane by plane
    or sign by sign with learned value estimates.
11. **LLM-guided program search (FunSearch, AlphaEvolve)**: evolve programs that GENERATE plane sets
    (cross-field-ideas X6).
12. **Homotopy continuation** (numerical algebraic geometry: Bertini, HomotopyContinuation.jl):
    follow a path from a solvable configuration (e.g. a smooth surface or a torus-relaxed one) to
    planar faces, with path tracking instead of random search.
13. **Bayesian optimisation with a surrogate**: for expensive objectives such as the simple-defect MILP
    (minutes per evaluation); not useful for the cheap ladder energy.

## Evaluation of the "AI-driven polyhedron discovery engine" brainstorm (user, 2026-10-30)

Key fact for every point: for OUR target (12 faces, every two adjacent) the combinatorial topology
is not open. The dual map must be one of exactly 59 neighbourly genus-6 triangulations (enumerated
twice). So "discovering new topologies" at the top level is done; the discrete freedom that matters is
(a) which sub-maps we climb through (the lattice of handle subsets of each type; dead ends vs
extendable), (b) which realization of a level we start from, (c) the oriented-matroid / isotopy class
of the embedding (twisted, knotted tunnels). Evidence 2026-10-30: discrete choices alone (branching
over handles + a second genus-3 realization) moved genus 4 from 8 to 2 violations in two hours.

| # | Proposal | Verdict for this problem | What to take |
|---|---|---|---|
| 1 | LLM hypothesis generation + tree search over graphs | low for the 12-face target (topologies enumerated); useful as an idea source, never as a validator | keep using LLM agents for ideas; no LLM in the inner loop |
| 2 | Two-level evolution: discrete topology + continuous CMA-ES | **high**, it is what works now: discrete = handle lattice + realization archive, continuous = annealing / CMA-ES | formalize: population of (type, sub-map, realization) with mutations add / remove / swap a handle |
| 3 | Bayesian optimization as scheduler | **medium-high** as a bandit (successive halving / UCB over arms), not a GP: arms are discrete and the start energy is already a good prior (17 -> 4, 27 -> 7) | successive halving over (realization, handle) arms with fixed CPU budget |
| 4 | AlphaEvolve-style evolution of the search code | medium-low now: costly; needs a benchmark (we have one: ladder n = 7 and the genus 3 -> 4 step) and the exact verifier as the only judge (reward hacking happened three times) | later, small budget |
| 5 | Independent exact verification, novelty check | already in place (rational verifiers, Euler / genus, type identification); gap: second independent implementation | adversarial-verifier agent on any genus >= 5 result |
| 6 | QUBO / quantum | not useful: the discrete layer is small, CP-SAT / SAT are far stronger on these constraints | skip |

Warning carried over: "near-zero defect" is not progress by itself (night 2: 9 zero closure defects,
all false). Only an exact zero of the full conditions counts; report the exact violation count.

Smallest proof of concept (planned): on type 0, equal CPU budget (e.g. 4 core-hours), compare (i) the
fixed chain, (ii) branching ladder, (iii) branching + realization archive + successive halving.
Metric: highest exactly realized genus and the best violation count at the next genus.
