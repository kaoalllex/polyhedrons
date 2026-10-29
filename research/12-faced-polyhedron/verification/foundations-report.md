# Adversarial verification of the foundations (V1–V3)

Verifier: adversarial-verifier (claude-opus-5-5, effort max), 2026-10-29.
Scope: the PI narrowed the task mid-run (usage limits) to **V1(b)** (Lemma 5.1) and **V2**
(the §5.2 in-face predicate), plus **V3** (fastviol) where quick. **V4 was skipped.** V1(a)
was checked by hand only, without dedicated computations. V1(c) was checked by computation
because it came for free.
No code from `../code` was trusted or imported, except `code/fastviol.py` itself, which V3 runs
as the object under test.
All of my code is in this directory: `exact_core.py` (exact integer/Fraction library),
`test_v1_v2.py`, `test_szilassi.py`, `test_v3_fastviol.py`, with logs and JSON outputs beside them.

## Verdicts

| Item | Verdict | Short reason |
|---|---|---|
| V1(a) face-plane reduction, openness, WLOG GP | ACCEPT with a minor correction (hand check only) | §2's reason for "three planes at a vertex are independent" misses the case of two coincident planes. A nondegeneracy convention must be stated in §1. |
| V1(b) Lemma 5.1, both directions | **ACCEPT** | The proof is correct under GP. Every listed suspect case is covered. Exact tests found 0 counterexamples to the lemma's finer intermediate claims. |
| V1(c) sign formulas §4/§5.1 | **ACCEPT** (direction to be stated explicitly) | `side` formula: 0 failures. Order formula: 0 failures when the direction is u* = n_Y × n_X; 100 % reversed for n_X × n_Y. |
| V2 in-face predicate §5.2 | **ACCEPT** | Proof below. The predicate equals "on the curve or odd mod-2 winding number" for every GP polygon, simple or not. Exact agreement with direct point-in-polygon in all tests. |
| V3 fastviol.py | **ACCEPT** | Faithful implementation. Exact violation sets agree on 1797/1797 near-misses and 300/300 random configurations. There were no disagreements. |
| V4 | not done (scope cut by PI) | Hand remark only, see end. |

---------------------------------------------------------------------------------------------

## V1(b) Lemma 5.1

Notation: GP means that no 4 of the 13 vectors `h_1..h_12, h_∞` are linearly dependent (all 715
4×4 determinants are nonzero). `F_X` is the polygon curve of face X together with the points of
odd crossing parity (mod-2 winding number).

**(⇒)** This direction needs no GP. In an embedding, the abstract faces X and Y meet exactly in
the closed abstract edge XY, so injectivity gives `F_X ∩ F_Y = e_XY`. For a non-triangle triple,
the abstract faces X, Y, Z have no common point, so `F_X ∩ F_Y ∩ F_Z = ∅`. The one point that
must be checked is that, for a simple polygon, the parity region equals the closed Jordan disk.
It does. Correct.

**(⇐)** I checked each step line by line, assuming GP.

1. *Simplicity.* Edges `e_XW1 ⊂ L_XW1` and `e_XW2 ⊂ L_XW2` lie on distinct lines in `H_X`,
   which meet only at `P_XW1W2`.
   * If `XW1W2` is a triangle, the edges share that vertex and meet nowhere else.
   * Otherwise a crossing puts `P_XW1W2` on the curve of X and on the curves of W1 and W2 (each
     edge is shared by both of its faces), so the triple is violated.

   Every other form of non-simplicity would need 4 concurrent planes, which GP excludes:
   * collinear overlap;
   * a vertex on a non-adjacent edge (`P_XAB ∈ L_XW`);
   * coincident vertices;
   * a zero-length edge (`P_XWA = P_XWB`);
   * a straight corner.

   Correct.
2. *Pairs.* For `X ≠ Y` we have `F_X ∩ F_Y ⊂ L_XY`. Let p be an endpoint of a component I of
   `F_X ∩ F_Y`. If I is a single point, p is that point.
   * If p were interior to both faces (relative to their planes), a neighbourhood of p in
     `L_XY` would lie in I. So p lies on the curve of X or of Y. This also holds for parity
     regions of non-simple curves, because the topological boundary of the parity region is
     contained in the curve.
   * Say p lies on `e_XW`. If `W ≠ Y`, then `e_XW ∩ L_XY = {P_XYW}`, and `P_XYW ∈ e_XW ⊂ F_W`.
     This is a violation unless `W ∈ {C, D}`, in which case p is an endpoint of `e_XY`.

   Hence `I ⊂ e_XY`, and `F_X ∩ F_Y = e_XY`. Correct.
3. Simple faces with `F_X ∩ F_Y = e_XY` for all pairs make the map from the abstract surface
   injective: the shared edge is parametrised identically from both sides, because it has the
   same two labelled endpoints. A continuous injection from a compact space to a Hausdorff space
   is an embedding. Correct.

**Suspect cases requested in the brief, and how each is covered:**
* Non-generic configurations: the lemma is stated only under GP. This is legitimate because GP
  is WLOG (V1(a)).
* Point components of `F_X ∩ F_Y`: covered by the endpoint argument in step 2.
* Corners of X on `L_XY` other than the ends of `e_XY`: these need `X, Y, U, V` concurrent,
  which GP excludes.
* Faces meeting at a vertex but not along the edge: impossible. Every pair of faces is adjacent,
  and `F_X ∩ F_Y = e_XY` covers this case.
* A vertex `P_XAB` lying in the interior of a face Y: needs `P_XAB ∈ H_Y` (a 4-fold point), which
  GP excludes. In any case it would also be caught by step 2.
* An edge piercing the interior of a face: `e_XY` meets `F_Z` only at `P_XYZ`, and the pair
  (X, Z) then fails step 2. This is caught.

**Remark (strengthening, also tested).** The proof shows more than the lemma states, for any GP
configuration, simple or not, with parity regions:
* (i) "no violated triple contains both X and Y" implies `F_X ∩ F_Y = e_XY`;
* (ii) a non-simple polygon X lies in a violated triple `{X, W1, W2}`.

**Exact computational evidence** (`test_v1_v2.py`, seed 11; logs `test_v1_v2_seed11.log` and
`.json`; `test_szilassi.py`, log `test_szilassi.log`):

RESULTS_V1B

---------------------------------------------------------------------------------------------

## V1(c) sign formulas

With `h = (a, b, c, e)` for the plane `a x + b y + c z + e = 0`, `h_∞ = (0, 0, 0, 1)` and
`χ = sign det` of the four rows:
* Let `q = *(h_a ∧ h_b ∧ h_c)` be defined by `q·v = det(h_a, h_b, h_c, v)`. Then
  `q = det(abc∞)·(P_abc, 1)`.
* So `side(abc; d) = sign(h_d·(P_abc, 1)) = χ(abcd)·χ(abc∞)`. **Correct.**
* For the order along `L_XY`, write `P_W − P_Z = s·u`, where `u` is the spatial part of
  `*(h_X ∧ h_Y ∧ h_∞)` under the same convention `w·v = det(h_X, h_Y, h_∞, v)`. One finds
  `n_W·u = det(XY∞W) = −det(XYW∞)`, and
  `s = det(XYZW) / (det(XYZ∞)·det(XYW∞))`.
* So `sign(t_W − t_Z) = χ(XYZW)·χ(XYZ∞)·χ(XYW∞)` **holds with σ_XY = +1, for
  t = u·p with u = n_Y × n_X = −(n_X × n_Y).**

Exact test: RESULTS_V1C

**Correction suggested.** §5.1 should state the direction explicitly as `u = n_Y × n_X`. Under
the other common Hodge convention, `w·v = det(v, h_X, h_Y, h_∞)`, the sign flips. fastviol
uses the opposite direction `n_X × n_Y`. This is harmless for parity and betweenness, but any
OM-SAT clause that mixes "Plus(Z)" defined by the χ formula with geometric directions must use
one convention throughout.

---------------------------------------------------------------------------------------------

## V2 in-face predicate §5.2

**Claim (proved).** Assume GP, and let `{X, Y, Z}` be a non-triangle with `R = P_XYZ`. Then
`IN[X; Y, Z]` as defined in §5.2 equals:

> 1 iff R lies on the closed polygon curve of X, or the mod-2 winding number (even–odd rule) of
> that curve about R is 1.

This holds for every closed 11-gon (or n-gon) curve, simple or not. It holds equally for the
ray along `L_XY` or along `L_XZ`, and in either direction.

**Proof.**
* *Boundary.* R lies on `L_XY ∩ L_XZ` and on no other `L_XW`, since that would be a 4-fold
  point. R is not a vertex, because `Z ∉ {C, D}` and `Y ∉ {A, B}`. So R is on the curve iff
  `R ∈ relint e_XY` or `R ∈ relint e_XZ`. These two cases are exactly the stated side tests:
  the endpoints of the edge lie strictly on opposite sides of the cutting plane.
* *Parity.* If R is off the curve, let `ρ` be the ray `{t > t_Z}` on `L_XY`. Shift it by a small
  `ε` inside `H_X` to obtain `ρ_ε`. For small `ε`, `R_ε` has the same parity as R, and `ρ_ε`
  misses all vertices. The only vertices on `L_XY` are `P_XYC` and `P_XYD`; all others are at
  positive distance. The crossings of `ρ_ε` are as follows:
  * one near each `P_XYW` with `W ∉ {Y, C, D}`, `t_W > t_Z` and `P_XYW ∈ relint e_XW`
    (a transversal crossing);
  * if `t_C, t_D > t_Z`, the number of the edges `e_XC`, `e_XD` that leave `L_XY` towards the
    `ε`-side. This is ≡ `[side(XCC'; Y) ≠ side(XDD'; Y)]` mod 2, because `e_XC` runs from
    `P_XYC` to `P_XCC'` and the side of `H_Y` within `H_X` is the side of `L_XY`;
  * nothing else. `e_XC` and `e_XD` meet `L_XY` only at their endpoints on it. Edges disjoint
    from `L_XY` are at positive distance from it. If `t_C < t_Z`, the crossings near `P_XYC`
    lie behind `R_ε`.

  Only one of C, D being in `Plus(Z)` would mean `R ∈ relint e_XY`, which was already handled.
  ∎

**The definition of "inside" for non-simple polygons** is therefore the even–odd rule together
with the curve. It is **not** the nonzero-winding rule. Configurations with an even, nonzero
winding number (for example ±2) occur, and there `IN = 0`. Counts are in RESULTS_V2.

**Consistency with Lemma 5.1.** The lemma defines `F_X` with exactly this convention, so it is
consistent. The (⇐) proof uses only two facts: the curve is contained in `F_X`, and the
topological boundary of `F_X` is contained in the curve. Both hold for the even–odd region.
For simple polygons this region is the closed disk, which (⇒) needs.

**Exact tests** (each compares the χ-only implementation of §5.2, `exact_core.IN_chi`, with a
direct exact 2-D point-in-polygon on Fraction coordinates; also compared: the reversed ray and
the ray along `L_XZ`):

RESULTS_V2

---------------------------------------------------------------------------------------------

## V3 fastviol.py

**Code review**

The following match §5.2 and Lemma 5.1:
* `triangulation_tables`: the partner of each ordered pair (X, W) is the two third vertices.
  `istri` is filled for all 6 permutations.
* `_inface(X, Y, Z)`:
  * `C, D` are the partners of XY. The `relint e_XY` test is `side(XYC; Z) ≠ side(XYD; Z)`.
    The `relint e_XZ` test uses the partners of XZ against Y.
  * The transversal loop excludes `X, Y, Z, C, D`, uses `tw > tz`, and tests
    `P_XYW ∈ relint e_XW` with the partners of XW against Y.
  * The run is counted iff `tc > tz` and `side(XCC'; Y) ≠ side(XDD'; Y)`, where `C'` is the
    partner of XC other than Y (and likewise D'). This is correct.
* `violations`: skips triangles (`istri[a, b, c]`) and requires `_inface(a, b, c)`,
  `_inface(b, c, a)` and `_inface(c, a, b)`. These are the three faces, each with its ray on
  a line through the face. Correct.
* The ray direction `n_X × n_Y` is the opposite of §5.1's `u*`. This is irrelevant for parity.

Float-only caveats (not bugs in exact logic):
* (1) `ok = False` only if `|det| < 1e-300`, so near-singular triples are not flagged.
* (2) A value of exactly 0 is classified as negative.
* (3) The run test checks only `tc > tz` and relies on the float `relint e_XY` test being
  consistent with `td`. A float inconsistency there could add or drop a run crossing.

**Numerical comparison** (`test_v3_fastviol.py`; output in `test_v3_fastviol.json` and `.log`).
The float planes were converted exactly with `Fraction(float)` and scaled per plane by a
positive power of two to integers. The exact violation *set* was computed from the χ-only
§5.2 implementation and compared with fastviol's `violation_list` on the same float planes.

| Data | Configs | Exact GP | Count ≠ stored `ours` | Violation set ≠ fastviol rerun |
|---|---:|---:|---:|---:|
| near-misses `hp_seeds_ranked.json` | 1797 | 1797 | **0** | **0** |
| random integer planes, \|coef\| ≤ 10^6, random relabelled types | 300 | 300 | — | **0** |

**Verdict V3: ACCEPT.** I found no disagreement. Every stored `ours` value is the exact
Lemma 5.1 count of the rationalised plane configuration.

Caveat for `results.md`: the 748/1797 differences from HackerPoet's own
"crossings + intersections" are therefore **not** fastviol rounding errors. They must come from
one of two sources, and my run does not establish which:
* the reconstruction, in which planes are fitted per face and the vertices are recomputed as
  triple points;
* a different counting convention in the source.

The attribution to float32 storage in `results.md` remains unverified.

---------------------------------------------------------------------------------------------

## V1(a) (hand check only; not part of the narrowed scope)

**Vertices are triple points.** At a degree-3 vertex the three faces are distinct (§1.2), so the
vertex lies in `H_X ∩ H_Y ∩ H_Z`.

**Independence of the three planes.** The stated reason ("otherwise the three edges would be
collinear and overlap") is correct only when the three planes are pairwise distinct. In that
case they share a line, and of three rays from v on one line, two overlap.

**Gap.** If `H_X = H_Y`, the edges `e_XZ` and `e_YZ` lie on one line through v and may point
in *opposite* directions. Then face Z has a straight angle at v, and the coplanar faces X and Y
meet along a "flat" edge. This is a locally embedded configuration, and it is excluded only by
a nondegeneracy convention.

**Correction.** Add to §1 either "distinct faces lie in distinct planes" or "no corner angle
equals π". Under the second convention, `H_X = H_Y` propagates around the link of X and forces
all 12 faces into one plane, which is impossible. Either convention then gives independence.

**Openness.** Correct, given that convention. A sketch:
* The vertices depend continuously on the planes, and the triangle determinants stay nonzero.
* A simple polygon stays simple: non-adjacent edges are disjoint compact sets, and adjacent
  edges lie on distinct lines with angle ≠ 0.
* For two faces:
  * away from `e_XY`, they are disjoint compact sets;
  * near the interior of `e_XY`, they are two half-planes in distinct planes;
  * near a vertex, there are three sectors with corner angles ≠ π. The local condition "X and Y
    are not both reflex across `L_XY`" is open.

**WLOG GP.** Each of the 715 determinants is a nonzero polynomial in the 48 coefficients, so GP
is open and dense, and it meets the nonempty open realization set. The perturbation keeps the
combinatorial type trivially, since the type is the input triangulation, and openness keeps the
embedding. Rational and integer coefficients follow. **ACCEPT** with the stated correction.

## V4 (skipped by the PI)

Hand remark only. The geometric argument is sound:
* an isometry preserving S preserves the bounded complementary region, hence the outer normal,
  so it reverses the orientation of S iff it is improper;
* a symmetry fixing every face fixes all 44 vertices, which span R^3, so it is the identity.
  Hence the symmetry group injects into Aut;
* a mirror reflection and the point reflection are improper involutions.

This needs the faces to be intrinsic to S, which again uses "adjacent faces not coplanar". The
combinatorial part ("no orientation-reversing involution in any of the 59 types") was **not**
re-checked by me.

Caution about `results.md` (PI benchmark section): "Since symmetric realizations are claimed
impossible (Moki & Julio 2026)". Track 2 excludes only mirror planes and centres of symmetry.
Rotational symmetry and the S4 rotoreflection in the C4 types are not excluded by anything I
checked. That sentence rests solely on the external claim.

## Reproduce

```
cd research/12-faced-polyhedron/verification
python3 test_v1_v2.py 100000 100000 100000 11   # time-budgeted phases (~12 min)
python3 test_szilassi.py 3                        # ~1 min
python3 test_v3_fastviol.py <hp_seeds_ranked.json> 300 5
```

## What would change the verdicts

* V1(b) or V2: a GP configuration where `IN_chi` differs from the direct exact point-in-polygon,
  or where implication (i) or (ii) fails. None were found.
* Note that the 0-violation case of (⇐) was tested only on n = 7 (Szilassi perturbations). For
  n = 12 no 0-violation configuration is known.
* V1(a): a definition of the target that allows coplanar adjacent faces. Then §2's independence
  claim, and with it the face-plane model, would need revisiting.
