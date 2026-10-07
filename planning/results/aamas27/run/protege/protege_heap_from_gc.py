"""
Protégé's Java heap in use while it loads a file and Pellet reasons over it, from the G1 GC log of a measure.sh
session and the times in protege.log: the heap after the last GC pause before "Loading ontology from" ("before"), the
largest heap after any GC pause until "Ontologies processed" ("peak"; an upper bound, as it may include old garbage),
and their difference ("increase"), as for GraphDB. Also the loading and reasoning times of protege.log and the peak
RSS of GNU time.
Usage: python3 protege_heap_from_gc.py results/raw results/reasoned > protege_measurements.json
"""
import json
import re
import sys
from datetime import datetime
from pathlib import Path

PAUSE = re.compile(r"^\[([^\]]+)\]\[[\d.]+s\].*GC\(\d+\) (Pause .*?) (\d+)M->(\d+)M\((\d+)M\)")
LOG_TIME = "%Y-%m-%d %H:%M:%S.%f"


def log_line(log: str, text: str) -> tuple:
    line = next(line for line in log.splitlines() if text in line)
    return datetime.strptime(line[:23], LOG_TIME).astimezone(), line


result = {}
for folder in map(Path, sys.argv[1:]):
    log = (folder / "protege.log").read_text()
    load_start, _ = log_line(log, "Loading ontology from")
    _, loaded = log_line(log, "Loading for ontology and imports closure successfully completed in")
    reasoned_at, reasoned = log_line(log, "Ontologies processed in")
    events = [(datetime.fromisoformat(m[1].replace("+0200", "+02:00")), m[2], int(m[4]))
              for m in map(PAUSE.search, (folder / "gc.log").read_text().splitlines()) if m]
    before = [e for e in events if e[0] < load_start][-1][2]
    peak = max(e[2] for e in events if load_start <= e[0] <= reasoned_at)
    rss = int(re.search(r"Maximum resident set size \(kbytes\): (\d+)", (folder / "time.txt").read_text())[1])
    loading_ms = int(re.search(r"completed in (\d+) ms", loaded)[1])
    reasoning_ms = int(re.search(r"processed in (\d+) ms", reasoned)[1])
    result[folder.name] = {"loading_ms": loading_ms, "reasoning_ms": reasoning_ms,
                           "seconds": round((loading_ms + reasoning_ms) / 1000, 2),
                           "heap_before_mib": before, "heap_peak_mib": peak, "heap_increase_mib": peak - before,
                           "peak_rss_mib": round(rss / 1024)}
print(json.dumps(result, indent=2))
