---
id: E-261116-09
title: Uniformity and perturbation lemmas - which scope words of the small-case results can be removed
date: 2026-11-16
status: done
concluded: 2026-11-22
verdict: FOUNDATION (L1-L5 PROVED-1; L6 at k = 4); part B no common family set, Lemma P parity on 3 + 17 records
direction: [DR19, DR11]
origin: [I-261116-07, I-261108-09]
tests: [H-261101-07]
produces: []
preregistered: true
---

> Done 2026-11-22 (`CONCLUSION.md`, `LEMMAS.md`), audit, jump 0. Scores T D F G R: 2 1 2 2 2 | budget: one session, exact local checks only.

## Goal

Week item 5 (`ROADMAP.md`). (a) Uniform position is no loss for cubic embedded objects (I-261116-07). (b) The
perturbation lemma I-261108-09 by its universal local check. Output: PROVED-1 text or a counterexample.
Extended 2026-11-17 (`reviews/dialogue-2026-11-16-strategy.md` §2): (c) the equivariant perturbation step of N2 (E-261117-02); (d) the P3 proof
obligations of E-261116-07 (finite-vertex coverage at OM level, the disk and manifold argument). Queue, not this week.

## Next

Update paper items B2-B5 and D3 in `paper/OUTLINE.md`. A counterexample keeps "uniform" / "cubic" in every statement.

Extended 2026-11-18 (`reviews/strategy-review-2026-11-18.md` §5): (e) the symmetric-slice lemma I-261118-02 (fixed faces, rotation orbits, C3 coverage, the C3 gauge).

Extended 2026-11-19 (`reviews/strategy-review-2026-11-19.md` §2, week item 4): (f) a uniform symmetry group of an
eight-face solid contains a free half-turn (the scope of E-261119-01's symmetric (8, 3) slice); (g) on an (11, 5) map
with Aut+ = 2 the only possible improper symmetries are mirrors, and every mirror class forces zero signs (the (11, 5)
closure). These lemmas carry the scope sentences of E-261119-01 and E-261119-02.

Extended 2026-11-22 (owner): part B of `PLAN.md`, the family-ablation diagnostic of the E-261119-02 stage-B formulas
(a stated deviation from "no compute").

## Results (2026-11-22)

Part A: `LEMMAS.md` (L0-L6, PROVED-1), exact checks `checks.py` -> `results/checks.json` (PASS). Part B (owner): family
ablation `ablate.py` -> `results/ablation/` (amendment 1: kissat child process, probes on every record, size <= 3 per
stratum) and the GF(2) parity check `parity.py` -> `results/parity.json`. Numbers and claims: `CONCLUSION.md`; ledger:
`STATUS.md` 3bi. Not run: L6 at k = 5, 6; parity on the unpriced maps.
