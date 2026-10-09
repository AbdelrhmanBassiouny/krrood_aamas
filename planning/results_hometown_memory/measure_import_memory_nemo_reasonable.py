"""
Same method as planning/results/aamas27/run/memory/measure_import_memory.py, for the two worker-based systems it
does not cover: the imports of the nemo_owlrl and reasonable_owlrl workers before they load data.
"""
import json, subprocess, sys

IMPORTS = {
    "nemo_owlrl": "import krrood_experiments.aamas27.loading_worker",
    "reasonable_owlrl": "import krrood_experiments.aamas27.loading_worker, rdflib, reasonable",
}
PROBE = "; import resource; print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)"
result = {}
for system, code in IMPORTS.items():
    values = [float(subprocess.run([sys.executable, "-c", code + PROBE], capture_output=True, text=True,
                                   check=True).stdout.split()[-1]) for _ in range(3)]
    result[system] = {"import_rss_mib": values, "max_mib": max(values), "imports": code}
print(json.dumps(result, indent=2))
