#!/usr/bin/env bash
# Laptop launcher for one experiment: N detached shards, each `bash <experiment>/run.sh <shard>` under
# caffeinate -dimsu (no sleep while it runs), log appended to <experiment>/results/<shard>/night.log.
#   bash overnight/launch.sh start  EXPERIMENT_DIR CORES [NEXT_DIR ...]   CORES processes, one core each; refused if
#     already running, or if all running launches together would use more than MAX_CORES (default 10: more freezes
#     the laptop). run.sh gets SHARDS=CORES and splits its units into that many shards, so any CORES covers every
#     unit. NEXT_DIR ...: a queue on the same cores; shard s of the next experiment starts when shard s of the
#     previous one ends. To change the load: stop, then start with another CORES (recorded units are skipped)
#   bash overnight/launch.sh status EXPERIMENT_DIR          per shard: state, records, minutes since the last output
#   bash overnight/launch.sh stop   EXPERIMENT_DIR          kills this launch (run.sh, python, solvers; with a queue, the
#     whole queue); units in flight are lost and rerun from their start on the next start
# Any other command prints this usage and does nothing. A restart (start after stop) resumes: runners skip the
# units recorded in any shard's results.jsonl. QUIET_MIN (default 60): a running shard silent for longer is flagged as hung.
set -euo pipefail
usage() { sed -n '2,15p' "$0" | sed 's/^# \{0,1\}//' >&2; exit 2; }
[ $# -ge 2 ] || usage
CMD=$1
[ -f "$2/run.sh" ] || { echo "no run.sh in '$2'" >&2; usage; }
EXP=$(cd "$2" && pwd)
NAME=$(basename "$EXP")
PIDS="$EXP/results/launch.pids"
QUIET_MIN=${QUIET_MIN:-60}
MAX_CORES=${MAX_CORES:-10}

tree() { echo "$1"; local c; for c in $(pgrep -P "$1" || true); do tree "$c"; done; }
alive_pid() { [ -n "${1:-}" ] && kill -0 "$1" 2>/dev/null; }
shard_pid() { [ -f "$PIDS" ] && awk -v s="$1" '$1 == s {print $2}' "$PIDS" || true; }
all_running() {   # alive launch processes of every experiment (a queue is listed in each of its experiments)
  { cat "$(dirname "$0")"/../experiments/*/results/launch.pids 2>/dev/null || true; } | awk '{print $2}' | sort -u |
    while read -r p; do if alive_pid "$p"; then echo "$p"; fi; done | wc -l | tr -d ' '
}
running_count() {
  local n=0 s p
  [ -f "$PIDS" ] || { echo 0; return; }
  while read -r s p; do alive_pid "$p" && n=$((n + 1)); done < "$PIDS"
  echo "$n"
}

case "$CMD" in
start)
  N=${3:-}
  [[ "$N" =~ ^[1-9][0-9]*$ ]] || { echo "start needs the number of cores" >&2; usage; }
  QUEUE=("$EXP")
  for d in "${@:4}"; do
    [ -f "$d/run.sh" ] || { echo "no run.sh in '$d'" >&2; usage; }
    QUEUE+=("$(cd "$d" && pwd)")
  done
  for e in "${QUEUE[@]}"; do
    grep -q 'SHARDS' "$e/run.sh" || { echo "$(basename "$e")/run.sh has a fixed shard count (it does not read SHARDS): make it read SHARDS first" >&2; exit 1; }
    PIDS="$e/results/launch.pids"
    if [ "$(running_count)" -gt 0 ]; then
      echo "$(basename "$e") is already running ($(running_count) shards); see: bash $0 status $e" >&2; exit 1
    fi
  done
  busy=$(all_running)
  if [ $((busy + N)) -gt "$MAX_CORES" ]; then
    echo "refused: $busy processes already run and $N more exceed MAX_CORES=$MAX_CORES; stop one, start fewer, or queue: start DIR CORES NEXT_DIR" >&2; exit 1
  fi
  for e in "${QUEUE[@]}"; do mkdir -p "$e/results"; : > "$e/results/launch.pids"; done
  for s in $(seq 0 $((N - 1))); do
    chain=""
    for e in "${QUEUE[@]}"; do
      mkdir -p "$e/results/$s"
      chain="$chain echo \"=== \$(date '+%F %T') launch.sh start, shard $s\" >> '$e/results/$s/night.log'; bash '$e/run.sh' $s >> '$e/results/$s/night.log' 2>&1;"
    done
    SHARDS=$N nohup caffeinate -dimsu bash -c "$chain" > /dev/null 2>&1 &
    for e in "${QUEUE[@]}"; do echo "$s $!" >> "$e/results/launch.pids"; done
  done
  echo "started $N shards (SHARDS=$N): $(for e in "${QUEUE[@]}"; do printf '%s ' "$(basename "$e")"; done)"
  echo "status: bash $0 status DIR      stop: bash $0 stop DIR (stops the whole queue)"
  ;;
status)
  now=$(date +%s); total=0; hung=0; run=0
  for d in "$EXP"/results/[0-9]*; do
    [ -d "$d" ] || continue
    s=$(basename "$d")
    n=$( (cat "$d/results.jsonl" 2>/dev/null || true) | wc -l | tr -d ' ')
    total=$((total + n))
    last=0
    for f in "$d/night.log" "$d/results.jsonl" "$d/progress.jsonl"; do
      [ -f "$f" ] && t=$(stat -f %m "$f") && [ "$t" -gt "$last" ] && last=$t
    done
    quiet=$(( (now - last) / 60 ))
    if alive_pid "$(shard_pid "$s")" && [ "$PIDS" -nt "$d/night.log" ]; then
      state=queued; run=$((run + 1))   # in a queue, waiting for the previous experiment's shard
    elif alive_pid "$(shard_pid "$s")"; then
      state=running; run=$((run + 1))
      if [ "$quiet" -ge "$QUIET_MIN" ]; then state="RUNNING, SILENT ${quiet} MIN - PROBABLY HUNG"; hung=$((hung + 1)); fi
    else
      state="ended rc=$( (grep '^exit_status' "$d/manifest.txt" 2>/dev/null || true) | tail -1 | awk '{print $2}')"
    fi
    printf 'shard %-2s %-10s %3s records, last output %3s min ago | %s\n' "$s" "$state" "$n" "$quiet" \
      "$(grep -v '^===' "$d/night.log" 2>/dev/null | tail -1 | cut -c1-90)"
  done
  echo "$NAME: $run shards running, $total records, $hung probably hung (silent >= $QUIET_MIN min)"
  ;;
stop)
  if [ ! -f "$PIDS" ] || [ "$(running_count)" -eq 0 ]; then echo "$NAME: nothing running"; exit 0; fi
  all=""
  while read -r s p; do alive_pid "$p" && all="$all $(tree "$p" | tr '\n' ' ')"; done < "$PIDS"
  # shellcheck disable=SC2086
  kill $all 2>/dev/null || true
  sleep 2
  echo "$NAME: stopped; still alive: $(running_count); units in flight are lost and rerun from their start"
  ;;
*)
  usage
  ;;
esac
