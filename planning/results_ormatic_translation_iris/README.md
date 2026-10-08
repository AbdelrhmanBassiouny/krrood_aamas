# ORMatic's translation of the 18 OWL2Bench queries, selecting IRIs (8 October 2026)

This run repeats `../results_ormatic_translation_fast/` with the translation returning the IRI of every answer
instead of its database id. All 18 translations return the same answers as EQL in working memory and as GraphDB in
the paper's run, compared directly as IRIs, without mapping database ids. Reading the IRIs costs one join of
`ThingDAO` per selected variable. The geometric mean is 0.83 ms, against 0.33 ms when ids are selected and 0.75 ms for
the hand-written SQLAlchemy queries of the paper's run.

## What changed in the translator

The translator is in `krrood/src/krrood/ormatic/eql_interface.py` of the branch `aamas27-fast-translation`. The commit
`f083e650c4` follows the translator of the previous run (`20f6990f69`), and this run used it.

`eql_to_sql(query, session, select_identifiers=True, identifying_attribute="uri")` returns every selected variable and
flattened collection as the value of the named attribute instead of its database id. Without the keyword, the
translation is unchanged. The new option adds no new rule. The attribute is read with the existing column rule:

- **One table per column.** The column is read by joining, on the id, only the table of the class hierarchy that
  declares it. For `uri`, that table is `ThingDAO`, not `SymbolDAO`, `ThingDAO` and `PersonDAO`. Each selected variable
  gets its own alias of `ThingDAO`.
- **Roles.** A role (Student, Faculty, T20CricketFan, LeisureStudent) has no IRI of its own. Its IRI is read through
  its role taker, as for any attribute of a role. The table that declares `_role_taker_id` is joined if the variable
  is not already bound to it, and the rows whose role taker is not set are dropped. The query's conditions are
  translated as before, on ids.

The translator rejects three cases:

- A selected reference such as `entity(s.role_taker)`, whose column holds a database id. A variable bound to the
  referenced objects must be selected instead.
- An identifying attribute given without `select_identifiers`.
- An identifying attribute that the class does not have (`MissingColumnError`).

`DISTINCT` now applies to the selected IRIs. This matches `distinct(c.uri)` (Q9), `distinct(p.uri)` (Q12) and
`distinct(s.uri, c.uri)` (Q22) more closely than distinct ids do. No query returns duplicate rows: raw rows equal
answers for all 18.

## Translated SQL

The statements are in `ormatic_translation.json`. Compared with the previous run, every statement joins one `ThingDAO`
alias per selected variable or element. Typical shapes:

- **Q2, Q3, Q7, Q8, Q10, Q20.** The association table joined twice with `ThingDAO`, on its source and on its target
  column, for example `SELECT t1.uri, t2.uri FROM <association> a JOIN "ThingDAO" t1 ON t1.database_id =
  a._source_id JOIN "ThingDAO" t2 ON t2.database_id = a._target_id`. Q20 also keeps its `PersonDAO` join, which
  restricts the subject to persons.
- **Q11.** The element is a Faculty role. It joins `EmployeeDAO`, the table that declares `_role_taker_id`, and then
  `ThingDAO` on the role taker.
- **Q4, Q12, Q13, Q15, Q16.** The class's own table joined with `ThingDAO` on its id. Q15 and Q16 keep their `EXISTS`
  over the association table. Q4 still reads `has_age` from `PersonDAO`.
- **Q5, Q19, Q14 (roles).** Q5: `T20CricketFanDAO` joined with `ThingDAO` on `_role_taker_id`, with no other table.
  Q19: `FacultyDAO`, `EmployeeDAO` and `ThingDAO`. Q14: `LeisureStudentDAO`, `StudentDAO` (the role taker, itself a
  role) and `ThingDAO`.
- **Q9.** The `has_college_discipline` association table, with `ThingDAO` joined for the discipline's `uri` (as
  before) and a second `ThingDAO` for the college's IRI.
- **Q21.** The `is_student_of` association table joined with `StudentDAO` and two `ThingDAO` aliases (the student's
  taker and the organization). The same single EXISTS as before.
- **Q22.** `SELECT DISTINCT` over the join of the `has_dean`, `teaches_course` and `takes_course` association tables,
  plus `StudentDAO` (role taker), `ThingDAO` for the student's taker and `ThingDAO` for the course. There is still no
  EXISTS.

## Result

| Query | Answers | = EQL | = GraphDB | Translated, ids (previous run) [ms] | Translated, IRIs [ms] | Hand-written, paper [ms] | evaluate, IRIs [ms] |
|---|---|---|---|---|---|---|---|
| Q2 | 7,421 | yes | yes | 1.73 | 3.07 | 1.73 | 13.40 |
| Q3 | 55 | yes | yes | 0.06 | 0.71 | 0.04 | 1.14 |
| Q4 | 2,486 | yes | yes | 0.66 | 1.02 | 1.52 | 4.50 |
| Q5 | 20 | yes | yes | 0.06 | 0.42 | 0.10 | 0.68 |
| Q7 | 1,684 | yes | yes | 0.46 | 1.23 | 0.65 | 3.76 |
| Q8 | 6 | yes | yes | 0.07 | 0.69 | 0.04 | 1.04 |
| Q9 | 0 | yes | yes | 0.21 | 0.18 | 0.23 | 0.59 |
| Q10 | 666 | yes | yes | 0.20 | 0.90 | 0.23 | 2.16 |
| Q11 | 2,422 | yes | yes | 0.65 | 1.63 | 0.57 | 5.23 |
| Q12 | 2,494 | yes | yes | 0.63 | 1.21 | 8.50 | 1.43 |
| Q13 | 0 | yes | yes | 0.05 | 0.06 | 0.59 | 0.24 |
| Q14 | 0 | yes | yes | 0.04 | 0.07 | 0.12 | 0.44 |
| Q15 | 21 | yes | yes | 0.13 | 0.31 | 0.10 | 0.68 |
| Q16 | 21 | yes | yes | 0.13 | 0.19 | 0.09 | 0.56 |
| Q19 | 858 | yes | yes | 0.28 | 0.62 | 2.17 | 0.93 |
| Q20 | 1,311,932 | yes | yes | 455.57 | 637.62 | 1,102.17 | 4,456.82 |
| Q21 | 145 | yes | yes | 0.38 | 0.72 | 5.45 | 1.84 |
| Q22 | 106 | yes | yes | 0.61 | 2.03 | 8.45 | 2.97 |
| Geometric mean | | | | 0.33 | 0.83 | 0.75 | |

"Translated, ids" is the median of `../results_ormatic_translation_fast/`. "Hand-written, paper" is the median of the
hand-written SQLAlchemy queries in the paper's query run (`queries_sqlalchemy.json`). Times are medians of 10 runs
without the first. `execute` is `session.execute(statement).all()` after `expunge_all`, measured as the hand-written
queries are. `evaluate` is `eql_to_sql(query, session, select_identifiers=True, identifying_attribute="uri").evaluate()`
and includes the translation. The returned IRIs are compared as they are with GraphDB's answer files and with EQL's
answers normalised to IRIs. The script raises an error if a translation returns a database id.

Selecting IRIs makes 17 of the 18 statements slower. Q9 is the exception: it returns no rows. Q2, Q3, Q8, Q10 and Q22
are the most affected:

- **Q3 and Q8** (55 and 6 rows): 0.06 ms rise to 0.7 ms. PostgreSQL plans one of the two `ThingDAO` joins as a
  sequential scan of its 3,462 rows. `EXPLAIN ANALYZE` of Q3 shows 0.28 ms planning and 0.28 ms execution.
- **Q20:** from 456 ms to 638 ms, because 2.6 million IRIs are read and transferred instead of ids. It is still faster
  than the hand-written query (1,102 ms), which reads ids only.
- **Q22:** from 0.61 ms to 2.03 ms, for the joins of `StudentDAO` and two `ThingDAO` aliases.

With `planning/query_summary.py` (the run's `queries` directory and this `ormatic_translation.json`), the translated
SQL is fastest on 14 of the 18 queries. It was fastest on all 18 in the ids run. EQL is faster on Q3 (0.70 against
0.71 ms), Q5 (0.33 against 0.42 ms) and Q8 (0.49 against 0.69 ms). GraphDB is faster on Q22 (1.34 against 2.03 ms).
The translated SQL is faster than the hand-written queries on 9 of the 18 queries: Q4, Q9, Q12, Q13, Q14, Q19, Q20,
Q21 and Q22. Six of these nine are the queries whose hand-written versions build data access objects. Its geometric
mean is 0.83 ms, against 0.75 ms for the hand-written queries.

## How it was run

The run used `scripts/aamas27/ormatic_translation/run_ormatic_translation.py` in `krrood_experiments` (branch
`aamas27-review6`, commit `20aed7b`). That commit adds `--selection iris`, which calls `eql_to_sql(...,
select_identifiers=True, identifying_attribute="uri")`, compares the returned IRIs directly, and records
`identifying_attribute` in the report. The image was `krrood-aamas27-dev` with the worktree's `krrood/src` (at
`f083e650c4`) first on `PYTHONPATH` (SQLAlchemy 2.1.3, Python 3.12.3).

The database was PostgreSQL 18.1 (image `postgres:18.1`), in a new container `ormatic-postgres` on the network
`ormatic-net` with 6 GB of memory and the same flags as the previous run (`--cpuset-cpus=2-15 --memory=6g
--shm-size=512m`). The previous run's container had been removed, so the database was rebuilt in this run: to_dao
9.9 s, commit 47.1 s (previous run: 9.9 s and 47.4 s). Both containers were pinned to CPUs 2-15 of the i7-13700.

```
docker run --rm --network ormatic-net --cpuset-cpus=2-15 --user 1000:1000 --entrypoint bash \
  -v ~/Projects/krrood_experiments:/work -v <scratch>:/s -v <worktree>/krrood/src:/cram_src:ro \
  -v ~/krrood-aamas27-final/krrood-aamas27-supplement/state:/closure:ro \
  -v ~/Projects/krrood_aamas/planning/results/aamas27/run:/paper_run:ro \
  -e HOME=/tmp -e OUT=/s/out_final krrood-aamas27-dev /s/run.sh --selection iris \
  --translator-commit f083e650c4868ee26cecdb1dc53d2261d80a9ad2
```

`run.sh` is the previous run's script, unchanged. It puts `/cram_src` first on `PYTHONPATH`, links psycopg2 from the
image's earlier environment, and runs the script with `--reasoned-file /closure/owl2bench_statements_reasoned.rdf
--reference-answers /paper_run/check/answers/graphdb --paper-sqlalchemy-times
/paper_run/queries/queries_sqlalchemy.json` and the same statements cache.

A check run on Q2, Q5, Q9, Q14, Q19, Q21 and Q22 (2 repetitions) preceded the final run, with the same results. The
final run rebuilt the database again.

## Conditions compared with the previous runs

- **Same as the ids run:** the closure, the reference answers, the stored model (`owl2bench_translation_model.py`),
  the image, PostgreSQL 18.1 with 6 GB, CPUs 2-15, the measurement and the 10 repetitions.
- **Machine load:** besides the run's two containers, the machine ran only desktop applications (PyCharm, Chrome) and
  an idle PostgreSQL container `krrood-aamas27-postgres-1` of another setup (about 5% of one CPU, not started or
  stopped for this run). The load average was 0.5 to 0.9 before the run and 1.25 after the 18 queries.
- **Database rebuilt in a new container** with the same image and flags. The ids run had also rebuilt its database.
- **Compared with the hand-written queries:** all of them select ids or data access objects, never IRIs alone. The
  eleven that select id columns (Q2, Q3, Q4, Q7, Q8, Q9, Q10, Q11, Q15, Q16, Q20) do less work than the IRI translation,
  which joins `ThingDAO` once per selected variable. The seven that select data access objects (Q5, Q12, Q13, Q14,
  Q19, Q21, Q22) build ORM objects, which include the IRI, and the translation does not. The other differences listed
  in `../results_ormatic_translation_fast/README.md` (schema, KRROOD and SQLAlchemy versions) apply unchanged.

## The translator's own tests

`translator_tests.log` holds the run of `test/krrood_test/test_ormatic/` before the change (at `20f6990f69`) and
after it (at `f083e650c4`). Both runs used the image's current environment plus `omegaconf`, `ruff` and
`pytest-xdist`, with `krrood/src` and `test/krrood_test` only, pinned to CPUs 2-15.

- **Before:** 304 passed, 1 expected failure.
- **After:** 315 passed, 1 expected failure (11 new tests).

The new tests are at the end of `test_eql_identifier_selection.py` and use `identifying_attribute="name"` on the
academy dataset. They check:

- That the answers equal the id-based answers mapped to names, for the shapes of Q2, Q20 (a subclass variable
  restricted by its own table), Q5/Q19 (a role read through its role taker), Q9 (an entity with a condition), Q4 (a
  selected value), Q22 (membership as a join in a distinct query, still without EXISTS) and Q21 (one EXISTS over
  nested collections).
- The SQL shape: only the declaring table is joined, one alias per variable, and no `SymbolDAO`.
- That the three rejections above raise.

The existing tests pass unchanged.
