# Roadmap: the experiment queue

**Focus since 2026-11-08** (`STRATEGY.md`): the focus target is S5 at (10, 4), gated by a speed-up benchmark; the
(8, 2) / (9, 3) negative result is a side track towards a note; S0 is parked, not abandoned. From 2026-11-03 to
2026-11-08 the focus was (9, 3), now decided (STATUS 3d). The S5 queue below was proposed by `reviews/strategy-review-2026-11-03.md` and approved by the owner on
2026-11-03; the S0 queue follows it, parked as it stood.

As of 2026-11-07. Principle: **theory and a cheap filter first -> a discriminating experiment -> an exact
solver -> a lemma or a certificate**. We do not try to enumerate the search space; we pick small, motivated
regions where one experiment can exclude a whole class or reveal a new constraint. How to run an item:
`PROTOCOL.md`. Current state: `STATUS.md`.

## Scoring (pre-registration)

Each item is scored 0-2 on: **T** theoretical motivation, **D** discriminating power (do different outcomes
change the plan?), **F** cheap falsification test exists, **G** generalisation potential (a lemma for many
types?), **R** reproducibility (exact, archivable). Do not run anything with T + D < 3, however easy to
parallelise. Every item's `PLAN.md` states what SAT / UNSAT / timeout / near-miss would mean **before** it runs.

## Phase 0 - foundations of the workflow (done 2026-11-01 unless marked)

* `SPEC.md` frozen; evidence labels and counters normalised.
* `verification/verify_all.py` (one command, 14 checks) and `verify_candidate.py` (any file format, `--target S0` = the solution check); CI on every push.
* `requirements.txt` pinned; hard-coded `/home/user` paths removed.
* Experiment template and GitHub Actions runner (`experiments/_template/`, `.github/workflows/experiment.yml`).
* DRAT certificates of `sym` / `symimm`: the night runs had deleted them after checking (no `--keep-proofs`).
  Regenerated 2026-11-01 with `--keep-proofs --keep-cnf`: all 50 CNFs and all 50 proofs are bit-identical to the
  SHA-256 recorded in the `results/{sym,symimm}/results.jsonl` of E-261029-13 and E-261029-15, 50/50 re-VERIFIED by drat-trim. Packed as
  `symmetric-{sym,symimm}-drat.tar.xz` (422 MB, 438 MB) and published on the GitHub release `state-2026-11-01`;
  hashes, versions and how to check: `verification/certificates/symmetric_drat/`. TODO (owner): Zenodo DOI via
  the GitHub-Zenodo integration before any write-up.
* Declined by the owner on 2026-11-07 (kept for the record): e-mail to the author of `pirozhkov-andrei/polyhedraproof` (E-261101-11). Why: he reduced exactly
  our problem to 59 SAT formulas independently and asks for collaborators; two encoders that agree predicate by
  predicate on random exact configurations are the cheapest strong evidence for the soundness of FD2/FD4 (today
  PROVED-1 by AI sessions); his two refuted formulas, if their certificates are shared, exclude two types for us at
  no cost; a shared campaign halves the ~19,000 core-h; otherwise the impossibility side may be settled without
  us. Content: three shared symmetric instances with CNF hashes, the predicate-equality harness
  (`code/omsat_validate.py`), one question. Second contact: Roest and Vigh (Szeged), who found the 8-face objects
  with an AI-assisted search and say the 12-face case is open.
* Tag `state-2026-11-01` = `main` after merging this restructure; witnesses and site lab models (`witnesses/`).
* Research graph: one file per idea / hypothesis / experiment with dated IDs (`PROTOCOL.md` §4), past work
  reconstructed as experiments with their data, `verification/trace.py` (in `verify_all`), interactive `map/`.
* TODO (infrastructure, from the 2026-11-01 process audit; each passes the infrastructure filter of `PROTOCOL.md` §3):
  * `lint_docs.py` in `verify_all`: STATUS levels are SPEC labels, ROADMAP rows have T + D >= 3, every backticked
    path in the control documents exists; `experiment.yml` accepts only `E-YYMMDD-NN` ids.
  * `verify_all` runs the verifier's mutation tests (`verification/test_mutants.py`) and re-encodes 2-3 symmetric
    instances to compare their CNF SHA-256 with the certificate records (proves HEAD still builds the certified
    formulas).
  * READMEs link to `STATUS.md` instead of repeating numbers.
  * Pilot the GitHub Actions runner before relying on it. Owner approved an Actions trial on 2026-11-08: the
    calibration wave on known (9,3) maps (I-261108-07, lead review 2026-11-08d queue item 6).
  * `lint_docs.py` also checks that every new `PLAN.md` has the counter-calibration and scenario-move lines (template
    changed 2026-11-01 after `reviews/strategy-review-2026-11-01.md`).

## Week plan (lead review 2026-11-08d, `reviews/strategy-review-2026-11-08d.md`, amended in items 1, 2 and 5 by the second-lead review `reviews/strategy-review-2026-11-08e.md` and its follow-up; both approved by the owner on 2026-11-08; replaced by the next lead review)

Lab sessions take these in order (PROTOCOL.md §8b). Anything outside a follow-up tree goes to "For the lead".
Laptop: at most 10 cores in total; every splittable run uses 8-10 shards (owner, 2026-11-08). Items 1, 3, 4 and 5 need
no night; item 2 is one owner launch of at most 2 h wall. Aggregate core-hour caps override per-unit caps.

1. **Multiplicity >= 3 positive control** (audit, exploit; [I-261108-04](ideas/I-261108-04-grooved-box-multiplicity-control.md)). Question: does the
   E-261103-02 encoder accept a real embedded polyhedron in which one face pair shares three (and four) collinear
   segments? Object: a box with two (three) V-grooves cut from one edge, groove walls tilted to general position,
   exact rational planes, checked by `ladder_exact` / `verify_solid`. Test: its own map through the `submap=True`
   path, planes pinned: SAT required; the same planes on a map with one segment pairing swapped: UNSAT-VERIFIED
   required; also the unpinned formula if it has <= 13 elements (SAT required). The swapped map must itself be a valid
   map on which the exact geometry rejects the pinned planes; a loader rejection is not a negative control. If the
   quadrupled box does not fit the session, finish the tripled one and record the remaining coverage (review 08e §3).
   At most 1 session, < 0.1 core-h. Experiment: [E-261109-01](experiments/E-261109-01-grooved-box-multiplicity-control/), done 2026-11-09 (all pass).
   * Kill: none (a control). Follow-up tree:
     * all pass -> record the control (EXACT) in E-261103-02 and STATUS; items 2-4 proceed;
     * a pinned SAT fails -> stop all S5 compute; the 18 tripled-pair (9,3) UNSATs and the tripled (8,2) UNSAT are
       suspended; escalate (encoder bug hunt, at most 1 session, then the lead).
2. **(10,4) speed-up benchmark** (exploit; I-261031-02, I-261108-05; follow-up of E-261103-07; what differs from the parked plain run:
   solver and cubing; design of review 08e Follow-up Q1, except the variants). Question: is there a variant that makes
   the (10,4) plain formulas >= 10x cheaper, measured on (10,4) maps rather than inferred from (9,3)?
   * Variants: V1 = kissat (pinned build, DRAT output); V2 = cube-and-conquer (cubes on the segment-order variables of
     the multiple pairs, or march_cu; each cube solved by CaDiCaL; one DRAT per cube plus a checked cube-cover formula;
     core-seconds summed over cubes). If V2 cannot be built and checked within the prep session, V2 = CaDiCaL
     `--unsat`; no other substitution. Freeze binary hashes and versions. Baseline: the recorded default-CaDiCaL runs,
     as censored observations (no new baseline jobs).
   * Phase A (correctness screen, no speed threshold, <= 1 core-h aggregate): the six known-answer (9,3) maps (map 7 and
     one more `1^6`, maps 87 and 130 `(1^4,2)`, one `(1,1,2,2)/(2,2,2)`, one `(1,1,1,3)`) plus the SAT controls. A wrong
     model or a rejected proof rejects the variant; a timed-out unit is unresolved, not a failure.
   * Phase B (target): (10,4) maps 96 `(1^4,2)`, 85 `1^6`, 146 `(2,2,2)/(2,2,2)`, 845 `(1,2,3)` of
     `experiments/E-261103-01-s5-map-census/results/maps_10_4.json` (SHA-256 frozen in the PLAN); 4 maps x 2 variants,
     3600 s end-to-end per unit (solver <= 2400 s, the checker the rest). An unchecked UNSAT is censored.
   * Projection (a scenario that allocates risk, not a bound): strata A = `(1^4,2)` (N = 520), B = `1^6` (N = 237),
     C = all other patterns (N = 360, pooled as a working assumption). Per variant and stratum: n units, k checked
     decisions, p = k / n, mu = mean end-to-end time of the decided units (0 if k = 0), tau = 3600 s;
     B_h = N_h [p_h mu_h + (1 - p_h) tau] / 3600, R_h(lambda) = N_h (1 - p_h)(lambda - 1) tau / 3600,
     P(lambda) = 1.25 sum_h [B_h + R_h(lambda)] for lambda in {4, 16}; a stratum without units gives P = infinity.
     Report n, k, p, mu, every censored cap, and sum B separately.
   * Winner: at least as many checked decisions as the other variant in each slow stratum, smaller P(4), and >= 2x
     lower sum B; otherwise no winner. Holdout, winner only, from a 2 core-h reserve: maps 926, 852, 78, 1104 at 1800 s
     each, proof included; all four must be checked. The holdout tests the projection's optimism and is not pooled
     into it.
   * Budget: 1 prep session; one owner launch, 8-10 shards, <= 2 h wall, <= 12 core-h (Phase A 1, Phase B 8,
     holdout 2, overhead 1).
   * Follow-up tree (nothing starts without the owner):
     * a control fails -> reject that variant; no target decision -> park these variants, not the exact route; no
       winner -> no campaign, the comparison is inconclusive;
     * winner with P(4) <= 160 and P(16) <= 160 core-h and all four holdouts checked -> propose a capped two-night
       attempt (PLAN amendment: fast patterns first, first-SAT stop, controls in every shard, the item 1 control
       included), not a promised completion;
     * otherwise P(4) <= 1,000 -> Actions calibration on known-answer maps ([I-261108-07](ideas/I-261108-07-actions-calibration-wave.md), owner approved a trial); a
       campaign only after the measured runner cost and the owner's approval;
     * P(4) > 1,000 -> park this route at this budget; escalate;
     * any SAT -> first-SAT stop; exact model check, realizers, `verify_candidate.py --target S5`, `candidate-check`.
   * Owner 2026-11-08 21:30: [E-261108-03](experiments/E-261108-03-s5-10-4-speedup-benchmark/) tonight with V2 = CaDiCaL `--unsat` (cube-and-conquer a later separate launch), Phase A <= 1 core-h (caps 120/90 s), Phase B as above, holdout a separate short launch after the analysis, <= 10 core-h, 10 shards. Amended 22:20 (owner): no DRAT (UNSATs are `UNSAT-SOLVER`), solver caps 1800 s (A) / 14400 s (B), a default-CaDiCaL baseline on 96 and 85, <= 47 core-h, <= 5.1 h.
   * Done 2026-11-09 (E-261108-03, 8.59 core-h): kissat wins, decides 96, 85, 146, 845 in 189-2749 s (UNSAT-SOLVER); `--unsat` slower than default; best measured ratio 2.35x (no 10x); P(4) = P(16) = 475 core-h without DRAT -> Actions calibration (I-261108-07); holdout not run (needs P(4) <= 160); cube-and-conquer still open (STATUS 3x).
3. **Independent census of (8,2) and (9,3)** (audit; [I-261108-08](ideas/I-261108-08-independent-s5-census.md)). Question: does an independently written enumerator
   reproduce 2 classes at (8,2) and 240 classes / 203 admissible at (9,3), with the same canonical hashes? Method not
   shared with E-261103-01 (e.g. genus-g rotation systems of K_F plus the extra edges, by CP-SAT with canonical-form
   deduplication, or lexicographic surface enumeration). At most 2 sessions, minutes of CPU.
   * Done 2026-11-09 ([E-261109-02](experiments/E-261109-02-independent-census/), seconds of CPU): the growth enumerator gives 1 / 2 / 240 classes (203 admissible), identical canonical sets, automorphism orders and reflexibility to E-261103-01 at (7,1), (8,2), (9,3); (9,3) 120 s (STATUS 3z).
   * Kill: two sessions without a complete run -> record, escalate. Follow-up tree: agreement -> coverage evidence
     becomes two-algorithm EXACT (arguments still PROVED-1); any missing map -> its plain formula on one day run,
     10 shards; extra maps in the new enumerator -> bug hunt in one of the two, at most 1 session.
4. **Second encoder on six (9,3) maps** (audit; I-261031-03, review 2026-11-08c §7 idea 1). An encoder written
   from `theory/mathematical-model.md` Lemma 5.1 and the S5 definition, not from `pilot.build`; maps 40 (62 s), one
   of each of `(1,2,3)/(2,3)` and `(1,1,2,2)/(2,3)` (tripled pairs), one `(1^4,2)`, one `(1,1,1,3)`, one
   `(2,2,2)/(2,2,2)`; plus the pinned Roest-Vigh, Mizhaev and item 1 controls. At most 2 sessions + 1 core-h, 8 shards (owner rule 2026-11-08).
   * Kill: a disagreement on any instance -> stop, the (9,3) claim is suspended, escalate. Follow-up tree: agreement
     on all -> the claim's encoder caveat reads "two encoders agree on six maps and all controls".
5. **Union of two matched solids** (explore, jump; [I-261108-11](ideas/I-261108-11-union-of-matched-face-neighbourly-solids.md), stage 1; review 08e Follow-up Q5;
   owner 2026-11-08). Question: does the Boolean union of two exact known solids, matched on k face planes by a
   projective map, give a 10-face genus-4 boundary with many adjacent pairs? Sources: Szilassi + Szilassi, k = 4,
   three intersection balls (3 free parameters); Szilassi + tetrahedron, k = 1, four balls (12 parameters). Control
   first: the union of two identical Szilassi copies returns the Szilassi boundary exactly. Then 128 frozen samples per
   source (plane correspondences x rational parameters), poles off both solids; the union boundary exactly from the
   cells of the plane arrangement (reuse the solid-first `Arrangement` / `extract_map` code): genus, face components
   and holes, simple faces, adjacent pairs. At most 1 session + 1 core-h, 8 shards.
   * Kill: the control fails -> stop; no boundary with 10 simple faces and genus 4 in a source -> park that source at
     this resolution (a sampled negative, not an exclusion). Follow-up tree: such boundaries with missing pairs -> one
     separately registered continuous search for the better source; any boundary with all 45 pairs ->
     `verify_candidate.py --target S5`, `candidate-check`. Later stages (general genus-0 pieces, (9, 4), the rigid
     (9, 3) cross-check, the 12-face filter) are not this week: the lab writes the item 5 verdict to "For the lead"
     in `CONTINUE_PROMPT.md`, and the next lead review decides them.

Not in this week: the note package (lead review 2026-11-08d §5 item 8; owner 2026-11-08: a note is a goal and says
that no independent review took place), after items 1, 3, 4 pass. Its first step is the one-way soundness chain of
review 08e Follow-up Q3: an S5 uniformization lemma with multiple segments; geometry to the admissible exported map;
necessity of INCONS, RFCONS, REFLEX1 and POC for multiple boundary runs, with the Tseitin extension; the gauge units
and the census-to-CNF manifest for all 205 formulas. The note says "cubic" unless the optional perturbation lemma
[I-261108-09](ideas/I-261108-09-perturbation-lemma-non-cubic-vertices.md) (universal local test) closes the non-cubic scope of `STATUS.md` §4; [I-261108-10](ideas/I-261108-10-defect-bounded-boundary-census.md) is
its fallback. Also not in this week: the face-contraction sieve ([I-261108-06](ideas/I-261108-06-face-contraction-sieve.md); moved out by review 08e: when it
runs, a capped pilot of one session and <= 1 core-h with an aggregate stop, since the worst case of 203 x 9 x 20 s is
10.15 core-h; auxiliary-variable closure inspected first; zero on a subset parks that version only); E-261101-10 (S0 slot).

Previous week plan (lead review 2026-11-08, items 1-5) is done: literature check, (9,3) long-cap pilot, core study,
arrangement sweep, and item 5a, which decided all 203 admissible (9,3) plain formulas UNSAT-VERIFIED (STATUS 3d); the
E-261103-07 cost probe followed (STATUS 3w). Its text is in `reviews/strategy-review-2026-11-08.md` §2, `-08b`, `-08c` §2.

## Queue: focus target S5 (approved 2026-11-03)

Proposed by `reviews/strategy-review-2026-11-03.md` (sections 2-3) and approved by the owner on 2026-11-03. Order rule:
the combinatorics first (the candidate maps are the input of every engine), then the exact route (encoder, then the
decision per map: (8, 2) in hours, the symmetric (9, 3) maps, then all admissible ones), with the heuristic engines as
explore runs (one run in two, `STRATEGY.md` section 2) behind pilots with stated kill criteria. Every row is a `planned`
folder; its `PLAN.md` is written and committed before any compute (skill `experiment-start`). Candidate maps, counts
and labels: `STATUS.md` section 3c.

| ID | State | Tests | Question | T D F G R | Budget | Stop rule |
|---|---|---|---|---|---|---|
| [E-261103-01](experiments/E-261103-01-s5-map-census/) | done | H-261103-01, H-261101-07 | **Completed E-261103-01** (EXACT computation, coverage PROVED-1; see CONCLUSION). Census of the candidate maps for (7, 1), (8, 2), (9, 3), (10, 4) (dual triangular maps with multiple edges, underlying K_F) with admissibility (distinct corner triples) and automorphism data, output in `links` format; controls: (7, 1) = 1 class, (12, 6) = 59 types with the FD3 orders, every sampled class of the review contained, the two (8, 3) maps contained if that case finishes | 2 2 2 2 2 | 2 sessions, minutes-hours of CPU | the four censuses with every control, or a written reason why a case does not finish |
| [E-261103-02](experiments/E-261103-02-s5-omsat-multi-adjacency-encoder/) | done | - | Completed E-261103-02 (EXACT controls, soundness PROVED-1; see CONCLUSION). OM-SAT encoder for multiple adjacencies and F != 12 (Lemma 5.1 with m shared segments per pair; symmetric clauses for C3 / C2 / D3); validated on the Roest-Vigh and Mizhaev chirotopes (SAT, 0 predicate mismatches on random perturbations) with both negative controls; `ladder_exact.verify` repeated-corner guard tested. Free C2/C3 calibrated; uniform fixed-face C2/D3 UNSAT is not a geometric exclusion | 2 2 2 2 2 | 1-2 sessions | the controls pass and the first (8, 2) instance is built, or a written obstruction |
| [E-261103-03](experiments/E-261103-03-s5-exact-decision-8-2-9-3/) | done (2026-11-08: all 203 admissible (9,3) plain formulas UNSAT-VERIFIED, STATUS 3d) | H-261103-03, H-261103-02, H-261101-07 | (8,2) stage completed (see CONCLUSION; exact formula decisions, geometric scope PROVED-1). Paired (9,3) pilot completed (CONCLUSION / STATUS 3e); wider plain coverage unresolved. Autonomous 60/300-second grid completed (CONCLUSION / STATUS 3f); new-map tranche activated and same-path pilot concluded (STATUS 3h); owner-run tranche concluded (STATUS 3i), LOW-YIELD; broader census goal incomplete, no automatic expansion. Exact decision per map: the 2 (8, 2) maps (9 elements, plain and C2), the 8 C3 (9, 3) maps with C3 clauses, the 24 C2 maps via asymmetric formulas unless a nonuniform symmetry extension is supplied (fixed-face C2/D3 uniform UNSAT is not a geometric exclusion), then all 203 admissible (9, 3) maps; realizers and final polynomials on every model; CNF + DRAT kept; a realized model goes to `candidate-check` and `--target S5` | 2 2 2 2 2 | hours for (8, 2); one night for (9, 3) | every map decided (UNSAT-VERIFIED / realized / NONREALIZABLE-EXACT / listed timeout), or median SAT time above ~1 h per (9, 3) map |
| [E-261103-04](experiments/E-261103-04-s5-genus-ladder-9-faces/) | done | H-261101-07, H-261103-02 | **Explore.** Legacy representation gate failed (STATUS 3j); replacement dart-preserving surgery gate passed (CONCLUSION / STATUS 3k, PROVED-1). Geometric recovery pilot concluded UNDERPOWERED (CONCLUSION / STATUS 3l). Conditional grid concluded UNDERPOWERED (STATUS 3n). Intermediate-map audit completed (STATUS 3o): Roest-Vigh g1 OM-SAT, Mizhaev g2 formula UNSAT-VERIFIED (geometric interpretation PROVED-1). Alternative first-removal audit completed (STATUS 3p): an OM-SAT alternative found and finite queue exhausted. Descendant audit completed CHAIN-PASS (STATUS 3q), combinatorial/OM route only. Saved-OM realization: Roest-Vigh g1 and Mizhaev g1/g2 auxiliaries accepted (STATUS 3r, 3s). **Concluded 2026-11-07**: hinge ladder parked (fails both controls); OM-first realization of intermediates works but adds no (9,3) power. Genus ladder on 9 faces: every admissible (9, 3) map from its sphere down (`tubes`) and up again with `genus_ladder.search`, exact verifier per level, `--target S5` at the top; controls R1 and the two (8, 3) maps through the same ladder; what is different from DR1: a genus-3 target below the ravine, 9 faces, all pairs adjacent | 1 2 2 1 2 | one night, 10 cores, many seeds x short budgets | the night, or the first S5 PASS |
| [E-261103-05](experiments/E-261103-05-s5-symmetric-solid-first/) | done | H-261103-02, H-261101-07 | **Explore pilot completed**, BENCHMARK-PASS (CONCLUSION / STATUS 3g); R2/R3 achieved, target/night not activated. Broader proposal: symmetric solid-first (the Roest-Vigh route): C3 / D3 / C2 arrangements of 9 planes, the CP-SAT inner solver extended to 1-3 edge runs per pair; gates R2 (the known planes give the known objects) and R3 (rediscover an (8, 3) object from random D2 / S4 planes in a session) | 2 2 2 1 2 | 1 session; one night only if R3 passes | R2, R3, then the night or the first 36-pair solid |
| [E-261103-06](experiments/E-261103-06-embedded-first-pilot/) | parked | H-261101-07 | **Explore.** Embedded first, planar later (I-261103-01): R1 Szilassi from a torus, then an (8, 3) object from a smooth genus-3 surface; **R1 pilot 2026-11-07**: 4 valid starts blocked by the barrier at energy 84-118, UNDERPOWERED, parked (CONCLUSION / STATUS 3u); kill: the planarity energy plateaus above zero on R1 with the barrier active | 1 2 2 2 1 | 1-2 sessions | R1 and R2' converge (then a pre-registered (9, 3) night), or R1 fails |
| [E-261107-01](experiments/E-261107-01-s5-nine-plane-solid-first-pilot/) | done | H-261103-02, H-261101-07 | **Explore.** Week plan item 1: nine-plane solid-first target pilot, the E-261103-05 engine on 30 uniform 9-plane arrangements (c3 / d2p1 / random), 36 pairs, E = 39, cap 180 s; **Concluded 2026-11-07**: all 30 INFEASIBLE, LOW-YIELD@0.38 core-h (CONCLUSION / STATUS 3t); kill: no 36-pair solid in budget -> park the configuration | 2 2 2 1 2 | <= 2 core-h, one shard | 30 units decided or 2 core-h |
| [E-261108-01](experiments/E-261108-01-s5-arrangement-source-sweep/) | done | H-261103-02, H-261101-07 | **Explore.** Week plan item 4: arrangement-source sweep for solid-first, the E-261107-01 engine unchanged on 300 nine-plane arrangements (100 Roest-Vigh + random ninth plane, 100 Mizhaev + ninth, 100 random C2-invariant), 36 pairs, E = 39, cap 60 s, 10 shards; **Concluded 2026-11-08**: all 300 INFEASIBLE, 0 SOLID, LOW-YIELD@1.33 core-h (CONCLUSION / STATUS 3v); kill: no 36-pair solid -> park arrangement-first for (9,3) with the bound 3/N | 2 2 2 1 2 | <= 2 core-h, 10 shards | 300 units decided or 2 core-h |
| [E-261101-11](experiments/E-261101-11-external-human-review/) | parked | FD5, FD6 | **Owner declined the letters on 2026-11-07.** Owner's e-mails (zero compute): the S5 letter to Roest-Vigh and Mizhaev (have they tried (8, 2) or (9, 3); their method; an offer of the map census), and the S0 letters as before | 2 2 1 1 2 | 0 | a reply, or 4 weeks |
| [E-261103-07](experiments/E-261103-07-s5-10-4-census-symmetry/) | done 2026-11-08 (cost probe: 10/10 TIMEOUT, needs a speed-up first; STATUS 3w) | H-261101-07 | Symmetric stretch preparation from the completed (10, 4) census of E-261103-01 (STATUS 3c; do not repeat its enumeration); preparation of the stretch, no geometry before (9, 3) is decided; since 2026-11-08 a (10, 4) cost probe (10 mixed-pattern maps at 300 s), a follow-up of week item 5a only | 1 2 2 2 2 | <= 6.5 core-h by the caps, expected 2-4 (owner 2026-11-08: slow maps at 1800 s) | the 10 maps decided or timed out |
| [E-261109-01](experiments/E-261109-01-grooved-box-multiplicity-control/) | done 2026-11-09 (all pass; STATUS 3y) | H-261101-07 | **Audit.** Week plan item 1: grooved box with k = 2, 3 notches (top/front pair shares 3, 4 segments), pinned positive SAT / swapped-pairing negative UNSAT-VERIFIED through `submap=True`, unpinned k = 2 | 2 2 2 2 2 | < 0.1 core-h, 1 shard | all 5 units ended or a failed pinned positive |
| [E-261109-02](experiments/E-261109-02-independent-census/) | done 2026-11-09 (agreement; STATUS 3z) | H-261101-07 | **Audit.** Week plan item 3: independent growth enumerator vs E-261103-01 at (7,1), (8,2), (9,3) | 2 2 2 2 2 | seconds | classes, |Aut+|, reflexibility equal or a listed difference |
| [E-261109-03](experiments/E-261109-03-second-encoder-six-9-3-maps/) | running | H-261101-07 | **Audit.** Week plan item 4: independently written encoder `enc2.py` (Lemma 5.1 + line-interval parity, no INCONS/RFCONS/REFLEX1/POC) vs the first encoder on maps 40, 43, 10, 30, 48, 5 and the pinned controls | 2 2 2 2 2 | <= 1 core-h, 8 shards | six targets and controls ended, a disagreement, or 2 sessions |
| [E-261108-03](experiments/E-261108-03-s5-10-4-speedup-benchmark/) | done 2026-11-09 (kissat wins, P(4) = 475 core-h, no 10x; STATUS 3x) | H-261101-07 | **Exploit.** Week plan item 2: (10,4) speed-up benchmark, V1 kissat rel-4.0.4, V2 CaDiCaL `--unsat` (owner 2026-11-08 21:30); Phase A six known (9,3) maps + controls, Phase B (10,4) maps 96, 85, 146, 845 at 14400 s solver cap without DRAT (amendment 2), default-CaDiCaL baseline on 96, 85; censored projection P(lambda), winner rule of item 2 | 1 2 2 2 2 | <= 47 core-h, 10 shards, one owner launch <= 5.1 h | all 22 units ended, stop, or first SAT |

S0 items kept alive at low cost while the focus has no result: E-261101-10
(the FD6 write-up, one session per two weeks), E-261101-09 step 1 (predicate equality; it also audits the shared predicates
of the S5 encoder), E-261101-06 (rank-3 SAT, built in its 9-element form first as a filter for E-261103-03). Everything
else in the S0 queue is parked, not dropped.

## S0 queue (parked 2026-11-03, not dropped)

Kept as it stood at parking time (`STRATEGY.md` section 1: S0 resumes when the owner says so or when a focus result
transfers). States are maintained; no S0 night run starts without a new strategy decision.

Order rule (revised 2026-11-01, evening, after the strategy review and its follow-up): first the two cheap
experiments that are decisive on both branches at the combinatorial level (E-261101-23 k-face sub-instances, which
are monotone in the faces, and E-261101-06 rank-3), with the theory session that sharpens both (E-261101-21) and the
primary reads that could change everything (E-261101-22); then the certified-core mining and the encoder agreement
(E-261101-18, -09, -11); then the three tests of whether the constructive plateau is geometry or artefact
(E-261101-16, -24, -19, -17); then the exact campaign pilot (E-261101-15), the write-up and the hygiene; the
constructive side line last. IDs are permanent. Every row is a `planned` experiment folder (its README header holds
origin, hypotheses and links; the map shows them). State: `open` / `running` / `done` / `killed` / `parked` (stopped UNDERPOWERED, not refuted) / `blocked`;
`experiment-conclude` updates the State here and the `status` in the folder. Each folder's README has a starting
point written for execution by a smaller model; the `PLAN.md` (counter calibration and scenario move included) is
filled and committed before any compute.

| ID | State | Tests | Question | T D F G R | Budget | Stop rule |
|---|---|---|---|---|---|---|
| [E-261101-26](experiments/E-261101-26-engine-benchmark-ladder/) | done | H-261101-17, H-261101-10 | Closed for S0 on 2026-11-03 (strategy review: R4 is the wall; the S5 rungs R2 / R3 and the (8, 2) maps are controls inside E-261103-04 and E-261103-05). Two engines scored (STATUS 3b): chirotope-first (2026-11-02, cap lifted 2026-11-03 by E-261102-03) and the genus-ladder search (E-261102-04); both fail R4, only genus-ladder passes R5. R4 is the first rung where every scored engine fails (the stop rule's second branch, reached for the engines scored so far); next: another engine only with a stated reason it could pass R4. Engine benchmark ladder: Szilassi from random, the 8-face objects from their planes and from random symmetric planes, a genus-3 witness from random and from its parent, k-face sub-instances; every construction engine scored here before the target (I-261101-22) | 1 2 2 2 2 | 1-2 days harness, one night per engine | all engines scored, or the first rung where every engine fails |
| [E-261102-03](experiments/E-261102-03-chirotope-alt-cap-or-wall/) | done | H-261101-17 | Chirotope-first on R4 / R5 / R6k k = 8, 9 with the alternation cap lifted, so the time budget binds: is the full-map frontier of E-261101-26 a cap or a wall? Grid over the budget per seed (40, 120 min) | 1 2 2 1 2 | day pilot ~1 h (1 seed); night ~45 core-h | the grid, or the first R4 / R5 success (`candidate-check`); decides E-261102-02 |
| [E-261102-04](experiments/E-261102-04-genus-ladder-engine-score/) | done | H-261101-10 | The genus-ladder search (`genus_ladder.search`, the engine of the 94 archived genus-3 realizations) scored on the same ladder tasks (R1, R4, R5): a second row of the engine-score table | 1 2 2 1 2 | ~2 h harness option + day pilot; night shared with E-261102-03 (~30 core-h) | all units of R1, R4, R5 |
| [E-261102-01](experiments/E-261102-01-kface-sweep-completion/) | done | H-261101-15, H-261101-02, H-261101-12 | Completion of the k-face sweep of E-261101-23 (night 6 hung in the final-polynomial LP): the 32 types not reached at k = 8, 9 on the greedy face set, with the LP time limit and stored final-polynomial certificates; k = 10 only with a longer timeout; a second face set per type if k = 9 is SAT | 2 2 2 2 2 | laptop, daytime, 8 shards (~1.5 h) | all 32 types at k = 8, 9, or the first UNSAT (drat-trim, hashes, the same face set on every type) |
| [E-261102-02](experiments/E-261102-02-chirotope-first-night2/) | killed | H-261101-17, H-261101-12, H-261101-01 | Killed 2026-11-03 before any run (E-261102-03: full map a wall at <= 120 min, k = 7 expected). Was blocked because in E-261101-26 every seed stopped at the 20-alternation cap, so this night would end in ~2.5 h with a predictable k = 7 outcome. Night run 2 of the chirotope-first engine (E-261101-25 night 6 was cut by the LP hang and `--rounds 12`): LP time limit, `--rounds 40`, a cap inside each step, all 10 seed slices, certificates stored; launched only after E-261101-26 has scored the engine (PROTOCOL 8a) | 2 2 2 2 2 | one laptop night, 10 shards | the night, or the first realized 12-face model (`candidate-check`), or 20 seeds ending ROUNDS at 40 rounds |
| [E-261101-06](experiments/E-261101-06-rank3-sat-per-type/) | open | H-261101-02, H-261101-03, DR9 | Rank-3 (normals-only) SAT per type with degree, exact covering on the chambers of the 66 great circles, saddle and face-winding clauses; model counts; the 44 vertex-type patterns as the cube basis | 2 2 2 2 2 | 1 day coding, minutes per type | per type: UNSAT (proof!) or a model count estimate; stop after 3 types if every one is SAT with no pruning |
| [E-261101-21](experiments/E-261101-21-fold-locus-controls/) | open | H-261101-14 | The Gauss map as a fold map: the identity on the controls and the archive, its proof, and its clause form for E-261101-06 and the cubes of E-261101-15 | 1 2 2 2 2 | 1 session | an identity with proof and clause form, or a written "already implied" |
| [E-261101-22](experiments/E-261101-22-equivelar-literature/) | open | - | Demoted 2026-11-03: the S5 objects at (8, 2)-(11, 5) are non-equivelar (2E/F is not an integer), so the equivelar reads cannot contain them; the S5 letter to Roest-Vigh and Mizhaev moved to E-261101-11. Step 0 done 2026-11-01 (`literature/primary-reads-2026-11-01.md`: the "empty set" sentence is the vertex version; the face version is open in print; both 8-face objects have 4 convex vertices). Remaining: equivelar {p,3} polyhedra (McMullen-Schulz-Wills, Brehm-Wills, Schulte-Wills 1985 and 2012), Bokowski-Schewe 2002, Arseneva et al. 2024 | 1 2 2 1 1 | 1 literature session | the sources read with exact statements, or two sessions |
| [E-261101-18](experiments/E-261101-18-face-grouped-mus-symmetric/) | open | H-261101-11, H-261101-02 | Face-grouped minimal unsatisfiable cores of the 50 certified symmetric instances; recurring small cores feed E-261101-23 | 2 2 2 2 2 | ~30 core-h (one night) after a one-session pilot | all 50 cores, or 10 cores with no pattern below 10 faces |
| [E-261101-09](experiments/E-261101-09-encoding-comparison/) | open | H-261101-06, DR8 | Encoding comparison with `pirozhkov-andrei/polyhedraproof`: predicate equality on random exact configurations first, timings second; map their two refuted formulas to our types | 1 2 1 1 2 | 1 day | predicate agreement or a named disagreement (which stops campaign work until resolved); time per instance for both |
| [E-261101-11](experiments/E-261101-11-external-human-review/) | parked | FD5, FD6, E-261101-03 | **Owner declined the letters on 2026-11-07.** External human review: first e-mail to the `polyhedraproof` author (three shared symmetric instances with CNF hashes, one question), then Bokowski / Brehm with FD5, FD6, Lemma A and the dossier; since 2026-11-03 also the S5 letter to Roest-Vigh and Mizhaev (S5 queue above) | 2 2 1 1 2 | owner's e-mail, no compute | a reply, or 4 weeks without one -> next reviewer |
| [E-261101-16](experiments/E-261101-16-arrangement-first-chamber-sat/) | open | H-261101-08, H-261101-10 | The S5 form is E-261103-05 (2026-11-03); this row keeps the S0 form (a symmetric arrangement with an asymmetric solid), parked. Arrangement first: exact chamber-SAT (disk condition encoded exactly) on G-symmetric arrangements with asymmetric solids allowed, on the 247 archived arrangements, on the 1005 near-miss arrangements and on normals realized from E-261101-06 / -23 models | 2 2 2 1 2 | one night (~20 core-h) | the night ends, or the first solid with >= 54 pairs (then `candidate-check`) |
| [E-261101-24](experiments/E-261101-24-farkas-descent-pilot/) | open | H-261101-16, H-261101-09 | Farkas-certificate descent: the exact dual gradient of offset infeasibility moves the normals (what is different from DR2/DR4: guided, not annealed); pilot on the 80 radius-0 seeds and a perturbed witness | 2 2 2 1 2 | 1 day coding, ~5 core-h | 50 steps per seed, or the first exact S3 object at a level where sampling found none; positive control first |
| [E-261101-19](experiments/E-261101-19-barrier-continuation-genus3-handle/) | open | H-261101-10, H-261101-03 | Barrier continuation inside the genus-3 realization space towards an in-class handle, with a measure that can go negative (replaces E-261101-07) | 2 2 1 2 2 | 1 core-h pilot, then one night (40 realizations) | all extendable arms of 40 realizations, or the first exact genus-4 object |
| [E-261101-17](experiments/E-261101-17-realization-space-geometry/) | open | H-261101-09, H-261101-10 | Geometry of the realization spaces: chord widths by hit-and-run, offsets and normals separately, shrinkage per handle, connectivity of the type-15 archive | 1 2 2 1 2 | ~10 core-h | 10 realizations x 2,000 steps and the pairwise segment tests |
| [E-261101-15](experiments/E-261101-15-cube-and-conquer-pilot/) | open | H-261101-06, H-261101-01, H-261101-12 | Cube-and-conquer pilot on one trivial-Aut type as an Actions matrix, cubes on the 44 vertex-type bits pruned by E-261101-21, LRAT checked on the fly (after E-261101-09 agreement) | 2 2 1 1 2 | ~300 core-h of Actions | one type decided, or the matrix exhausted; report refuted fraction per core-hour and proof-handling cost |
| [E-261101-10](experiments/E-261101-10-write-up-symmetric-immersion/) | open | FD6, H-261101-13 | Write-up: no symmetric immersion (second encoder, soundness proofs, archived certificates, Lemma A for improper isometries reviewed or the statement restricted to rotations) | 2 1 1 1 2 | 2-3 sessions | arXiv-ready draft reviewed by `adversarial-verifier` (a filter) and one human |
| [E-261101-03](experiments/E-261101-03-type0-dossier/) | open | H-261101-05, FD10 | Type-0 genus-3 dossier: the owner's independent second verifier first, then canonical form, certificate re-run, novelty search | 1 2 2 1 2 | 1-2 sessions, no compute | stop after the 5 steps or 2 sessions; any verifier mismatch -> fix FD10 first |
| [E-261101-20](experiments/E-261101-20-incremental-sat-across-types/) | open | H-261101-06 | One incremental SAT session for the 25 symmetric instances with selector literals: do shared GP lemmas cut the total time? | 1 2 2 1 2 | a few core-h | two orders; below 1.5x closes it, above 2x makes it the campaign default |
| [E-261101-08](experiments/E-261101-08-relaxed-s1-twelve-faces/) | open | H-261101-07, DR12 | Relaxed S1 target, a goal in itself: 12 faces, three doubled pairs as one C3 orbit (genus 7, the smallest S1 case), after Roest-Vigh calibration | 1 2 2 1 2 | 2 nights max, <= 25 % of compute | calibration fails -> fix engine, do not run n = 12 |
| [E-261101-12](experiments/E-261101-12-maximal-face-neighbourly/) | open | H-261101-07, DR12, DR15 | Umbrella row of the focus, split on 2026-11-03 into E-261103-01 to -07 (S5 queue above). **Focus target since 2026-11-03 (`STRATEGY.md`): (9, 3) first, stretch (10, 4)** (SPEC S5, `--target S5`); the strategy review splits this row into experiments. Maximal face-neighbourly cubic polyhedra per genus, (F, g) = (8, 2), (9, 3), (10, 4), (11, 5) with 2, 3, 3, 2 doubled pairs; (8, 2) only as a warm-up if it calibrates the (9, 3) method; symmetric ansatzes first (black-box engines were underpowered there) | 1 2 2 2 2 | literature 1 session; then 1 night per case | (9, 3): an S5 PASS (`candidate-check`), or every map tried UNSAT with a written power statement; then (10, 4) under the same rule |

Done or merged this cycle: [E-261102-03](experiments/E-261102-03-chirotope-alt-cap-or-wall/) (done 2026-11-03, night 7: full-map frontier unchanged with the cap lifted, 0/12 at 120 min, R6k k = 8, 9 4/4 each) and [E-261102-04](experiments/E-261102-04-genus-ladder-engine-score/) (done 2026-11-03, night 7: genus-ladder search, R4 0/14, R5 5/10 at 6 min); [E-261102-02](experiments/E-261102-02-chirotope-first-night2/) (killed 2026-11-03 before any run, by the pre-registered rule of E-261102-03); [E-261101-23](experiments/E-261101-23-k-face-subinstances-face-cegar/) and [E-261101-25](experiments/E-261101-25-chirotope-first/) (done 2026-11-02, night 6, both UNDERPOWERED: a final-polynomial LP without a time limit hung 9 of 10 shards; follow-ups E-261102-01, -02); [E-261102-01](experiments/E-261102-01-kface-sweep-completion/) (done 2026-11-02, LOW-YIELD@4.2 core-h for exclusion on the greedy face set at k <= 9, UNDERPOWERED for realization); [E-261101-07](experiments/E-261101-07-pinned-hemisphere-margin/) (done, verdict ARTEFACT:
the "pinned margin" was a floor of `gauss_gate.hemisphere_margin`; its real question is E-261101-19);
[E-261101-13](experiments/E-261101-13-exact-covering/) (killed: merged into E-261101-06, exact covering on chambers).

Below the gate (T + D < 3; run only after re-scoring with a written reason):

| ID | Question | T D F G R | Why below |
|---|---|---|---|
| [E-261101-04](experiments/E-261101-04-normals-first-power-study/) | Power of normals-first: how often is the *control* SAT at radius r? | 1 1 2 1 2 | re-scored 2026-11-01: the Wendel estimate (`reviews/fresh-eyes-review.md` 2.3) predicts the answer; run a 2 core-h check only if E-261101-17 finds widths comparable across genus |
| [E-261101-14](experiments/E-261101-14-chirotope-chambers/) | Chirotope chambers of the 247 archive realizations | 1 1 2 1 2 | descriptive; E-261101-17 measures the same spaces with a decision attached |

## Parked methods (low measured yield, not refuted)

Tried, with little yield at the budget stated in `STATUS.md` §3 (LOW-YIELD rows). None is refuted, so none is
forbidden. A new run needs a `PLAN.md` that says what is different this time (objective, ansatz, power, scale)
and which outcome would change the estimate. An unchanged re-run at a similar budget is expected to repeat the
result, so it scores D = 0 and does not pass the gate.

| Method | Measured yield | What would make a new run informative |
|---|---|---|
| Genus ladder / arch / glad climbing (DR1) | genus 3 for 4 types, genus 4 never, nights 3-5 | a handle choice that passes the Gauss gate (k_tau = -1), or a new type; or a target below the ravine: the 9-face ladder E-261103-04 (explore, 2026-11-03) |
| Normals-first / k-drift climbing (DR2) | 12,202 UNSAT, 0 SAT, ~150 core-h; low power | E-261101-04 shows the control is SAT often enough |
| Closure-first pdefect / sdefect (DR4) | zero defects only with >= 11 non-simple faces | face simplicity inside the model |
| Black-box engines on the pair energy (DR6) | n = 7 solved; plateau at n = 8 and genus 4 | a different objective (e.g. with Gauss-class terms), not more seeds |
| Near-miss repair (DR5) | all 1005 near-misses in the wrong Gauss class (FD11) | a near-miss in the right class |
| Gauss clauses as a SAT speed-up (DR16) | no speed-up observed | - |
| Asymmetric immersion instances without cubing (DR8) | 8/8 timeouts at 2.2 h | cube-and-conquer (E-261101-15) |

## Decision point

Three scenarios with explicit credences (idea I-261101-17; all CONJECTURE, set 2026-11-01 by the strategy review,
updated by `experiment-conclude` from the "scenario move" line of each `PLAN.md`):

S0 table (unchanged 2026-11-03: no S0 evidence since 2026-11-01):

| Scenario | Credence | What raises it | What lowers it |
|---|---|---|---|
| A: a realization exists | 0.20 | any S3 object of genus >= 4 (E-261101-16, -19); a realizable OM model | per-type OM-UNSAT (E-261101-15); H-261101-10 supported |
| B: all 59 types are OM-UNSAT (as in the vertex version) | 0.55 | a rank-3 UNSAT (E-261101-06); a decided type (E-261101-15); small recurring cores (E-261101-18) | any OM-SAT model |
| C: some types are OM-SAT with only non-realizable models | 0.25 | an OM-SAT model that fails the realizability audit (I-261029-57) | per-type OM-UNSAT |

S5 table (set 2026-11-03 by the strategy review, (9, 3) row moved 2026-11-08 by `reviews/strategy-review-2026-11-08.md` §9 and again by the E-261103-03 item 5a conclusion; all rows set 2026-11-08 by `reviews/strategy-review-2026-11-08d.md` §8, owner-approved; all CONJECTURE; "cannot tell" = not decided within the strategy's
horizon by our tools; moved by the "scenario move" lines of the E-261103 PLANs):

| Case | exists | does not exist | cannot tell | Evidence in one line |
|---|---|---|---|---|
| (9, 3) | 0.05 | 0.95 | 0 | E-261103-03: all 203 admissible plain formulas UNSAT-VERIFIED (EXACT); residual weight for an encoder or census error: no positive control with a pair of multiplicity >= 3 (18 maps have one), one enumerator, one encoder, no independent review (lead review 2026-11-08d §8) |
| (8, 2) | 0.03 | 0.97 | 0 | E-261103-03: both plain formulas UNSAT-VERIFIED; one map has a tripled pair with no positive control; conditional on PROVED-1 census coverage and encoder soundness, not reviewed (lead review 2026-11-08d §8) |
| (10, 4) | 0.15 | 0.40 | 0.45 | both smaller minimal-genus cases empty at the OM level (inductive, weak); E-261103-07: 10/10 TIMEOUT, growth F > 3.3 per map, 10-40 estimated, so the exact route may be out of reach (lead review 2026-11-08d §8) |

Rules for S5: both (8, 2) and (9, 3) decided non-existent -> write the note, focus moves to (10, 4) with E-261103-07
(fired 2026-11-08: owner approved lead review 2026-11-08d; the note is gated by week items 1, 3, 4 and says that no
independent review took place);
(9, 3) exists -> the stretch starts from the method that found it; E-261103-03 stalls on models that neither realize nor
certify -> build the realizability stage (I-261029-57) before more SAT.

Exploration quota (I-261101-22): while the focus target has no result, one run in two is drawn from the mutation pool
(a parked method with one stated change, a re-scored below-gate row, or a new idea), logged as "explore" (`STRATEGY.md`
section 2; PROTOCOL 8a's default is one in four). No construction engine runs on the target before it is scored on the
benchmark ladder: for S5 the rungs are R2 / R3 (the 8-face objects) and the (8, 2) maps, as controls inside E-261103-04
and E-261103-05.

Rules. After E-261101-06, -18, -16, -19 and -17: if B >= 0.7, run the certified campaign (E-261101-15 scaled to all
types, with `polyhedraproof` if they agree on predicates); if A >= 0.35, put the constructive items first (the
arrangement or the path that raised it); if C >= 0.4, build the realizability stage before more SAT; otherwise
publish the shareable results (`STATUS.md` section 5) and re-plan. Decide from the table, not from sunk cost.
