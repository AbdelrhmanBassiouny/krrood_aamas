"""
The summary of the query times for the paper (Table "query summary"); the per-query times are in the supplementary
material. For every system and query, the time is the median of the 10 runs without the first, which includes
warm-up; the summary gives, per system, its geometric mean over the 18 queries, on how many queries it is the
fastest, its slowest query, and on how many queries its answer set equals GraphDB's.

Usage: python3 planning/query_summary.py planning/results/aamas27/run/queries krrood_aamas_2027/tables/query_summary.tex
"""
import json
import math
import statistics
import sys
from pathlib import Path

SYSTEMS = [("eql", "EQL"), ("sqlalchemy", "SQLAlchemy"), ("graphdb", "GraphDB"), ("rdflib", "RDFLib"),
           ("owlready2", "Owlready2")]


def median_without_first(entry: dict) -> float:
    return statistics.median(entry["times_ms"][1:])


def format_ms(value: float) -> str:
    return f"{value:.2f}" if value < 10 else f"{value:.1f}" if value < 100 else f"{value:,.0f}".replace(",", "{,}")


directory, output = Path(sys.argv[1]), Path(sys.argv[2])
times = {name: {q: median_without_first(e) for q, e in json.loads((directory / f"queries_{name}.json").read_text())
                ["queries"].items()} for name, _ in SYSTEMS}
check = json.loads((directory / "answer_check.json").read_text())["queries"]
queries = sorted(times["graphdb"], key=int)
fastest = {name: 0 for name, _ in SYSTEMS}
for q in queries:
    fastest[min(SYSTEMS, key=lambda s: times[s[0]][q])[0]] += 1
rows = []
for name, label in SYSTEMS:
    values = [times[name][q] for q in queries]
    geometric = math.exp(sum(map(math.log, values)) / len(values))
    equal = len(queries) if name == "graphdb" else sum(check[q][name]["equal"] for q in queries)
    rows.append((label, geometric, fastest[name], format_ms(times[name]["20"]), format_ms(times[name]["22"]), equal))
best = min(row[1] for row in rows)
lines = [r"\begin{tabular}{@{}lrrrrr@{}}", r"\toprule",
         r"\textbf{System} & \textbf{Geo.\ mean} & \textbf{Fastest} & \textbf{Q20} & \textbf{Q22} & \textbf{Equal}\\",
         r"\midrule"]
for label, geometric, count, q20, q22, equal in rows:
    mean = f"\\textbf{{{geometric:.2f}}}" if geometric == best else f"{geometric:.2f}"
    lines.append(f"{label} & {mean} & {count} & {q20} & {q22} & {equal}/{len(queries)}\\\\")
lines += [r"\bottomrule", r"\end{tabular}"]
output.write_text("\n".join(lines) + "\n")
print("\n".join(lines))
faster = sum(times["eql"][q] < times["graphdb"][q] for q in queries)
print(f"EQL faster than GraphDB on {faster} queries; geometric-mean ratio {rows[0][1] / rows[2][1]:.2f}")
