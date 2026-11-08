# Strategy

Set by the owner on 2026-11-03; changed only by the owner, with a dated entry in the log at the end. `ROADMAP.md`
orders the work under this strategy; `STATUS.md` owns the numbers; `SPEC.md` owns the definitions.

## 1. Targets

* **Focus target: S5 at (9, 3)**, a maximal face-neighbourly polyhedron with 9 faces and genus 3: embedded, cubic,
  every two faces adjacent, exactly three adjacencies beyond the 36 pairs (V, E, F, chi = 26, 39, 9, -4). Success
  is only `verification/verify_candidate.py FILE --target S5` PASS, then `candidate-check`.
  * Why (9, 3): it is the first face count beyond the 2026 eight-face objects (Roest-Vigh, Mizhaev, both (8, 3)),
    the maximal case at a genus our engines already reach (genus 3 on 12 faces, 94 realizations), and symmetric
    realizations are allowed. The first ansatz, a free C3 action, is used up: its uniform formulas are UNSAT on all 8
    free-C3 maps (EXACT; geometric coverage conditional, PROVED-1; `STATUS.md` 3d-3i), so a (9, 3) object, if any, is
    asymmetric or has a symmetry of order 2; most undecided maps have spread-out doubled pairs
    (`reviews/strategy-review-2026-11-08.md` §3.1). If found and new, it is a result of the same kind as those two papers.
  * **Stretch: (10, 4)**, the first genus where every one of our engines has failed; it is where the "ravine"
    (below) must be crossed without a ladder. (8, 2) is a cheaper warm-up on the same methods, worth doing only
    if it costs less than a session or calibrates the (9, 3) method.
  * First step before any compute: the literature check (is any (8, 2), (9, 3) or (10, 4) polyhedron published?
    E-261101-22, E-261101-12).
* **Defining problem: S0 (Szilassi-12, (12, 6)), parked 2026-11-03, not abandoned.** Every S0 result stays as it is
  (FD rows, certificates, witnesses, the engine-score table, the 59-type data, all experiment folders). Work on S0
  resumes when the owner says so or when a focus result transfers (a method that passes R4, a structural fact
  about face-neighbourly maps). The S0 snapshot at parking time is `STATUS.md` as of 2026-11-03.

## 2. Stance: risky, jump-first

* **Compute is scarce** (one laptop, at most 10 cores, free GitHub Actions); ideas are cheap. Prefer methods that
  can succeed in one night over methods that need a campaign.
* **Jump, do not climb.** Evidence suggests a ravine between genus 3 and 4 for handle ladders at nearly fixed planes
  (H-261101-10; the Gauss gate on 21 of 21 type-0 arms; night 7: no engine passes R4). Methods that reach the target
  genus directly get priority: symmetric ansatzes with few parameters (legal for S5), arrangement first (E-261101-16),
  embedded first, planar later (I-261103-01), chirotope-first on small instances.
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
