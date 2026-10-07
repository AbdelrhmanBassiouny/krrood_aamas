#!/usr/bin/env bash
# Measures GraphDB's Java heap in use during loading (GC log), with the same server start as reproduce.sh.
set -euo pipefail
export PATH=/opt/venvs/earlier/bin:$PATH
cd /opt/aamas27/code/earlier/experiments
for input in raw reasoned; do
    home=/w/graphdb-home-$input
    rm -rf "$home" && cp -a /state-ro/graphdb-home "$home"
    GDB_HEAP_SIZE=8g GDB_JAVA_OPTS="-Xlog:gc:file=/w/gc_$input.log:uptime,level,tags" \
        /opt/graphdb/dist/bin/graphdb -d -p /w/graphdb_$input.pid \
        -Dgraphdb.home="$home" -Dgraphdb.license.file=/license/graphdb.license \
        -Dgraphdb.connector.port=7200 > /w/graphdb_$input.log 2>&1
    for _ in $(seq 150); do
        python -c "import urllib.request; urllib.request.urlopen('http://localhost:7200/rest/info/version', timeout=5)" 2>/dev/null && break
        sleep 2
    done
    pid=$(cat /w/graphdb_$input.pid)
    sleep 20
    jcmd "$pid" GC.run > /dev/null
    echo "$(date -u +%T) start loading $input" | tee -a /w/driver.log
    python scripts/aamas27/run_loading.py --systems graphdb --inputs "$input" --repetitions 1 \
        --results-dir /w/results_$input 2>&1 | grep -v 'it/s' | tee -a /w/driver.log
    jcmd "$pid" GC.run > /dev/null
    echo "$(date -u +%T) finished $input" | tee -a /w/driver.log
    kill "$pid"; sleep 15
    rm -rf "$home"
done
echo "DRIVER DONE" | tee -a /w/driver.log
