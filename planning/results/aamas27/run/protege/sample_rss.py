"""
Samples the resident set size of a process tree every 50 ms, as the loading experiment does, until the root exits.
Writes one line per sample: Unix time in seconds and the RSS of the tree in KiB.

Usage: python3 sample_rss.py <root pid> <output file>
"""
import sys
import time
from pathlib import Path


def children(pid: int) -> list:
    result = []
    for task in Path(f"/proc/{pid}/task").glob("*"):
        try:
            result += [int(child) for child in (task / "children").read_text().split()]
        except OSError:
            pass
    return result


def tree_rss_kib(root: int) -> int:
    total, stack = 0, [root]
    while stack:
        pid = stack.pop()
        try:
            for line in Path(f"/proc/{pid}/status").read_text().splitlines():
                if line.startswith("VmRSS:"):
                    total += int(line.split()[1])
        except OSError:
            continue
        stack += children(pid)
    return total


root, output = int(sys.argv[1]), Path(sys.argv[2])
with output.open("w") as file:
    while Path(f"/proc/{root}").exists():
        file.write(f"{time.time():.3f} {tree_rss_kib(root)}\n")
        file.flush()
        time.sleep(0.05)
