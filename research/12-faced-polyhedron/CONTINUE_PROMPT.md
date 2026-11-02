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

## Hand-over (2026-11-02, evening)

* **Branch.** Still `experiment/E-261101-25-chirotope-first` (on top of `claude/strategy-review-2026-11-01`); all
  work committed there. Owner: one PR of the stack into `main` when convenient (`verify` green).
* **Done this session**: E-261101-26 first scope concluded (`CONCLUSION.md`, `STATUS.md` 3b): chirotope-first with
  the E-261102-02 settings reaches R1 20/20 and R6k k = 7 / 8 / 9 at 5/10, 1/10, 1/10, but R4 0/10 and 0/10 and R5
  0/10 (80 units, 6.6 core-h). Every failure stopped at `--alt 20` after 16-36 % of its time. `launch.sh start DIR CORES` now sets `SHARDS`, and
  runners skip units recorded in any shard. PROTOCOL §2.4 / §2.5: the pilot gates the long run (binding limit,
  budget fraction, projected outcome, one prediction that can fail), and a long run is a grid over the binding
  parameter. E-261102-02 is **blocked**; new rows E-261102-03 and E-261102-04 (folders with README, no PLAN yet).
* **Completed**: the 16 missing units of E-261101-26 (resumed run, all 80 units, `CONCLUSION.md` Amendment: R1 20/20,
  R4 0/10 and 0/10, R5 0/10, R6k 5/10, 1/10, 1/10; verdict unchanged). Nothing is running.
* **Next session, in order**:
  1. (done 2026-11-02) E-261101-26 scored on all 80 units.
  2. `experiment-start` E-261102-03 (cap or wall): an `--alt` override in `ladder.py`, the PLAN with the pilot gate
     and a budget grid (40 / 120 min), a day pilot of one R4 type-15 seed.
  3. `experiment-start` E-261102-04 (genus-ladder search on the ladder): `ladder.py --engine genus-ladder` calling
     `code/genus_ladder.search`, R1 / R4 / R5, a day pilot. Nights 7+ can share cores between -03 and -04.
  4. In parallel by day: E-261101-06 (rank-3 SAT per type), the exact side; an independent checker of the three
     stored final-polynomial certificates (types 0 k = 9, 53 k = 9, 57 k = 8).
* **E-261102-02** is launched only with the amendment that E-261102-03 decides, or killed.
* **Open owner actions:** merge the branches; send the first external e-mail (E-261101-11 README "Why and whom");
  Zenodo DOI (Phase 0 TODO).
* **Do not** use `gauss_gate.hemisphere_margin` as an objective or a diagnostic (floors at 0, E-261101-07).
