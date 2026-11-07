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

## Conditional free-C3 coverage argument (draft, 2026-11-04)

**PROVED-1, single-author draft, not independently reviewed.** This addresses the extra C3-specific
coverage obligations raised in the strategy review. It assumes the existing census coverage,
nondegenerate face-plane openness, and encoder soundness arguments. It does not upgrade the
ledger to CERTIFIED or silently reinterpret a formula decision as an unconditional theorem.
The family here is proper order-three rotations acting freely on all nine faces; fixed-face
order-three actions and other symmetry groups are outside this statement.

1. Conjugate a putative proper order-three Euclidean rotation by a rigid motion so that its axis
   passes through the origin and its linear part is the cyclic coordinate permutation R, or R^-1.
   On each of the three free face orbits choose one homogeneous plane vector h and propagate it
   by R. This chooses compatible coorientations without imposing extra geometric conditions:
   R^3=I closes each orbit. Thus the parameter space is three arbitrary four-component seed
   vectors, an open part of R^12, with h_(p i)=R h_i and infinity fixed. Proper rotation gives
   chi(p S)=chi(S). Inverting p gives the same subgroup and same invariance constraints.

2. For any specified three disjoint 3-cycles p, every determinant of four rows drawn from the
   nine planes and infinity is a polynomial in those twelve parameters. None is identically
   zero: the saved exact C3_control.input.json supplies one simultaneous uniform arrangement
   for one such p, and relabeling transports it to every free action of cycle type 3+3+3.
   An independent Leibniz expansion rechecks all 210 determinants as nonzero and verifies the
   actual coordinate action. A finite product of nonzero real polynomials has zero set with
   empty interior. Uniform configurations are therefore dense in this equivariant parameter space.
   Intersecting with the relatively open neighborhood of a nondegenerate embedding of its fixed
   paired-link map yields a symmetry-preserving uniform embedding. This step depends explicitly
   on the existing face-plane openness argument, extended to paired multiple segments; it is not
   inferred from the arrangement control being an embedded target (it is not).

3. The orbit reorientation gauge loses no geometry. Changing a seed vector's sign changes all
   three vectors in that orbit. On an infinity quadruple its sign changes by the parity of the
   number of entries from that orbit. The three INF-quadruples consisting of one entire orbit
   have the three unit parity vectors. Hence the parity map has rank three; any basis chosen by
   orbfix_quads permits making its three signs positive independently. Whole-orbit reorientation
   preserves the cooriented C3 relations.

4. The finite-quadruple mirror gauge is compatible with those INF signs and the fixed R. Reflect
   space in the plane perpendicular to the rotation axis, a determinant-minus-one map commuting
   with R, then negate every finite plane vector. A four-finite-row determinant changes sign;
   a three-finite-row plus infinity determinant does not. Thus chi(0,1,2,3) can be made positive
   while retaining every orbit-gauge sign and C3 invariance. For R cycling x,y,z this operation
   has the exact integer formula h=(a,b,c,d) -> (2s-3a,2s-3b,2s-3c,-3d), s=a+b+c,
   after a positive scale of three. The independent control checks all determinant signs before
   and after this transformation. No symmetry-fixed C2 or D3 normalization is used.

5. On the saved eight free-C3 maps, Aut+ has order three or six. Sylow's count gives a unique
   subgroup of order three in either case (its count divides one or two and is one modulo three).
   The stored generator preserves the actual cyclic links and segment pairing; its inverse
   generates the same subgroup. Thus one subgroup per such map covers its free order-three
   actions, conditional on the census/isomorphism coverage already claimed at PROVED-1.
   An orientation-preserving ambient rotation of an embedded closed orientable surface preserves
   the boundary orientation of its bounded side, so its map action belongs to Aut+.

Conditional consequence: accepting those premises and this draft, the eight checked formulas
exclude this free-face proper-C3 geometric family at PROVED-1. Asymmetric realizations of the
same maps, fixed-face actions, C2/D3 families, and arbitrary (9,3) existence remain outside the
consequence. The conservative ledger continues to distinguish exact formulas from this draft
until its premises and argument receive external review. No new target SAT call was used here.


## 2026-11-04: autonomous 60/300-second grid conclusion

Pre-registration/computation source: 8f8132c. One worker, 3300-second computation ceiling;
results/grid_9_3 preserves the manifest, full inputs, models, CNFs, full/partial DRAT and logs.
Recorded wall seconds: 989.340322667; core-hours: 0.274816756296. The five experiment manifests, including the
original (8,2) pilot, control recheck and interrupted paired attempt, sum to 1647.726973708 wall seconds
and 0.457701937141 core-hours. Preparation, packing and regression/proof replays are outside those measured
run totals. No target solve or result directory was overwritten.

Required controls pass, including warm and unseeded known-object reconstructions, exact nine-plane
predicates, free-C3 arrangement, pairing/admissibility guards and saved (8,2) proof replay. This
calibrates the pipeline, not target construction power. Launcher stderr was `nice: setpriority:
Operation not permitted`; the job continued at its inherited priority. launcher.log retains that
output. One worker and the numerical thread limits were applied; no lowered nice priority is claimed.

| New cell | Solver seconds | Checker seconds | Outcome |
|---|---:|---:|---|
| map0_plain_t60 | 60.007075 | not run | TIMEOUT |
| map1_plain_t60 | 60.009009 | not run | TIMEOUT |
| map0_plain_t300 | 300.015313 | not run | TIMEOUT |
| map1_plain_t300 | 300.012950 | not run | TIMEOUT |
| map40_plain_t300 | 75.728226 | 62.166003 | UNSAT-VERIFIED |
| map48_plain_t300 | 62.514461 | 44.730775 | UNSAT-VERIFIED |

The prior 60-second cells of maps 40/48 were reused as baseline, not rerun. Maps 0/1 receive
complete 60-second cells in place of the earlier 30-second/interrupted observations; both remain
unresolved at 300 seconds. The two new plain decisions pass independent DRAT checking. Solver
and checker costs are distinct: map 40's proof check itself exceeds 60 seconds. A later tranche
must budget proof replay separately, not call the solver timing the total decision cost.
The binding limit on four new calls was solver timeout; the other two completed with checked proof.
No hard global cap or model/iteration limit bound the run. Stop: exhausted prescribed grid.
There was no target SAT and therefore no target realization/final-polynomial processing.

**EXACT, instance scope:** two additional saved plain formulas, maps 40 and 48, are UNSAT-VERIFIED.
The quick suite reconstructs each new CNF and its clause hash, validates the baseline and artifact
hashes, and replays completed proofs when drat-trim is available. Both limits of a given map have
the same clause formula; comments/cell names are not treated as semantic changes. Portable mode
without drat-trim validates hashes and accepted saved transcripts, not a fresh proof replay.
Compressed files retain decompressed original hashes in packing.json. Large partial proofs are
local-only; they support no negative assertion and need not be downloaded by portable verification.

Cumulative (9,3) plain coverage: five verified formulas (5,6,30,40,48), seven attempted maps still
unresolved (0,1 at 300 seconds; 2,3,4,7,10 at 60 seconds), and 191 admissible maps not attempted.
All eight C3 formulas remain checked ansatz negatives. These are thirteen distinct checked (9,3)
formulas, not thirteen excluded geometric maps. The same **PROVED-1 conditional** encoder/census
interpretation applies; arbitrary (9,3) existence and S0 remain open. The C3 coverage draft above
has only single-author/AI review, not independent human validation.

Both grid predictions hold: at least one new decision, and at least two of four selected maps
complete by 300 seconds. This permits assessing a bounded coverage tranche; it does not establish
a median cost for the full census. Two selected maps remain censored and the panel is purposive.
Verdict: **PROMISING for bounded additional plain coverage at the measured budget**, with the
unresolved tail explicitly retained. No full-sweep or geometric non-existence conclusion.
H-261103-02 and H-261101-07 remain open; H-261103-03 retains its earlier conditional evidence.

### Costed next tranche proposal, not an executable pre-registration

The registered grid decision explicitly retains the explore-before-tranche condition of the
strategy review (section 5, E-261103-05). That control pilot is a separate experiment and has not
run. E-261103-03 remains running, with no active process; the next coverage stage is not launched.
This is a scientific scheduling gate, not an unrequested approval to publish or push.

After that gate is concluded, propose the first 80 previously unattempted admissible maps in saved
census order, excluding all previously dispatched plain maps. No retries of checked formulas and
no unchanged repeat of the hard tail. Use solver <=60 seconds and independent proof checker <=120
seconds per map, calibrated by the observed proof cost. Worst-case target solver/checker work is
4 core-hours. Eight one-worker shards would receive at most ten maps each, a control allowance of
300 seconds, first-SAT processing <=360 seconds, and setup/report allowance <=300 seconds; the
conservative tranche bound is below 6.2 core-hours and the review's 10-core-hour ceiling. Numerical
threads remain one per worker, at most eight workers total. A target SAT stops further dispatch
and gets the existing exact model/candidate pipeline. No inference uses unchecked proofs/timeouts.

This proposal needs its own committed PLAN activation, deterministic frozen queue, bounded
checkpoint/resume runner and a same-path pilot after the explore gate. No multi-hour session job,
night, push, PR or external proof upload is started. The remaining maps cannot be called decided.

### Internal review

A small read-only reviewer pass found no significant issue in the grid time bounds, baseline and
skip-decided logic, or conditional C3 argument. It ran no solver and changed no files. It is an
AI-session filter, not an independent mathematical reviewer and not a CERTIFIED upgrade.

### Final local verification after autonomous follow-through

verify_all.py --quick: ALL PASS (18 checks; full archive skipped). The saved S5 evidence check
includes the new grid, fresh DRAT replay, baseline/CNF reconstruction, and the independent exact
C3 determinant and mirror-gauge controls. Seven bounded runner regressions pass; research graph
has no link errors. Source/document diff checks and selected text-artifact English checks pass.
Raw solver/checker transcript whitespace is preserved. No GitHub CI, full archive, external human
review or external artifact publication was performed.

### Dependency update after the explore pilot

E-261103-05 has now concluded its registered R2/R3 explore prerequisite (STATUS 3g).
The costed coverage proposal above can proceed to a committed activation and bounded same-path
pilot; no E-261103-03 coverage computation was performed in that explore session.


## New-map coverage activation and same-path pilot (2026-11-04)

Pre-registration c707bc5, source 697e3e5, branch Codex/s5-coverage-tranche from 9f9f898.
The E-261103-05 explore prerequisite was already concluded. The frozen tranche_queue.json
contains the first 80 previously unattempted admissible maps, excluding all twelve previously
dispatched plain maps. Its new budget is solver 60 seconds, checker 120 seconds, at most eight
single-worker shards, with a persistent conservative ceiling below 6.2 core-hours.

### Observed pilot and controls

The registered same-path pilot used one shard on maps 8 and 9. Both calls ended by the intended
60-second solver timeout (60.007556 and 60.010907 seconds); no target SAT, UNSAT decision,
proof-check call or geometric candidate occurred. These are unresolved instances, not negative
mathematical results. Each map retains its CNF, partial DRAT and raw solver transcript with hashes.
Artifacts: results/coverage_pilot/0/attempt_98a31f50327c40b6aeab9018e20eac1b/.

All required controls pass: pinned known-object SAT assignments, both warm and unseeded
reconstructions (construction_power CONTROL-PASS), checked cross-map negative, inadmissibility
and malformed-pairing guards, saved (8,2) proof replay, exact nine-plane predicate/GP positive,
and the uniform free-C3 arrangement positive. Controls supply exact formula/geometry checks;
they do not supply a positive geometric S5 (9,3) object. No float diagnostic enters a verdict.

Manifest: 141.988871541 wall seconds, 0.039441353206 core-hours, including the run's controls,
setup and evidence hashing. A subsequent same-command resume prints "no pending units;
recorded units skipped", dispatches no target and creates no new measured attempt. Regression
checks, proof replay and post-run packaging are outside the measured run totals. All six
experiment manifests now sum to 1789.715845249 wall seconds, 0.497143290347 core-hours.
The sandbox printed "nice: setpriority: Operation not permitted"; the short pilot proceeded
at the sandbox's default priority. The laptop wrapper still requests nice priority. The
DRAT tool's source commit is unknown; its binary SHA-256 and raw version/help output are retained.

### Coverage, decision and limits

Cumulative plain census coverage is five UNSAT-VERIFIED formulas (5,6,30,40,48), nine
attempted/unresolved maps (0,1,2,3,4,7,8,9,10), and 189 unattempted admissible maps. All eight
previous uniform C3 decisions remain checked. No new exclusion, target SAT or focus witness.
EXACT remains scoped to checked saved formulas; geometric interpretations remain conditional
PROVED-1. Existence hypotheses and scenario credences are unchanged. S0 is untouched.

The launch gate passes for controls, timeout binding, evidence retention and resume. The
prediction of at least 20 affordable decisions in the frozen tranche is still untested; two
censored calls cannot estimate its yield or any median speedup. This is readiness for a bounded
coverage measurement, not evidence that its yield will be high. The owner can launch the remaining
78 units; production imports the two pilot checkpoints and charges their resources against the
same ceiling. No automatic retry of the old hard tail or either new timeout is permitted.
A first target SAT atomically halts new solver dispatch and enters only its bounded model study.
No tranche, night, push, PR or external upload was launched from this session.

### Implementation review and regression evidence

A bounded read-only AI review found four runner issues before the pilot: orphan nested solver
processes on stop; a race between SAT-latch checking and solver spawn; missing ALL_OPTS source
identity; and repeated/overwritten interrupted SAT stages. All were corrected with failing-then-
passing tests. Cleanup now cascades SIGTERM through nested wrappers before a SIGKILL fallback;
a real nested-process test confirms the solver is reaped. The shared lock covers actual solver
spawn. Formula options are hashed. SAT stages checkpoint fresh artifact directories and charge
an interrupted stage's allocation without retrying it. This is an AI code-review filter, not
an independent human mathematical review or a CERTIFIED upgrade.

Post-pilot integration imports completed pilot units into production, includes pilot resource
accounting, and reports a saved failure stop as an error rather than an empty completed queue. The original run's source/proof provenance is retained. The saved CNFs rebuild exactly
from current source, and the inheritance regression passes without another target call. The runner
refuses source/input drift and a previous control/error stop; an interrupted unit gets a fresh
attempt directory. A torn final checkpoint is truncated without rewriting completed bytes.

Local verification: 19 tranche/evidence tests and seven existing runner regressions pass;
verify_all.py --quick ALL PASS (20 checks, full archive skipped). Checked evidence is replayed,
new saved CNFs are reconstructed, and all retained small artifacts are hashed. CNFs and small control proofs are packed losslessly using the existing gzip artifact pattern.
Original raw files remain local; large timeout proofs remain local and untracked, with recorded SHA-256. Not checked: a real concurrent eight-
shard run, target-SAT realizability, the full archive, external human review, or GitHub CI.

## Owner-run new-map tranche concluded (2026-11-04)

The frozen queue is complete. Canonical outcomes, coverage and measured costs are in STATUS
section 3i; per-unit hashes and per-attempt manifests are indexed by results/tranche_audit.json.
All production controls pass, including construction_power CONTROL-PASS. Every recorded output
hash matches. Completed UNSATs retain CNF, DRAT and successful checker transcripts. The audit
also reconstructs new UNSAT clause formulas and replays their proofs; audit time is separate
from the registered run cost. No target SAT occurred, so no target model/realizer/FP stage ran.

The registered affordable-decision prediction failed. Verdict: LOW-YIELD for this queue at
its measured budget, not a refutation of the method. EXACT instance evidence adds checked
plain formulas; the census/encoder geometric interpretation remains conditional PROVED-1.
Timeouts provide no negative evidence. Arbitrary (9,3) existence and S0 remain open.
H-261103-02 and H-261101-07 stay open; H-261103-03 retains its earlier (8,2) evidence.
No foundation or witness row changes and no CERTIFIED upgrade.

All final shards reached SHARD-COMPLETE. Earlier INTERRUPTED attempts are retained and charged;
resume did not duplicate completed units. UTC timestamps and monotonic elapsed costs show no
obvious long sleep gap, but no OS sleep telemetry was collected. Partial timeout proofs remain
local; no release, upload, push or PR was made. Do not automatically rerun this queue, expand
coverage, or retry the hard tail. The broader experiment stays running with incomplete census
coverage; the next queued exploration is E-261103-04, subject to experiment-start.

Routine conclusions now reuse hash-bound successful proof checks. Saved-evidence tests default
to integrity/transcript checks; REPLAY_DRAT=1 explicitly requests fresh audit replay. Initial
proof checking remains mandatory. Missing provenance, changed inputs/checker or suspected
corruption requires investigation/replay rather than silently accepting stale evidence.

Verification: all new target proofs passed the explicit fresh audit (recorded in tranche_audit.json).
The revised saved-evidence path passes 34 focused tests using hashes/transcripts by default;
its opt-in/missing-tool behavior is regression-tested. Initial proof acceptance and rejection
controls still run. No full archive, GitHub CI or external human review was performed.

Final verify_all.py --quick: ALL PASS; full archive skipped.

Commit packaging: numeric-shard CNFs, completed target proofs and small control proofs are
stored as lossless gzip; results/packing_tranche.json binds raw and compressed SHA-256 hashes.
Large completed proofs are local-only, as marked in that index; git retains their hashes and
successful checker/audit transcripts. External certificate publication is still pending.
Each compressed stream was checked against its original before removing the redundant raw copy.
Large partial proofs remain local and ignored; manifests and resource guards are retained.
The stale launch.pids file was removed after acquiring every shard lock; lock files remain
local and ignored. No solver or proof replay was repeated for packaging.
