---
id: E-261123-01
title: The full cubic (8, 3) census and plain pass - formula-scope classification of the eight-face case, gate of non-equivelar (9, 4) strata
date: 2026-11-23
status: planned
direction: [DR19]
origin: [E-261117-04, E-261103-01, I-261123-02, I-261123-03]
tests: []
produces: []
preregistered: true
---

> Planned: week item 1 of the owner-approved final lead review 2026-11-23 (`reviews/strategy-review-2026-11-23-final.md`
> §2; `ROADMAP.md` week plan). Rung, J 0. Scores T D F G R: 2 2 2 2 2. Census <= 4 core-h, formulas <= 12 core-h, lab
> jobs <= 50 min wall after a one-line permission, otherwise an owner day run. Before any compute: `PLAN.md` (skill
> `experiment-start`). No proofs; every UNSAT is UNSAT-SOLVER.

## Goal

Is any admissible cubic (8, 3) map other than Roest-Vigh's and Mizhaev's SAT under the plain sub-map formula, and is
it realized? Stage A of E-261117-04 ran 796 maps (the 51 admissible equivelar classes and 745 non-equivelar free-C2
maps); the full census has an estimated 40-65 thousand admissible classes (lead review K1, cross-review check D;
NUMERICAL). Step 0 registers the two truncated-solid controls at 10 elements (I-261123-02).

## Starting point

* Step 0: fixtures from `code/control_rost_vigh.py`:23 and E-261107-01 `results/0/mizhaev_E36.output.candidate.json`,
  cut planes and face-8 links in the week plan; bare `verify_candidate.py`, `tranche.submap_formula(9, links)`,
  `pilot.model_valid`, the hinge bridge.
* Census: `census.run(8, 3, ..., graphs=...)` on slices of `census.extra_graphs(8, 8)` (1806 inputs); the session
  check `reviews/strategy-review-2026-11-23-checks/k1_full_census_8_3.py` shows the split (incomplete at 330 s x 8).
  Unit dispatch, budget and stop file as `E-261117-04/p6.py census-b`.
* Formulas: the stage-A path of E-261117-04 (`p6.py build`, `run.sh`), every admissible class decided or matched to a
  stage-A record by canonical code; K2 (`k2_plain_sample_8_3.py`) measured 0.30 s mean on 240 sampled maps.

## Next

The PLAN (lab session, Opus high / Codex gpt-6-astra high).
