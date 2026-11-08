# E-261108-02: conclusion (2026-11-08)

**Verdict: PARK (kill criterion met).** 0 of the 24 admissible 11-gon (9,3) maps have an UNSAT face-support sub-formula on
<= 6 faces (needed: >= 3). Scope (NUMERICAL/EXACT per sub-formula): clause subsets of the plain formula indexed by constraint
face tuples (PLAN amendment), levels k = 3..6 exhaustive (C(9,k) sets per map), cap 20 s, 0 TIMEOUT at k <= 6; at k = 7 also
0 UNSAT, 0 TIMEOUT; at k = 8 0 UNSAT with 94 TIMEOUTs over the 33 maps (descriptive, undecided). Sub-formulas that are UNSAT
would have been DRAT-verified; none occurred. Not tested: cores that use clauses indexed by 7+ faces, other maps, other groupings.

* Controls: C0 none (pass); C1 planted core k_min 3 with 20/15/6 UNSAT sets at 6/7/8 = exactly the supersets (pass); C2
  (item 1's negative control) k_min 6, assumption-core union 8 faces, consistent (pass). The measure takes the values 3, 6 and
  none, so the null on the maps is not a constant artefact of the measurer. Monotonicity held on all 33 units.
* Strict transitive-support measure (the pre-amendment plan) was blind (every constraint has 9-face support); pilot only.
* Comparators (2,2,2) x3, (1^6) x3: also none at k <= 7. No contrast between concentrated and spread maps, so no phenomenon.
* Hash check: rebuilt formula hash equals the recorded `formula_sha256` for 27 of 30 maps; maps 40, 48, 5, 6 have no local
  record (hash computed and stored in result.json, no external match).
* Cost: 0.072 core-h wall (10 shards, 258 s), 0.72 core-h of summed solver time. Per-solve logs deleted after
  aggregation; `result.json` per unit keeps status, CNF and proof SHA-256 of every sub-formula.
* Follow-up (PROVED-1 lemma draft, (10,4) count) is not triggered. The fast UNSAT of concentrated maps is not explained by a
  core on <= 6 faces in this formulation; the unresolved 8-face TIMEOUTs leave "core on 7-8 faces" open.
