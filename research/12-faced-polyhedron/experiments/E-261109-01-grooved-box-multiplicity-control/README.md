---
id: E-261109-01
title: Grooved-box multiplicity control - does the S5 encoder accept a real embedded polyhedron with a face pair sharing 3 and 4 segments
date: 2026-11-09
status: done
concluded: 2026-11-09
verdict: FOUNDATION (m = 3 and m = 4 pinned positives SAT, swapped-pairing negatives UNSAT-VERIFIED; unpinned k = 2 SAT)
direction: [DR19]
origin: [E-261103-02, E-261103-03, I-261108-04]
tests: [H-261101-07]
produces: []  # a control; no FD / W / C
preregistered: true
---

> Week plan item 1 (`ROADMAP.md`, lead review 2026-11-08d, amended by 08e). Scores T D F G R: 2 2 2 2 2. Design: `PLAN.md`.

## Goal

Positive control of the E-261103-02 encoder for a pair of faces that shares m >= 3 collinear segments (k = 2: m = 3,
12 faces; k = 3: m = 4, 15 faces), and a valid-map negative control.

## Results

All five units as predicted (`CONCLUSION.md`): k = 2 (12 faces, m = 3) and k = 3 (15 faces, m = 4) pinned positives SAT, swapped
pairings UNSAT-VERIFIED, unpinned k = 2 SAT. The encoder passes the m >= 3 positive control.

## Next

Week item 3.
