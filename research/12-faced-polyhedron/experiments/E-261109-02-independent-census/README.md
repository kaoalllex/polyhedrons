---
id: E-261109-02
title: Independent census of the (8, 2) and (9, 3) candidate maps (week item 3, I-261108-08)
date: 2026-11-09
status: done
direction: [DR19]
origin: [I-261108-08, E-261103-01]
tests: [H-261101-07]
produces: []
preregistered: false
verdict: PROMISING
concluded: 2026-11-09
---

> Audit, EXACT computation, instance scope (7,1), (8,2), (9,3). Not pre-registered: the experiment was written and
> run in one lab session as a bounded audit (seconds of CPU); the pass criterion below was fixed by the row, not tuned.

## Question

Does an enumerator that shares no code with E-261103-01 reproduce 1 / 2 / 240 classes (203 admissible at (9,3)) with the
same classes, automorphism orders and reflexibility?

## Method

`enum_growth.py` (Python reference, label-free canonical form) and `grow.c` (the same search in C, leaf emitter).
Growth of an oriented triangulated surface triangle by triangle: the lowest open side u->v is glued to an existing open
side v->u or to a side of a new triangle (v, u, w), w an existing or the next unused vertex label. Pruning: excess of edges
over one per pair of K_F <= E - C(F,2) (lower bound from closed edges and directed open sides), corners per vertex
<= F - 1 + extra, missing pairs <= 2 (remaining triangles), a closed vertex link must be one cycle of all its corners with
F - 1 distinct neighbours, no new triangle at a closed vertex. Final checks: F vertices, all pairs, every link a single cycle.
Dedup: BFS code over all root sides and both orientations (own implementation, not `review.TriMap.canon`).
`compare.py F g EXE` converts the E-261103-01 dart codes to the same structure and compares the sets of canonical
codes plus |Aut+|, reflexibility, admissibility. Completeness argument (PROVED-1, AI-written): every labelled map is
reached by the "lowest open side" rule from any root triangle; the prunes are necessary conditions.

## Results

| (F, g) | leaves | classes (mine / E-261103-01) | only in one | attribute mismatches | admissible |
|---|---:|---:|---:|---:|---:|
| (7, 1) | 2 | 1 / 1 | 0 | 0 | 1 |
| (8, 2) | 80 | 2 / 2 | 0 | 0 | 2 |
| (9, 3) | 34346 | 240 / 240 | 0 | 0 | 203 |

(9,3): 120 s total (C search plus Python canonicalisation). The Python reference without the closed-link prune gave
identical node counts to the C search at (8,2) (13,217,758 before the prune, 354,944 after in C); the unpruned Python
(8,2) also gave 2 classes.

## Limits

* Agreement of two algorithms is evidence, not a proof: the coverage argument is AI-written (at most PROVED-1), no human
  review. The census is now two-algorithm EXACT for the class lists; the geometric / encoder caveats of STATUS are unchanged.
* The pruned C search was compared only through the class sets; the prune soundness is supported by the (8,2) and (9,3)
  agreement (a wrong prune would lose classes; it lost none), not proved separately.
* (10, 4) (1183 / 1117) and (12, 6) not run.
