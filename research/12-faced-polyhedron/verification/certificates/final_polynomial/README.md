# Biquadratic final-polynomial certificates (three k-face SAT models)

Three SAT models of k-face sub-instances of the asymmetric OM-SAT encoding (greedy face set, `faces` in
`certificates.json`) have a biquadratic final polynomial: their rank-4 chirotopes on 13 elements (12 face planes and
the plane at infinity, homogeneous coordinates) are not realizable. Checked 2026-11-03 by `verify.py`, standard library
only, which shares no code with the producer (`experiments/E-261101-25-chirotope-first/final_polynomial.py`).

| id | type | k | source record | rows | brackets |
|---|---|---|---|---|---|
| type00_k9 | 0 | 9 | E-261101-23 night 6 (multipliers not stored then; regenerated 2026-11-03 from the stored model) | 13 | 46 |
| type53_k9 | 53 | 9 | E-261102-01 | 11 | 37 |
| type57_k8 | 57 | 8 | E-261102-01 | 20 | 58 |

```bash
python3 -I verify.py certificates.json --selftest
```

**Soundness.** For vectors in R^4 in general position every bracket is nonzero. A 3-term Grassmann-Pluecker relation
[tab][tcd] - [tac][tbd] + [tad][tbc] = 0 then has exactly one term D of sign opposite to the other two O1, O2, so
|D| = |O1| + |O2| > |Oi| and log|D| - log|Oi| > 0, a strict linear inequality in the values log|bracket|. Which term
is D depends only on the signs. `verify.py` re-derives each relation from its six brackets, recomputes the term signs
with its own permutation-parity rule, checks that the claimed dominant term is the odd one, and checks that the
positive rational combination of the chosen inequalities is the zero form; then a realization would give 0 > 0.
Self-tests: the GP identity in this sign convention on random integer vectors; a doubled multiplier and five flipped
signs per certificate are rejected; signs computed from 20 random integer configurations per certificate (realizable
by construction) are rejected.

**Linkage** (made with the encoder, not independent): `extract.py` (run from `research/12-faced-polyhedron/`) rebuilt each CNF from type and face set, its SHA-256
equals the record's `cnf_sha256`, and every certificate sign equals the sign of the recorded SAT model
(`cnf_rebuilt_matches`, `signs_match_model`).

**Scope.** Each certificate excludes one sign pattern on its listed brackets (in general position), hence that SAT
model and every model agreeing with it there. It excludes no type and no k-face sub-instance: other models of the
same CNF were not examined. Label: EXACT (reproduced by `verify_all.py`); not CERTIFIED, because the checker is written
by the same chain of AI sessions as the producer, not by a third party.
