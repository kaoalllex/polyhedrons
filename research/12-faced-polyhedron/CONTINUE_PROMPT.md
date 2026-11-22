# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-22, E-261119-02 amendment 6 ready: the random 10% of (9, 5) pass 1 awaits the owner launch)

* Branch `lab/2026-11-19`; week plan in `ROADMAP.md` (owner-approved lead review 2026-11-19 and its reconcile).
* Item 2: (9, 4) all UNSAT-SOLVER (3bf); C3 (9, 5) empty (3bg); C2 (9, 5) 978228 classes (3bh). Amendment 5: lean runner,
  36 of 36 priced UNSAT-SOLVER. Amendment 6 (owner): pass 1 on a random 10% first (chunks 0-9, 97830 maps, cap 5 s,
  20 core-h hard cap, ~14 core-h, ~1.4 h); checks passed (lean SAT units keep folders, smoke 0.50 core-s per unit).
* Owner launch: `bash overnight/launch.sh 261119-02 start` (`STAGE=B5p1`; status shows `progress.sh`; stop resumable).
  Chunk files are not committed: on a new checkout `python stageb.py --g5-pass1` rebuilds them (hash-pinned).
* After the 10%: `experiment-conclude`-style reading per amendment 6 (TIMEOUTs -> pass 2; SAT -> bridge, escalate); then
  the owner chooses chunks 10-99 (~122 core-h, `CHUNKS=10-99`, new amendment for the cap) or the lemma (item 4).
* For the lead: one status across all (9, 4) and priced (9, 5) symmetric formulas, each < 1 s; a common-obstruction lemma
  (item 4) may be worth more than the remaining 90%.
* For the lead: a P3-sym UNKNOWN at nine faces carries no information until a refutation rung decides (3bd).
* For the lead: E-261119-01 overran its hard 20 core-h by 6.8 (a discarded first launch); its normaliser rule under-blocks.
