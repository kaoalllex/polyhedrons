# Prompt for a strategic review of the research (2026-11-01)

## How to run / Как запустить

**Option A, recommended: a new Claude Code session with access to the repository.**
1. Open the repository `kaoalllex/polyhedrons` on branch `main`, after PR #1 is merged; before that, use branch
   `claude/research-restructure`.
2. Pick the strongest model available (`/model`).
3. Paste everything between the two `-----` lines as the first message.

The reviewer writes `research/12-faced-polyhedron/reviews/strategy-review-2026-11-01.md`, and does not push.

**Option B: a chat without the repository.** Paste the prompt and attach these files from
`research/12-faced-polyhedron/`:
- `SPEC.md`, `STATUS.md`, `ROADMAP.md`;
- `reports/NIGHT_REPORT_2026-11-01.md`;
- `reviews/external-audit-2026-10-31-v3.ru.md`;
- `theory/theory-notes.md`;
- `proof-no-symmetric-immersion/README.md`.

This option is weaker: the reviewer cannot check code or data.

Вариант A: новая сессия Claude Code на этом репозитории, самая сильная модель, вставить текст между линиями `-----`.

-----

You are an independent senior reviewer of a research project. Think of a research mathematician in discrete and
computational geometry who has run computer-assisted proofs. Be skeptical, concrete and constructive. Never
fabricate results or citations. Mark every factual statement as VERIFIED (you checked it in code or data),
PLAUSIBLE or CONJECTURE. Small checks are welcome; do not launch any computation longer than about 10 minutes. Do
not modify files other than your report.

**PROBLEM.** Does a polyhedron embedded in R^3 exist with these properties?
- 12 planar simple faces;
- every two faces share exactly one complete edge;
- 3 faces at every vertex;
- hence V = 44, E = 66, genus 6.

It would be the 12-face analogue of the Szilassi polyhedron (7 faces, genus 1); short name: Szilassi-12. Its dual
is one of the 59 neighbourly genus-6 triangulations with 12 vertices. The vertex version is impossible (Schewe
2010). The face version is open.

**READ FIRST** (in `research/12-faced-polyhedron/`):
- `STATUS.md`: the ledger. It holds the foundations FD1-FD11, the exact witnesses, the directions DR1-DR17 with
  their measured verdicts, and what may be claimed.
- `ROADMAP.md`: the scored queue E01-E13 and the parked methods.
- `SPEC.md`: the targets S0-S4, the counters and the evidence labels.
- `reports/NIGHT_REPORT_2026-11-01.md`: the latest compute.
- `reviews/fresh-audit-2026-11-01.md` and `reviews/external-audit-2026-10-31-v3.ru.md` (Russian): the process
  audits.
- `theory/theory-notes.md` and `proof-no-symmetric-immersion/README.md`.

The code is in `code/` (registry in `code/README.md`). Run the evidence base with
`python3 verification/verify_all.py --quick` (about 15 s; needs `requirements.txt`).

**WHAT THE PROJECT HAS** (check, do not trust):
1. No symmetric embedding: 25/25 classes are UNSAT with DRAT proofs (CERTIFIED). This reproduces Moki & Julio 2026.
2. No symmetric polyhedral immersion: 25/25 DRAT-checked (EXACT). We believe this is new; the soundness write-up
   is pending.
3. Exact genus-3 objects with 12 faces and 48 of 66 pairs adjacent. One of them sits on a map that is
   combinatorially completable to the target map by 3 handles.
4. Genus 4 was never reached. A Gauss-map degree argument explains the plateau for type 0 (k_tau = 0, while
   -1 is needed).
5. 12,202 exact UNSAT results of "normals first". Their statistical power is low.

**QUESTIONS.** Answer each one; the order is the priority.
1. **Where should the next 3 months go?** Rank at most 5 directions by the expected value of information per
   unit of effort. Include directions the project has not listed. For each one give:
   - the hypothesis;
   - the cheapest test that could falsify it;
   - what each outcome changes;
   - a rough cost.
2. **Is the impossibility route realistic?** Consider a per-type exact decision (OM-SAT, rank-3 SAT,
   cube-and-conquer) or a structural lemma that kills many of the 59 types at once. What would a credible
   campaign cost, and what has to be true first?
3. **Is the construction route realistic?** Is there a class of geometric ansatz not yet tried, with a reason
   to expect it to break the genus-3 plateau? Examples: partial symmetry not in the 25 classes, a parametrised
   family, continuation from a degenerate configuration, lifting from a known object. Be concrete.
4. **Which intermediate goals are worth reaching for their own sake?** Assess these candidates:
   - maximal face-neighbourly cubic polyhedra per genus, (F, g) = (8, 2), (9, 3), (10, 4), (11, 5), with
     E - C(F, 2) = 2, 3, 3, 2 extra edges, i.e. doubled pairs (ROADMAP E13);
   - a genus-4 analogue of the Mizhaev / Röst–Vígh octahedra;
   - publishing results 1 and 2 above.
   
   Which of them is new? Which is likely feasible? Which would teach the most about Szilassi-12?
5. **Are the verdicts honest?** Look for a direction marked LOW-YIELD or OPEN-LOW that was underpowered, or that
   was tested with a flaw that invalidates the measurement. Look for a claim stronger than its evidence.
6. **How should the work be organised?** The team is one owner, an experienced software engineer who is not a
   mathematician, plus AI coding agents. There is a MacBook for nights and free GitHub Actions runners.
   - What should the owner do personally?
   - What should be delegated to agents?
   - What needs an outside human mathematician, and who would be a good first contact?

**OUTPUT** (`reviews/strategy-review-2026-11-01.md`):
- a 10-line verdict;
- an answer to each question;
- a ranked table of directions with hypothesis, test, cost and decision value;
- a list of errors or overclaims you found, with file:line;
- the 3 things you would do first next week.
