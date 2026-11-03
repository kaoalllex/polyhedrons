# E-261101-07: conclusion

* **Runs**: none. The question was answered by reading `code/gauss_gate.py` and `code/kdrift.py` and by a
  three-line check of the measuring function (strategy review 2026-11-01, Appendix A.3). No core-hours.
* **Controls**: the six octahedron axes (not in any closed hemisphere; true value of max_w min_i <w, v_i> about
  -0.58) return `-0.0` from `gauss_gate.hemisphere_margin`; 200 random 6-vector sets return 105 values of exactly 0,
  95 positive values and no negative one.
* **Prediction vs outcome**: the row allowed three outcomes (proof, counterexample, artefact). Outcome: **artefact**.
  The LP in `hemisphere_margin` has optimum t = 0 at w = 0 whenever the vectors are not in an open hemisphere, so
  the function floors at 0. `kdrift.py` added `20 * max(0, margin + 0.05)` to its energy, a target the function
  cannot reach. Moreover k_tau != 0 already implies that the six handle normals are not in an open hemisphere
  (the PL image of the handle sphere would otherwise miss the antipodal region), so "margin exactly 0 on 153/153
  class-reaching drifts" was guaranteed twice over.
* **Exact verification**: not applicable (no candidate).
* **What may be claimed** (EXACT on the function): `hemisphere_margin` returns 0 for every non-hemispheric input;
  the nights-4/5 "pinned margin" is a floor of the measurement, not a property of polyhedra.
* **What may NOT be claimed**: anything about how far in-class handle normals can move beyond the hemisphere wall
  while the base polyhedron stays embedded; that question is E-261101-19.
* **Verdict for the direction**: DR3 keeps FOUNDATION as a filter; the DR2 drift evidence is void (re-worded in
  `STATUS.md`). No new theory note beyond this file and `reviews/strategy-review-2026-11-01.md` 5.1.
* **Next step**: E-261101-19 (barrier continuation with a non-saturating measure).
* **Rows updated**: `STATUS.md` DR2, DR3; `ROADMAP.md` State done; `experiment-log.md` 2026-11-01.
