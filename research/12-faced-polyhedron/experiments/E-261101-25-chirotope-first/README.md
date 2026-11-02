---
id: E-261101-25
title: Chirotope-first realization - core-guided SAT with geometric assumptions, numerical realization, exact check
date: 2026-11-01
status: done
direction: [DR8, DR9, DR17]
origin: [I-261101-21, I-261101-18, E-261029-12, E-261030-11]
tests: [H-261101-17, H-261101-12, H-261101-01]
produces: []
verdict: UNDERPOWERED@44.1 core-h (night 6; LP hang and --rounds 12; see CONCLUSION.md)
preregistered: true
---

> Done 2026-11-02 (night run 1 = night 6). Results: most seeds used up the 12 core-guided rounds at k = 7, the
> seeds that reached models never realized them, and all four shards hung in the final-polynomial LP. Numbers,
> claims and labels: `CONCLUSION.md`; follow-up E-261102-02.

> Scores T D F G R: 2 2 2 2 2 | budget: pilot in the session (minutes), then one laptop night. `PLAN.md` is the
> pre-registration; `chirotope_first.py` is the engine (algorithm v2 of the construction side).

## Goal

Whether the SAT solver, given the normal combinatorics of a geometric seed as assumptions, reaches models of the full
embedding instance after a bounded number of core-guided releases, and whether those models realize. Controls:
n = 7 from random planes must end EMBEDDED; the realizer must recover known 12-plane chirotopes.

## Next

Stop rule: the night ends; or the first realized 12-face model (`candidate-check`); or 20 seeds in a row that time
out at every round (then the assumptions carry no information and H-261101-17 is weakened).
