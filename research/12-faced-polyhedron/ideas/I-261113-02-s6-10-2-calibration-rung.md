---
id: I-261113-02
title: The (10, 2) maps as a calibration rung for S6 - time to SAT over seeds and the bridge realization rate
date: 2026-11-13
status: open
direction: [DR19, DR8]
origin: [I-261110-02, E-261110-02]
---

## Idea

Measure, on the rung where SAT is known to occur (the S6 (10,2) witness map is SAT in 0.7 s, E-261110-02 prep),
how fast kissat finds a model across maps and seeds and how often the SAT-to-coordinates bridge realizes it. Input:
Lutz's list of the 865 vertex-minimal 10-vertex genus-2 triangulations (untrusted data, `code/lutz_import.py`).

## Why / cheapest test

All 20 (10, 3) formulas timed out at 3600 s; without a time-to-SAT distribution at the same element count a
timeout cannot even be ranked. The prep of E-261110-02 saw 3 of 6 foreign (10,2) models not realized (NUMERICAL):
the bridge rate prices every SAT at (10, 3). Cheapest test: E-261113-02, 50 maps, 3 seeds, cap 300 s. A fast,
light-tailed distribution makes "probably UNSAT" the planning reading of the (10, 3) timeouts (never a claim); a
heavy tail argues for seed portfolios instead of longer caps. Untested proposal.

Source: `reviews/strategy-review-2026-11-13.md` §6 (N4); approved by the owner on 2026-11-13.
