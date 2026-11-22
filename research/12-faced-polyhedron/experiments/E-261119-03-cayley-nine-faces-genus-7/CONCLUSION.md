# E-261119-03: conclusion

**NO-ADMISSIBLE-CAYLEY-9-7**: no face-transitive cubic (9, 7) map with every face pair adjacent passes the census
admissibility rule. Stage B (plain formula) had no input and did not run.

* **Runs**: pre-registration `968deb68` (owner exception to T + D >= 3, 2026-11-22); first stage-A launch stopped by
  the session over its 0.2 core-h line (~10 min wall x 10 workers, ~1.7 core-h, no output; `results/aborted-1/`);
  amendment 1 `ece1eb0a` (canonical code only for admissible maps at (9, 7)); stage A rerun in the session,
  `WORKERS=9 bash run.sh stage_a` -> `results/census/`, 103 s wall (`results/census.manifest.txt`), <= 0.26 core-h.
  Probes and tests < 0.05 core-h. Total ~2.0 core-h against a planned <= 0.9: an overrun, all in the aborted launch.
  `dirty_files: 2` is the output and its log (created before the manifest).
* **Controls** (all passed): `test_cayley7.py` (6 tests in the run, 7 with the evidence test): `rho_dfs` equals the
  `brute` set per labelling on Z7 and order 8, gives nothing on Z9 at (9, 4), returns exactly K7 and the one
  vertex-regular K12 census class (the other 58 absent), and the admissible-only mode equals the full lists on
  (8, 3), (9, 4). Rung: `rho_dfs` reproduces the saved E-261117-01 brute raw counts per group and class lists at
  (8, 3) (Roest-Vigh's map inside) and (9, 4). The admissibility function returns both values on controls: True on
  all 448 (8, 3) rotations, False on the (9, 4) pillows.

| Group | Labellings | Raw (both methods) | Valid | Admissible | Seconds (9 workers): by_phi / rho_dfs |
|---|---:|---:|---:|---:|---|
| Z9 | 272 | 48768 | 48768 | 0 | 13.2 / 89.0 (both groups) |
| Z3 x Z3 | 272 | 522240 | 522240 | 0 | |

* **Session sample** (not ledger evidence; first three rotations per labelling): every sampled map repeats a vertex
  triple; in 180 of 360 Z9 and 792 of 816 Z3 x Z3 samples every repeated triple is a coset of an order-3 subgroup
  (the genus-4 pillow pattern), the others also repeat other triples. No single mechanism is claimed.
* **Prediction vs outcome**: P1 (no admissible class, ~65 %) held -> slice closed at genus 4 and 7. P2 void.
* **Exact verification**: no candidate; no `verify_candidate.py` call applies. `test_cayley7.py` checks the saved
  counts (in `verify_all`); a full rerun is `bash run.sh stage_a` into a fresh folder.
* **What may be claimed**: every cubic (9, 7) map with all 36 face pairs adjacent whose Aut+ is transitive on the
  faces has a repeated vertex triple, hence is not the map of a polyhedron with nine mutually adjacent faces (EXACT
  computation; coverage PROVED-1: the Sylow argument of PLAN.md and the slot parametrisation, AI-written,
  unreviewed). With E-261117-01: no face-transitive cubic nine-face S1 map at genus 4 or 7.
* **What may NOT be claimed**: anything at genus 10 or higher, about non-face-transitive (9, 7) maps, non-cubic
  objects, or "no nine-face object". The number of distinct inadmissible (9, 7) classes was not computed
  (amendment 1). No formula ran.
* **Hypotheses**: H-261101-07 unchanged (open; genus 7 lies outside its range, and the slice is empty).
* **Verdict for the direction**: the face-transitive nine-face slice is EMPTY at genus 4 and 7 (EXACT, coverage
  PROVED-1); closed for planning.
* **Next step**: none from this item; the week plan has no further lab item, so the lead review.
* **Rows updated**: `STATUS.md` 3bj and header, `ROADMAP.md` State done, `experiment-log.md` (2026-11-22),
  `paper/OUTLINE.md` B7, idea I-261119-03, README, `verify_all.py` line.
