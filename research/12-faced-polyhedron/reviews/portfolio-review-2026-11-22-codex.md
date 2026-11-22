# C2-b · Choosing the next research week

1. Give the first session to 111 nine-face maps of genus 4. Search for coordinates that may break the map's combinatorial symmetry.
2. These are the equivelar maps already present in the two symmetric census lists. Selecting them needs no new enumeration.
3. All 119 map/action records returned UNSAT-SOLVER with symmetry imposed. Only two of the 111 map codes occur in the earlier plain-formula pricing sample. Both timed out at 5 s.
4. First price the plain per-map formula on all eight extra-edge patterns. Budget one session, eight cores for at most 15 minutes after approval.
5. The endpoint is a saved nine-face object passing the exact all-pairs check. A satisfiable sign assignment earns realization work.
6. Abandon this batch if its controls fail, all plain formulas return UNSAT-SOLVER, or the pilot leaves too many timeouts for the agreed budget.
7. The best route within the existing symmetry restriction is the genus-5 C2 census. Its random tenth finished with 97,830 distinct UNSAT-SOLVER records.
8. The other 880,398 records cost about 129 core-hours at the observed rate. A unique satisfiable record had about a 90% chance of escaping the first pass.
9. Choose the small genus-4 test first because it changes a geometric assumption at low cost. The best argument for genus 5 is its complete finite list and tested pipeline.
10. Owner decision requested: allow plain realizations on this restricted genus-4 list. Keep the nine-face S1 target, defer the paper, and reserve the night budget pending the pilot.

## Evidence behind the choice

Evidence snapshot `1310847b` with its local result logs. Paths below are relative to `research/12-faced-polyhedron/`. Experiment IDs refer to their unique directories in `experiments/`. The proposed ordering, thresholds and budgets are planning judgments.

**Why these 111.** Both known eight-face controls have nine sides on each face. Their extra-edge graphs have cycle lengths 8 and 4+4. With nine faces, giving each face ten sides leaves two extra incidences per face after one edge to each neighbour. The extra edges therefore form cycles, including a length-two cycle for a triply adjacent pair. This gives a concrete family to test. Two known objects supply motivation but no nine-face hit-rate estimate. E-261117-04/README.md:17–27 also identifies the extra-edge cap that a new general census would have to change.

**Reproducible read-only count** (planning diagnostic). In E-261119-02/maps/pass1.json (SHA-256 `82faa3402b1d64a4eb1249604060629e1e4d4612e03f3a5419eeb99121be58a7`), select records whose nine cyclic links all have length ten, then deduplicate by `canonical_sha256`. The 104 C2 and 15 C3 records give 111 codes. Counting connected-component sizes of the multigraph of extra edges gives:

| Cycle sizes | 9 | 4+5 | 2+7 | 2+2+2+3 | 3+6 | 2+2+5 | 2+3+4 | 3+3+3 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Map codes | 50 | 16 | 16 | 8 | 8 | 8 | 4 | 1 |

The source records retain the action and the link order (E-261119-02/stageb.py:98–109). All 12,562 genus-4 action records were UNSAT-SOLVER on their uniform symmetric formulas (E-261119-02/README.md:53–69). Joining the 111 codes to the 33 pricing records gives indices 2 and 4. Both plain probes were UNKNOWN (E-261116-09/results/ablation/records.jsonl:6 and :8). Other priced maps were often easy even without symmetry: 23/33 genus-4 and 36/36 genus-5 plain formulas returned UNSAT-SOLVER within 5 s (E-261116-09/CONCLUSION.md:28–39). Neither timeouts nor symmetry imply that any of the 111 admits coordinates. This list omits equivelar maps outside the two combinatorial census families.

**Price of staying with symmetry.** E-261119-02/PLAN.md:220–246 fixes the seed, 5 s cap and unit. In local `results/stageB5-pass1-c000` through `-c009`, count completed integer-index records by canonical hash. All 97,830 distinct codes were UNSAT-SOLVER. Five SKIPPED-STOP entries added no distinct final record. The pinned controls gave 100 SAT and 100 expected UNSAT-SOLVER statuses across the chunks and shards. NUMERICAL timing: 14.34 aggregate shard-hours, 4.30 solver-hours, slowest solve 2.02 s rounded up. Projecting by record count gives about 129 more aggregate hours. This prices the rest. Conditional on exactly one satisfiable formula, a uniform draw misses it with probability 880,398/978,228. The sample supplies no prior for there being such a formula. These solver statuses support planning at instance scope. The census count is EXACT with PROVED-1 coverage; the genus-5 C3 list is empty in that census (E-261119-02/README.md:74–92).

**What a theorem could buy.** Collinear-segment parity is necessary for a uniform embedding (PROVED-1). On 36 priced genus-5 records, the segment equations alone contradict three maps; with the specified action they contradict 12. The corresponding certificates are EXACT. The 36 were sampled three per stratum, so 12/36 is not a population estimate. A theorem explaining rejection for an entire stratum would be a separate endpoint. No common small family of clauses was found across the priced representatives, and the published parity routine builds the full formula before elimination. An unconditional sweep of that routine has no measured time advantage. E-261116-09/CONCLUSION.md:24–51 and parity.py:90–107.

## Finalists

T/D/F/G/R score theoretical motivation, discrimination, cheap falsification, generalization and reproducibility on 0–2 (ROADMAP.md:18–23). J measures direct access to the target genus. Costs below are proposed caps or measured costs as indicated.

| Rank and route | T/D/F/G/R · J | First discriminating result and missing link |
|---|---|---|
| 1. Plain equivelar genus-4 pilot | 2/2/2/1/2 · 2 | At most 2 core-h for controls and pricing. Can one of these map codes support unrestricted signs, and can those signs be realized? A feasible batch or a model earns one bounded follow-up. |
| 2. Remaining symmetric C2 genus-5 maps | 2/2/1/1/2 · 2 | Known operational price, about 129 core-h for completion. May find a rare sign model directly. Its first useful early stop would be SAT; further sample negatives cannot resolve the singleton case. Best permitted constructive route if the owner retains geometric symmetry. |
| 3. Parity before genus-5 SAT | 2/2/2/2/2 · 2 | One session to price a direct equation builder against the reference on frozen records. It earns a place before rank 2 only if its cost per input is below the saved end-to-end cost of the rejected records. Survivors still need the geometric pipeline. |
| 4. Fixed-source cell extension | 2/1/1/1/2 · 2 | Supplies actual planes. Four exact solids in 25,531 eight-plane cells, all one known map. At nine planes 2,004 near-copy orbits gave no solid. The generic ninth-plane stage is priced around 79 core-h. To reopen, recover a deleted plane unaided with the proposed one-formula plus LP method and beat the enumeration price. STATUS.md:322–328, 369–377 and I-261117-03:12–26. |
| 5. Joint map/sign search (P3-sym) | 2/1/1/1/2 · 2 | Finds both known eight-face maps unaided in 59 and 81 s, each exactly realized. After blocking both, UNKNOWN at 5,257 s; the known-negative nine-face control also timed out. A changed search must distinguish a blocked discovery rung before a new nine-face night. E-261119-01/CONCLUSION.md:18–39. |
| 6. Geometry by construction | 1/1/1/2/2 · 2 | Tropical patchwork realizes the known Szilassi map exactly, but both eight-face controls were UNKNOWN at 90 s. A stronger matching encoding would first need an eight-face recovery. Embedded-first flattening stopped on local contacts in four valid torus starts; a changed contact treatment would first have to clear that seven-face rung. E-261117-03/CONCLUSION.md:18–45 and E-261103-06/CONCLUSION.md:14–32. |

**What reverses the order.** There is no measured enrichment for equivelarity, and the two prior timeouts could simply reflect expensive contradictions. If even the pattern-stratified plain pilot produces mostly timeouts with no model, rank 2 takes priority over a longer plain run. If the owner values completing a finite symmetric list despite solver-only negatives, rank 2 also wins. A measured parity speed-up can reduce its price. A plain SAT reverses the immediate decision in favour of realization. No scenario credence changes on a timeout or on the random tenth alone.

## Week plan for decision

1. **First action, subject to the scope decision.** Register the 111-code set and frozen order. Test one code per pattern (lowest canonical hash), plus the two priced UNKNOWN codes if absent. Use the ordinary generator-free formula (`tranche.py:151–162` in E-261103-03). Preserve cyclic link order, document orientation coverage, and retain the formula hash and SAT models. Check the same path on both known (8,3) maps without sign pins and on a previously decided plain (8,2) negative. Verify each positive control's saved coordinates with `--all-pairs`; the control maps themselves are supplied. Compare the plain clause families with the ablation reference (E-261116-09/ablate.py:100–109, 135–142). One session, eight shards/cores, 15 min wall, 30 s per target formula. A failed control stops the batch.
2. **Branch on the pilot.** One SAT goes straight to item 3. With controls passed and at least half the pilot decided, price the remaining codes from the observed whole-unit times. Complete only if projected within a further 2 core-h at the same cap, after owner permission. All UNSAT-SOLVER in the completed list closes this list for planning. With fewer than half decided, an unaffordable remainder, or only UNKNOWNs left, park the plain batch and offer item 4. Keep any unknown formulas explicitly open.
3. **On a target SAT.** Check every clause, decode, and run the existing bridge. Stop on exact `verify_candidate.py FILE --all-pairs` PASS with nine faces, followed by `candidate-check`. If the first bridge misses, price the registered many-model approach (at least 30 distinct models per SAT map when available) against a separately agreed cap. Without a verified embedding, retain the model and record the unresolved realization. E-261103-03/tranche.py:165–181 and E-261114-02/CONCLUSION.md:13–20.
4. **If scope stays symmetric or the plain test stops.** Price direct segment parity on a held-out, proportionally sampled batch of genus-5 codes after reproducing the saved contradiction certificates and preserving known realizations. Include formula construction, I/O, checking and skipped-solver savings. Cap 1 core-h over eight shards. If the projected total cost falls, use parity before the remaining symmetric formulas. Otherwise offer the unchanged ~129 core-h sweep to the owner. An inconclusive price earns no night. The owner's launch decision remains separate. No proof replay is budgeted.

Use Opus high / Codex gpt-6-astra high for formula scope, certificate equivalence and any SAT conclusion. Routine batch accounting can use Sonnet medium / Codex gpt-6.1-sol medium. Use committed plans and the owner's laptop launch limits (STRATEGY.md:39–40). The full asymmetric equivelar census remains an unpriced fallback; the existing 111 codes bypass its enumerator cap only for this restricted pilot.

## Inventory coverage

The graph and the individual idea and hypothesis files have the same IDs. All 176 ideas (117 open, 46 tried, 13 parked) and 41 hypotheses (28 open, 6 weakened, 5 supported, 1 proved, 1 refuted) occur exactly once below. The experiment index has 114 entries (84 done, 22 planned, 5 parked, 2 killed, 1 running). Historical status is retained; an open record alone does not earn compute. The last column counts open ideas and hypotheses together. For example, I1029:42 expands to I-261029-42. The rankings above distinguish variants that materially change the decision.

| Mechanism | IDs | Ideas / hypotheses / open |
|---|---|---:|
| Maps | I1029:42,49 I1030:18,19,31 I1101:15 I1108:08 I1110:06 I1114:01 I1117:01 I1118:02 I1119:01,03 H1103:01,02,03 | 13 / 3 / 7 |
| Obstructions | I1029:02,15,16,23,24,41,52,58,61,62 I1030:23 I1101:02,10,13,14,16 I1108:01,06,09,10 I1110:04 I1116:07 I1118:03 H1029:04,06,08,10 H1101:02,11,13,14,15 H1110:01 | 23 / 10 / 26 |
| Joint signs | I1029:11,12 I1103:02 I1118:01 I1119:02 H1101:17 | 5 / 1 / 4 |
| Realization | I1029:10,45,48,50,57 I1030:32 I1101:05,21 I1114:02 H1101:12 | 9 / 1 / 9 |
| Fixed source | I1103:04 I1112:01 I1113:03 I1116:06 I1117:03 H1112:01 | 5 / 1 / 5 |
| Plane families | I1029:04,06,14,27,51,60,63 I1030:01,07,08 I1101:08,20 I1103:03,06 I1108:03 I1110:01 I1113:04 I1117:02,04 H1029:02,05 H1101:08 H1110:02 | 19 / 4 / 17 |
| Surface first | I1029:05,26 I1103:01,05 I1108:11 I1116:01 I1118:04 | 7 / 0 / 4 |
| Handles and normals | I1029:01,03,07,17-21,55 I1030:02,03,05,12-16,20-22,24-28,30 I1031:05 I1101:01,03,04,09,11,19 I1114:04,05 H1029:01,03,09,11 H1030:01-05 H1101:03,04,09,10,16 | 35 / 14 / 30 |
| Search objectives | I1029:08,09,13,22,29-40,46,59 I1030:17 I1102:01 | 20 / 0 / 10 |
| Decision tools | I1029:25,28,43,44,47,54,56 I1030:29 I1031:01-03 I1101:12,18 I1108:02,04,05 I1110:05,07 H1029:12 H1101:06 | 18 / 2 / 15 |
| Other targets | I1029:53 I1030:04,06,09-11 I1101:07 I1110:02,03 I1113:01,02 I1114:03 I1116:02-05 H1029:07 H1101:01,07 H1110:03 | 16 / 4 / 12 |
| Evidence and process | I1031:04,06 I1101:06,17,22 I1108:07 H1101:05 | 6 / 1 / 6 |

**Disposition of the remaining families.** Map enumeration supplies the 111 inputs. Face-transitive nine-face maps at genera 4 and 7 have already failed admissibility (EXACT enumeration, coverage PROVED-1, E-261119-03/CONCLUSION.md:27–38). For obstruction methods, the one-face contraction systems are all satisfiable on the 203 genus-3 maps; this limits that grouping, whereas the segment-parity witness couples faces (E-261109-05/CONCLUSION.md:17–25). Filtering and realization tools remain conditional on a construction they can advance. Deletion can make a relaxed formula SAT without restoring the missing face (H-261101-07:98–101).

Plane families can produce coordinates directly. The frozen symmetric nine-plane boxes returned no all-pairs solid in 63.8 core-h with 10–19% UNKNOWN; a new family needs its own eight-plane rate (NUMERICAL, STATUS.md:497–505). Handle surgery can reach both eight-face control maps combinatorially, but geometric continuation lost simplicity on both. Fixed-normal and search-objective variants have mostly been tested on S0, where a zero closure defect still left at least 11 nonsimple faces in nine examples (STATUS.md:83–90, 223–234). They have no demonstrated route through the eight-face geometric rung at this budget. An untested general curvature bound or an improved solver could matter if it gives a new necessary condition or changes a measured price.

Other-target and process entries include the solver-only (10,4) decisions, closed laptop (11,5) route, deferred S6 replay, S0 pricing, external review and write-up. Their endpoints or compute requirements differ from this week's approved target (STRATEGY.md:20–44). The public negative note stays deferred. A successful control, an abstract map, a solver status and an exactly verified new geometric object each answer a different question (SPEC.md:72–89).
