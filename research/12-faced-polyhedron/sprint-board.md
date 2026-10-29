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
| Q1 | Joint normals+offsets annealing inside the admissible class beats 20 | 8 min x 2 types | running | |
| Q2 | Admissible normals nearest to the best asymmetric seed + its offsets | 8 min, seed topology_33 | running | |
| Q5 | Every one of the 59 types has admissible normals | 3 x 30 s annealing per type | running | |
| Q10 | UNSAT cores of the gauge-fixed SMT are small (guide normal moves) | z3 unsat core, type 0 | running | |
