# Prompt to continue this research in a new session

Copy everything below the line into a new Claude Code session on the repository
`kaoalllex/polyhedrons`, branch `claude/wonderful-carson-saxyck`.

---

You are continuing an autonomous research project in the repository `kaoalllex/polyhedrons`,
branch `claude/wonderful-carson-saxyck`, directory `research/12-faced-polyhedron/`.
Goal: the open Series-1 problem from the README — a polyhedron embedded in R^3 with 12 planar simple
11-gonal faces, every two faces sharing exactly one complete edge, three faces per vertex
(V=44, E=66, genus 6). Find and exactly verify one, or prove impossibility (fully or for some
combinatorial types). Never weaken the requirements; never fabricate results. Report to the user
in Russian; write repository files in English; commit and push intermediate results.

Read first: `sprint-board.md` (every hypothesis tested, with verdicts), `results.md`,
`proof-roadmap.md`, `solution-portrait.md`, `fresh-eyes-review.md`, `theory-notes.md` (PI addendum
+ local lemma), `mathematical-model.md`, `external-review-results.md`, `HOW_TO_RUN_OVERNIGHT.md`.
Agent definitions: `.claude/agents/` (7 roles).

State at the end of session 1:
* Formulation: a candidate = 12 planes; all conditions are strict sign conditions (uniform
  chirotope of 12 planes + plane at infinity); Lemma 5.1 and the in-face predicate were
  adversarially verified (`verification/foundations-report.md`).
* Combinatorics: exactly 59 types (independent enumeration).
* Symmetric case: 25/25 classes UNSAT with drat-trim-verified DRAT proofs (our encoder, user's
  machine): no symmetric 12-face polyhedron. Moreover, without the global non-intersection clauses
  all 25 classes are UNSAT too (no symmetric polyhedral IMMERSION; unverified here — night 2
  phase 1 produces the DRAT proofs into `overnight/results/symimm/`).
* Topology: any embedding has Gauss-map degree -5 with convex covering (proved, incl. a local
  lemma). All 1005 known near-misses (HackerPoet) fail this: they are in the wrong topological
  class and not even immersions (>= 7 locally overlapping vertices each).
* Asymmetric case: immersion instances (no global clauses) did not resolve in 2.2 h per type
  (types 0-7). Full asymmetric OM-SAT is estimated at ~300 core-hours per type.
* Fixed normals: the obstruction is cohomological (fresh-eyes review): faces close locally but
  not around the 12 handles. `code/period_defect.py` measures it (MILP; Szilassi 0; random
  admissible normals 17-24; annealing on type 0 reached 13.5 and was still decreasing).
* Night 2 (`overnight/run_night2.sh`, user's machine): phase 1 `symimm` (certified "no symmetric
  immersion"), phase 2 `pdefect` (period-defect annealing over all 59 types; defect 0 = CANDIDATE).

State at the end of session 2 (2026-10-29, evening):
* CERTIFIED: no symmetric polyhedral immersion (25/25 UNSAT-VERIFIED, `overnight/results/symimm/`);
  separate write-up task in `proof-no-symmetric-immersion/` (own CONTINUE_PROMPT).
* Period defect (`pdefect`, night 2): zero closure defect is reachable (pd10_0, pd37_0, pd4_1, pd5_1)
  but every such normal set is a FALSE POSITIVE: exact closure needs >= 11 of 12 faces to be
  non-simple (simple-defect MILP, proved optimal for pd10_0 and pd4_1). The T^3 relaxation shows
  the same. Face simplicity is the core obstruction, not closure. The job now checks simple faces
  itself (status ZERO_DEFECT_NOT_SIMPLE). Best positive defects per type: `experiment-log.md`.
* Own path "ladder" (`code/ladder*.py`, no external data): closed polyhedra with n mutually adjacent
  faces; maps generated from scratch; exact rational verifier `code/ladder_exact.py` (agrees with
  `planes.check_embedding`). n = 7: Szilassi rediscovered from random planes by every engine
  (annealing, GA, CMA-ES). n = 8 (genus 2, two doubled adjacencies): four engines (annealing, exact
  one-plane relocation, GA, CMA-ES) all stop at 1-2 violations. Three optimizer exploits were caught
  by the exact verifier (merged collinear doubled edges, gap overlaps between doubled edges, scale
  collapse); the honest energy is `ladder.pair_energy`. Maps for n = 9..11 are not generated yet
  (random rotation-system annealing fails; needs a better generator).
* Night 3 is ready (`overnight/run_night3.sh`, see `HOW_TO_RUN_OVERNIGHT.md`): `ladder` (GA on n = 8,
  exact check of zeros) and `sdefect` (12 faces: closure defect to 0, then non-simple faces to 0).
* Idea lists: `cross-field-ideas.md` (rounds 2a-2c incl. complex numbers), `search-algorithms.md`
  (tried engines + to try: Differential Evolution, Nevergrad NGOpt, smooth least squares, MAP-Elites,
  cross-entropy, RRR, homotopy continuation). Research map: `figures/research-map.png`.
* Practical lessons: background processes in the cloud container die when the session idles
  (container restarts) - long runs belong to the user's night scripts; every float "zero" must be
  re-checked exactly; never `pkill -f` a pattern that also occurs in the same shell command.

First tasks (session 3):
0. `git pull`; analyze the newest `overnight/results/` (pdefect, and ladder/sdefect after night 3):
   any CANDIDATE first, re-checked exactly (`code/ladder_exact.py` for the ladder; for 12 faces
   `period_defect.torus_simple(..., general=False, phi=0)` and `planes.check_embedding`).
1. Ladder n = 8: decide it exactly (OM-SAT on 9 elements with the doubled-adjacency conditions) or
   switch the rung to two 4-valent vertices; try the engines listed in `search-algorithms.md`.
Older first tasks (session 1):
1. `git pull`, then analyze `overnight/results/symimm/` (expect 25 UNSAT-VERIFIED) and
   `overnight/results/pdefect/` (best defect per type; any ZERO_DEFECT / CANDIDATES first: run the
   exact gauge-fixed offset SMT `code/fixed_normals_gauge.py` on those normals, then the exact
   checker). Record results in `results.md`, `sprint-board.md`, `experiment-log.md`.
2. If defects plateau above 0 for all types: study the LP dual (Farkas) certificates of the period
   obstruction for a human-readable lemma (proof direction). If some reach 0: exact search there.
3. Keep hypotheses fast and many (startup style: sprint board), and ask before launching large
   subagent tasks (usage limits).
