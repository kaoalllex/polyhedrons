---
id: E-261101-15
title: Cube-and-conquer pilot on 3 types (after E-261101-06 and -09)
date: 2026-11-01
status: planned
direction: [DR8]
origin: [I-261031-02, E-261101-06, E-261101-09]
tests: [H-261101-06, H-261101-01]
produces: []
preregistered: false
---

> Planned. Scores T D F G R: conditional | budget: one night or an Actions matrix. Before any compute: `PLAN.md` from `experiments/_template/` (skill
> `experiment-start`).

## Goal

Refuted fraction per core-hour on type 0, type 58 and one trivial-Aut type.

## Next

Stop rule: one type decided or the matrix exhausted; report refuted fraction per core-hour and the cost of proof
handling. Revised 2026-11-01: the 2,000 core-h threshold is not the gate any more (`ROADMAP.md`, decision table).

## Starting point (2026-11-01)

* Cube on the 44 vertex-type bits (F3: convex iff chi(X, Y, Z, inf) = +1), not on the 220 rank-3 signs: the
  patterns allowed by degree -5, >= 13 saddles and the fold-locus identities of E-261101-21 are far fewer than the
  rank-3 chirotopes, and every refuted cube reads as a lemma about a saddle arrangement. Take the pattern list from
  E-261101-06's models.
* Per cube: CaDiCaL with LRAT, `cake_lpr` on the fly inside the shard, keep cube, verdict and hashes, discard the
  checked proof (the policy of the Keller and Schur-5 campaigns). Shards under 5 h (`PROTOCOL.md` section 6).
* Coordinate with `polyhedraproof` after E-261101-09: same type, both encodings, compare verdict and cost.

## 2026-11-10: edge-convexity bits as the cube basis (I-261110-07)

Proposed replacement of the split basis: the 66 edge-convexity bits instead of the 44 vertex-type bits, if
E-261110-01 confirms on data that the edge signs determine the vertex types (statements 1 and 2 of I-261110-07;
statement 2 is unchecked). No new experiment: this row takes the basis that survives that check.
