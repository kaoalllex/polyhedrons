---
id: E-261101-16
title: Arrangement first - exact chamber-SAT on structured and archived 12-plane arrangements
date: 2026-11-01
status: planned
direction: [DR7, DR18]
origin: [I-261101-08, I-261030-07, E-261030-02, E-261030-10]
tests: [H-261101-08, H-261101-10]
produces: []
preregistered: false
---

> Planned. Scores T D F G R: 2 2 2 1 2 | budget: one laptop night (about 20 core-h), target S3 (any genus) and S0.
> Before any compute: `PLAN.md` from `experiments/_template/` (skill `experiment-start`).

## Goal

The largest number of adjacent pairs any all-adjacent cubic solid reaches on (a) G-symmetric arrangements with a
free action, (b) the 247 archived arrangements, (c) the 1005 near-miss arrangements. A solid with 66 pairs is an S0
candidate (run `candidate-check`); 54 or 60 pairs is the first genus-4/5 S3 witness.

## Next

Stop rule: the night ends, or the first solid with >= 54 pairs (then `candidate-check`, then a second night on
perturbations of that arrangement). Report the histogram of maximal adjacency per catalogue part with the solver
status (OPTIMAL / FEASIBLE / UNKNOWN) for every arrangement.

## Starting point

* Inner solver exists: `code/solid_cpsat.best_solid(A, time_limit, target_adj=...)` with `code/solid_first.Arrangement`.
  Use it twice per arrangement: the decision `target_adj=66` (60 s) and the maximisation (60 s). Record the CP-SAT
  status; UNKNOWN is a timeout, not a verdict.
* Catalogue generator (new script in this folder): for G in {A4, D3, D2, S4, C3, C2} take an explicit orthogonal
  representation (`code/omsat_sym.find_reps` gives signed-permutation ones), sample the free planes per orbit, build
  the 12 planes as the orbit union, perturb by 1e-6 to break exact coincidences, apply the filters of I-261101-08.
  Grid the A4 family (3 parameters) densely; sample the others.
* The decision version must not rely on the lazy "one disk face per plane" loop of `best_solid` (no-goods with
  `max_cuts`): encode the disk condition exactly in CP-SAT, V - E + F = 1 for the selected 2-cells of every plane,
  with parity variables for the 1-cells and 0-cells inside the plane; then INFEASIBLE is a verdict.
* Third source of arrangements: normals realized from rank-3 models of E-261101-06 and partial objects from
  E-261101-23, each with offsets chosen by the LP of FD8 (these satisfy every normal-level condition by construction).
* Positive control: the Roest-Vigh planes (`code/control_rost_vigh.py`) must give 28 pairs with 8 doubled ones in the
  S1 variant, and the archived type-0 genus-3 arrangement must reach 48. Negative control: 30 random arrangements
  must stay below 48 (as in E-261030-02).
* Power statement: the decision at 60 s per arrangement is exact only when CP-SAT reports OPTIMAL or INFEASIBLE;
  count how often it does on the controls before trusting the histogram.
* Outcomes: >= 54 pairs anywhere supports H-261101-08 and refutes H-261101-10 for that arrangement; 48 everywhere
  (with mostly OPTIMAL statuses) weakens H-261101-08 and leaves DR7 at OPEN-LOW with a power statement.
