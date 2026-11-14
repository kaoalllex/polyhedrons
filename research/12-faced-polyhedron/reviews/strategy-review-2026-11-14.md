# Strategy review, 2026-11-14: the plain S5 / S6 formulas ran without the reorientation normalisation

## Owner digest (ten lines; the rest is reference)

1. **Verdict (Recommendation).** Keep targets and stance. Much of the "solver wall" is an encoder option left off:
   the plain S5 / S6 formulas carry no reorientation or mirror units (EXACT, §1).
2. **Session check (NUMERICAL, UNSAT-SOLVER, 0.13 core-h):** with the existing `symbreak` / `mirror` options on, five
   known UNSAT maps at (8, 2), (9, 3), (10, 4) are decided **10-89x faster**; the positive controls stay SAT.
3. **No recorded result becomes wrong** (adding clauses keeps UNSAT; SAT models stay models). Prices change: (10, 4)
   A + B from about 6 nights to under one (estimate); the (10, 3) twenty may fall inside the cap (untested).
4. The 2026-11-13 week plan is done: five items in one day, 17.8 core-h, no candidate; Stage B stays parked.
5. **Approval 1: the week plan of §2. First item:** the twenty (10, 3) formulas with the units, <= 20 core-h.
6. **Approval 2: (10, 4) S5 returns as item 2**, one night <= 80 core-h (`STRATEGY.md` wording in §3).
7. **Later:** no proofs in items 1-2; if a whole list ends UNSAT-SOLVER, a proof replay now fits the laptop. I ask then.
8. **Your realization-space notes:** no separate programme, no hitting-set pilot; two pieces enter the plan (§3).
9. march_cu cubes, the full 865, thin wedges: not now (§3).
10. **Not done:** no target formula run, no proof; the mirror unit is checked on three objects only; no human review.

## 1. Scope and checks

Evidence cut: `9f4dcf13` on `lab/2026-11-09`. Labels: `SPEC.md` §5; **Recommendation** marks a judgment.

* **Finding (EXACT).** `code/omsat_validate.py:24-25` (`ALL_OPTS`) sets neither `symbreak` nor `mirror`, and
  `experiments/E-261103-03-s5-exact-decision-8-2-9-3/tranche.py:153` builds every plain S5 / S6 formula from it: the
  (10, 3) formula of Lutz #1 has 0 unit clauses on chirotope variables. S0 formulas have the units
  (`code/immersion_sat.py:17`, `overnight/run_overnight.py:990`), so S0 prices do not move.
* **Check** (`reviews/strategy-review-2026-11-14-symbreak.py` and `.json`; kissat 4.0.4, 9 processes at once, known
  answers only; a session check, not ledger evidence; all UNSAT-SOLVER on both sides):

  | formula | plain s | with units s | ratio |
  |---|---:|---:|---:|
  | (8, 2) #0 | 7.98 | 0.09 | 89 |
  | (9, 3) #40 | 58.66 | 1.12 | 52 |
  | (10, 4) #845 (plain hash equals the record) | 145.84 | 4.40 | 33 |
  | (10, 4) #96 | 1073.49 (recorded, E-261108-03) | 25.32 | 42 (33 after the load factor 0.77) |
  | (10, 4) #85 | 2748.86 (recorded) | 210.77 | 13 (10) |

  Two (10, 2) maps stay SAT (0.3-0.7 s plain, 1.3-1.7 s with units); Roest-Vigh, Mizhaev and Szilassi, re-gauged
  (two after a mirror image), are SAT pinned. Not run: any (10, 3) formula (needs a PLAN); `verify_all.py --quick`.

## 2. Week plan (ready for `ROADMAP.md`; at most 10 cores, 10 shards, the owner launches every run)

1. **Normalised S6 (10, 3)** (exploit, jump 2; new experiment, PLAN first).
   * Question: are the twenty `submap=True` formulas decided within 3600 s once `symbreak` and `mirror` are on?
   * Prep: (a) exact invariance test of every `ALL_OPTS` clause family under one-element reorientation and the
     mirror on random uniform chirotopes (`omsat.Eval`), one PROVED-1 paragraph; (b) re-gauged positive controls
     pinned SAT (Roest-Vigh, Mizhaev, Szilassi, convex f9 / f10, grooved box, the 16 realized (10, 2) objects), the
     50 (10, 2) maps unpinned SAT; (c) the 2 (8, 2) and 203 (9, 3) formulas with units all UNSAT-SOLVER (minutes),
     ratios on 845, 96, 85; (d) pilot Lutz #1, #2 at 1200 s.
   * Gate: a failed positive control -> one retry with reorientation units only, then escalate; both pilot units
     TIMEOUT -> no day run, item 4 first. Run: 20 maps, cap 3600 s, <= 20 core-h, no proofs, bridge on every SAT.
   * Follow-up: SAT -> at least 30 models by seed, bridge, `--target S6`, `candidate-check`, escalate; all
     UNSAT-SOLVER -> planning reading, the lead proposes a proof replay; > 20 % TIMEOUT -> item 4. Lab: Opus, high.
2. **(10, 4) S5, strata A + B with the units** (exploit, jump 2; E-261110-06 reopened; needs approval 2).
   * Prep on item 1's controls: the 10 maps of E-261103-07 (10 / 10 TIMEOUT plain), cap 1800 s, price the 757 maps.
     Projected <= 80 core-h -> one owner night, cap 3600 s, bridge on every SAT, no first-SAT stop; above -> the
     fastest patterns first inside one night. Follow-up: SAT -> 30 models, bridge, `--target S5`, `candidate-check`,
     escalate; all UNSAT-SOLVER -> the lead proposes the proof replay and N3. Lab: Opus, medium; conclusion high.
3. **Bridge recovery control** (explore; < 1 core-h, chained with item 1's prep).
   * The exact chirotopes of the 16 realized (10, 2) objects through `tranche.bridge`, three optimizer seeds; 30
     solver seeds on five maps never realized. Recovery >= 0.8 -> the bridge is adequate and the remedy is many
     models per SAT; <= 0.3 -> one session on the realizer before a target SAT is judged. Lab: Opus, medium.
4. **Chart normalisation at a hull vertex** (N2, I-261110-06; only if item 1 has > 20 % TIMEOUT or item 2 > 1 night).
   * Lemma to write (PROVED-1 at most): some convex vertex `a, b, c` is a hull vertex; with a plane just outside it
     sent to infinity, INF is a positive combination of the three outward planes, so `chi(i, j, k, INF)` is forced
     whenever the signs against `a`, `b`, `c` agree. Control: exact re-charting of the control objects at every
     hull vertex (verifier PASS, formula and selector clauses satisfied). Pilot: one cube per vertex on the two
     slowest normalised maps, <= 3 core-h. Kill: summed cube time >= 0.7x monolithic on both. Lab: Opus, high.
5. **(8, 2) immersion core** (explore; registered follow-up of E-261110-05; one session, <= 1 core-h; Opus, medium).
   * Face-grouped minimal cores of V1 on (8, 2) #0, #1, with units; a core on <= 6 faces -> one theory session, else park.

## 3. Answers

* **Lead 1, march_cu on 96 / 85.** Not now: the units give 10-42x there; reopen only for maps still at TIMEOUT after
  items 1 and 4. **Lead 2, bridge about 10 %.** Item 3. **Lead 3.** Item 5. **Lead 4.** S6 (10, 3) stays first.
* **Lead 5, the full 865.** Drop as designed (D = 0, the same sample 17 times); "are all 865 realizable?" is a
  one-night census below the significance filter, only on the owner's word. **Lead 6, thin wedges.** Not this week;
  no decision depends on it. **Lead 7, far cells.** No session: a datum for the idea file N5.
* **Owner, `STRATEGY.md` (proposed, not applied).** §1: "S5 at (10, 4) second, by the normalised formulas, one night;
  nine faces third, Stage B parked". PLAN template: "A target formula lists its clause families and normalisations
  and uses the option set validated in FD4, or says why not."
* **Owner, the realization-space notes** (three untracked `NEW-IDEA-*.md` at the repository root; Recommendation).
  The meta-space is the face-plane space already in use; e-means does not apply. The proposed pilot (dependency
  sets of violated predicates, a hitting-set bound) is below the gate: conflict analysis in the solver derives
  stronger statements from the same predicates plus the Grassmann-Pluecker clauses. Fixed-normal convexity is FD8,
  Farkas transfer is E-261101-24, the literature repeats I-261029-41, -45, -46 (not checked here, CLAIMED). Gain:
  "which transformations to quotient out" has two paying answers (§1, item 4), "transitions" one test (N4).

## 4. Scores (T D F G R, J = jump, cost to the first result that could park it)

| Candidate | T D F G R | J | Cost to first kill | Note |
|---|---|---|---|---|
| Item 1, normalised (10, 3) (new) | 2 2 2 2 2 | 2 | 1 session + <= 20 core-h | changed set-up, measured on controls |
| Item 2, (10, 4) A + B with units (E-261110-06) | 2 2 2 2 2 | 2 | 1 session + 1 night | T, G up: under a night |
| Item 3, bridge recovery (new) | 1 2 2 2 2 | 0 | < 1 core-h | decides how a target SAT is read |
| Item 4, hull-vertex chart (I-261110-06) | 2 2 2 2 2 | 0 | 1 session + <= 3 core-h | conditional; serves S0 too |
| Item 5, (8, 2) immersion core | 2 1 2 2 2 | 0 | 1 session | lemma candidate |
| N3, (11, 5) census and cost probe | 2 2 2 2 2 | 2 | 1 session | only after item 2 |
| N4, handle-neighbourhood SAT | 1 2 2 1 2 | 0 | 1 session | only if (10, 3) stays at TIMEOUT |
| march_cu cubes; I-261108-02 lex-leader | 1 1 2 2 2; 1 1 1 2 2 | 0 | <= 3 core-h; 1 session | D down: after the units |
| E-261112-02 Stage B | 2 1 1 1 2 | 2 | 2 nights | parked, unchanged |
| I-261110-01 wedges; I-261113-04 fixed-face C2 | 1 1 1 2 1; 1 1 1 1 2 | 2 | 1-2 sessions | D down; C2 moot if item 1 decides |
| Full 865; hitting-set pilot | 1 0 2 1 2; 1 1 2 1 2 | 0 | 4 core-h; 1 session | below the gate (§3) |

As filed: E-261101-08, E-261110-01, -03, -04 and the other open ideas and hypotheses; S0 scores of 2026-11-09 stand.

## 5. Queue (after the week plan)

1. **Item 1** (first; exploit). H: a (10, 3) formula is SAT. A realized SAT is a result of the class of the
   eight-face objects; all UNSAT-SOLVER -> proof replay proposed. Stop: 20 maps recorded or 20 core-h.
2. **Item 2** (exploit). H: a (10, 4) map of strata A, B is SAT. One night; either outcome ends E-261110-06.
3. **Item 3** (explore). H: the bridge recovers realizable chirotopes; decides the reading of an unrealized SAT.
4. **Proof replays** (exploit; owner's word, the PLAN names the claim) of the lists that ended all UNSAT-SOLVER.
5. **Item 4**, **N3**, **item 5**, **N4** (all explore): one session each, conditions and kill rules in §2 and §6.

## 6. New ideas (untested proposals, not evidence)

* **N1. Normalised asymmetric formulas** (items 1, 2). Why: §1. **N2. INF as a positive combination at a hull
  vertex** (item 4): the three-line form of I-261110-06 forces 3 (F - 3) signs; this puts clauses on all C(F, 3).
* **N3. (11, 5), the last S5 rung below S0.** Census by the E-261103-01 enumerator (two doubled pairs, as at (8, 2)),
  then three formulas at 12 elements with units; kill: above about 10^4 maps or hours per formula.
* **N4. Handle-neighbourhood SAT** (only if (10, 3) keeps TIMEOUT units). Remove a handle of a (10, 3) map, realize
  the (10, 2) parents, solve the (10, 3) formula with phases or assumptions from a parent's chirotope. Known-answer
  rung: genus-2 parents in the archive. Differs from E-261101-25: 11 elements, SAT calls of seconds.
* **N5. Realization-space geometry (owner's notes)**: one idea file under DR10 / DR13 / DR17; actionable parts N2, N4.

## 7. Audit

1. **Unnormalised formulas priced the strategy.** `code/omsat_validate.py:24-25`; `STATUS.md:269` ("the 10x goal is not
   met"), sections 3ad (6.06 nights), 3af (20 / 20 TIMEOUT), 3aj (cube ratios); `STRATEGY.md:90-93` demoted (10, 4) on
   that price. `ideas/I-261110-06-chart-normalisation-hull-vertex.md:27` assumes the breakers are on.
2. **Claims stronger than their evidence.** `STATUS.md:372-373` "discovery power ... measured": it is planted
   recovery (2 / 2) plus two cells of the same map, one solid per cell. `ROADMAP.md:172` "cubes do not pay": one
   fallback cube basis, lowest-index cubes. `STATUS.md:348`: genus-2 time-to-SAT (nine free pairs) read onto genus 3.
3. **Text budgets** (`PROTOCOL.md:215`): CONCLUSION 58 / 50 / 45 lines against 25, PLAN 114 / 86 against 80 (E-261113-*).
4. **Process.** Five lead decisions in six days (`STRATEGY.md:84-102`), none compared the options of the target
   formulas with the validated S0 encoder. The root notes make run manifests dirty (E-261113-04 CONCLUSION, line 7).
5. **Chains to stop**: the full 865, march_cu on 96 / 85, thin wedges, longer caps on unnormalised formulas.

## 8. Credences (all CONJECTURE, planning weights)

* (10, 3) S6 exists: **0.25 -> 0.20** (ten symmetric formulas UNSAT-SOLVER, the T family empty); item 1 is the datum.
* (10, 4): **0.10 / 0.50 / 0.40 -> 0.10 / 0.60 / 0.30** (10-42x on three known maps: A + B and a proof replay fit).
* Nine faces, genus >= 4: **0.55 stays**; a hit inside the two ninth-plane families: **0.03 -> 0.01**. S0: unchanged.

## 9. Three things to do first

1. Owner: approvals 1 and 2. 2. Lab (Opus, high): item 1 prep with item 3 chained, then the owner's day run.
3. Lab (Opus, medium): item 2 prep on the same controls, then the owner's night.

## Owner's decisions (2026-11-14)

Approvals 1 and 2 given (week plan; (10, 4) second in `STRATEGY.md`). Applied the same day; the credences of §8 and
the PLAN-template sentence of §3 are not applied (not asked).
