# E-261108-01: conclusion

2026-11-08. Explore run at S5 (9, 3). Scope (`SPEC.md` section 4): 300 exact uniform 9-plane arrangements from three
sources (100 Roest-Vigh + a random ninth plane, 100 Mizhaev + a random ninth plane, 100 random C2-invariant), hard CP
model (36 pairs, E = 39, <= 3 runs per pair). Not an S5 witness, not a 12-face result.

* **Runs**: 10 shards, commit 5dee969 (pre-registration), all shards exit_status 0, no BUDGET-STOP. Core-hours 1.33
  (sum of unit and control wall times from `results.jsonl` / `controls.jsonl`; shard `manifest.txt` records only the exit
  status, no CPU time), against the 2 core-h budget. Per unit 6.1-27.6 s (mean 15.3 s), cap 60 s.
* **Controls**: all 40 control runs (4 per shard x 10) as stated: tetrahedron E = 7 and nine-plane E = 33 INFEASIBLE;
  Roest-Vigh and Mizhaev E = 36 SOLID with the known map.
* **Prediction vs outcome**: (1) controls pass on all shards - yes. (2) >= 90 % of units decided in 60 s - yes, 300/300
  (`ended_by` completed, no timeout). (3) no SOLID - yes, 0/300.
* **Exact verification**: no candidate, so no `verify_candidate.py` / `candidate-check` run. No engine code changed
  (`nine.py`, `pilot.py` untouched); no `verify_all` run.
* **What may be claimed**: EXACT computation (re-solved CP models, no DRAT): for each of the 300 exact integer
  arrangements the hard model is INFEASIBLE, so no 36-pair disk-face solid exists on those arrangements. Geometric
  reading PROVED-1 via the E-261103-05 encoding argument. If the draws are treated as i.i.d. from their sources, the
  density of 36-pair solids per source (100 draws) is < 3 % and over the pooled 300 < 1 % (95 %, rule of three).
* **What may NOT be claimed**: any exclusion of S5 at (9, 3) or of Roest-Vigh/Mizhaev extensions in general (one random
  ninth plane per draw, a particular offset distribution); any exclusion of C2 solids (only the arrangement is
  C2-invariant, one involution type, mirror impossible); other symmetries, other caps. The draws are not a proven
  uniform sample of any family, so the bound is a heuristic under the i.i.d. assumption. No pair-count diagnostic was
  run (Phase B dropped in the plan), so nothing is known about near-misses. Draws needing re-rejection: 132 in total.
* **Verdict for the direction**: LOW-YIELD@1.33 core-h, 300 arrangements. Kill rule fired: park arrangement-first
  for (9, 3) with the bound above. H-261103-02 and H-261101-07 unchanged; no credence moves.
* **Observation (to the lead)**: with E-261107-01 this is 330 INFEASIBLE decisions in ~15 s each. No
  near-feasibility diagnostic was run (Phase B dropped), so how far these sources are from a 36-pair solid is not known. Whether the hard model is *too* strict
  (e.g. the <= 3 runs per pair cap, or E = 39 fixed) was checked only by the positive controls at 8 planes.
* **Next step**: none from this experiment (the Phase B follow-up branch was dropped). Week plan item 3 is next.
* **Rows updated**: `STATUS.md` 3v, `ROADMAP.md` E-261108-01 `done`, `experiment-log.md` 2026-11-08, README `done`.
