# External AI reviews: received answers and our assessment

## ChatGPT on Prompt 1 (Gauss-map degree argument)

Verdict: claims (i) and (ii) correct; the argument needed an explicit LOCAL LEMMA (area of the
normal triangle = |angle deficit|, sign det = sign deficit) and a careful definition of
"generic" directions. Status: lemma proved and checked numerically (theory-notes.md, "Local
lemma"); genericity is automatic in general position.

## z.ai on Prompt 2 (10 new approaches) — assessment

| # | Proposal | Assessment |
|---|---|---|
| 1 | Gauss–Morse: degree, covering, Morse index identities | degree + covering done; Morse/Banchoff identity c0 - c1 + c2 = chi holds for ANY surface with simple faces (no new constraint) |
| 2 | Fix normals, solve offsets exactly | done (`fixed_normals.py`, `gnormals`); note: with fixed normals ALL conditions (simplicity too) are linear in the offsets, not cubic |
| 3 | Polar pipeline over centres | tested (Q4, best 32); the general version is equivalent to the original problem |
| 4 | Genus ladder (g = 7 with six 4-valent vertices) | nice interpretation (local overlap ~ attempted 4-face corner); a different problem; resolution of 4-valent vertices cannot produce g = 6 (adds a second edge to an adjacent pair) |
| 5 | Symmetric PLANE arrangements with asymmetric triangulations | genuinely new loophole of the symmetric theorem; tested as Q15 |
| 6 | Chirotope SAT | done (Track 3 + prior work); note: face version has 13 elements and is not acyclic |
| 7 | Automated final polynomials (SDP) | relevant only if an OM-SAT instance turns out SAT |
| 8 | Monodromy / chamber enumeration on 3-slices | our exact single-plane relocation already enumerates 3-dim slices exactly |
| 9 | Lasserre moment–SOS | heavy; fixed-normal slices are already exact SMT(LRA) |
| 10 | GPU search with topological losses | essentially Q1 (inside the admissible class: best 22) |

## ChatGPT, "10 crazy ideas" (second round) — assessment

| # | Proposal | Assessment |
|---|---|---|
| 1 | Repair the last 2 intersections of the best near-miss (Bokowski–Kevin H. Kepler–Poinsot model) | refuted as a strategy: near-misses have the wrong Gauss degree and >= 7 local overlaps; the degree is a topological invariant; exact single-plane relocation found no improvement |
| 2 | Consistent cycles in the 12 line arrangements | = geometry-first SAT (Track 4); per-face decomposition is on the roadmap |
| 3 | Walk across critical configurations | = exact single-plane relocation (cell enumeration) |
| 4 | Spherical covering P >= 1, N >= 6 | have it (Gauss prefilter); admissible normals exist; the stronger obstruction is cohomological (period defect) |
| 5 | Oriented matroids | done (Track 3, 25 certified symmetric cases) |
| 6 | Degenerate boundary configurations | boundary of the same solution set; equality constraints, not easier |
| 7 | Maximally asymmetric search | all our searches are asymmetric; symmetric realizations are excluded (certified) |
| 8 | Higher-dimensional shadow | fails for planar faces: twelve 2-planes in R^4 meeting pairwise in lines lie in a common 3-space |
| 9 | CAD plate model | equivalent to numerical search with collision checks |
| 10 | Normals first with the right covering, then offsets | = current pipeline (Gauss-admissible normals, period defect, exact offset SMT; night 2) |
