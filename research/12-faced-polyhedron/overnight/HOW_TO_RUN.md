# How to run an experiment on the laptop

A night on the laptop is one way to run an experiment `E-YYMMDD-NN` (`../PROTOCOL.md` §2). Its pre-registration
(`PLAN.md`) and runner (`run.sh`) live in `../experiments/<ID>-<slug>/`. The skills `experiment-start` and
`overnight-run-script` prepare them.

## 1. One-time setup

```bash
git clone https://github.com/kaoalllex/polyhedrons
cd polyhedrons
git checkout main
python3 -m pip install -r research/12-faced-polyhedron/requirements.txt
```

The pins in `requirements.txt` come from Python 3.14.6. Use Linux or macOS; on Windows use WSL. For SAT
certificates, put CaDiCaL and drat-trim on `PATH` (see `README.md` in this folder).

## 2. Start

```bash
git checkout experiment/<ID>-<slug>
caffeinate -dimsu bash research/12-faced-polyhedron/experiments/<ID>-<slug>/run.sh 0
```

- **Keep it awake.** Use `caffeinate -dimsu`, AC power and an open lid; otherwise idle sleep stops the night (one
  night lost 8 h this way). If the Mac does sleep, only time is lost: budgets count awake time only
  (`time.monotonic()`), so the run continues on wake.
- **Interruptions.** If the computer turns off, run the same command again; finished tasks are skipped.
- **Where results go.** A run of `run_overnight.py` writes into the experiment's `results/` (`--results-dir`).
  Jobs that read another job's results (`gate`, `arch`, `n5`) find them in the newest experiment that recorded
  that job.

## 3. After the run

```bash
git add research/12-faced-polyhedron/experiments/<ID>-<slug>/results
git commit -m "<ID>: results"
git push
```

Then ask a session to conclude it (skill `experiment-conclude`).

## 4. Jobs of `run_overnight.py`

`README.md` in this folder: what each job decides, its options and how to read its records.

The past nights (2026-10-29 to 2026-11-01) are recorded as experiments:

| Experiment | Jobs |
|---|---|
| E-261029-12 | `immersion` |
| E-261029-13 | `sym` |
| E-261029-15 | `sym --sym-immersion` |
| E-261029-16 | `pdefect` |
| E-261030-05 | `glad` |
| E-261030-06 | `gate` |
| E-261030-10 | `arch` |
| E-261030-11 | `n5` |
