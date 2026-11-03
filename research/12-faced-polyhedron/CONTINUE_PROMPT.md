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

## Hand-over (2026-11-03, evening, after the strategy review was applied)

* **Branch.** `claude/strategy-review-2026-11-03`, pushed; PR into `main` opened 2026-11-03 (`gh pr view` on the branch).
  If the PR is merged, branch `experiment/E-261103-01-s5-map-census` from `main` for the next item; if not, continue on
  this branch.
* **Done this session**: `reviews/strategy-review-2026-11-03.md` (verdict, answers, queue, audit, S5 credences) with its
  reproducible sampler `reviews/strategy-review-2026-11-03-flipwalk.py` and the sampled maps
  `reviews/strategy-review-2026-11-03-maps.json`; the review applied with the owner's approval: S5 queue E-261103-01 to
  -07 in `ROADMAP.md` (S0 queue parked), `STATUS.md` 3c and DR19, SPEC S5 wording (multiplicity >= 2), H-261103-01 to
  -03, I-261103-02 to -06, `ladder_exact.verify` guard against repeated corner triples. `experiment-log.md` 2026-11-03.
* **In flight**: nothing. No night run is planned; the first candidates for a night are E-261103-03 ((9, 3) part) and
  E-261103-04, each only after its `PLAN.md`.
* **Next session, in order**:
  1. **E-261103-01 (census of the candidate maps)** with `experiment-start`: `PLAN.md`, then the enumerator (design in
     the README: `enum_k12.c` generalised to multiple edges, or the (phi, alpha) dart representation of the sampler),
     controls (7, 1) = 1 class with |Aut+| 42, (12, 6) = 59 with the FD3 orders, every sampled class of the review's JSON
     contained, the two (8, 3) maps contained if that case finishes. Output in `links` format with admissibility and
     automorphism data.
  2. **E-261103-02 (OM-SAT encoder for multiple adjacencies)** can start in parallel: it does not depend on the census;
     validation on the Roest-Vigh and Mizhaev chirotopes, negative control, 0 predicate mismatches.
  3. Then E-261103-03 part (a): the two (8, 2) maps, hours of compute, DRAT kept, realizers on any model.
* **Open owner actions**: merge the PR (`verify` green); delete the merged branches (`claude/strategy-review-2026-11-01`,
  `experiment/E-261101-25-chirotope-first`, `claude/research-restructure`); the S5 letter to Roest-Vigh and Mizhaev and
  the first `polyhedraproof` e-mail (E-261101-11); Zenodo DOI (Phase 0 TODO).
* **Do not**: run any geometry on the (9, 3) target before E-261103-01 and -02 are done; call the sampled counts (240 /
  203 / 8, 2) a census; use `gauss_gate.hemisphere_margin` as an objective or a diagnostic (E-261101-07).
