---
name: experiment-conclude
description: Use when a run of a 12-face research experiment has finished (laptop night, GitHub Actions shards, or an interactive run), or when night results arrive and must be analysed, verified and recorded in the ledger; also for any edit of STATUS.md, ROADMAP.md or SPEC.md.
---

# Conclude an experiment and update the ledger

Paths and commands are relative to `research/12-faced-polyhedron/`. Rules: `PROTOCOL.md` §2.6-§2.8 and §3.
Use `python3` from an activated environment with `requirements.txt` installed.

1. **Collect.**
   - Actions: `gh run download <run-id>`.
   - Laptop: the run's `results/` folder. Raw unit output (`attempt_*/` logs, specs, maps) is read here but not
     committed (`PROTOCOL.md` §5); after the conclusion commit run `python3 overnight/move_raw.py`.

   Sum the core-hours from every `manifest.txt`. If a manifest is missing, say so; do not estimate.
2. **Controls first.** If the positive control failed, or never had the chance to succeed under the same budget,
   the verdict is "underpowered", not LOW-YIELD. If a verdict rests on a diagnostic that was constant across the
   runs (pinned, exactly 0, always even), check the measuring function on controls that must give the other sign
   before interpreting it (`reviews/strategy-review-2026-11-01.md` 5.1). A negative statement names its scope
   (`SPEC.md` section 4) and what was not run.
3. **Verify.** Run every candidate through the `candidate-check` skill. Every UNSAT used as evidence keeps its
   formula's SHA-256 and its proof's SHA-256 with the checker transcript (files deleted, `PROTOCOL.md` §5).
   - Routine conclusions reuse a saved successful proof check when CNF, proof and checker provenance
     are bound by recorded hashes and the success transcript is intact. Validate hashes and transcripts;
     do not replay DRAT merely because a new session starts or drat-trim is installed. Replay once for
     missing evidence/provenance, changed formula/proof/checker, suspected corruption, or an explicit
     audit request. A hash mismatch must be investigated, never silently accepted. Report cached
     acceptance separately from fresh replay. E-261103-03 evidence tests use `REPLAY_DRAT=1` for
     explicit audit replay; initial checking of new UNSAT certificates remains mandatory.
4. **Conclude.** Fill in `CONCLUSION.md` from the template:
   - for a laptop night, a "Runs" bullet: wall time vs budget, any sleep gaps, per job the tasks, outcomes and
     exact checks. It replaces the night report (owner, 2026-11-10; `PROTOCOL.md` §8b); write nothing in `reports/`;
   - prediction vs outcome;
   - claims with `SPEC.md` §5 labels and their scope (instance / family / theorem), and what must not be
     claimed;
   - how the outcome moves each hypothesis in `tests` (update the hypothesis file's status and evidence);
   - for a claim that changes an FD or witness row: a `REVIEW.md` by someone other than the author;
   - the verdict with its budget (e.g. "LOW-YIELD@8 core-h, 2 seeds"; REFUTED only with a proof);
   - the next step.
5. **Ledger, in the same commit** (one commit for the whole conclusion, the handover block included; `PROTOCOL.md`
   §8b):
   - **`STATUS.md`:** update the row(s) and the "As of" date.
   - **`ROADMAP.md`:** set the State to `done` or `killed`. A follow-up row needs scores, T + D >= 3, a budget, a
     stop rule and its DR/FD link.
   - **`experiment-log.md`:** a 1-3 line dated entry pointing to `CONCLUSION.md`.

   - **Experiment `README.md`:** `status: done` (or `killed`), `concluded: YYYY-MM-DD`, `verdict`, `produces` (FD / W: / C: it established),
     and a short results / conclusions summary.
   - **New ideas or hypotheses** that came out of it: one file each, with this experiment in their `origin`.
   - Run `verification/trace.py` so the map is up to date.

   Do not restate numbers anywhere else. `results.md` is frozen. Change `SPEC.md` only through its change log.
6. **Close.** Reuse applicable successful checks from the run/session; conclusion and ledger wording edits
   alone do not trigger tests. For relevant code/evidence changes, run only affected checks not already
   covered; run `python3 verification/verify_all.py --quick` once if an integration concern remains. State
   the reason before repeating any check; reuse the result at handover. Follow `PROTOCOL.md` section 8.
   Run the full suite only when explicitly requested. Propose a PR into `main`, and open it only when the
   owner says so. Report in Russian: outcomes, verification scope, STATUS changes and next ROADMAP item.

Labels: an AI-written proof is at most PROVED-1. CERTIFIED needs a checked certificate, a written soundness
argument and recorded hashes.
