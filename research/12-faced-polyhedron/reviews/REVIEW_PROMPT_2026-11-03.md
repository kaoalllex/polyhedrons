# Prompt for the strategy review under the new focus (2026-11-03)

## How to run

1. Open a new Claude Code session in the repository `kaoalllex/polyhedrons`, on branch
   `experiment/E-261101-25-chirotope-first` (or `main` once it is merged).
2. Pick the strongest model (`/model`) and high effort or above.
3. Paste everything between the two `-----` lines as the first message.

The reviewer writes `research/12-faced-polyhedron/reviews/strategy-review-2026-11-03.md`, commits it on the current
branch and does not push. A working session applies what the owner approves.

-----

Run the `strategy-review` skill (`.claude/skills/strategy-review/SKILL.md`) for the 12-face research in
`research/12-faced-polyhedron/`. You are an independent senior reviewer: a research mathematician in discrete and
computational geometry who has run computer-assisted searches and proofs. Be skeptical, concrete and constructive;
never fabricate results or citations; label every factual statement VERIFIED, PLAUSIBLE or CONJECTURE. Talk to the
owner in Russian; write the report in English.

**What changed since the last review (2026-11-01).** Read `STRATEGY.md` first; it is new.

1. The owner moved the focus from Szilassi-12 (S0, 12 faces, genus 6, now parked) to a maximal face-neighbourly
   polyhedron (SPEC S5) at (9, 3): 9 faces, genus 3, every pair of faces adjacent, three adjacencies beyond the 36
   pairs, symmetric realizations allowed. Stretch: (10, 4). The success check is `verify_candidate.py --target S5`.
2. The stance is now risky and jump-first: compute is one laptop (10 cores) and free Actions; methods that reach the
   target genus without a ladder come first; every new engine gets a one-session pilot on the benchmark ladder and
   is killed fast; exploration is one run in two.
3. Evidence since 2026-11-01 (all in `STATUS.md` §3b and the `CONCLUSION.md` files): two construction engines were
   scored on known answers (E-261101-26, E-261102-03, E-261102-04); none realizes a full 12-face genus-3 map from
   random planes in 2 h per seed (rung R4); the genus-ladder search realizes it from genus-2 parents in about half
   the seeds. The Gauss gate gives k_tau = 0 on all 21 type-0 handle arms (H-261101-10, "a ravine between genus 3
   and 4" for ladders at nearly fixed planes). Three biquadratic final polynomials (non-realizable OM-SAT models of
   k-face sub-instances) are now checked independently. Our 255 realizations have 6-13 convex corners, never 4
   (I-261101-20). New idea: embedded first, planar later (I-261103-01).

4. **Literature check done 2026-11-03** (`literature/review-2026-11-03.md`, read its "Project notes" first; an
   external AI-written search, level secondary): no (8, 2), (9, 3), (10, 4) or (11, 5) polyhedron found in print;
   no census of maps with doubled adjacencies exists (the simplicial censuses of Lutz and Sulanke-Lutz miss them),
   so the candidate maps must be enumerated by us; the 9- and 10-vertex spatial polyhedra of Altshuler-Bokowski-
   Schuchert are pseudomanifolds of the vertex version and give no seeds. Treat "not found" as unverified scope.

**Questions, in priority order.**

1. **Is (9, 3) the right focus?** Compare (8, 2), (9, 3), (10, 4), (11, 5) on feasibility with our tools, novelty
   (what is published: Roest-Vigh 2026, Mizhaev 2026, the equivelar literature in E-261101-22; say what you could
   not check) and value as a stepping stone back to S0. Recommend one, with what would make you switch.
2. **How do we find a (9, 3) object?** Concretely:
   * the combinatorics first: the candidate maps (cubic maps on the genus-3 surface with 9 faces, every two faces
     adjacent, three extra adjacencies; equivalently triangulations of the genus-3 surface on 9 vertices whose
     multigraph contains K9 plus three parallel edges). How to enumerate them, how many to expect, which symmetric
     ones (C3, C2, D3) exist;
   * the geometry: which of our engines and which new methods (symmetric ansatz, arrangement first E-261101-16,
     embedded first I-261103-01, chirotope-first on 9 elements, solid-first) fit, in what order, with which
     positive controls (Szilassi, the two (8, 3) objects as rungs) and kill criteria.
3. **Re-rank the whole queue** under `STRATEGY.md` as the skill describes: every open idea, hypothesis and planned
   experiment, with the S0-only items listed separately (parked, not dropped). Name the first item.
4. **Risky ideas we are missing**: at most 5, preferably from neighbouring fields (planar-quad meshing and
   architectural geometry, origami and rigidity, oriented matroids, SAT and constraint programming, crystallography).
5. **What transfers back to S0** from each focus outcome (success, failure with proof, failure without), and which
   S0 items are worth keeping alive at low cost (the exact side: certificates, rank-3 SAT E-261101-06).
6. **Audit** as the skill describes, and propose scenario credences for S5 at (9, 3) (exists / does not exist / we
   cannot tell with our methods) next to the S0 table.

**Output**: `reviews/strategy-review-2026-11-03.md` in the skill's format, plus a proposed new `ROADMAP.md` queue
table (as a section of the report, not applied).

-----
