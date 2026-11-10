---
id: I-261110-07
title: Edge-convexity bits as the cube basis - 66 edge signs determine the 44 vertex types
date: 2026-11-10
status: open
direction: [DR8, DR9]
origin: [I-261031-02, E-261101-15, I-261101-20]
---

## Idea

At a cubic vertex the three edges are convex or reflex. Derivation sketch (2026-11-10 session):

1. a vertex is a saddle iff its three edges do not have the same convexity;
2. at a saddle the reflex face corner is the one opposite the odd edge.

Evidence: statement 1 holds on all 62 vertices of Szilassi, Roest-Vigh and Mizhaev (NUMERICAL, float computation of
the session, `reviews/HANDOFF_PROMPT_2026-11-10-wedges.md` §2: every saddle has edge signs CCR or CRR, none RRR);
statement 2 was **not** checked on data. Neither is proved here.

If both hold, the 66 edge bits of an S0 object determine all 44 vertex types, and they are a smaller and more uniform
split basis than the 44 vertex-type patterns planned for E-261101-15.

## Why it might help

Cube-and-conquer needs split variables that the geometry constrains strongly; edge bits tie two vertices each, so a
cube on few edges already fixes many vertex types, and every refuted cube reads as a statement about a convexity
pattern.

## Cheapest test

`code/edge_types.py` (E-261110-01) checks statements 1 and 2 exactly on Szilassi, the two 8-face objects and the
247-realization archive. Then E-261101-15 takes the edge bits as its cube basis (dated section in that README); no
separate experiment.

## Source

Handoff of the 2026-11-10 strategy session (`reviews/HANDOFF_PROMPT_2026-11-10-wedges.md` §4 I-G).
