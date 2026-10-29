# Prompt to continue this research in a new session

Copy everything below the line into a new Claude Code session on this repository
(branch `claude/wonderful-carson-saxyck`).

---

You are continuing an autonomous research project in the repository `kaoalllex/polyhedrons`,
branch `claude/wonderful-carson-saxyck`, directory `research/12-faced-polyhedron/`. The goal is
the open Series-1 problem from the README: a polyhedron embedded in R^3 with 12 planar simple
11-gonal faces, every two faces sharing exactly one complete edge, three faces at every vertex
(V=44, E=66, genus 6). Find and exactly verify one, or prove impossibility (fully or for some
combinatorial types). Never weaken the requirements; never fabricate results.

Read first, in this order: `research-plan.md`, `mathematical-model.md`, `results.md`,
`literature-review.md`, `theory-notes.md`, `hypotheses.md`, `next-steps.md`,
`experiment-log.md` (latest entries), `overnight/README.md`. Agent definitions are in
`.claude/agents/` (7 roles with models/effort); in a new session they load as real agent types.

State at the end of session 1 (2026-10-29):
* Reduction: a candidate is 12 planes; no equalities; embedding <=> 176 forbidden-triple
  conditions (Lemma 5.1), all expressible in the uniform chirotope of 12 planes + plane at
  infinity. Two independent encoders exist and agree with exact geometry
  (`code/omsat.py` formulation A = fixed type/unknown chirotope; `code/geomsat.py`
  formulation B = fixed planes/unknown triangulation; `code/planes.py` exact checker).
* Combinatorics: exactly 59 types, independently re-enumerated (`data/`).
* Prior work (third-party, unrefereed, AI-assisted, see literature-review.md): symmetric
  realizations claimed impossible (DRAT-certified); we independently reproduced 4 cases
  (Lutz #54 T, #3 D3, #48 D3, #48 C2: UNSAT). Asymmetric case open (~19,000 core-hours
  estimated for full OM-SAT). Best known near-misses (HackerPoet): 4 violations (symmetric),
  5 on maps with trivial automorphism group.
* Our experiments so far: geometry-first SAT on 30 random 12-plane arrangements: all UNSAT,
  best-triangulation violation counts 23-39. Exact single-plane relocation from the best
  asymmetric near-miss (5 violations): no improvement in 33 relocations (all plateau moves).
* New method E1 (`code/fixed_normals.py`): with the face normals fixed, all signs are linear in
  the 12 offsets, so existence for fixed normals is an exact SMT(LRA) problem. Validated on
  Szilassi (n=7, normals perturbed up to sigma ~0.15: SAT, exact check passes). On n=12 seeds it
  needs >300 s per instance; the `overnight/run_overnight.py normals` job runs it at scale.

First tasks:
1. If `overnight/results/` contains new results (the user runs the overnight jobs locally and
   pushes them), analyze them: any `CANDIDATES/` first (re-verify independently in exact
   arithmetic with a fresh checker before believing anything), then UNSAT/UNKNOWN statistics of
   `normals`, `sym` verification status, `cube` refuted fraction, `ils` improvements.
   Record the analysis in `results.md` and `experiment-log.md`.
2. Continue with the ranked plan in `next-steps.md` (j-plane OM-SAT neighbourhoods around
   near-misses; Track 6 clause families F7-F9 (Gauss degree, covering, >= 13 saddles) as
   prefilters for the normals search; E3: choose normals with Gauss-map degree -5).
3. Commit and push intermediate results (English) as they accumulate; report to the user in
   Russian. Usage limits may be tight: prefer local computation over many subagents, and ask
   before launching large subagent tasks.
