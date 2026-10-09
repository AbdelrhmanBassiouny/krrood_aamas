#!/bin/bash
# Run A: KRROOD-only agent-loop rerun, earlier KRROOD + memoization patch
for s in 0 1 2 3 4; do
  echo "seed $s start $(date -u +%FT%TZ) load $(cut -d' ' -f1-3 /proc/loadavg)" >> /home/bassioun/Projects/aamas27_unification_runs/krrood_rerun/machine_load.log
  sg docker -c "docker run --rm --cpuset-cpus=0-5 -m 16g --entrypoint bash     -v /home/bassioun/Projects/krrood_experiments:/opt/aamas27/code/earlier/experiments -v /home/bassioun/Projects/aamas27_unification_runs/earlier_krrood:/opt/aamas27/code/earlier/krrood     -v /home/bassioun/Projects/aamas27_unification_runs/krrood_rerun:/out -w /opt/aamas27/code/earlier/experiments krrood-aamas27-dev     -lc '/opt/venvs/earlier/bin/python scripts/aamas27/run_agent_loop.py --variants krrood --seed $s --steps 200 --results-dir /out/seed$s'" > /home/bassioun/Projects/aamas27_unification_runs/krrood_rerun/run_seed$s.log 2>&1
  echo "seed $s end $(date -u +%FT%TZ) exit $? load $(cut -d' ' -f1-3 /proc/loadavg)" >> /home/bassioun/Projects/aamas27_unification_runs/krrood_rerun/machine_load.log
done
