# Protocol of solution-search methods (state 2026-10-30)

One page: every method used so far, what it is, how far it got, and what is next. Details and
dates: `experiment-log.md`; engines on the small test bench: `search-algorithms.md`; all directions
at a glance: `figures/research-map.png`. Target: 12 planar faces, all 66 pairs adjacent = an embedded
polyhedron of genus 6 (V = 44, E = 66). Progress measure: the number of adjacent pairs of faces of an
EXACTLY verified embedded 12-face polyhedron (30 + 6 g; genus g).

**Best so far:** genus 3 (48 of 66 pairs), exactly verified, several times: a free solid-first result
(dead end: it cannot be completed by attaching handles) and, since 2026-10-30, a type-0 genus-ladder
result that is still extendable to 66 (`experiments/genus_ladder/type0_genus3_extendable.json`).

Verdict scale: **works** (reached a new level), **partial** (gives information or a plateau),
**no** (did not help), **proof** (impossibility side).

## A. Formulations (what is searched)

| Method | What it is | Best result | Verdict | Prospects |
|---|---|---|---|---|
| Face-plane reduction | unknowns = 12 planes (48 numbers); vertices = triple points; Lemma 5.1 | basis of everything | works | - |
| Map-fixed search | fix one of the 59 neighbourly maps, find planes; honest pair energy | near-misses with 1-5 violations (genus 6 directly) | partial | used inside the ladder |
| Period-defect MILP (night 2) | choose normals, closure of the faces as linear equations | 9 zero-defect normal sets of 170, all with non-simple faces | partial (necessary condition only) | combine with simple faces (`sdefect`) |
| Smaller analogues (ladder n = 7, 8) | same problem with 7 / 8 faces as a test bench | n = 7 (Szilassi) solved by every engine; n = 8 stuck at 1-2 | partial | n = 8 rungs are poor analogues (advisor) |
| Solid-first | state = planes + set of cells of the arrangement, always embedded; objective = face-structure defects | Szilassi from random planes without a map | works (n = 7) | basis of the exact-inner engine |
| Solid-first + exact CP-SAT inner step | for fixed planes CP-SAT picks the best solid (manifold, one disk face per plane, at most one edge per pair) | **n = 12 genus 3 (48 pairs), exact**; plateau at 48 | works, then dead ends | add the extendability penalty (`--reach`) |
| Genus ladder (sphere + 6 handles) | remove 6 handles (tubes) from a neighbourly map to a sphere; realize genus 0, 1, 2, ... seeded from the level below | type 11 genus 2; **type 0 genus 3, extendable** | works | night 3 over all 59 types |
| Branching ladder + realization archive | from a realized level, try every next handle that keeps all 66 pairs reachable; several realizations of the same level | type 0: 4 genus-3 realizations; genus 4 honest plateau at 4 violations | partial | in night 3 (`--branch-minutes`) |
| Target-graph exact step | exact solid solver aiming at the next level's adjacency graph | slack 16 -> 10, no zero | partial | run from the extendable genus-3 polyhedron |

## B. Engines (how it is searched)

| Engine | n = 7 | n = 8 / n = 12 | Verdict |
|---|---|---|---|
| Simulated annealing, one plane per move | seconds | n = 8: 1; inside the ladder: realizes genus 0-3 | works (workhorse) |
| Exact single-plane relocation | - | n = 8: 2 (true local minimum) | partial |
| Iterated local search with kicks | - | n = 8: 2 | no |
| Genetic algorithm, island model | exact | n = 8: 1 seeded, 3 unseeded | partial |
| CMA-ES (BIPOP-like restarts) | exact | n = 8: 1-2; half of every ladder level | works |
| Nevergrad NGOpt / DE | NGOpt exact in 379 evaluations; DE no | n = 8: 2-5 | no (worse than annealing / CMA) |
| CP-SAT inner solid solver | Szilassi in 45 s from random planes | n = 12: genus 3 | works |
| Secondary score / guided moves / dead-end penalty | - | shows "almost one more handle" (slack) | partial |
| Beauty polishing | - | removes spikes keeping the structure | works (presentation, robustness) |

## C. Exact verification (every candidate passes all of these)

`code/ladder_exact.py` (rational arithmetic: simple faces, every pair of faces meets exactly in its
shared edges), `code/verify_solid.py`, `code/planes.py` check_embedding. They caught every float
exploit so far (merged collinear edges, scale collapse, shared edge through a 4-valent point).

## D. Impossibility side

| Method | Result | Verdict |
|---|---|---|
| No symmetric embedding (C2, C3; SAT with DRAT certificates) | 25 of 25 cases UNSAT, certified (night 2) | proof |
| No symmetric immersion (same, without global clauses) | 25 of 25 UNSAT, certified | proof |
| Asymmetric immersion OM-SAT (`immersion`) | 8 of 8 runs TIMEOUT | open |
| Gauss-degree filter, parity theorem, local curvature lemma | restrictions on normals / signs | proof (partial) |
| Cube-and-conquer on the full asymmetric instance | not run yet | open |

## E. Not tried yet (ranked by expected value)

1. Branching ladder at scale (night 3) and target-graph exact steps from extendable polyhedra.
2. Large-neighbourhood search with an exact solver: free the 6 planes of the next handle, solve
   that subproblem exactly (CP-SAT / OM-SAT), keep the rest.
3. Spine-seeded solids (user's idea 2026-10-30, `cross-field-ideas.md` round 2e): start from a
   thickened spatial graph of cycle rank 6 (K5, K3,4, knotted or branching tunnels).
4. Quality-diversity (MAP-Elites) over (genus, extendability, beauty) to keep many different
   realized polyhedra instead of one best (started by hand: 4 genus-3 realizations of type 0).
5. Flips through degenerate limits (singularity / branch idea, round 2f): every stalled search
   that collapses an edge points to a 2-2 flip of the map; test the valid flips.
6. Difference map / RRR, nested sampling, cross-entropy method, MCTS, homotopy continuation,
   LLM-guided program search (FunSearch-style) - see `search-algorithms.md` 6-13.
7. Impossibility: cube-and-conquer, second independent encoder, LRAT checking.

## F. Lessons

* Every engine solves 7 faces; 12 faces need structure, not a stronger black box (advisor).
* Climbing must stay on maps that can still be completed: free search finds genus 3 but always
  in dead-end maps; the genus ladder keeps extendability by construction.
* Every float "solution" must pass the exact check; zero defects of necessary conditions
  (night 2) are not solutions.

## Own method: GCL, the Gauss-class ladder (2026-10-30)

Assembled from this project's own pieces (none taken from the literature): (1) the genus ladder with tube
decomposition and extendability (`genus_ladder.py`, `handle_add.reach`); (2) the Gauss-degree statement with
positive covering for every genus (theory-notes F7). CORRECTION of wording: the statement itself is a
polyhedral form of a CLASSICAL fact (degree of the Gauss map = chi/2, Hopf / Gauss-Bonnet; polyhedral
versions in the spirit of Banchoff 1967; covering = the maximum of a linear function is attained at a convex
vertex). What is ours: the exact formulation from the face planes' normals alone (signs of 3x3 determinants,
orientation gauge), its use as an exact necessary filter independent of the offsets, the proof write-up for
this setting, and the per-level / per-handle use (controls: Szilassi, five type-0 genus-3 realizations,
Röst-Vígh's polyhedron) used as a per-level gate, with the handle decomposition
D_{M+tau} = D_M + k_tau (review 2026-10-30); (3) drift inside the realization space of level g toward the
class of level g+1 (`kdrift.py`); (4) normals first, then the offsets decided EXACTLY by the sub-map OM-SMT
(`normals_first.py`, `fixed_normals_gauge.py`, positive control `nf_control.py`); (5) exact rational
verification of every claim (`ladder_exact.py`). Status: implemented and tested on type 0 (night 4 runs it
on all night-3 realizations); variant P1 (projective ladder) proposed.
