---
name: candidate-check
description: Use whenever a search, solver or agent reports a candidate, a near-miss, zero violations, EMBEDDED, a solution, or a new witness polyhedron for the 12-face research, before anyone calls it a result.
---

# Check a candidate before it is called anything

Paths are relative to `research/12-faced-polyhedron/`. Definitions: `SPEC.md` §1-§4.

1. **Save it.** Save the candidate as JSON in a layout that `verification/verify_candidate.py` accepts (see
   its docstring). Write the numbers from the solver's own output; never re-type them.
2. **Run the check.** Use the venv `~/.venvs/polyhedra/bin/python`:

   ```
   verification/verify_candidate.py FILE --target S0
   ```

   For an auxiliary target, use `--all-pairs` (S1) or no flag (embedded on its map). Paste the full output.
3. **If S0 passes:**
   - Stop all other work.
   - Have the `adversarial-verifier` agent re-check it independently, without importing `code/ladder_exact.py`.
   - Re-check the planes at a second rounding scale. They are rounded at 1e-9 everywhere; also round at 1e-12.
   - Tell the owner at once.
4. **Degeneracies.** Check `SPEC.md` §3 explicitly:
   - four planes through a point;
   - coincident vertices;
   - zero-length edges;
   - a margin at the 1e-9 rounding scale.

   A near-miss counts only if it is non-degenerate and exactly re-checked.
5. **Classify** the candidate as one of:
   - an S0 solution;
   - an S1-S4 object, naming its target;
   - not embedded.

   Use the label EXACT only once `verify_all.py` reproduces it. For a lasting witness, add an entry to
   `witnesses/witnesses.json` (then run `witnesses/export_site.py` to show it on the site) and add its file to
   `verification/verify_all.py` CHECKS.
6. **Report** with the target label. Only an S0 PASS may be called "found" or "a solution".
