---
name: experiment-conclude
description: Use when a run of a 12-face research experiment has finished (laptop night, GitHub Actions shards, or an interactive run), or when night results arrive and must be analysed, verified and recorded in the ledger; also for night reports and for any edit of STATUS.md, ROADMAP.md or SPEC.md.
---

# Conclude an experiment and update the ledger

Paths are relative to `research/12-faced-polyhedron/`. Rules: `PROTOCOL.md` §2.6-§2.8 and §3.

1. **Collect.**
   - Actions: `gh run download <run-id>`.
   - Laptop: the run's `results/` folder.

   Sum the core-hours from every `manifest.txt`. If a manifest is missing, say so; do not estimate.
2. **Controls first.** If the positive control failed, or never had the chance to succeed under the same budget,
   the verdict is "underpowered", not LOW-YIELD. If a verdict rests on a diagnostic that was constant across the
   runs (pinned, exactly 0, always even), check the measuring function on controls that must give the other sign
   before interpreting it (`reviews/strategy-review-2026-11-01.md` 5.1). A negative statement names its scope
   (`SPEC.md` section 4) and what was not run.
3. **Verify.** Run every candidate through the `candidate-check` skill. Every UNSAT used as evidence keeps its
   formula (CNF / SMT2 file or its SHA-256) and, for SAT, its proof.
4. **Conclude.** Fill in `CONCLUSION.md` from the template:
   - prediction vs outcome;
   - claims with `SPEC.md` §5 labels and their scope (instance / family / theorem), and what must not be
     claimed;
   - how the outcome moves each hypothesis in `tests` (update the hypothesis file's status and evidence);
   - for a claim that changes an FD or witness row: a `REVIEW.md` by someone other than the author;
   - the verdict with its budget (e.g. "LOW-YIELD@8 core-h, 2 seeds"; REFUTED only with a proof);
   - the next step.
5. **Ledger, in the same commit:**
   - **`STATUS.md`:** update the row(s) and the "As of" date.
   - **`ROADMAP.md`:** set the State to `done` or `killed`. A follow-up row needs scores, T + D >= 3, a budget, a
     stop rule and its DR/FD link.
   - **`experiment-log.md`:** a 1-3 line dated entry pointing to `CONCLUSION.md`.

   - **Experiment `README.md`:** `status: done` (or `killed`), `concluded: YYYY-MM-DD`, `verdict`, `produces` (FD / W: / C: it established),
     and a short results / conclusions summary.
   - **New ideas or hypotheses** that came out of it: one file each, with this experiment in their `origin`.
   - Run `verification/trace.py` so the map is up to date.

   Do not restate numbers anywhere else. `results.md` is frozen. Change `SPEC.md` only through its change log.
6. **Night report.** For a laptop night, also write a short `reports/NIGHT_REPORT_YYYY-MM-DD.md` covering:
   - wall time vs budget, and any sleep gaps;
   - per job: tasks, outcomes, exact checks;
   - the verdict.
7. **Close.** Run `verification/verify_all.py`. Propose a PR into `main`, and open it only when the owner says
   so. Report to the owner in Russian: the outcome, what changed in STATUS, the next ROADMAP item.

Labels: an AI-written proof is at most PROVED-1. CERTIFIED needs a checked certificate, a written soundness
argument and recorded hashes.
