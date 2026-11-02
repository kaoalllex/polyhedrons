#!/usr/bin/env bash
# Night 6 (2026-11-01): the two pre-registered experiments, 10 single-core processes for the 10 performance cores
# of the owner's Apple M4 Pro (14 cores, 48 GB). Each process is wrapped in caffeinate -dimsu (no sleep while it
# runs). Logs: experiments/<ID>/results/<shard>/night.log. Stop everything: bash overnight/run_night6.sh stop
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
E23="$ROOT/experiments/E-261101-23-k-face-subinstances-face-cegar"
E25="$ROOT/experiments/E-261101-25-chirotope-first"
if [ "${1:-}" = "stop" ]; then
  pkill -f "E-261101-2[35].*run.sh" || true; pkill -f "kface_sweep.py" || true; pkill -f "chirotope_first.py run" || true
  pkill -f "^cadical" || true; echo "stopped"; exit 0
fi
if [ "${1:-}" = "status" ]; then
  for d in "$E23"/results/[0-9]* "$E25"/results/[0-9]*; do
    [ -d "$d" ] || continue
    n=$( (cat "$d/results.jsonl" 2>/dev/null || true) | wc -l | tr -d ' ')
    p=$( (cat "$d/progress.jsonl" 2>/dev/null || true) | wc -l | tr -d ' ')
    echo "$(basename "$(dirname "$(dirname "$d")")") shard $(basename "$d"): $n records, $p progress lines, last: $(tail -1 "$d/night.log" 2>/dev/null | cut -c1-110)"
  done
  echo "processes: $(pgrep -f 'kface_sweep.py|chirotope_first.py run' | wc -l | tr -d ' ')"; exit 0
fi
for s in 0 1 2 3 4 5; do
  mkdir -p "$E23/results/$s"
  nohup caffeinate -dimsu bash "$E23/run.sh" "$s" >> "$E23/results/$s/night.log" 2>&1 &
done
for s in 0 1 2 3; do
  mkdir -p "$E25/results/$s"
  nohup caffeinate -dimsu bash "$E25/run.sh" "$s" >> "$E25/results/$s/night.log" 2>&1 &
done
sleep 2
echo "started: $(pgrep -f 'kface_sweep.py|chirotope_first.py run' | wc -l | tr -d ' ') worker processes (expect 10 after a few seconds)"
echo "status:  bash overnight/run_night6.sh status      stop: bash overnight/run_night6.sh stop"
