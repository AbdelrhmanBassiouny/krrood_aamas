#!/bin/bash
# Run run_ormatic_translation.py with the translator of the worktree (mounted at /cram_src) first on the path.
mkdir -p /tmp/pg && ln -sf /opt/venvs/earlier/lib/python3.12/site-packages/psycopg2 /tmp/pg/ && ln -sf /opt/venvs/earlier/lib/python3.12/site-packages/psycopg2_binary.libs /tmp/pg/
cd /work/scripts/aamas27/ormatic_translation
export PYTHONPATH=/cram_src:/tmp/pg
/opt/venvs/current/bin/python -c "import krrood, sys; print('krrood from', krrood.__file__)"
/opt/venvs/current/bin/python run_ormatic_translation.py \
  --reasoned-file /closure/owl2bench_statements_reasoned.rdf \
  --reference-answers /paper_run/check/answers/graphdb \
  --paper-sqlalchemy-times /paper_run/queries/queries_sqlalchemy.json \
  --database-uri postgresql+psycopg2://krrood:krrood@ormatic-postgres:5432/translation \
  --statements-cache /s/statements_cache_final.json.gz \
  --output-dir "${OUT:-/s/out}" "$@"
