---
name: candidate-check
description: Use whenever a search, solver or agent reports a candidate, a near-miss, zero violations, EMBEDDED, a solution, or a new witness polyhedron for the 12-face research, before anyone calls it a result.
---

# Check a candidate before it is called anything

Paths and commands are relative to `research/12-faced-polyhedron/`. Use `python3` from an activated environment
with `requirements.txt` installed. Definitions: `SPEC.md` §1-§4; the focus target and its (F, g) are in `STRATEGY.md`.

1. **Save it.** Save the candidate as JSON in a layout that `verification/verify_candidate.py` accepts (see
   its docstring). Write the numbers from the solver's own output; never re-type them.
2. **Run the check for the stated target.** For the focus S5 target:

   ```
   python3 verification/verify_candidate.py FILE --target S5
   ```

   Also check that the reported face count and genus match `STRATEGY.md`; an S5 PASS at another (F, g) is an
   auxiliary result. For S0 use `--target S0`; for S1 use `--all-pairs`; no target flag checks embedding on the
   given map only. Paste the full output and name any target conditions the selected check does not cover.
3. **If the stated target passes:**
   - Stop all other work.
   - Have the `adversarial-verifier` agent re-check it independently, without importing `code/ladder_exact.py`.
   - For floating-point input, re-check the planes at a second rounding scale: 1e-12 as well as 1e-9.
   - Tell the owner at once.
4. **Degeneracies.** Check `SPEC.md` §3 explicitly:
   - four planes through a point;
   - coincident vertices;
   - zero-length edges;
   - a margin at the 1e-9 rounding scale.

   A near-miss counts only if it is non-degenerate and exactly re-checked.
5. **Classify** the candidate as one of:
   - an S0 solution;
   - an S5 object, reporting (F, g), adjacency multiplicities, and whether it matches the focus target;
   - an object for another SPEC target, naming the conditions actually checked;
   - not embedded.

   Use the label EXACT only once `verify_all.py` reproduces it. For a lasting witness, add an entry to
   `witnesses/witnesses.json` (then run `witnesses/export_site.py` to show it on the site) and add its file to
   `verification/verify_all.py` CHECKS.
6. **Report** with the target and `SPEC.md` §5 evidence label. Only an S0 PASS may be called a solution of the
   12-face problem. An S5 PASS at the focus (F, g), with the required checks, is a focus result.
