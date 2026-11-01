# Prompt for a separate session on the symmetric-immersion proof (ROADMAP E08)

This work is ROADMAP item E08. It overlaps E07, the comparison of encoders. The rules in the root `CLAUDE.md`
apply. Paste everything below the line into a new Claude Code session on `kaoalllex/polyhedrons`.

---

You are working on ROADMAP E08: turning a computer-assisted result into a checked, written proof. Read these
files in `research/12-faced-polyhedron/` first:
- `SPEC.md`, for the labels;
- `STATUS.md` FD5/FD6;
- the E08 row of `ROADMAP.md`;
- `proof-no-symmetric-immersion/README.md`, which gives the theorem, the status of every part and the remaining
  work.

Background, when needed: `theory/mathematical-model.md`, `verification/foundations-report.md`,
`theory/theory-notes.md` (Q2), `reviews/fresh-eyes-review.md` and `code/omsat.py` + `code/omsat_sym.py`.

**The theorem.** No polyhedral immersion in R^3 with planar faces of any of the 59 neighborly genus-6 12-face
maps has a non-trivial isometric symmetry.

**The evidence.** All 25 symmetry classes are UNSAT, with DRAT proofs verified by drat-trim
(`experiments/E-261029-15-symmetric-immersion-certificates/results/symimm/`), using one encoder. The status is EXACT. It becomes CERTIFIED after this item:
written soundness argument, a second encoder and published certificates.

Branch: `experiment/E08-symmetric-immersion` from `main`. Use the `experiment-start` skill to create
`experiments/E08-symmetric-immersion/PLAN.md` before any compute. Do these steps in order:

1. **Second encoder.** Write a SECOND, independent encoder of the local clause families from the geometric
   definitions, WITHOUT reading `omsat.py`. You may read the mathematical model. The families are:
   - face simplicity;
   - at most one reflex corner per vertex;
   - orientation consistency;
   - the symmetry action;
   - the normalisations.

   Then:
   - Validate it against exact geometry (Fraction arithmetic) on random and Szilassi-derived configurations.
   - Check the controls: Szilassi n=7 is SAT, and #48 C2 without simplicity is SAT.
   - Run all 25 classes.

   A disagreement with the first encoder is a bug to find, not something to average away.
2. **Soundness proofs.** Collect complete written soundness proofs of every clause family into
   `proof-no-symmetric-immersion/proof.md`. Run `adversarial-verifier` on it. That agent is a filter, not an
   independent reviewer (`SPEC.md` §5).
3. **Note and e-mail drafts.** Draft the 4-6 page note `proof-no-symmetric-immersion/note.md`. It gives the
   table of the 25 cases (from the results JSONL) and reproduction instructions. Point to the DRAT release; the
   owner decides when to publish it. Prepare short e-mail drafts (English) asking for a human review, for the
   owner to send (ROADMAP E12). Possible recipients: J. Bokowski and Kevin H., A. Pirozhkov, Moki & Julio.

Finish with `experiment-conclude` and a PR into `main`. Do not push to `main` directly.

Do not overclaim: the asymmetric 12-face problem remains open.
