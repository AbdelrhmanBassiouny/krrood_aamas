"""
The summary of the query times for the paper (Table "query summary"); the per-query times are in the supplementary
material. For every system and query, the time is the median of the 10 runs without the first, which includes
warm-up; the summary gives, per system, its geometric mean over the 18 queries, on how many queries it is the
fastest, its slowest query, and on how many queries its answer set equals GraphDB's.

With a third argument, the results of ORMatic's translation of the 18 queries (ormatic_translation.json, a separate
run over the part of the model the queries use), a row "SQL translated from EQL" follows SQLAlchemy's; it is the
fastest on a query only if it beats all other systems.

Usage: python3 planning/query_summary.py planning/results/aamas27/run/queries krrood_aamas_2027/tables/query_summary.tex
    [planning/results_ormatic_translation/ormatic_translation.json]
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
    if name == "sqlalchemy" and len(sys.argv) > 3:
        translation = {str(r["query"]): r for r in json.loads(Path(sys.argv[3]).read_text())["queries"]}
        translated = {q: translation[q]["execute_median_ms"] for q in queries}
        geometric = math.exp(sum(math.log(translated[q]) for q in queries) / len(queries))
        wins = sum(translated[q] < min(times[s][q] for s, _ in SYSTEMS) for q in queries)
        equal = sum(translation[q]["equal_to_graphdb"]["equal"] if isinstance(translation[q]["equal_to_graphdb"], dict)
                    else bool(translation[q]["equal_to_graphdb"]) for q in queries)
        rows.append((r"SQL translated from EQL$^{\dagger}$", geometric, wins, format_ms(translated["20"]),
                     format_ms(translated["22"]), equal))
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
geometric_of = {row[0]: row[1] for row in rows}
print(f"EQL faster than GraphDB on {faster} queries; geometric-mean ratio {geometric_of['EQL'] / geometric_of['GraphDB']:.2f}")
