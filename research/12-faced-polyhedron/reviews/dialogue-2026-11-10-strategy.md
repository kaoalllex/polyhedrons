# Dialogue 2026-11-10-strategy: revised strategy proposal

Status: approved by the owner in C3 (#29, 2026-11-12). Drafted by claude; astra's amendments of #16, #21 and #26
(its review of the full text) are folded in. Nothing here is evidence: both authors are AI sessions (`SPEC.md` §5).
Labels are `SPEC.md` §5; every number is a session check of the thread unless a repository file is cited. The
thread directory `dialogue/threads/` is not in git. Nothing is filed or launched.

## 1. Owner digest

1. **Verdict.** The 2026-11-10 strategy is right about the laptop and about construction first, and wrong in two
   places: it tests families by a few hundred random arrangements, which have about 12 % detection probability
   at the measured Gaussian seven-plane rate, and it has no exact, finite search space for its main constructive target.
2. **Filter (owner, #7).** A target must be at least as significant as the Mizhaev / Roest-Vigh objects.
3. **Route 1: nine mutually adjacent faces by exact ninth-plane cells.** Add one plane to the eight planes of a
   known object; its positions form a finite list (47,802 cells for Roest-Vigh, 47,212 for Mizhaev, EXACT counts).
   Stage A, the 2,004 symmetry classes next to an existing plane, costs about 7.3 core-h (a day run); 251 of them
   (12.5 %) were decided in a session check, all infeasible, without a checked proof. The full census is forecast
   at about 86 core-h including A, the remaining Stage B at about 79 before overhead (classes of size 4 assumed,
   not measured): Roest-Vigh first; real orbit counts and a measured cost gate each night of at most 80 core-h.
4. **Route 2: S6 at (10, 3)** by the planned 20-map night, kept by the owner (#14), behind a bridge gate.
5. **Route 3: thin wedges**, an exploratory backup for ten faces; both 8-face objects pass a float pre-check (K3); the exact gate is pending.
6. **In hand:** an exact S6 (10,2) polyhedron, registered locally as a witness; literature novelty not checked; by
   the filter it is a control, not a headline.
7. **Demoted at this budget, not refuted:** fewer-faces descent from the genus-3 archive; the cyclic arrangement.
   Dropped by the filter: (11, 3) as a target.
8. **S0** stays parked. The owner's hairy-ball idea was tried (K10-K12): no independent Hopf-half constraint
   survives and no new run is justified. The index sum around a line is Euler plus one planar fact per face
   (claude); the other half cancels edge by edge (astra, #21). By-product: a derivation of F7 without Hopf.
9. **Needs approval:** the `STRATEGY.md` text of §6; Stage A as a day run and Stage B as the first night, each
   after its ROADMAP row and `PLAN.md`.
10. **Not done:** no human review, no literature check, no DRAT; no independent rerun of claude's checks.

## 2. Shortlist (ranked; T D F G R as in `ROADMAP.md`)

| # | Idea | Target | Cheapest test | Cost | Kill rule | T D F G R | Proposed / objection |
|---|---|---|---|---|---|---|---|
| 1 | NEW, extends I-261103-04, I-261110-03: ninth-plane cells, Stage A (near-copy cells, both sources) | S1, nine faces, genus free | "edge runs >= 39" on 2,004 certified orbits; controls: recovery at eight planes, and reinsertion of a deleted plane through the same representative-to-solver path | 7.3 core-h, 10 shards, day run | a control fails, or the list count differs from the Zaslavsky count | 2 2 2 1 2 | astra (cells), claude (list, certificate, pricing). astra: verdicts are UNSAT-SOLVER, never a family negative; scope is the generic open cells of two fixed sources |
| 2 | NEW: Stage B, all cells | same | rank-4 enumerator, K1's count, real orbit sizes, 50 timed cells | 1 session, then one night per source (Roest-Vigh first; unfinished orbits carry over by manifest) | count mismatch; a measured cost above one night per source needs an explicit budget decision of the owner | 2 2 1 1 2 | astra, claude. astra: 86 core-h is A + B for both sources, B alone about 79, no margin for one night; earned by a certified list and a measured cost, not by a Stage A miss |
| 3 | E-261110-02 behind a gate (I-261110-02) | S6 (10, 3) | the (10,2) witness map SAT with `submap=True`; the SAT-to-coordinates bridge returns an object from a foreign model | prep session + one night | bridge fails its control: no construction night | 2 2 2 2 2 | plan of 2026-11-10; owner keeps it (#14). astra: state two payoffs, 20 checked UNSATs are a conditional exclusion, a SAT without coordinates leaves realization open |
| 4 | I-261110-01 as a symbolic degeneration | S1 ten faces; S5 (10, 4) | exact replay of K3 on a small-parameter interval; exact count of leading-sign cells | 1 session | replay fails, or enumeration plus measured decisions exceed one night | 1 2 2 2 2 | astra (wild idea), claude (K3). astra: an exploratory backup, not an established finite ansatz |
| 5 | E-261110-05 unchanged (week item 5) | mechanism of the (8,2) / (9,3) UNSATs | V2 on the two (8,2) maps | <= 3 core-h | its registered hash and control gates and the V1 / V2 follow-up tree, unchanged | 2 2 2 2 2 | astra keeps it ahead of any census; claude: no local core on <= 7 faces (STATUS 3d) |
| 6 | E-261110-06 unchanged | S5 (10, 4) | cube-and-conquer pilot (week item 4) | by its rule | by its rule | 1 2 2 1 2 | plan of 2026-11-10 |

## 3. Drop or demote

* E-261110-03 isotropic arms and E-261110-04 (random family scoring, then a sweep): replaced by rows 1-2. At the
  only rung with a known tight answer the Gaussian hit rate is 6.4e-4 (C6), so 200 draws detect with probability
  1 - (1 - p)^N = 12 %. The rate is not transferable to structured families (D2 at 8 planes, STATUS 3g).
* "LOW-YIELD" readings of E-261107-01 (30 draws) and E-261108-01 (300 draws): keep the numbers, drop the inference.
* Demoted at this budget: single-adjacency descent in the number of faces from the genus-3 archive (1 admissible
  edge of 192, K6; that edge is untested); the cyclic arrangement (0 of 13,320, C6, a sample); the Szilassi chamber
  census as a census (astra: SAT models are not chambers); a native sampling night for (10, 3). Dropped by the
  owner's filter: (11, 3) as a target.
* Pencil identities (owner's #8; FD7, I-261101-13), no run earned: for a generic line L,
  `G+(L) = G-(L) = (chi - #(L cap S)) / 2`. The sum is Euler plus a planar ray-count lemma per face (claude, #17);
  the difference vanishes for every closed oriented dual map with a rank-two contraction (astra, #21). Both
  PROVED-1, checked on two objects (K10-K12), written out in `theory/theory-notes.md`, addendum 2026-11-12. Whether
  the planar lemma follows from the implemented F1-F7 clauses is a separate encoder question (astra).

## 4. Disagreements

* **Crease lemma.** claude: confirmed on 108 exact instances; astra: reported checks, not a verified universal
  lemma, five "outside" chords unexplained. Decider: a written proof and the five cases.

## 5. Computed in this thread (claude, `work/claude/`; session checks, not results) and not checked

| Check | Numbers | Label |
|---|---|---|
| C1 `s6_native.py` | one 36-pair solid in 45 capped solves on 10 Gaussian planes: the S6 (10,2) witness, verified by two checkers | EXACT object |
| C3 `s6_hard.py` | ">= 42 pairs" on 10 planes: 251 of 251 INFEASIBLE, median 13 s; the ">= 36" control TIMEOUT at 60 s | NUMERICAL |
| C6 `szilassi_rate.py` | Szilassi in 8 of 12,540 Gaussian 7-plane draws; cyclic arrangement 0 of 13,320 | NUMERICAL |
| K1, K2 `cells9.py` | ninth-plane cells 47,802 / 47,212; near-copy cells 510 per plane (504-508 Mizhaev) | EXACT |
| K3 `cells9.py` | both 8-face chirotopes unchanged when the four wedge pairs close to t = 1e-7 | NUMERICAL |
| K5 `crease_exact.py` | 108 of 108 creases of the (10,2) witness EMBEDDED, planted merges 108 of 108 | EXACT |
| K6 `merge_lucky.py` | 1 of 192 archive edges has two common neighbours (geometric part not run) | EXACT |
| K8, K9 `cells_exact.py`, `stage_a_*.py` | near-copy union 4,024 / 3,992, orbits 1,006 / 998; recovery at eight planes passes; 251 of 251 orbits INFEASIBLE at ">= 39", 13.1 s each | EXACT lists, UNSAT-SOLVER verdicts |
| K10 `pencil_identity.py` | 300 exact lines each on Szilassi and the (10,2) witness: planar lemma and `sum j + #(L cap S) = chi`, 0 failures; scrambled-face control fails as it should | EXACT check of a PROVED-1 statement |
| K11 `pencil_gauss.py` | 500 exact lines each: `G+ = G- = (chi - #(L cap S)) / 2`, 0 failures, 0 pointwise mismatches with the Banchoff index | EXACT check of a PROVED-1 statement |
| K12 `half_cancellation.py` | astra's cancellation: determinant identity exact on every corner of 300 lines per object; `#(+++) - #(---) = 0` for 2,984 / 2,970 random rank-two vector sets on the two dual maps; antisymmetric signs from no rank-two set violate it in 1,718 / 1,992 trials | EXACT check of a PROVED-1 statement |
| C2, C4, K4, K7 | 125 + 236 INFEASIBLE at E = 45; C4 70 of 70 TIMEOUT; K7 two cells | scoped, no information beyond it |

Not checked: literature novelty of S6 (10,2) and of nine mutually adjacent faces; the combinatorial bounds 7, 10,
10, 11, 12, 12 (memory); the pencil identities on the own axes `A cap B` (degenerate; no one-sided form derived);
F7 without Hopf: written as an addendum of 2026-11-12 in `theory/theory-notes.md` (PROVED-1, claude, not
reviewed by astra, realizations only; the planar lemma is not compared with the implemented F6 clauses); the
reinsertion control of row 1 (no OR-Tools environment in the session of 2026-11-12); the symmetry of Stage B cells; any INFEASIBLE verdict by a proof checker; K3 in exact
arithmetic; whether astra reproduces any of the above.

## 6. Proposed `STRATEGY.md` changes (not applied; the owner changes that file)

Replace the "Focus" bullet of §1 by:

```
* **Focus (owner, 2026-11-12): one constructive target at a time, each at least as significant as the 2026
  eight-face objects (owner's filter).**
  * **First: nine mutually adjacent faces, genus free (S1)**, searched as an exact finite family: one plane added
    to the eight planes of Roest-Vigh or Mizhaev, one decision per chirotope cell of the new plane, the cell list
    certified by its count. Stage A (near-copy cells), then Stage B (all cells, one source per night). Success is
    only `verify_candidate.py FILE --all-pairs` PASS with nine faces, then `candidate-check`. A run without
    checked proofs yields no family negative.
  * **Second (kept by the owner, 2026-11-12): S6 at (10, 3)** by E-261110-02, gated by the (10,2) witness as the
    control of the formula and of the model-to-coordinates bridge.
  * **S5 at (10, 4)** only under the rule of E-261110-06.
```

Add to §2:

```
* **Prefer enumeration to sampling** when a certified list of cells and its decisions fit the budget. The list
  carries distinct exact rational representatives and an independently justified count.
* **State the power of a sample.** A sampling result names its unit, a hit rate p measured on a rung with a known
  answer in the same family, and the detection probability 1 - (1 - p)^N; without them it is not "low yield".
* **Two controls for a solver result, reported separately**: planted recovery and discovery power. A missing or
  failed correctness control blocks conclusions about the target; an unresolved time-capped solve is
  "solver-limited"; passing recovery alone does not establish discovery power.
```

Log entry: "2026-11-12 (owner's decisions #2, #7, #14 in the dialogue of 2026-11-10 and its synthesis): significance
filter; first target nine mutually adjacent faces by ninth-plane cells; (10, 3) second; three standing rules added;
S0 parking and the side track unchanged."
