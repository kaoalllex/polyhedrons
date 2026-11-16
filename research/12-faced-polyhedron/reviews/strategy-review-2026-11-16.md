# Strategy review, 2026-11-16: (10, 4) is closed at solver level; (11, 5) prices the last rung and S0

## Owner digest (ten lines; the rest is reference)

1. **Verdict (Recommendation).** Keep the stance; replace the target list: target 2 is finished, target 1 hit the wall again.
2. **(10, 4) S5: every one of the 1117 admissible maps is UNSAT-SOLVER** (C 360 plain, A + B 757 normalised in 14.2 core-h;
   STATUS 3ad, 3ao; NUMERICAL, no checked proof). With (8, 2), (9, 3) decided, three S5 rungs are negative. STATUS never says so.
3. **S6 (10, 3)** is still undecided: both normalised pilots TIMEOUT at 1200 s; the hull-vertex cubes ran at a 10 s cap (no information).
4. **Session check (NUMERICAL, 2 min):** the census enumerator at (11, 5) gives 4099 classes, **3986 admissible** (not small).
5. **Approval 1: week plan §1. First item: (11, 5) census and cost probe** (<= 10 core-h); it also prices S0 (59 formulas).
6. **Approval 2 (your call):** is "(10, 4) excluded at formula scope" a claim you want? If yes, item 3 prices a proof replay
   (LRAT, one session) before any night. If no, (10, 4) stays UNSAT-SOLVER and nothing is replayed.
7. **Approval 3 (later, conditional):** a one-day S0 price probe if the (11, 5) median is <= 20 min (item 4); S0 stays parked otherwise.
8. **Not done:** no target formula run; (11, 5) census is a session check, not ledger evidence; no human review.

## 1. Week plan (ready for `ROADMAP.md`; at most 10 cores, 10 shards, the owner launches every run, no proofs unless item 3)

1. **(11, 5) census and cost probe** (I-261114-03; new experiment, PLAN first; exploit, jump 2).
   * Census: rerun `E-261103-01/census.py 11 5` with its manifest (session check: 3986 admissible, 44 s;
     `reviews/strategy-review-2026-11-16-census-11-5.json`); Euler and admissibility checks, S0 control unchanged.
   * Controls: the E-261114-01 positive / negative sets plus convex f11 pinned and unpinned at 12 elements.
   * Probe: 10 admissible maps by a frozen seed, stratified by doubled-pair pattern ([1,1,1,1] 5, [1,1,2] 4, [2,2] 1),
     normalised formulas, kissat, cap 3600 s, 10 shards, <= 10 core-h; bridge and 30 models on any SAT.
   * Output: censored price of the 3986 maps; median time against element count 9, 10, 11, 12 (existing records).
   * Follow-up: price <= 1 night -> owner night, fastest pattern first; 1-4 nights -> lead; > 4 nights or >= 5 / 10
     TIMEOUT -> no sweep, only the 24 symmetric maps by symmetric formulas (minutes, N3). SAT -> 30 models,
     `--target S5`, `candidate-check`, escalate. Median <= 20 min -> the lead asks approval 3 (item 4).
   * Kill: census differs on rerun, a failed control. Lab: Opus, medium (existing runner at a new size); conclusion high on SAT.
2. **S6 (10, 3) cube pilot** (new; exploit, jump 2; replaces the NO-DAY-RUN branch of E-261114-01).
   * Lutz #1, #2 normalised: march_cu cubes (built by the owner, untried) at a depth giving 100-500 cubes, cube cap
     600 s; in the same day run `kissat --sat` on both at 3600 s. <= 8 core-h, 10 shards.
   * Controls: cube cover (formula plus "no cube holds" is UNSAT-SOLVER); one SAT (10, 2) map through the same pipeline.
   * Follow-up: a map decided (all cubes UNSAT, or a SAT cube, or `--sat` decides) -> one owner night on all 20 by
     that method, <= 80 core-h; SAT -> 30 models, `--target S6`, `candidate-check`. Neither decided -> **park S6 (10, 3)**
     as solver-limited at laptop scale (OPEN, no negative); no long-cap night unless the owner asks.
   * Lab: Opus, medium.
3. **(10, 4) proof pricing** (only with approval 2; audit, jump 0; the PLAN names the claim: STATUS exclusion of (10, 4)).
   * One session: CaDiCaL `--lrat` with a linear LRAT checker against kissat DRAT + drat-trim on #85, #96, #926
     (normalised 24-204 s): proof size, check time, peak memory; extrapolate to 1117 maps (stratum C re-solved normalised).
   * Gate: <= 2 nights and <= 200 GB transient disk -> owner nights, proofs checked and deleted, hashes kept; above -> lead.
   * Lab: Opus, medium.
4. **S0 price probe** (only with approval 3, after item 1; exploit, jump 2; S0 unparked for one run).
   * The validated S0 embedding encoder with its units (FD4), asymmetric, 10 types with trivial automorphisms by a
     frozen seed, kissat, cap 4 h, <= 40 core-h, no proofs. Never run before with our encoder (`results.md:151`).
   * Follow-up: any type decided -> price the 59; the lead proposes a campaign and E-261101-09 (encoder comparison)
     first. SAT -> realizability stage (I-261029-57) and `candidate-check` before any word. All TIMEOUT -> S0 exact
     route > 4 h / type on the laptop; S0 stays parked. Lab: Opus, high (a SAT model on S0 needs care).
5. **Polar transfer of the vertex realizations** (N1; explore, jump 2; one session, seconds of compute).
   * Hougardy-Lutz-Zelke give small-integer realizations of 17 of the 20 (10, 3) maps (vertex version, CLAIMED,
     `literature/literature-review.md:151`). Polar planes of each; every affine chart (each feasible sign pattern of
     the hyperplane at infinity, exact LP) through `verify_candidate.py --target S6`. Control: cube -> octahedron.
   * Different from `literature/README.md:49` ("does not transfer by duality"): that is a general statement; no chart was tested.
   * Follow-up: PASS -> `candidate-check`, escalate; none -> park N1 with the count of charts tried. Coordinates not
     obtainable -> Szilassi's planes as points against the Csaszar torus instead. Lab: Sonnet, medium.

Deferred: E-261114-03 as designed, the (10, 3) long-cap night, I-261114-04, Stage B, thin wedges, I-261113-04, full 865.

## 2. Answers

* **Verdict.** The stance holds: exact formulas with the right normalisations priced A + B at 14.2 core-h against the
  485 projected plain (STATUS 3ad), one night as predicted. The targets do not: (10, 4) is exhausted without a candidate,
  (10, 3) resists normalised formulas at 1200 s (the 2026-11-14 hope that it falls inside the cap failed), nine faces
  are parked. Would change it: an (11, 5) median <= 20 min (S0 becomes priceable); a (10, 3) map decided; an item 5 hit.
* **Proposed `STRATEGY.md` §1 (not applied).** "First: S5 at (11, 5), census and cost probe; its price decides a sweep.
  S6 at (10, 3): one cube pilot, then parked if no map is decided. (10, 4): all 1117 admissible maps UNSAT-SOLVER; a
  proof replay only for a named claim. S0: one price probe of the asymmetric formulas when the 12-element price permits."
* **Lead 1, S5 A + B proof replay.** Not by default. It serves one claim only; approval 2 decides; item 3 prices it.
  Recommendation: (8, 2) + (9, 3) + (10, 4) is the strongest shareable focus result so far; it may be the
  "genuinely worthwhile result" that reopens the note. Your decision.
* **Lead 2, I-261114-03.** Item 1. The census is larger than the 2026-11-14 review implied (3986, not tens).
* **Lead 3, E-261114-03 speedup.** Do not reopen as designed: 10 s cubes against a baseline censored at 1200 s
  could not finish (audit 2). The lemma stands (PROVED-1); reuse it only inside item 4 if S0 needs cubes.
* **Lead 4, S6 full run NO-DAY-RUN.** Item 2, then park on failure.

## 3. Scores (T D F G R, J = jump, cost to the first result that could park it)

| Candidate | T D F G R | J | Cost to first kill | Note |
|---|---|---|---|---|
| Item 1, (11, 5) census + probe (I-261114-03) | 2 2 2 2 2 | 2 | 1 session + <= 10 core-h | prices S5 and S0 |
| Item 2, (10, 3) cubes + `--sat` (new) | 1 2 2 1 2 | 2 | 1 session + <= 8 core-h | failure parks S6 (10, 3) |
| Item 3, (10, 4) LRAT pricing (N2) | 1 2 2 1 2 | 0 | 1 session | D only if approval 2 |
| Item 4, S0 price probe (N4) | 2 2 2 2 2 | 2 | 1 day, <= 40 core-h | conditional on item 1 |
| Item 5, polar transfer (N1) | 1 2 2 1 2 | 2 | 1 session | explore |
| (10, 3) normalised long cap, 20 x 4 h | 1 1 1 1 2 | 2 | 1 night | below item 2 |
| I-261114-04 handle-neighbourhood SAT | 1 2 2 1 2 | 0 | 1 session | only if the owner keeps S6 |
| N3, symmetric (11, 5) slice | 1 1 2 1 2 | 2 | minutes | inside item 1's tree |
| E-261114-03 reopened with real cube caps | 2 1 2 2 2 | 0 | <= 3 core-h | only inside item 4 |
| E-261112-02 Stage B; I-261110-01 wedges | 2 1 1 1 2; 1 1 1 2 1 | 2 | 2 nights; 1-2 sessions | parked / deferred |
| I-261113-04 fixed-face C2; full 865; hitting-set | 1 1 1 1 2; 1 0 2 1 2; 1 1 2 1 2 | 0-2 | 1 session; 4 core-h; 1 session | below the gate |

Parked target only (S0): E-261101-09 encoder comparison (2 2 1 1 2) rises to first if item 4 decides a type; E-261101-15
cubes per type and E-261101-06 rank-3 SAT as filed. Other open ideas and hypotheses: scores as filed.

## 4. Queue (top items, in order)

1. **Item 1** (exploit). H: some (11, 5) formula is SAT. Test: 10 stratified maps at 3600 s. SAT -> result candidate;
   all UNSAT-SOLVER -> price; TIMEOUTs -> no sweep. Budget 1 session + 10 core-h. Stop: 10 maps recorded or a failed control.
2. **Item 2** (exploit). H: march_cu or a SAT configuration decides a (10, 3) map. Fail -> S6 (10, 3) parked. Stop: 8 core-h.
3. **Item 5** (explore). H: some chart of a polar HLZ realization is an S6 object. Stop: all charts of 17 objects.
4. **Item 3** (audit, approval 2). H: LRAT replay of 1117 maps fits two nights. Stop: three maps priced.
5. **Item 4** (exploit, approval 3). H: an asymmetric S0 formula is decided within 4 h. Stop: 10 types or 40 core-h.
6. **(11, 5) sweep** (follow-up of 1) only if priced <= 1 night; **N3** if not.

## 5. New ideas (untested proposals, not evidence)

* **N1. Polar transfer** (item 5). Why: polarity maps face planes to vertices, triple points to triangle planes,
  exactly; embeddedness differs, but with all charts the test is finite and exact. Cheapest test: item 5.
* **N2. LRAT instead of DRAT** (item 3; verified SAT proof checking). Why: the 2026-11-09 review found drat-trim on
  long solves beyond 48 GB; normalised solves are 10-45x shorter and LRAT checking is linear. Test: three maps.
* **N3. Symmetric (11, 5) slice.** The 24 admissible maps with Aut+ 2 or 3, symmetric formulas as in E-261113-01.
  Why: minutes; a symmetric S5 object would be a result. Test: 24 formulas, one shard-hour.
* **N4. S0 per-type price from the element curve** (item 4). Why: (10, 4) / (9, 3) mean time ratio is about 15 (68 s
  against 4.4 s); if it holds, S0 costs about 4 h per type and 59 types about 3 nights, less than an (11, 5) sweep of
  3986 maps (about 14 nights at the same factor). A scenario, not a bound; S0 lacks the doubled-pair encoding.
* **N5. Launcher heartbeat** (tooling). One line per minute per shard; removes the "no heartbeat, sleep not
  excluded" caveat repeated in every CONCLUSION since 2026-11-13.

## 6. Audit

1. **Missing synthesis.** `STATUS.md:404-411` (3ao) and 3ad never state that all 1117 admissible (10, 4) maps have
   solver answers; `ROADMAP.md:301` still cites only stratum C at 0.10 / 0.50 / 0.40; `STRATEGY.md:15` lists the done
   target as second. Fix in the applying session (wording only).
2. **Unpowered gate.** `experiments/E-261114-03-hull-vertex-chart-pilot/PLAN.md:31,48`: the lab added a 10 s
   small-pilot cube gate in front of the week plan's one-cube-per-vertex pilot (`ROADMAP.md` item 4, <= 3 core-h);
   0.06 core-h spent, verdict UNRESOLVED. Correctly not called a kill; a gate needs a cap that can pass.
3. **Lead's own error.** The 2026-11-14 review hoped the (10, 3) twenty may fall inside the cap (failed) and wrote that
   (11, 5) formulas "have the element count of S0" (`ideas/I-261114-03-*.md:18`): S0 has 13 elements, (11, 5) 12.
4. **Documentation against compute.** Week of 2026-11-14: 14.6 core-h, five items, one day; CONCLUSIONs within budget,
   but about a fifth of their lines are accounting caveats (outer CPU, heartbeat, caffeinate timing). N5 removes most.
5. **Working tree.** 753 untracked raw `results/run/0/map*/` directories of E-261110-06 (`git status`): move them with
   `move_raw.py` to `../polyhedrons-data` so later manifests are clean.
6. **Chains to stop.** Hull-vertex cubes as designed; segment-order cubes; plain long caps; any further (10, 4) solving
   other than a replay for a named claim; (10, 3) beyond item 2 without the owner.

## 7. Credences (all CONJECTURE, planning weights)

* (10, 4): **0.10 / 0.50 / 0.40 -> 0.03 / 0.87 / 0.10**: every admissible map UNSAT-SOLVER; the rest is solver, encoder
  and census soundness (PROVED-1, unreplayed). A checked replay would move "cannot tell" to about 0.
* (11, 5) S5 (new row): **0.03**: three rungs below negative, 3986 maps not run.
* (10, 3) S6: **0.25 -> 0.20** (as proposed 2026-11-14: symmetric formulas UNSAT-SOLVER, T family empty; no new datum).
* Nine faces, genus >= 4: **0.55** stays. S0: **A 0.20 -> 0.17, B 0.55 -> 0.60, C 0.25 -> 0.23**: every rung of the same
  formula family at 8, 9, 10 faces is OM-level UNSAT (two verified, one by solver); weak transfer, no S0 datum.

## 8. Three things to do first

1. Owner: approval 1 (week plan), and a yes / no on approval 2. 2. Lab (Opus, medium): item 1 prep, then the owner's
   day run. 3. Lab (Opus, medium): item 2 prep chained with item 5 (Sonnet, medium) in the same day run slot.
