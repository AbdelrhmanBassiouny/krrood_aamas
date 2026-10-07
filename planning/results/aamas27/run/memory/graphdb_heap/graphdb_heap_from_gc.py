"""
GraphDB's Java heap in use during each load, from the G1 GC logs written by driver.sh: the heap after the forced full
GC before the load ("before"), the largest heap after any GC pause during the load ("peak"; no old-generation cycle
ran during the loads, so it may include old garbage and is an upper bound), and their difference ("increase").
Usage: python3 graphdb_heap_from_gc.py > graphdb_heap.json   (in this folder)
"""
import json, re
from pathlib import Path

PAUSE = re.compile(r"\[(\d+\.\d+)s\].*GC\(\d+\) (Pause .*?) (\d+)M->(\d+)M\((\d+)M\)")
result = {}
for input_name in ("raw", "reasoned"):
    events = [(float(m[1]), m[2], int(m[3]), int(m[4]))
              for m in map(PAUSE.search, Path(f"gc_{input_name}.log").read_text().splitlines()) if m]
    forced = [e for e in events if "Diagnostic Command" in e[1]]
    during = [e for e in events if forced[0][0] < e[0] < forced[-1][0]]
    before, peak = forced[0][3], max(e[3] for e in during)
    result[input_name] = {"heap_before_mib": before, "heap_peak_mib": peak, "heap_increase_mib": peak - before,
                          "heap_after_load_mib": forced[-1][3], "pauses_during_load": len(during),
                          "old_generation_cycles_during_load": sum("Remark" in e[1] or "Mixed" in e[1] for e in during)}
print(json.dumps(result, indent=2))
