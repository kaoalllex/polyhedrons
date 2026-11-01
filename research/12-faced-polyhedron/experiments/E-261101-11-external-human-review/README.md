---
id: E-261101-11
title: External human review of FD5/FD6 and the type-0 dossier
date: 2026-11-01
status: planned
origin: [I-261101-06, E-261029-13, E-261029-15, E-261101-03]
tests: []
produces: []
preregistered: false
---

> Planned. Scores T D F G R: 2 2 1 1 2 | budget: owner's e-mail, no compute. Before any compute: `PLAN.md` from `experiments/_template/` (skill
> `experiment-start`).

## Goal

Turn PROVED-1 / EXACT claims into reviewed ones.

## Next

Stop rule: a reply, or 4 weeks without one -> next reviewer

## Why and whom (2026-11-01)

1. **The author of `pirozhkov-andrei/polyhedraproof`** (identity and affiliation not known to us; the repository and
   its Zenodo record reduce exactly our problem to 59 SAT formulas, report two refuted formulas in 648.5 core-h and
   ask for collaborators). Why first: two independently written encoders that agree predicate by predicate on random
   exact configurations are the cheapest strong evidence for the soundness of our FD2/FD4 (PROVED-1 by AI sessions
   today); his two refuted formulas, if the LRAT certificates or cube lists are shared, exclude two types for us at
   no cost; a shared campaign halves the estimated 19,000 core-h; and otherwise the impossibility side may be
   settled without us. Content of the first e-mail: three shared symmetric instances with CNF hashes, the
   predicate-equality harness (`code/omsat_validate.py`), one question. Everything received stays CLAIMED until
   re-checked here.
2. **Gergely Roest and Viktor Vigh** (Bolyai Institute, University of Szeged): found the second 8-face
   face-neighbourly polyhedron with an AI-assisted search, verified exactly, and state that the 12-face case is open
   (`literature/primary-reads-2026-11-01.md`). Human mathematicians working on this family right now, at Szilassi's
   institute: the natural readers of Lemma A, Lemma B and the type-0 dossier.
3. **Juergen Bokowski** (TU Darmstadt) and **Kevin H.** (CodeParade): the authors of the only published attempt at the
   face version (numerical) and of the vertex-version impossibility machinery.
