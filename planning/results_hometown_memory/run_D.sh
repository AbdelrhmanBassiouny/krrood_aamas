#!/bin/bash
# Run D: Nemo / reasonable memory on OWL2Bench inputs without hasSameHomeTownWith (run_loading.py, as in the paper)
R=/home/bassioun/Projects/aamas27_unification_runs/hometown
d(){ sg docker -c "docker run --rm --cpuset-cpus=6-23 -m 28g --user 1000:1000 --entrypoint bash -e HOME=/tmp   -v /home/bassioun/Projects/krrood_experiments:/opt/aamas27/code/earlier/experiments -v /home/bassioun/Projects/aamas27_unification_runs/earlier_krrood_unpatched:/opt/aamas27/code/earlier/krrood   -v $R:/h -w /opt/aamas27/code/earlier/experiments krrood-aamas27-dev -lc '$1'"; }
echo "start $(date -u +%FT%TZ) load $(cut -d' ' -f1-3 /proc/loadavg)" > $R/machine_load.log
for case in "nemo_owlrl reasoned reasoned_without_hometown" "reasonable_owlrl reasoned reasoned_without_hometown" "nemo_owlrl reasoned reasoned_without_hometown_plus_raw_hometown" "reasonable_owlrl raw raw_without_hometown"; do
  set -- $case; mkdir -p $R/$1__$3
  d "/opt/venvs/earlier/bin/python scripts/aamas27/run_loading.py --systems $1 --inputs $2 --$2-file /h/inputs/$3.rdf --repetitions 5 --results-dir /h/$1__$3" > $R/$1__$3/run.log 2>&1
  echo "$1 $3 end $(date -u +%FT%TZ) exit $? load $(cut -d' ' -f1-3 /proc/loadavg)" >> $R/machine_load.log
done
# nmo alone, peak RSS from /usr/bin/time -v (as the earlier probe), 3 runs each
for f in reasoned_without_hometown reasoned_without_hometown_plus_raw_hometown; do for i in 1 2 3; do
  d "mkdir -p /tmp/e && /usr/bin/time -v nmo --overwrite-results --export-dir /tmp/e --report short --param input=\\"/h/inputs/$f.rdf\\" src/krrood_experiments/aamas27/owl2rl.rls" >> $R/nmo_alone__$f.log 2>&1
done; done
echo "end $(date -u +%FT%TZ)" >> $R/machine_load.log
