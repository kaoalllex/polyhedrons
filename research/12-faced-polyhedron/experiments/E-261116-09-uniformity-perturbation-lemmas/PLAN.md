# E-261116-09: uniformity and perturbation lemmas, and the common obstruction of the stage-B formulas

Pre-registration (`PROTOCOL.md` §8b). Week item 4 (lead review 2026-11-19); owner addition of 2026-11-22 (part B).

* **ROADMAP row / scores**: T 2 D 1 F 2 G 2 R 2 (T + D = 3). Audit; one session.
* **Question**: which scope words of the small-case and symmetric-slice results can be removed by a written lemma, and
  is there one small clause-family set that makes every stage-B symmetric nine-face formula of E-261119-02 UNSAT?
* **Hypotheses moved**: H-261101-07 only through scope: a lemma widens or narrows what an UNSAT-SOLVER slice covers.
* **H1 / H0**: A: each lemma below holds as stated (H0: a counterexample, which keeps its scope word). B: one family
  set of size <= 4 is UNSAT-SOLVER on all 69 priced records (H0: the minimal sets differ by stratum or family).

## Part A: lemmas (proofs; at most PROVED-1; exact checks only; no solver; runs while E-261119-02 holds the cores)

Output `LEMMAS.md`, one section per lemma: statement, scope sentence (target, map class, group, chart, genus, what
it does not cover), proof, label. Input: Codex review §4 (`reviews/strategy-review-2026-11-19-codex.md`): the
stabiliser test runs over every group element, powers included; it is not a full dependency test, so a uniformity
claim for a group also needs a nonzero integer witness on its equivariant parameter space.
* **L1 uniformity (I-261116-07)**: a cubic embedded object (S1/S5, planar simple faces, strict corners) has a small
  perturbation with a uniform chirotope (INF included) and the same map; the uniform plain formulas lose no cubic object.
* **L2 equivariant uniformity**: for C3 3+3+3 (standard chart) and C2 4 x 2 + 1 (moved chart) at nine faces and free
  C2 at eight (standard chart): no forced zero for any element, and an integer witness with every minor nonzero, so a
  generic equivariant perturbation is uniform; combined with L1's openness, the slice formulas lose no such solid.
* **L3 I-261118-02**: fixed faces keep their covector; a rotation fixes at most one face; prime order >= 5 forces a
  zero; the list of uniform families at nine faces (C3 3+3+3, C2 4 x 2 + 1), mirror families excluded.
* **L4 owner 5**: an eight-face S1 solid whose symmetry group contains a half-turn carries a free half-turn; a group
  with no half-turn is a mirror or C7 case outside every uniform symmetric formula. Scope of E-261119-01's (8, 3) slice.
* **L5 lead 4**: on the (11, 5) maps with Aut+ in {1, 2, 3} every improper symmetry is a mirror (forced zero), so
  no uniform formula keeps an improper symmetry; it says nothing on solids with a mirror under a smaller formula.
* **L6 I-261108-09, universal local check, k = 4**: for the generic central arrangement of 4 planes, every union of
  cones whose boundary is a manifold 4-valent vertex with all 4 planes as face sectors, and both perturbation signs,
  some choice of the bounded cell gives a valid patch (far trace kept, each face a disk sector, cubic manifold
  vertices, a disk patch, outgoing edges kept). Exact enumeration in `checks.py`. k = 5, 6 and non-generic central
  stars only if time remains; otherwise recorded as not run, and the (8, 2) / (9, 3) note keeps "cubic".
* Controls (part A): `checks.py` must reproduce the Codex witness minima (C3: 8, C2: 44); L6's check must accept the
  convex 4-valent vertex (true by convexity) and reject a planted bad patch (the bounded cell chosen by a wrong rule).

## Part B: family-ablation diagnostic (owner addition; a stated deviation from "no compute": seconds to minutes)

Not started while `bash overnight/launch.sh 261119-02 status` shows the launch active; E-261119-02's `results/`,
`maps/` and `run.sh` are read only.
* **Formula**: for each record of `maps/pricing.json` (33, (9, 4)) and `maps/pricing_9_5.json` (36, (9, 5)), the
  formula built exactly by `tranche.submap_formula` (E-261103-03), with each clause tagged by family while it is built:
  GP, SEGMENT_DISJOINT, TRIPLE, INCONS, RFCONS, REFLEX1, POC, SYM, SB_ORBFLIP, SB_MIRROR (any other tag found is a family
  too); Tseitin definitions are always kept (conservative). Identity check: the untagged formula's `formula_sha256`
  equals the stage-B record's (`results/stageB-pricing`, `results/stageB5-pricing_9_5` or lean) for every record.
* **Ablation**: (1) drop one family, every record; (2) every subset of size <= 4, by size, skipping supersets of a
  found UNSAT set, every record; (3) one greedy deletion-minimal set from the full set per record (fixed family order).
  Solver `n2.sat` (cadical195, the controls_b path), cap 10 s per formula; a timeout is UNKNOWN, never pruned on.
  Monotone: a subset of a SAT set is SAT, a superset of an UNSAT set is UNSAT (added clauses only).
* **Controls (same code path, filtered formulas)**: per record, 5 symmetric generic plane draws pinned under {GP, SYM,
  SB_ORBFLIP, SB_MIRROR} SAT, 5 wrong-action draws UNSAT (`controls_b.draw`, `wrong`, `gauge`, `pin`); the three SAT
  (8, 3) rung records (`maps/rung_8_3.json`) SAT with all families and their models re-checked by the ablation filter;
  comparison arm: the 32 (9, 3) rung records (plain formulas UNSAT-VERIFIED, STATUS 3d) under the same ablation.
* **Shards / budget**: 10 worker processes over records, one session run after the launch ends; hard cap 2 core-h
  (expected < 0.3). Output `results/ablation/` (manifest: commit, dirty, host, python, wall, core-s; one JSON line per
  record). Code `ablate.py`. Proofs: none (owner rule; a family-ablation UNSAT is UNSAT-SOLVER, never a negative result).
* **Predictions**: P1 (~60 %): every record is UNSAT with {GP, SYM, gauge} plus one map family. P2 (~40 %): the C3 and
  C2 records share no common minimal set. P3 (~70 %): the (9, 3) comparison arm shows the same minimal sets.
* **Reading**: one set S common to all 69 records -> state and attempt a lemma (at most PROVED-1) with its exact scope
  (which formula, action, chart, genus); a proof covering every C2 4 x 2 + 1 (9, 5) map goes to "For the lead" with
  the evidence for or against stopping the remaining 90 % of pass 1 (this session does not decide it). No common set ->
  per-stratum sets recorded; the lead reads them. A failed control -> stop part B, report, no reading.

## Outcomes, stop rule, ledger

* A lemma proved -> PROVED-1 (an AI author), `STATUS.md` one line each, `paper/OUTLINE.md` items only by the lead.
  A gap -> the lemma is recorded as a sketch with the gap named; a counterexample keeps the scope word.
* Part B outcomes are UNSAT-SOLVER / SAT / UNKNOWN per filtered formula; no scope beyond those exact formulas.
* Scenario move: none for A / B / C (scope only); a lemma that covers all (9, 5) maps moves no credence by itself.
* Stop: both parts recorded, a failed control, or the 2 core-h cap. Ledger: README, `STATUS.md` (one line per lemma
  and the diagnostic), log, handover.

## Amendments
