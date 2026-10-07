"""
Samples the CPU time of a process (user + system, all threads) every 20 ms until it exits, to find when Protégé is busy
running a query; Snap SPARQL shows the number of results but no time. Writes Unix time and CPU seconds per line.
Usage: python3 sample_cpu.py <pid> <output file>
"""
import os
import sys
import time
from pathlib import Path

TICKS = os.sysconf("SC_CLK_TCK")
pid, output = int(sys.argv[1]), Path(sys.argv[2])
with output.open("w") as file:
    while True:
        try:
            fields = Path(f"/proc/{pid}/stat").read_text().rsplit(")", 1)[1].split()
        except OSError:
            break
        file.write(f"{time.time():.3f} {(int(fields[11]) + int(fields[12])) / TICKS:.2f}\n")
        file.flush()
        time.sleep(0.02)
