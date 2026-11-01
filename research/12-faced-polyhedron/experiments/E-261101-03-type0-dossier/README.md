---
id: E-261101-03
title: Type-0 genus-3 dossier: is the best result correct and new?
date: 2026-11-01
status: planned
direction: [DR1]
origin: [I-261031-04, E-261030-03, E-261101-02]
tests: [H-261101-05]
produces: []
preregistered: false
---

> Planned. Scores T D F G R: 1 2 2 1 2 | budget: 1-2 sessions, no compute. Before any compute: `PLAN.md` from `experiments/_template/` (skill
> `experiment-start`).

## Goal

A second independent verifier, canonical map form, certificate re-run, novelty search, a 2-page dossier.

## Next

Stop rule: stop after the 5 steps in ROADMAP or 2 sessions; any verifier mismatch -> fix FD10 first

## Starting point (moved from ROADMAP.md)

Hypothesis: the five `type0_genus3_extendable*.json` files are exact embeddings of one map that is completable by
the three certified handles to target type 0. Steps: (1) a second, independently written verifier that does not
import `ladder_exact` and uses a different representation (vertex coordinates and face polygons, not planes +
links): face incidence and vertex stars (3 faces per vertex, edges in exactly 2 faces), orientation, chi = -4,
planarity, simple face boundaries, every pair of faces meets exactly in its shared edges; plus regression tests on
Szilassi, Roest-Vigh (positive) and the genus-4 attempts and mutated copies (negative);
(2) canonical form of the map (relabelling + mirror), proof that all five variants share it; (3) re-run the
certificate; (4) novelty search: genus-3 maps with 12 faces (Wedd's list, Conder's census), known R^3
realizations; (5) a 2-page dossier: theorem, certificates, limits, questions for a mathematician.
Outcomes: all pass -> shareable result #2 in `STATUS.md`; any mismatch -> a bug in FD10, top priority.
