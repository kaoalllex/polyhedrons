---
id: E-261114-03
title: Chart normalisation at a hull vertex - lemma, re-charting controls and per-vertex cubes on the slowest normalised maps
date: 2026-11-14
status: done
concluded: 2026-11-14
verdict: UNRESOLVED (small-pilot gate closed; solver-limited)
direction: [DR19, DR8]
origin: [I-261110-06, I-261114-01]
tests: [H-261101-06]
produces: []
preregistered: true
---

> Explore, activated by E-261114-01's pilot gate. Scores T D F G R: 2 2 2 2 2.
> Pre-registration: PLAN.md; soundness argument: SOUNDNESS.md. Controls precede target cubes.

## Goal

Week item 4 (`ROADMAP.md`). Restrict chart freedom near a hull vertex. SOUNDNESS.md makes the
sketch precise: use inward planes and a small old-INF perturbation so the vertex remains finite.

## Outcome and next step

The re-charting controls pass; every small-pilot cube times out. The full pilot was not run.
See CONCLUSION.md and STATUS.md section 3an for verification, timing and scope. The speedup
comparison remains unresolved; no geometric negative claim. Next: week item 2. Reopening the
full chart pilot requires an owner/lead decision under PLAN.md.
