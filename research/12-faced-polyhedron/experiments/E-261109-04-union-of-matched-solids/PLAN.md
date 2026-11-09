# E-261109-04: union of two matched solids

Pre-registration (`PROTOCOL.md` §2) of `ROADMAP.md` week item 5 (idea I-261108-11, stage 1), committed before any run.

* **ROADMAP row / scores**: T 1 D 2 F 2 G 2 R 2 (set by this session from the item text: the topology is PROVED-1
  conditional, the outcome is decisive for the two sources); T + D = 3.
* **Question**: does the Boolean union of two exact solids, matched on k face planes by a projective map, give a boundary
  with 10 simple faces and genus 4, and how many of the 45 pairs are adjacent?
* **Hypotheses moved**: H-261103-02 (S5 solids from arrangements) through the new source only; nothing else.
* **H1**: some sample has 10 planes, one simple disk face per plane, no bad vertex or diagonal edge and chi = -6. **H0**:
  none in 128 samples per source (the source is parked at this resolution, a sampled negative, not an exclusion).
* **Objects**: Szilassi from `index.html` (`szilassi.py`; its 7 planes have three triples without an affine triple
  point, so the arrangement code cannot take them). Base solid B = image of Szilassi under the fixed map
  T1 = [[1,0,0,0],[0,1,0,0],[0,0,1,0],[1/20,1/30,1/40,1]] on homogeneous points (exact `Fraction`); the check "all 7 planes
  have triple points, w > 0 on the 14 vertices" is run in `union.py` and stops the run if it fails.
* **Source A** (Szilassi + Szilassi, k = 4, 3 parameters): copy 1 = B; copy 2 = M(B) with G = M^-T mapping four planes
  B_tau(i) to lambda_i B_sigma(i), G = [lambda_i B_sigma(i)] [B_tau(i)]^-1, lambda = (1, r2, r3, r4), r = +-m with m in
  {1/4, 1/3, 1/2, 2/3, 3/2, 2, 3, 4}. Correspondence (tau, sigma) = ordered 4-tuples of distinct planes with both
  4-sets linearly independent. Frozen order: `random.Random(2611090401)` draws correspondences; each gets 8 ratio triples;
  samples are kept in draw order until 128 are valid (pole plane misses both solids: all 14 vertices of copy 2 have
  the same sign of w, exact; the 10-plane arrangement is general, i.e. `Arrangement` builds) or 400 correspondences
  are used. Invalid draws are counted by reason. Matched planes are asserted equal exactly (`Fraction`).
* **Source B** (Szilassi + tetrahedron, k = 1, 12 parameters in the idea; here 9): copy 2 = tetrahedron with one face
  on a plane B_j and three faces on planes through random points of the bounding box of B, random integer normals in
  [-9, 9]^3 (`Random(2611090402)`, 18-19 samples per j, in order j = 0..6); same validity rule (tetrahedron bounded,
  general arrangement of 10 planes), up to 2000 draws. The tetrahedron has 4 vertices, no pole.
* **Method** (`union.py`, reuses `solid_first.py`, `szilassi.py`, `planes.py`): planes of both copies, deduplicated by
  exact projective equality; `Arrangement`; S_i = `solid_from_winding` of copy i's oriented faces (orientation made
  coherent by edge traversal; tetrahedron outward); S = S_1 union S_2; `evaluate(detail)`, `boundary_euler`.
  Counters (SPEC §4 names): planes, faces = components of boundary facets, disks, bad vertices, diagonal edges, chi,
  adjacent pairs of 45 (runs per plane pair), connectivity of S through the cell graph. Floats only inside the
  arrangement (cell centroids and winding); a sample that passes the screen is re-checked exactly (`candidate-check`).
* **Controls** (before any sample; a failure stops the run): positive (a) the two identical copies (G = I, sigma = tau =
  identity) give 7 planes, 7 simple disk faces, chi = 0, 21 pairs, 0 violations, i.e. the Szilassi boundary exactly;
  (b) the same through the formula with a nontrivial lambda = (1, 1, 1, 1) and a pair of planes of B swapped in sigma and
  tau both, which is a relabelling and must give the same counters. Negative: copy 2 = M(B) with M a translation by
  (10, 0, 0) (14 planes, two components): must show violations (missing = 49 pairs, disconnected S).
* **Counter calibration**: the screen counters are integers, no float threshold. The one float step is membership of
  cell centroids (winding rounded to an integer): on the controls the maximum |winding - round| over cells must be
  < 1e-6 (the controls must show it on the same code) and is recorded for every sample; a sample above 1e-3 is
  INVALID (reported, not silently dropped).
* **Pilot / pilot gate**: shard 0 on its slice; gate: controls pass, < 5 s per sample, no crash. A full run is < 1 core-h.
* **Predictions**: controls pass (90 %); source A has at least one valid sample with 10 faces (70 %), but none with
  all faces simple, no bad vertex and chi = -6 (65 %); source B likewise (60 %); no sample with all 45 pairs (95 %).
* **Grid**: the sampling above is the grid; 128 per source; nothing is tuned after seeing results.
* **Budget**: < 1 core-h by the row, laptop, 8 shards (units split by sample index mod 8), one owner launch; a session
  can run it if < 10 min (< 0.2 core-h, then no launch is needed).
* **Power statement**: 128 samples of a 3- and a 9-parameter family detect a source only if it has non-negligible
  measure in the sampling box; absence is a sampled negative at this resolution and names the box, not an exclusion.
* **Outcomes**: control failure: stop, code bug, no claim. Zero qualifying samples: park the source at this
  resolution. Qualifying samples with missing pairs: record the histogram of adjacent pairs and the best sample for
  the lead (one separately registered continuous search is the follow-up). 45 pairs: `verify_candidate.py FILE --target S5`
  with (F, g) = (10, 4), then `candidate-check`; never an S0 claim.
* **Follow-up tree**: as week item 5 of `ROADMAP.md`; later stages are decided by the lead review, not here.
* **Stop rule**: both sources sampled, a failed control, or one session.
* **STATUS / ROADMAP**: concluded -> STATUS section 3ab, the item 5 "Done" line, the verdict in "For the lead".

## Amendments
