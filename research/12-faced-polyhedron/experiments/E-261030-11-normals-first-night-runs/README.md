---
id: E-261030-11
title: Normals first, k-drift and direct genus 6 at scale
date: 2026-10-30
status: done
direction: [DR2]
origin: [I-261030-24, I-261030-25, I-261030-28, E-261030-08]
tests: [H-261101-04, H-261029-09]
produces: []
verdict: LOW-YIELD@150 core-h
preregistered: false
---

> Reconstructed on 2026-11-01 from `experiment-log.md`, `results.md` and the night reports; not pre-registered.

## Goal

Climb by normals first and k-drift from every gated arm; try genus 6 directly from random admissible normals.

## Method

Laptop nights 4-5, job `n5` (nfirst : kdrift : g6 = 4 : 4 : 1, z3 timeout 600 s); `overnight/analyze_n5.py`.

## Results

432 tasks, 12,202 exact UNSAT offset decisions, 0 SAT, no timeouts (radius 0: 80, 0.02: 2142, 0.05: 2657, 0.1: 2855, 0.2: 2982); k-drift reached the class 153 times, hemisphere margin exactly 0 every time. Records: `results/n5/`.

## Conclusions

EXACT per instance, low power as evidence (control SAT only at r = 0.05, one trial); report `reports/NIGHT_REPORT_2026-11-01.md`.

## Next

Power study (planned E-261101-04), UNSAT cores at r = 0 (planned E-261101-05), pinned margin (planned E-261101-07).
