set -euo pipefail
cd /opt/aamas27/code/earlier/experiments
RAW=resources/owl2bench_statements_unreasoned.rdf
REASONED=/data/owl2bench_statements_reasoned.rdf
OUT=/out
python /opt/aamas27/tools/import_memory.py $OUT/memory/import_memory.json || { mkdir -p $OUT/memory; python /opt/aamas27/tools/import_memory.py $OUT/memory/import_memory.json; }
python scripts/aamas27/run_loading.py --systems krrood --inputs raw,reasoned --repetitions 5 --raw-file $RAW --reasoned-file $REASONED --results-dir $OUT/loading
python scripts/aamas27/run_loading.py --systems nemo_owlrl,reasonable_owlrl --inputs raw,reasoned --repetitions 5 --memory-limit-gib 24 --raw-file $RAW --reasoned-file $REASONED --results-dir $OUT/loading
mkdir -p $OUT/baselines
for s in nemo_owlrl reasonable_owlrl; do python -m krrood_experiments.aamas27.loading_worker --system $s --input-file $RAW --closure-output $OUT/baselines/$s.nt > /dev/null; done
python -m krrood_experiments.aamas27.closure_comparison --raw $RAW --reference $REASONED --candidate nemo_owlrl=$OUT/baselines/nemo_owlrl.nt --candidate reasonable_owlrl=$OUT/baselines/reasonable_owlrl.nt --output $OUT/baselines/closure_comparison.json
rm -f $OUT/baselines/*.nt
nmo --version > $OUT/nemo_version.txt
echo DONE
