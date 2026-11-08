#!/usr/bin/env bash
# Laptop launcher: detached shards, each `bash <experiment>/run.sh <shard>` under caffeinate -dimsu (no sleep while it
# runs), log appended to <experiment>/results/<shard>/night.log.
#   bash overnight/launch.sh CODE [CODE ...] start [CORES]   CORES processes (default 10), one core each. Several codes
#       form a queue on the same cores: shard s of the next experiment starts when shard s of the previous one ends.
#       Refused if one of them is running, or if all launches together would use more than MAX_CORES (default 10).
#       run.sh gets SHARDS=CORES and splits its units into that many shards, so any CORES covers every unit.
#   bash overnight/launch.sh CODE [CODE ...] status   per shard: state, records, minutes since the last output; then the
#       experiment's own progress (done / left / time left) if experiments/<ID>/progress.sh exists
#   bash overnight/launch.sh CODE [CODE ...] stop     each shard stops after its current unit (nothing is recomputed)
#   bash overnight/launch.sh CODE [CODE ...] kill     stops now; units in flight rerun from their start on the next start
# CODE: the end of an experiment id (02-03, 261102-03, E-261102-03; it must match one folder) or a folder path.
# stop and kill act on the whole queue a shard belongs to. A restart (start after stop or kill) resumes: runners skip
# the units recorded in any shard's results.jsonl. QUIET_MIN (default 60): a running shard silent for longer is
# flagged as hung. Any other command prints this usage and does nothing.
set -euo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
EXPS="$HERE/../experiments"
QUIET_MIN=${QUIET_MIN:-60}
MAX_CORES=${MAX_CORES:-10}
STOP_POLL=${STOP_POLL:-10}
usage() { awk 'NR > 1 && /^#/ {sub(/^# ?/, ""); print; next} NR > 1 {exit}' "$0" >&2; exit 2; }

tree() { echo "$1"; local c; for c in $(pgrep -P "$1" || true); do tree "$c"; done; }
alive_pid() { [ -n "${1:-}" ] && kill -0 "$1" 2>/dev/null; }
pids_of() { echo "$1/results/launch.pids"; }
shard_pid() { [ -f "$(pids_of "$1")" ] && awk -v s="$2" '$1 == s {print $2}' "$(pids_of "$1")" || true; }
running_count() {
  local n=0 s p
  [ -f "$(pids_of "$1")" ] || { echo 0; return; }
  while read -r s p; do if alive_pid "$p"; then n=$((n + 1)); fi; done < "$(pids_of "$1")"
  echo "$n"
}
all_running() {   # alive launch processes of every experiment (a queue is listed in each of its experiments)
  { cat "$EXPS"/*/results/launch.pids 2>/dev/null || true; } | awk '{print $2}' | sort -u |
    while read -r p; do if alive_pid "$p"; then echo "$p"; fi; done | wc -l | tr -d ' '
}
lines() { local n=0 f; for f in "$@"; do [ -f "$f" ] && n=$((n + $(wc -l < "$f"))); done; echo "$n"; }

# internal: wait until the shard process P writes a new record to one of FILES, then kill its tree
if [ "${1:-}" = __watch ]; then
  P=$2; shift 2
  base=$(lines "$@")
  while alive_pid "$P"; do
    if [ "$(lines "$@")" -gt "$base" ]; then kill $(tree "$P" | tr '\n' ' ') 2>/dev/null || true; break; fi
    sleep "$STOP_POLL"
  done
  exit 0
fi

resolve() {
  if [ -f "$1/run.sh" ]; then (cd "$1" && pwd); return; fi
  local m=() d
  for d in "$EXPS"/E-*/; do
    d=${d%/}
    [[ "$(basename "$d" | cut -d- -f1-3)" == *"$1" ]] && m+=("$d")
  done
  if [ ${#m[@]} -ne 1 ]; then
    echo "code '$1' matches ${#m[@]} experiments: $(for d in "${m[@]+"${m[@]}"}"; do printf '%s ' "$(basename "$d")"; done)" >&2
    exit 2
  fi
  [ -f "${m[0]}/run.sh" ] || { echo "no run.sh in $(basename "${m[0]}")" >&2; exit 2; }
  (cd "${m[0]}" && pwd)
}

ARGS=("$@"); n=$#
[ "$n" -ge 2 ] || usage
N=10
if [[ "${ARGS[n-1]}" =~ ^[0-9]+$ ]]; then N=${ARGS[n-1]}; n=$((n - 1)); fi
[[ "$N" =~ ^[1-9][0-9]*$ ]] || usage
[ "$n" -ge 2 ] || usage
CMD=${ARGS[n-1]}
case "$CMD" in start|status|stop|kill) ;; *) usage ;; esac
QUEUE=()
for c in "${ARGS[@]:0:n-1}"; do d=$(resolve "$c") || exit 2; QUEUE+=("$d"); done

case "$CMD" in
start)
  for e in "${QUEUE[@]}"; do
    grep -q 'SHARDS' "$e/run.sh" || { echo "$(basename "$e")/run.sh has a fixed shard count (it does not read SHARDS): make it read SHARDS first" >&2; exit 1; }
    if [ "$(running_count "$e")" -gt 0 ]; then
      echo "$(basename "$e") is already running ($(running_count "$e") shards); see its status" >&2; exit 1
    fi
  done
  busy=$(all_running)
  if [ $((busy + N)) -gt "$MAX_CORES" ]; then
    echo "refused: $busy processes already run and $N more exceed MAX_CORES=$MAX_CORES; stop one, start fewer, or put the experiments in one queue" >&2
    exit 1
  fi
  for e in "${QUEUE[@]}"; do mkdir -p "$e/results"; : > "$(pids_of "$e")"; rm -f "$e/results/stop.requested"; done
  for s in $(seq 0 $((N - 1))); do
    chain=""
    for e in "${QUEUE[@]}"; do
      mkdir -p "$e/results/$s"
      chain="$chain echo \"=== \$(date '+%F %T') launch.sh start, shard $s\" >> '$e/results/$s/night.log'; bash '$e/run.sh' $s >> '$e/results/$s/night.log' 2>&1;"
    done
    SHARDS=$N nohup caffeinate -dimsu bash -c "$chain" > /dev/null 2>&1 &
    for e in "${QUEUE[@]}"; do echo "$s $!" >> "$(pids_of "$e")"; done
  done
  echo "started $N shards (SHARDS=$N): $(for e in "${QUEUE[@]}"; do printf '%s ' "$(basename "$e")"; done)"
  ;;
status)
  for e in "${QUEUE[@]}"; do
    now=$(date +%s); total=0; hung=0; run=0
    for d in "$e"/results/[0-9]*; do
      [ -d "$d" ] || continue
      s=$(basename "$d")
      n=$( (cat "$d/results.jsonl" 2>/dev/null || true) | wc -l | tr -d ' ')
      total=$((total + n))
      last=0
      for f in "$d/night.log" "$d/results.jsonl" "$d/progress.jsonl"; do
        [ -f "$f" ] && t=$(stat -f %m "$f") && [ "$t" -gt "$last" ] && last=$t
      done
      quiet=$(( last > 0 ? (now - last) / 60 : 0 ))
      if alive_pid "$(shard_pid "$e" "$s")" && [ "$(pids_of "$e")" -nt "$d/night.log" ]; then
        state=queued; run=$((run + 1))   # waiting for the previous experiment's shard
      elif alive_pid "$(shard_pid "$e" "$s")"; then
        state=running; run=$((run + 1))
        [ -f "$e/results/stop.requested" ] && state="running, stops after this unit"
        if [ "$quiet" -ge "$QUIET_MIN" ]; then state="RUNNING, SILENT ${quiet} MIN - PROBABLY HUNG"; hung=$((hung + 1)); fi
      else
        state="ended rc=$( (grep '^exit_status' "$d/manifest.txt" 2>/dev/null || true) | tail -1 | awk '{print $2}')"
      fi
      printf 'shard %-2s %-10s %3s records, last output %3s min ago | %s\n' "$s" "$state" "$n" "$quiet" \
        "$(grep -v '^===' "$d/night.log" 2>/dev/null | tail -1 | cut -c1-90)"
    done
    echo "$(basename "$e"): $run shards running, $total records, $hung probably hung (silent >= $QUIET_MIN min)"
    # Optional experiment-specific progress (units done / left, time left): experiments/<ID>/progress.sh prints it.
    [ -f "$e/progress.sh" ] && { echo "--- progress"; bash "$e/progress.sh" || true; }
  done
  ;;
stop)
  for e in "${QUEUE[@]}"; do
    if [ "$(running_count "$e")" -eq 0 ]; then echo "$(basename "$e"): nothing running"; continue; fi
    touch "$e/results/stop.requested"
    while read -r s p; do
      alive_pid "$p" || continue
      files=()
      for f in "$EXPS"/*/results/launch.pids; do   # every experiment of this shard's queue
        if awk -v p="$p" '$2 == p {found = 1} END {exit !found}' "$f"; then
          files+=("$(dirname "$f")/$s/results.jsonl"); touch "$(dirname "$f")/stop.requested"
        fi
      done
      nohup bash "$0" __watch "$p" "${files[@]}" > /dev/null 2>&1 &
    done < "$(pids_of "$e")"
    echo "$(basename "$e"): $(running_count "$e") shards stop after their current unit (status: 'stops after this unit'); kill stops now"
  done
  ;;
kill)
  for e in "${QUEUE[@]}"; do
    if [ ! -f "$(pids_of "$e")" ] || [ "$(running_count "$e")" -eq 0 ]; then echo "$(basename "$e"): nothing running"; continue; fi
    all=""
    while read -r s p; do if alive_pid "$p"; then all="$all $(tree "$p" | tr '\n' ' ')"; fi; done < "$(pids_of "$e")"
    # shellcheck disable=SC2086
    kill $all 2>/dev/null || true
    sleep 2
    echo "$(basename "$e"): killed; still alive: $(running_count "$e"); units in flight rerun from their start on the next start"
  done
  ;;
esac
