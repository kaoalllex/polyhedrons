# Specification: target, relaxations, counters, evidence levels

Frozen 2026-11-01. Change only by an explicit, dated entry at the end of this file. Every claim, script
and table in this project uses the definitions below; if a document disagrees, this file wins.

## 1. The strict target (S0)

A **solution** is a closed orientable polyhedral surface embedded in R^3 with

1. exactly 12 faces, each a planar **simple** polygon;
2. every two faces share **exactly one complete edge**, and every edge belongs to exactly two faces;
3. exactly three faces at every vertex;
4. no other intersections: two faces meet exactly in their shared edge (and its end points), a face does
   not meet itself except along its boundary cycle.

Consequences: F = 12, E = 66, V = 44, every face is an 11-gon, chi = -10, genus 6. The dual is an
orientable triangulation of the genus-6 surface with 12 vertices and 1-skeleton K12: one of exactly
**59 combinatorial types** (`data/k12_triangulations.json`, ids 0-58). Condition 3 is stated explicitly; it does
not follow from 2 alone.

Representation: a candidate is 12 planes `h_X = (a, b, c, d)` (`a x + b y + c z + d = 0`) plus a map (dual
triangles or cyclic neighbour lists `links`). Vertices are triple points of planes; planarity is automatic.
The realization space of a type is open in R^36, so general position is WLOG and a solution, if any, has a
rational (hence integer) certificate.

**Only `verification/verify_candidate.py FILE --target S0` returning PASS counts as a solution**: exact
`EMBEDDED: True` (`ladder_exact.verify`), 12 faces, every two faces adjacent, every adjacency single,
(V, E, F, chi) = (44, 66, 12, -10). `--all-pairs` alone is S1 (it accepts doubled adjacencies; `verify_all`
checks that S0 rejects the Roest-Vigh object). Nothing else - no energy, no counter, no picture - is
evidence of a solution.

## 2. Auxiliary targets (never solutions; label every result with its target)

| Id | Target | Status in this project |
|---|---|---|
| S1 | **Doubled adjacencies**: every pair of faces adjacent, some pairs share two collinear edges; d doubled pairs raise the genus | the 2026 eight-face objects (Mizhaev, Roest-Vigh) are of this kind; 12-face version untried |
| S2 | **Polyhedral immersion**: conditions 1-3 plus *local* embeddedness (simple faces, at most one reflex corner per vertex, orientation consistency); global intersections allowed | symmetric case excluded (CERTIFIED); asymmetric open |
| S3 | **Partial polyhedron**: 12 planar simple faces, embedded, genus g < 6, 30 + 6g adjacent pairs, every adjacency single | genus 3 reached (types 0, 15, 39, 53) |
| S5 | **Maximal face-neighbourly polyhedron (F, g)**: embedded, cubic, every two of the F faces adjacent (multiple adjacencies allowed: a pair may share two or more collinear edge segments; the multiplicity is reported), and F = F_max(g), the most faces possible at genus g (F (F - 1) / 2 <= E = 3 (F + 2g - 2)): (7, 1) Szilassi, (8, 2), (9, 3), (10, 4), (11, 5); (12, 6) is S0. Success check: `verify_candidate.py FILE --target S5` PASS | (7, 1) known; the 2026 eight-face objects are (8, 3), not maximal; (8, 2) to (11, 5) unknown to us (literature check open); symmetric realizations allowed (FD5 is about S0 only) |
| S4 | **Smaller analogues**: n mutually adjacent faces, n = 7 (Szilassi, genus 1), n = 8 (genus 2 needs doubled adjacencies or 4-valent vertices) | n = 7 solved by every engine; n = 8 strict rungs open |

"Extendable" (for S3) means only: the abstract map can be completed to a genus-6 target map by handle
attachments (`code/handle_add.reach` = 66; certificate for type 0 in `verification/certificates/`). It
says nothing about geometric continuation.

## 3. Degeneracies

Not allowed in any claim: four planes through one point, a vertex at infinity, zero-length edges,
collinear consecutive edges merged into one, two vertices coinciding, a shared edge passing through a
fourth face. The exact verifier rounds planes at 1e-9 (Gauss tools: normals at 1e-6); a certificate is
exact **for the rationalized configuration the code checks**, and must be reported as such. Near-misses
that vanish only in a degenerate limit (`ladder.degeneracy`) are not progress.

## 4. Counters (name the counter in every table)

| Counter | Meaning | Exact? | Allowed in claims |
|---|---|---|---|
| `EMBEDDED` | `ladder_exact.verify` / `verify_solid` verdict | exact | yes - the only success criterion |
| `nonsimple_faces`, `bad_pairs` | exact defects: faces that are not simple; pairs of faces whose intersection is not exactly their shared edges | exact | yes, reported as a pair, never summed silently |
| `adjacent_pairs` | pairs of faces sharing an edge in the realized map (30 + 6g for S3) | exact | yes |
| `events` / `pair_energy` (`ladder.pair_energy`) | optimizer objective of the ladder engines | float | no - search diagnostics only |
| `fastviol` | violated forbidden triples (`code/fastviol.py`), the counter of 2026-10-29 near-miss tables | float | no |
| `local_viol` | immersion defects (`code/local_viol.py`) | float | no |
| `class_energy` | Gauss-class energy of the normal-space annealers | float | no |
| `own_degree`, `target_degree` | Gauss-map degree of the realized normals in their gauge; target 1 - g | exact (signs of 3x3 determinants) | yes |
| `k_tau` | degree change of the next handle at fixed normals (D_{M+tau} = D_M + k_tau) | exact | yes |
| `saddles` | saddle vertices (need >= 2g + 1) | exact | yes |
| `covering` | positive covering of the sphere | **sampled** (64-2256 directions) | only as "sampled covering"; not exact until `ROADMAP.md` E-261101-13 lands |
| `hemisphere_margin` | how far the handle normals are from a closed hemisphere | float | diagnostics |

Solver outcomes: **SAT** (a model; re-check exactly before use), **UNSAT** (scoped to exactly that formula:
those normals, gauge, bounds and margins; never generalise beyond it), **UNKNOWN / timeout** (no information,
never a negative result), **UNSAT-SOLVER** (the solver's UNSAT without a checked proof: may skip or rank a
map in a search, never a negative result until a replay gives UNSAT-VERIFIED), **ERROR** (the run failed; no information), **NO_ADMISSIBLE_NORMALS** (the annealer
found no normals in the class within its budget - a search failure, not a proof). A SAT model or a search output
is a **CANDIDATE** until `verify_candidate.py` passes; none of these outcomes is an evidence label (§5).

**Scope of a negative result** - every UNSAT / "not found" statement names one of:
1. *instance*: this formula only (these normals, this gauge, these bounds);
2. *family*: every instance of a stated family (e.g. "all 25 symmetry classes", "all normal sets passing gate
   T1 for type 0"), with the argument that the instances cover the family;
3. *theorem*: a mathematical statement, with its evidence label (§5).

Going from 1 to 2 needs a coverage argument; from 2 to 3 needs a soundness argument for the encoding.

**Certificate chain** (say which link a claim reaches): the solver answered -> it produced a certificate (DRAT /
LRAT / exact witness) -> an independent checker accepted it -> a written argument turns it into a theorem.
Only the last link is CERTIFIED (§5).

## 5. Evidence levels (use these labels in `STATUS.md`, `CONCLUSION.md` files and agent output)

| Label | Meaning |
|---|---|
| **CERTIFIED** | computer proof with a checked certificate (DRAT/LRAT checked by drat-trim / cake_lpr) **plus** a written soundness argument for the encoding; certificate hashes recorded |
| **PROVED** | written proof reviewed by at least one reviewer independent of the author |
| **PROVED-1** | written proof, single author (an AI session counts as one author), unreviewed |
| **EXACT** | exact-arithmetic witness or computation, reproduced by `verification/verify_all.py` |
| **NUMERICAL** | floating-point observation; guides the search, proves nothing |
| **CLAIMED** | third-party statement not reproduced here |

AI agents working on the same code and premises are **not** independent reviewers. Theorem-level public
claims need a human mathematical review outside this chain of agents.

## Change log

* 2026-11-08 (correction, strategy review M1): the 2026-11-03 evening entry's count is wrong; the exact census has
  18 admissible (9, 3) maps with a tripled pair, not 10. Definitions unchanged.
* 2026-11-03 (evening, strategy review applied): §2 S5 says explicitly that adjacencies of multiplicity two or more
  are allowed (one of the two (8, 2) candidate maps and 10 admissible (9, 3) maps have a tripled pair; `--target S5`
  already accepted them). No target weakened.
* 2026-11-03: §2 adds S5 (maximal face-neighbourly polyhedra) and its check `--target S5`; the owner made S5 at
  (9, 3) the focus target (`STRATEGY.md`); S0 stays the defining problem of the project, parked, not weakened.

* 2026-11-08: §4 adds UNSAT-SOLVER (owner: search runs may skip DRAT; negative claims still need a checked proof).
* 2026-11-01: §4 adds ERROR / CANDIDATE, the scope of a negative result and the certificate chain.
* 2026-11-01: §1 success check is `verify_candidate.py --target S0` (the earlier `--all-pairs` wording
  accepted doubled adjacencies; found by the fresh-eyes process audit of 2026-11-01, finding F01).
  §5: `results.md` is frozen history and keeps its old labels.
* 2026-11-01: created from `theory/mathematical-model.md` and the process audits of 2026-10-31.
