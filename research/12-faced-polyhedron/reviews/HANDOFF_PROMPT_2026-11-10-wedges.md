# Prompt: apply the 2026-11-10 session (face-minimal ladder, relaxed Szilassi-12, wedge ansatz, harness changes)

## How to run

1. Open a new Claude Code session in the repository, on branch `lab/2026-11-09` (or the week branch the owner names).
2. Pick the strongest model (`/model`) and high effort or above.
3. Paste everything between the two `-----` lines as the first message.

The session formalises the material below into the project's documents (`STRATEGY.md` log entry, idea and hypothesis
files, planned experiment folders, a new week plan in `ROADMAP.md`, `TODO.md`) in the protocol's formats, commits on
the current branch and does not push. It runs no solver and no night. Everything here is a proposal of one AI session
(2026-11-10) and, where it says NUMERICAL, a read-only float computation on published coordinates; nothing here is
evidence under `SPEC.md` §5 until re-checked.

-----

You are a lead session of the 12-face research in `research/12-faced-polyhedron/`. The owner has decided
(2026-11-10): **compute is the owner's laptop only** (at most 10 cores, 8-10 shards per splittable run, nights under
`caffeinate`), no rented compute, no GitHub Actions. A previous session did a strategy investigation and left its
findings, ideas and a proposed week plan in this prompt. Your job is to **formalise them in the project's format**,
not to redo the investigation and not to run anything beyond ~10-minute checks.

**Owner's decisions of 2026-11-10 (record them as decided, do not ask again):** (a) laptop-only compute, no rented
compute, no Actions; (b) the harness changes of §11 are **approved** (items 1-7; item 8 only after two manual mornings
went well). **Still to be approved by the owner, ask in your final message:** the `STRATEGY.md` text of §8, the
`SPEC.md` S6 entry, the week plan of §7 and the E-B night.

**Rules.** Root `CLAUDE.md` and `PROTOCOL.md` apply in full: `SPEC.md` §5 labels on every claim, no fabricated results,
scoped negatives, IDs `<K>-YYMMDD-NN` with today's date, one file per idea/hypothesis/experiment with the header of
`PROTOCOL.md` §4, PLAN before compute, T + D >= 3 to enter the queue, text budgets of §8b. `STRATEGY.md` is changed only
by the owner: write the proposed §1/§2 text and a dated log entry, and ask the owner to approve it in your final
message (Russian). Files, code and commits in English. Check `map/graph.json` titles before creating an idea file;
where an existing idea covers part of a proposal, extend that file (a dated section) instead of duplicating it, and
make the new file's `origin` point to it. Run `python3 verification/trace.py` (or `verify_all.py --quick` if it is the
only way) after the graph edits.

**Read first:** `STRATEGY.md`; `STATUS.md` §0, §2, 3c, 3d, 3ad, §4; the week plan and the "Decision point" of
`ROADMAP.md`; `SPEC.md` §2; `PROTOCOL.md` §4, §8a, §8b; `reviews/strategy-review-2026-11-09.md` §1-§2;
`reviews/strategy-review-2026-11-08e.md` (the alternatives table); `ideas/I-261101-20`, `I-261030-06`,
`I-261101-08`, `I-261030-01`, `I-261103-02`; `experiments/E-261103-05-s5-symmetric-solid-first/CONCLUSION.md` and
`E-261107-01`, `E-261108-01` (the solid-first engine and its two (9, 3) sweeps); `experiments/E-261109-06` CONCLUSION.

## 1. Where the previous session thinks the strategy is wrong (judgment, not evidence)

1. **(10, 4) is a poor proxy for S0.** S5 at (8, 2), (9, 3), (10, 4) *requires* multiple adjacencies (slack s = 2, 3, 3
   excess edges), S0 has none (s = 0). The (9, 3) solve times split by multiplicity pattern (STATUS 3d, NUMERICAL:
   concentrated patterns `(1,2,3)`, `(2,2,2)` in 22-76 s; spread-out `1^6` in 523-914 s), which suggests the
   multiple-adjacency constraints (`SEGMENT_DISJOINT` plus the collinear-segment geometry) are what the solver refutes.
   If so, the negative ladder says little about S0, and the remaining A + B sweep (about 485 core-h = 6 laptop nights,
   STATUS 3ad) buys mostly more of the same. **Recommendation:** finish (10, 4) only if cube-and-conquer (week item 3)
   makes A + B <= 3 nights; otherwise demote it to an explore slot and move the nights to items 2-3 below.
2. **OM-SAT is an exclusion tool, not a construction tool** for this project: 0 of 42 SAT models were ever realized
   (DR8). A positive result is more likely from a geometric ansatz with few parameters, decided exactly (solid-first +
   CP-SAT, chamber-SAT), than from a SAT model plus a realizer.
3. **S0 itself** at ~19,000 core-h (Pirozhkov's estimate, CLAIMED) is out of reach on one laptop; the previous session's
   subjective credence that S0 exists is about 0.05. The S0 queue stays parked. What is in reach on a laptop and new
   to the literature (CLAIMED, web search 2026-11-10: nothing found in print) are the three targets below.

## 2. Observation: sharp wedge pairs in the three known face-neighbourly polyhedra (NUMERICAL, weak evidence)

Read-only float computation on the published coordinates (Szilassi from `index.html`; Roest-Vigh from
`code/control_rost_vigh.py` planes + cycles; Mizhaev from `literature/mizhaev2026-planes.json`), after orienting the
face walks coherently (the Mizhaev walks needed four flips, the Szilassi walks two); the script is not in the
repository (about 80 lines: Newell normals, outward orientation by signed volume, edge convexity from
`(n_f x n_g) . t`, interior dihedral angle). Controls that passed: convex/saddle vertex counts reproduce I-261101-20
(Szilassi 6 convex of 14; both 8-face objects 4 convex of 24); Szilassi has 16 convex and 5 reflex edges, Roest-Vigh
20/16, Mizhaev 22/14; every saddle vertex has edge signs CCR or CRR, no vertex is RRR.

| Object | disjoint face pairs with the sharpest convex edges | interior dihedral angle | unpaired |
|---|---|---|---|
| Szilassi (7, 1) | {1,2}, {3,5}, {4,7} | 28.1, 40.2, 40.2 degrees, single adjacencies | face 6 |
| Roest-Vigh (8, 3) | {A1,B2}, {A2,B1}, {A3,B4}, {A4,B3} | 24.5 degrees, each a doubled adjacency | none |
| Mizhaev (8, 3) | {1,4}, {2,3}, {5,7}, {6,8} | 10.2 degrees, each a doubled adjacency | none |

In both 8-face objects four of the eight doubled pairs are these wedge rims; the other four are reflex (Roest-Vigh
{A1,B4}, {A2,B3}, {A3,B2}, {A4,B1} at 232.7 degrees; Mizhaev {1,5}, {2,6}, {3,7}, {4,8} at 255.2 degrees).

**Null model (session Monte Carlo, 20,000 samples per row, not in the repository).** Event: F planes contain k
disjoint pairs whose acute plane angle is at most theta. A small plane angle is necessary, not sufficient, for a sharp
convex wedge, so these frequencies are upper bounds for chance. Per pair, P(angle <= t) = 1 - cos t: 1.6 % at 10.2,
9.0 % at 24.5, 23.6 % at 40.2 degrees.

| Family | event | frequency |
|---|---|---:|
| isotropic, 7 planes | 3 disjoint pairs <= 40.2 (Szilassi) | 0.50 |
| C2 family (3 pairs + 1 plane), 7 planes | same | 0.53 |
| isotropic, 8 planes | 4 disjoint pairs <= 24.5 (Roest-Vigh) | 0.005 |
| D2, two 4-orbits (the Roest-Vigh ansatz) | same | 0.50 |
| isotropic, 8 planes | 4 disjoint pairs <= 10.2 (Mizhaev) | 0 of 20,000 |
| D2, two 4-orbits (stand-in for Mizhaev's S4 family, not simulated) | same | 0.12 |
| isotropic, 9 planes | 4 disjoint pairs <= 24.5 | 0.038 |
| isotropic, 12 planes | 6 disjoint pairs <= 24.5 | 0.004 |
| isotropic, 12 planes | 6 disjoint pairs <= 40 | 0.33 |

**What this does and does not support.** The matching itself is close to a coin flip: any 7 planes have Szilassi's
three pairs half the time, and in a two-orbit symmetric family a cross-orbit pair orbit is automatically a perfect
matching, so Roest-Vigh's four wedges are a coin flip inside its own ansatz family and Mizhaev's about one in eight.
**Do not file "wedge structure is generic" as a supported regularity** (CLAUDE.md: a diagnostic is checked on controls
before a phenomenon is named). **Do not claim that the (9, 3) solid-first sweeps lacked wedges:** 200 of the 300
arrangements of E-261108-01 were built on the Roest-Vigh and Mizhaev planes, which contain these wedges, and those
sweeps are explained by the (9, 3) exclusion anyway. What remains is (i) a mechanism (derivation sketch of the
session, to be checked before use): two thin wedge-shaped plates that pierce each other realize all four adjacencies
between their faces along one bundle of lines, the rim realizes the fifth, and a rim pierced by another plate is a
doubled adjacency, which is what both 8-face objects show at their sharpest wedges; (ii) a sampling fact: isotropic
samplers give F/2 disjoint sharp pairs in about 0.5 % of 8-plane and 0.4 % of 12-plane arrangements, two-orbit
symmetric families in about half. If wedges matter, isotropic sampling at 12 planes wastes two orders of magnitude;
whether they matter is an open question that E-C measures on a rung with known answers.

## 3. Targets, in the order the previous session proposes

### T1. Relaxed Szilassi-12 (S1 at 12 faces, genus free), the main constructive goal
12 planar simple faces, embedded, cubic, every two faces adjacent, **multiple adjacencies allowed**, genus free.
Counting (cubic: V = 2E/3, g = 1 + (E - 3F)/6, so E = 3F mod 6): at F = 12 the admissible edge counts are E = 66 (S0,
g = 6), 72 (g = 7, **six** extra segments), 78 (g = 8). Note that `E-261101-08` speaks of "three doubled pairs, genus
7": three extra segments give E = 69 and a non-integer genus, so that row is miscounted; the session corrects it. The
smallest relaxed case is therefore six extra segments (e.g. six doubled pairs, or two tripled and two doubled...), which
makes a C3 or D3 orbit of doubled pairs natural. This is exactly what Mizhaev and Roest-Vigh did at 8 faces; nothing is in print at
12 (CLAIMED). It is not S0 (never report it as S0) but it is the nearest *existence* result to S0 the laptop can reach,
and FD5 does not forbid symmetric realizations here (FD5 is about single adjacencies; check and state this scope).
Existing rows to merge: `I-261030-06` (relaxed 12 faces with doubled pairs), `E-261101-08` (S1 with three doubled pairs
as a C3 orbit, genus 7, "after Roest-Vigh calibration"), `DR12`. The new content is the ansatz family of §4 and the
wedge mechanism.

### T2. Face-minimal polyhedra without multiple adjacencies (the S0 ladder that has no slack)
Duals of the **vertex-minimal triangulations** of the orientable surfaces: all faces simple polygons, cubic, *single*
adjacencies, **not** all pairs adjacent (so `Triangulation(..., submap=True)` and `verify_candidate.py` with the plain
EMBEDDED check plus a stated pair count; propose a new target id S6 in `SPEC.md`, owner's approval needed, no weakening
of S0). Counts (CLAIMED, from the literature and memory; the session must verify the numbers before writing them into
`STATUS.md`): (10, 2): 865 maps, 36 of 45 pairs; (10, 3): 20 maps, 42 of 45; (11, 4): 821 maps, 51 of 55;
(12, 5): 751,593 maps, 60 of 66; (12, 6): 59 maps = S0. Sources: Hougardy-Lutz-Zelke (arXiv math/0507592,
math/0604017, math/0608538), Lutz's lists; Schewe (arXiv 0801.2582) for non-realizable genus-5 and genus-6 vertex
triangulations. The vertex version is realizable through genus 4 and fails at 5-6; the face version appears to be
untouched in print (CLAIMED, one web search). Value: an (10, 3) SAT model that realizes is a new polyhedron (fewest
faces for genus 3, no multiple edges); 20 UNSAT-VERIFIED formulas at (10, 3) are a face-minimality theorem for genus 3
(conditional, PROVED-1) and the first S0-relevant negative, because this ladder has S0's zero slack at every rung.
Compute: the (10, 3) formulas have 11 elements like (10, 4) but fewer constraints; expect minutes to an hour per map
(untested); 20 maps fit one night with DRAT. Where the maps come from: Lutz's `MANIFOLD_PAGE` lists or
`passagemath-simpcomp-data` (the repo already holds `SurfOG06.scb`); the session checks what is on disk and writes a
converter as part of E-B's prep, with a (7, 1) control (the Csaszar/Szilassi dual) and the 59-type control at (12, 6).

### T3. (9, g) and (10, g) with multiple adjacencies, genus free
Nine mutually adjacent faces with any genus (cubic, E = 3 mod 6: E = 39 is genus 3, E = 45 genus 4, E = 51 genus 5;
at ten faces E = 0 mod 6: 48 is genus 4, 54 genus 5): the smallest case with nothing in print (CLAIMED). The project's
two (9, 3) sweeps fixed E = 39, now excluded at formula scope; the new run frees the genus (E in {45, 51} for nine
faces, {54} for ten) and uses the arrangement families that E-C scores best.

## 4. Ideas to file (each: statement, why, cheapest test; status open; origin as given)

* **I-A. Wedge-plate ansatz** (origin: owner, L:roestvigh2026, L:mizhaev2026, I-261101-20, I-261030-01). 2m faces as m
  wedges: plane pairs (n_i, d_i), (n_i', d_i') with a small angle, rim lines L_i. Mechanism: mutual piercing of two
  wedges gives 4 adjacencies; a pierced rim gives a doubled pair (T1, T3); an unpierced rim gives a single pair (T2,
  S0). No parameter is saved (two planes = a mid-plane, a rim line in it and an angle, 6 numbers either way); the
  gain is combinatorial: in the thin limit the chirotope is fixed by the arrangement of the m mid-planes (6 planes
  have a few dozen affine types) and by the position of each rim line among the m - 1 trace lines of its plane, so
  the search splits into a small arrangement and m line placements, and a 12-plane sampler can be biased towards the
  0.4 % of arrangements that have six disjoint sharp pairs (§2). Evidence: the mechanism and the weak observation of
  §2 only. Cheapest test: E-C. Kill: within one symmetry family, arrangements with F/2 disjoint sharp pairs contain an
  all-pairs solid no more often than the others.
* **I-B. Multiplicity-free face-minimal ladder** (T2; origin: L:schewe2010, I-261101-07, owner). Statement and
  sources above. Cheapest test: build the (10, 3) formulas with `submap=True`, run two of them for 20 minutes.
* **I-C. Genus-free relaxed targets** (T1, T3; origin: I-261030-06, E-261101-08, E-261107-01). The solid-first inner
  model with `target_adj` = all pairs and E free (minimize nothing, or minimize E); on wedged arrangements of 9, 10, 12
  planes; symmetric families D2 x 3 orbits (12 faces, 8 parameters), T-orbit of one plane (12 congruent faces, 2
  parameters: exhaustive by exact chamber enumeration), C3/D3 at 9 planes.
* **I-D. Multiplicity is the obstruction** (hypothesis H-A below), tested by the immersion-only (S2) formulas.
* **I-E. XOR-aware solving.** The encoder's `IN` predicates are crossing parities (long XOR chains, `code/omsat.py`
  `Predicates.IN`). Cheapest test: CryptoMiniSat with Gauss-Jordan on three known (9, 3) maps against kissat; and an
  order-encoding of the triple points along each line L_XY (the "ordered beads" of brainstorm item 19) as an
  alternative to parity. Kill: < 1.5x on all three. Low priority; it only matters if a long sweep stays in the plan.
* **I-F. Chart normalisation at a hull vertex.** A projective map that sends a plane just outside a convex-hull vertex
  v = (X, Y, Z) to infinity keeps the polyhedron bounded and its map, so WLOG some vertex v with three convex edges is
  the triple point nearest to infinity on each of the lines L_XY, L_XZ, L_YZ (the `lt` signs of the other F - 3 planes
  against v are fixed on those three lines). Encoding: one selector per candidate vertex, a clause "some selector",
  3 (F - 3) implied order literals each; it removes the freedom in the choice of the plane at infinity (PROVED-1
  sketch, to be written and checked on the pinned controls). Test on three (9, 3) maps; kill as in I-E.
* **I-G. Edge-convexity bits as the cube basis.** A cubic vertex is a saddle iff its three edges do not have the same
  convexity, and the reflex face is the one opposite the odd edge (derivation sketch; the first statement holds on all
  62 vertices of the three objects of §2, the second was not checked on data). So at S0 the 66 edge bits determine all 44 vertex types; they are a smaller and more uniform
  split basis than the 44 vertex-type patterns of E-261101-15. Extend that row instead of a new experiment.

## 5. Hypotheses to file

* **H-A. The multiple-adjacency constraints are what refutes the (8, 2), (9, 3), (10, 4) formulas.** Rival: the
  obstruction is global (genus/covering). Test: (i) solve times by pattern (already NUMERICAL, STATUS 3d); (ii) the
  immersion-only formulas (`triples` off, `reflex`/`poc` on; the S2 encoding of FD6) for the two (8, 2) maps and six
  (9, 3) maps: SAT means the obstruction is global and geometric; UNSAT means it is local and a lemma may be readable
  from the 36-second (8, 2) cores; (iii) the (10, 3) multiplicity-free formulas (T2): SAT models there, and none at
  (10, 4), support H-A.
* **H-B. Wedge seeding raises the hit rate** (operational): within one symmetry family at the 8-plane rung,
  arrangements with four disjoint pairs at an acute plane angle <= 25 degrees contain an all-pairs solid at least
  twice as often as the others. Rival: no dependence once the family is fixed (the §2 null model already explains the
  observed matchings). Evidence so far: none beyond §2. Moves with E-C; every new witness reports its wedge covariate.
* **H-C. Face-minimal polyhedra without multiple adjacencies exist at (10, 3) and (11, 4), and fail at (12, 5) or
  (12, 6)** (the face analogue of the vertex-version picture). Moves with E-B.

## 6. Experiments to register (planned folders; the session writes README + ROADMAP rows, PLAN only for the first)

* **E-A. Edge-type tool and wedge census with its null (exact, no solver; batched with the E-C prep).** `code/edge_types.py`:
  exact edge convexity, vertex types, dihedral angles and the wedge covariate (largest k with k disjoint pairs under a
  threshold) from (planes, links); re-run §2 on Szilassi, Roest-Vigh, Mizhaev, the two witnesses of STATUS §2 and the
  247-realization archive, and the §2 null model from committed code (isotropic, C2, D2, S4 families). Prediction of
  the session: nothing beyond chance for Szilassi and Roest-Vigh, Mizhaev in the upper ~10 % of its family. It is the
  counter calibration of E-C, not a result. Budget: 1 session, < 0.1 core-h. T D F G R = 1 2 2 1 2.
* **E-B. (10, 3) face-minimal decision** (T2, first night). Convert the 20 vertex-minimal genus-3 triangulations to
  `links` (dual), controls (7, 1) and (12, 6), plain formulas with `submap=True`, kissat, DRAT kept (20 maps, so proofs
  are affordable; if a proof exceeds memory, record UNSAT-SOLVER), 10 shards, cap 3600 s per map, any SAT -> the
  saved-OM realization tools of E-261103-04 then `verify_candidate.py` (EMBEDDED, 42 pairs, all single) and
  `candidate-check`. Pre-register: SAT + realized = a new polyhedron; 20 UNSAT-VERIFIED = conditional face-minimality
  theorem for genus 3 (PROVED-1 scope, census CLAIMED from Lutz's list until re-enumerated); timeouts are nothing.
  Budget: 1 prep session + 1 night <= 80 core-h. T D F G R = 2 2 2 2 2, jump 2.
* **E-C. Arrangement-family scoring at the 8-plane rung, with the wedge covariate** (benchmark-ladder rule of
  PROTOCOL §8a for samplers; day run). Families: isotropic `random_planes`; D2 two 4-orbits (the E-261103-05 family,
  1 SOLID in its first 5 seeds, not a rate); wedge-seeded isotropic (four pairs at 10-40 degrees, random mid-planes
  and rims); wedge-seeded D2. 200 arrangements each, the disk-aware inner model of E-261103-05 with all 28 pairs
  adjacent and E free (36 or 42); record per arrangement the wedge covariate and the outcome; exact verification of
  every SOLID. Report the rate per family and, inside each family, the rate with and without four disjoint pairs
  <= 25 degrees. Budget: <= 3 core-h, 8-10 shards. Kill for I-A / H-B: ratio < 2 inside every family with >= 10
  positives in total; fewer than 10 positives -> UNDERPOWERED, record. The best family by positives per core-second
  seeds E-D. T D F G R = 2 2 2 1 2.
* **E-D. (9, g) and (10, g) genus-free sweep** (T3, night, only after E-C names a family with a measured rate). The E-C winner at 9 and 10 planes (C3/D3 three orbits, 4 wedges + 1 plane, 5 wedges as candidates);
  all pairs adjacent, E free in {45, 51} resp. {54} (the parity rule of §3 T1); first-witness stop; exact verification as above. Budget: one
  night. T D F G R = 2 2 2 1 2, jump 2.
* **E-E. Relaxed Szilassi-12 symmetric ansatz** (T1; after E-C or E-D gives a witness). Families: T-orbit of one plane
  (2 parameters: exhaustive exact chamber walk), D2 with three 4-orbits (8 parameters), 6 wedges with C3 or D3
  symmetry. Inner solver as above; genus free (>= 7). Budget: one night per family. T D F G R = 2 2 2 2 2, jump 2.
* **E-F. Immersion-only formulas at (8, 2) and six (9, 3) maps** (H-A test ii). Reuse `omsat_sym`/`build` with the S2
  option set; cap 1800 s; DRAT for (8, 2). Budget: <= 3 core-h day run. T D F G R = 2 2 2 2 2.
* **E-G. (10, 4) remainder.** Keep week item 3 (cube-and-conquer on 96, 85) as is. Rule: strata A + B run as laptop
  nights only if cubes bring them to <= 3 nights; otherwise they become an explore slot (one night, fastest A maps
  first) after E-B and E-D.

## 7. Proposed week plan (<= 5 items, laptop only; the session adapts the format of `ROADMAP.md`)

1. **Idea and hypothesis files (I-A..I-G, H-A..H-C), SPEC S6 proposal, harness items 4a, 4d, 4e, 5 of §11** (this
   session, no compute; lead model, since it writes the hypotheses, a SPEC entry and protocol wording).
2. **E-B prep and night: (10, 3) face-minimal decision** (prep 1 session: converter, controls, smoke test; 1 owner
   night). Follow-up tree: any SAT -> realization stage, `candidate-check`, escalate; 20 UNSAT-VERIFIED -> H-C weakened
   at genus 3, propose (11, 4) only if E-B's median time < 10 min; timeouts > 20 % -> record, escalate.
3. **E-A + E-C: edge-type tool, null model and family scoring at 8 planes** (1 prep session + <= 3 core-h day run).
   Follow-up tree: a family with >= 10 positives -> the E-D night with that family is proposed to the owner; ratio
   < 2 for the wedge covariate -> I-A parked with its rate, E-D uses the best family without wedge seeding; fewer
   than 10 positives in total -> record UNDERPOWERED, escalate.
4. **Week item 3 as planned: cube-and-conquer on 96, 85** (explore, <= 3 core-h). Follow-up tree unchanged; the A/B
   decision rule of E-G.
5. **E-F immersion-only formulas** (explore, <= 3 core-h day run). Follow-up tree: (8, 2) SAT -> H-A supported, write
   one paragraph in `theory/`; UNSAT -> core mining on the (8, 2) formulas (I-261101-02 / E-261101-05 tools) in one
   session.

Not in this week: strata A and B of (10, 4) (E-G rule); the note (deferred by the owner); E-D and E-E (wait for E-C).

## 8. STRATEGY.md changes to propose to the owner (text, not applied)

* §1 Targets: focus = **constructive, laptop-only, three targets in parallel**: T2 (10, 3) decision first (one night,
  decisive either way), T3/T1 by the wedge ansatz (gated by E-C), (10, 4) continues only under the E-G rule. S0 stays
  the defining problem, parked; the new targets are reported as S6 / S1, never as S0 or S5.
* §2 Stance: add "an arrangement family is scored on a rung with known answers (8 planes) before it is used on a
  target, and its report includes the wedge covariate".
* Log: 2026-11-10, owner: no rented compute, no Actions; the (10, 4) route demoted to the E-G rule; the three
  targets adopted for one week of tests; the wedge ansatz is an explore item gated by E-C.

## 9. Credences (subjective planning weights of the previous session, for the Decision point table)

(10, 3) face-minimal exists 0.25 (the vertex version is realizable at genus 3, the face version has no data);
(9, g >= 4) with multiple adjacencies exists 0.55; relaxed Szilassi-12 (T1) exists 0.4; S0 exists 0.05; (10, 4) S5
exists 0.10 (down from 0.15: stratum C 360/360 UNSAT-SOLVER is weak but non-zero evidence against).

## 10. Output of this session

Commits on the current branch: idea/hypothesis files, planned experiment folders (README + scores; PLAN.md for E-A and
E-B only), the week plan block in `ROADMAP.md`, the approved harness items as §11 says, the proposed `STRATEGY.md` text in a review file
`reviews/strategy-review-2026-11-10.md` (10-line verdict, the plan, the credences, what the owner must approve), the
`SPEC.md` S6 proposal in that review (not in SPEC until the owner approves), `CONTINUE_PROMPT.md` handover, the
owner's local `TODO.md` (Russian, untracked). `trace.py` 0 errors. Then tell the owner in Russian: what was filed, the
three approvals you need (STRATEGY text, SPEC S6, the E-B night), and the first lab step.

-----

## 11. Harness changes (**approved by the owner 2026-11-10**: less owner time, same control; infrastructure filter of PROTOCOL §3)

**Who does what.** This session: record the approval (a dated line in `PROTOCOL.md` §8b and `experiment-log.md`), apply
the wording items 4a, 4d, 4e and 5 to `PROTOCOL.md` and the three skills they touch (`experiment-conclude`,
`session-handover`, `strategy-review`), and list items 1, 3, 2 (+ 4b, 4c), 6 in this order under the ROADMAP Phase 0
infrastructure TODO, each as one lab session with its acceptance check (the control-surface test: `start` ->
`status`/`board` -> `stop` -> `start` in a scratch directory; `verify_all.py --quick` green; no change to any recorded
result). Item 7 is part of the E-A/E-B/E-C preps. Item 8 stays conditional. Harness sessions come before or between
week items, never during a night.

Observed cost of the current process (git log 2026-11-03..10, NUMERICAL): 195 commits for about 100 core-h, 10 of
them handover-only (27 mention a handover); 16 review and prompt files, about 378 KB, in ten days; every experiment writes README + PLAN + run.sh +
CONCLUSION + STATUS section + ROADMAP row + log entry + night report + handover + TODO. Owner touchpoints: start every
lab session by hand (prompt, model, effort), `start`/`status`/`stop` of nights, a morning session to conclude, "For the
lead" answers, week-plan approval, PR merge, reading the reviews. The proposals below are ranked by payoff per session;
each names what the owner keeps. File them as infrastructure items (no ROADMAP scores needed; `PROTOCOL.md` §3
filter: each makes a result independently checkable or saves owner/lab time that goes to compute).

1. **Permissions and hooks** (`.claude/settings.json`, project level; half a session). Allowlist the read-only commands
   lab sessions use (git status/log/diff/show, ls, `python3 verification/trace.py --check`, `launch.sh status`, the
   test files of `verify_all`), run the `fewer-permission-prompts` skill once; a `PostToolUse` hook on edits under
   `ideas/`, `hypotheses/`, `experiments/*/README.md`, `ROADMAP.md` runs `trace.py --check`; a `Stop` hook warns when
   the tree is dirty without a handover. Owner keeps: the allowlist is one reviewed commit; no push, no `sudo`, no
   `launch.sh start` in the allowlist.
2. **`launch.sh post` and `board`** (one session; extend `launch.sh`, no new launcher). `post` runs automatically when the
   last shard of a queue ends: the experiment's `summary.py` writes `results/SUMMARY.md` and `verdict.json` (the
   PLAN's registered rules, machine-readable), every CANDIDATE goes through `verify_candidate.py` in the run, results
   are committed on the lab branch, a macOS notification (`osascript`) reports the verdict line. `board` prints one
   screen from `ROADMAP.md`, `STATUS.md`, `CONTINUE_PROMPT.md` and the shard state: branch and dirty flag, running
   shards with progress, last verdict, next week item, open approvals ("For the lead" lines, pending PR), the credence
   table (`verification/board.py`, also `--handover` to generate the mechanical part of the handover block). Optional
   `arm HH:MM` (refuses off AC power, dirty tree or an uncommitted PLAN) and `session N` (opens Claude Code with the
   pinned model and effort and the standard prompt for week item N). Owner keeps: `start`/`arm` is the approval of a
   night; the board is the control surface, read in one minute.
3. **Experiment contract and `lint_docs.py`** (one session; the ROADMAP Phase 0 TODO of 2026-11-01, still unbuilt).
   Every night experiment ships `queue.json` or a unit list, `progress.sh`, `summary.py`/`verdict.json`, and `run.sh`
   verifies candidates in the run. `lint_docs.py` in `verify_all --quick`: PLAN committed before any `results/`,
   T + D >= 3 on every open row, STATUS "As of" equals the latest CONCLUSION date, README `status` equals the ROADMAP
   State, every backticked path exists, text budgets of §8b. This removes the audit items of the lead reviews (A1, A8,
   A9 of 2026-11-09) from the lead's time.
4. **Trim the documentation tax** (PROTOCOL change, owner's decision; one session to generate). (a) Drop the night
   report: its content is the CONCLUSION "Runs" bullet plus `SUMMARY.md`. (b) STATUS §3 experiment sections (3d..3ad)
   become one table generated by `trace.py` from the README headers (`verdict`, `produces`, label, link); hand-written
   STATUS keeps §0-§2 and §4-§7. (c) Handover: `board.py --handover` writes the mechanical lines, the session adds only
   "For the lead". (d) One commit per stage (pre-registration; conclusion), no separate handover commits. (e) Lead
   reviews: at most 150 lines, opening with a 10-line **owner digest** (verdict, approvals needed, first item); the
   owner reads the digest only. Owner keeps: approvals move to the digest; nothing is deleted from history.
5. **Lab sessions chain items** (PROTOCOL §8b wording). A lab session may take consecutive week items in one session
   when none needs a night or an owner approval; "escalate, do not improvise" stays. Cuts the number of sessions the
   owner starts from about three a day to one.
6. **Compute accounting** (15 minutes). `core_hours = wall x WORKERS` overstates (lead review A2); record CPU seconds
   (`resource.getrusage(RUSAGE_CHILDREN)` in `run_overnight.py`, or `/usr/bin/time -l` in `run.sh`). Pricing decisions
   (A/B nights) depend on it.
7. **Tools the new strategy needs** (part of the E-A/E-B/E-C prep, not extra): `code/edge_types.py` (exact edge
   convexity, dihedral angles, wedge matching; also a report field of `verify_candidate.py`, so every future witness is
   characterised automatically); a generic `solid` job in `run_overnight.py` = arrangement generator plugin (random,
   wedges(m, angle range), orbit(G, params)) x `solid_cpsat.best_solid` with E free and all pairs adjacent, SAT -> exact
   verify -> CANDIDATE, built from the E-261107-01 / E-261108-01 workers; `code/lutz_import.py` (vertex-minimal
   triangulation lists -> dual `links`, admissibility, (7, 1) and (12, 6) controls); `verify_candidate.py --target S6`
   after the owner approves the SPEC entry; benchmark-ladder rows for wedge-seeded engines (R1 from 3 wedges + 1 plane,
   R2/R3 from 4 wedges) with file-driven kill rules.
8. **Stage 2, optional, after two manual mornings go well:** `launch.sh morning` runs a headless
   `claude -p` session with the `experiment-conclude` skill and a restricted tool set; it commits the conclusion on the
   lab branch marked `DRAFT` for the owner's review. Never pushes, never merges.

Parked by the owner and left as is: `.github/workflows/experiment.yml` (Actions; mark "parked" in PROTOCOL §6);
`verify.yml` stays. What the owner keeps in every variant: week-plan approval (digest), nights (`start`/`arm`), merges
to `main`, changes to `SPEC.md`/`STRATEGY.md`, and candidate announcements (notification + `candidate-check`).
