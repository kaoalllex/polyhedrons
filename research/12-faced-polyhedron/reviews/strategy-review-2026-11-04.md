# Strategy review, 2026-11-04

Evidence cut: `dfbc81ffb3527e6d32288b3399720d65af1a3209`, on
`experiment/E-261103-03-s5-exact-decision-8-2-9-3`. This is the requested separate strategy-review
session. No dated November 4 prompt exists; the owner's current questions define the scope. The
November 3 review is historical evidence, not a reused instruction prompt. Only this report changes.
Queue entries and scores below are recommendations requiring owner approval and subsequent
pre-registration; they do not authorize computation or change the ledger.

Scientific evidence labels are those of SPEC section 5: EXACT for the reproduced computations,
PROVED-1 for unreviewed arguments, NUMERICAL for floating observations, CLAIMED for unreproduced
external statements. Recommendations and subjective credences are explicitly judgments, not new
evidence labels. This AI review provides no independent human mathematical review.

## 1. Verdict in ten lines

1. **Recommendation:** keep S5 (9,3) as the focus, (10,4) as stretch, and S0 parked.
2. **EXACT:** both plain (8,2) formulas are UNSAT-VERIFIED; their free-C2 refutations are redundant for plain-map exclusion.
3. **PROVED-1, conditional:** the geometric (8,2) exclusion still depends on census coverage, necessary encoding clauses and general-position reduction.
4. **EXACT:** no (9,3) target formula was solved through the evidence cut; neither existence nor nonexistence has new direct evidence there.
5. **Recommendation:** retire (8,2) as a positive construction benchmark; retain it as a proof-pipeline negative control.
6. **Judgment:** the seconds-scale plain decisions justify measuring (9,3) now; they do not establish a one-night decision bound for 203 maps.
7. **Recommendation:** first run a bounded paired C3/plain pilot, including plain maps outside the C3 subset, under an amended E-261103-03 PLAN.
8. **Recommendation:** retain one explore run in two, with solid-first controls next; do not buy another S0 ladder or cap-extension campaign.
9. **Audit:** fix model-versus-map, abstract-versus-geometric symmetry, and timeout-versus-decision wording before the next run.
10. **Budget recommendation:** one preparation session and at most 1 core-hour for the first pilot; no automatic night or full census sweep.

## 2. Evidence delta and its meaning

The review used STRATEGY, STATUS, ROADMAP, SPEC, PROTOCOL sections 2 and 8a, the last two night
reports (November 2 and 3), the previous strategy reviews, experiment-log, and the conclusions of
E-261103-01, -02 and the partial -03. These are the new experiment conclusions since the November 3
review. The full graph inventory and the source files of its open candidates inform section 6.
Targeted code inspection covered formula construction, pairing, symmetry normalization and saved
evidence replay. No new literature search or novelty claim is part of this evidence-cut review.

| New evidence | Level and scope | What changes |
|---|---|---|
| E-261103-01: 2 admissible (8,2) maps; 240 (9,3) maps, 203 admissible; 1183 (10,4) maps, 1117 admissible | EXACT enumeration outputs and controls; completeness PROVED-1 | Inputs are finite and available. Repeating the census is unnecessary. Counts alone do not establish realizability. |
| Separate C3 exact cover agrees on eight admissible (9,3) maps; K7 and all 59 K12 canonical classes agree | EXACT computations; coverage PROVED-1 | Stronger census validation than sample saturation. Different enumeration algorithms still share canonicalization/checking machinery. |
| E-261103-02: 3000 accepted exact perturbation comparisons, no predicate mismatches; own pinned models, negatives and S0 circuit hashes pass | EXACT bounded controls; encoding arguments PROVED-1 | Multiple adjacencies are supported and calibrated. This is neither exhaustive semantic validation nor an external second encoder. |
| E-261103-03: plain maps 0 and 1 refuted in 5.261121 and 12.393358 solver seconds; CNF/DRAT retained and checked | EXACT, two formulas | A real small-case decision replaces the old heuristic plateau. Two easy instances are no runtime distribution for (9,3). |
| Eight supplied-chirotope recoveries pass exact signs, embedding and the separate all-pairs recheck | EXACT, S1 (8,3) controls | Both realizer paths work on these known inputs, with warm and unseeded recovery distinguished. Arbitrary target SAT models remain untested. |

Recorded pilot plus separate control recheck totals 0.010037820301 core-hours. Regression and
development checks are outside that total, as the conclusion states. No (9,3) solve, target model,
target realization or target final polynomial exists in this delta. The full experiment remains
`running` as a ledger state, with no active process.

The change is methodological: a negative answer can now be obtained and replayed cheaply at nine
OM elements. It is not a genus monotonicity theorem. Deleting a face from a hypothetical (9,3)
surface does not yield a closed maximal (8,2) surface. The failure of that warm-up therefore does
not kill the focus or the use of genus-2 parents with fewer adjacencies. Conversely, successful
12-face genus-3 parents do not establish nine-face construction power. Night 7 tested R4 at genus 3
from random starts and R5 from parents; it did not test a general genus-3-to-4 obstruction.

## 3. Census and encoding claim boundary

### 3.1 The chain that is actually available

1. **Census family:** loopless oriented triangular dual maps with complete underlying graph,
   explicit parallel darts, and the required Euler characteristic; mirrors identified. The saved
   counts, map checks, K7/K12 agreement, sampled-code containment and fresh (9,3) replay are EXACT.
   The argument that augmentation, root normalization and triangle completion cover every map is
   PROVED-1, not a human-reviewed enumeration theorem.
2. **Geometric admissibility:** distinct corner triples are necessary under the project's
   nondegeneracy conditions; admissibility is not sufficiency. All 37 rejected (9,3) maps are
   rejected before geometry in the regression. Dart codes are authoritative: a neighbor word may
   lose pairing information on an inadmissible map. For admissible inputs the endpoint-corner
   pairing is checked, rather than guessed. Interpretation of this filter remains PROVED-1.
3. **Uniform reduction:** for a negative geometric conclusion, every allowed embedding must yield
   a uniform encoding after an allowed perturbation. For multiple shared segments this must preserve
   all prescribed corners, simple faces, disjoint segment gaps, embedded vertex stars and absent
   extra intersections. The original openness discussion is for S0; the S5 extension should be
   written explicitly with these hypotheses. The current conclusion is appropriately conditional.
4. **Necessary formula:** every such embedding must satisfy every enabled clause family, including
   GP, segment disjointness, IN consistency, reflex constraints, orientation consistency and gauge
   normalization. For UNSAT exclusion the essential direction is embedding implies SAT; proving
   the converse does not substitute for it. E-261103-02's SOUNDNESS note is PROVED-1. Its exact
   positive and defective samples test implementation, not every possible realization.
5. **Exact refutation:** rebuilt plain formulas match the saved hashes and the retained DRAT
   refutations check. This is the EXACT part of the (8,2) result. The proof checker validates the
   DIMACS contradiction, not map coverage or geometry. No CERTIFIED geometric theorem is added.

These distinctions survive another AI review. A public theorem still needs the external
implementation/human checks required by PROTOCOL section 3. This need not block a small exploratory
(9,3) pilot with conditional claims; it does block unconditional publication language.

### 3.2 Symmetry is a restriction, not map coverage

EXACT census data: the eight free-C3 maps and the 24 maps with an involution overlap in two maps;
their union has **30**, not 32, members. The remaining 173 admissible maps have trivial Aut+.
The two overlapping maps may be run with C3 clauses without imposing their full D3 group.

The free-C3 positive controls establish uniform **plane arrangements** obeying the symmetry-only
formula. They do not embed any of the eight target maps. A C3 UNSAT excludes its precise uniform
cooriented ansatz. Turning all eight such UNSATs into a geometric C3 exclusion additionally needs
coverage of the relevant actions, coorientations, normalization and symmetry-preserving generic
perturbation. Free-C3 generic controls are evidence for that route, not the whole proof.

Fixed-face C2 and D3 are different: the known odd-permutation invariant quadruples force zero
determinants (PROVED-1 argument, EXACT formula controls). Their uniform symmetry-only UNSATs are
not geometric exclusions. Use plain formulas on these maps; reserve a nonuniform extension for a
separately justified experiment. Plain formulas also allow asymmetric realizations of maps with
automorphisms. A C3-only negative never removes that map from the plain coverage ledger.

A SAT model with invariant signs need not be realized by coordinates carrying an order-three
Euclidean rotation. **PROVED-1 reasoning:** sign constraints are inequalities; the rotation
requires additional equalities on the coordinates. Realizing the former does not check the latter.
An S5 PASS with F=9 and g=3 suffices for the focus result regardless of symmetry, but H-261103-02 additionally needs
an explicit rotation and exact plane/face correspondence, or an independently justified symmetry
realization argument. Symmetric arrangements with asymmetric selected solids require the same care.

### 3.3 A model is not a map

Maintain separate outcomes for each formula and each model. A checked final polynomial excludes
one chirotope only. A map becomes geometrically excluded only by a plain UNSAT with the necessary
interpretation, or by exhaustive sound model exclusion followed by a checked residual UNSAT and
coverage of the exclusions. Heuristic no-goods cannot enter that certificate chain. A timeout,
unrealized model, LP timeout, or one exact nonrealizable model leaves the map unresolved.

## 4. Proposed next experiment: E-261103-03, (9,3) pilot

**Single first item.** Amend and commit its PLAN before compute. This is an affordability and
outcome-routing pilot, not a promise to decide the focus. Hypotheses: the full ten-element formulas
are useful at a minute per call; C3 restrictions offer useful savings; SAT outcomes can be routed
to the existing realization/certificate checks. These are untested recommendations.

**Inputs and deterministic selection.** Freeze the census JSON hash, zero-based map indices and
canonical-code hashes. Take maps 0-7 with free C3, each with a C3 formula and a plain formula.
Add plain maps **10, 30, 40, 48**, the first saved representatives of the remaining extra-edge
patterns: three-edge path, two-edge path plus disjoint edge, tripled pair plus doubled pair,
and three-edge star. The C3 panel already supplies matching and triangle patterns. This is at
most **20 formulas, 12 distinct plain maps**, covers all six excess patterns, and includes a
C2-only map and a tripled adjacency. It is a purposive panel, not an unbiased runtime sample.
Verify each selected action preserves the cyclic links and segment pairings. Store the generator
and its full C3 closure; no D3 or fixed-face C2 clauses.

**Order.** After controls, run `(C3, plain)` on maps 0 and 5 (the two C3 excess patterns), then
plain 10, 30, 40, 48, then the remaining six pairs in saved index order. A plain UNSAT settles
that formula even if its C3 counterpart times out; a C3 UNSAT never settles the plain counterpart.

**Budget.** One preparation session, then one worker with a **3600-second hard computational cap
(at most 1 core-hour)**. Each solver call gets 60 seconds; each proof check gets at most 60 seconds.
Reserve 300 seconds for controls and 300 for building/bookkeeping, with up to 600 seconds reserved
for handling the first target SAT model. All stages receive the remaining global deadline;
record final manifest-writing time separately. Worst-case 20 solver/checker pairs use 2400 seconds.
The first target SAT stops further target dispatch after its bounded model processing. This keeps
the pilot small even if realization is harder than solving. No night is authorized by this review.

**Controls before targets.** Replay both plain (8,2) proofs with the external checker, rebuild their
formulas, and run the existing own-map pinned positives, cross-map negative, malformed pairing and
37 inadmissible-map guards. Require exact reconstruction of the two known (8,3) chirotopes, reporting
warm and unseeded paths separately. Add a deterministic generic nine-plane, ten-element pinned
GP/predicate control, checked against direct exact geometry, and the existing free-C3 symmetry-only
positive with the actual selected action after relabeling. These latter controls are not positive
(9,3) embeddings. A required mismatch blocks targets. Failure to fit a nine-plane positive into
the control budget calls for a bounded amendment, not silently dropping it.

**First SAT model.** Save the full assignment and check every clause. Give hinge and two-stage
realization at most 120 seconds each, then the final-polynomial stage at most 120 seconds;
use the remainder of the 600-second reserve for exact signs, geometry and certificate checking.
An optimizer's failed recovery is unresolved. Require `wrong_signs == 0` and an independent exact
sign comparison before geometry. Any geometric output goes through `candidate-check` and
`verify_candidate.py FILE --target S5`, explicitly F=9, g=3, (V,E,F,chi)=(26,39,9,-4).
The all-pairs test alone is insufficient. A symmetry claim also needs the check in section 3.2.

**Predictions and stop rule.** Pre-register as uncertain: at least one plain (9,3) formula completes
within 60 seconds; at least six of the 12 plain panel formulas complete if no SAT interrupts the
panel. Stop on a required control failure, first processed SAT, exhausted prescribed panel or hard
deadline. Preserve CNF, partial/full DRAT, models, checker transcripts and hashes, plus per-stage
elapsed time, budget fraction and actual binding limit. An unchecked UNSAT is not UNSAT-VERIFIED.

| Outcome | Decision before any follow-up |
|---|---|
| Exact S5 witness | Verify, freeze artifacts, obtain independent review; the construction method leads the stretch proposal. |
| First SAT, no witness | Keep the map open. One bounded realization/certificate study takes priority over collecting more models. A final polynomial is model-level only. |
| At least six plain formulas complete, all completed outcomes UNSAT-VERIFIED | Proceed to a costed coverage tranche after the explore pilot. Measure unresolved patterns separately; do not extrapolate the easy median over the hard tail. |
| C3 finishes but plain mostly times out | Record only symmetry-ansatz exclusions. Next discriminate with a 60/300-second paired grid on at most four unresolved plain maps, not a 203-map night. |
| No plain decision, or proofs dominate the budget | Park the full sweep at this budget; one rank-3/core/solver-change pilot must supply a new reason. No mathematical negative conclusion. |
| Failed control or inconsistent pairing/predicate | Stop dependent solving and repair the named boundary before further decisions. |

The 60/300-second follow-up would cost at most 0.8 core-hours including equally capped proof checks,
plus a small registered control allowance, and requires its own amendment. A later coverage tranche
is capped at **10 core-hours**, with fixed map order, stage accounting and no restart of completed
units. An owner-approved laptop night is considered only after measured projection includes proof
checking, realized-model handling and the unresolved tail. The old median-above-one-hour rule is
too permissive: 203 one-hour plain calls alone already cost 203 core-hours.

## 5. Proposed queue (not applied)

Scores for these rows and every other open candidate are in section 6. Queue order includes
conditional branches, not an instruction to execute all items. The next scheduled compute after
item 1 is an explore pilot; do not satisfy the one-in-two quota by relabeling routine proof replay.

| Rank | Item / hypothesis | Cheapest falsifying test | Budget and stop | What the outcomes change | Explore |
|---|---|---|---|---|---|
| **1** | **E-261103-03 paired pilot**; affordable full formulas, H-261103-02 and residual H-261101-07 | Section 4 panel and controls | 1 preparation session + <=1 core-h; first processed SAT, failed control, panel or cap | Route to construction, realizability, plain coverage or a changed exact method | No |
| 2 | E-261103-05; a multisegment solid-first engine has power on known objects | Exact disk-aware inner solver recovers both supplied (8,3) objects; then random symmetric control starts | 1 session, <=2 core-h; R2 failure stops R3, no R3 success parks this configuration | Pass earns a separately costed target pilot; failure is an engine limit, not S5 nonexistence | **Yes** |
| 3 | E-261101-09 step 1 with E-261101-11 review preparation; the conditional chain survives an external implementation/reader | Shared-predicate comparison on the two plain negatives and known positives; explicitly identify missing multisegment support | 1 session, <=0.25 core-h; first mismatch stops dependent claims; owner contact wait at most 4 weeks before another reviewer | Mismatch repairs interpretation; agreement strengthens validation without automatically upgrading a theorem | No; review work |
| 4 | E-261103-03 conditional continuation; either a target model is recoverable or remaining plain formulas are affordable | First saved target model, or the 60/300-second four-map grid | Model study <=1 core-h; otherwise <=1 core-h grid, then separately approved <=10 core-h tranche; no automatic extension | Witness closes focus; exact model obstruction yields sound cuts only; timeouts trigger re-plan | No |
| 5 | E-261103-04; multiedge-aware descent and ascent really supply useful parents | Construct a valid descent chain and rediscover the known (8,3) controls through that same path | 1 session, <=2 core-h, 3/10-minute per-level grid with few seeds; failed chain/control parks | Passing controls earns a small target pilot; a failed target pilot buys no unchanged second night | **Yes** |
| 6 | Proposed plain-(8,2) core study (section 7), under a new scored row; a small obstruction transfers | One clause-family ablation on each saved plain formula, retaining proofs | 1 session, <=0.5 core-h; no common useful pattern stops mining | A proved reusable pattern informs (9,3); dense/unrelated cores leave the current plan unchanged | No |
| 7 | E-261103-06; planarity can be reached while maintaining embedding | Embedded Szilassi control with barrier and exact final judge | 1 session, <=2 core-h; failed R1 parks; second session only after pass, for an (8,3) control | Only both passes earn a target pilot; a spectral drawing alone is not a pass | **Yes** |
| 8 | E-261101-06 in S5 form, only if full-formula costs warrant it; rank-3 constraints prune | Known normals pass; compare three unresolved map relaxations against the full formulas | 1 session, <=0.5 core-h; no pruning on all three stops | A checked exclusion helps coverage; all SAT without useful pruning returns effort to model realization | No |

Items 1/2, 4/5 and 6/7 pair exploitation and exploration. If a conditional item is skipped, preserve
the quota in the next actually executed pair. E-261103-07 needs no new census; leave stretch geometry
behind a focus result or an explicit owner strategy change. External messages remain the owner's
action; this review sends none. Publication/novelty work cannot be inferred complete from internal
tests or an unanswered email.

## 6. Re-scoring all open candidates

Inventory at the cut: **94 open ideas, 26 open hypotheses, 23 planned experiments and one running
experiment: 144 candidates**. Every one appears exactly once below. Supported H-261103-01 and -03
and completed E-261103-01/-02 are evidence, not open candidates. Scores are judgments under the
current focus, not a restatement of historical S0 scores. Hypothesis scores value the next useful
test, not belief in the hypothesis. An open graph status is not permission to restart consumed work.

T/D/F/G/R retain ROADMAP's 0-2 definitions. `J=2` means a direct focus construction/decision route,
`J=0` a ladder; `-` means supporting work or no current focus construction. `s` is a work session,
`h` a core-hour. Kill cost is the proposed first bounded test that could park the item, not a promise
of a mathematical refutation or an approved run. T+D below 3 is below the execution gate. Equal
scores need not imply equal queue order: dependencies, duplicated work and the explore quota matter.

Disposition keys: **Q** queued/conditional, **A** supporting audit, **B** backlog needing a new
discriminating test, **C** consumed question (retain as a control), **P** parked S0/S1 scope,
**S** stretch only. A reusable idea adapted to S5 is shown in the focus table; its original S0 run
is not thereby reopened. All original S0-only experiments/hypotheses are listed separately.

### 6.1 Focus, shared validation, consumed controls and reusable backlog

| ID | Candidate | T D F G R | J | First kill cost | Disposition / reason |
|---|---|---|---|---|---|
| [E-261101-06](../experiments/E-261101-06-rank3-sat-per-type/README.md) | Rank-3 (normals-only) SAT per type | 2 2 1 2 2 | - | 1s+0.5h | Q: Only if full S5 formulas stall |
| [E-261101-09](../experiments/E-261101-09-encoding-comparison/README.md) | Compare our encoding with polyhedraproof on shared instances | 2 2 1 2 2 | - | 1s+0.25h | A: Shared semantics; external implementation needed |
| [E-261101-11](../experiments/E-261101-11-external-human-review/README.md) | External human review of FD5/FD6 and the type-0 dossier | 2 2 1 2 2 | - | 1s; 4-week reply limit | A: Human review; owner handles contact |
| [E-261101-12](../experiments/E-261101-12-maximal-face-neighbourly/README.md) | Maximal face-neighbourly cubic polyhedra per genus | 2 2 2 2 2 | 2 | 1h via E-261103-03 | Q: Umbrella; no duplicate run |
| [E-261101-21](../experiments/E-261101-21-fold-locus-controls/README.md) | The Gauss map as a fold map - find the identity on the controls, then add it to the rank-3 encoding | 1 1 1 2 2 | - | 1s | B: No demonstrated extra pruning |
| [E-261103-03](../experiments/E-261103-03-s5-exact-decision-8-2-9-3/README.md) | Exact decision per candidate map - OM-SAT for the 2 (8, 2) maps, then the symmetric and all admissible (9, 3) maps | 2 2 2 2 2 | 2 | 1s+1h | Q: First paired target pilot |
| [E-261103-04](../experiments/E-261103-04-s5-genus-ladder-9-faces/README.md) | Genus ladder on 9 faces - the admissible (9, 3) maps from their sphere down and up again (explore) | 1 2 1 1 2 | 0 | 1s+2h | Q: Need multiedge chain and recovery controls |
| [E-261103-05](../experiments/E-261103-05-s5-symmetric-solid-first/README.md) | Symmetric solid-first for S5 - C3, D3 and C2 arrangements of 9 planes with the exact inner solver (the Roest-Vigh route) | 2 2 1 1 2 | 2 | 1s+2h | Q: First explore; exact disk/multirun controls |
| [E-261103-06](../experiments/E-261103-06-embedded-first-pilot/README.md) | Embedded first, planar later - pilot on Szilassi from a torus, then an 8-face object from a smooth genus-3 surface | 1 2 1 2 1 | 2 | 1s+2h | Q: Embedding-preserving control before target |
| [E-261103-07](../experiments/E-261103-07-s5-10-4-census-symmetry/README.md) | Census and symmetric sub-list of the (10, 4) candidate maps - preparation of the stretch target | 1 1 2 2 2 | - | 0.25h | S: Census done; symmetry compatibility only |
| [H-261101-02](../hypotheses/H-261101-02-short-structural-obstruction.md) | A short structural obstruction (a lemma on few constraint families) kills many types | 2 2 2 2 2 | - | 1s+0.5h | Q: Adapt to two plain small-case cores |
| [H-261101-07](../hypotheses/H-261101-07-maximal-face-neighbourly-exist.md) | Maximal face-neighbourly cubic polyhedra with few doubled pairs exist for genus 2-5 | 2 2 2 2 2 | 2 | 1h via first pilot | Q: Genus-2 branch conditionally closed; 3-5 open |
| [H-261101-14](../hypotheses/H-261101-14-fold-locus-identity.md) | A fold-map identity constrains the convex region of the Gauss map beyond the known counts | 1 1 1 2 2 | - | 1s | B: Identity may be redundant |
| [H-261103-02](../hypotheses/H-261103-02-s5-9-3-c3-object-exists.md) | A (9, 3) polyhedron exists with a 3-fold rotational symmetry, on one of the 8 admissible maps with a free C3 | 2 2 2 1 2 | 2 | 1h via first pilot | Q: Needs exact geometric symmetry, not signs alone |
| [I-261029-02](../ideas/I-261029-02-gauss-bonnet-discharging-bound.md) | Gauss-Bonnet discharging bound on face weights | 1 1 1 2 2 | - | 1s | B: Local bounds may inform core study |
| [I-261029-05](../ideas/I-261029-05-planarization-flow-with-barrier.md) | Planarization flow with a barrier from a smooth surface | 1 2 1 2 1 | 2 | 1s+2h | Q: Use existing embedded-first pilot |
| [I-261029-06](../ideas/I-261029-06-llm-guided-plane-generator-search.md) | LLM-guided search for plane-set generators (FunSearch style) | 0 1 2 1 1 | 2 | 1s+0.5h | B: Generator search lacks discriminating control |
| [I-261029-08](../ideas/I-261029-08-difference-map-rrr-engine.md) | Difference map / RRR feasibility engine | 1 1 1 1 1 | 2 | 1s+0.5h | B: New engine must beat known-object control |
| [I-261029-09](../ideas/I-261029-09-rare-event-level-sampling.md) | Rare-event level sampling (subset simulation, Wang-Landau, population annealing) | 1 1 0 1 1 | 2 | 1s+1h | B: Rare-event objective not calibrated |
| [I-261029-10](../ideas/I-261029-10-tropical-patchworking-valuation-seeds.md) | Tropical limit / Viro patchworking seeds | 1 1 1 2 1 | 2 | 1s+0.5h | B: Distinct seed family; no current evidence |
| [I-261029-11](../ideas/I-261029-11-cegar-immersion-sat-loop.md) | CEGAR loop on the immersion SAT | 2 2 1 2 2 | 2 | 1h on first target model | Q: Sound refinements only |
| [I-261029-16](../ideas/I-261029-16-generalized-winding-number-test.md) | Generalized winding number test of embeddedness | 1 1 2 1 2 | - | 1s | B: Extra verifier only if a specific gap appears |
| [I-261029-19](../ideas/I-261029-19-homotopy-continuation-complex-detours.md) | Homotopy continuation with complex detours | 1 1 1 2 1 | 2 | 1s+1h | B: Inequalities and embedding remain bottlenecks |
| [I-261029-20](../ideas/I-261029-20-signs-to-phases-relaxation.md) | Chirotope signs to unit-phase relaxation | 0 1 0 1 1 | 2 | 1s | B: No justified phase-relaxation advantage |
| [I-261029-21](../ideas/I-261029-21-staged-search-preserving-invariants.md) | Staged search that preserves invariants (Thistlethwaite style) | 1 1 0 1 1 | 2 | 1s | B: Staging alone supplies no success gate |
| [I-261029-22](../ideas/I-261029-22-macro-operator-plane-moves.md) | Learned macro-operators of 2-3 plane moves | 0 1 0 1 1 | 2 | 1s | B: No tested predictive move signal |
| [I-261029-23](../ideas/I-261029-23-parity-invariant-for-n8-plateau.md) | Parity-type invariant explaining the n = 8 plateau | 1 0 2 2 2 | - | 0h | C: n=8 decision done; use proof cores for explanation |
| [I-261029-24](../ideas/I-261029-24-pattern-database-face-subsets.md) | Pattern database of locally feasible face subsets | 2 1 1 2 2 | - | 1s+0.5h | B: Prerequisite is reusable local obstruction |
| [I-261029-25](../ideas/I-261029-25-fail-first-branching-lemma-clauses.md) | Fail-first branching and failure-pattern lemmas | 1 1 1 1 2 | - | 0.5h | B: Only if solver profile identifies branching cost |
| [I-261029-28](../ideas/I-261029-28-failed-literal-probing.md) | Lookahead / failed-literal probing | 1 1 1 1 2 | - | 0.5h | B: Probing needs a measured baseline |
| [I-261029-35](../ideas/I-261029-35-smooth-formulation-lbfgs-least-squares.md) | Smooth formulation with L-BFGS / Levenberg-Marquardt | 1 2 1 1 2 | 2 | 1h on first target model | Q: Use existing realizers before another implementation |
| [I-261029-37](../ideas/I-261029-37-cross-entropy-method-construction.md) | Cross-entropy method (Wagner 2021 style) | 0 1 0 1 1 | 2 | 0.5h | B: Generic black-box mutation, no focus evidence |
| [I-261029-39](../ideas/I-261029-39-mcts-alphazero-construction.md) | MCTS / AlphaZero-style plane-by-plane construction | 0 1 0 1 1 | 2 | 1s | B: Learned search has no training/control case |
| [I-261029-40](../ideas/I-261029-40-bayesian-optimisation-surrogate.md) | Bayesian optimisation with a surrogate for expensive objectives | 0 1 0 1 1 | 2 | 1s | B: Expensive-surrogate premise not established |
| [I-261029-43](../ideas/I-261029-43-sat-symmetry-breaking-breakid-satsuma.md) | Symmetry breaking for the chirotope SAT (BreakID, satsuma) | 2 1 2 2 2 | - | 0.25h | A: Audit existing normalization before stronger breakers |
| [I-261029-45](../ideas/I-261029-45-final-polynomials-nonrealizability.md) | Final polynomials as realizability certificates | 2 2 2 2 2 | - | 0.25h per model | Q: Exact certificates exclude models only |
| [I-261029-46](../ideas/I-261029-46-bokowski-hay-numerical-optimization.md) | Bokowski-Hay numerical optimization method | 1 1 1 1 1 | 2 | 1s+0.5h | B: Existing hinge path first |
| [I-261029-47](../ideas/I-261029-47-small-om-database-encoder-ground-truth.md) | Small realizable-OM databases as encoder ground truth | 2 2 1 2 2 | - | 1s | A: Ground-truth comparison supplements known objects |
| [I-261029-48](../ideas/I-261029-48-dreal-delta-sat-sign-conditions.md) | dReal delta-complete SMT for the sign conditions | 2 1 1 1 2 | 2 | 1s+0.5h | B: Delta-sat is not an exact witness |
| [I-261029-50](../ideas/I-261029-50-mnev-realization-space-continuation-test.md) | Realization-space warning (Mnev) and continuation test | 1 1 1 1 1 | - | 1h per model | B: Failed continuation is not nonrealizability |
| [I-261029-57](../ideas/I-261029-57-realizability-audit-om-models.md) | Check whether SAT oriented-matroid models of relaxed instances are realizable | 2 2 2 2 2 | - | 1h on first target model | Q: Next branch after target SAT |
| [I-261029-62](../ideas/I-261029-62-face-local-reflex-types.md) | Face-local types with a prescribed reflex count | 2 1 1 2 2 | - | 1s+0.5h | B: Conditional local-type pruning |
| [I-261030-01](../ideas/I-261030-01-spine-seeded-solids.md) | Spine-seeded solids (thickened graphs of cycle rank 6) | 1 1 1 2 1 | 2 | 1s+0.5h | B: Adapt spine genus to focus; benchmark first |
| [I-261030-03](../ideas/I-261030-03-branching-handles-in-ladder.md) | Branching handles in the ladder | 1 1 1 1 2 | 0 | 0.5h | B: Move variant only inside controlled ladder |
| [I-261030-07](../ideas/I-261030-07-symmetric-orbit-ansatz-plane-only.md) | Symmetric orbit ansatz with plane-only construction (Roest-Vigh style) | 2 2 1 1 2 | 2 | 1s+2h | Q: S5 adaptation is solid-first explore |
| [I-261030-08](../ideas/I-261030-08-small-integer-lattice-plane-search.md) | Small-integer lattice search of plane coefficients | 1 2 1 1 2 | 2 | 0.5h after controls | B: Finite coefficient box; no complete exclusion |
| [I-261030-10](../ideas/I-261030-10-doubled-rung-ladder-over-n.md) | Ladder over n with doubled rungs | 1 2 1 1 2 | 0 | 0.5h after controls | B: Re-select cells, no monotone maximal ladder |
| [I-261030-11](../ideas/I-261030-11-known-8-face-objects-as-engine-bench.md) | Known 8-face objects as engine test bench | 2 2 2 2 2 | - | 1s+2h | Q: Construction controls still needed |
| [I-261030-14](../ideas/I-261030-14-chain-choice-by-spanning-margin.md) | Chain choice by spanning margin | 1 1 1 1 2 | 0 | 0.5h | B: Only if valid S5 descent exists |
| [I-261030-18](../ideas/I-261030-18-voltage-lifting-symmetric-relaxed-maps.md) | Voltage-graph lifting for symmetric relaxed maps | 2 0 2 2 2 | - | 0h | C: C3 census cross-check already completed |
| [I-261030-22](../ideas/I-261030-22-more-chains-per-type.md) | More chains per type in the genus ladder | 1 0 1 1 2 | 0 | 0.5h | B: More chains needs measured S5 control power |
| [I-261030-23](../ideas/I-261030-23-exact-local-obstruction-stuck-pattern.md) | Exact local obstruction test of a stuck pattern | 2 1 1 2 2 | - | 0.5h | B: Only a named recurring local failure |
| [I-261030-29](../ideas/I-261030-29-rank3-sat-per-type.md) | Rank-3 (normals-only) SAT per type | 2 2 1 2 2 | - | 1s+0.5h | Q: S5 rank-3 fallback, not immediate prerequisite |
| [I-261030-31](../ideas/I-261030-31-n8-exact-omsat.md) | Decide the n = 8 rung exactly with 9-element OM-SAT | 2 0 2 2 2 | - | 0h | C: Both plain n=8 decisions already obtained |
| [I-261030-32](../ideas/I-261030-32-sign-target-realization.md) | Realize a SAT chirotope by maximizing the minimum margin of its signs | 2 2 2 2 2 | 2 | 1h on first target model | Q: Controlled sign realizer, exact final judge |
| [I-261031-01](../ideas/I-261031-01-count-rank3-solutions.md) | Count and sample rank-3 solutions per type and test their stretchability | 2 1 1 2 2 | - | 0.5h after rank-3 pilot | B: Counting useful only for a chosen split |
| [I-261031-02](../ideas/I-261031-02-cube-and-conquer-rank3-split.md) | Cube-and-conquer with cubes on the rank-3 variables and DRAT per cube | 2 1 1 2 2 | 2 | 1s+1h | B: Cube only after plain runtime gate fails |
| [I-261031-03](../ideas/I-261031-03-encoding-comparison.md) | Compare our encoding with a third-party one on shared instances | 2 2 1 2 2 | - | 1s+0.25h | A: External encoder agreement |
| [I-261101-04](../ideas/I-261101-04-exact-covering-check.md) | Replace sampled covering by an exact covering check | 2 1 1 2 2 | - | 1s | B: Exact covering only when a clause needs it |
| [I-261101-06](../ideas/I-261101-06-external-human-review.md) | Ask a human mathematician to review the certified results and the dossier | 2 2 1 2 2 | - | 1s; 4-week reply limit | A: Human review of conditional chain |
| [I-261101-07](../ideas/I-261101-07-maximal-face-neighbourly-ladder.md) | Maximal face-neighbourly cubic polyhedra per genus | 2 2 2 2 2 | 2 | 1h via first pilot | Q: Residual maximal cases remain open |
| [I-261101-08](../ideas/I-261101-08-arrangement-first-structured-arrangements.md) | Arrangement first - symmetric plane arrangements with asymmetric solids, decided exactly per arrangement | 2 2 1 1 2 | 2 | 1s+2h | Q: S5 arrangement adaptation; asymmetric solids allowed |
| [I-261101-12](../ideas/I-261101-12-incremental-sat-shared-gp-lemmas.md) | One incremental SAT session for all types - shared Grassmann-Pluecker lemmas, selector literals per type | 1 1 2 1 2 | - | 1h | B: Shared clauses only after measured need |
| [I-261101-13](../ideas/I-261101-13-convex-region-fold-map-topology.md) | The Gauss map as a fold map - topology of the convex region as rank-3 clauses | 1 1 1 2 2 | - | 1s | B: Fold identity needs independent constraints |
| [I-261101-17](../ideas/I-261101-17-scenario-probability-ledger.md) | An explicit three-scenario credence ledger for the decision point | 2 2 2 2 2 | - | 0h; this review | A: Separate credence from conditional closure |
| [I-261101-18](../ideas/I-261101-18-face-ladder-cegar.md) | The face ladder is monotone, the genus ladder is not - k-face sub-instances and face-CEGAR seeds | 2 1 1 2 2 | 0 | 1h | B: Face subsets only after full S5 formulas stall |
| [I-261101-20](../ideas/I-261101-20-few-convex-vertices-spike-ansatz.md) | Few convex vertices - both known 8-face objects have exactly 4, the covering minimum; search and encode that first | 1 2 1 1 2 | 2 | 0.5h after controls | B: Few-convex ansatz; exclude only restricted formula |
| [I-261101-22](../ideas/I-261101-22-research-loop-exploit-explore.md) | Choose the next experiment by credences with an explicit exploration quota, and gate every engine by a benchmark ladder | 2 2 2 2 2 | - | 0h; this review | A: One-in-two quota and useful benchmark gates |
| [I-261103-01](../ideas/I-261103-01-embedded-first-planar-later.md) | Embedded first, planar later - flatten the faces of an embedded genus-6 surface with the target adjacency, never leaving embedding | 1 2 1 2 1 | 2 | 1s+2h | Q: Use E-261103-06 pilot |
| [I-261103-02](../ideas/I-261103-02-om-level-tope-selection-census-free.md) | Census-free exact search - select the solid's topes inside the oriented matroid, chirotope and cell set in one SAT instance | 1 1 0 2 1 | 2 | 1s scoping | B: Census-free rebuild no longer removes a bottleneck |
| [I-261103-03](../ideas/I-261103-03-interval-branch-and-bound-c3-ansatz.md) | Interval branch-and-bound over the C3 ansatz - a complete decision of the symmetric (9, 3) case by validated numerics | 2 1 0 1 1 | 2 | 1s+0.5h | B: Chart/box coverage missing |
| [I-261103-04](../ideas/I-261103-04-ninth-plane-sweep-known-8-plane-arrangements.md) | Ninth-plane sweep - add one plane to the Roest-Vigh or Mizhaev arrangement and let the exact inner solver re-select the solid | 1 2 1 1 2 | 2 | 0.5h after inner controls | B: Correct 36-pair trigger; small panel first |
| [I-261103-05](../ideas/I-261103-05-spectral-start-embedded-first.md) | Spectral start for embedded-first - a Tutte / Colin de Verdiere type 3D drawing of the cubic 1-skeleton as the initial embedded surface | 1 2 2 1 1 | - | 1s | B: Drawing must pass embedding before flattening |
| [I-261103-06](../ideas/I-261103-06-z3-fundamental-piece-construction.md) | Z3 fundamental piece - build a C3-symmetric (9, 3) polyhedron as three copies of a planar-faced patch whose boundary matches its rotated image | 2 1 1 1 2 | 2 | 1s+0.5h | B: Patch formulation only if C3 survives |

### 6.2 Parked S0 and twelve-face S1 candidates

| ID | Candidate | T D F G R | J | First kill cost | Disposition / reason |
|---|---|---|---|---|---|
| [E-261101-03](../experiments/E-261101-03-type0-dossier/README.md) | Type-0 genus-3 dossier: is the best result correct and new? | 1 1 2 1 2 | - | 1s | P: Dossier; no focus decision |
| [E-261101-04](../experiments/E-261101-04-normals-first-power-study/README.md) | Power of normals first: how often is the control SAT at radius r? | 1 0 2 1 2 | - | 2h | P: Low-power S0 sampling |
| [E-261101-05](../experiments/E-261101-05-unsat-core-mining/README.md) | Proof mining: small cores of fixed-normal UNSAT instances | 1 1 2 2 2 | - | 0.5h | P: Fixed-normal cores; no direct transfer |
| [E-261101-08](../experiments/E-261101-08-relaxed-s1-twelve-faces/README.md) | Relaxed S1 target: 12 faces with doubled pairs, symmetric ansatz | 1 1 1 1 2 | - | 1s+2h | P: Twelve-face S1 behind focus |
| [E-261101-10](../experiments/E-261101-10-write-up-symmetric-immersion/README.md) | Write-up: no symmetric polyhedral immersion | 2 1 1 1 2 | - | 1s | P: Capped existing write-up allowance |
| [E-261101-14](../experiments/E-261101-14-chirotope-chambers/README.md) | Chirotope chambers of the archived realizations | 1 0 2 1 2 | - | 1s | P: Descriptive archive work |
| [E-261101-15](../experiments/E-261101-15-cube-and-conquer-pilot/README.md) | Cube-and-conquer pilot on 3 types (after E-261101-06 and -09) | 2 1 0 1 2 | - | 1s scoping | P: S0 campaign has no focus budget |
| [E-261101-16](../experiments/E-261101-16-arrangement-first-chamber-sat/README.md) | Arrangement first - exact chamber-SAT on structured and archived 12-plane arrangements | 2 1 2 1 2 | - | 1s+2h | P: S5 adaptation is E-261103-05 |
| [E-261101-17](../experiments/E-261101-17-realization-space-geometry/README.md) | Geometry of the realization spaces - chord widths, shrinkage per handle, connectivity of the archive | 1 1 2 1 2 | - | 2h | P: Widths do not decide focus |
| [E-261101-18](../experiments/E-261101-18-face-grouped-mus-symmetric/README.md) | Face-grouped minimal unsatisfiable cores of the 50 certified symmetric instances | 2 1 2 2 2 | - | 0.5h | P: Symmetry-background cores; prefer plain S5 cores |
| [E-261101-19](../experiments/E-261101-19-barrier-continuation-genus3-handle/README.md) | Barrier continuation from genus-3 realizations towards an in-class handle (replaces E-261101-07) | 2 1 1 2 2 | - | 1h | P: S0 genus-3-to-4 continuation |
| [E-261101-20](../experiments/E-261101-20-incremental-sat-across-types/README.md) | One incremental SAT session for the symmetric instances - do shared GP lemmas cut the total time? | 1 1 2 1 2 | - | 1h | P: Optimize only after S5 timings |
| [E-261101-22](../experiments/E-261101-22-equivelar-literature/README.md) | Literature - the two unread primary sections that could change the plan, then equivelar {p,3} polyhedra | 1 1 2 1 1 | - | 1s | P: Remaining equivelar literature; no novelty conclusion |
| [E-261101-24](../experiments/E-261101-24-farkas-descent-pilot/README.md) | Farkas-certificate descent on the normals - pilot on the 80 radius-0 seeds and a perturbed witness | 2 1 1 1 2 | - | 1s+1h | P: Guided S0 offset experiment |
| [H-261029-01](../hypotheses/H-261029-01-gauss-condition-rare.md) | The Gauss-degree condition is rare: under 1e-3 of random normal sets per type pass it | 1 1 2 1 2 | - | 0.25h | P: Rarity on S0 normals does not decide S5 |
| [H-261029-02](../hypotheses/H-261029-02-chamber-formulation-faster.md) | The chamber formulation (165 variables, no parity) solves fixed-arrangement instances 10x faster than formulation B | 1 1 2 1 2 | - | 0.5h | P: S0 fixed-arrangement timing claim |
| [H-261029-03](../hypotheses/H-261029-03-fixed-normal-objective-smoother.md) | At fixed normals, min over offsets of the violation count is a smoother objective; local search on normals with it gets below the 21-24 plateau | 1 1 1 1 1 | - | 1s+1h | P: No new focus test |
| [H-261029-04](../hypotheses/H-261029-04-no-convex-face-many-saddles.md) | In any realization no face is convex and the saddle count is well above the bound 13 | 1 1 2 1 2 | - | 0.25h | P: Twelve-face saddle/convex-face claim |
| [H-261029-05](../hypotheses/H-261029-05-szilassi-fixed-face-mechanism.md) | Szilassi embeds because of its symmetry-fixed central convex face; a 12-face analogue has no fixed face | 1 1 1 1 1 | - | 1s | P: Explanatory analogy, weak discrimination |
| [H-261029-06](../hypotheses/H-261029-06-no-immersion-at-all.md) | The 12-face map admits no polyhedral immersion with planar faces at all (asymmetric case included) | 2 1 1 2 2 | - | 1h pilot | P: Asymmetric S0 immersion still open |
| [H-261029-09](../hypotheses/H-261029-09-admissible-normals-rarely-closable.md) | Gauss-admissible normals are almost never closable: the realization space projects to a tiny set inside the admissible region | 1 1 2 1 2 | - | 2h | P: Closability rarity; bounded evidence |
| [H-261029-10](../hypotheses/H-261029-10-c2-immersion-needs-simplicity.md) | In every C2 class the immersion instance is UNSAT, and without face simplicity it is SAT | 2 1 1 1 2 | - | 0.5h | P: S0 simplicity ablation; no focus change |
| [H-261101-01](../hypotheses/H-261101-01-szilassi-12-exists.md) | Szilassi-12 exists: some asymmetric realization of one of the 59 types | 2 1 0 2 2 | - | 1h pilot | P: S0 existence is still parked |
| [H-261101-03](../hypotheses/H-261101-03-gauss-class-binding-barrier.md) | The Gauss class (degree, covering, saddles) is the main barrier above genus 3 | 2 1 1 2 2 | - | 1h | P: Genus-3-to-4 claim, not focus exclusion |
| [H-261101-04](../hypotheses/H-261101-04-normals-first-unsat-real.md) | The 12,202 normals-first UNSATs reflect a real obstruction between levels | 1 0 2 1 2 | - | 2h | P: Prior negatives have weak control power |
| [H-261101-05](../hypotheses/H-261101-05-type0-witness-correct-new.md) | The type-0 genus-3 object is correct and new | 1 1 2 1 2 | - | 1s | P: Dossier correctness/novelty separate |
| [H-261101-06](../hypotheses/H-261101-06-per-type-decision-affordable.md) | An exact per-type decision costs about 300 core-hours and its proofs can be checked on the fly in 6-hour shards | 2 1 0 1 2 | - | 1s scoping | P: S0 campaign costs not inferred from n=8 |
| [H-261101-08](../hypotheses/H-261101-08-structured-arrangement-high-genus-solid.md) | Some structured 12-plane arrangement carries an all-adjacent solid of genus >= 4 | 2 1 2 1 2 | - | 1s+2h | P: Twelve-plane arrangements; S5 has own experiment |
| [H-261101-09](../hypotheses/H-261101-09-thin-realization-region.md) | The realization regions are thin and shrink sharply per handle, so sampling has no power at any genus | 1 1 2 1 2 | - | 2h | P: Thinness remains a sampling hypothesis |
| [H-261101-10](../hypotheses/H-261101-10-handles-wrong-move.md) | Handles are the wrong move - no genus-3 realization space reaches an in-class handle | 2 1 1 2 2 | - | 1h | P: No new evidence for universal handle barrier |
| [H-261101-11](../hypotheses/H-261101-11-few-face-core.md) | The symmetric obstructions have cores on at most six faces that recur across classes | 2 1 2 2 2 | - | 0.5h | P: S0 symmetric-core size needs testing |
| [H-261101-12](../hypotheses/H-261101-12-om-sat-nonrealizable-types.md) | Some types are SAT at the oriented-matroid level with only non-realizable models | 2 1 1 2 2 | - | 0.25h per model | P: Full S0 models not decided by submodels |
| [H-261101-13](../hypotheses/H-261101-13-no-improper-symmetric-immersion.md) | No polyhedral immersion of the 12-face map has a mirror or point-reflection symmetry | 2 1 1 2 2 | - | 1s review | P: Improper-isometry statement needs human review |
| [H-261101-15](../hypotheses/H-261101-15-k-face-obstruction.md) | The obstruction is local in faces - every type has an UNSAT sub-instance on at most nine faces | 1 1 2 2 2 | - | 1h | P: Greedy-face results do not cover all subsets |
| [H-261101-16](../hypotheses/H-261101-16-farkas-descent-reaches-closable-normals.md) | Guided by the Farkas certificate, the normals reach offset-feasible configurations that annealing never found | 2 1 1 1 2 | - | 1s+1h | P: Farkas-guided S0 feasibility only |
| [H-261101-17](../hypotheses/H-261101-17-chirotope-first-reaches-models.md) | Core-guided SAT under rank-3 assumptions reaches embedding models of the full 12-face instance in minutes | 1 0 1 1 2 | - | 0h; existing controls | P: Stop cap-extension chain; full-map gate failed |
| [I-261029-01](../ideas/I-261029-01-maxwell-cremona-lifting-genus-g.md) | Maxwell-Cremona lifting criterion for genus g | 1 1 0 2 1 | - | 1s | P: Unspecified general lifting theorem |
| [I-261029-03](../ideas/I-261029-03-single-farkas-certificate-period-conditions.md) | One Farkas certificate for the period conditions | 1 1 0 2 1 | - | 1s | P: Universal certificate not supplied |
| [I-261029-12](../ideas/I-261029-12-local-search-sat-immersion-cnf.md) | Local-search SAT (probSAT, yalsat, ddfw) on the immersion CNF | 1 1 1 1 2 | - | 0.5h | P: Unchanged S0 immersion search |
| [I-261029-13](../ideas/I-261029-13-gwas-on-near-miss-defects.md) | GWAS-style analysis of near-miss defects | 1 0 2 1 1 | - | 0.25h | P: Near-miss pattern diagnosis |
| [I-261029-14](../ideas/I-261029-14-landau-irrep-subspace-search.md) | Search near symmetric near-misses along one irrep at a time | 1 1 1 1 1 | - | 0.5h | P: S0 symmetry-breaking perturbations |
| [I-261029-15](../ideas/I-261029-15-projective-symmetries-covered-free.md) | Projective symmetries covered by the symmetric theorem | 2 1 1 2 2 | - | 1s review | P: Strengthen S0 theorem only after proof review |
| [I-261029-17](../ideas/I-261029-17-penrose-cohomology-sugihara-lp.md) | Penrose cohomology and Sugihara LP for the period obstruction | 1 1 0 2 1 | - | 1s | P: Cohomology framing without a cheap discriminator |
| [I-261029-18](../ideas/I-261029-18-weierstrass-period-problem-analogy.md) | Weierstrass representation and the period problem | 1 1 0 2 1 | - | 1s | P: Degree-five S0 analogy; no concrete focus test |
| [I-261029-41](../ideas/I-261029-41-schewe-nonrealizability-transfer-to-dual.md) | Transfer Schewe non-realizability to the dual (planes) problem | 1 1 1 2 2 | - | 1s | P: Vertex/face transfer needs a theorem |
| [I-261029-49](../ideas/I-261029-49-toroidal-catalogs-pairwise-adjacent.md) | Check toroidal polyhedra catalogs for pairwise-adjacent faces | 1 1 2 1 1 | - | 1s | P: Toroidal catalogue has no direct genus-3 test |
| [I-261029-51](../ideas/I-261029-51-geometry-first-maxsat-near-miss.md) | Geometry-first MaxSAT on near-miss arrangements | 1 1 1 1 2 | - | 0.5h | P: S0 near-miss arrangements; control power first |
| [I-261029-52](../ideas/I-261029-52-prior-work-exclusion-of-types.md) | Check prior work for excluded types (Bokowski-Pisanski 2007) | 2 1 2 1 2 | - | 1s | P: Avoid duplicated S0 work, not focus compute |
| [I-261029-58](../ideas/I-261029-58-turning-defect-diagnostics.md) | Log per-face turning numbers, multi-reflex vertices and crossings in the immersion annealer | 1 1 2 1 2 | - | 0.25h | P: Diagnostics only, no target decision |
| [I-261029-60](../ideas/I-261029-60-first-moment-calibration.md) | First-moment estimate of how rare closable normals should be | 1 1 1 1 2 | - | 1h | P: S0 rarity estimate not geometric exclusion |
| [I-261029-61](../ideas/I-261029-61-arf-invariant-annuli.md) | Arf invariant of the three-face annuli of an immersion | 1 1 0 2 1 | - | 1s after immersion | P: No immersion input; theorem needs verification |
| [I-261029-63](../ideas/I-261029-63-two-charts-at-infinity.md) | A second plane at infinity in OM-SAT (14th element) | 1 0 1 1 2 | - | 0.5h | P: Extra chart has no measured pruning benefit |
| [I-261030-06](../ideas/I-261030-06-relaxed-12-face-doubled-pairs.md) | Relaxed 12-face target with collinear doubled pairs | 1 1 1 1 2 | - | 1s+2h | P: Twelve-face S1 behind focus |
| [I-261030-12](../ideas/I-261030-12-projective-ladder-chart-search.md) | Projective ladder with a free plane at infinity | 1 1 1 1 2 | - | 0.5h | P: S0 free-chart proposal |
| [I-261030-20](../ideas/I-261030-20-uniform-thomson-normal-starts.md) | Uniform (Thomson / spherical-design) starts for normal annealers | 1 0 2 1 1 | - | 0.25h | P: More normal seeds do not change decisions |
| [I-261030-21](../ideas/I-261030-21-realization-space-width-lp.md) | Realization-space width via LP at fixed normals | 1 1 2 1 2 | - | 0.5h | P: Archive-width diagnosis |
| [I-261030-30](../ideas/I-261030-30-projective-recharting-move.md) | Projective re-charting move that moves the plane at infinity | 1 0 2 1 2 | - | 0h; existing chart check | P: Stop unchanged projective ladder follow-up |
| [I-261031-04](../ideas/I-261031-04-type0-dossier.md) | A referee-style dossier on the best positive object | 1 1 2 1 2 | - | 1s | P: S0 dossier |
| [I-261031-05](../ideas/I-261031-05-rigidity-config-space.md) | Configuration-space planning and rigidity (stress matrices) between ladder levels | 1 1 0 2 1 | - | 1s | P: No cheap rigidity falsifier yet |
| [I-261031-06](../ideas/I-261031-06-write-up-symmetric-immersion.md) | Write up the symmetric-immersion result | 2 1 1 1 2 | - | 1s | P: Existing write-up allowance only |
| [I-261101-01](../ideas/I-261101-01-normals-first-power-study.md) | Measure the power of normals-first with a positive control | 1 0 2 1 2 | - | 2h | P: Low-power S0 sampling |
| [I-261101-02](../ideas/I-261101-02-unsat-core-mining.md) | Mine minimal UNSAT cores of fixed-normal offset problems | 1 1 2 2 2 | - | 0.5h | P: Fixed-normal cores; plain S5 proposal differs |
| [I-261101-05](../ideas/I-261101-05-chirotope-chambers.md) | Study chirotope chambers of the archived realizations | 1 0 2 1 2 | - | 1s | P: Descriptive archive chambers |
| [I-261101-09](../ideas/I-261101-09-realization-space-geometry-hit-and-run.md) | Measure the realization spaces of the archived polyhedra - widths, volume ratio per handle, connectivity | 1 1 2 1 2 | - | 2h | P: S0 archive widths |
| [I-261101-10](../ideas/I-261101-10-face-grouped-mus-symmetric-cores.md) | Face-grouped minimal unsatisfiable cores of the 50 certified symmetric instances | 2 1 2 2 2 | - | 0.5h | P: S0 symmetry cores; not plain obstructions |
| [I-261101-11](../ideas/I-261101-11-barrier-continuation-handle-feasibility.md) | Barrier continuation inside a genus-3 realization space towards an in-class handle | 2 1 1 2 2 | - | 1h | P: S0 genus-3-to-4 barrier experiment |
| [I-261101-15](../ideas/I-261101-15-equivelar-p3-literature.md) | Szilassi-12 is an equivelar polyhedron of type {11,3} - read the equivelar-polyhedra literature | 1 1 2 1 1 | - | 1s | P: Equivelar S0 literature, no absence proof for S5 |
| [I-261101-16](../ideas/I-261101-16-improper-isometry-lemma-immersions.md) | Close the FD6 gap - no polyhedral immersion has a mirror or point-reflection symmetry | 2 1 1 2 2 | - | 1s review | P: Improper-isometry lemma still unreviewed |
| [I-261101-19](../ideas/I-261101-19-farkas-certificate-descent.md) | Farkas-certificate descent - the exact gradient of offset infeasibility with respect to the normals | 2 1 1 1 2 | - | 1s+1h | P: S0 guided normals, not focus follow-up |
| [I-261102-01](../ideas/I-261102-01-adaptive-seed-budget.md) | Adaptive time per seed on the target (successive halving / restarts), with the progress signal calibrated on the benchmark ladder | 1 0 2 1 2 | - | 0h; existing measurements | P: No predictive seed signal; no cap campaign |


## 7. Missing ideas (untested proposals, not evidence)

1. **Plain-proof ablation before a new theory.** Treat the two short (8,2) refutations as a
   clause-family experiment: GP and valid normalization stay fixed; remove local families or
   segment-disjointness one at a time and compare both maps. Why: these are plain rather than
   symmetry-background contradictions, so a common obstruction could actually transfer. Cheapest
   test: <=0.5 core-hours, checked refutation of every claimed residual contradiction and pinned
   positive controls. A shared syntactic core is not yet a geometric lemma. Proposal scores 2 2 2 2 2,
   J=-; no new graph ID is assigned in this review.
2. **Proof-carrying partial-model cuts.** On the first nonrealizable target model, minimize the
   chirotope signs used by its checked final polynomial and attach the exact certificate to the
   blocking clause. Why: exclude a certified family of models rather than accumulating heuristic
   no-goods. Cheapest test: one of the three existing certified models, <=1 session/0.25 core-hours;
   deleting a needed sign must invalidate the certificate. Proposal scores 2 2 1 2 2, J=-.
3. **Metamorphic pairing audit.** Relabel and reverse selected admissible multisegment maps and
   coorientations, compare projected pinned predicates with exact geometry, and explicitly include
   the tripled-pair pattern. Why: the geometric controls have doubled pairs, while the census also
   contains triple runs. Cheapest test: one session/0.25 core-hours with controlled broken pairing
   and known positive configurations. No positive (8,2) embedding is demanded. Proposal scores
   2 2 2 2 2, J=-. This extends validation, not the census.

These are small adaptations of proof mining, proof-carrying refinement and metamorphic testing,
not claims of new mathematics. Census-free topes, interval C3 search, ninth-plane sweeps, spectral
starts and fundamental pieces are already I-261103-02 through -06, so they are not presented again
as missing ideas.

## 8. Audit findings at the evidence cut

Locations below are relative to `research/12-faced-polyhedron/`. These are proposed corrections;
the cited files have not been edited. File wording is directly observed; mathematical corrections
are PROVED-1 reasoning unless an existing EXACT check is cited.

| Priority / location | Finding and required boundary |
|---|---|
| High: `experiments/E-261103-03-s5-exact-decision-8-2-9-3/README.md:43`, `:46`; `ROADMAP.md:66` | A listed timeout is called a decided map; one NONREALIZABLE-EXACT model is allowed to close a map and trigger the nonexistence note. Replace with formula/model/map status columns and the exhaustive exclusion rule in section 3.3. The partial CONCLUSION and PLAN already state the correct boundary. |
| High: same README `:21`, `:58` | The Goal still schedules fixed-face C2/D3 uniform runs although the handover correctly disclaims their geometric meaning. Use plain fallback; full D3 is not required on the two C3 maps with Aut+=6. |
| High: same README `:48` | Fractions of decided maps are not likelihoods of existence. There is no uniform prior on realizable maps, and the selected easy/symmetric maps are biased. Remove mechanical credence updates by map count. |
| High: `hypotheses/H-261103-02-s5-9-3-c3-object-exists.md:27` | Realization of C3-invariant signs alone does not verify an order-three isometry; all eight uniform C3 UNSATs still need symmetry-family coverage. State the additional obligations in section 3.2. Its rival at line 17 must also allow realizations with other symmetry groups, such as C2; failure of C3 does not imply asymmetry. |
| Medium: `experiments/E-261103-03-s5-exact-decision-8-2-9-3/CONCLUSION.md:45`; `theory/mathematical-model.md:82`; `experiments/E-261103-02-s5-omsat-multi-adjacency-encoder/SOUNDNESS.md:48` | The (8,2) conclusion cites an open-realization/general-position extension, while the explicit openness discussion is twelve-face and the multisegment note assumes uniform planes. Add a focused S5 perturbation lemma, with no claim of human review. This is a missing explicit link, not a counterexample to the exclusion. |
| Medium: `reviews/strategy-review-2026-11-03.md:36`; `STATUS.md:14`; `ROADMAP.md:66` | Affordability of every (9,3) map was asserted before any target timing. The new two plain timings support a pilot only. Cost proof replay and the SAT realization branch as well as the unresolved tail. |
| Medium: `STRATEGY.md:29`; `experiments/E-261103-04-s5-genus-ladder-9-faces/README.md:29` | R4 failure at genus 3 is not a 3-to-4 theorem; constructing parents is a prerequisite, not an exemption from control tests. A triangular multigraph is not automatically a simplicial sphere. Demonstrate valid multiedge-aware chains and known-object recovery before promising every census map a ladder. |
| Medium: same ladder README `:42` | Passing a control and failing a target night does not automatically justify another night with another seed kind. Require a changed, discriminating test under STRATEGY's follow-up rule. |
| Medium: `experiments/E-261103-05-s5-symmetric-solid-first/README.md:33`, `:36`, `:40` | Generic perturbation can break the requested symmetry; random arrangements are not known negative controls; symmetric planes do not force the selected solid to be symmetric. Use demonstrated negative inputs, preserve or explicitly drop symmetry, and check any claimed isometry. |
| Medium: `ideas/I-261103-04-ninth-plane-sweep-known-8-plane-arrangements.md:25` | The trigger above 36 distinct pairs is impossible on nine faces. Use exactly 36 plus E=39, genus 3 and the exact S5 check. Two thousand 60-second calls cost up to 33.3 core-hours before controls, so first pilot a much smaller panel. |
| Medium: `ideas/I-261103-03-interval-branch-and-bound-c3-ansatz.md:17` | A compact projective box covering every proper-C3 realization has not been supplied. Exhausting a chosen box excludes only that box, including its stated chart and boundary treatment. Do not call this a complete symmetric decision without a coverage proof. |
| Low: `experiments/E-261103-07-s5-10-4-census-symmetry/README.md:36`; `ideas/I-261030-31-n8-exact-omsat.md:12` | The stretch stopping rule still asks for an already completed census, and the n=8 idea remains open after its decision. Consume these subquestions; retain geometric-symmetry analysis and proof review only. |
| Low: `ROADMAP.md:166` | The (8,2) 0/1/0 row is explicitly conditional, which is essential. Keep that condition inseparable from the numbers; it is not certainty in the census/encoder or an independently reviewed theorem. |

**Follow-up chains to stop.** No longer (8,2) search or symmetry run; no repeated census; no
S0 alternation-cap, adaptive-seed, normals-first or archive-width campaign without a focus-changing
question. Do not build a nonuniform fixed-face encoder merely to get a symmetry label when plain
formulas answer the focus question. No generic realizability package before the first target model
identifies the actual bottleneck. E-261103-03 gets a follow-up because moving to ten elements tests
a new decision, not because the previous short run left spare budget.

## 9. Scenario credences and reversal conditions

These are subjective planning weights, not measured probabilities or evidence levels. Keep the
current values rather than assigning a cross-genus likelihood ratio without data:

| Case / scenario | Proposed values | Reason |
|---|---|---|
| S5 (8,2), conditional on coverage and necessary encoding/general-position arguments | exists 0 / does not exist 1 / cannot tell 0 | EXACT plain refutations close this conditional branch. Confidence in the arguments themselves is a separate review question. |
| S5 (9,3) | 0.40 / 0.35 / 0.25, unchanged | No target formula solved; cheaper validated tools improve operational readiness, while the ten-element SAT/realization cost is unmeasured. |
| S5 (10,4) | 0.30 / 0.30 / 0.40, unchanged | EXACT census is larger than the former sample; no geometry or runtime evidence at this size. |
| S0 A/B/C | 0.20 / 0.55 / 0.25, unchanged | No new S0 full formula decision or transferable obstruction. The (8,2) result is not one. |

The S5 columns mix mathematical existence with whether our tools decide it in the planning horizon;
retain them only as coarse planning scenarios. Do not interpret them as an exhaustive partition of
mathematical truth. In particular, two known (8,3) witnesses among many abstract maps do not measure
the fraction of realizable maps; most maps have never been tested.

What changes the strategy: an exact S5 (9,3) witness leads to stretch construction; all 203 plain
maps excluded with the stated coverage/soundness chain motivates a reviewed nonexistence note and
owner decision on (10,4); persistent full-formula timeouts after the bounded grid shift effort to
one new exact relaxation or constructive pilot; a target SAT model that cannot be realized or
certified shifts effort to its realization problem. A proven reusable obstruction can change S0
priorities. A control disagreement suspends dependent interpretation, irrespective of sunk time.

## 10. Three things to do first

1. Approve the bounded E-261103-03 pilot in section 4 and apply its claim-boundary corrections in a
   working session; commit the amended PLAN before any target computation.
2. Run that pilot with paired scopes and exact evidence retention; route the first SAT immediately
   to its bounded realization check, otherwise report the plain completion fraction and hard tail.
3. Spend the next explore slot on E-261103-05's known-object controls, while preparing the small
   census/encoding review packet for an external human. No automatic target night or message send.

## Appendix: verification and limits of this review

At the evidence cut, activated `~/.venvs/polyhedra` and ran
`PYTHONDONTWRITEBYTECODE=1 python3 research/12-faced-polyhedron/verification/verify_all.py --quick`
from the repository root: **18 PASS, archive SKIP, ALL PASS**. The external `~/bin/drat-trim`
binary is present; the saved-evidence test therefore performed fresh proof checks, not just
hash/transcript fallback. The suite rebuilt the four (8,2) formulas and freshly exhausted the
(9,3) combinatorial census. It did not solve a (9,3) target formula or rerun all 3000 encoder
perturbations. No new candidate was produced; candidate-check was not applicable.

Read-only JSON checks selected the stated panel and confirmed C3 indices 0-7, involution indices
0,1,8-29, intersection {0,1}, and the six extra-degree patterns. These are inventory checks on
the EXACT census data, not new geometry. Source inspection and document arithmetic support the
audit, not an external second implementation. The report inventory check initially caught two
incorrect audit references (an abbreviated SOUNDNESS path and an out-of-range STATUS line); both
were corrected before final validation. A hypothesis-path lookup also failed, then was resolved
from the graph; no evidence check failed.

No long runs, external messages, push, PR, archive recheck or GitHub CI. All recommendations above
remain unapplied outside reviews/. Post-edit validation is recorded below.

Post-edit verification: the same quick command returned **18 PASS, archive SKIP, ALL PASS**
(exit 0), again with fresh external DRAT replay. Report checks passed: all 144 graph candidates
appear exactly once with five scores in range 0-2; all candidate links and explicit file:line
references resolve; ten verdict entries; English-only text; six-column score tables; whitespace
check clean. The working-tree scope check found this report as the only changed/untracked file.
No scientific evidence or ledger file was changed; the report is committed on the current
experiment branch without a push. The next session starts from section 10 after owner approval.
