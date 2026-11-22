# Portfolio review 2026-11-22, C2-a (Claude Code): choosing the next research week

Blind assignment of `reviews/portfolio-review-2026-11-22-prompt.md`; evidence at `1310847b` plus the local
`results/stageB5-pass1-c000..c009` logs of E-261119-02. One AI author: every ranking, probability and price below is a
planning judgment (CONJECTURE); proof sketches are at most PROVED-1 (`SPEC.md` §5). Paths are relative to
`research/12-faced-polyhedron/`.

## Owner digest

1. **Verdict.** The symmetric nine-face route has spent its evidence: genus 4 is complete (12562 formulas UNSAT-SOLVER), C3 genus 5 has no map, the C2 genus-5 random 10 % is 97830 of 97830 UNSAT-SOLVER, and the plain formula refutes every priced symmetric map as well (69 of 69).
2. **Main investment: P6, the equivelar slice** (E-261117-04): every face an (F + 1)-gon, the extra edges a 2-regular graph, each map decided by the plain (asymmetric) formula. It is the only finite, unrun S1 slice that holds both known eight-face objects and reaches genus 4 directly.
3. **New session evidence (NUMERICAL, not ledger):** the equivelar (8, 3) census has 97 classes, 51 admissible, in 22 s, with Mizhaev's map (pattern 8) and Roest-Vigh's (4 + 4) inside. The (9, 4) census is priced at about 4 core-h (2 h wall; 4104 to about 27000 classes), and a hard (9, 4) plain formula decides in 4-24 s.
4. **First action:** P6 stage A at (8, 3), a lab job of minutes. The plain formula runs on the 51 admissible maps; both known maps must come back SAT and be realized unaided, and the other 49 get decided.
5. **Week:** stage A, then the free-C2 (8, 3) per-map pass (790 classes, minutes), then the (9, 4) equivelar census (owner day run), then the (9, 4) plain pass (at most one owner night), then conclusion of the 10 % pass.
6. **Abandon P6** on a failed stage-A control that fails again after one repair, a (9, 4) census projection above 12 core-h, or a stage-C price above one night. An all-UNSAT-SOLVER slice ends it as planning evidence; it is not a negative result.
7. **Strongest rival:** the C2 (9, 5) remainder (about 129 core-h, postponed by the owner). It loses on its own 10 % sample and on the heavier genus-5 multiplicity load. The order flips if the free-C2 (8, 3) pass finds new realized maps while stage A finds none.
8. **Owner decisions, all open** (the owner did not decide on 2026-11-22; §6 lists options, consequences and defaults): the week plan; one-line permissions for items 1-2; the census cap 8 -> 9 and the item-3 day run; the item-4 night; whether a new (8, 3) object, if one appears, counts under the filter. Until then nothing runs.
9. **Odds:** low. I put the chance of a verified nine-face object this week at about 5 %. Either way, the week measures the rung-below rate that `STRATEGY.md` §2 asks for.
10. **Independence:** the session-start hook showed the `CONTINUE_PROMPT.md` handover and the Git commit subjects, including the draft's proposed item 1. I opened no excluded file. My item 2, which matches that proposal, rests on STATUS 3bd/3be and E-261119-02 `README.md`:40-41 alone.

## 1. Inventory coverage

`map/graph.json`: 176 ideas + 41 hypotheses = 217 nodes, equal to the 217 files in `ideas/` and `hypotheses/` (0 missing
either way). Ideas: open 117, tried 46, parked 13. Hypotheses: open 28, weakened 6, supported 5, proved 1, refuted 1.
Experiments: 114 (done 84, planned 22, parked 5, killed 2, running 1 = E-261119-02). Families group IDs by how they could
yield a result, not by direction tag (placements that differ from the tags: I-261101-15 in B as P6's origin; H-261101-07
in A; I-261119-02 in C; I-261029-04, -26 in D). In ID lists, a..b is a range of serial numbers.

| Fam | Route to a result | IDs | n | open / tried / parked / other | S1 nine-face evidence (STATUS) |
|---|---|---|---|---|---|
| A | exact per-map / per-type decision machinery (encoders, cubes, certificates, bridge) | H-261029-02,12; H-261101-01,06..07,12; H-261103-01,03; H-261110-03; I-261029-11..12,16,24..25,28,41..45,47..48,57,63; I-261030-29,31..32; I-261031-01..03; I-261101-12,18; I-261108-02,04..06,08; I-261110-05..07; I-261113-02; I-261114-01..04; I-261116-02..03,05 | 48 | 38/4/3, sup 2, weak 1 | (8, 2), (9, 3) UNSAT-VERIFIED (3d); (10, 4), S6 (10, 3) UNSAT-SOLVER; bridge 16/153 at (10, 2) (3ah) |
| B | structured map slices + per-map formulas (symmetric, face-transitive, equivelar) | H-261103-02; I-261030-07,18; I-261101-15; I-261103-03,06; I-261113-01,04; I-261116-04; I-261117-01..02,04; I-261118-02..03; I-261119-01,03 | 16 | 6/8/1, weak 1 | 3au, 3bj (face-transitive empty), 3be-3bh, 3bi |
| C | census-free / chirotope-level construction (P3, P3-sym, P4, chirotope first) | H-261101-17; I-261029-20; I-261101-21; I-261103-02; I-261117-03; I-261118-01; I-261119-02 | 7 | 4/3/0 | 3aw, 3ax, 3bb, 3bd: no nine-face model, no refutation power |
| D | arrangement first: plane families, cells, solid-first, sources | H-261030-03; H-261101-08; H-261110-02; H-261112-01; I-261029-04,10,26..27; I-261030-08; I-261101-08,20; I-261103-04; I-261108-03,11; I-261110-01; I-261112-01; I-261113-03; I-261116-01,06 | 19 | 12/4/2, weak 1 | 3ae (0/2004), 3ak (only the source map), 3ay (0 hits) |
| E | continuous / heuristic engines, ladders, realization-space geometry | H-261029-03; H-261030-04..05; H-261101-04,09..10,16; I-261029-05..06,08..09,13..14,19,21..22,29..40,46,51,55,59; I-261030-01..03,05,12..17,20..22,24..28,30; I-261031-05; I-261101-01,03,05,09,11,19; I-261102-01; I-261103-01,05; I-261114-05 | 62 | 38/21/1, weak 2 | S0-era; LOW-YIELD at n = 8 and genus 4 (DR1, DR2, DR6); embedded-first R1 UNDERPOWERED (3u) |
| F | theory, obstructions, lemmas | H-261029-01,04..11; H-261030-01..02; H-261101-02..03,11,13..15; H-261110-01; I-261029-01..03,15,17..18,23,50,54,56,58,60..62; I-261030-23; I-261101-02,04,10,13..14,16; I-261108-01,09; I-261110-04; I-261116-07 | 43 | 32/4/1, sup 3, weak 1, proved 1, refuted 1 | L1-L6, Lemma P (3bi); multiplicity hypotheses H-261110-01 |
| G | relaxed / alternative targets (other F, non-cubic, curved face) | I-261029-07,53; I-261030-04,06,09..10; I-261101-07; I-261108-10; I-261110-02..03; I-261118-04 | 11 | 6/1/4 | deletion sieve (9, 3) only (3az); 12-face S1 untried |
| H | literature, review, write-up, process | H-261101-05; I-261029-49,52; I-261030-11,19; I-261031-04,06; I-261101-06,17,22; I-261108-07 | 11 | 9/1/1 | none |

Totals reconcile: 48 + 16 + 7 + 19 + 62 + 43 + 11 + 11 = 217; open 145, tried 46, parked 13, weakened 6, supported 5,
proved 1, refuted 1. Most open items of A, E, F and H serve S0 or the closed S5 / S6 rungs; the live S1 routes are in B, C, D and G.
Source files read for contenders and consequential rejections: H-261101-07, H-261112-01, H-261110-01, H-261103-02;
I-261101-15, I-261108-01, I-261110-01, I-261110-03, I-261116-06, I-261117-03, I-261119-01; and the parked ones that
touch S1: I-261118-04 (curved face; parked because nine faces had no census to sieve; P6 would supply one, but
straightening is the full formula, so no change), I-261117-04 (Z9 orbit; input empty at genus 4 and 7, 3au, 3bj),
I-261108-06 (contraction sieve, 0 of 203), I-261029-53 (non-cubic vertices; L6 reduces degree <= 4 to cubic, 3bi),
I-261030-09, I-261116-01 (S0 / S6 only). No parked or rejected S1 route has a concrete change that answers its failure,
except Stage B ninth-plane cells (E-261112-02), which reopens on a new (8, 3) map by its own rule (`ROADMAP.md`:152-156).

## 2. Evidence on the common endpoint (a verified nine-face S1 object; `STRATEGY.md`:16-17)

* Symmetric per-map (B): C3 3+3+3 and C2 4 x 2 + 1 at (9, 4), 12562 of 12562 UNSAT-SOLVER (3bf); C3 (9, 5) has no map
  (EXACT, coverage PROVED-1, 3bg); C2 (9, 5) chunks 0-9 (local logs): 97830 completed records, all UNSAT-SOLVER, max
  2.0 s, mean 0.16 s, 14.3 core-h by the budget ledgers, f9 pinned pair 100 SAT / 100 UNSAT, 5 SKIPPED-STOP lines rerun
  to completion. A sample bound only: by the rule of three, the 95 % upper bound on the SAT share is about 3e-5 (PLAN:243 applies it to the undecided share).
* Plain formula on symmetric maps: UNSAT-SOLVER on 36 of 36 priced (9, 5) and 23 of 33 (9, 4) at 5 s
  (E-261116-09 `CONCLUSION.md`:31-35). The 10 UNKNOWN ones were all-doubled strata (C2 m22222, m222222; C3 m222) plus
  one C3 m32. Session check D1: all 10 UNSAT-SOLVER in 4.2-24.1 s. So 69 of 69 priced nine-face maps fall to the plain
  formula. Lemma P excludes 3 maps outright (EXACT certificates, PROVED-1 reading).
* Census-free (C): P3 v2 UNKNOWN on 48 cubes; P3-sym nine faces UNKNOWN at 1 h; no refutation power at 66 / 72 orbits
  (3aw, 3bb, 3bd). P4 realizes Szilassi only (3ax).
* Arrangements (D): near-copy ninth-plane cells 0 of 2004 (3ae); the rung below found only the source map in 25531 cells
  (3ak); C3 / C2 nine-plane sampling 0 hits, p >= ~9e-4 rejected (3ay). At eight planes the D2 2 x 4 box gives 7.1 %
  solids, all with Roest-Vigh's map (`reviews/dialogue-2026-11-16-strategy.md`:102, session check).
* Earlier targets: the realization link is weak beyond known objects. The bridge realized 16 of 153 (10, 2) SAT models
  (3ah); rule: >= 30 models per SAT (STATUS:384). Two (9, 3) sieve models stayed unrealized (3az).

## 3. Finalists

Endpoint: a nine-face object with `--all-pairs` PASS, then `candidate-check`. Unaided discovery of a known map, planted
recovery (pinned planes), a SAT sign formula (CANDIDATE) and a verified new object are reported apart.

| # | Finalist | Missing link | Evidence for the link | A week decides | T D F G R | J | Cost to first discriminating result |
|---|---|---|---|---|---|---|---|
| 1 | **P6 equivelar, plain per map** (E-261117-04; README:19-27; dialogue A6, :209-218) | a realizable equivelar (9, 4) map | both known (8, 3) objects lie in the slice (D2); the face-transitive (8, 3) classes reproduce (D2); plain (9, 4) formulas take seconds (D1) | the whole slice at UNSAT-SOLVER level, against a measured (8, 3) rate | 2 2 2 1 2 (ROADMAP:177 had 1 2 1 1 2) | 2 | stage A, < 0.1 core-h, one session |
| 2 | free-C2 (8, 3) per-map symmetric pass | a third symmetric (8, 3) map | P3-sym ran 5257 s UNKNOWN after the two known maps (3bd); 788 classes never run (README:40-41) | the symmetric (8, 3) slice; the symmetric route's rung rate | 2 2 2 1 2 | 0 | < 0.1 core-h |
| 3 | C2 (9, 5) remainder, chunks 10-99 | a SAT genus-5 symmetric map | none: 0 / 97830, plain 36 / 36 UNSAT | nothing unless SAT (UNSAT-SOLVER is no negative) | 1 1 2 1 2 | 2 | ~122-129 core-h, two nights (README:126, PLAN:244) |
| 4 | plain formula on all 12562 symmetric (9, 4) maps | an asymmetric realization of a symmetric map | 33 / 33 priced UNSAT | the same, ~35-50 core-h | 1 1 2 1 2 | 2 | overlaps item 1 on equivelar maps |
| 5 | deleted-plane sources from the realized (10, 2) objects (I-261116-06) | an inherited arrangement with a new solid | none; K13 and 3ak found only known maps | the 8-plane rate | 1 2 2 1 2 | 0 | minutes |
| 6 | relaxed Szilassi-12, genus >= 7 (E-261101-08; target change) | any calibrated 12-face method | none at 12 faces | no rate in a week | 1 1 1 2 2 | 2 | >= 2 sessions |

**Order:** 1, 2 (a cheap companion that calibrates the rival route; it does not compete for the night), 3, 4, 5, 6.
Deleted-plane sources and relaxed 12 faces are the serious alternatives with a different mechanism; neither has a
rung-below rate, and the second needs an owner target change.

**Why P6 beats the C2 (9, 5) remainder.**
* Structure: genus 4 carries the fewest extra segments at nine faces (9 against 15). Every priced genus-5 map falls to
  the plain formula in under 5 s.
* Calibration: P6 has a rung with known answers inside its own slice (97 / 51 classes, both objects present, `STRATEGY.md`:63-64). The remainder has no rate for its population.
* Scope: P6 covers asymmetric realizations, which no symmetric run touches.
* Cost: about one night for P6 in total, against two nights for the remainder.

**Best argument against P6.** The evidence that closes the symmetric route also predicts P6's answer. Every priced
nine-face map, all-doubled strata included (these contain the symmetric equivelar maps), falls to the plain formula.
"Equivelar" extrapolates from two objects that are both face-transitive, and face-transitivity already fails at nine
faces (3au, 3bj). The likeliest outcome is a complete slice with every map UNSAT-SOLVER.

**What reverses the order.** If stage A returns only the two known maps while item 2 returns new realized maps, the
symmetric slice is the fertile one at the rung below. Then the C2 (9, 5) remainder, or a C2 genus-6 census, moves ahead
of P6 stage C. P6 also drops below "no night" if item 3 projects above 12 core-h or the stage-C price exceeds one night.
No night is justified yet: the item-4 night is earned only by items 1 and 3.

## 4. One-week plan (paste-ready for the lead)

1. **P6 stage A at (8, 3)** (E-261117-04 PLAN first; explore, J 0 on its own, the gate of J 2): details in §5.
   Lab: Opus, high / Codex gpt-6-astra, high (a new eight-face object is possible).
2. **Free-C2 (8, 3) per-map symmetric pass** (E-261119-02 amendment): every record of the 790-class list (one per free-C2
   group), the stage-B rung formula and runner (lean, kissat cap 30 s); controls: the f9 pair and the three known SAT
   units with `--all-pairs` PASS (README:120-124). Tree: a new SAT -> bridge (>= 30 models), `--all-pairs`,
   `candidate-check`, escalate, and E-261112-02's reopening; all others UNSAT-SOLVER -> rate 2 maps / 790 classes, the
   C2 (9, 5) remainder stays postponed with that comparison recorded. Budget <= 0.2 core-h, lab-run.
   Lab: Opus, medium / Codex gpt-6.1-sol, medium (SAT: high / astra high).
3. **P6 stage B: the (9, 4) equivelar census.** Allow 9 extra edges (`census.py:154`, `enum_multi.c:186`), re-read the
   coverage argument, one process per pattern (8), cap 12 core-h. Controls: (8, 3) rerun = 97 / 51 with both known codes;
   the Z3 x Z3 pillows (2 inadmissible classes, 3au) appear in 3+3+3; cross-enumerator check: every equivelar class of
   the E-261119-02 (9, 4) C3 / C2 lists appears, and every new class with such an action is in those lists. About 2 h
   wall, so it is an owner day run. Stop: a control or count mismatch, or a projection above 12 core-h.
   Lab: Opus, high / Codex gpt-6-astra, high.
4. **P6 stage C: the (9, 4) plain pass** over every admissible class (one orientation suffices: a mirror image realizes
   the mirror map), lean runner, 10 shards, kissat cap 60 s, the first chunk prices the rest. Projection 5-31 core-h
   (2.2k-14k classes x ~8 s, D1 median under load; NUMERICAL). Owner night if above 50 min wall. Tree: SAT -> >= 30
   models, bridge, `--all-pairs` with nine faces, `candidate-check`, escalate. TIMEOUT -> one 600 s pass. All UNSAT-SOLVER
   -> "the equivelar (9, 4) slice is UNSAT-SOLVER at formula scope" (planning only), back to the lead.
   Lab: Opus, high / Codex gpt-6-astra, high.
5. **Conclude E-261119-02's random 10 %** (`experiment-conclude`, no compute; numbers in §2). Chunks 10-99 stay postponed;
   parity and replays stay with the deferred paper. Lab: Sonnet, medium / Codex gpt-6.1-sol, medium.

## 5. First action: P6 stage A at (8, 3)

* **Run:** commit the E-261117-04 PLAN (skill `experiment-start`). Enumerate the seven 2-regular patterns with the
  committed enumerator (k = 8 is inside its cap), keep the admissible classes (expect 51), then for each class the
  plain and normalised S1 formulas at 9 elements as in E-261118-01, kissat cap 60 s, no proofs. Each SAT model goes to
  the frozen bridge with >= 30 models, and each realized file to `verify_candidate.py --all-pairs`.
* **Controls:**
  * c1, census: 97 classes and 51 admissible; the six classes with Aut+ in {8, 24} match E-261117-01's face-transitive codes; Roest-Vigh's and Mizhaev's codes match `maps/rung_8_3.json`.
  * c2, planted: Roest-Vigh's planes pinned on his own map give SAT, and on another class UNSAT-SOLVER.
  * c3, unaided: both known maps SAT and realized, (V, E, F, chi) = (24, 36, 8, -4).
  * c4: E-261118-01 classes 1-5 come back UNSAT-SOLVER again.
* **Budget:** <= 0.5 core-h and <= 50 min wall on 8-10 shards; the lab runs it after the owner's one-line permission (P1, §6).
* **Success check:** c1-c4 pass and every formula is decided. A new object counts only after `--all-pairs` PASS and `candidate-check`.
* **Stop condition:** a failed control gets one repair, then escalation. A count that differs from D2 stops the item until the session check and the enumerator are told apart.
* **If positive** (a new map SAT and realized): `candidate-check`, then escalate to the owner (D3, §6). The new object is a source for E-261112-02; item 3 stays next.
* **If negative** (only the two known maps SAT): record a rung rate of 2 in 51 (UNSAT-SOLVER, ranking only), then items 2 and 3.
* **If inconclusive** (UNKNOWN at 60 s, or a SAT model the bridge cannot realize): rerun the UNKNOWNs once at 600 s. An unrealized SAT keeps its map open; P4 at K = 32 is a second realizer only if it costs under 10 min. This does not block item 3.

## 6. Owner decisions (all open)

Status: open. On 2026-11-22 the owner chose not to decide in this session. This report is an input to the C3 comparison
and to the final review; nothing in it runs before the owner approves the final week plan
(`.claude/skills/strategy-review/SKILL.md`:53). If nothing is decided, nothing runs and the plan waits. In order of need:

* **D0. Approve the week plan** (through C3 and the final version).
  * Blocks: every item.
  * Recommendation: §4 as written. Item 5 needs no compute and may go first.
* **P1. One-line permission for item 1:** <= 0.5 core-h, <= 50 min wall, 8-10 cores (`PROTOCOL.md` §8b launch rule).
  * Blocks: P6 stage A.
  * If declined: P6 has no rung, and items 3-4 lose their power statement. Then I would not run them.
* **P2. One-line permission for item 2:** <= 0.2 core-h, <= 50 min wall, 8-10 cores.
  * Blocks: the free-C2 (8, 3) pass.
  * If declined: the symmetric (8, 3) slice stays OPEN (3bd), and the C2 (9, 5) remainder keeps no rung-below comparison.
* **D1. Census tool change and the item-3 day run:** allow 9 extra edges at `census.py:154` and `enum_multi.c:186`; one owner launch of about 2 h wall, capped at 12 core-h.
  * Why the owner: it changes an EXACT census tool whose coverage argument is PROVED-1, so the argument must be re-read and checked by item 3's controls; the run is longer than 50 min.
  * Precondition: item 1 passes c1-c4.
  * If approved: stage B lists the slice.
  * If declined: P6 stops at (8, 3), and no asymmetric nine-face slice is left on the laptop. The lead then chooses between the C2 (9, 5) remainder and parking nine faces.
  * Recommendation: approve. It is within `STRATEGY.md`:14-15 (P6 is the fallback, and neither census family advanced at genus 4).
* **D2. The item-4 night:** 5-31 core-h projected (NUMERICAL, from D1 and D3); the first chunk prices the rest.
  * Preconditions: items 1 and 3 pass, and the stage-B list has at most about 14k admissible classes.
  * If the measured price fits 50 min wall, the lab runs it after a one-line permission instead of a night.
  * If declined: the slice stays undecided. Only a SAT would have changed the plan, so the loss is the ~5 % chance, not a claim.
  * Recommendation: approve once the price is in.
* **D3. A new eight-face object** (only if items 1-2 produce one, after `candidate-check`).
  * Option (i): it counts under the filter (`reviews/dialogue-2026-11-10-strategy.md`:13) and takes the candidate-announcement path, which the owner keeps (`PROTOCOL.md` §8b).
  * Option (ii): it serves as a source and a paper item, and nine faces stay first.
  * Either way it meets E-261112-02's reopening rule, so ninth-plane Stage A over the new object becomes the lead's next proposal.
  * Recommendation: (ii), with the paper item.
* **D4. Kept as is; no action is needed now.**
  * The C2 (9, 5) remainder (~122-129 core-h) stays postponed. It returns for a decision only if item 2 finds new realized symmetric (8, 3) maps while item 1 finds none (§3, reversal).
  * Relaxed Szilassi-12 (E-261101-08) stays outside the target. It returns only by an owner target change, and it has no calibrated method yet.
  * Parity and the checked replays stay with the deferred paper.

## 7. Evidence versus judgment

* **Evidence (labelled):** 3bf, 3bg, 3bh and the local logs (UNSAT-SOLVER; EXACT census, coverage PROVED-1);
  E-261116-09 ablation (UNSAT-SOLVER) and Lemma P (EXACT certificates); 3au and 3bj (EXACT); 3bd (UNKNOWN, no power);
  3ae, 3ak, 3ay (UNSAT-SOLVER, NUMERICAL rates); session checks D1-D3 (NUMERICAL, unregistered, not ledger evidence).
* **Judgment (CONJECTURE):** genus 4 is the best nine-face genus; equivelar is the best slice; the ~5 % odds; the price
  extrapolation of D3; one orientation per class suffices for the plain formula (a geometric mirror argument,
  PROVED-1 sketch); the C2 (9, 5) remainder's low value.

## 8. Session diagnostics (<= 10 min each, <= 8 processes, scratch only; reproducible from this text)

* **D1** (one run, 25.7 s wall, 8 processes). Rebuild the 10 (9, 4) records whose ablation `plain` probe was UNKNOWN
  (indices 1, 2, 4, 7, 8, 12, 14, 15, 16, 17 of E-261119-02 `maps/pricing.json`) with `ablate.build`; every formula hash
  equals stage B's. Keep all families except SYM, SB_ORBFLIP and SB_MIRROR, then
  run `ablate.sat` at a 240 s cap. Result: all UNSAT-SOLVER. Times: 4.2 (C2f m22222), 5.2 (C3 m222), 6.1 (C2f m222222),
  6.9 (C3 b3 m222), 7.1 (C3 m32), 8.6 (C2f m22222), 9.8 (C2f m222222), 11.6 (C3 b3 m222), 16.0 (C2f m222222) and
  24.1 s (C3 m222).
* **D2** (7 processes, <= 9.7 s each). The committed `enum_multi.c` on one cycle-union pattern per input (`8 3 8 1`, edges
  of cycles over consecutive labels, a part of size 2 as a doubled edge), then `census.record`. Result: 8: 43 / 12,
  6+2: 13 / 11, 5+3: 8 / 0, 4+4: 21 / 16, 4+2+2: 6 / 6, 3+3+2: 0 / 0, 2+2+2+2: 6 / 6, so 97 classes and 51 admissible.
  Mizhaev's map is in pattern 8 (Aut+ 2) and Roest-Vigh's in 4+4 (Aut+ 8). Six admissible classes have Aut+ 8 or 24,
  which matches the five-plus-one face-transitive classes of E-261117-01 by count (not yet by code).
* **D3** (8 processes, 300 s cap each). The same with the check `extras > 8` raised to 9 in a scratch copy, at (9, 4)
  (`9 4 9 1`). Classes found / roots done of 126000: 9: 2110 / 18900; 7+2: 324 / 82896; 6+3: 729 / 17047;
  5+4: 458 / 22045; 5+2+2: 188 / 48652; 4+3+2: 143 / 74275; 3+3+3: 141 / 5224; 3+2+2+2: 11, complete in 179 s.
  * Root total: every pattern puts vertex 0 on a cycle of length >= 3 with two doubled neighbours. `rotations()`
    (`enum_multi.c`:159-175) then gives the same root count as the complete 3+2+2+2 run; this is a code reading, not a
    measurement.
  * Projection, linear in roots: about 15000 core-s (4.2 core-h), longest 3+3+3 at about 2 h, about 27000 classes as a
    crude ceiling against 4104 found. The admissible share at (8, 3) is 53 %. Uncertainty is at least 2x, since root
    cost is not uniform.

Total session compute about 0.75 core-h; nothing written outside the scratchpad except this report; no commit.
