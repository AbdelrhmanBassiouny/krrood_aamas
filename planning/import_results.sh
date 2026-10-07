#!/usr/bin/env bash
# Imports the results archive of the measured run into the paper: unpacks it into planning/results/, checks it,
# and copies the two LaTeX tables into krrood_aamas_2027/tables/.
#
# Usage: bash planning/import_results.sh /path/to/aamas27_results.tgz
set -euo pipefail

ARCHIVE="${1:?usage: bash planning/import_results.sh /path/to/aamas27_results.tgz}"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET="$REPO/planning/results"
RUN="$TARGET/aamas27/run"

rm -rf "$TARGET" && mkdir -p "$TARGET"
tar xzf "$ARCHIVE" -C "$TARGET"
echo "unpacked into $TARGET"

python3 - "$RUN" <<'PY'
import csv, json, sys
from pathlib import Path
run = Path(sys.argv[1])
problems = []
def load(path):
    try:
        return json.load(open(run / path))
    except FileNotFoundError:
        problems.append(f"missing {path}")
        return None

print("BUNDLE", (run / "BUNDLE").read_text().strip() if (run / "BUNDLE").exists() else "missing")
check = load("check/answer_check.json")
if check:
    print("answer check: all equal" if check["all_equal"] and not check["mismatches"] else f"answer check: {check['mismatches']}")
    if not check["all_equal"]:
        problems.append("answer sets differ")
audit = load("audit/audit.json")
if audit:
    for part in ("classes", "object_properties", "data_properties"):
        totals = {f: sum(x[f] for x in audit[part].values()) for f in ("krrood", "reference", "unsound", "missing")}
        print(f"audit {part}: {totals}")
        if totals["unsound"] or totals["missing"]:
            problems.append(f"audit {part} differs")
    print("OWL 2 RL check passed:", audit["owl2_rl_check"]["passed"])
loading = load("loading/loading.json")
if loading:
    print("loading runs:")
    for r in loading["runs"]:
        print(f"  {r['system']:<36} {r.get('input', ''):<9} {r.get('status')}")
for table in ("loading_table.tex", "query_table.tex"):
    if not (run / "tables" / table).exists():
        problems.append(f"missing tables/{table}")
if not (run / "protege.json").exists():
    print("note: no protege.json, so the tables have no Protégé numbers")
monitor = run / "host" / "monitor.csv"
if monitor.exists():
    rows = list(csv.DictReader(open(monitor)))
    busy = [r for r in rows if r["busy_outside_docker"]]
    print(f"monitor: {len(rows)} samples, {len(busy)} with other programs busy, "
          f"max load {max((float(r['load1']) for r in rows), default=0):.1f}")
    for r in busy[:10]:
        print("   ", r["time"], r["busy_outside_docker"])
else:
    print("note: no host/monitor.csv")
print("PROBLEMS:", problems if problems else "none")
PY

cp "$RUN/tables/loading_table.tex" "$RUN/tables/query_table.tex" "$REPO/krrood_aamas_2027/tables/"
# The paper names two rows differently from make_tables.py of the bundle (renamed after the run had started).
sed -i 's/KRROOD + ORMatic/KRROOD (with ORMatic)/; s/Eager chaining/KRROOD without step 5/' \
    "$REPO/krrood_aamas_2027/tables/loading_table.tex"
grep -q "KRROOD (with ORMatic)" "$REPO/krrood_aamas_2027/tables/loading_table.tex" \
    && grep -q "KRROOD without step 5" "$REPO/krrood_aamas_2027/tables/loading_table.tex" \
    || { echo "FAILED: the two loading-table rows were not renamed"; exit 1; }
python3 "$REPO/planning/bold_lowest_memory.py" "$REPO/krrood_aamas_2027/tables/loading_table.tex"
# Protégé's queries ran once (std_ms 0 in protege.json): its column, the last one, shows the time without "± 0.00".
python3 - "$REPO/krrood_aamas_2027/tables/query_table.tex" <<'PY'
import re, sys
path = sys.argv[1]
lines = open(path).read().split("\n")
header = next((l for l in lines if l.startswith("\\textbf{Query}")), "")
if "Prot" in header.split("&")[-1]:
    for i, line in enumerate(lines):
        if re.match(r"Q\d+ &", line):
            cells = line.split(" & ")
            cells[-1] = cells[-1].replace(" \\pm 0.00", "")
            lines[i] = " & ".join(cells)
    open(path, "w").write("\n".join(lines))
    print("Protégé column: single runs, without ± 0.00")
PY
echo "copied loading_table.tex and query_table.tex into krrood_aamas_2027/tables/"
git -C "$REPO" diff --stat -- krrood_aamas_2027/tables
