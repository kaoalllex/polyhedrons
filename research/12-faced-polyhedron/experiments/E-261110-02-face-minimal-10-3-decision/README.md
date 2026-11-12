---
id: E-261110-02
title: (10, 3) face-minimal decision - the duals of the 20 vertex-minimal genus-3 triangulations, single adjacencies
date: 2026-11-10
status: planned
direction: [DR19, DR8]
origin: [I-261110-02, E-261103-02, E-261103-03]
tests: [H-261110-03, H-261110-01]
produces: []
preregistered: true
---

> Planned. Scores T D F G R: 2 2 2 2 2, jump 2 | budget: 1 prep session + one owner night, <= 80 core-h, 10 shards.
> `PLAN.md` is committed. The approved night now follows ninth-plane cells and the 2026-11-12 bridge gate;
> it starts only after the prep amendment with input hashes and passing formula/realization controls.

## Goal

Decide the plain formula of each of the 20 maps (10 faces, 28 vertices, 42 edges, 42 of 45 pairs adjacent, every
adjacency single) with `submap=True`, kissat and checked DRAT. A SAT model that realizes is a new polyhedron of the
target S6; 20 UNSAT-VERIFIED formulas are a conditional face-minimality statement for genus 3 in the cubic
single-adjacency class (I-261110-02). Never reported as S0 or S5.

## Next

`PLAN.md`, including its 2026-11-12 amendment. First the (10,2) formula and foreign-model bridge controls. Prep: `code/lutz_import.py`, the (7, 1) and (12, 6) controls, the two-map pilot, the
smoke test of the owner's entry point, amendment 1 with hashes. Stop rule: all 20 maps recorded, a failed control, or
the 80 core-h cap.
