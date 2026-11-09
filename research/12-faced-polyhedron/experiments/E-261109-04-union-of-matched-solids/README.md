---
id: E-261109-04
title: Boolean union of two projectively matched exact solids as a (10, 4) source - Szilassi + Szilassi (k = 4) and Szilassi + tetrahedron (k = 1) (week item 5, I-261108-11 stage 1)
date: 2026-11-09
status: running
direction: [DR19]
origin: [I-261108-11, E-261107-01]
tests: [H-261103-02]
produces: []
preregistered: true
---

> Explore. Pre-registered in `PLAN.md`. The union boundary is read exactly from the cells of the plane arrangement
> (`solid_first.Arrangement`, `evaluate`, `boundary_euler`, `extract_map`).

## Goal

Does the union of two exact solids matched on k face planes give a boundary with 10 simple faces and genus 4, and how
many of the 45 pairs does it make adjacent?

## Next

`PLAN.md`: write `union.py`, the controls, the frozen samples, 8 shards (< 1 core-h).
