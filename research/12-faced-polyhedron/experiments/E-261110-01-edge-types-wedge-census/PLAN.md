# E-261110-01: edge-type tool and wedge census with its null model

Pre-registration, 2026-11-10 (lead session; week plan item 3, batched with the E-261110-03 prep). No solver, no target
claim. Not started before the owner approves the week plan.

* **ROADMAP row / scores**: T 1 D 2 F 2 G 1 R 2 (T + D = 3).
* **Question**: does the tool that measures sharp wedge pairs work on controls, and do the pairings seen in Szilassi,
  Roest-Vigh and Mizhaev exceed chance inside their own plane families?
* **Hypotheses moved**: none (`tests: []`). It calibrates the covariate of H-261110-02 and checks the two statements
  of I-261110-07 on data.
* **H1 / H0**: H1 (the session's reading): the pairings are within chance for Szilassi and Roest-Vigh; Mizhaev's are
  rare in its family. H0: the session's numbers do not reproduce from committed code.
* **Why**: the observation is the only evidence behind I-261110-01, it came from a script that is not in the
  repository, and its null model used a D2 stand-in for Mizhaev's S4 family.
* **Method**: `code/edge_types.py`, input (planes, links), exact rational arithmetic for every sign:
  * outward orientation from the signed volume; edge convexity = sign of (n_f x n_g) . t along the oriented edge;
  * vertex type from the three edge signs and, independently, from `code/vertex_types.py` (float) as a cross-check;
  * interior dihedral angle per edge (float, from the exact normals; a diagnostic, SPEC §4);
  * wedge covariates: `wedge_edges(theta)` = size of a maximum matching among the convex edges with interior angle
    <= theta (faces as vertices); `wedge_planes(theta)` = the same on plane pairs with acute plane angle <= theta
    (defined for an arrangement without a solid; the covariate of E-261110-03).
  Inputs: Szilassi (`witnesses/`), Roest-Vigh (`code/control_rost_vigh.py`), Mizhaev
  (`literature/mizhaev2026-planes.json`, read as data), the two S3 witnesses of STATUS §2, the 247-realization
  archive. Null model: 20,000 samples per row, fixed seeds, families isotropic (7, 8, 9, 12 planes), C2 (7), D2 two
  4-orbits (8), S4 two 4-orbits (8); thresholds 10.2, 24.5, 40.2 degrees. 8 worker processes for the archive and
  the null model.
* **Controls**: cube (12 convex edges at 90 degrees, 8 convex vertices); an L-shaped prism (exactly one reflex edge,
  270 degrees); vertex counts equal I-261101-20 (Szilassi 6 convex of 14, both 8-face objects 4 of 24); per-pair null
  frequency equals 1 - cos t within 3 sigma at the three thresholds; planted arrangements with exactly k pairs at
  angle a give `wedge_planes` = k for theta just above a and k - 1 or less just below (k = 3, 4, 6).
* **Pilot**: the controls above plus Szilassi; it exposes an orientation or matching bug in seconds.
* **Pilot gate**: not a long run; the census starts when every control passes.
* **Predictions**: (P1, ~85 %) edge counts reproduce the session: Szilassi 16 convex + 5 reflex, Roest-Vigh 20 + 16,
  Mizhaev 22 + 14; (P2, ~80 %) null frequencies within 0.05 of the session's table for the rows it simulated;
  (P3, ~50 %) Mizhaev's event (4 disjoint pairs <= 10.2 degrees) has frequency <= 0.15 in the S4 family;
  (P4, ~90 %) "saddle iff mixed edge signs" on every vertex of every input; (P5, ~60 %) "the reflex corner is
  opposite the odd edge" on every saddle.
* **Grid**: the three thresholds; no other parameter.
* **Budget**: 1 session, < 0.1 core-h, laptop, day.
* **Power statement**: decides whether the tool is correct on controls and whether the session's tables reproduce; it
  cannot show that wedges help a search (that is E-261110-03).
* **Counter calibration**: the planted-pair control puts an input on each side of every threshold; the 1 - cos t check
  calibrates the sampler.
* **Scenario move**: none.
* **Outcomes**:
  * all controls pass, P1-P2 hold: the covariate is usable; E-261110-03 may start;
  * a control fails: fix the tool; two failed attempts -> escalate, E-261110-03 does not start;
  * P1 or P2 fails with passing controls: record the committed numbers as the reference, mark the session's table as
    not reproduced in I-261110-01;
  * P4 or P5 fails: record the counterexample in I-261110-07; E-261101-15 keeps the vertex-type basis.
* **Follow-up tree**: none beyond E-261110-03; `verify_candidate.py` gets the edge-type report field only after the
  controls pass and `verify_all.py --quick` stays green.
* **Stop rule**: all inputs and null rows computed, or a failed control.
* **STATUS / ROADMAP**: ROADMAP row to done; no STATUS row unless P1-P5 give an EXACT statement worth a line in 3ae.

## Amendments
