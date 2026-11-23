# Strategy review 2026-11-23, final (cycle step 3): nine faces stays first behind two gates; the (8, 3) rung first, P3 with guarded label breaking second
Inputs: the draft `strategy-review-2026-11-23.md` (owner-accepted, its closing section), the cross-review `-codex.md` (draft `57fce28a`) and the files it
cites. Codex's checks A-F and my re-check B' are session checks, not ledger evidence; prices and credences are planning judgments (CONJECTURE / NUMERICAL).

## Owner digest
1. **The draft stands, with six repairs from the cross-review.** Nine faces stays first behind two gates; P6 ends at the equivelar slice; credence 0.35 -> 0.28.
2. **Step 0 already passed in Codex's session:** both truncated solids give an unaided SAT plain formula in 0.08 s and are realized; the lab registers them as fixtures, checked by the bare verifier (31 of 36 pairs), while `--all-pairs` stays the discovery check.
3. **My label-breaking rule was unsound** (Codex B, reproduced: stage-A record 51, 0 of 96 size-sorted labellings survive); the repair compares adjacent swaps of equal-size faces only (4 survive, PROVED-1). P3 gets the old 16-cube layout at 3.0 core-h, any UNKNOWN parks it, and the (8, 36) discovery test comes only after both negatives are refuted (chirotope blocking does not block a map).
4. **Larger census, narrower claims:** ~40-65 thousand admissible (8, 3) classes (heavy-tailed); the eight-face classification is cubic only (L6 resolves, it does not contract); rates are observed counts (2 of 51, 0 of 1071) with no transferred bound; the twelve-face credence stays 0.40.
5. **Your approval now:** the week plan (§2), the `STRATEGY.md` text (§3), the credence 0.28; one-line permissions for items 1, 2 when the lab asks. Later: O4 (the cubic classification note path), O5 (if both gates close: park nine faces, or the C2 (9, 5) remainder).

## 1. Points (A accept, R reject, U unresolved)
| # | Point (source) | Verdict and evidence | Label |
|---|---|---|---|
| 1 | Step 0 already passed (codex:6, :27-34) | A. SAT 0.08 s each, `pilot.model_valid`, hinge-embedded, bare verifier exit 0, (26, 39, 9, -4); the lab registers both fixtures | session check (EXACT verifier, instance scope) |
| 2 | `--all-pairs` fails on a truncation; it covers the plain path only (codex:7, :34) | A. `verify_candidate.py`:60-64 (23 single, 8 double, 5 absent pairs): controls use the bare verifier and counts. `controls_b.py`:5-16 covers GP + SYM + gauge; with A the map clauses at 10 elements have a SAT control too | - |
| 3 | Unguarded label breaking is unsound (codex:8, :36) | A. Re-check B': record 51 (`3a9473fb...`), 96 size-sorted labellings, 0 survive unguarded, 4 guarded (both size orders). Repair: equal-size adjacent swaps only | PROVED-1 (Codex), EXACT count |
| 4 | Chirotope blocking does not block a map (codex:9, :38) | A. `p3.py`:312 blocks one signed chirotope; a second labelling of Roest-Vigh's map survives in cube 13. (8, 36) residual test deferred | session check |
| 5 | Item 2 budget inconsistent: 1 h on 8 workers = 8 core-h vs 3 (codex:21) | A. Use E-261116-07's layout, 16 x (225 + 450) s = 3.0 core-h (`PLAN.md`:49); reuse its UNKNOWN baseline; any UNKNOWN parks | - |
| 6 | Coverage rules for item 1 (codex:19) | A. Completion bit per input; every admissible class decided or matched to a stage-A record by canonical code; zero-SAT branch only on full coverage | - |
| 7 | Census price (codex:13, :40) | A. 32 random unfinished inputs: 9167 classes, 1586 admissible (0-633 each), so ~52 thousand admissible in all (~40-65); formulas ~5-12 core-h | NUMERICAL |
| 8 | Transfer rule; no rule-of-three across genera (codex:11, :40) | A. Report 0 of N per completed stratum. A realized new stratum gets one transfer rule pre-registered before its probe (e.g. its extra degrees plus a ninth face of extra degree 2) | CONJECTURE |
| 9 | O4 claim cubic only (codex:10, :42) | A. `E-261116-09/LEMMAS.md`:128-132 resolves degree-4 objects to cubic ones; contraction of the known maps is open. Draft N3's wording withdrawn | PROVED-1 (L6) |
| 10 | "14 times lower"; "non-equivelar (9, 4) never run plain" (codex:44) | A. The first compared a point estimate with a bound: state 2 of 51, 0 of 1071. 23 of 33 priced (9, 4) records ran plain (`STATUS.md`:589); 12428 symmetric maps outside stage C ran symmetric formulas only | NUMERICAL |
| 11 | Credence 0.28 (codex:12) | A. Forecast explicit at draft 2026-11-22:101 | CONJECTURE |
| 12 | Twelve-face 0.40 -> 0.25 optional (codex:12, :46) | R, my own proposal: no datum bears on it, and credences move by evidence lines. Stays 0.40 | CONJECTURE |
| 13 | Control-file dedup; E-261110-01 (codex:23, :46) | A. Fix dropped: git stores identical blobs once, manifests hash per path (20 copies in stage C, 30 with A). E-261110-01 carried as deferred | - |

## 2. Week plan (for `ROADMAP.md`; replaces the 2026-11-22 plan; branch `lab/2026-11-23`)
Rules: <= 10 cores, 8-10 shards, no proofs, PLAN and tests first, UNSAT = UNSAT-SOLVER; jobs <= 50 min wall the lab launches after a one-line permission, longer ones the owner; elapsed budget and stop reason in every manifest; success only `--all-pairs` PASS with the face count, then `candidate-check`.
1. **Full (8, 3) classification at formula scope** ([E-261123-01], PLAN first; J 0, the rung for any non-equivelar (9, 4) stratum; 2 2 2 2 2).
   * Step 0, register the 10-element controls: Roest-Vigh's planes (`code/control_rost_vigh.py`:23) cut by (7, 14, 21, -57), face-8 link (2, 6, 3); Mizhaev's
     (E-261107-01 `results/0/mizhaev_E36.output.candidate.json`) cut by (1, 2, 3, -1113), link (3, 2, 0). Bare verifier EMBEDDED, (26, 39, 9, -4), 8 doubled
     pairs, on the built and the bridged files; unpinned plain formula SAT with a clause-checked model; bridge recovery recorded separately. A plain-CNF UNSAT
     on a verified fixture -> encoder audit, lead; a bridge timeout -> recovery diagnosis.
   * Census: all 1806 inputs of `census.extra_graphs(8, 8)` by `census.run` in input-slice units, a completion bit per input. Controls: the 97 equivelar
     classes of stage A record for record, the 790 free-C2 codes, the six face-transitive classes, the (8, 2) census by the same path. Lean: admissible
     records committed if <= 20 MB, else SHA-256 only. Expected ~400 thousand classes, ~40-65 thousand admissible (NUMERICAL).
   * Formulas: every admissible class decided or matched to a stage-A record by canonical code. Plain formula, 9 elements, code orientation, kissat
     cap 60 s, lean, 10 shards; a chunk 0 of ~2000, stratified by extra-edge degree sequence, prices the rest end to end.
   * Tree: step 0 fails -> lead. Coverage incomplete at the caps (an unfinished input, UNKNOWN after the 600 s pass, an unbridged SAT) -> lead with the
     open IDs, counts over completed strata only. Full coverage, only the two known maps SAT -> "every admissible cubic (8, 3) map other than Roest-Vigh's
     and Mizhaev's has an UNSAT-SOLVER plain formula" (formula scope, planning; 0 of N per stratum); no non-equivelar (9, 4) run on the laptop; O4. A new
     map realized -> `candidate-check`, escalate (reopens E-261112-02 Stage B); if non-equivelar, a transfer rule pre-registered, then a <= 10 min probe.
   * Budget: census <= 4 core-h, formulas <= 12 core-h; lab jobs <= 50 min wall, otherwise an owner day run. Lab: Opus, high / Codex gpt-6-astra, high.
2. **P3 with guarded face-label breaking, refutation rungs** ([E-261123-02] from E-261116-07, parked rule `ROADMAP.md`:323; explore, J 2 through the tree;
   1 2 2 2 2).
   * Breaking: faces ordered by size; the upper-triangle multiplicity word lex-<= its image under each adjacent swap of two equal-size faces. After
     relabelling, the sign gauge and mirror fix are reapplied, then the cube is assigned. Soundness and coverage over the union of cubes are PROVED-1 in
     the PLAN. Regressions: stage-A record 51 and both known solids, pinned in canonical labellings; (7, 21) finds K7.
   * Rungs: (8, 30) and (9, 39), 16 one-worker cubes each at 225 / 450 s, builds inside the cap (<= 3.0 core-h, 1 prep session); E-261116-07's baseline
     (all UNKNOWN) reused. Lab: Opus, high / Codex gpt-6-astra, high.
   * Kill: any UNKNOWN at either rung -> parked, cause recorded. A model -> decode the map, check its chirotope against that map's plain formula, then
     a cause (a bug: one repair). Both rungs INFEASIBLE -> a priced (8, 36) unaided recovery (canonical dart codes), then (9, 45) priced; no
     residual-INFEASIBLE test until a whole-map-class blocker has controls.
3. **Conditional, O4** (item 1 fully covered with the two known maps, and the owner asks): price checked replays for "cubic eight-face map classes at genus
   3", stage A's negatives included (<= 10 min, 200 formulas), with census coverage, encoding soundness, L1 and proof provenance; for degree <= 4 only "admits
   a cubic resolution of one of the two map types". Lab: Sonnet, medium / Codex gpt-6.1-sol, medium.
4. **Ledger fixes** (no compute, with item 1's conclusion): H-261101-07 -> weakened (genera 2-3, formula scope); E-261117-04 `tests:` emptied; a nine-face
   hypothesis file (credence 0.28) takes the nine-face links. Lab: Sonnet, medium / Codex gpt-6.1-sol, medium.

Deferred: C2 (9, 5) remainder (O5), parity (paper), plain formulas on symmetric (9, 4) maps, C3 (9, 6), E-261110-01, E-261116-08, P4, I-261117-03, curved faces,
deletion sieve, E-261101-08, (10, 4) replay. Parked: P3-sym, nine faces. Closed for the laptop: (11, 5), face-transitive nine faces (genus 4, 7), C2 genus >= 6, equivelar (9, 4) (3bn), equivelar genus 7.

## 3. `STRATEGY.md` diff and credences
* §1 "First" becomes: "**First (owner, 2026-11-16b, confirmed 2026-11-17, -18, -19, -22 and -23): S1, nine mutually adjacent faces with the genus free.**
  The symmetric route ends at genus 4 on the laptop (2026-11-22), and P6 ends at the equivelar slice: all 1071 admissible equivelar (9, 4) plain formulas
  are UNSAT-SOLVER (E-261117-04). Two gates decide whether nine faces keeps a laptop route. First, the full (8, 3) rung (E-261123-01): a non-equivelar
  (9, 4) stratum runs only after it realizes a map outside the equivelar slice, under a transfer rule pre-registered before its probe. Second, the
  census-free refutation rung (E-261123-02): (8, 30) and (9, 39) INFEASIBLE on every cube, then an unaided (8, 36) recovery, before any (9, 45) price.
  If both close, the owner chooses between parking nine faces and the C2 (9, 5) remainder. P3-sym is parked; mirror families only by plain formulas
  (L1); no nine-plane sampling night without a rung-below rate. Success is only `verify_candidate.py FILE --all-pairs` PASS with nine faces, then
  `candidate-check`."
* Log: "2026-11-23 (owner's approval of `reviews/strategy-review-2026-11-23-final.md`, cycle step 3): nine faces stay first behind two gates (the full (8, 3)
  rung; P3 with guarded label breaking on the known negatives); P6 ends at the equivelar slice; credence 0.35 -> 0.28. Stance, S0 parking, side track unchanged."
* Credences (CONJECTURE): nine faces 0.35 -> 0.28 (point 11); relaxed Szilassi-12 stays 0.40 (point 12); the others unchanged, no new datum.

## 4. Owner decisions
* Now: §2, §3 and the credence. After approval this session applies `ROADMAP.md`, `STATUS.md`, `STRATEGY.md`, the idea files (N1, N2, N4), `TODO.md` and the
  handover; then the end-of-week PR of `lab/2026-11-22` and the branch `lab/2026-11-23`. Later: O4, O5.
