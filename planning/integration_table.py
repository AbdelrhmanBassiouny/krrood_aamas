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
* Synchronization lines: counted by the @boundary markers of the agent loop's code.
* All boundary lines: every line the markers count, also the mapping and procedure-integration lines, which are not
  shown on their own: the mapping lines follow from the simulated perceptions, which arrive as IRIs in every build,
  and the procedure lines from wrapping the planner, not from the number of world models.

The rows are grouped by what they follow from: the semantics (queries are evaluated over the program's objects, so
there is one world model, the planner is a predicate of the query, and nothing is written to another store or
synchronized), or the implementation (one language and one process, which a wrapper that generates SPARQL or an
embedded store could also give while keeping two world models).
* Step time: median over all steps of all seeds; the largest deviation of a seed's median from it is printed for
  the caption.

* Owlready2: from its own run with seed 0 (results_agentloop_owlready2/agent_loop_seeds.json, fourth argument):
  facts asserted on Owlready2's objects, the previous inferences deleted and Pellet run again every step. Pellet runs
  as a Java process started per step ("1 run"); its writes are the inferences deleted and written back per step;
  it ran one seed.
* Nemo: from its own run (results_agentloop_nemo/agent_loop_seeds.json, third argument). Its knowledge is the
  program's objects plus a file of the perceived facts, and each step starts one Nemo process instead of a request
  to a server, shown as "1 run" among the round trips.

Usage: python3 planning/integration_table.py planning/results_agentloop_seeds/agent_loop_seeds.json \
           krrood_aamas_2027/tables/integration_table.tex planning/results_agentloop_nemo/agent_loop_seeds.json \
           planning/results_agentloop_owlready2/agent_loop_seeds.json
"""
import json
import sys
from pathlib import Path

COLUMNS = [("krrood", "KRROOD"), ("graphdb", "GraphDB"), ("graphdb_push", "push"), ("nemo", "Nemo"),
           ("owlready2", "Owlready2")]
STRUCTURE = {
    "Languages": {"krrood": "1", "graphdb": "2", "graphdb_push": "2", "nemo": "2", "owlready2": "1"},
    "Processes": {"krrood": "1", "graphdb": "2", "graphdb_push": "2", "nemo": "2", "owlready2": "2"},
    "World models": {"krrood": "1", "graphdb": "2", "graphdb_push": "2", "nemo": "2", "owlready2": "2"},
    "Planner vs.\\ query": {"krrood": "inside", "graphdb": "after", "graphdb_push": "before", "nemo": "after",
                           "owlready2": "after"},
}


def number(value: float) -> str:
    if value >= 1e6:
        return f"{value / 1e6:.1f}\\,M"
    return f"{value:,.0f}".replace(",", "{,}")


def step_time(key: str) -> str:
    return f"{summary[key]['median_step_ms']:,.0f}".replace(",", "{,}")


def seed_spread(key: str) -> float:
    """
    :return: The largest deviation of a seed's median step time from the median over all steps, relative to it.
    """
    median = summary[key]["median_step_ms"]
    return max(abs(seed - median) / median for seed in summary[key]["per_seed_median_step_ms"])


summary = json.loads(Path(sys.argv[1]).read_text())["variants"]
summary["nemo"] = json.loads(Path(sys.argv[3]).read_text())["variants"]["nemo"]
summary["owlready2"] = json.loads(Path(sys.argv[4]).read_text())["variants"]["owlready2"]


def lines_of(key: str, category: str) -> str:
    return str(summary[key]["boundary_lines"]["per_category"].get(category, 0))


semantics = [[label] + [STRUCTURE[label][key] for key, _ in COLUMNS] for label in ("World models", "Planner vs.\\ query")]
semantics.append(["Writes"] + [
    "0" if key.startswith("krrood") else number(summary[key]["median_per_step"]["statements_inserted"]
                                                + summary[key]["median_per_step"]["statements_deleted"])
    for key, _ in COLUMNS])
semantics.append(["Sync.\\ lines"] + [lines_of(key, "synchronization") for key, _ in COLUMNS])
implementation = [[label] + [STRUCTURE[label][key] for key, _ in COLUMNS] for label in ("Languages", "Processes")]
implementation.append(["Round trips"] + [
    "1 run" if key in ("nemo", "owlready2") else number(summary[key]["median_per_step"]["round_trips"]) for key, _ in COLUMNS])
implementation.append(["Boundary lines"] + [str(summary[key]["boundary_lines"]["total"]) for key, _ in COLUMNS])
implementation.append(["Step [ms]"] + [step_time(key) for key, _ in COLUMNS])
lines = [r"\begin{tabular}{@{}l" + "r" * len(COLUMNS) + "@{}}", r"\toprule",
         " & ".join([""] + [f"\\textbf{{{label}}}" for _, label in COLUMNS]) + r"\\", r"\midrule"]
for title, rows in (("From the semantics", semantics), ("From the implementation", implementation)):
    lines.append(f"\\multicolumn{{{len(COLUMNS) + 1}}}{{@{{}}l}}{{\\emph{{{title}}}}}\\\\")
    lines += [" & ".join(row) + r"\\" for row in rows]
lines += [r"\bottomrule", r"\end{tabular}"]
Path(sys.argv[2]).write_text("\n".join(lines) + "\n")
print(f"% largest deviation of a seed median: {max(seed_spread(key) for key, _ in COLUMNS):.1%}")
print("\n".join(lines))
