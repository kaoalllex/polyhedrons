---
id: I-261117-03
title: Ninth plane as one formula - the census-free formula with eight planes pinned, a linear program per sign vector of the ninth plane
date: 2026-11-17
status: open
direction: [DR19, DR18]
origin: [I-261103-02, I-261112-01, E-261112-02]
---

## Idea

Run the census-free formula (I-261103-02, A1) with the eight-plane sub-chirotope pinned to Roest-Vigh or Mizhaev:
84 unknown signs plus the cells. For a sign vector, s_ijk det(p_i, p_j, p_k, x) > 0 is linear in the ninth plane x
over the fixed old coordinates, so a linear program tests and, if feasible, realizes the extension; infeasible
extensions are blocked and the solver continues. One cap for solve and LP.

## Why it might help

A changed method for the parked ninth-plane Stage B (E-261112-02, about 79 core-h): one formula instead of a cell
list, with coordinates for free whenever the LP is feasible. It does not give coordinates automatically for an
unpinned model (critic, #24). Price unmeasured. Untested proposal.

## Cheapest test

A conditional extra rung of E-261116-07: only after its L0-L2 pass; the deleted-plane reinsertion of the known
objects must be recovered.

Source: `reviews/dialogue-2026-11-16-strategy.md` §2 (conditional), Appendix A5 (N3). Nearest: I-261112-01.
