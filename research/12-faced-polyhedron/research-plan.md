# Research plan: the 12-face Series-1 polyhedron

Principal investigator: main Claude Code session (claude-opus-5-5, effort `xhigh` — the session
was started with `xhigh`, not `max`; this cannot be changed from inside the session).

## Goal

Decide whether there is a polyhedral surface embedded in R^3 with 12 planar simple 11-gonal
faces, every two faces sharing exactly one complete edge, three faces at every vertex
(V = 44, E = 66, genus 6). Ideal outcome: an exactly verified construction. Also valuable:
a proof that no such polyhedron exists, or that specific combinatorial types are impossible.

## Three separate questions

1. Combinatorics: settled in the literature — exactly 59 types (duals of the orientable
   neighborly 12-vertex genus-6 triangulations, Altshuler–Bokowski–Schuchert 1996). Being
   re-verified independently (Track 2).
2. Planar-face realization: automatic in the face-plane formulation (mathematical-model.md §2).
3. Embedding (no self-intersection): the entire difficulty. All conditions are strict sign
   conditions on the oriented matroid of the 12 face planes plus the plane at infinity.

## Team and tracks (cycle 1, started 2026-10-29)

| Track | Lead (model, effort) | Task |
|---|---|---|
| 1 Literature | literature-researcher (Sonnet 5.5, high) | Bokowski–Pisanski 2007, Schewe 2010, ABS 1996 data, post-2007 work, Mizhaev 2026 |
| 2 Combinatorics | combinatorial-topology (Opus 5.5, xhigh) | independent enumeration of the 59 types, automorphisms, checker |
| 3 OM-SAT | algebraic-geometry (Opus 5.5, xhigh) | chirotope SAT per type: UNSAT = impossibility proof for that type |
| 4 Geometry-first SAT | computational-search (Sonnet 5.5, high) | fixed planes, SAT over all triangulations; MaxSAT-guided arrangement search |
| 5 Scouting | interdisciplinary-scout (Haiku 5.5, medium) | realizability tools, SAT/geometry techniques |
| 6 Theory | mathematical-researcher (Opus 5.5, max) | sound extra clauses, symmetry analysis, Szilassi mechanism, ansatzes |
| Verification | adversarial-verifier (Opus 5.5, max) | to be launched on the first encodings/candidates |

Agent definitions are in `.claude/agents/`. Custom agent types are not loaded into a session
that was already running, so in cycle 1 each agent runs as a general-purpose subagent with the
model and effort of its definition passed explicitly and its definition file as instructions.
Model assignment was verified from the subagent transcripts (all as intended).

## Decision logic

* If OM-SAT proves UNSAT for all 59 types (with checked proofs and an adversarially verified
  encoding): nonexistence theorem. Requires independent verification of every clause family.
* If OM-SAT gives SAT for a type: try to realize the oriented matroid; any realization is a
  polyhedron (predicates depend only on the chirotope). Non-realizability certificates feed back
  as cuts.
* Geometry-first search runs in parallel as the constructive approach; its MaxSAT score gives a
  graded objective for arrangement-level local search.
