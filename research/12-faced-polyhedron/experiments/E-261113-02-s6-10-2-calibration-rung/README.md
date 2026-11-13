---
id: E-261113-02
title: (10, 2) calibration rung - time to SAT over seeds and bridge realization rate on 50 of Lutz's 865 maps
date: 2026-11-13
status: done
direction: [DR19, DR8]
origin: [I-261113-02, E-261110-02]
tests: [H-261110-03]
produces: []
preregistered: true
verdict: DONE (calibration)@0.239 core-h (153/153 SAT, median 0.83 s, no timeout; bridge 16/153 realized; no proofs)
concluded: 2026-11-13
---

> Done (2026-11-13): SAT at (10, 2) is fast and light-tailed (median 0.83 s, max 5.2 s over 150 drawn units); the
> frozen bridge realizes ~10 % of models. Readings LIGHT, BRIDGE < 50 %, CHEAP (`CONCLUSION.md`, STATUS 3ah).
## Goal

Week item 2 (`ROADMAP.md`). Fetch Lutz's list of the 865 vertex-minimal 10-vertex genus-2 triangulations from the
archived Manifold Page into `literature/lutz-manifold-page/` (untrusted data, hash recorded, parsed by
`code/lutz_import.py` under `python3 -I`). 50 maps by a frozen seed; per map the `submap=True` formula of
E-261110-02 under kissat with 3 seeds, cap 300 s; the bridge with the frozen settings of E-261110-02 on up to 6
models per SAT map. Report the time-to-SAT distribution and the fraction of models that realize.

## Next

Controls: the importer checks (closed, orientable, simplicial, counts, pairwise non-isomorphic); the witness map of
`witnesses/` SAT and realized. Stop rule: 50 maps recorded, an importer control failure or the cap. Reading (decided
now): median SAT < 60 s and none after 300 s -> the (10, 3) timeouts read as "probably UNSAT" for planning, never
as a claim; a heavy tail -> a seed-portfolio day run on (10, 3) is proposed to the owner; bridge rate < 50 % ->
E-261113-01 takes more models per SAT. 50 maps under 0.3 core-h -> the full 865 within the same budget. Every
realized object passes `--target S6` and is a control, not a headline.
