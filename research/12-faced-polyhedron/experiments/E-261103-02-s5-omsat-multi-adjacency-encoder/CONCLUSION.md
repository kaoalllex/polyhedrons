# E-261103-02: conclusion

## Runs and controls

Pre-registration: `5dc2caa`, based on the E-261103-01 result `e13b79e`, on
`experiment/E-261103-02-s5-omsat-multi-adjacency-encoder`. No target solving, new census campaign,
long run, subagent, push or PR. Two bounded single-worker runs:

| Run | Wall seconds | Recorded core-hours | Binding limit |
|---|---:|---:|---|
| `results/pilot/` | 4.917281 | 0.001365911 | prescribed controls completed |
| `results/0/` | 206.528460 | 0.057369017 | prescribed counts completed |
| Total | | 0.058734928 | |

The full run used 22.95% of the 900-second hard cap and completed within its 600-second control budget.
No control reached a solver timeout. Manifests include input/output SHA-256, Python dependencies,
parameters, commit, dirty state, and exact source snapshots. Development test commands outside these
two runs have no resource manifests and are not included in the recorded total. After the source snapshots, only
nonsemantic encoder cleanup, extra evidence-replay tests, and a further S0 full-group hash check were
added; the archived source snapshots identify the precise computation versions.

| Exact direct-geometry control | Accepted uniform inputs | Degenerate attempts rejected | Predicate mismatches | EMBEDDED | Not EMBEDDED |
|---|---:|---:|---:|---:|---:|
| Roest-Vigh | 1000 | 0 | 0 | 416 | 584 |
| Mizhaev | 1000 | 0 | 0 | 356 | 644 |
| Szilassi | 1000 | 25 | 0 | 506 | 494 |

All six Boolean predicates (IN, REFLEX, RTURN, E, line order, side) take both truth values in each
object's sample. Inputs are fixed-seed integer perturbations at six noise radii; every accepted
configuration and its outcome is retained in `*.perturbations.jsonl.gz`. The checks also compare
the forbidden-triple plus disjoint-segment verdict with exact direct embeddedness, and require every
embedded configuration to satisfy all optional sound clause families. No float defect threshold is used.

Original Roest-Vigh and Mizhaev planes are already uniform: their own Eval formulas have no violations,
and their original chi-pinned CNFs are SAT. Raw Szilassi has three zero quadruples; its fixed uniform
perturbation passes the same controls. All asserted chirotope signs match the stored SAT models;
all named CNF predicates agree with Eval. Original inputs and perturbation details are retained.

Negative controls:

* Roest-Vigh planes on the Mizhaev map: pinned CNF UNSAT, independently checked by unit propagation
  on the stored DIMACS. Scope: only those planes, map and clause families. CNF, solver DRAT and the
  independently verified empty-clause RUP certificate are retained.
* One-sided swapped parallel-edge pairing: rejected at map construction. All 37 inadmissible (9,3)
  census maps return EMBEDDED False from `ladder_exact.verify` without raising and are rejected by
  `Triangulation`. The verifier guard already existed in `e13b79e`, so no verifier rewrite was needed.

## Compatibility and stopping criterion

Seven S0 circuit baselines match `e13b79e`: plain and orbit-normalized formulas for types 0, 15, 58,
plus type 58 with its complete 12-element automorphism group. `s0_baseline.json` fixes variable counts,
clause counts and serialized circuit SHA-256; the last comparison was also made directly against
modules loaded from `git show e13b79e`. Existing benchmark-ladder submaps still construct successfully.

Both maximal cases reuse E-261103-01 inputs; every admissible (8,2)/(9,3) map constructs successfully,
including maps with tripled adjacency. `results/0/first_8_2.cnf.gz` is the full embedding formula for
the first (8,2) census record: 126 chirotope variables, 4269 total variables, 35651 clauses. Its map,
formula and hashes are retained. It has **not been solved**. The README's control/build stopping
criterion is met.

## Symmetry scope and obstruction

Free C2 (8 faces) and free C3 (9 faces): exact uniform proper-rotation plane configurations satisfy
symmetry-only GP formulas under their asserted chirotopes. These controls do not assert embedding
clauses and do not realize the corresponding census maps.

The tested C2 action fixing a face forces four zero quadruples; the tested D3 action forces twelve.
Their uniform symmetry-only formulas are UNSAT, with retained CNFs, DRAT and independently verified
unit refutations. **These are not geometric exclusions.** PROVED-1: a fixed cooriented face X, exchanged
faces A,B, and infinity form an invariant quadruple with odd permutation, forcing chi = -chi = 0.
A nonuniform encoder is needed to cover these symmetry-preserving families; perturbing away symmetry
permits use of the asymmetric uniform formulas. `SOUNDNESS.md` records this limitation and the
single-author extension of Lemma 5.1. The next experiment's README and queue wording carry the warning.

## Claims, verdict and next step

**EXACT:** the stated bounded control computations, the saved CNF models/unit refutations, rejection
controls and S0 regression. `verification/verify_all.py --quick` includes `test_encoder.py`: artifact
hashes and SAT models, negative unit refutations, S0 circuit hashes, own-map controls and replay of
all six perturbation-radius cells per object. The full sample is reproducible with `controls.py`;
the quick regression does not repeat all 3000 direct-geometry comparisons.

**PROVED-1:** the multi-segment soundness note and the forced-zero symmetry argument; no human review.
No CERTIFIED theorem is announced, no S5 map has been decided, and no new witness/FD row is created.
No inference about geometric nonexistence follows from the fixed-face symmetry UNSATs. No independent
external encoder comparison (E-261101-09 step 1), realizer test, or nonuniform extension was run.
The archive recheck and GitHub CI were not run; the required quick verifier is recorded at hand-over.

Verdict: **FOUNDATION** for the S5 encoder, **PROMISING** for DR19; scenario credences unchanged.
No tested hypothesis changes (`tests: []`). Next: E-261103-03, pre-register bounded (8,2) decisions
first, with proofs retained; free-C3 controls are ready, fixed-face C2/D3 must not be counted as
geometric decisions. No target run is authorized by this conclusion.

Rows updated together: STATUS 3b / DR19, ROADMAP E-261103-02 state and dependency wording,
experiment-log; README and CONTINUE_PROMPT carry the completed hand-over.

Final local verification: `~/.venvs/polyhedra/bin/python verification/verify_all.py --quick`
returned **ALL PASS** (17 checks passed, archive check skipped). The dedicated encoder regression
ran seven tests with no failures or skips. `git diff --check` passed.
