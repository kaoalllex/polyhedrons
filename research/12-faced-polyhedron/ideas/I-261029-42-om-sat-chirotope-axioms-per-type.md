---
id: I-261029-42
title: OM-SAT: Schewe-style chirotope SAT decision per type
date: 2026-10-29
status: tried
direction: [DR8]
origin: [L:schewe2010]
---

## Idea
One Boolean per ordered 4-subset of 13 elements, 3-term Grassmann-Plucker clauses (16 clauses per relation); UNSAT per type is an impossibility proof, SAT a candidate OM.

## Why it might help
Exact decision per type; reuse the published encoding.

## Cheapest test
Generate the 715-variable GP clause set, check count, run on Szilassi's 7 planes (n = 8 incl. infinity).

## Source
literature/scout-leads.md lead 2; archive/research-plan.md Track 3 / decision logic; STATUS DR8 (never run to completion; symmetric cases certified, FD5)
