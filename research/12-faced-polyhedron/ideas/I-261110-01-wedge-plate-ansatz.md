---
id: I-261110-01
title: Wedge-plate ansatz - 2m faces as m thin wedges; mutual piercing gives the adjacencies, a pierced rim a doubled pair
date: 2026-11-10
status: open
direction: [DR12, DR18, DR7]
origin: [owner, L:roestvigh2026, L:mizhaev2026, I-261101-20, I-261030-01]
---

## Idea

Take 2m face planes as m wedges: pairs of planes (n_i, d_i), (n_i', d_i') at a small angle, meeting in a rim line
L_i. Mechanism (derivation sketch of the 2026-11-10 session, **not checked**; to be written and tested before use):

* two thin wedge-shaped plates that pierce each other realize all four adjacencies between their faces along one
  bundle of lines;
* the rim realizes the fifth adjacency of each wedge;
* a rim pierced by another plate is a doubled adjacency (targets S1 and the genus-free relaxed targets,
  I-261110-03); an unpierced rim is a single adjacency (S6, S0).

No parameter is saved: two planes are a mid-plane, a rim line in it and an angle, 6 numbers either way. The gain is
combinatorial. In the thin limit the chirotope is fixed by the arrangement of the m mid-planes (6 planes have a few
dozen affine types) and by the position of each rim line among the m - 1 trace lines of its mid-plane. The search
splits into a small arrangement and m line placements, and a 12-plane sampler can be biased towards the arrangements
that have six disjoint sharp pairs.

## Why it might help

Evidence is weak and is recorded as such (NUMERICAL, a read-only float computation of the 2026-11-10 session on the
published coordinates; tables, controls and the null model: `reviews/HANDOFF_PROMPT_2026-11-10-wedges.md` §2; the
script is not in the repository, E-261110-01 re-runs it from committed code):

* in Szilassi, Roest-Vigh and Mizhaev the sharpest convex edges form a set of disjoint face pairs (3 of 7 faces
  paired, 4 pairs, 4 pairs); in both 8-face objects these four rims are doubled adjacencies;
* the null model says the matching itself is close to chance: any 7 isotropic planes contain Szilassi's three pairs
  in about half the samples, and a two-orbit D2 family contains four pairs at Roest-Vigh's angle in about half. **The
  wedge structure is not a supported regularity** and must not be cited as one (`CLAUDE.md`: a diagnostic is checked
  on controls before a phenomenon is named);
* what remains is a sampling fact: isotropic samplers give F/2 disjoint sharp pairs in about 0.5 % of 8-plane and
  0.4 % of 12-plane arrangements, two-orbit symmetric families in about half. If wedges matter, isotropic sampling
  at 12 planes wastes two orders of magnitude; whether they matter is open.

Not claimed: that the (9, 3) solid-first sweeps lacked wedges (200 of the 300 arrangements of E-261108-01 were built
on the Roest-Vigh and Mizhaev planes, which contain them; those sweeps are explained by the (9, 3) exclusion).

## Cheapest test

E-261110-03 (arrangement families at the 8-plane rung, where the answers are known), with the wedge covariate of
E-261110-01 recorded per arrangement. Kill: inside one symmetry family, arrangements with F/2 disjoint sharp pairs
contain an all-pairs solid no more often than the others (ratio < 2 with >= 10 positives in total); the idea is then
parked with its measured rate. Hypothesis: H-261110-02.

## Source

Handoff of the 2026-11-10 strategy session (`reviews/HANDOFF_PROMPT_2026-11-10-wedges.md` §2, §4 I-A); filed by
`reviews/strategy-review-2026-11-10.md`.
