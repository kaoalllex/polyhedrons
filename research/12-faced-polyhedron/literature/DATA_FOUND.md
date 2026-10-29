# DATA FOUND: the 59 neighborly genus-6 12-vertex triangulations

Written 2026-10-29 by literature-researcher.

**File:** `research/12-faced-polyhedron/literature/HackerPoet-NeighborlyPolyhedra/topologies.txt`
- Format: plain text, 59 lines `no.NN t1 t2 ... t44`, each `t` a triangle written as 3 hex digits (vertices 0..9,a,b).
- Content: 59 triangulations, 12 vertices, 44 triangles each.
- Source: https://raw.githubusercontent.com/HackerPoet/NeighborlyPolyhedra/main/topologies.txt (GitHub repo HackerPoet/NeighborlyPolyhedra, third-party; the repo README says it ships "the 59 topologies"). Downloaded 2026-10-29. sha256 `cadaa7c7a386015d7aa659bdca677e303d05ff9481c5352046a1a7343f98e356`.
- Provenance upstream of that repo (Lutz / Altshuler-Bokowski-Schuchert) is NOT stated in the file; treat as untrusted third-party data.

**Independent verification (done here, script `literature/verify_59.py`, run with `python3 -I`):**
all 59 entries are closed orientable simplicial surfaces (44 triangles, 66 edges each in exactly 2 triangles,
all 12 vertex links are single 11-cycles, orientable); the 59 canonical forms are pairwise distinct (non-isomorphic);
so the file is a list of 59 pairwise non-isomorphic neighborly orientable genus-6 triangulations. That the list is COMPLETE rests on
Altshuler-Bokowski-Schuchert 1996 (count 59); the file's count matches it.
Numbering: `no.58` is isomorphic to Sage's `simplicial_complexes.GenusSix()` which Sage documents as number 58 of [ABS96] with symmetry group of order 12,
so the file's `no.NN` appears to be the ABS96 numbering (1-indexed). (Inference from one match; not proven for the other 58.)
Full automorphism-group orders (including reflections) computed here: histogram {1:39, 2:9, 3:1, 4:7, 6:2, 12:1}.

Secondary data: `sage-GenusSix/` (the one triangulation, copied from Sage source) and `passagemath-simpcomp-data/extracted/SurfOG06.scb` (one genus-6 surface in GAP/simpcomp binary format; not the full list; not otherwise used).

## Second, better-provenance copy (added)

**File:** `literature/Hashirama1337s-szilassi-12/code/k12_g6_lutz.txt` (25272 bytes), format = Lutz "Manifold Page" text, 59 blocks `manifold_lex_d2_n12_o1_g6_#K=[[a,b,c],...]`, 1-indexed vertices, numbering #1..#59 (Lutz numbering).
- Source: https://raw.githubusercontent.com/Hashirama1337s/szilassi-12/main/code/k12_g6_lutz.txt (third-party GitHub repo, AI-assisted authors "Moki & Julio", 2026, Zenodo DOI 10.5281/zenodo.23003257). Downloaded 2026-10-29. sha256 `55912614618733476d07094ca4ed638df84ab58b42e8dba9eb81730da1a589b7` (equals the hash the repo README states).
- The repo claims it is a copy of F. H. Lutz's `manifold_lex_d2_n12_o1_g6` list; we could not fetch Lutz's own file (page.math.tu-berlin.de blocked in this sandbox), so this equality is UNVERIFIED.
- Verified here: 59 entries, all valid orientable neighborly surfaces, pairwise non-isomorphic, and the SAME 59 isomorphism classes as `HackerPoet-NeighborlyPolyhedra/topologies.txt`. Cross-map Lutz # -> HackerPoet no. printed by `python3 -I verify_59.py Hashirama1337s-szilassi-12/code/k12_g6_lutz.txt HackerPoet-NeighborlyPolyhedra/topologies.txt`
  (e.g. Lutz #54 = HackerPoet no.58 = Sage GenusSix() = ABS96 #58 (group order 12)).
- Also stored from that repo: `code/automorphisms.json`, `results/certificates.csv`, `code/omsat.py`, `code/autos.py`, README.md (all untrusted; not executed).
Lutz numbering and ABS96 numbering are DIFFERENT; keep a mapping table when citing "map #k".

Update: the third-party repo pirozhkov-andrei/polyhedraproof (docs/SOURCES.md) reports downloading Lutz's `manifolds_lex_d2_n12_o1_g6.txt` from the Manifold Page on 2026-10-13/15 with size 25,272 bytes and raw sha256 identical to the hash above, so the Hashirama copy is very likely byte-identical to Lutz's file (not verified by us; Lutz's page is blocked in this sandbox).
