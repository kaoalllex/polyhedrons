---
id: E-261119-03
title: Face-transitive nine-face maps at genus 7 - Cayley maps of Z9 and Z3 x Z3 at valence 14, plain formula on admissible classes
date: 2026-11-19
status: done
concluded: 2026-11-22
verdict: NO-ADMISSIBLE-CAYLEY-9-7
direction: [DR18]
origin: [I-261119-03, E-261117-01]
tests: []
produces: []
preregistered: true
---

> Concluded: no face-transitive cubic (9, 7) map is admissible (Z9 48768, Z3 x Z3 522240 valid rotations, every
> one with a repeated vertex triple); with E-261117-01 the slice is empty at genus 4 and 7. EXACT, coverage PROVED-1;
> no formula ran; ~2.0 core-h (1.7 in an aborted launch). Run on an owner exception to T + D >= 3 (scores 1 1 2 1 2).
> Evidence: [CONCLUSION.md](CONCLUSION.md).

## Goal

N1's two independent enumerators (E-261117-01) extended to valence 14 for Z9 and Z3 x Z3 (genus 7, E = 63), with its
K7, K12 and Roest-Vigh controls; the plain formula at 10 elements on every admissible class.

## Next

No admissible class -> the face-transitive nine-face slice closed at genus 4 and 7 (EXACT computation, coverage
PROVED-1). SAT -> bridge, `--all-pairs` nine faces, `candidate-check`, escalate. Lab: Opus, medium / Codex
gpt-6.1-sol, medium; SAT: Opus, high / gpt-6-astra, high.
