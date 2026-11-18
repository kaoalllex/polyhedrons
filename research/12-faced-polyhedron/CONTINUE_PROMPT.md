# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-18, week item 5 prepared; the owner night is next)

* Branch `lab/2026-11-16`. Week item 5, E-261110-04, pre-registered (`PLAN.md`, `night.py`, `run.sh`, `progress.sh`):
  c3 (C3 3+3+3) and c2 (C2 4 x 2 + 1, moved chart) at nine planes, E = 45 and 51, cap 20 s; geo2 / geo3 (D2 2 x 4,
  coefficients +-q^w, w <= 3) at E = 36, cap 15 s, 3000 draws per q. Stage A PASS; pilot 0.11 core-h, gate holds
  (c2 E = 45 UNKNOWN 2 of 5, close to the cap). A verified nine-face hit touches `results/stop.requested`.
* Owner: `bash research/12-faced-polyhedron/overnight/launch.sh 10-04 start` on AC (10 shards x 27000 s = 75 core-h).
* Next: after the night, `python3 night.py summary results`, then `experiment-conclude` (a hit: `candidate-check`
  first, Opus high). The night's results are not in git until then.
* For the lead (unchanged from 2026-11-17): a faster P4 host at nine elements; whether a P3 rerun earns a row (cube 5
  first); plane-only formulas for the (11, 5) Aut+ = 2 and (9, 4) one-face-involution maps only as a new registration.
