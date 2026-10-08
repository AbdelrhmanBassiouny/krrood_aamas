"""
Rewrites the loading table so that memory is the increase during loading, and adds whether a system persists its
data. make_tables.py of the bundle reports the peak RSS of each process; a worker process also holds the interpreter
and its imports, and GraphDB's server holds its fixed 8 GB Java heap, so the peak hides how memory grows with the
data. The increase is:

* for a worker-based system, the largest peak RSS of its runs (as make_tables.py takes it) minus the peak RSS of a
  fresh worker after its imports (memory/import_memory.json);
* for GraphDB, the Java heap in use after GC at its peak during the load minus before it
  (memory/graphdb_heap/graphdb_heap.json);
* for Protégé, likewise its Java heap in use after GC, from loading the file until Pellet has finished
  (heap_increase_mib in protege.json, see protege/README.txt); its JVM has a 28 GB heap, so its RSS shows how lazily
  the JVM collects garbage rather than what Pellet needs.

The Protégé row is kept as a row to fill in while there is no protege.json. Run before bold_lowest_memory.py.

Usage: python3 planning/loading_memory_increase.py planning/results/aamas27/run krrood_aamas_2027/tables/loading_table.tex
"""
import json
import sys
from pathlib import Path

ROWS = {
    "KRROOD": "krrood",
    "RDFLib": "rdflib_owlrl",
    "Owlready2": "owlready2_pellet",
    "GraphDB": "graphdb",
    "KRROOD + ORMatic": "krrood_ormatic",
    "KRROOD without step 5": "krrood_eager_symmetric_transitive",
}
PERSISTS = {"GraphDB", "KRROOD + ORMatic"}
PROTEGE = "Prot\\'eg\\'e"
HEAP = "$^{\\ast}$"
"""Marks a memory cell that is the increase of a Java heap in use, not of process memory (see the table's caption)."""
INPUTS = ("raw", "reasoned")


def format_memory(mib: float) -> str:
    """The format of make_tables.py of the bundle."""
    return f"{mib / 1024:.2f}\\,GB" if mib >= 1024 else f"{mib:.0f}\\,MB"


def peak_mib(runs: list) -> float:
    """The peak RSS that make_tables.py reports: the largest of the finished runs, else that of the first run."""
    finished = [run for run in runs if run["status"] == "ok"]
    return max(run["peak_rss_mib"] for run in finished) if finished else runs[0]["peak_rss_mib"]


def import_mib(imports: dict, system: str) -> float:
    entry = imports[system]
    return imports[entry["same_as"]]["max_mib"] if "same_as" in entry else entry["max_mib"]


def increase_mib(run_dir: Path, system: str, input_name: str):
    if system == "graphdb":
        heap = json.loads((run_dir / "memory/graphdb_heap/graphdb_heap.json").read_text())
        return heap[input_name]["heap_increase_mib"]
    loading = json.loads((run_dir / "loading/loading.json").read_text())
    runs = [run for run in loading["runs"] if run["system"] == system and run.get("input") == input_name]
    if not runs:
        return None
    imports = json.loads((run_dir / "memory/import_memory.json").read_text())
    return peak_mib(runs) - import_mib(imports, system)


run_dir, path = Path(sys.argv[1]), Path(sys.argv[2])
lines = path.read_text().split("\n")
output = []
for line in lines:
    label = line.split("&")[0].strip()
    if line.startswith("\\begin{tabular}"):
        line = "\\begin{tabular}{@{}lrrrrc@{}}"
    elif line.lstrip().startswith("& \\multicolumn"):
        line = line.rstrip("\\") + " & \\\\"
    elif line.startswith("\\textbf{System}"):
        line = line.rstrip("\\") + " & \\textbf{Persists}\\\\"
    elif label in ROWS:
        cells = [cell.strip() for cell in line.rstrip("\\").split("&")]
        for column, input_name in ((2, "raw"), (4, "reasoned")):
            mib = increase_mib(run_dir, ROWS[label], input_name)
            if mib is not None:
                cells[column] = format_memory(mib) + (HEAP if ROWS[label] == "graphdb" else "")
        cells.append("yes" if label in PERSISTS else "no")
        line = " & ".join(cells) + "\\\\"
    elif label == PROTEGE:
        cells = [cell.strip() for cell in line.rstrip("\\").split("&")]
        if (run_dir / "protege.json").exists():
            loading = json.loads((run_dir / "protege.json").read_text())["loading"]
            for column, input_name in ((2, "raw"), (4, "reasoned")):
                cells[column] = format_memory(loading[input_name]["heap_increase_mib"]) + HEAP
        line = " & ".join(cells + ["no"]) + "\\\\"
    output.append(line)
    if label == "Owlready2" and not any(l.split("&")[0].strip() == PROTEGE for l in lines):
        output.append(f"{PROTEGE} & \\tbd{{}} & \\tbd{{}} & \\tbd{{}} & \\tbd{{}} & no\\\\")
path.write_text("\n".join(output))
print("loading table: memory as the increase during loading, and a Persists column")
