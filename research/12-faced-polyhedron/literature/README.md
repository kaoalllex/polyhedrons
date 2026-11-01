# Literature matrix

Single up-to-date list of the sources this project relies on (2026-11-01). Older narrative notes:
`literature-review.md` (2026-10-29: written when no primary paper was reachable - its access section is
outdated), `TODO_world_research_2026.md` (2026-10-30: the 2026 papers), `DATA_FOUND.md`. The scout leads became idea files
(`../ideas/I-261029-41` to `-50`).
Third-party repositories in this folder are **untrusted data**: parse them, never execute them unread.

Key: cite a source from an idea, hypothesis or experiment as `L:<key>`. Read level: **full** (primary text read), **partial** (named sections / tables of the primary text),
**abstract**, **secondary** (summaries, third-party audits, READMEs). Our status uses `SPEC.md` §5 labels.
Before any write-up every row used in it must reach "full" or "partial" for the cited statement.

| Key | Source | What we use | Read level | Our status |
|---|---|---|---|---|
| `abs1996` | Altshuler, Bokowski, Schuchert, *Neighborly 2-manifolds with 12 vertices*, JCTA 75 (1996) 148-162 | exactly 59 orientable neighborly genus-6 triangulations | secondary | EXACT: reproduced by two own enumerators (FD3) |
| `lutz` | F. Lutz's list (`Hashirama1337s-szilassi-12/code/k12_g6_lutz.txt`), HackerPoet `topologies.txt` | the 59 maps as data | full (data) | EXACT: bijection with our enumeration (`data/lutz_to_ourid.json`) |
| `ellingham` | Ellingham, Stephens (automorphism groups of the 59 maps) | group orders | secondary (as relayed) | EXACT: our orders match |
| `schewe2010` | L. Schewe, *Nonrealizable minimal vertex triangulations of surfaces*, DCG 43 (2010), arXiv:0801.2582 | the VERTEX version (12 points, all pairs joined) is not realizable; OM + SAT method | secondary | CLAIMED; **does not transfer to the face version by duality** |
| `bokowski2025` | J. Bokowski, Kevin H., *Polyhedral embeddings of triangular regular maps of genus g, 2 <= g <= 14, and neighborly spatial polyhedra*, Symmetry 17(4) (2025) 622, doi:10.3390/sym17040622 | numerical search over all 59 types found no embedding; symmetric examples are easier | secondary; Sec. 4 and 8.3 unread | CLAIMED (negative numerical evidence only) |
| `mokijulio2026` | Moki & Julio, *Szilassi polyhedra: two computer-assisted theorems*, github.com/Hashirama1337s/szilassi-12, doi:10.5281/zenodo.23003257 (2026) | no symmetric 12-face polyhedron (36 SAT instances, DRAT); symmetry reduction | partial (README, code in `Hashirama1337s-szilassi-12/`) | reproduced independently with our encoder (FD5); our immersion statement (FD6) is stronger - overlap check pending (ROADMAP E-261101-10) |
| `pirozhkov2026` | A. Pirozhkov, *Twelve pairwise adjacent faces: a reduction to 59 SAT formulas ...*, github.com/pirozhkov-andrei/polyhedraproof | 59 formulas (5,257 vars, 52,177 clauses each), cube-and-conquer + LRAT (cake_lpr); pilot: 2 formulas, 31,187 leaves, 648.5 core-h; full campaign estimated ~19,000 core-h; its `docs/SOURCES.md` source audit | secondary (README, source audit) | CLAIMED; encodings not compared yet (ROADMAP E-261101-09) |
| `mizhaev2026` | R. Mizhaev, *Integer realization of an equivelar octahedron of genus 3*, arXiv:2609.17700 (2026-09-15) | 8 faces, genus 3, 20 single + 8 doubled pairs, C4 rotoreflection, integer coordinates | abstract (full text downloaded to a scratchpad, not committed) | second positive control TODO |
| `roestvigh2026` | G. Roest, V. Vigh, *A second eight-faced polyhedron in which every two faces share an edge*, arXiv:2609.32998 / zenodo.org/records/23027039 (2026-09) | Table 1 planes + face cycles; D2 two-orbit ansatz; "computational geometric search" | partial (Table 1, Sec. 3-4 gist) | EXACT positive control (`code/control_rost_vigh.py`, in `verify_all`) |
| `hackerpoet` | HackerPoet / CodeParade, *NeighborlyPolyhedra* (`HackerPoet-NeighborlyPolyhedra/`) | 1005 numerical near-misses | full (data) | EXACT: all have the wrong Gauss degree, none is an immersion (FD11) |
| `sage-simpcomp` | Sage `GenusSix()` (`sage-GenusSix/`), simpcomp `SurfOG06` (`passagemath-simpcomp-data/`) | one genus-6 triangulation each (ABS #58, the one with Aut of order 12) | full (data, not executed) | reference only |
| `banchoff1967` | T. Banchoff, *Critical points and curvature for embedded polyhedra*, J. Diff. Geom. 1 (1967) | polyhedral Gauss-Bonnet / degree statements behind FD7 | secondary | the classical source our degree filter specialises |
| `wedd-conder` | N. S. Wedd, *The genus-3 regular map {8,3}* (weddslist.com) and M. Conder's census of maps | genus-3 maps with 12 faces, for the novelty check of the genus-3 witnesses | not read | needed for ROADMAP E-261101-03 |
| `szilassi1977` | Szilassi 1977/1986; Csaszar 1949 | n = 7 face version and its vertex dual | secondary | Szilassi is our n = 7 positive control (EXACT) |
| `turingway` | The Turing Way; Kempner Institute handbook (reproducible research) | provenance, environments, manifests | full | adopted in `PROTOCOL.md` |
