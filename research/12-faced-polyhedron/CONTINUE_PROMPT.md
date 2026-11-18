# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-18, week item 3 waiting for the owner run)

* Week branch `lab/2026-11-18`. Week plan: `ROADMAP.md` -> Week plan (`reviews/strategy-review-2026-11-18.md` §1).
* Items 1, 2 done (STATUS 3az, 3ba). Item 3, P3-sym (E-261118-02), running: controls pass; the D2 / S4 rung passed in
  the pilot (Roest-Vigh's and Mizhaev's maps unaided in 2.3 s and 5.0 s, both realized, `--all-pairs` PASS; known
  objects). Amendment 1 registers C3 3+3+3 at nine faces (E = 45, 51, 57, 1 h, 5 workers) + the plain cube-5 side
  unit; C3 pilot at 60 s: all UNKNOWN, gate passed. `launch.sh` now refuses a dirty tree outside results (audit 2).
* Next: the owner runs `bash research/12-faced-polyhedron/overnight/launch.sh 261118-02 start` (<= 17 core-h,
  <= 2.3 h). Then `experiment-conclude` (`p3sym.py summary results`); any realized nine-face model ->
  `candidate-check` and the owner first.
* For the lead: (1) Cs 4 x 2 + 1 and Cs 3 x 2 + 3 are outside P3-sym: two mirror pairs of planes are concurrent, so
  chi(0123) = 0 in every chart (PLAN deviation 1; I-261118-02's family list and `STRATEGY.md` §1 need correcting).
  (2) The curved-face encoder (E-261118-04) and (3) the two unrealized map-29 models stay open from items 1, 2.
