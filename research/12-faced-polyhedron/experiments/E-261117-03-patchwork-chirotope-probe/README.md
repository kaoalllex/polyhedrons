---
id: E-261117-03
title: Patchwork chirotopes probe - certificate test C0, coverage of the controls C1, Szilassi's map formula with P4 C2
date: 2026-11-17
status: done
concluded: 2026-11-17
verdict: OPEN at seven faces (Szilassi patchwork at K = 32, C2 S5 by construction); UNDERPOWERED@0.87 core-h at n >= 9
direction: [DR19]
origin: [I-261029-10, E-261113-02, E-261114-02]
tests: []
produces: []
preregistered: true
---

> Planned, explore, jump 0. Scores T D F G R: 1 2 1 2 2 | budget: one session, <= 1 core-h; the sampler <= 6 core-h
> only after C1 passes (gated). Before any compute: `PLAN.md` (skill `experiment-start`). No proofs.

## Goal

Week item 4 (`ROADMAP.md`; `reviews/dialogue-2026-11-16-strategy.md` §2 row 4, Appendix A2). Are the known face-neighbourly chirotopes patchwork
(coherent weight matrix H_ij = s_ij t^w_ij, w in [0, K], unique minimum-weight matching in every 4 x 4 minor) at
small K, so that a chirotope realizable by construction can be searched for?

## Next

Step 0, batched: `candidate-check` of the 16 realized S6 (10, 2) files of E-261113-02 (13 maps; the independent
checker `witnesses/verify_s6_10_2.py` exists), then one witness per distinct accepted map, the rest archived as
variants; these objects are C1 controls. C0: the potentials certificate (factor 4) against all 24 costs on tied and
uniquely optimal matrices. C1: Szilassi (perturbed), Roest-Vigh, Mizhaev, the 17 K13 solids, the 16 (10, 2)
objects; coverage per K. C2: Szilassi's map formula AND P4. Kill: no control in the box K parks that box; C2
UNSAT-SOLVER in the box. A finite K never refutes membership; "realized, not verifier-conditioned" is not a result.

## Results

Step 0: the 16 S6 (10, 2) files passed `candidate-check` (13 maps, `witnesses/s6_10_2_controls/`). C0 passed. Amended
run (K = 32, n <= 9): Szilassi's chirotope is patchwork; C2 realized Szilassi's map by construction (S5 PASS);
Roest-Vigh, Mizhaev and K13 UNKNOWN at 90 s. Details: `CONCLUSION.md`.
