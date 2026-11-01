---
id: E-261101-18
title: Face-grouped minimal unsatisfiable cores of the 50 certified symmetric instances
date: 2026-11-01
status: planned
direction: [DR10, DR11]
origin: [I-261101-10, E-261029-13, E-261029-15]
tests: [H-261101-11, H-261101-02]
produces: []
preregistered: false
---

> Planned. Scores T D F G R: 2 2 2 2 2 | budget: about 30 core-h (one laptop night) after a one-session pilot.
> Before any compute: `PLAN.md` (skill `experiment-start`).

## Goal

For each of the 25 embedding and 25 immersion instances, a minimal set of faces whose local clauses (with GP, SYM
and the normalisations as background) are unsatisfiable; the recurring patterns; and, if a pattern on k <= 6 faces
recurs, the asymmetric sub-instance test on every type containing that sub-map.

## Next

Stop rule: all 50 cores extracted, or 10 cores with no pattern smaller than 10 faces (then H-261101-11 is weakened
and the second half is skipped).

## Starting point

* Regenerate a CNF with `overnight/run_overnight.py sym [--sym-immersion] --only <task> --keep-cnf --results-dir
  <scratch>`; its SHA-256 must match `results/*/results.jsonl` (that is the certificate link).
* Shrink first: `drat-trim <cnf> <proof> -c core.cnf` gives the clauses used by the proof.
* Group: a clause belongs to face X's group if it is a TRIPLE / SIMPLE / REFLEX1 / POC clause whose predicate is
  about face X (the encoder tags clauses; extend `omsat.CNF` tags with the face if needed). GP, SYM and SB clauses
  are hard.
* Deletion-based group MUS: one selector literal per face group; CaDiCaL via pysat with assumptions; drop a group,
  re-solve, keep it out if still UNSAT. Record the minimal face set, its size, the induced sub-map (which pairs of
  the set are adjacent is always all of them; record the vertices of T inside the set).
* Pilot (minutes): Lutz #54 under T and #3 under D3.
* Positive control: with all 12 groups the instance is UNSAT (certified); negative control: with no local group the
  instance is SAT (the `control_no_triples_SAT` field).
* Outcomes: a recurring core on <= 6 faces supports H-261101-11; then build the asymmetric sub-instance (same faces'
  local clauses, GP, no SYM) for the 59 types and report SAT/UNSAT per type (an UNSAT excludes the type: run
  `drat-trim`, record hashes, label EXACT). Cores of >= 10 faces weaken H-261101-11 and H-261101-02.
