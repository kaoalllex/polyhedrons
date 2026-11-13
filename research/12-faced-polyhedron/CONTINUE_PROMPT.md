# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-13, week item 5 prepared)

* Branch `lab/2026-11-09`, committed, not pushed. Nothing in flight.
* E-261113-03 ready (PLAN amendment 1): 25,531 certified cells; pilot 50/50 UNSAT-SOLVER, mean 2.34 s, controls pass
  (planted cells P0, P4 SOLID with Roest-Vigh's map), projected 16.6 core-h, about 1.7 h wall on 10 cores.
* OWNER: `bash research/12-faced-polyhedron/overnight/launch.sh 261113-03 start` (on AC), then `status`; it resumes after
  the 50 pilot units. Then `experiment-conclude`: `census.py --summary results`; any NEW-MAP unit ->
  `verify_candidate.py raw/<unit>.output.candidate.json --all-pairs`, `candidate-check`; reading as in the PLAN.
* NEXT after the census: the week plan is done; the lead review decides Stage B and the items below.
* Checks: `test_census.py` 4/4, Stage A list regenerates byte-identical after the `cells.local_cells` refactor.
* For the lead: (1) march_cu (`~/bin/march_cu`, built by the owner) cube pilot on (10, 4) 96 / 85 as a changed set-up;
  (2) bridge ~10 % at (10, 2); (3) LOCAL at (8, 2) core mining; (4) does S6 (10, 3) keep first place; (5) the full 865
  of E-261113-02 or drop it.
