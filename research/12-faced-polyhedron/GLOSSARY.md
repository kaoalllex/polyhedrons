# Glossary: the 12-face polyhedron research in plain words

A short guide for readers new to the project (Russian version: `GLOSSARY.ru.md`). For precise definitions see
`SPEC.md`. For the current state see `STATUS.md`.

## The problem

The **Szilassi polyhedron** (1977) has 7 flat faces, and every face touches every other face along an edge. It
has one hole, like a doughnut. The next case of this kind would have **12 faces**, each touching all 11 others
along exactly one edge, with three faces at every vertex. We call it **Szilassi-12**. Nobody has built it, and
nobody has proved it impossible.

- **Genus `g`**: the number of holes. Euler's formula links it to the counts of vertices, edges and faces:
  `V - E + F = 2 - 2g`. Szilassi-12 must have V = 44, E = 66 and F = 12, so g = 6.
- **Map** (combinatorial type): the scheme "which face touches which, and in what order around each face", with
  no coordinates. If Szilassi-12 exists, its map is one of exactly **59** known maps. "Type 0" ... "type 58" are
  our numbers for them.
- **Embedding vs immersion.**
  - An embedding never passes through itself. That is the goal.
  - An immersion is correct locally, but distant parts of the surface may pass through each other. That is a
    weaker requirement.
  - So "no symmetric immersion" is a stronger result than "no symmetric embedding".
- **Face planes.** We describe a candidate by the 12 planes of its faces plus its map. Vertices are the points
  where three planes meet, so every face is flat automatically.

## Our best object, in plain words

`witnesses/` and the site show "Lab · 12 faces, genus 3 (type 0)". It is a real polyhedron in space:
- 12 flat faces;
- no self-intersections, checked in exact arithmetic;
- only **48 of the 66** face pairs touch;
- **3** holes instead of 6.

A **handle** is a tunnel that adds one hole and 6 new touching pairs: 48 -> 54 -> 60 -> 66.

"Its map extends to type 0 by 3 handles" means this. On paper, in the map alone, three specific handles can be
attached, and the result is exactly map number 0 of the 59. So at the level of the map the object is not a dead
end. Our other genus-3 object is a dead end: its map can grow to 54 pairs at most.

The **certificate** in `verification/certificates/type0_handle_completion/` lets anyone check those three handles
on paper without trusting us.

"**Realizing them geometrically**" means moving the planes so that these tunnels really appear in space, still
without self-intersections. That is the unsolved part, and there is no guarantee that it is possible. An analogy:
3 of 6 floors are built, and the plan of the remaining floors is consistent on paper. Nobody knows whether the
upper floors can stand.

## Computation and proof

- **SAT / UNSAT.** The question is written as a large system of logical conditions and given to a **SAT solver**.
  It answers in one of three ways:
  - **SAT**: it found an example where every condition holds;
  - **UNSAT**: it proved that no such example exists;
  - **timeout / UNKNOWN**: it ran out of time. That is not an answer.

  An UNSAT holds **only for the system we wrote**. If the system fixes particular face directions, "impossible"
  is proved for those directions, not for the whole problem. `SPEC.md` §4 lists the three scopes of a negative
  result: instance, family, theorem.
- **CNF, DRAT.**
  - CNF is the file format of the conditions given to the solver.
  - A DRAT file is a step-by-step record of the solver's UNSAT proof. A separate small program, `drat-trim`,
    checks it, so nobody has to trust the solver. Our DRAT files are in the GitHub release `state-2026-11-01`.
- **Exact check** (EXACT). Computing with fractions instead of rounded decimals. Only an exact check counts as
  evidence that an object is correct. The single solution check is
  `verification/verify_candidate.py FILE --target S0`.
- **Chirotope / oriented matroid.** For each triple of planes we record on which side things lie: signs of
  determinants. This turns geometry into logic that a SAT solver can handle.
- **Gauss map and its degree.**
  - Each face has a normal direction, a point on the sphere.
  - How many times these normals "wrap around" the sphere is fixed by the genus: it must be `1 - g`, so -5 for
    Szilassi-12.
  - `k_tau` is how much one more handle changes this number.
  - This explains why type 0 does not get past genus 3 to genus 4: the next handle would need -1, and the
    available ones give 0.
- **Normals first.** Pick face directions with the right Gauss properties first, then let an exact solver
  search for the plane offsets. This gave 12,202 UNSAT results. A control run showed the method may simply search
  badly, so this is weak evidence; experiment E02 measures it.
- **Q1.** A single run on type 58. The face directions satisfied the Gauss conditions on every level, yet the
  offsets were UNSAT already at the first level. So "the right Gauss class" alone is not enough. The result
  holds for that one instance only.
- **Near-miss.** A numerically "almost" solution. It counts for nothing until the exact check confirms it. All
  1,005 known near-misses from a public collection turned out to be in the wrong Gauss class.
- **Witness.** An exactly verified object, such as our genus-3 objects. The curated ones are in `witnesses/`.
- **Symmetry results.**
  - FD5: no symmetric Szilassi-12 exists. CERTIFIED; it reproduces Moki & Julio 2026.
  - FD6: there is not even a symmetric immersion. DRAT-checked, EXACT; the written proof is ROADMAP E08.
  - So any solution must be asymmetric.

## Targets, labels and IDs

- **Targets.**
  - **S0** is Szilassi-12 itself, the only "solution".
  - **S1** allows doubled adjacencies, like the 8-face Mizhaev and Röst–Vígh polyhedra.
  - **S2** is an immersion.
  - **S3** is a partial object, like our genus-3 ones.
  - **S4** covers smaller analogues.
- **Evidence labels** (`SPEC.md` §5):
  - **CERTIFIED**: a computer proof with a checked certificate and a written soundness argument;
  - **PROVED**: a proof checked by an independent reviewer;
  - **PROVED-1**: a proof without review. Anything written by an AI is at most this.
  - **EXACT**: an exact computation;
  - **NUMERICAL**: a floating-point observation;
  - **CLAIMED**: someone else's statement that we have not reproduced.
- **Verdicts for methods** (`STATUS.md` §3):
  - **LOW-YIELD@budget**: the method was tried and gave little at that budget. It is not refuted.
  - **REFUTED**: needs a proof. No method is REFUTED today.
- **IDs.**
  - **FD**: a foundation we rely on.
  - **DR**: a direction of search.
  - **E##**: an experiment in the queue (`ROADMAP.md`).
  - **H#**: a competing hypothesis that experiments try to tell apart (`STATUS.md` §3a).
