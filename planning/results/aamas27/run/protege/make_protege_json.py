"""
Writes protege.json (the format of protege_template.json) from the measure.sh sessions: loading and reasoning times
of protege.log, the peak RSS of GNU time and the heap increase of the GC log (protege_heap_from_gc.py), and the query
times that Snap SPARQL logs ("Evaluated BGP in N ms", one run per query; the time excludes showing the results).
Q9 is rejected by Snap SPARQL's parser and Q20 was stopped after it had not finished for more than 60 s.
Usage: python3 make_protege_json.py <results folder> > protege.json
"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
results = Path(sys.argv[1])
QUERY_ORDER = {"queries": [2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 19, 20], "queries_21_22": [21, 22]}
COUNTS = {2: 7421, 3: 55, 4: 2486, 5: 20, 7: 1684, 8: 6, 10: 666, 11: 2422, 12: 2494, 13: 0, 14: 0, 15: 21, 16: 21,
          19: 858, 21: 145, 22: 106}
"""The numbers of results that Snap SPARQL showed, as noted by hand."""
SKIPPED = {9: "error", 20: "timeout"}

heap = json.loads(subprocess.run([sys.executable, HERE / "protege_heap_from_gc.py", results / "raw",
                                  results / "reasoned"], capture_output=True, text=True, check=True).stdout)
queries = {}
for session, numbers in QUERY_ORDER.items():
    log = (results / session / "protege.log").read_text()
    times = [int(t) for t in re.findall(r"Evaluated BGP in (\d+) ms", log)]
    started = log.count("Evaluating BGP:")
    evaluated = [n for n in numbers if n not in SKIPPED]
    assert len(times) == len(evaluated), (session, times, evaluated)
    assert started == len(numbers), (session, started, numbers)
    for number, milliseconds in zip(evaluated, times):
        queries[str(number)] = {"mean_ms": float(milliseconds), "std_ms": 0.0, "results": COUNTS[number]}
for number, status in SKIPPED.items():
    queries[str(number)] = {"mean_ms": None, "status": status}
print(json.dumps({
    "protege_version": "5.6.7",
    "pellet_plugin_version": "2.2.0 (com.clarkparsia.protege.plugin.pellet), Snap SPARQL Query 6.0.0",
    "java_options": "-Xmx28G (bundled OpenJDK 11.0.25), -Xlog:gc",
    "loading": {name: {"seconds": entry["seconds"], "peak_rss_mib": entry["peak_rss_mib"],
                       "heap_increase_mib": entry["heap_increase_mib"], "loading_ms": entry["loading_ms"],
                       "reasoning_ms": entry["reasoning_ms"], "status": "ok"} for name, entry in heap.items()},
    "queries": dict(sorted(queries.items(), key=lambda item: int(item[0]))),
}, indent=2))
