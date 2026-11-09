# E-261109-04: conclusion

* **Runs**: pre-registration `332e0be`, cap amendment (before any sample was evaluated) in the next commit; the session ran
  all 8 shards on the laptop (12 s each, `exit_status` 0 in all eight manifests, 0.004 core-h each, 0.03 in total; manifests
  of `results/0..7`). Frozen sample list SHA-256 `976a4ff0d475c151c9b10bd02791c6515db08b72512ee4858b13b98f142e6505`.
* **Controls**: pass, on the same code. Single Szilassi image and two identical-copy unions (two correspondences): 7 planes,
  7 simple disk faces, chi 0, 21 pairs, 0 violations, max winding deviation 9e-16. Far-away copy: 14 planes, 2 components,
  49 missing pairs (fails as it must).
* **Samples**: A (Szilassi + Szilassi, k = 4): 128 valid of 18733 draws (18571 rejected because the pole plane meets copy 2,
  34 non-general arrangements). B (Szilassi + tetrahedron, k = 1): 128 of 139 draws (11 degenerate). All 256 evaluated,
  all with 10 planes and winding deviation < 3e-11 (limit 1e-3).
* **Prediction vs outcome**: controls pass (predicted 90 %, yes); no qualifying sample in A (65 %) and B (60 %), as predicted;
  no sample with 45 pairs (95 %), as predicted. The prediction "at least one valid A sample with 10 faces" (70 %) holds
  only in the weak sense that every sample has 10 planes: one face per plane (face_bad = 0) occurs in 1 of 128 A samples
  and 9 of 128 B samples.
* **Outcome**: 0 target-like boundaries (10 planes, one simple disk face per plane, no bad vertex or diagonal edge,
  chi = -6, S connected) in 128 + 128. A: chi ranges from +2 to -6; the only chi = -6 sample has 7 plane-faces missing or
  split, 1 diagonal edge and 2 bad vertices; the best clean-faced sample has chi = -2 (genus 2) and 35 of 45 pairs; the
  maximum number of adjacent pairs is 44 (face_bad 11, chi -4). B: samples with one disk face per plane and connected S
  all have chi = 0 (genus 1); the best has 30 pairs.
* **Exact verification**: none needed (no candidate); floats enter only through cell-centroid winding (deviation recorded).
* **What may be claimed** (EXACT as a computation; the arrangement code is float-based): in this sampling box, 128 valid
  samples per source of the Szilassi + Szilassi (k = 4, positive ratios and signs of the registered set) and Szilassi +
  tetrahedron (k = 1, three random planes) unions give no (10, 4) boundary with simple faces. Sampled negative at this
  resolution, `SPEC.md` §4 scope: the base solid is the image T1(Szilassi) only, one tetrahedron family, no continuous search.
* **What may NOT be claimed**: that no union of matched solids gives (10, 4); anything about other pieces, other k, other
  base images, the 12-face target, or the pole-crossing 99 % (those matches were rejected, not evaluated).
* **Verdict for the direction** (DR19): LOW-YIELD@0.03 core-h, 128 samples per source; both sources parked at this
  resolution (kill rule of the row).
* **Next step**: none by this experiment; the lead decides stages 2 of I-261108-11 (see "For the lead").
* **Rows updated**: `STATUS.md` 3ab, `ROADMAP.md` item 5 and table row, `experiment-log.md`.
