# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-22, week items 1, 3 and 5 done, item 2 skipped)

* Branch `lab/2026-11-22`. Week plan: `ROADMAP.md` "Week plan". Done: item 1 (STATUS 3bk), item 3 (E-261117-04 stage B,
  STATUS 3bl: the equivelar (9, 4) census, 4118 classes, 1071 admissible, every control passed) and item 5 (STATUS
  3bm: E-261119-02 concluded, the random 10 % of the C2 (9, 5) list 97830 of 97830 UNSAT-SOLVER, 14.32 core-h; power
  lines, the 862-action note, the parity scope correction, `tests:` links removed). Item 2 skipped (no input).
* Next: **item 4, P6 stage C** (the plain (9, 4) pass): a PLAN amendment (the second since the lead review; a third is
  an escalation) with its unit tests first; records from `results/census_9_4/maps_9_4.json` (admissible classes,
  `p6.py` stage-A `build`/`queue` pattern generalised to (9, 4), 10 elements, cap 60 s, lean, 10 shards), controls the
  f9 pinned pair and the ten K2 maps. Price (NUMERICAL): 1071 x 8.1 s ~ 2.4 core-h, far below the plan's 5-31; the
  stratified first chunk decides whether it fits a lab run (<= 50 min wall) or stays an owner night.
* The close-out commit holds `audit_pass1.py`, `pass1_summary.json` (SHA-256 of every shard's `results.jsonl`), the
  manifests and night logs of `results/stageB5-pass1*`; the 77 MB of lean `results.jsonl` stay untracked.
* Tooling: `p6.py census-b|merge` (stage B), `run.sh` (`Q=` queue), `p6.py summary|followup`; `control_rv8.json`.
