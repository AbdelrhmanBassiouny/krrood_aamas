"""
The integration requirements of the delivery robot (Section 7.4), per way of building it, from the agent loop's
runs with five seeds (aggregate_agent_loop_seeds.py) and from its code:

* Languages: the languages in which the robot's developer writes code or queries (the OWL ontology is the same
  input for all). KRROOD: Python. GraphDB: Python and SPARQL (updates and queries).
* Processes: the processes that hold the robot's knowledge at runtime. GraphDB runs as a Java server, reached
  over HTTP.
* World models: the representations of the robot's world at runtime: the objects of the program, and for GraphDB
  also its RDF store.
* Planner: where the planner's predicate and function run: inside the query (KRROOD), on the query's answers
  (GraphDB), or before the query, with its results written into the store (GraphDB, push).
* Round trips and writes: medians per step over all steps of all seeds; writes are statements inserted into or
  deleted from another store (KRROOD's assignments change its own objects).
* Synchronization lines, and mapping / procedure-integration lines: counted by the @boundary markers of the agent
  loop's code.

The rows are grouped by what they follow from: the semantics (queries are evaluated over the program's objects, so
there is one world model, the planner is a predicate of the query, and nothing is written to another store or
synchronized), or the implementation (one language and one process, which a wrapper that generates SPARQL or an
embedded store could also give while keeping two world models).
* Step time: median over all steps of all seeds, with the range of the per-seed medians.

* Nemo: from its own run (results_agentloop_nemo/agent_loop_seeds.json, third argument). Its knowledge is the
  program's objects plus a file of the perceived facts, and each step starts one Nemo process instead of a request
  to a server, shown as "1 run" among the round trips.

Usage: python3 planning/integration_table.py planning/results_agentloop_seeds/agent_loop_seeds.json \
           krrood_aamas_2027/tables/integration_table.tex planning/results_agentloop_nemo/agent_loop_seeds.json
"""
import json
import sys
from pathlib import Path

COLUMNS = [("krrood", "KRROOD"), ("graphdb", "GraphDB"), ("graphdb_push", "GraphDB, push"), ("nemo", "Nemo")]
STRUCTURE = {
    "Languages": {"krrood": "1", "graphdb": "2", "graphdb_push": "2", "nemo": "2"},
    "Processes": {"krrood": "1", "graphdb": "2", "graphdb_push": "2", "nemo": "2"},
    "World models": {"krrood": "1", "graphdb": "2", "graphdb_push": "2", "nemo": "2"},
    "Planner runs": {"krrood": "in query", "graphdb": "on answers", "graphdb_push": "before query", "nemo": "on answers"},
}


def number(value: float) -> str:
    return f"{value:.0f}"


summary = json.loads(Path(sys.argv[1]).read_text())["variants"]
summary["nemo"] = json.loads(Path(sys.argv[3]).read_text())["variants"]["nemo"]


def lines_of(key: str, category: str) -> str:
    return str(summary[key]["boundary_lines"]["per_category"].get(category, 0))


semantics = [[label] + [STRUCTURE[label][key] for key, _ in COLUMNS] for label in ("World models", "Planner runs")]
semantics.append(["Writes / step"] + [
    "0" if key.startswith("krrood") else number(summary[key]["median_per_step"]["statements_inserted"]
                                                + summary[key]["median_per_step"]["statements_deleted"])
    for key, _ in COLUMNS])
semantics.append(["Synchronization lines"] + [lines_of(key, "synchronization") for key, _ in COLUMNS])
implementation = [[label] + [STRUCTURE[label][key] for key, _ in COLUMNS] for label in ("Languages", "Processes")]
implementation.append(["Round trips / step"] + [
    "1 run" if key == "nemo" else number(summary[key]["median_per_step"]["round_trips"]) for key, _ in COLUMNS])
implementation.append(["Mapping/proc.\\ lines"] + [
    f"{lines_of(key, 'mapping')}/{lines_of(key, 'procedure_integration')}" for key, _ in COLUMNS])
implementation.append(["Step [ms]"] + [
    f"{summary[key]['median_step_ms']:,.0f} ({min(summary[key]['per_seed_median_step_ms']):,.0f}--"
    f"{max(summary[key]['per_seed_median_step_ms']):,.0f})".replace(",", "{,}") for key, _ in COLUMNS])
lines = [r"\begin{tabular}{@{}lrrrr@{}}", r"\toprule",
         " & ".join([""] + [f"\\textbf{{{label}}}" for _, label in COLUMNS]) + r"\\", r"\midrule"]
for title, rows in (("From the semantics", semantics), ("From the implementation", implementation)):
    lines.append(f"\\multicolumn{{5}}{{@{{}}l}}{{\\emph{{{title}}}}}\\\\")
    lines += [" & ".join(row) + r"\\" for row in rows]
lines += [r"\bottomrule", r"\end{tabular}"]
Path(sys.argv[2]).write_text("\n".join(lines) + "\n")
print("\n".join(lines))
