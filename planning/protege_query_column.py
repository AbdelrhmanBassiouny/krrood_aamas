"""
Rewrites the Protégé column of the query table. make_tables.py of the bundle treats it like the measured columns, but
Protégé's queries ran once by hand and Snap SPARQL logs whole milliseconds:

* a time is shown as whole milliseconds, without "± 0.00", and 0 ms as "<1";
* the fastest of a query is chosen among the other frameworks only (a single run with 1 ms resolution is not
  comparable with a mean of 10 runs in bold);
* the geometric mean is that of the other frameworks over the queries they all completed (as before Protégé was
  added; Protégé did not complete Q9 and Q20), and "---" for Protégé.

Usage: python3 planning/protege_query_column.py planning/results/aamas27/run krrood_aamas_2027/tables/query_table.tex
"""
import json
import math
import re
import statistics
import sys
from pathlib import Path

run_dir, path = Path(sys.argv[1]), Path(sys.argv[2])
frameworks = {name: run["result"]["queries"]
              for name, run in json.loads((run_dir / "queries/queries.json").read_text())["frameworks"].items()}
lines = path.read_text().split("\n")
header = next(line for line in lines if line.startswith("\\textbf{Query}"))
labels = [re.sub(r"\\textbf\{(.*)\}", r"\1", cell.strip().rstrip("\\")) for cell in header.split("&")][2:]
assert labels[-1] == "Prot\\'eg\\'e", labels
keys = [label.lower() for label in labels[:-1]]
assert set(keys) == set(frameworks), (keys, list(frameworks))


def completed(key: str, number: str) -> bool:
    entry = frameworks[key].get(number, {})
    return entry.get("status") == "ok" and entry.get("mean_ms") is not None


def strip_bold(cell: str) -> str:
    return re.sub(r"\\mathbf\{(.*)\}", r"\1", cell)


numbers = sorted({n for queries in frameworks.values() for n in queries}, key=int)
all_completed = [n for n in numbers if all(completed(key, n) for key in keys)]
geometric = {key: math.exp(statistics.mean(math.log(frameworks[key][n]["mean_ms"]) for n in all_completed))
             for key in keys}
best = min(geometric, key=geometric.get)
for index, line in enumerate(lines):
    match = re.match(r"Q(\d+) &", line)
    if match:
        cells = [cell.strip() for cell in line.rstrip("\\").split(" & ")]
        number = match[1]
        means = {key: frameworks[key][number]["mean_ms"] for key in keys if completed(key, number)}
        fastest = min(means, key=means.get)
        for column, key in enumerate(keys, start=2):
            cells[column] = strip_bold(cells[column])
            if key == fastest:
                cells[column] = f"$\\mathbf{{{cells[column].strip('$')}}}$"
        protege = re.match(r"\$(?:\\mathbf\{)?([\d.]+) \\pm [\d.]+\}?\$", cells[-1])
        if protege:
            milliseconds = float(protege[1])
            cells[-1] = "$<1$" if milliseconds < 1 else f"${milliseconds:.0f}$"
        lines[index] = " & ".join(cells) + "\\\\"
    elif line.startswith("\\textbf{Geom. Mean}"):
        cells = [f"$\\mathbf{{{geometric[key]:.2f}}}$" if key == best else f"${geometric[key]:.2f}$" for key in keys]
        lines[index] = "\\textbf{Geom. Mean} & --- & " + " & ".join(cells) + " & ---\\\\"
    elif line.startswith("% geometric mean over"):
        lines[index] = (f"% geometric mean over the {len(all_completed)} queries completed by all frameworks but "
                        f"Protégé: Q" + ", Q".join(all_completed))
path.write_text("\n".join(lines))
print(f"query table: Protégé column as single runs, geometric means over {len(all_completed)} queries")
