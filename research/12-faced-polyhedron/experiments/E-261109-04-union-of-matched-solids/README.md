---
id: E-261109-04
title: Boolean union of two projectively matched exact solids as a (10, 4) source - Szilassi + Szilassi (k = 4) and Szilassi + tetrahedron (k = 1) (week item 5, I-261108-11 stage 1)
date: 2026-11-09
status: done
direction: [DR19]
origin: [I-261108-11, E-261107-01]
tests: [H-261103-02]
produces: []
preregistered: true
verdict: LOW-YIELD@0.03-core-h
concluded: 2026-11-09
---

> Explore. Pre-registered in `PLAN.md`. The union boundary is read exactly from the cells of the plane arrangement
> (`solid_first.Arrangement`, `evaluate`, `boundary_euler`, `extract_map`).

## Goal

Does the union of two exact solids matched on k face planes give a boundary with 10 simple faces and genus 4, and how
many of the 45 pairs does it make adjacent?

## Outcome

Controls pass; 0 of 128 + 128 samples give 10 simple faces with genus 4 (`CONCLUSION.md`).
