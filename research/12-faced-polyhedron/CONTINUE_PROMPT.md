# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-22, item 4 E-261116-09 done; E-261119-02's 10 % run stopped by the owner at 50 %, resumable)

* Branch `lab/2026-11-19`; week plan in `ROADMAP.md` (owner-approved lead review 2026-11-19 and its reconcile).
* Item 2, amendment 6: the owner stopped the random 10 % of (9, 5) pass 1 at 49194 of 97830 maps (all UNSAT-SOLVER,
  5 SKIPPED-STOP); `bash overnight/launch.sh 261119-02 start` resumes it. Its reading belongs to the owner's other session.
* Item 4 done (STATUS 3bi, `experiments/E-261116-09-uniformity-perturbation-lemmas/CONCLUSION.md`): L1-L6 PROVED-1
  (L6 at degree <= 4 only); part B: no common family set, SYM not needed, parity Lemma P exact on 3 + 17 records.
* Next: item 5 (optional) or the lead; owner decides on chunks 10-99 after the 10 % (amendment 6).
* For the lead: the priced (9, 4) / (9, 5) stage-B UNSATs do not use the symmetry (drop SYM: 69 of 69 UNSAT; plain
  formula UNSAT-SOLVER on 36 of 36 (9, 5)); the remaining 90 % of pass 1 likely tests plain non-realizability. A parity
  pass (GF(2), no solver) over all 978228 + 12562 records, then the plain formula, may be worth more; not priced here.
* For the lead: L6 at k = 5, 6 (non-generic central stars appear there) is the open part of I-261108-09.
* For the lead: a P3-sym UNKNOWN at nine faces carries no information until a refutation rung decides (3bd).
* For the lead: E-261119-01 overran its hard 20 core-h by 6.8 (a discarded first launch); its normaliser rule under-blocks.
