# E-261117-01: conclusion

**NO-ADMISSIBLE-CAYLEY-9-4**: no face-transitive cubic (9, 4) map with every face pair adjacent passes the census
admissibility rule. Stage B (formulas) had no input and did not run.

* **Runs**: pre-registration `6c5c288f`; stage A in the session, 2026-11-17, `bash run.sh stage_a` -> `results/census/`
  (10 workers, 5.9 s wall by `time`, <= 0.017 core-h as wall x workers). The manifest has no `wall_seconds` line:
  the formula-controls step wrote `controls/formula_controls.json` (PASS) and then crashed in its summary `print`
  (a key without a status); fixed in `formulas.py` after the run, no rerun (the saved report is complete).
  `dirty_files: 1` is the output directory itself (created before the manifest). Stage B and the owner launch: not
  needed. Total well inside the 1 core-h cap.
* **Controls** (all passed): Z7 gives exactly the one K7 census class (both methods); the five groups of order 12
  give exactly the one K12 census class whose Aut+ (order 12) acts freely on vertices (from A4; the other 58 classes
  and four groups give nothing); Roest-Vigh's map appears at (8, 3) (class 0); `brute` and `by_phi` agree on raw
  counts per group and on the class sets at (8, 3) and (9, 4); every class has F | Aut+. Formula side: Roest-Vigh
  pinned SAT, Roest-Vigh's planes on Mizhaev's map UNSAT-SOLVER (the negative failed as required); the nine-plane
  and C3 calibration controls had no target input (no admissible map). Helper test on the (9, 3) census: link
  automorphisms equal Aut+, exactly 8 free-C3 maps.

| Stage | Group | Labellings | Rotations tried (brute) | Raw | Valid | Admissible | Classes (valid / admissible) |
|---|---|---:|---:|---:|---:|---:|---|
| (8, 3) | Z8, Z4 x Z2, Z2^3 | 10, 28, 112 | 403200, 1128960, 4515840 | 0 | 0 | 0 | 0 / 0 |
| (8, 3) | D4 | 62 | 2499840 | 352 | 352 | 352 | 5 / 5 |
| (8, 3) | Q8 | 10 | 403200 | 96 | 96 | 96 | 1 / 1 |
| (9, 4) | Z9 | 8 | 2903040 | 0 | 0 | 0 | 0 / 0 |
| (9, 4) | Z3 x Z3 | 8 | 2903040 | 384 | 384 | 0 | 2 / 0 |

  (8, 3): six classes, Aut+ 8, 24, 8, 8, 8 (reflexible), 8 (Q8, reflexible); Roest-Vigh's is the first (D4).
  (9, 4): the two valid classes (Aut+ 9 reflexible, Aut+ 18 chiral) are "pillows": the three cosets of one
  subgroup of order 3 each carry two triangles with the same vertex triple, so three face triples meet at two
  vertices each. The census rule (E-261103-01 `admissible`) rejects them: two distinct vertices on the same three
  face planes.
* **Prediction vs outcome**: P1 (an admissible class exists, ~60 %) failed -> slice closed for planning. P2 and P3
  are void (no formula).
* **Exact verification**: no candidate; no `verify_candidate.py` call applies. `test_cayley.py` (in
  `verify_all.py`) reruns both stages by `by_phi` and matches the saved codes and admissibility flags.
* **What may be claimed**: every cubic (9, 4) map with all 36 face pairs adjacent whose orientation-preserving
  automorphism group is transitive on the faces is one of two classes, both with a repeated vertex triple, hence
  not the map of a polyhedron with nine mutually adjacent faces (EXACT computation; coverage PROVED-1: the Sylow
  argument of A3 and the slot / involution / rotation parametrisation, AI-written, unreviewed). At (8, 3) there are
  exactly six such classes (same labels). Scope: cubic, genus 4, face-transitive under Aut+ (which covers Aut).
* **What may NOT be claimed**: anything about non-face-transitive (9, 4) maps, genus 7 (face transitivity allows
  g = 1 mod 3; not enumerated), non-cubic objects, or "no nine-face object". No formula ran; no OM or geometric
  statement about the (8, 3) classes beyond Roest-Vigh's known realization.
* **Hypotheses**: H-261101-07 unchanged (open): the slice was empty before any geometry.
* **Verdict for the direction**: the face-transitive (9, 4) slice is EMPTY (EXACT, coverage PROVED-1); closed for
  planning. Cost 0.017 core-h.
* **Next step**: week item 2 (E-261117-02, N2). The (8, 3) list could serve as calibration inputs (five unrealised
  classes besides Roest-Vigh's); not queued here. A3 notes that this slice covers patterns 9 and 3+3+3 of
  A6; those patterns keep their non-face-transitive members.
* **Rows updated**: `STATUS.md` 3au and header, `ROADMAP.md` State done, `experiment-log.md` (2026-11-17),
  `paper/OUTLINE.md` B7, README, PLAN amendment.
