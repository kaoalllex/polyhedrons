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

## Hand-over (2026-11-03, after E-261103-02)

* **Branch:** `experiment/E-261103-02-s5-omsat-multi-adjacency-encoder`, local, not pushed, based on
  the census result `e13b79e`. Pre-registration `5dc2caa`; implementation and results are in the
  following local session commit. E-261103-01 data are reused, without a new census campaign.
* **Done:** the multi-adjacency, variable-face-count OM-SAT encoder passes its bounded controls
  (EXACT); S0 formulas retain their base hashes. Counts, resources, scope and artifacts live in
  `experiments/E-261103-02-s5-omsat-multi-adjacency-encoder/CONCLUSION.md`. The extended argument
  is PROVED-1, without human review. The existing repeated-corner verifier guard was tested.
* **Limitation:** fixed-face C2 and the tested D3 action force zero determinants. Their uniform
  symmetry-only UNSATs do not decide geometric families. Free C2/C3 have uniform positive controls;
  use asymmetric formulas or a separately pre-registered nonuniform extension for fixed-face cases.
* **Artifacts:** `results/0/first_8_2.cnf.gz` and `.map.json` in the encoder experiment, built only;
  original-control pinned CNFs/models, negative CNFs/DRAT/unit refutations, perturbation inputs and
  provenance/source snapshots. `test_encoder.py` is in `verify_all.py`; the quick replay checks
  saved evidence and all six radius cells per object, not the full perturbation sample.
* **In flight:** nothing. No target solve, night run, subagent, push or PR.
* **Next:** E-261103-03 with `experiment-start`, pre-register the (8,2) decisions first. Reuse
  E-261103-01 datasets and -02 predicates/controls. Keep every target CNF and checked proof.
  Do not treat uniform fixed-face symmetry contradictions as geometric exclusions.
* **Owner actions:** integrate local experiment branches through a PR with verify green when ready;
  no push or PR authorized. Previous branch cleanup, literature e-mails and Zenodo remain owner actions.
* **Not checked:** target realizability, nonuniform extension, external encoder/human review, archive
  recheck, GitHub CI. The required `verify_all.py --quick` returned ALL PASS (archive skipped).
