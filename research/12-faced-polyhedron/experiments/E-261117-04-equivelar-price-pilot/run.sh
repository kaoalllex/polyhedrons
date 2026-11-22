#!/usr/bin/env bash
# E-261117-04 stage A (PLAN.md): one shard of a p6.py queue through the E-261119-02 shard runner run_b.sh (the
# E-261103-03 runner in its imported-map mode: kissat, no proof, lean UNSATs, every SAT model through the bridge and
# verify_candidate.py --all-pairs; the runner's convex controls and the pinned Roest-Vigh pair in every shard).
# Usage: [Q=stageA|stageA_retry|stageA_models] bash run.sh SHARD   -> results/<Q>/<SHARD>/
# BUDGET is the runner's reservation ceiling in core-s over the 10 shards (a shard dispatches a unit only while its
# allowance keeps solver + checker caps + 420 s; 2400 s per shard leaves ~25 min of dispatch); the
# PLAN's 1 core-h for stage A is the session's stop rule (results/<Q>/stop.requested) on the budget ledgers.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
Q="${Q:-stageA}"
case "$Q" in
  stageA|stageA_models) B=24000 ;;
  stageA_retry) B=30000 ;;
  *) echo "unknown queue $Q" >&2; exit 2 ;;
esac
[[ -f "$HERE/queue_$Q.json" ]] || { echo "queue_$Q.json missing: python3 p6.py build (or followup) first" >&2; exit 2; }
mkdir -p "$HERE/results/$Q"
BUDGET="${BUDGET:-$B}" QUEUE="$HERE/queue_$Q.json" RESULTS="$HERE/results/$Q" \
  bash "$HERE/../E-261119-02-symmetric-nine-face-census/run_b.sh" "${1:?numeric shard}"
