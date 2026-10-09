# Runs for the unification revision (on the PC with Docker and GraphDB)

Everything that runs without Docker/GraphDB was run in the cloud session (see "Already run" at the end). The four
jobs below need the PC. Paths: `EXP` = the krrood_experiments checkout, `CRAM` = the
cognitive_robot_abstract_machine checkout, `PAPER` = this repository.

## 0. Apply the patches (experiments repo and the earlier KRROOD version)

The experiments repository's branch `aamas27-review6` is not public, so the cloud session worked on the copies in
the supplement zip and wrote patches (paths are relative to each repository's root):

```bash
cd $EXP && git checkout aamas27-review6 && git checkout -b unification-revision
git apply --check $PAPER/planning/unification_revision/experiments_m1_counters_and_memoization_tests.patch
git apply $PAPER/planning/unification_revision/experiments_m1_counters_and_memoization_tests.patch
# the earlier KRROOD version used by the experiments (code/earlier/krrood in the bundle; in the Docker image
# krrood-aamas27-dev it is the krrood source the experiments import):
cd <earlier krrood checkout> && git apply $PAPER/planning/unification_revision/earlier_krrood_memoization.patch
```

Check, inside the image (earlier env):

```bash
docker run --rm -v $EXP:/exp -v <earlier krrood>:/krrood -w /exp krrood-aamas27-dev \
  bash -lc 'pip install -e /krrood -q && pytest -q tests/aamas27/test_procedure_results.py tests/aamas27/test_agent_loop.py'
```

Expected: all pass (`test_procedure_results.py` fails without the KRROOD patch: 6 calls instead of 3).

## 1. KRROOD-only agent-loop rerun (earlier version + memoization patch), ~10-20 min

The other builds are unaffected (their code does not use EQL predicates), so only KRROOD runs again.

```bash
for s in 0 1 2 3 4; do
  docker run --rm --cpuset-cpus=0-5 -m 16g -v $EXP:/exp -v $HOME/krrood_rerun:/out -w /exp krrood-aamas27-dev \
    bash -lc "pip install -e /krrood -q && python scripts/aamas27/run_agent_loop.py \
      --variants krrood --seed $s --steps 200 --results-dir /out/seed$s"
done
python3 $PAPER/planning/unification_revision/compare_krrood_rerun.py \
  $PAPER/planning/results_agentloop $HOME/krrood_rerun
```

Expected: `all_actions_and_digests_equal: true` against stored graphdb, graphdb_push and krrood (Nemo and Owlready2
are compared through the stored krrood run, which they matched). New: `median_step_ms` and `median_calls_per_step`
(can_reach should drop from 1,124 to roughly the number of distinct target rooms reached, about 49-201). Copy
`$HOME/krrood_rerun` to `planning/results_agentloop_krrood_memo/` with a provenance.txt, then update KRROOD's column
of `tables/integration_table.tex` (step time) and the 90/88 ms in Section 7.4's Results paragraph.

## 2. M1: writes and rows as the campus grows (GraphDB), est. 1.5-2 h

One GraphDB load (raw data does not change with k) reused by all runs: run k=5 seed 0 first, which loads, then pass
`--resume` with a copied `graphdb_repository_state.json` (see results_agentloop/provenance.txt for the mechanism).

```bash
for k in 5 3 2 1; do for s in 0 1 2 3 4; do
  out=/out/m1/k$k/seed$s; mkdir -p $HOME/m1/k$k/seed$s
  cp $HOME/m1/graphdb_repository_state.json $HOME/m1/k$k/seed$s/ 2>/dev/null || true
  docker compose run --rm -T experiments bash -lc "pip install -e /krrood -q && \
    python scripts/aamas27/run_agent_loop.py --variants krrood,graphdb,graphdb_push \
      --courses-per-classroom $k --seed $s --steps 200 --results-dir $out --resume --keep-graphdb-repository"
  cp $HOME/m1/k$k/seed$s/graphdb_repository_state.json $HOME/m1/ 2>/dev/null || true
done; done
for k in 5 3 2 1; do python scripts/aamas27/aggregate_agent_loop_seeds.py \
  $HOME/m1/k$k/agent_loop_seeds.json $HOME/m1/k$k/seed{0,1,2,3,4}; done
```

(Adjust the volume mounts to your compose file.) Read per k: `median_per_step.statements_inserted/deleted`,
`planner_values_pushed`, `rows_returned`, `median_can_reach_false_per_step`, and `target_rooms` from the push
variant's final measurements. Expected (not yet measured): push writes about 405/634/916/1,764 per step for
201/315/456/880 target rooms; GraphDB 4 writes; KRROOD 0 writes and 0 rows across a boundary. Then replace the
`\pending{...}` paragraph "As the campus grows" in main.tex with the measured numbers (a few rows in Table 4 or one
small figure).

## 3. 18-query translation rerun (current version after the ORMatic fixes), ~2 min + database

```bash
cd $CRAM && git checkout claude/krrood-aamas-unification-rih3rk   # rename to aamas27-unification-revision if wanted
# in the bundle's container with PostgreSQL, current-version env:
python scripts/aamas27/ormatic_translation/run_ormatic_translation.py --selection iris \
  --reasoned-file <pre-reasoned OWL2Bench file> \
  --reference-answers <results/check/answers/graphdb of run ae0b139a> \
  --database-uri postgresql://<user>@<host>/<db> \
  --output-dir results/ormatic_translation_unification
```

(Same arguments as the stored run in `planning/results_ormatic_translation_iris`, whose provenance records them.)

Expected: 18/18 queries equal in working memory, SQL and GraphDB (as in results/ormatic_translation). The three code
commits change the translator only by rejecting a bare variable used as a condition (none of the 18 queries does)
and the generated schema only for references typed with their own class (OWL2Bench has none), so the answers should
not change.

## 4. Supplement rebuild

```bash
cd $EXP/supplement
cp $PAPER/planning/unification_revision/supplement/README.md README.md
cp $PAPER/planning/unification_revision/supplement/formalization/eql_formalization.tex formalization/
cp $PAPER/planning/unification_revision/supplement/formalization/unification_proofs.tex formalization/
# listings/ormatic/test_ormatic_listing.py: use eql_to_sql(..., select_identifiers=True, identifying_attribute="uri")
python make_supplement.py <out> --results $PAPER/planning/results/aamas27/run --code-from <dirs as before>
pytest -q listings/test_listings.py listings/ormatic/test_ormatic_listing.py
```

Add the new results folders (KRROOD rerun, M1, translation rerun) to the bundle's results and provenance.

## Already run in the cloud session

- Current version: `test/krrood_test/test_eql` 1,447 passed (4 failed and 9 errors, the same as before the change:
  igraph/visualization and probabilistic-backend imports missing in the cloud env); `test/krrood_test/test_ormatic`
  317 passed, 1 xfailed; translator files `test_eql_identifier_selection.py` + `test_eql_collections.py`
  78 passed, 1 xfailed (77 + the new rejection test).
- Earlier version: `test_procedure_results.py` (memoization) fails before the patch, passes after;
  `test_agent_loop.py::test_procedure_meter_counts_calls_that_return_false` passes.
- `compare_krrood_rerun.py` on the stored KRROOD run: 0 differing actions and digests, median step 89.6 ms,
  can_reach 1,124 calls per step (median).
- Paper builds (`latexmk -pdf main.tex`); main text ends on page 9 (about 40 column lines over).
- Formalization builds with `unification_proofs.tex`, no undefined references.
- Not run: the listing tests of the supplement (they need the bundle's current-version env and data).
