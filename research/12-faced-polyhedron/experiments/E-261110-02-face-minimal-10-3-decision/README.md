---
id: E-261110-02
title: (10, 3) face-minimal decision - the duals of the 20 vertex-minimal genus-3 triangulations, single adjacencies
date: 2026-11-10
status: done
direction: [DR19, DR8]
origin: [I-261110-02, E-261103-02, E-261103-03]
tests: [H-261110-03, H-261110-01]
produces: []
preregistered: true
verdict: OPEN@20.03 core-h, solver-limited (20/20 TIMEOUT at 3600 s, kissat, no proofs; 0 SAT, 0 UNSAT)
concluded: 2026-11-13
---

> Done (2026-11-13): one owner launch, 10 shards, 20.03 core-h, 2.0 h wall; controls pass in every shard; all 20 maps
> TIMEOUT at 3600 s (kissat, no proofs), 0 SAT, 0 UNSAT. OPEN, solver-limited; nothing about existence; escalated
> under the "> 20 % timeouts" rule (`CONCLUSION.md`). Scores T D F G R: 2 2 2 2 2, jump 2.

## Goal

Decide the plain formula of each of the 20 maps (10 faces, 28 vertices, 42 edges, 42 of 45 pairs adjacent, every
adjacency single) with `submap=True` and kissat (no proofs in the night; owner, 2026-11-13). A SAT model that realizes is a new polyhedron of the
target S6; 20 UNSAT-VERIFIED formulas are a conditional face-minimality statement for genus 3 in the cubic
single-adjacency class (I-261110-02). Never reported as S0 or S5.

## Next

Escalated to the owner / lead (`CONCLUSION.md`): a changed formula or solver set-up needs a new PLAN amendment; otherwise
the slot goes to week item 1B or 3. Evidence: `CONCLUSION.md`, `results/run/` (summary: `python3 summary.py`), prep
records in `prep/`, inputs in `maps/` and `queue.json`.
