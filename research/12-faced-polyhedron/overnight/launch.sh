#!/usr/bin/env bash
# Laptop launcher for one experiment: N detached shards, each `bash <experiment>/run.sh <shard>` under
# caffeinate -dimsu (no sleep while it runs), log appended to <experiment>/results/<shard>/night.log.
#   bash overnight/launch.sh start  EXPERIMENT_DIR SHARDS   refuses if this experiment is already running
#   bash overnight/launch.sh status EXPERIMENT_DIR          per shard: state, records, minutes since the last output
#   bash overnight/launch.sh stop   EXPERIMENT_DIR          kills this experiment's processes (run.sh, python, solvers)
# Any other command prints this usage and does nothing. A restart (start after stop) resumes: runners skip the
# units already in results.jsonl. QUIET_MIN (default 60): a running shard silent for longer is flagged as hung.
set -euo pipefail
usage() { sed -n '2,8p' "$0" | sed 's/^# \{0,1\}//' >&2; exit 2; }
[ $# -ge 2 ] || usage
CMD=$1
[ -f "$2/run.sh" ] || { echo "no run.sh in '$2'" >&2; usage; }
EXP=$(cd "$2" && pwd)
NAME=$(basename "$EXP")
PIDS="$EXP/results/launch.pids"
QUIET_MIN=${QUIET_MIN:-60}

tree() { echo "$1"; local c; for c in $(pgrep -P "$1" || true); do tree "$c"; done; }
alive_pid() { [ -n "${1:-}" ] && kill -0 "$1" 2>/dev/null; }
shard_pid() { [ -f "$PIDS" ] && awk -v s="$1" '$1 == s {print $2}' "$PIDS" || true; }
running_count() {
  local n=0 s p
  [ -f "$PIDS" ] || { echo 0; return; }
  while read -r s p; do alive_pid "$p" && n=$((n + 1)); done < "$PIDS"
  echo "$n"
}

case "$CMD" in
start)
  N=${3:-}
  [[ "$N" =~ ^[1-9][0-9]*$ ]] || { echo "start needs the number of shards" >&2; usage; }
  if [ "$(running_count)" -gt 0 ]; then
    echo "$NAME is already running ($(running_count) shards); see: bash $0 status $2" >&2; exit 1
  fi
  mkdir -p "$EXP/results"; : > "$PIDS"
  for s in $(seq 0 $((N - 1))); do
    mkdir -p "$EXP/results/$s"
    echo "=== $(date '+%F %T') launch.sh start, shard $s" >> "$EXP/results/$s/night.log"
    nohup caffeinate -dimsu bash "$EXP/run.sh" "$s" >> "$EXP/results/$s/night.log" 2>&1 &
    echo "$s $!" >> "$PIDS"
  done
  echo "started $N shards of $NAME"
  echo "status: bash $0 status $2      stop: bash $0 stop $2"
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
    if alive_pid "$(shard_pid "$s")"; then
      state=running; run=$((run + 1))
      if [ "$quiet" -ge "$QUIET_MIN" ]; then state="RUNNING, SILENT ${quiet} MIN - PROBABLY HUNG"; hung=$((hung + 1)); fi
    else
      state="ended rc=$(grep '^exit_status' "$d/manifest.txt" 2>/dev/null | tail -1 | awk '{print $2}')"
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
  echo "$NAME: stopped; still alive: $(running_count)"
  ;;
*)
  usage
  ;;
esac
