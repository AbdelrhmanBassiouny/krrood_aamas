"""
Adds the in-memory baselines (Nemo and reasonable) to the loading table, from their separate run (provenance.txt of
that run: same machine and Docker set-up as the main run, measured after it, with KRROOD measured again alongside).
Their memory is the increase as for the other worker-based systems: peak RSS of the process tree minus that of a
fresh worker after its imports. A run stopped at the memory limit is "out of memory". Run after
loading_memory_increase.py and before bold_lowest_memory.py.

Usage: python3 planning/baseline_rows.py planning/results/aamas27/baselines krrood_aamas_2027/tables/loading_table.tex
"""
import json
import statistics
import sys
from pathlib import Path

ROWS = [("nemo_owlrl", "Nemo"), ("reasonable_owlrl", "reasonable")]
AFTER = "GraphDB"
"""The new rows follow the like-for-like baselines."""


def format_memory(mib: float) -> str:
    return f"{mib / 1024:.2f}\\,GB" if mib >= 1024 else f"{mib:.0f}\\,MB"


def format_time(values: list) -> str:
    mean = statistics.mean(values)
    text = f"{mean:.3g}" if mean < 100 else f"{mean:.0f}"
    if len(values) > 1:
        deviation = statistics.stdev(values)
        text += f" \\pm {deviation:.2f}" if deviation < 1 else f" \\pm {deviation:.1f}"
    return f"${text}$"


def cells(runs: list, import_mib: float, limit_gib: float) -> tuple:
    finished = [run for run in runs if run["status"] == "ok"]
    if finished:
        time = format_time([run["worker_result"]["load_and_reasoning_seconds"] for run in finished])
        return time, format_memory(max(run["peak_rss_mib"] for run in finished) - import_mib)
    if runs and runs[0]["status"] == "memory_limit":
        return "out of memory", f"$>${limit_gib:.0f}\\,GB"
    return "failed", "n/a"


run_dir, path = Path(sys.argv[1]), Path(sys.argv[2])
loading = json.loads((run_dir / "loading/loading.json").read_text())
imports = json.loads((run_dir / "memory/import_memory.json").read_text())
limit = loading["arguments"].get("memory_limit_gib") or 24
lines = path.read_text().split("\n")
labels = {label for _, label in ROWS}
lines = [line for line in lines if line.split("&")[0].strip() not in labels]
new = []
for system, label in ROWS:
    row = [label]
    for input_name in ("raw", "reasoned"):
        runs = [run for run in loading["runs"] if run["system"] == system and run["input"] == input_name]
        entry = imports[system]
        entry = imports[entry["same_as"]] if "same_as" in entry else entry
        row += cells(runs, entry["max_mib"], limit)
    new.append(" & ".join(row + ["no"]) + "\\\\")
index = next(i for i, line in enumerate(lines) if line.split("&")[0].strip() == AFTER)
lines[index + 1:index + 1] = new
path.write_text("\n".join(lines))
print("loading table: rows for Nemo and reasonable")
