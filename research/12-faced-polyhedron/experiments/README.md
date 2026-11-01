# Experiments

**New experiments** (from 2026-11-01): one folder per pre-registered experiment, `E##-slug/`, copied from
`_template/` (`PLAN.md` before compute, `run.sh` = one shard with a provenance manifest, `matrix.json` = shard list
for GitHub Actions, `results/<shard>/`, `CONCLUSION.md` after). Branch `experiment/E##-slug`. Rules:
`../PROTOCOL.md` section 2; the queue: `../ROADMAP.md`.

**Legacy artifact folders** (sessions 1-5, kept as evidence; every file is re-checked by
`../verification/verify_all.py` where marked *):

| Folder | Content |
|---|---|
| `genus_ladder/` | * five exact type-0 genus-3 realizations of one extendable map; * two genus-4 attempts (negative controls, NOT embedded) |
| `solid_first/` | * Szilassi found without a map; * genus-2 and genus-3 12-face solids (dead-end maps) |
| `gauss_class/` | k-drift class seeds (genus-4 class, on the class wall) and normals-first logs incl. the positive control |
| `chain_normals/` | type-58 chain-consistent normals (all 7 levels in class; sphere UNSAT) - input for E03 |
| `omsat/` | OM-SAT validation, symmetric-instance logs, Track-4 cross-check, Lutz id map |
| `torus/` | T^3 zero-defect normal sets (closure-first, refuted direction) |
| `track4_anneal_sphere_unif_1.json` | early Track-4 annealing output |

Night-run outputs live in `../overnight/results/` (append-only JSONL per job; analysis scripts in `../overnight/`).
