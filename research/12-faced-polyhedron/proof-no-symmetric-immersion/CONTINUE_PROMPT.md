# Prompt for a separate session on the symmetric-immersion proof

Copy everything below the line into a new Claude Code session on the repository
`kaoalllex/polyhedrons`, branch `claude/wonderful-carson-saxyck`.

---

You are working on one well-defined task in the repository `kaoalllex/polyhedrons`
(branch `claude/wonderful-carson-saxyck`): turning a computer-assisted result into a checked,
written proof. Read `research/12-faced-polyhedron/proof-no-symmetric-immersion/README.md` first —
it states the theorem, the current status of every part, and the ordered list of remaining work.
Background, when needed: `research/12-faced-polyhedron/mathematical-model.md`,
`verification/foundations-report.md`, `theory-notes.md` (Q2 symmetry analysis), `fresh-eyes-review.md`,
`results.md`, and the encoder `code/omsat.py` + `code/omsat_sym.py`.

The theorem: no polyhedral immersion in R^3 with planar faces of any of the 59 neighborly genus-6
12-face maps has a non-trivial isometric symmetry. Evidence: 25/25 symmetry classes UNSAT with
drat-trim-verified DRAT proofs (`overnight/results/symimm/`), using one encoder.

Do, in order:
1. Write a SECOND, independent encoder of the local clause families (face simplicity, at most one
   reflex corner per vertex, orientation consistency, symmetry action, normalizations) from the
   geometric definitions, WITHOUT reading `omsat.py` (you may read the mathematical model). Validate
   it against exact geometry (Fraction arithmetic) on random and Szilassi-derived configurations,
   check the controls (Szilassi n=7 SAT; #48 C2 without simplicity SAT), then run all 25 classes.
   Disagreement with the first encoder is a bug to be found, not averaged away.
2. Collect complete written soundness proofs of every clause family into
   `proof-no-symmetric-immersion/proof.md`; use an independent reviewer subagent
   (`adversarial-verifier`) on it.
3. Draft the 4-6 page note (`proof-no-symmetric-immersion/note.md`) with the table of the 25 cases
   (from the results JSONL) and reproduction instructions; prepare a short e-mail draft (English) to
   J. Bokowski and Kevin H. for the user to send himself.
Report to the user in Russian; write repository files in English; commit and push as you go.
Do not overclaim: the asymmetric 12-face problem remains open. Ask before launching large subagent
tasks (usage limits).
