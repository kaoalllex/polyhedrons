---
id: I-261101-08
title: Arrangement first - symmetric plane arrangements with asymmetric solids, decided exactly per arrangement
date: 2026-11-01
status: open
direction: [DR7, DR18]
origin: [I-261030-07, I-261029-27, FD5, L:roestvigh2026, L:mizhaev2026]
---

## Idea

FD5 excludes symmetric *polyhedra*: planes and solid invariant under the same isometry. It says nothing about a
symmetric *arrangement* of 12 planes carrying an *asymmetric* solid (a union of chambers that the group does not
preserve). For a fixed arrangement the question is finite and exact: `code/solid_cpsat.best_solid(A, target_adj=66)`
decides whether any all-adjacent cubic solid exists on these planes (every one of the 59 types at once), and the
plain maximisation gives the best genus the arrangement supports. So: build a catalogue of structured
arrangements and decide each one.

Catalogue, in order of cost:
1. arrangements invariant under a group acting freely on the 12 planes: A4 (one orbit, 3 parameters), S3 and D3
   (two orbits), D2 and the C4 rotoreflection S4 (three orbits), C3 (four orbits), C2 (six orbits); sweep the
   1-3-parameter families on a grid, sample the larger ones;
2. the 247 archived arrangements (`experiments/E-261030-10-realization-archive-climb/results/arch/archive.json`),
   asking for 54 or more adjacent pairs (a different solid on a known good arrangement);
3. the 1005 near-miss arrangements (`overnight/data/seeds.json`): their maps are in the wrong Gauss class, their
   arrangements may carry other solids;
4. random perturbations of every hit.

Filters before the solver (seconds): no two normals antipodal (adjacent faces cannot be parallel, and every pair is
adjacent); the 12 normals not in an open hemisphere (covering, FD7); general position.

## Why it might help

The only 8-face all-adjacent polyhedra known (Mizhaev, Roest-Vigh) live on symmetric two-orbit arrangements. The
Wendel estimate (`reviews/fresh-eyes-review.md` 2.3) says random arrangements almost never carry a closed
all-adjacent solid; structured arrangements concentrate the incidences. And the loophole is real: nothing certified
excludes an asymmetric solid on a symmetric arrangement. Cross-field: crystallographic point groups as a sampling
scheme; tiling and Ising-type cell-selection CSPs.

## Cheapest test

100 A4 and D2 arrangements x `best_solid` with a 60 s limit: does the maximal adjacency exceed 48 anywhere? If it
never reaches 48 on arrangements that are known to carry a genus-3 solid (catalogue item 2), the solver settings are
wrong, not the idea.

## Source

Strategy review 2026-11-01 (`reviews/strategy-review-2026-11-01.md` section 3 and 7, direction 4 made concrete).
