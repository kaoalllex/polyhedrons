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
