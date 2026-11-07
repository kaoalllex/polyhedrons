# E-261103-05: disk-aware solid-first explore pilot

2026-11-04. The registered R2/R3 pilot is complete. Focus remains S5 (9,3); no nine-plane
focus arrangement was run, and this is not an S5 witness or a 12-face solution.
Pre-registration/computation source f9b9744, on a branch inheriting 7509f39. Original pilot
artifacts are immutable; post-run canonical exports/rechecks are separate.

## Predictions, controls and resources

Both registered predictions hold. Roest-Vigh and Mizhaev are recovered from their own planes
without hints or fixed occupancy, with exact topology and the expected paired cyclic links.
The sampler then finds an auxiliary (8,3) solid at D2 seed 4; seeds 0..3 have completed
INFEASIBLE CP models. The run stops at its first positive, so seeds 5..15 and every 60-second
cell were not run. This is a purposive finite catalogue success, not an estimate of a success rate.

| Unit | Solver seconds | Status | Exact geometry |
|---|---:|---|---|
| negative_tetra | 0.001391 | INFEASIBLE | not applicable |
| roest_vigh_15 | 1.320000 | OPTIMAL | EMBEDDED |
| mizhaev_15 | 1.300000 | OPTIMAL | EMBEDDED |
| d2_seed0_15 | 1.608476 | INFEASIBLE | not applicable |
| d2_seed1_15 | 0.703477 | INFEASIBLE | not applicable |
| d2_seed2_15 | 0.839676 | INFEASIBLE | not applicable |
| d2_seed3_15 | 1.207082 | INFEASIBLE | not applicable |
| d2_seed4_15 | 1.280000 | OPTIMAL | EMBEDDED |

All solver decisions ended by completion; no cutoff, cut count or hard deadline bound a unit.
Positive-control and sampled-cell solver allocations were both 15 seconds. There were no
solver UNKNOWNs or parent timeouts. Per-cell wall duration and budget fraction can be recovered
from recorded wall_seconds / subprocess_budget_seconds; solver duration / its input cutoff
is the separate solver fraction. The global stopping condition was first exact R3 recovery.
No long run is inferred affordable from these eight-plane times.

Pilot manifest: 18.156652583 wall seconds, 0.005043514606 core-hours, one worker. Canonical export/recheck:
0.689066542 wall seconds, 0.000191407894 core-hours (timing excludes final metadata hashing). The two recorded
manifests sum to 0.005234922500 core-hours. Development, independent review/checking and regression runs
are outside these measured run totals; no resources are estimated for them. No sleep gap or
unattended night is claimed. The 2400-second hard computation ceiling was not approached.

## Exact auxiliary object and identity

The seed-4 candidate has integer planes, V,E,F,chi=(24,36,8,-4), genus 3, 28 adjacent pairs,
20 single and 8 doubled adjacencies; all faces are simple 9-gons. verify_candidate --all-pairs
passes; --target S5 fails as expected, since F_max(3)=9. Its cell union is invariant under the
two generating D2 half-turn permutations; this is checked on the actual selected solid, not
inferred from symmetry of the plane arrangement.

A cyclic-link isomorphism to the known Roest-Vigh map is
{0:0,1:3,2:1,3:2,4:7,5:4,6:6,7:5}. This certificate is checked per face with parallel-edge
pairings retained. This is a new coordinate recovery of that known combinatorial type,
not a novelty claim or a new public/gallery witness. The engine calibration is the result.

The standalone checker in verify_independent.py imports only the standard library, not
ladder_exact or other project geometry helpers. It uses Fraction arithmetic, an independent
winding-number line-section construction, face simplicity, edge incidence, vertex links,
orientability, and interval-union equality for every pair. It accepts this one candidate.
All 56 normal triples and 70 four-plane determinants are nonzero; min absolute determinants
are 12 and 56, respectively. Min nonincident plane value is 1/6; minimum squared edge length
and vertex separation are both 2695/110976. All 56 arrangement triple points are distinct.
These exact positive quantities are for the stored integer representatives, not invariant
normalized margins. Rounding at 1e-9 or 1e-12 changes none of these integer input planes.
The independent check and an intentionally invalid-map rejection are in verify_all.
REVIEW.md is an AI-session filter, not independent human review.

## Encoding and claim boundary

**EXACT:** the retained integer-coordinate auxiliary object and both known-object recoveries;
the quick suite reconstructs the rational chamber data, regenerates the deterministic D2 draws,
rebuilds and compares every saved CP model byte-for-byte, re-solves every saved integer CP model,
rechecks the saved geometry and cell-to-link extraction, and runs the independent checker.
The impossible tetrahedron edge-count control is INFEASIBLE. Failed/stopped or unrun cells
are never called excluded geometric families.

**PROVED-1:** the hard disk formulation and its interpretation. Rooted integral flow forces all
selected boundary facets in a plane into one component. The no-diagonal constraints exclude
point pinches; a connected bounded planar manifold region with chi=1 has exactly one boundary
component, hence is a disk. Selected solid octants and no-diagonal 1-cells supply the local
boundary conditions. At most three disjoint shared segments are needed at eight/nine uniform
planes because 2r distinct endpoint partners require 2r <= F-2. The model therefore does not
cut the stated target by its run cap. Exact signs and line orders are computed before table
construction; float signs actually consumed by Tables are checked against exact values.

The INFEASIBLE results concern only their saved CP models at those rational planes, E=36 and
max_runs=3. They are re-solved integer computations, not independently checked DRAT certificates.
Their geometric interpretation still depends on the single-author encoding argument. No
CERTIFIED theorem, D2-family exclusion or S5 non-existence claim follows. No nine-plane target,
S4/C4 sampler, full catalogue or numerical optimization was run.

## Corrections retained with provenance

The first verify_candidate invocation on the raw worker result selected its legacy `solid`
parser because that key was present, then failed with `AssertionError: not orientable` while
attempting triangle-set reconstruction. That path loses parallel-edge pairing. The failure is
retained in results/recheck/legacy-parser-failure.log. Canonical exports contain only the
original planes and paired links; all three exports pass --all-pairs and correctly fail S5.
No candidate numbers were retyped and no target computation was rerun for this correction.

Read-only review identified two failure-path gaps in the original runner: unexpected CP status
or failed exact geometry could have continued as a failed recovery; float/exact disagreement
could have been caught as a degenerate random draw. Post-run hardening introduces strict result
validation and a separate ArithmeticError category, with regressions. Every recorded result
passes the stricter validation; deterministic input regeneration reproduces all accepted inputs
and rejection counts. The old successful run retains its original source commit, without a
claim that the later guards were active then. New tests exercise wrong status, geometry and
topology, the cancellation boundary, and the canonical export API. Follow-up review found no
remaining significant issue. Neither AI review is an external mathematical referee.

## Verdict and next step

**BENCHMARK-PASS / PROMISING at the measured budget:** R2 and R3 are achieved, so the registered
explore prerequisite of E-261103-03 is concluded. Its separately costed coverage proposal may
now be activated under a committed PLAN and the remaining execution gates; no tranche is run
as part of this pilot. For this constructive engine, next is a separately registered small
nine-plane pilot, not an automatic night. Eight-plane recovery times do not predict nine-plane
coverage or geometric realizability.

H-261103-02 and H-261101-07 remain open: a nonmaximal eight-face calibration moves neither the
free-C3 (9,3) existence claim nor maximal genus-3 existence. No scenario credences are changed.
The current chamber builder requires uniform arrangements. At nine faces, exact fixed-face C2
or D3 plane families can force zero determinants and are outside this implementation; rejecting
them is not a geometric exclusion. A later pilot needs a justified nonuniform extension or must
explicitly use uniform arrangements/perturbations. Symmetric planes alone do not impose symmetry
of the selected solid; any future geometric symmetry claim needs its own action check.

The experiment is marked done for its registered bounded R2/R3 pilot; its original conditional
nine-plane/night proposal was not activated. No push, PR, release or external communication.

## Final local verification

verify_all.py --quick: ALL PASS (19 checks; full archive skipped). The added solid-first check
runs all nine local tests, including deterministic catalogue regeneration, byte-identical model
reconstruction, fresh CP-SAT replay, primary exact geometry, and the standalone Fraction checker
with a rejection control. The original S5/OM-SAT saved evidence still passes. Research graph has
no errors; source/document diff checks and experiment text English checks pass. Raw failure logs
are retained. No full archive, GitHub CI or independent human review was run.
