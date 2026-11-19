# Prompt to continue this research in a new session

The standing rules are in the root `AGENTS.md` (Codex) and `CLAUDE.md` (Claude Code).
The `session-handover` skill updates the handover block below.

---

Continue the 12-face research in `research/12-faced-polyhedron/`.

Use the handover below and follow `PROTOCOL.md` §8 to choose and carry out the current stage.

## Hand-over (2026-11-19, E-261119-01 pre-registered and piloted; owner launch pending)

* Branch `lab/2026-11-19`; week plan in `ROADMAP.md` (owner-approved lead review 2026-11-19 and its reconcile).
* E-261119-01 (week item 1): PLAN `c6313628`, amendments 1 (`0cfcf241`) and 2 (`0de9a2f8`). The unpinned blocking control
  failed with the row's normaliser images (Roest-Vigh's map has 240 free-C2-invariant labellings, the normaliser reaches
  96) and was repaired once: every action-invariant relabelling of the run set is blocked; controls and both blocking
  controls pass. U4 decided in the pilot (D2 -> Roest-Vigh's map, S4 -> Mizhaev's, each then INFEASIBLE, UNSAT-SOLVER).
* Next: the owner runs `bash research/12-faced-polyhedron/overnight/launch.sh 261119-01 start` (U1 free C2 (8, 36) with
  blocking 1.5 h, U2 (8, 30) 1 h, U3 (9, 39) after U2; <= 17.5 core-h, about 2 h); then `experiment-conclude` with
  `python3 ladder.py summary results`. Item 2 (E-261119-02, stage A) may be prepared meanwhile.
* Watch: a model in U2 or U3 stops the run (`stop.candidate`) and goes to the clause-level diagnostic, never a result; a
  new realized (8, 3) map stops U1 and goes to `candidate-check`. Mirror (Cs) families are out of domain.
* For the lead: the normaliser rule under-blocks maps whose automorphisms hold non-conjugate free involutions
  (amendment 1); E-261119-02's per-map blocking should use invariant copies.
