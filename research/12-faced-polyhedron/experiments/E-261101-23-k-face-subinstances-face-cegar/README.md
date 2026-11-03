---
id: E-261101-23
title: k-face sub-instances of the asymmetric OM-SAT encoding, and face-CEGAR seeds from their models
date: 2026-11-01
status: done
concluded: 2026-11-02
direction: [DR8, DR11]
origin: [I-261101-18, E-261029-12, E-261101-18]
tests: [H-261101-15, H-261101-02, H-261101-12]
produces: []
verdict: UNDERPOWERED@59.75 core-h (night 6; LP hang, 27 of 59 types reached; see CONCLUSION.md)
preregistered: true
---

> Done 2026-11-02 (night 6). Results: on the greedy face set, k = 8 and k = 9 sub-instances were SAT wherever
> decided, every k = 10 run timed out, no UNSAT, no SAT model realized; five of six shards hung in the
> final-polynomial LP, so 32 types were never reached. Numbers, claims and labels: `CONCLUSION.md`; follow-up
> E-261102-01.

## Goal

For three types first (one trivial-Aut, type 0, type 58), then all 59: the verdict (SAT / UNSAT / timeout at
10 min) of every k-face sub-instance for k = 7, 8, 9 over face sets up to automorphism, ordered by the number of
triangles of T they span; DRAT proofs for every UNSAT; and, from the SAT models of the largest k, numerically
realized partial objects (face-CEGAR seeds), each re-checked exactly on its k faces.

## Next

Stop rule: the three pilot types done at k <= 9, then the night; or the first UNSAT at k <= 9 (then `drat-trim`,
record hashes, run the same face set on every type containing the sub-map). Outcomes: UNSAT at small k supports
H-261101-15 and excludes types with small formulas (EXACT); all SAT weakens it, and the realized models are the first
seeds in the right combinatorial class for E-261101-16 (arrangement first) and E-261101-19.

## Starting point

* Build: `omsat.build` with the local families restricted to a face set (add a `faces` option: TRIPLE clauses only
  for non-triangle triples inside the set, SIMPLE / REFLEX1 / POC only for faces in the set; GP, SB unchanged). The
  monotonicity that makes this meaningful: a full solution satisfies every sub-instance (I-261101-18).
* Face sets: for k = 7 the sets up to Aut(T) that span 9 triangles (the maximum, `results.md` "No Szilassi embryo"),
  then those spanning 8; for k = 8, 9 the sets that contain a maximal 7-set. Expect dozens to a few hundred per type.
* Solver: CaDiCaL (binary) with `--proof` for every run; 10-minute limit; record vars, clauses, status, time, SHA-256
  of CNF and proof.
* Realization of a SAT model (face-CEGAR): fit 12 planes to the model's 715 signs by hinge loss on normalised
  determinants (random restarts; the rank-3 contraction first, then rank 4), then `ladder_exact`-style exact check of
  the k faces (simple, pairwise correct); add the next face's clauses with the model as phase hints; repeat up to 12.
* Positive control: the Szilassi map (n = 7) sub-instances on 6 faces are SAT and their models realize. Negative
  control: a sub-instance whose set contains a face with all its 11 neighbours plus the symmetric D3 class (#3, where
  simplicity alone is UNSAT) must be UNSAT under that symmetry.
* Counter calibration: report the fraction of timeouts; a sweep that is mostly timeouts is uninformative, not negative.
