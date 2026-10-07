#!/usr/bin/env bash
# Starts a fresh Protégé 5.6.7 for one measurement and records its peak memory (GNU time) and its memory over time
# (sample_rss.py), with Protégé's own log of this session. Usage: measure.sh raw|reasoned|queries
set -euo pipefail
NAME="${1:?raw, reasoned or queries}"
HERE="$(cd "$(dirname "$0")" && pwd)"
OUT="$HERE/results/$NAME"
rm -rf "$OUT"; mkdir -p "$OUT"
: > "$HOME/.Protege/logs/protege.log" 2>/dev/null || true
printf "max_heap_size=28G\nappend=-Xlog:gc:file=%s:time,uptime\n" "$OUT/gc.log" > "$HOME/.Protege/conf/jvm.conf"
cp "$HOME/.Protege/conf/jvm.conf" "$OUT/jvm.conf"
cd "$HERE/Protege-5.6.7"
/usr/bin/time -v -o "$OUT/time.txt" ./run.sh > "$OUT/stdout.log" 2>&1 &
TIME_PID=$!
python3 "$HERE/sample_rss.py" "$TIME_PID" "$OUT/rss.txt" &
echo "Protégé started for '$NAME'; results in $OUT"
wait "$TIME_PID" || true
wait
cp "$HOME/.Protege/logs/protege.log" "$OUT/protege.log"
echo "Protégé closed; peak: $(grep 'Maximum resident' "$OUT/time.txt")"
