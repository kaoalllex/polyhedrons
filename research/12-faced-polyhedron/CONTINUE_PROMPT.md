# Prompt to continue this research in a new session

The standing rules are in the root `CLAUDE.md`, which loads automatically. This file holds only the hand-over:
what was in flight when the last session ended. The `session-handover` skill rewrites the block below. Paste the
part under the line into a new Claude Code session on `kaoalllex/polyhedrons`.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

1. Read `STATUS.md` and `ROADMAP.md`.
2. Read the hand-over below.
3. Unless the owner names another task, work on the top `open` row of `ROADMAP.md`, using the `experiment-start`
   skill.

## Hand-over (2026-11-03, after E-261103-01)

* **Branch:** `experiment/E-261103-01-s5-map-census`, local, not pushed. Based on `a037d4e`
  (the previous strategy-review PR is merged). Pre-registration commit `e834e86`; results and
  code are in the following local session commit. No PR has been opened for this experiment.
* **Done:** E-261103-01 exhausted all four required cases and the K12 control. Counts and limitations
  live in `STATUS.md` section 3c and the experiment's `CONCLUSION.md`. The sampled (8,2)/(9,3)
  code sets match; the separate C3 exact-cover enumeration matches the symmetric sub-list.
  Computations are EXACT via `verify_all.py`; mathematical coverage is PROVED-1, no human review.
* **Artifacts:** `experiments/E-261103-01-s5-map-census/results/maps_F_g.json`, with full dart codes,
  `links`, admissibility and automorphism data; symmetric admissible maps first. Raw streams, manifests,
  original-output gzip archives and export hashes are retained. `test_census.py` is in `verify_all.py`.
* **In flight:** nothing; no night run, no subagents, no geometry. All tests and pilots have exited.
* **Next:** top open row E-261103-02, using `experiment-start`: multiple-adjacency OM-SAT encoder,
  known Roest-Vigh/Mizhaev controls, negative control and predicate agreement. Then E-261103-03,
  first the (8,2) maps. Do not run geometry on (9,3) until -02 passes its controls.
* **Stretch:** E-261103-07 should reuse the (10,4) census from -01; only further symmetry/geometry
  preparation remains. Do not repeat that census unchanged.
* **Owner actions:** integrate this branch through a PR with `verify` green when ready (no push or PR
  was authorized this session); previous branch cleanup, S5 letters to Roest-Vigh/Mizhaev, the first
  `polyhedraproof` e-mail and Zenodo DOI remain owner actions.
* **Not checked:** optional non-maximal (8,3) census, geometry, external human review, GitHub CI.
  The archive re-check is skipped by `verify_all.py --quick`. The first exploratory C3 diagnostic
  lacked a manifest; its provenance-recorded repeat supplies the evidence (see CONCLUSION.md).
