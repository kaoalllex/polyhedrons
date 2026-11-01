# Experiments

There is one folder per experiment, `E-YYMMDD-NN-<slug>/`. A laptop night, a GitHub Actions matrix and an
interactive session are all just ways to run an experiment. IDs, the header and the links are defined in
`../PROTOCOL.md` §4; the interactive map is `../map/index.html`. To see what is queued, read `../ROADMAP.md` or the
`planned` experiments here.

Each folder contains:

- **`README.md`**: the header (origin, hypotheses tested, results produced, status, verdict) plus a summary: goal,
  method, results, conclusions, next steps;
- **`PLAN.md`**: the pre-registration, written before any compute (from `_template/`, skill `experiment-start`);
- **`run.sh` and `matrix.json`**: one shard with a provenance manifest, and the shard list for GitHub Actions;
- **`results/`**: the data. Night jobs write `results/<job>/` through `run_overnight.py --results-dir`;
- **`CONCLUSION.md`** (and `REVIEW.md` when needed): written afterwards (skill `experiment-conclude`).

The experiments up to 2026-11-01 were reconstructed afterwards from the experiment log, the evidence ledger and the
night reports. They are marked `preregistered: false`. Their data was moved into their folders with history
preserved (`git log --follow`).

Files that `../verification/verify_all.py` re-checks:

- `E-261029-20…/results/szilassi_found_without_map.json`: positive control;
- `E-261030-02…/results/genus*`: solid-first witnesses;
- `E-261030-03…/results/type0_genus3_extendable*`: the type-0 witnesses;
- `E-261030-04…/results/type0_genus4_attempt_*`: negative controls;
- `E-261030-10…/results/arch/archive.json`: the realization archive.
