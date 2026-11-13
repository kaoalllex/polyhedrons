---
id: E-261110-02
title: (10, 3) face-minimal decision - the duals of the 20 vertex-minimal genus-3 triangulations, single adjacencies
date: 2026-11-10
status: running
direction: [DR19, DR8]
origin: [I-261110-02, E-261103-02, E-261103-03]
tests: [H-261110-03, H-261110-01]
produces: []
preregistered: true
---

> Prep done (PLAN amendment 2, 2026-11-13): bridge gate and controls pass, pilot recorded; the approved night is ready.
> Scores T D F G R: 2 2 2 2 2, jump 2 | budget: one owner night, <= 80 core-h, 10 shards.

## Goal

Decide the plain formula of each of the 20 maps (10 faces, 28 vertices, 42 edges, 42 of 45 pairs adjacent, every
adjacency single) with `submap=True`, kissat and checked DRAT. A SAT model that realizes is a new polyhedron of the
target S6; 20 UNSAT-VERIFIED formulas are a conditional face-minimality statement for genus 3 in the cubic
single-adjacency class (I-261110-02). Never reported as S0 or S5.

## Next

The owner's night: `bash research/12-faced-polyhedron/overnight/launch.sh 10-02 start` (then `status`, `stop`), on AC
power. Afterwards `python3 summary.py` and `experiment-conclude`. Prep evidence: `prep/` (bridge gate, controls (b) and
(d), pilot, startup check); inputs: `maps/` (from `literature/lutz-manifold-page/` by `code/lutz_import.py`), `queue.json`.
