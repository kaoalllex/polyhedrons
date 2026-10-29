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
| Q10 | UNSAT cores of the gauge-fixed SMT are small (guide normal moves) | z3 unsat core, type 0 | core = 0 of 176 triples: UNSAT already from LOCAL conditions (gauge + one reflex corner per vertex + orientation consistency) | DONE: local structure is the bottleneck |
| L1 | Near-misses are immersions (locally embedded) | local violation counter on 300 seeds | NO: every one has >= 7 vertices with two reflex corners (Razorcross: 0 crossings, 8 such vertices) | DONE: key insight |
| Q13 | (diff. geometry) tangent planes of a smooth genus-6 surface (tube around K5) are good seeds | 8 samples, CP-SAT best triangulation | best 26 | KILL |
| Q12 | (biology: fragment assembly = local "secondary structure" first) Some type admits a polyhedral IMMERSION | OM-SAT without global clauses, type 0, k = 0 / 2 | running | |

## Queued ideas from distant fields

| Field | Correspondence | Concrete test |
|---|---|---|
| Astronomy: gravitational lensing image-counting (odd-number theorem) | Gauss-map degree = signed count of "images" (vertices whose normal cone contains a direction) | used in G1; look for lensing "magnification invariants" giving further identities |
| Astronomy: star-tracker geometric hashing | match a set of 12 normals to the labeling/type that makes it admissible | hash triangle-orientation patterns of normal sets vs the 59 types |
| Biology: protein fragment assembly (Rosetta two-stage) | stage 1 immersion (local), stage 2 embedding (global) | Q12, then embedding search seeded from immersions |
| Population genetics: island models, neutral networks | parallel populations with migration; drift on plateaus | engineering for any annealer that shows signal |
| Cosmology: genus statistics of excursion sets; graphics: CSG | solid = Boolean function of the 12 half-space signs (union of chambers); read-once formulas | is Szilassi read-once in its 7 half-spaces? |
| Ecology / geometry: mutually touching bodies (Tietze, Littlewood's 7 cylinders) | "every pair touches" problems; Voronoi cells of points on the moment curve are pairwise adjacent | look for a moment-curve-type ansatz for the 12 planes |
