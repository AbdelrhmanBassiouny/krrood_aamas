"""Peak RSS of the nmo process alone (os.wait4 rusage of the child), 3 runs per input."""
import os, subprocess, sys, tempfile, json
rules = "/opt/aamas27/code/earlier/experiments/src/krrood_experiments/aamas27/owl2rl.rls"
result = {}
for f in sys.argv[1:]:
    runs = []
    for _ in range(3):
        with tempfile.TemporaryDirectory() as d:
            with open(os.devnull, "w") as null:
                p = subprocess.Popen(["nmo", "--overwrite-results", "--export-dir", d, "--report", "short",
                                      "--param", f'input="{f}"', rules], stdout=null, stderr=null)
                _, status, usage = os.wait4(p.pid, 0)
            runs.append({"exit_status": os.waitstatus_to_exitcode(status), "max_rss_mib": usage.ru_maxrss / 1024})
    result[f] = runs
print(json.dumps(result, indent=1))
