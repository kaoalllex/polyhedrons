# E-261103-06: embedded first, planar later - R1 pilot (Szilassi from a torus)

Pre-registration, 2026-11-07, branch `lab/2026-11-07`. Week plan item 2. Explore. Target: S5 at (F, g) = (7, 1) only
(the Szilassi calibration rung R1); the (8, 3) rung R2' is a follow-up, nothing at (9, 3) here.

* **ROADMAP row / scores**: T 1 D 2 F 2 G 2 R 1 (T + D = 3).
* **Question**: starting from a smooth embedded torus split into 7 regions with the K7 map, does planarity
  minimisation under a non-intersection check reach 7 planar regions without leaving embedding?
* **Hypotheses moved**: H-261101-07 (maximal genus-3 existence), only through the method's viability. R1 pass does
  not move it; R1 fail parks the method, no credence move. Scenario credences unchanged.
* **H1**: at least one of the 6 starts converges (planarity energy below 1e-12 with every step embedded) and its
  7 plane fits pass `verify_candidate.py --target S5` after rounding. **H0**: all starts plateau above zero or are
  blocked by the barrier.
* **Why this**: every plane-based engine stalls at genus 3-4 (H-261101-10); this one never leaves embedding and has
  no ladder (`ideas/I-261103-01`). New relative to parked methods: surface mesh, not planes, is the variable.
* **Method** (`embfirst.py`, new, numpy + scipy only): mesh = N x N grid on the flat torus R^2/Z^2 (N = 28),
  triangulated, mapped to a standard torus (R/r in {2, 3}). Regions = Voronoi cells of the 7 lattice points
  (k/7, 2k/7) in the metric making that lattice hexagonal (assigned per triangle centroid). Control of the start: the 7
  regions are connected and all 21 pairs are adjacent through a shared boundary vertex pair. Energy = sum over
  regions of the squared distances of the region's vertices (boundary vertices belong to every adjacent region) to the
  best-fit plane, plus 1e-3 x edge-length regularisation to keep triangles non-degenerate. Descent: L-BFGS-style steps
  with backtracking; a step is accepted only if the mesh passes the intersection test (non-adjacent triangle pairs,
  KD-tree candidate pairs, exact triangle-triangle test) and no vertex moves more than 0.25 of its nearest
  non-neighbour distance (so a sheet cannot tunnel between two checks). The verdict is the exact verifier alone: fit
  7 planes, round to integers (scale 1e3..1e6), run the E-261103-05 solid-first engine (`best_solid`, E = 21, one run
  per pair) on them, then `verify_candidate.py FILE --target S5`.
* **Controls**: positive (must succeed): the detector reports no intersection on the 6 start meshes; the energy
  reads < 1e-20 on a coplanar point set; the exact tail (round, solid-first, `--target S5`) accepts the known
  Szilassi planes of `experiments/E-261101-25-chirotope-first/szilassi_control.json`. Negative (must fail): the
  detector reports an intersection on a torus whose handle is pushed through itself; the energy reads > 1e-3 on random
  points; `--target S5` rejects the same planes with one plane perturbed.
* **Counter calibration**: planarity energy threshold 1e-12: coplanar points (< 1e-20) below, random points and the
  untouched round-torus start (both > 1e-3) above. The intersection test is calibrated by the two torus meshes.
* **Pilot / gate**: one start, 300 steps, to measure the step cost; the long run starts only if one step costs < 2 s
  (so 6 starts fit 1 core-h). The limit that should bind: step acceptance (barrier or displacement cap) rather than
  the wall clock; both are logged per step.
* **Predictions**: (1) all controls behave as stated (~85 %). (2) at least one of 6 starts reaches energy < 1e-12
  with the barrier on (~30 %). (3) when energy plateaus, the barrier or displacement cap is the active limit in most
  accepted-step rejections (~60 %).
* **Grid**: R/r in {2, 3} x lattice orientation (shear 0, 1, 2 of the 7-point lattice: points (k/7, jk/7), j = 2, 3, 4,
  all giving K7 hexagonal cells). 6 starts. A start is a run, not a seed grid; no random restarts.
* **Budget**: <= 1 core-h, 1 worker per start, laptop, one shard, bounded 10 min per start. Not a night.
* **Power statement**: detects whether a smooth round-torus start with this energy can be flattened to the Szilassi
  or any K7 torus polyhedron on this mesh resolution. It cannot exclude other starts, finer meshes, other energies,
  or other maps; a plateau shows the failure mode of this mesh, not impossibility.
* **Outcomes**: SAT (converged + `--target S5` PASS) -> R2' on an (8, 3) map in the same session if < 1 core-h.
  Plateau above 0 with barrier active -> kill: park, record energy trace and the active constraint. Intersection
  detector failing a control -> stop. timeout -> no information (not a kill). near-miss: energy 1e-12..1e-8 -> only
  the exact tail decides.
* **Follow-up tree**: R1 pass -> R2' (8, 3) control in the same session if < 1 core-h; R1 fail -> park with the failure
  mode; any plateau diagnosis beyond that goes to "For the lead".
* **Stop rule**: 6 starts decided or 1 core-h; kill as in the row.
* **STATUS / ROADMAP**: STATUS section 3u and ROADMAP State done|killed with the verdict; scenario unchanged.

## Amendments
