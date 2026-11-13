# Strategy

Set by the owner on 2026-11-03; changed only by the owner, with a dated entry in the log at the end. `ROADMAP.md`
orders the work under this strategy; `STATUS.md` owns the numbers; `SPEC.md` owns the definitions.

## 1. Targets

* **Focus (owner, 2026-11-12): one constructive target at a time, each at least as significant as the 2026
  eight-face objects (owner's filter).**
  * **First (owner, 2026-11-13): S6 at (10, 3)**, symmetric realizations first (E-261113-01), the asymmetric maps
    only with a changed solver set-up; gated by the (10,2) witness as the control of the formula and of the
    model-to-coordinates bridge. Success is only `verification/verify_candidate.py FILE --target S6` PASS at
    (10, 3), then `candidate-check`.
  * **Second: nine mutually adjacent faces, genus free (S1)**, searched as an exact finite family: one plane added
    to the eight planes of Roest-Vigh or Mizhaev, one decision per chirotope cell of the new plane, the cell list
    certified by its count. Stage A (near-copy cells, done), then Stage B (all cells, one source per night), gated
    by the same enumeration one rung below (E-261113-03). Success is only `verify_candidate.py FILE --all-pairs`
    PASS with nine faces, then `candidate-check`. A run without checked proofs yields no family negative.
  * **S5 at (10, 4)** only under the rule of E-261110-06. Success is only
    `verification/verify_candidate.py FILE --target S5` PASS at (10, 4), then `candidate-check`.
  * S1 and S6 objects are never reported as S0 or S5. Symmetric realizations are allowed (FD5 covers the
    59 single-adjacency (12, 6) maps only).
* **Side track: the (8, 2) / (9, 3) negative result.** Consolidated at low compute (multiplicity >= 3 control, second
  census, second encoder on six maps: all passed, 2026-11-09). **The note is deferred** (owner, 2026-11-09): no session
  time on it unless a genuinely worthwhile result is found; if written, it says plainly that no independent (human)
  review took place (owner, 2026-11-08).
* **Compute: the owner's laptop only** (owner, 2026-11-10): at most 10 cores, 8-10 shards per splittable run, nights
  under `caffeinate`; no rented compute, no GitHub Actions.
* **Defining problem: S0 (Szilassi-12, (12, 6)), parked 2026-11-03, not abandoned.** Every S0 result stays as it is
  (FD rows, certificates, witnesses, the engine-score table, the 59-type data, all experiment folders). Work on S0
  resumes when the owner says so or when a focus result transfers (a method that passes R4, a structural fact
  about face-neighbourly maps). The S0 snapshot at parking time is `STATUS.md` as of 2026-11-03.

## 2. Stance: risky, jump-first

* **Compute is scarce** (one laptop, at most 10 cores); ideas are cheap. Prefer methods that
  can succeed in one night over methods that need a campaign.
* **Jump, do not climb.** Evidence suggests a ravine between genus 3 and 4 for handle ladders at nearly fixed planes
  (H-261101-10; the Gauss gate on 21 of 21 type-0 arms; night 7: no engine passes R4). Methods that reach the target
  genus directly get priority: symmetric ansatzes with few parameters (legal for S5), arrangement first (E-261101-16),
  embedded first, planar later (I-261103-01), chirotope-first on small instances.
* **Score the sampler first.** An arrangement family is scored on a rung with known answers (8 planes) before it is
  used on a target, and its report includes the wedge covariate.
* **Prefer enumeration to sampling** when a certified list of cells and its decisions fit the budget. The list
  carries distinct exact rational representatives and an independently justified count.
* **State the power of a sample.** A sampling result names its unit, a hit rate p measured on a rung with a known
  answer in the same family, and the detection probability 1 - (1 - p)^N; without them it is not "low yield".
* **Two controls for a solver result, reported separately**: planted recovery and discovery power. A missing or
  failed correctness control blocks conclusions about the target; an unresolved time-capped solve is
  "solver-limited"; passing recovery alone does not establish discovery power.
* **Score a finite family one rung below.** Before a target run the enumerator runs where an object is known and
  must find it unaided.
* **A pilot can stop a night.** If every pilot unit ends by the cap, the night needs a changed set-up or the
  owner's word.
* **Risky ideas are welcome and killed fast.** Every new engine gets a one-session pilot on the benchmark ladder
  (R1 Szilassi, then a rung with a known answer at the target's size) with a stated kill criterion; a pass earns a
  night, a fail parks the idea with its failure mode written down.
* **Exploration share: one run in two**, not one in four (PROTOCOL 8a), while the focus target has no result.
* **Follow-up rule.** A follow-up of a finished experiment enters the queue only if its outcome changes a decision
  in the scenario table or the focus plan; "the engine was cut by a cap" alone is not enough.
* **The exact side continues at low cost** where it is cheap and reusable for both targets (certificates,
  rank-3 relaxations, the final-polynomial pipeline), never at the cost of a focus night.

## 3. Process

* Hard rules are unchanged (`CLAUDE.md`, `PROTOCOL.md`): pre-registration, exact verification, scoped claims,
  labels, no fabricated results.
* **Weekly lead review** (owner, 2026-11-07): the lead (strongest model) reviews the week's work about once a
  week and writes the week plan; lab sessions execute it with light documentation (`PROTOCOL.md` §8b). The review
  is skipped while no new work exists, and is called early after any result that moves a scenario by 0.1 or more:
  `.claude/skills/strategy-review` in a separate session with the strongest model at high effort; it writes
  `reviews/strategy-review-YYYY-MM-DD.md` and a proposed `ROADMAP.md` order, and changes nothing else without the
  owner's approval.

## Log

* 2026-11-03: created. Focus S5 (9, 3), stretch (10, 4); S0 parked; risky, jump-first stance; exploration one in
  two; follow-up rule; regular strategy reviews. First review under this strategy:
  `reviews/REVIEW_PROMPT_2026-11-03.md`.
* 2026-11-07: owner's process change: weekly lead review with a week plan; lab sessions light and cheap; review
  cadence by elapsed work, not calendar (`PROTOCOL.md` §8b).
* 2026-11-08 (owner's request, lead review M2): §1 no longer names the free C3 ansatz as the natural first ansatz;
  all 8 uniform free-C3 formulas are UNSAT. Targets and stance unchanged.
* 2026-11-08 (owner's decision on lead review 2026-11-08d): focus moves to S5 at (10, 4), gated by a speed-up
  benchmark; the (8, 2) / (9, 3) negative result becomes a side track towards a note marked as not independently
  reviewed; GitHub Actions approved for a trial. Stance and S0 parking unchanged.
* 2026-11-09 (owner's decisions on lead review 2026-11-09): the gate is decided (kissat, P(4) = 475 core-h, route =
  stratified first-witness sweep, stratum C first); the note is deferred unless a worthwhile result is found; the lab
  checks GitHub's Actions terms before any job. Targets, stance and S0 parking unchanged.
* 2026-11-10 (owner's decisions on the handoff of the 2026-11-10 strategy session,
  `reviews/strategy-review-2026-11-10.md`): compute is laptop-only, no rented compute, no Actions; the (10, 4) route
  is demoted to the rule of E-261110-06; three constructive targets (S6 at (10, 3); S1 with the genus free at 9, 10
  and 12 faces) adopted for one week of tests; the wedge ansatz is an explore item gated by E-261110-03. The side
  track and S0 parking are unchanged.
* 2026-11-12 (owner's decisions #2, #7, #14 and approval #29 in the dialogue of 2026-11-10,
  `reviews/dialogue-2026-11-10-strategy.md`; filed at the owner's request): significance filter; first target nine
  mutually adjacent faces by ninth-plane cells; (10, 3) second; three standing rules added; S0 parking and the
  side track unchanged.
* 2026-11-13 (owner's decisions on lead review `reviews/strategy-review-2026-11-13.md`): S6 at (10, 3) becomes the
  first target, symmetric realizations first; nine faces second, Stage B gated by a census one rung below; two
  standing rules added (rung-below scoring, pilot gate). No proofs in the symmetric runs. S0 parking, the side
  track and the stance are unchanged.
