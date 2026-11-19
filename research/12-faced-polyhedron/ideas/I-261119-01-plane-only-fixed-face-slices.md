---
id: I-261119-01
title: Plane-only fixed-face slices wherever a map census has involutions fixing faces
date: 2026-11-19
status: open
direction: [DR19, DR18]
origin: [E-261118-03, I-261117-02]
---

## Idea

E-261118-03 decided all 20 plane-only C2 formulas of the (11, 5) Aut+ = 2 maps (12 elements) in 17-90 s, where the
plain normalised formulas of E-261116-01 were censored at 3600 s. Run the same runner mode (`tranche.py` records
with `sym_generator` and `sym_planes_only`) on every census map whose orientation-preserving involution fixes a face:
S6 (11, 4) and (12, 5) and the nine-face S1 maps by genus, where such maps exist. Not S0: a half-turn of an S0
object fixes no face, and FD5 already covers its rotations.

## Why it might help / cheapest test

A cheap symmetric slice of cases priced out for plain formulas; a SAT model goes to the bridge and its target check.
Cheapest test: count the maps with a fixed-face involution per case from an existing census (minutes), then one
probe as E-261118-03 (`make_queue.py`, `controls_12.py` pattern). Untested proposal; the speed is NUMERICAL for
20 (11, 5) formulas only. A slice that is UNSAT-SOLVER says nothing about asymmetric objects.

Source: `experiments/E-261118-03-s5-11-5-plane-only-price-probe/CONCLUSION.md`.

## 2026-11-19 lead review 2026-11-19

Nine-face part taken up by E-261119-02 (week item 2, the main investment): a symmetric nine-face census (C3 3+3+3 and
C2 4 x 2 + 1, lifting the C3 exact cover of E-261103-01) with per-map symmetric formulas (C3 clauses in the standard
chart, plane-only C2 in a moved chart). The S6 (11, 4) and (12, 5) parts serve the parked S6 target.
