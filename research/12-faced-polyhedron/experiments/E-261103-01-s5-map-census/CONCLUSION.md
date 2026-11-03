# E-261103-01: S5 candidate-map census

## Outcome

All four requested cases exhausted. These are abstract dual maps of S5 candidates, not embedded
polyhedra. No geometric realization or non-realizability statement follows.

| (F, g) | Classes, mirror identified | Distinct-corner classes | C enumeration seconds |
|---|---:|---:|---:|
| (7, 1) | 1 | 1 | 0.000148 |
| (8, 2) | 2 | 2 | 0.001158 |
| (9, 3) | 240 | 203 | 1.203256 |
| (10, 4) | 1183 | 1117 | 38.075081 |
| (12, 6), S0 control | 59 | 59 | 15.245258 |

The admissible (9,3) automorphism-order histogram is 1:173, 2:22, 3:6, 6:2; eight maps have a
free C3, 24 have an involution, none is reflexible. At (10,4) the histogram is 1:1021, 2:83,
3:11, 4:2; 85 have an involution and one is reflexible. Full fixed-cell data are in each record.

## Controls and verification

* **EXACT:** The two (8,2) and all (9,3) canonical-code sets equal the review's sampled sets,
  including inadmissible maps. Pairing is recovered uniquely from both endpoint corners in those
  sample records; no repeated triple is collapsed into a single triangle.
* **EXACT:** K7 is one chiral class with |Aut+|=42. K12 equals all 59 FD3 canonical classes,
  orientation-preserving orders and reflexibility flags, not just the total count.
* **EXACT:** A separate Python triangle-orbit exact cover exhausted its C3 search and obtained
  exactly the same eight admissible free-C3 codes: 28,531 search nodes, 2,052 covers before the
  vertex-link and equivariant-gluing checks. This is an independent algorithm, not a human review.
* **EXACT:** `verification/verify_all.py` includes the nine focused tests: corruption and wrong-Euler
  rejection, repeated-triple admissibility rejection, reflection/relabel invariance, timeout semantics, occupied-output preservation,
  archived-output hashes, every saved map and its automorphisms, catalogue/sample/C3 equality, and a
  fresh exhaustive (9,3) run matching all saved codes. No `verify_candidate.py` call applies: there
  are no plane coordinates or geometric candidates.
* **PROVED-1:** Completeness rests on the coverage arguments in `PLAN.md`: extra-graph augmentation,
  root-rotation normalization and exhaustive triangle assignment; for the C3 control, invariant
  triangle sets and every equivariant parallel-edge gluing. These arguments have no human review.
  The computation is reproducible; the mathematical coverage claim is not CERTIFIED.

A C build with AddressSanitizer and UndefinedBehaviorSanitizer also exhausted (9,3), matching
the saved class count with no diagnostics. `bash -n run.sh` passes.

The optional (8,3) census was not attempted: it has eight extra edges and is outside the required
maximal cases. Its published maps were not used as an enumeration control in this experiment.

## Prediction, hypotheses and decision

The (8,2) and (9,3) completion predictions succeeded; the uncertain (9,3) minute-cap prediction
resolved positively. The stretch also finished inside its amended minute cap. H-261103-01 is
supported by exhaustive computation (coverage PROVED-1); H-261101-07 remains open: no geometry ran.
No S5 scenario credence changes. DR19 remains PROMISING. The exact geometric queue keeps its
existing focus inputs; the larger stretch list replaces its sampled lower bound.

Next: E-261103-02, the multiple-adjacency OM-SAT encoder and known geometric controls. E-261103-03
still waits for that encoder. E-261103-07 can use the exported (10,4) census rather than repeat it.

## Provenance and limitations

Pre-registration: `e834e86`; base `a037d4e`. All five C pilots record that pre-registration commit,
dirty flag, source/input/output hashes, compiler, platform, Python, pip freeze and one worker in
`results/*/manifest.json`. Their exported datasets are `results/maps_F_g.json`, ordered with
admissible symmetric maps first. `results/exports.json` records source/export hashes; original
indented JSON is gzip archived byte-for-byte. Raw canonical-code streams and progress are retained.
Compiled executables are hashed in the manifests but deliberately not archived; rebuild from C.

The five pilots plus the provenance-recorded C3 repeat account for **0.0227297884 core-hours**.
The first exploratory C3 check (`results/c3-crosscheck.json`) lacked a manifest and is excluded
from this sum; it is not needed as evidence because `c3-verified.json` repeats it with provenance.
Development tests and final verification are also outside the experiment compute ledger.
Source files were dirty during development; hashes identify the measured versions. Later changes
add compact output, pip cache suppression, the comparison adapter, occupied-output protection and the POSIX clock feature
macro; the fresh (9,3) test checks the final enumerator against the saved codes.

No geometry, OM-SAT formulas, DRAT runs, long jobs, external review, push or PR were performed.
STATUS section 3c/DR19, ROADMAP, both hypothesis evidence sections and the session handover are updated.

Final local verification: `verification/verify_all.py --quick` returned ALL PASS (the archive
re-check skipped as intended). The first catalogue-comparison test exposed string-keyed `links`
in the existing K12 JSON; its test adapter now normalizes those keys. No census output changed.
`git diff --check` reports only blank-at-EOF warnings in the two zero-extra-edge `graphs.txt`
inputs: their empty edge-pattern lines are retained to preserve the recorded input hashes.
