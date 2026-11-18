# Ideas triage, 2026-11-18 (owner's ideas of 2026-11-18, prompt B of the root `TODO.md`)

Session: the lead review of 2026-11-18 (`strategy-review-2026-11-18.md`), after the owner's approval. Nothing here is
evidence: an AI session wrote it (`SPEC.md` §5). The owner's ETH and Degen ideas are in the review (§5; dropped,
owner-approved 2026-11-18). Marks V N L F, 0-3: mathematical validity, novelty, research leverage, feasibility on the laptop.

## 1. Knot theory: what can it give us?

| Question | Existing ids | V N L F | Verdict, next step |
|---|---|---|---|
| Q1. Does a topological invariant (linking numbers, the Seifert form, Heegaard position) give a necessary condition beyond the OM encoding? | DR16 (Gauss clauses), FD7, FD9 | 3 0 0 1 | **drop.** Every map embeds topologically (standard Heegaard position), so topology alone excludes no map; only straightness does. The chirotope plus the solid fixes the embedding, so any topological identity is already implied. At best it adds redundant clauses, and DR16 found no speed-up |
| Q2. Do linear-embedding theorems (every spatial K6 has linked triangles, every spatial K7 a knotted Hamiltonian cycle: Conway-Gordon-Sachs; every linear K7 a trefoil: Ramirez Alfonsin) obstruct? | none | 2 0 0 2 | **drop.** They hold in every embedding, so they obstruct nothing. Our face graph K_F lies on the surface with bends at the shared edges; it is not a linear K_F (CLAIMED, from memory) |
| Q3. Can knot theory serve as a tool where topology genuinely matters? | I-261110-01 (wedges), I-261101-18 | 2 1 1 1 | **park, as part of idea 2.** One such place is the capping condition: the skew boundary of a curved face must bound an embedded disk that misses the other faces, an unknotting / unlinking check. The other is the ansatz "surface = boundary of a thickened polygonal graph" (nearest: wedge plates) |

## 2. One curved face: quasi-polyhedra and their straightening (owner's clarification 2026-11-18)

Reading: F - 1 planar polygons plus one non-planar face S spanning a skew polygon. Its vertices lie on the lines X ∩ Y,
so the planar faces stay polygons. Curved edges would make the neighbours non-polygons and the object no polyhedron.
The owner's intent: quasi-polyhedra are not solutions. Either S can be straightened (a route to a solution), or it
provably cannot.

* **Logic.** A solution is a quasi-polyhedron whose S is already planar. So "no quasi-polyhedron can be straightened"
  is equivalent to "no solution": in general neither direction is easier. The idea helps where the quasi-objects of a
  case form a small explicit list, because straightening one list member with the other planes fixed is a ninth- or
  twelfth-plane cell question (Stage A, E-261113-03, N3 = I-261117-03: a linear program per sign vector). A failure
  with all planes moving is the full formula.
* **Existing line.** This is the face ladder (I-261101-18): k-face sub-instances (E-261101-23, E-261102-01) were SAT at
  k <= 9 wherever decided, k = 10 timed out, no model realized; k = 11 is S0 with one free face and was never run.
  Repair of a defective face is DR4 (closure-first planarity defect: zero defect only with >= 11 non-simple faces)
  and DR5 (near-miss repair: all 1005 near-misses in the wrong Gauss class). What is new: exactly one defective face,
  a quasi-object checked exactly, and a straightening rung with a known answer.
* **Session check (EXACT, combinatorics only; `ideas-triage-2026-11-18-strip.py`, 0.06 s).** Could a curved ninth face be
  cut out of a known eight-face object? D must be a disk, and a band through a face interior splits that face. So D
  is a thin neighbourhood of a tree in the 1-skeleton. Every tree edge consumes one adjacency segment, which only a
  doubled pair can spare. In Roest-Vigh's and in Mizhaev's object the 16 doubled-pair edges form components of at
  most 3 edges, and none touches more than 6 of the 8 faces. **This local surgery gives no nine-face quasi-polyhedron**
  from either object. Scope: D on the old surface, planar faces unchanged; planes that move are not covered.

| Question | Existing ids | V N L F | Verdict, next step |
|---|---|---|---|
| Q1. (9, 3) deletion sieve: for each of the 203 admissible maps and each face, the formula without that face (9 elements) | I-261101-18, H-261101-15 (its S0 form), E-261109-05 (contraction, another relaxation) | 3 2 2 3 | **keep, queue (not this week).** 1827 formulas at 9 elements, kissat seconds each, <= 1 core-h, 10 shards, no proofs. All UNSAT-SOLVER: the (9, 3) obstruction needs only 8 planar faces, and there are no (9, 3) quasi-polyhedra to straighten. A SAT: the bridge realizes the 8 planes, S is built on the lines, the capping is checked; these are the first quasi-polyhedra, and their non-straightening is already the UNSAT-VERIFIED full formula of their map (STATUS 3d) |
| Q2. Straightening rung with a known answer: bend one face of Roest-Vigh's object (move its vertices along their lines), then minimise S's planarity defect with the planes free | DR4, DR5, E-261101-24 (Farkas descent) | 2 1 1 2 | **park until Q1 has a SAT.** A repair engine must return the planar object from a small bend before any target run (benchmark-ladder rule); 1 session |
| Q3. Nine faces (focus) and S0 with one curved face as targets in their own right | E-261101-23, E-261102-01; STRATEGY §1 filter | 2 1 1 0 | **park.** Below the significance filter (owner: not a solution); the nine-face census is too large for per-map deletion, and S0 at k = 11 has 12 elements per formula and S0 is parked |

## 3. Claims resting on memory

Conway-Gordon-Sachs and Ramirez Alfonsin (linear K7), Waldhausen (Heegaard splittings of S^3 are standard): CLAIMED,
not read here; no decision rests on them. The DR4 / DR5 summaries are from `ROADMAP.md` "Parked methods".

## 4. For the owner

Keep: idea 2 Q1 in the queue (one lab session, <= 1 core-h). Drop: idea 1 except its capping role in idea 2.
Nothing changes this week's order. Filing is a later lead session after your approval.
