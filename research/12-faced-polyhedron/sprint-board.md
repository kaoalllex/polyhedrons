# Hypothesis sprint board

Fast tests (minutes each), many ideas, kill quickly. Verdict: KEEP (worth more compute),
KILL (no signal), DONE (answered). Counts = violated forbidden triples (float, fastviol).
Reference points: best known near-miss 4 (symmetric), 5 (asymmetric); random arrangements 23-39.

| # | Hypothesis | Test (budget) | Result | Verdict |
|---|---|---|---|---|
| G1 | Near-misses are topologically wrong (Gauss degree != -5) | exact prefilter on all 1005 seeds (5 min) | all 1005 fail; own degrees -5..+4, mostly -1..+1 | DONE: key insight |
| G2 | Admissible normals exist | annealing (seconds) | yes, easily (types 0, 5, 58) | DONE |
| G3 | Exact offset SMT is fast when gauge is fixed | z3 on 3 admissible normal sets | UNSAT in 19-90 s (vs >300 s UNKNOWN without gauge) | KEEP: overnight `gnormals` |
| G4 | Gauss clauses speed up OM-SAT | #48 C2, k = 0/2/4, same load | 92 / 100 / 98 s | KILL |
| H-a | Random admissible normals + annealed offsets get close | offsets only, 10 min x 2 types | best 32-39 | KILL (as a seed source) |
| Q4 | Polar duals of a vertex-version near-miss are good face seeds | 20,000 random centres, Dual44 (1 min) | best 32, degree +2 | KILL |
| Q1 | Joint normals+offsets annealing inside the admissible class beats 20 | 8 min x 2 types | best 22 (types 0, 58) | KILL |
| Q2 | Admissible normals nearest to the best asymmetric seed + its offsets | 8 min, seed topology_33 | best 26 | KILL |
| Q5 | Every one of the 59 types has admissible normals | 3 x 30 s annealing per type | running | |
| Q10 | UNSAT cores of the gauge-fixed SMT are small (guide normal moves) | z3 unsat core, type 0 | core = 0 of 176 triples: UNSAT already from LOCAL conditions (gauge + one reflex corner per vertex + orientation consistency) | DONE; refined by fresh-eyes review: the fixed-normal obstruction is COHOMOLOGICAL (36 handle period conditions; without them SAT in < 0.4 s; an LP decides it in seconds) |
| L1 | Near-misses are immersions (locally embedded) | local violation counter on 300 seeds | NO: every one has >= 7 vertices with two reflex corners (Razorcross: 0 crossings, 8 such vertices) | DONE: key insight |
| Q13 | (diff. geometry) tangent planes of a smooth genus-6 surface (tube around K5) are good seeds | 8 samples, CP-SAT best triangulation | best 26 | KILL |
| Q12 | (biology: fragment assembly = local "secondary structure" first) Some type admits a polyhedral IMMERSION | OM-SAT without global clauses, type 0, k = 0 / 2 | no answer in 30 min (both); numerical annealing: best 12 local violations (random starts) | KEEP: overnight `immersion`, hours per type |
| Q14 | Edge convex/reflex 2-colouring (convex vertex: 3 equal; saddle: 2+1) prunes admissible normals | 10 types, SAT | always colourable; admissible normals have 27-33 saddles of 44 | KILL |
| Q12c | Numerical immersion search on types 58, 57, 56 | annealing 60 min each, random restarts | best 12 / 12 / 14 local violations; every value observed is EVEN | explained: parity theorem [P, fresh-eyes]: sum of face self-crossings + sum_v C(r_v,2) = chi (mod 2) — not an obstruction |
| S1 | Independent certified reproduction of the symmetric theorem | user's machine, `sym` job, our encoder + CaDiCaL + drat-trim | all 25 cases (21 C2 classes, 4 C3) UNSAT-VERIFIED, 8-147 s each (console report; results to be pushed) | DONE |
| A1 | Symmetric obstruction is local (immersion-level) | OM-SAT without global clauses on #54 T, #3 D3, #45 C3 | all UNSAT in 1-19 s; D3: simple faces alone UNSAT; T: simple + reflex UNSAT | DONE (sound); caveat: for #48 C2 the immersion instance costs as much as the embedding one (91 s vs 92 s), simplicity essential (without it SAT) |
| A2 | Asymmetric immersion (simple + reflex only) | types 0, 41, 25 min each; type 0 simple-only | simple-only: SAT 527 s; simple + reflex: no answer in 25 min (both types) | KEEP: decided by overnight `immersion` (2.2 h per type) |
| B1 | (architecture: dual-mesh planarization) planes fitted to the dual mesh of the vertex-version near-miss Dual44 | 6 weightings | 53-75 violated triples, ~60 crossings | KILL |
| Q15 | (z.ai #5) symmetric PLANE sets (tetrahedral orbit) with asymmetric triangulations | 24 arrangements, CP-SAT best triangulation | best 24 | KILL |
| C2s | (fresh-eyes #1) immersion for all 21 half-turn classes (+4 C3) | OM-SAT; then DRAT on user's machine | 25/25 UNSAT; night 2: 25/25 UNSAT-VERIFIED | DONE: certified theorem (no symmetric immersion) |
| M1 | Szilassi embryo inside some type | 59 types x 792 7-subsets | max 9 induced triangles (need 13) | KILL (structural fact) |
| M2 | (crystallography) flat 3-torus: periods in a lattice instead of 0 | closure MILP with lattice periods, types 0 and 58 | general lattice: defect exactly 0 (det 414, 49); but faces not simple | closure level only: with SIMPLE faces added (`torus_simple`) both instances are INFEASIBLE in T^3 (116-392 s) and in R^3 (2-3 s) -> face simplicity is an independent, strong part of the obstruction; sweep over more normals/classes running |
| PD | Period-defect annealing in R^3 | type 0, ~1.5 h | 17.6 -> 8.5 | KEEP (night 2 runs all types) |
| Q16 | (current graphs, cross-field round 2, X4) 12 planes = perturbed orbit of a screw motion | 24 samples, CP-SAT best triangulation | best 27 / 28 (random: 23-39) | KILL |
| Q17 | (computer graphics: generalized winding number, Y10) w is constant on arrangement cells; embedding => w in {0,1} | Monte Carlo (40,000 points) and exact octant test at all 220 triple points, 1005 seeds | values -2..3 occur; Monte Carlo misses thin defects (261 seeds look clean at 40k points); exact test: 45 seeds have w in {0,1} at every cell, i.e. their 2-cycle bounds a solid; the inspected ones have 4 face self-crossings (bow-tie faces: one plane carries several lobes) and 12 'multi-reflex' vertices, which are then artefacts of the reversed lobes (interpretation, not yet checked one by one) | DONE: cheap exact classifier; Monte Carlo volume excess is NOT a usable objective (defects are thin) |
| Q18 | (genetics: GWAS, Y7) defects (vertices with >= 2 reflex corners) sit at the same combinatorial positions across seeds of one type | canonical relabeling + automorphism orbits, 12 types with >= 25 seeds | no universal position (max rate 0.55-0.85 per vertex); strong hotspots in symmetric types: type 56 — two orbits of 4 vertices at 83-85 %, all other orbits <= 13 %; type 57 — one orbit of 3 at 76 % | KEEP: test "type 56 immersion with the hotspot vertices single-reflex" by a LOCAL SAT (only nearby faces) -> candidate local lemma |
| R1 | (review 2026-10-30) the genus-4 plateau is a Gauss-class obstruction | T1 gate on the 5 type-0 genus-3 realizations (12 s) | all 15 arms: degree -2 (need -3), k_tau = 0; no admissible gauge (1000-direction confirmation) | DONE: explains the plateau |
| R2 | exact offset solver works on sub-maps | Eval + z3 at own normals of 5 realizations; genus-4 maps at genus-3 normals | 5/5 SAT (96-173 s, exactly EMBEDDED); 3/3 UNSAT for genus 4 | DONE: tool validated |
| R3 | drift inside the realization space reaches k_tau = -1 | kdrift, 15 min per arm, 5 arms | only (0,5,8)-(2,6,7) (A, C), on the class wall; margin pinned at 0 elsewhere | KEEP: night 5 `kdrift` |
| R4 | normals first + exact offsets climbs the ladder | from the class seed, r <= 0.2; control on the realized map | genus 4: all UNSAT; control: SAT only at r = 0.05 | KEEP: night 5 `nfirst` with small radii |

## Queued ideas from distant fields

Round 2 (historical cross-field breakthroughs, 17 ideas X1-X6, Y1-Y11): see `cross-field-ideas.md`.

| Field | Correspondence | Concrete test |
|---|---|---|
| Astronomy: gravitational lensing image-counting (odd-number theorem) | Gauss-map degree = signed count of "images" (vertices whose normal cone contains a direction) | used in G1; look for lensing "magnification invariants" giving further identities |
| Astronomy: star-tracker geometric hashing | match a set of 12 normals to the labeling/type that makes it admissible | hash triangle-orientation patterns of normal sets vs the 59 types |
| Biology: protein fragment assembly (Rosetta two-stage) | stage 1 immersion (local), stage 2 embedding (global) | Q12, then embedding search seeded from immersions |
| Population genetics: island models, neutral networks | parallel populations with migration; drift on plateaus | engineering for any annealer that shows signal |
| Cosmology: genus statistics of excursion sets; graphics: CSG | solid = Boolean function of the 12 half-space signs (union of chambers); read-once formulas | is Szilassi read-once in its 7 half-spaces? |
| Ecology / geometry: mutually touching bodies (Tietze, Littlewood's 7 cylinders) | "every pair touches" problems; Voronoi cells of points on the moment curve are pairwise adjacent | look for a moment-curve-type ansatz for the 12 planes |
