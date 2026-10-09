"""Build the inputs of run D: OWL2Bench files without (or with only the raw) hasSameHomeTownWith statements."""
import sys
from pathlib import Path
import rdflib

raw_file, reasoned_file, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
raw = rdflib.Graph(); raw.parse(str(raw_file), format="xml")
reasoned = rdflib.Graph(); reasoned.parse(str(reasoned_file), format="xml")
hst = [p for p in set(raw.predicates()) | set(reasoned.predicates()) if str(p).endswith("#hasSameHomeTownWith")]
assert len(hst) == 1, hst
hst = hst[0]
raw_hst = list(raw.triples((None, hst, None)))
reasoned_hst = list(reasoned.triples((None, hst, None)))
print("property", hst, "raw statements", len(raw), "raw hst", len(raw_hst), "reasoned statements", len(reasoned), "reasoned hst", len(reasoned_hst))

def write(graph, name):
    graph.serialize(str(out / name), format="xml")
    print(name, len(graph))

for t in reasoned_hst: reasoned.remove(t)
write(reasoned, "reasoned_without_hometown.rdf")
for t in raw_hst: reasoned.add(t)
write(reasoned, "reasoned_without_hometown_plus_raw_hometown.rdf")
for t in raw_hst: raw.remove(t)
write(raw, "raw_without_hometown.rdf")
