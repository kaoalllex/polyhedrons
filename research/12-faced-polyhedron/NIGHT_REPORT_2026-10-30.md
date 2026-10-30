# Night report 2026-10-29/30 (autonomous session)

## Headline
Our own new engine — **solid-first search with an exact CP-SAT inner step** — finds, from random
planes and without fixing any combinatorial type:
* the Szilassi polyhedron (7 faces, all pairs adjacent) in 45 s (exactly verified);
* **12-face embedded polyhedra of genus 2 and genus 3** (42 and 48 of the 66 pairs of faces adjacent),
  exactly verified (`experiments/solid_first/`, picture `figures/genus3_12faces.png` / `.html`).
The target is genus 6 (66 pairs). The search currently plateaus at genus 3; runs continue.

## What was done (chronologically)
1. Ladder rung 8b (two 4-valent vertices): 23 maps, best 2 violations (both n = 8 rungs plateau).
2. Solid-first formulation (always-embedded solids; face-structure objective); validated on Szilassi
   (0) and on the 45 embedded imported seeds (12). Greedy search trapped at 4 on n = 7 (topology).
3. Topology macro-moves (tunnel / handle) + Euler-characteristic target: Szilassi found without map.
4. Numba evaluator (150x faster).
5. Thesis-advisor subagent: critique and ranked directions (see `experiment-log.md`); correction:
   Mizhaev's octahedron (genus 3) already has 8 mutually adjacent faces; verified with our tools.
6. Genus ladder (sphere + 6 handles via tube removal; map-fixed climb): type 11 realized up to genus 2.
7. Exact CP-SAT inner step (manifold, <= 1 edge per pair, one disk face per plane via Euler
   characteristic + no pinches): Szilassi from random planes in 45 s; n = 12 climbs to genus 3.
8. Secondary score (slack of the best next-genus attempt) and guided plane moves to see "almost
   one more handle".

## Numbers
* Random 7-plane arrangements: 2000 of 2000 admit only a genus-0 solid (P(Szilassi) < 1/2000),
  yet directed search finds Szilassi in under a minute.
* n = 12 exact-inner runs: genus 1 within ~30 s, genus 2 within ~1-4 min, genus 3 after ~6 min (one
  run of four); no genus 4 after ~1.5 h so far (best next-genus slack 13).

## Key insight of the night: dead-end maps
Attaching a handle = a tube (6-triangle annulus) between two disjoint triangles of the dual map with
six new adjacencies (`code/handle_add.py`). Maps on the tube chains of the 59 neighbourly types reach
all 66 adjacencies by such steps (checked). **Every polyhedron found by the free-type solid search is a
dead end**: genus-1 maps reach at most 60, genus-2 maps 54-60, genus-3 maps 54. So the free search
was climbing the wrong mountains; climbing must stay on extendable maps (the chains), e.g. the
map-fixed genus ladder (frontier so far: genus 2, type 11). Four ladders (types 11, 4, 54, 9,
15 min per level) are running.

## Later in the night
* Genus ladders (map-fixed, extendable by construction) on types 11, 4, 54, 9 with a stronger
  per-level search: frontier genus 2 (types 4 and 11 exactly), genus 3 at 4-5 violations.
* Exact-solid ladder steps toward a prescribed next-level adjacency graph: soft slack decreased
  (16 -> 10, 99 -> 14) but no zero.
* Continuous crossing depth added to the honest energy (tie-breaker): small gains, no zero; n = 8
  plateau unchanged (1).
* Night-2 `pdefect` (user's machine) finished: 9 zero-defect normal sets, all non-simple (false).

## Next
* Run night 3 (genus ladder over all 59 types) on the user's machine: which types climb highest.
* Climb only on extendable maps (chains); combine the exact solid solver with the chain targets.
* Speed and strength of the inner CP-SAT at n = 12 (it does not prove optimality within 60 s).
* Advisor's remaining directions: IPC planarization flow, continuous violation depth, OM-SAT n = 8.
