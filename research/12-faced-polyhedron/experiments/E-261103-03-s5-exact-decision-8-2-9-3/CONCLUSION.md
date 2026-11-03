# E-261103-03: (8,2) pilot conclusion

2026-11-04. Partial conclusion: the (8,2) stage is complete; the bounded (9,3) paired pilot is now complete (see the appended section); wider coverage is unfinished.
Pre-registration ac2ad98; computation c48ab73 on this experiment branch, clean tree.

## Controls, resources and predictions

Recorded pilot: 35.579626 wall seconds, 0.009883229479 core-hours,
one worker, 900-second computational budget. Control recheck: 0.556527 wall seconds,
0.000154590822 core-hours. Total of the two manifests:
0.010037820301 core-hours. Development and regression commands, including
proof replays, are not part of these resource totals. No laptop night, Actions run or (9,3) target solve.

Both own pinned Roest-Vigh and Mizhaev formulas are SAT, with clause-by-clause checked models.
Hinge and two-stage realizers recover both supplied chirotopes, each with and without supplied planes:
eight exact sign matches, wrong_signs = 0, EMBEDDED True. The separate verify_candidate --all-pairs
recheck passes for all eight (S1 controls, F=8,g=3; these are not maximal S5 objects).
The cross-map pinned negative is UNSAT with checked DRAT. All 37 inadmissible census maps are rejected.
No floating diagnostic enters the verdict.

| Formula | Solver seconds | Status | Scope |
|---|---:|---|---|
| map0_plain | 5.261121 | UNSAT-VERIFIED | full plain embedding formula for census map 0 |
| map0_C2 | 0.020651 | UNSAT-VERIFIED | uniform free-C2 ansatz for map 0 |
| map1_plain | 12.393358 | UNSAT-VERIFIED | full plain embedding formula for census map 1 |
| map1_C2 | 0.020887 | UNSAT-VERIFIED | uniform free-C2 ansatz for map 1 |

Exact timings and fractions are in results/pilot/summary.json. Each SAT-call budget was 60 s;
all ended by completion, not by the timeout. The registered prediction (at least one plain formula
finishes within 60 s) holds, and controls have power at this size. There are no target SAT models,
so no target realization, final-polynomial computation or candidate-check was needed.

## Evidence and claim boundary

**EXACT:** four saved formulas are UNSAT with retained DRAT checked by drat-trim.
The new verify_all quick check re-encodes the formulas, compares their SHA-256, validates original
artifact hashes, rechecks recovered control signs/geometry, and replays the proofs when drat-trim
is installed. Without that binary it checks hashes and the saved verified checker transcripts;
that portable mode is not a fresh proof check. No target formula is inferred from a symmetry-only
contradiction: both plain formulas were solved independently.

**PROVED-1, conditional geometric conclusion:** the two admissible census maps admit no uniform
embedding chirotope satisfying the encoder. Combining these exact decisions with E-261103-01's
coverage argument, repeated-corner exclusion, and E-261103-02's open-realization/general-position
and multi-segment encoding arguments excludes S5 (8,2) under those unreviewed arguments.
The chain is: solver UNSAT -> retained CNF/DRAT -> independent DRAT checker accepts ->
PROVED-1 census/encoding interpretation. This session adds no human mathematical review or
independent second encoder, and does not upgrade the statement to CERTIFIED.

Both C2 decisions concern only their uniform free-C2 formulas and are redundant for the plain-map
conclusion. No fixed-face C2/D3 family was tested. No result about (9,3), (10,4) or S0 follows.
NONREALIZABLE-EXACT of a future model must exclude that model only, never a whole map by itself.

## Review corrections and reproducibility

A short code review identified a possible false recovery through realize2's supplied-plane fallback.
Post-run code requires wrong_signs = 0 as well as exact sign matching. Every saved recovery already
has wrong_signs = 0, so the recorded gate remains valid without recomputation. Regression tests reject
the fallback. The main-process alarm was added after the run; the original run used subprocess
bounds and cooperative deadline checks. PLAN amendments preserve that distinction.

An initial control-export check failed because verify_candidate requires a links object, not an
array (AttributeError: 'list' object has no attribute 'items'). The export and future candidate
writer were corrected; all eight exported controls then passed. Original pilot artifacts are unchanged.
The regression tests also exercise real process timeout, the Python deadline alarm, and rejection of a damaged DRAT proof.
Raw solver/checker transcripts retain their original whitespace and carriage returns: unrestricted
git diff --check flags them. Source/document diff checks exclude results and pass; evidence bytes
are not normalized after hashing.

## Hypotheses, verdict and next step

H-261103-03 is supported by the two plain UNSAT decisions (EXACT formulas, geometric interpretation
PROVED-1). The genus-2 case of H-261101-07 is excluded at that conditional level; genus 3-5 stay open.
H-261103-02 is unchanged: no (9,3) instance was run. The S5 (8,2) scenario becomes OM-UNSAT conditional
on the existing census/encoder arguments; this does not assign human-reviewed theorem status.

Verdict: **FOUNDATION** for the small-case exact pipeline and a conditional negative (8,2) result.
E-261103-03 remains running because its (9,3) stages are unfinished; there is no active process.
No longer run is needed for (8,2). Next: commit a new PLAN amendment for the eight free-C3 (9,3)
formulas, with plain fallback coverage and the registered affordability gate, before target compute.
The scenario change triggers the standing strategy-review requirement in a separate session;
no strategy review or focus change is performed here. No push, PR, archive check or GitHub CI.

## Final local verification

verify_all.py --quick: ALL PASS (18 checks, archive skipped), including saved formula
reconstruction and fresh drat-trim replay. Five dedicated runner regressions pass.
Source/document git diff --check passes with raw results excluded; the unrestricted check
reports only preserved solver/checker transcript whitespace. GitHub CI was not run.


## 2026-11-04: paired C3/plain (9,3) pilot

Pre-registration bc0ae0e; corrected panel/controls/first-SAT stop pre-registered in 0db8d8e.
The first attempt used the stale hand-over before review 69caae8 was noticed. It was stopped
by SIGINT during map1_plain (manifest ERROR / KeyboardInterrupt). Its artifacts were retained;
no formula was retried. The continuation inherits three completed decisions and one interrupted
call, then finishes the corrected purposive panel: pairs 0..7 and plain 10/30/40/48.
Actual dispatch differs from the review's proposed order because map 1 had already started.
All six extra-edge patterns are covered; this is not an unbiased runtime sample.

Both attempts together: 622.250497958 wall seconds, 0.172847360544 core-hours (one worker), below the 1 core-hour cap.
These are the sum of the run manifests, including failed-attempt time and repeated controls;
preparation, lossless packing and subsequent verification are separate, not estimated run time.
The continuation spent 561.971181625 seconds. No night, push, PR, target model enumeration or long run.

Required controls pass: own pinned Roest-Vigh/Mizhaev SAT, both warm and unseeded exact
reconstructions with wrong_signs=0 and EMBEDDED; cross-map negative UNSAT-VERIFIED;
inadmissible-map and malformed-pairing guards; rebuilt/replayed saved (8,2) proofs;
nine-plane definitions/GP pinned SAT and exact predicate/geometry agreement; free-C3
arrangement pinned SAT. The nine-plane/C3 controls are arrangements, not S5 (9,3) embeddings.
No float diagnostic enters the verdict. There is no target SAT, realizer or final-polynomial run.

| Plain map index | Solver seconds | Outcome / binding limit |
|---|---:|---|
| 0 | 30.005248 | TIMEOUT / solver_timeout |
| 1 | not separately recorded | INTERRUPTED / panel_correction |
| 2 | 60.006014 | TIMEOUT / solver_timeout |
| 3 | 60.011203 | TIMEOUT / solver_timeout |
| 4 | 60.015539 | TIMEOUT / solver_timeout |
| 5 | 22.514486 | UNSAT-VERIFIED / completed |
| 6 | 27.000345 | UNSAT-VERIFIED / completed |
| 7 | 60.014110 | TIMEOUT / solver_timeout |
| 10 | 60.005450 | TIMEOUT / solver_timeout |
| 30 | 30.386661 | UNSAT-VERIFIED / completed |
| 40 | 60.008245 | TIMEOUT / solver_timeout |
| 48 | 60.009194 | TIMEOUT / solver_timeout |

All eight C3 formulas are UNSAT-VERIFIED, in 0.071..0.256 solver seconds, with retained
CNF/DRAT and accepted drat-trim checks. Plain: three UNSAT-VERIFIED (5,6,30), eight TIMEOUT,
one INTERRUPTED. The first plain timeout used 30 seconds; subsequent timeouts used 60 seconds.
The interrupted call has no measured standalone duration and is not counted as a timeout.
Completed plain solver calls took 22.514..30.387 seconds; checker time is additional
(the checker logs record it, but summary.seconds measures the solver only). C3 calls
ended by completion, eight plain calls by solver cap, and one by the documented panel correction.
The global deadline did not bind. The pre-registered stop was exhausted panel, without target SAT.

The corrected prediction of at least one plain completion holds; at least six of twelve fails
(only three complete). The earlier four-C3-decision prediction holds. Mixed/censored times
support no aggregate speedup estimate and no whole-census runtime extrapolation. Warm and
unseeded known-object controls pass, but construction power at nine planes remains unknown.

**EXACT, instance scope:** eleven saved formulas have independently accepted DRAT proofs.
The quick verification reconstructs the panel formulas and compares CNF hashes, validates run
artifact hashes, repeats the nine-plane exact predicate comparison, and replays completed proofs
when drat-trim is installed. The two original and continued manifests retain their source provenance.
Compressed CNF/DRAT bytes are lossless: packing.json records packed and original hashes;
original output hashes refer to decompressed bytes. Partial timeout/interruption proofs are retained
locally with hashes but excluded from git bulk; they support no negative claim. CNFs and completed
proofs are kept in git. Portable verification skips absent partial proofs only, never a completed proof.
Without drat-trim it checks saved accepted transcripts/hashes rather than claiming a fresh proof replay.

**PROVED-1, conditional interpretation:** plain decisions exclude uniform embedding chirotopes
for maps 5,6,30 under the existing encoder/general-position arguments; those arguments lack human
review. Eight C3 negatives exclude their exact uniform cooriented ansatzes. This is not a geometric
C3-family exclusion without equivariant general-position/coorientation/coverage arguments, and
never an asymmetric exclusion of those eight maps. No CERTIFIED theorem, S5 witness, (9,3)
non-existence statement or S0 result follows. The remaining plain formulas are unresolved.

H-261103-02 stays open: its uniform C3 ansatz is weakened, geometric-family interpretation needs
review. H-261101-07 stays open for genus 3-5; H-261103-03 retains the prior (8,2) evidence.
No existence credence change is inferred from a timeout or the number of easy formulas.
Verdict: useful cheap symmetry-ansatz decisions, partial plain coverage; no automatic full sweep.
Next decision: a separately registered 60/300-second paired grid on at most four unresolved plain
maps (the 30-second timeout and interruption must be identified as such), or an exploration pilot
from the strategy review. A night/full-census launch has not passed its gate. E-261103-03 stays
running only because wider plain coverage remains unfinished; no process remains active.

### Local verification after the paired pilot

verify_all.py --quick: ALL PASS (18 checks; archive skipped). Its saved S5 evidence check now
also reconstructs and replays the paired (9,3) evidence through EvidenceTests. The dedicated
paired evidence test passes; six runner regressions pass. Selected text artifacts contain no
Cyrillic; source/document diff checks pass. Raw checker/solver whitespace is preserved.
GitHub CI and the full archive were not run. Completed proofs and CNFs are versioned; the nine
large partial proofs remain local, listed by packing.json with their hashes. No external upload.
