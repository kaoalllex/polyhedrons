# Scientific audit 2026-10-31: status of every direction, foundations, and the recommended path


> **Status: unreviewed draft** written by an AI session on 2026-10-31 in a side worktree (branch
> `audit/night4`, base `7194400`) while night 5 was still running; imported 2026-11-01 without edits.
> Section 2 numbers are partial - final numbers: `NIGHT_REPORT_2026-11-01.md`. Its recommendations were
> merged with the external audit v3 into `STATUS.md` and `ROADMAP.md`.


Audience: the next AI session (or human) continuing this project. Read this file first, then
`METHODS_PROTOCOL.md`, `results.md`, `reviews/review-2026-10-30.md`. Everything below was checked
against the repository state at commit `7194400` plus the unanalysed night-4/5 results
(`overnight/results/arch`, `gate`, `n5`), which this audit analysed for the first time (section 2).

Labels: **CERTIFIED** (SAT proofs checked by drat-trim), **PROVED** (written proof, reviewed by at
least one independent reviewer), **PROVED-1** (written proof, one author, unreviewed),
**EXACT** (exact arithmetic, reproducible), **NUMERICAL**, **CLAIMED** (third party, unverified here).

## 0. One-paragraph state

Target: an embedded polyhedron with 12 planar simple 11-gons, every two faces sharing exactly one
edge, 3 faces per vertex (V 44, E 66, genus 6). Combinatorics is finished: 59 dual types, all with
small automorphism groups (39 trivial). Impossibility side: no symmetric realization exists, even as a
polyhedral immersion (25/25 cases, CERTIFIED). Every necessary condition found so far is satisfied by
"admissible normal sets" that are easy to produce, yet no admissible normal set has ever admitted
offsets (about 1,300 exact UNSAT decisions over nights 2 and 5). Construction side: the best exactly
verified object has genus 3 (48 of 66 adjacent pairs); more than 160 such realizations exist for four
types; not one genus-4 step succeeded in three nights (about 70 core-hours). The full asymmetric exact
decision (oriented-matroid SAT per type) has never been run; a third party estimates it at about
19,000 core-hours for all 59 types.

## 1. Ledger of directions

Verdicts: **FOUNDATION** (rely on it), **PROMISING** (worth the next compute), **OPEN-LOW** (not
refuted, low expected value), **DEAD** (do not repeat; the evidence is listed).

| # | Direction | Evidence (where) | Verdict |
|---|---|---|---|
| 1 | Face-plane formulation; openness of the realization space; general position WLOG; Lemma 5.1 (embedding = 176 forbidden-triple conditions on the chirotope of 12 planes + plane at infinity) | `mathematical-model.md`; adversarial review ACCEPT (`verification/foundations-report.md`); fresh-eyes review 1.3 | FOUNDATION (PROVED) |
| 2 | 59 combinatorial types, automorphism groups, orbit data | two independent enumerators, bijection with HackerPoet and Lutz lists, group orders match Ellingham-Stephens as relayed (`results.md` Track 2) | FOUNDATION (EXACT) |
| 3 | OM-SAT encoder (GP, triples, REFLEX1, POC, symmetry, normalisations) | 0 mismatches in 2.5 M predicate evaluations against exact geometry; Szilassi controls; cross-check with Track 4 (`results.md` Track 3) | FOUNDATION with one caveat: a single encoder; the immersion families have no second implementation |
| 4 | No symmetric embedding (C2, C3 classes, hence all groups) | 25/25 UNSAT-VERIFIED, drat-trim, user's machine (`overnight/results/sym`) | FOUNDATION (CERTIFIED); independent reproduction of Moki & Julio 2026 |
| 5 | No symmetric polyhedral immersion (no global clauses) | 25/25 UNSAT-VERIFIED (`overnight/results/symimm`) | FOUNDATION (CERTIFIED); new, write-up pending (`proof-no-symmetric-immersion/`) |
| 6 | Gauss-map degree theorem (degree 1 - g in the gauge, positive covering, >= 2g+1 saddles); local lemma; face-winding identity; parity theorem; handle decomposition D_{M+tau} = D_M + k_tau | `theory-notes.md` 2.1 + PI addendum; fresh-eyes 1.1, 2.1, 2.2; review 2026-10-30 2.1(3); controls: tetrahedron, cube, Szilassi, Roest-Vigh, 150+ genus-2/3 realizations | FOUNDATION (PROVED; the degree statement is a polyhedral form of Hopf / Gauss-Bonnet, the exact normal-only filter is this project's) |
| 7 | Fixed normals make all conditions linear in the offsets; exact SMT/LP decides a normal set in seconds to minutes | `theory-notes.md` 3.1; `fixed_normals_gauge.py`, `normals_first.py`; positive controls SAT, exact re-check | FOUNDATION (PROVED + EXACT) |
| 8 | Fixed-normal obstruction is cohomological (36 handle periods), and face simplicity is an independent strong obstruction (T^3 relaxation) | fresh-eyes 2.3; `period_defect.py`, `torus_simple`; night 2: 9 zero-defect normal sets, all need >= 11 non-simple faces | FOUNDATION (NUMERICAL, consistent across ~180 instances) |
| 9 | Exact rational verifiers (`ladder_exact`, `planes.check_embedding`, `verify_solid`) | caught 4 optimizer exploits; positive controls Szilassi, Roest-Vigh, Mizhaev; the 2026-10-30 review re-ran them | FOUNDATION (EXACT) |
| 10 | All 1005 known near-misses (HackerPoet) have the wrong Gauss degree and are not immersions (>= 7 locally overlapping vertices each) | `results.md` PI sections; exact per instance | FOUNDATION (EXACT); shareable (section 3) |
| 11 | Realization data: 162 exact genus-2/3 polyhedra of 30 types (archive), Roest-Vigh and Mizhaev controls, chain-consistent normals for type 58 | `overnight/results/arch/archive.json`, `experiments/` | FOUNDATION as a dataset; no further climbing (see 14) |
| 12 | Exact decision of the asymmetric case (OM-SAT per type, cube-and-conquer, proofs) | never run here; `immersion` 8/8 timeouts at 2.2 h; third-party pilot 2 maps in 648 core-hours (CLAIMED) | **PROMISING, top priority** (section 5) |
| 13 | Rank-3 (normals-only) SAT per type with degree, covering, saddle and face-winding clauses | proposed by review 2026-10-30 direction 6; not run | **PROMISING**: cheap first step of 12 |
| 14 | Genus ladder, branching ladder, realization archive + bandit, solid-first exact inner step | genus 3 for types 0, 15, 39, 53 (160+ realizations); genus 4: best 4 events on 5 arms (night 4), 0 realizations; type 0 genus 4 is a proved class obstruction (review 2.1) | DEAD for the strict target (robust plateau, 3 nights); keep the data |
| 15 | Normals first + exact offsets; k-targeted drift (night 5) | 1,138 decided normal sets: 0 SAT; kdrift reaches the class only on its wall (margin -0.0000) in 11/15 arms; positive control SAT only at radius 0.05 | DEAD as a climbing engine; its UNSAT statistics are evidence (section 4) |
| 16 | Closure-first (`pdefect`, `sdefect`, T^3 relaxation) | 9 zero defects, all false; simplicity must fail on >= 11 faces | DEAD |
| 17 | Improving near-misses (exact single-plane relocation, ILS, polar duals, dual-mesh planes) | plateau moves only; wrong topological class (10) | DEAD |
| 18 | Black-box engines on the unchanged energy (SA, CMA-ES, GA, ILS, NGOpt, DE, depth weights, floors, LNS) | all solve n = 7; none breaks n = 8 (1-2) or genus 4 | DEAD (advisor and review stop list) |
| 19 | Gauss clauses as SAT speed-up (G4); kappa-CSP prefilter (Q14); symmetric plane sets with asymmetric maps (Q15); screw orbits (Q16); smooth-surface tangent planes (Q13); Szilassi embryo (M1) | sprint board | DEAD |
| 20 | n = 8 genus-2 rung (two doubled adjacencies) as benchmark | plateau 1, not degenerate; advisor: poor analogue | DEAD as benchmark; its existence question is OPEN-LOW (9-element OM-SAT would settle it) |
| 21 | Relaxed 12-face target: all pairs adjacent, d = 6 or 12 pairs doubled (genus 7 / 8), symmetric two-orbit ansatz (Roest-Vigh style) + exact inner solid solver (L1, L2) | not started; the only existing 8-face objects are of this kind, both symmetric | **PROMISING** as the constructive line (section 5.2) |
| 22 | Chain-consistent normals (Q1), projective ladder (P1), flips through degeneration (Q3), spine-seeded solids | Q1: normals found for type 58, sphere level UNSAT; others untested | OPEN-LOW |
| 23 | Farkas certificate mining of the period obstruction (human proof route) | proposed (fresh-eyes 4), not run | OPEN-LOW, cheap; run only on the side of 12/13 |
| 24 | Full write-up of the certified theorem (5), with a second independent encoder | `proof-no-symmetric-immersion/README.md` plan | **PROMISING**: the only result ready to share |

## 2. What nights 4 and 5 showed (analysed here for the first time)

Night 4, job `arch` (375 tasks, 24 core-hours; `overnight/results/arch/`):

| Item | Value |
|---|---|
| new exact realizations | 154 (type 15 genus 3: 43; type 53 genus 3: 42; 17 types at genus 2) |
| genus-3 arm tasks | 273, best event count 0 (types 15, 53), median 1-2 elsewhere |
| genus-4 arm tasks | 5 (types 39, 53), best 4.0 events, no realization |
| archive at the end | 162 realizations, 956 arms |

Night 5, jobs `gate` and `n5` (`overnight/results/gate`, `n5`; `analyze_n5.py` output):

| Item | Value |
|---|---|
| gated realizations | 156 (30 types); own Gauss degree = 1 - g on every one (theorem confirmed 156 times) |
| type 0 genus-3 arms | 18, T1 pass 0, k_tau = 0 on all (review confirmed) |
| other types, genus-2 arms | most pass T1; k_tau = -1 on 54 arms (the next map is in class at the seed) |
| test 2.2 (night-3 chains) | 352 of 378 failed levels out of their Gauss class (93 %), 26 in class |
| n5 tasks | 33, all NOT_REALIZED |
| decided normal sets | g6: 158 UNSAT, 19 gate-failed; kdrift: 566 UNSAT, 22 no admissible normals; nfirst: 408 UNSAT, 166 no admissible normals; z3 median 9-16 s |
| kdrift | 11 of 15 arms reach k_tau = -1, every one with hemisphere margin -0.0000 (on the class wall) |

Reading. (a) The Gauss class explains the type-0 genus-4 plateau and 93 % of failed ladder levels,
but in-class arms (k_tau = -1) of other types also fail: 566 + 408 exact UNSATs at radii 0.02-0.2
around in-class seeds, against a single positive control that is SAT at radius 0.05. So the Gauss
class is necessary but far from sufficient; an unexplained obstruction sits between genus 2 and 4.
(b) Genus 3 is reachable for at least four types and is reproducible (dozens of distinct oriented
matroids), genus 4 never: the constructive plateau is robust against engines, seeds, types and the
class-aware tools. (c) `arch`, `glad`, `n5` should not be run again on the strict target.

## 3. Results worth sharing with the community (ranked)

1. **Theorem (computer-assisted, CERTIFIED): no polyhedral immersion in R^3 with planar faces of any
   of the 59 twelve-face Series-1 maps has a non-trivial symmetry.** Strengthens the embedding
   statement of Moki & Julio 2026 (which it also reproduces independently with a different clause form)
   and is new as far as the project knows. Needs before sharing: second independent encoder of the
   local families on the 25 instances (plan in `proof-no-symmetric-immersion/README.md`), written
   soundness proofs of REFLEX1 / POC / SIMPLE / SYM, LRAT or drat-trim logs with CNF hashes, 4-6 pages.
   Audience: J. Bokowski, the szilassi-12 authors, arXiv math.MG/math.CO.
2. **Diagnostic note: the known numerical near-misses are topologically far from solutions.** Every
   one of the 1005 HackerPoet configurations has Gauss degree in -5..+4 (mostly -1..+1, target -5) and
   >= 7 vertices with two reflex corners; the triple-point count used by all prior searches hides this.
   Together with the exact normal-only filter (degree, covering, saddle count, face-winding identity
   r_X = sigma_X + 2 w_X - 2) this is a short, useful note for anyone optimising such polyhedra, and it
   explains why GPU searches plateau at 4-5 violations. Ready to write (2-3 pages); exact per instance.
3. **Structural fact: for fixed admissible normals the obstruction is cohomological** (face closures
   are satisfiable, the 36 handle periods are not; simplicity is an independent second wall;
   Wendel-type heuristic 1.6e-10 for a random 9-dimensional offset image to meet an orthant). NUMERICAL
   on ~200 normal sets of several types; shareable as an observation, not a theorem.
4. **Tooling that others can reuse**: exact rational verifier for face-neighbourly polyhedra with
   doubled adjacencies (validated on Szilassi, Roest-Vigh, Mizhaev), the exact-inner solid-first engine
   (rediscovers Szilassi from random planes without a map), the 162-realization dataset of partial
   polyhedra, the enumeration code with checker. Worth a repository release with a README; not a paper.

Not shareable as results: genus-3 partial polyhedra (no known question they answer), the ladder
plateau, and all KILL verdicts (internal negative results; keep them in the repository).

## 4. Progress assessment: barrier or progress?

Progress is real on the impossibility and understanding side (items 1-10 of the ledger, two
certified theorems, a correct diagnosis of why every heuristic plateaus). On the construction side
the project has hit a barrier: genus 3 since 2026-10-30 morning, unchanged after three nights and ten
engines, and the class-aware tools built after the review produced 0 SAT in 1,138 exact decisions.

Evidence summary for the existence question (all pointing the same way, none decisive):

* vertex version impossible (Schewe 2010, CLAIMED but published and reproduced by third parties);
* every symmetric case impossible even as an immersion (CERTIFIED);
* three independent numerical searches (CodeParade/Bokowski-H., Moki & Julio GPU, this project)
  converge to configurations in the wrong topological class;
* every admissible normal set tested so far is exactly UNSAT for the offsets (~1,300 decisions);
* the constructive ladder stalls at genus 3 for every type and every realization.

Honest reading: the prior for existence has dropped (this auditor's estimate: 20-30 %), but no
asymmetric type has been excluded, so the question is open in both directions. In this regime more
heuristic search has low expected value, while an exact decision has high value either way: UNSAT for
all 59 types is a theorem of the same kind and standing as Schewe 2010; SAT for a type gives a
concrete chirotope to realize, a far better-posed problem than blind search.

## 5. Recommendation: direction and method for the next sessions

### 5.1 Main line: exact decision per type, "normals first" done exhaustively (cube-and-conquer on the rank-3 contraction), with certificates

Why this and why now:
* The whole obstruction found so far lives in the rank-3 contraction chi(.,.,.,inf), i.e. the oriented
  matroid of the 12 normals: degree, covering, saddle count, face-winding, kappa-CSP all constrain it
  (`theory-notes.md` 0, fresh-eyes 2.1). Fixed normals make the rest an exact linear problem decided in
  10-90 s. So the natural split of the SAT search space is: outer = rank-3 chirotope of the normals,
  inner = rank-4 extension (the offsets' signs). This is the project's own "normals first" insight
  turned into an exhaustive, certified procedure instead of a sampled one.
* Compute is affordable, contrary to the project's working assumption. The third-party pilot gives
  about 324 core-hours per map with a 5,257-variable encoding and no orientation clauses; the project's
  own REFLEX1 + POC clauses gave 2.7-10x on symmetric instances. Even at 19,000 core-hours the campaign
  is 4-5 days on a single 192-vCPU cloud instance (the owner's organisation uses AWS and GCP; price it
  before deciding, spot prices are typically in the range of a few hundred USD for that volume). On the
  laptop (11 workers) it is about 70 days, so the laptop is for pilots only.
* Reference points from the SAT-in-mathematics literature: Schewe's 59 vertex instances take minutes
  each; the large certified campaigns (Boolean Pythagorean triples, Schur 5, Keller 7) ran from tens of
  thousands of core-hours down to hours once the encoding and the cubing variables were right. The
  lesson from all of them: encoding and splitting heuristics, not raw compute, decide feasibility.

Protocol (each step has a stop rule; record every run in `experiment-log.md`):

E1. **Rank-3 instance per type** (1 day of coding, minutes of solving). Variables: the 220 signs
    chi(X,Y,Z,inf) in the gauge W = +1 (mirror fixed), the 66 kappa bits, the 44 vertex-type bits.
    Clauses: rank-3 three-term Grassmann-Pluecker on 12 elements; DEG_W (degree -5 at every -N_W),
    COV_W, CNT >= 13; the vertex rule F3/F4 and the face-turning table F6; the face-winding identity
    with w_X <= 1 and 0 <= r_X <= 8. Controls: Szilassi normals (n = 7, target 0) SAT; the 156 realized
    polyhedra's normals SAT for their sub-maps (target 1 - g); random normal sets mostly UNSAT.
    Outcomes: UNSAT for a type = a short, human-checkable impossibility proof for that type (unlikely
    but decisive); SAT = go to E2.
E2. **Count and sample rank-3 solutions per type** (ApproxMC or blocking-clause enumeration with a
    cap of 10^6). For a sample of 200 solutions test stretchability numerically (fit 12 normals to the
    220 signs by hinge loss; 24 parameters, seconds). Record the realizable fraction. Stop rule: if
    fewer than 10^7 solutions per type and most are realizable, cube on them (E3); if the count is
    astronomically large, use the rank-3 variables only as the splitting heuristic in E3.
E3. **Cube-and-conquer pilot on 3 types** (one trivial-Aut type, type 0, type 58), one night on the
    laptop (about 90 core-hours). Cubes = partial assignments of the rank-3 variables (lookahead on the
    220 variables only; fall back to the existing `job_cube` splitting with `order` restricted to the
    rank-3 variables, which is a small change in `run_overnight.py`), inner solver CaDiCaL with REFLEX1,
    POC, triples, GP, symmetry breaking; DRAT per cube, checked by drat-trim in a second pass. Metric:
    refuted fraction per core-hour, extrapolated time per type. Compare with the plain run of
    `job_cube` on the same type. Stop rule: if the extrapolation is below 2,000 core-hours per type, go
    to E5; otherwise improve the encoding (E4) first.
E4. **Encoding comparison** (1 day). Build the third-party encoding (pirozhkov, 5,257 vars / 52,177
    clauses per map, cube-and-conquer with cake_lpr) and the project's encoding on the same four
    symmetric instances; measure conflicts and time; port whatever is faster. Add the rank-3
    realizability check as a cube filter only where it is certified (LP-provable non-stretchability);
    otherwise solve the cube.
E5. **Campaign**: cloud instance, all 59 types, cubes in a queue with checkpoints (the existing
    `state.json` design), DRAT proofs streamed to storage, hashes of CNFs recorded, two independent
    encoders agreeing on every UNSAT type before it is declared excluded. Order the types by E3 cost,
    easiest first, so partial results (excluded types) accrue early.
E6. **If a type is SAT**: the model is a uniform rank-4 chirotope on 13 elements satisfying every
    embedding predicate. Realize it: maximise the minimum signed 4x4 determinant margin over the 36
    plane parameters (smooth, well-conditioned; review 2026-10-30 direction 9), seeded from normals that
    fit its rank-3 contraction. Success = planes, then `planes.check_embedding` exactly = the polyhedron.
    Failure = try a biquadratic final polynomial (LP) for non-realizability; add it as a blocking clause
    and continue (CEGAR). Realizability is a separate, well-studied problem; budget it separately.

What counts as done: every type either CERTIFIED UNSAT (two encoders, checked proofs) or realized
exactly. Either outcome is publishable; intermediate outcome (k of 59 types excluded) is also a
reportable partial theorem.

### 5.2 Second line (constructive, cheap, publishable on its own): the relaxed 12-face target

The only known closed polyhedra with 8 mutually adjacent faces have doubled collinear adjacencies and a
symmetry group (Mizhaev C4-rotoreflection, Roest-Vigh D2). The analogous 12-face object (all 66 pairs
adjacent, d = 6 or 12 pairs doubled, genus 7 or 8) is not excluded by anything in this project, is not
in the literature, and has a 12- or 8-parameter symmetric ansatz (3 or 2 orbit representatives).
Protocol: (1) calibration: `solid_cpsat.py` with "<= 2 collinear edge runs per pair" must rediscover
Roest-Vigh's polyhedron from random D2 two-orbit planes (rate per CPU-hour is the engine's score); (2)
the same engine on 12 planes = 3 orbits of D2 / C4 / S4, objective = adjacent pairs, exact verification
with `ladder_exact` (doubled links supported). Budget: two nights. Stop rule: if calibration fails,
fix the engine, do not run n = 12. Success is a new object worth a short paper; failure is a clean
negative benchmark. Keep this line small (<= 25 % of compute).

### 5.3 Third line: finish and share what is ready

Write up item 1 of section 3 (certified theorem) and item 2 (diagnostic note) now, before new compute:
they are the project's only shareable scientific products, and writing them forces the second encoder
(E4 reuses it). Target: arXiv-ready drafts in `proof-no-symmetric-immersion/`, reviewed by the
adversarial-verifier agent, then sent to Bokowski and to the szilassi-12 authors for comment.

### 5.4 Stop list (do not spend compute on these again for the strict target)

Genus ladder / arch / glad / n5 / kdrift / normals-first climbing; pdefect / sdefect; black-box
engines on the pair energy; near-miss repair; Gauss clauses as SAT speed-up; asymmetric immersion
instances without cubing (subsumed by 5.1).

## 6. Method: how to run this project like a research group

What the project already does well: a claims ledger with evidence labels (`results.md`), append-only
experiment log, exact verification of every candidate, hashes of CNFs and proofs, independent
reviews, positive and negative controls, "kill fast" sprint board. Gaps, with the fix:

1. **Underpowered KILL verdicts.** Many KILLs rest on 8-30 minute runs with one seed. Keep the
   verdict scale but add a power statement to each test (budget, number of seeds, what effect size
   it could have detected) and allow "KILL at this budget". The ladder's genus-3 realizations needed
   8-15 attempts of 15 min; a single 8-min run would have killed it.
2. **One metric, named.** The 2026-10-30 review found three incompatible violation counts (events,
   exact defects, class defects). Every table must name its counter; the exact-defect count of
   `ladder_exact` is the only one allowed in claims.
3. **Pre-registered stop rules.** Nights 3-5 ran exploratory jobs without a rule for when to stop
   climbing; section 5 attaches a stop rule to every step. Decide before the run what result changes
   the plan.
4. **Independent re-implementation before any theorem is announced.** The certified results rest on
   one encoder; bbchallenge-style practice is two independent deciders plus a formally verified
   checker. E4 and the write-up supply the second encoder; use cake_lpr (LRAT) if drat-trim is not
   accepted by reviewers.
5. **Documentation hygiene.** Twenty-four markdown files, several stale (`hypotheses.md`,
   `next-steps.md`, `open-questions.md`, `research-plan.md`, `solution-portrait.md` row 2 and 7 are
   outdated). Move stale files to `archive/` and keep four living documents: this ledger (status),
   `results.md` (evidence), `experiment-log.md` (append-only), `CONTINUE_PROMPT.md` (hand-over).
6. **Data as a product.** The 162 realizations, the 1,005 imported seeds with exact invariants, the
   59 types with invariants, and the 25 CNF/proof hashes are reusable datasets; give each a README and a
   schema (as `data/README.md` already does for the enumeration).
7. **Compute planning by cost.** Keep a table core-hours spent per direction versus information gained
   (nights 3-5: about 100 core-hours, result: 160 realizations and a confirmed plateau). The exact
   campaign is the first item whose cost is known in advance; budget it explicitly.
8. **Literature discipline.** No primary paper has been read in full (network limits); every citation
   in the write-ups must be checked against the primary text before submission. Section 7 lists what
   the literature agent could verify on 2026-10-31.

## 7. Literature and world practice check (2026-10-31)

See the appendix below (filled from the literature agent's report of the same day; each item is marked
VERIFIED / REPORTED / NOT FOUND by that agent).

## 8. Risks and open questions

* The OM-level problem may be SAT for many types while no realization exists (Mnev universality
  warns that realization spaces can be arbitrarily bad). Then E6 becomes the bottleneck; final
  polynomials do not always exist. Mitigation: E2's realizable fraction gives early warning.
* The third-party 324 core-hours per map is an extrapolation from two maps with a different encoding;
  hardness varies by type. E3 measures it before the campaign is bought.
* The encoder is the trust point of every CERTIFIED claim (DRAT certifies the CNF only). E4 is not
  optional.
* The relaxed target (5.2) might be excluded by a symmetric UNSAT too; run the 9-element and
  13-element symmetric instances for the doubled maps before heavy numerical search.
* Unexplained: why in-class genus-2 seeds are UNSAT for genus 3 at every radius (night 5). A single
  Farkas-certificate study (ledger 23) on 20 of those UNSAT instances might expose the mechanism; cheap,
  do it on the side.

## 9. Краткое резюме для владельца (Russian summary)

* **Что надёжно (фундамент).** Формулировка через 12 плоскостей и лемма 5.1 (проверены
  противником); ровно 59 типов (две независимые переборки); кодировщик OM-SAT (0 расхождений на
  2.5 млн предикатов); две сертифицированные теоремы: нет симметричного вложения и нет даже
  симметричной полиэдральной иммерсии (25/25, DRAT проверены); теорема о степени отображения Гаусса и
  тождество о числе рефлексных углов; точная линейность задачи при фиксированных нормалях; точные
  верификаторы (поймали 4 обмана оптимизаторов); все 1005 известных «почти решений» топологически
  неверны.
* **Что тупик.** Лестница по роду (ночи 3-5): род 3 достигнут для 4 типов 160+ раз, род 4 ни разу;
  «сначала нормали» дало 0 SAT из 1138 точных решений; closure-first, улучшение почти-решений, все
  чёрные ящики, симметричные анзацы для строгой цели.
* **Прогресс или барьер.** На стороне невозможности и понимания прогресс есть; конструктивная
  сторона упёрлась в устойчивый барьер (род 3). Оценка шансов существования упала до 20-30 %, но ни
  один асимметричный тип не исключён.
* **Что делиться.** (1) Сертифицированная теорема о симметричных иммерсиях (нужен второй независимый
  кодировщик и текст 4-6 страниц). (2) Заметка: известные почти-решения не являются даже иммерсиями и
  имеют неверную степень Гаусса; точный фильтр по нормалям. (3) Наблюдение о когомологической природе
  препятствия при фиксированных нормалях. (4) Инструменты и датасет.
* **Куда копать и как.** Главная линия: точное решение для каждого из 59 типов методом
  cube-and-conquer с расщеплением по 220 знакам ранга 3 (хиротоп нормалей), с DRAT/LRAT
  сертификатами и двумя кодировщиками; пилот на ноутбуке (E1-E3), затем облако (оценка ~19 000
  core-часов до улучшений, то есть несколько дней на одной большой машине). Любой исход публикуем:
  UNSAT по всем типам = теорема уровня Schewe 2010; SAT = конкретный хиротоп для реализации. Вторая
  линия (<= 25 % ресурсов): ослабленная цель с удвоенными парами (род 7/8) и симметричным анзацем
  после калибровки на многограннике Рёста-Вига. Третья: дописать и разослать готовые результаты.
