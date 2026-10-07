"""
Marks the lowest peak memory per input in bold in the loading table, as make_tables.py of the bundle marks the
lowest time. Like the time, it compares only the systems that make_tables.py compares (not KRROOD with ORMatic
or the ablation), and only runs that finished: a run that timed out or failed stopped early.

Usage: python3 planning/bold_lowest_memory.py krrood_aamas_2027/tables/loading_table.tex
"""
import re
import sys

COMPARED = ("KRROOD", "RDFLib", "Owlready2", "Prot\\'eg\\'e", "GraphDB", "Nemo", "reasonable")
FINISHED = re.compile(r"^\$(\\mathbf\{)?[0-9]")
UNITS = {"MB": 1.0, "GB": 1024.0}


def megabytes(cell: str) -> float:
    number, unit = cell.strip().replace("$^{\\ast}$", "").split("\\,")
    return float(number) * UNITS[unit]


path = sys.argv[1]
lines = open(path).read().split("\n")
rows = {i: [c.strip() for c in line.rstrip("\\").split("&")]
        for i, line in enumerate(lines) if line.split("&")[0].strip() in COMPARED}
for time_column in (1, 3):
    memory_column = time_column + 1
    finished = [(megabytes(cells[memory_column]), i) for i, cells in rows.items()
                if FINISHED.match(cells[time_column]) and "\\," in cells[memory_column]]
    if finished:
        i = min(finished)[1]
        rows[i][memory_column] = f"\\textbf{{{rows[i][memory_column]}}}"
for i, cells in rows.items():
    lines[i] = " & ".join(cells) + "\\\\"
open(path, "w").write("\n".join(lines))
print("loading table: lowest memory per input in bold")
