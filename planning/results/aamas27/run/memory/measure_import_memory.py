"""
Peak RSS (MiB) of a fresh Python process after the imports that a loading worker performs before it loads any data,
for the systems measured by run_loading.py in a worker process. Run in the bundle's image, with the earlier venv:
    /opt/venvs/earlier/bin/python measure_import_memory.py          (from code/earlier/experiments)
Each measurement runs in its own process, three times.
"""
import json, subprocess, sys

IMPORTS = {
    "krrood": "from krrood_experiments.aamas27 import loading_worker as w; w._import_krrood()",
    "owlready2_pellet": "import krrood_experiments.aamas27.loading_worker, owlready2",
    "rdflib_owlrl": "import krrood_experiments.aamas27.loading_worker, owlrl, rdflib",
}
PROBE = "; import resource; print(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024)"
result = {}
for system, code in IMPORTS.items():
    values = [float(subprocess.run([sys.executable, "-c", code + PROBE], capture_output=True, text=True,
                                   check=True).stdout.split()[-1]) for _ in range(3)]
    result[system] = {"import_rss_mib": values, "max_mib": max(values), "imports": code}
result["krrood_ormatic"] = result["krrood_eager_symmetric_transitive"] = {"same_as": "krrood"}
print(json.dumps(result, indent=2))
