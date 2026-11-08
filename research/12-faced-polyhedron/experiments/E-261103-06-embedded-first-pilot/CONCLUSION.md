# E-261103-06: conclusion

2026-11-07. Explore R1 pilot of embedded-first at S5 (7, 1) only. Scope (`SPEC.md` §4): this implementation
(28 x 28 torus mesh, damped block-coordinate flattening, discrete intersection check), 4 valid starts. No (8, 3) or
(9, 3) rung was run. Not a result about the idea in general.

* **Runs**: commit after 630645b plus the PLAN amendments; one shard, 1 worker. `results/0`: 7.7 s, 0.002 core-h.
  `results/run1-superseded` (start-construction bug, same flattening code): a few seconds. Total far below the 1
  core-h budget. Pilot and debugging runs in scratch are not counted.
* **Controls**: all passed: energy 0 on coplanar, 25 on random points, 92 on the round-torus start; the detector flags
  the spindle torus and not the round torus; the exact tail accepts the perturbed Szilassi planes (`--target S5`
  PASS) and returns INFEASIBLE with one plane moved. The K7 start control passed for j = 2, 3 and failed for j = 4
  (empty region, defect in my start construction, not investigated): two BAD-START of six.
* **Prediction vs outcome**: (1) controls as stated - yes. (2) at least one of 6 starts reaches energy < 1e-12
  (~30 %) - no: 0 of 4 valid starts. (3) the barrier is the active limit - yes, but not in the registered sense: see
  below.
* **Outcome**: all four valid starts (R/r 2, 3; j = 2, 3) end BLOCKED after 3-6 accepted steps: the energy falls from
  150-191 to 84-118 (about halved), then every step down to 1/128 of the clipped correction is rejected by the detector.
  The hits found in one diagnosed start are triangle pairs sharing a vertex or one ring apart (local folds or
  near-coplanar overlap), not distant sheets. It is not shown whether these are genuine folds or detector
  artefacts on nearly coplanar triangles. This is a block, not a converged plateau.
* **Exact verification**: no converged start, so no tail on a surface; no `candidate-check` needed.
* **What may be claimed** (EXACT computation, instance scope): the 4 starts above are blocked by this barrier
  implementation at energy 84-118. The controls pass.
* **What may NOT be claimed**: that embedded-first is dead or its kill criterion (plateau with the barrier active)
  is met in its proper form; that R1 is impossible; anything about finer meshes, tangential regularisation, smooth
  contact handling (IPC-type) or other starts.
* **Verdict for the direction**: R1 not achieved; UNDERPOWERED rather than refuted (no positive case where the
  method converges). H-261101-07 and scenario credences unchanged. Per the row, the idea is parked with this failure
  mode; R2' (8, 3) was not run (follow-up tree: R1 fail -> park).
* **Next step**: none from the lab. For the lead: whether to fund a repaired flattening (tangential mesh
  regularisation, contact-sliding barrier, finer mesh) before R2'; the failing quantity is local folds at ring <= 1.
* **Rows updated**: `STATUS.md` 3u, `ROADMAP.md` E-261103-06 `killed`, week plan item 2, `experiment-log.md`, README.
