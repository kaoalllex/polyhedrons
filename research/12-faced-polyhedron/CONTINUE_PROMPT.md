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

First tasks:
1. `git pull`, then analyze `overnight/results/symimm/` (expect 25 UNSAT-VERIFIED) and
   `overnight/results/pdefect/` (best defect per type; any ZERO_DEFECT / CANDIDATES first: run the
   exact gauge-fixed offset SMT `code/fixed_normals_gauge.py` on those normals, then the exact
   checker). Record results in `results.md`, `sprint-board.md`, `experiment-log.md`.
2. If defects plateau above 0 for all types: study the LP dual (Farkas) certificates of the period
   obstruction for a human-readable lemma (proof direction). If some reach 0: exact search there.
3. Keep hypotheses fast and many (startup style: sprint board), and ask before launching large
   subagent tasks (usage limits).
