# ORMatic's translation of the 18 OWL2Bench queries, selecting identifiers (8 October 2026)

This run repeats `../results_ormatic_translation/` with a translator that selects database ids and joins only the
tables a query needs. All 18 translations return the same answers as EQL in working memory and as GraphDB in the
paper's run. Their statements are now faster than the hand-written SQLAlchemy queries of the paper's run: the
geometric mean is 0.33 ms, against 0.75 ms for the hand-written queries and 10.95 ms in the first
run.

## What changed in the translator

The translator is in `krrood/src/krrood/ormatic/eql_interface.py` of the branch `aamas27-fast-translation`, which
starts at the supplement's translator (`3308cb252f`, branch `fix/eql-to-sql-collections`). The commits are
`aa8e9299a3` (identifier selection and join elimination), `67a666b1e2` (references keyed by element identity) and `20f6990f69` (membership joins only for conjuncts of the condition, after a review found that a membership test inside `case_when` was joined). The run used `20f6990f69`.

`eql_to_sql(query, session, select_identifiers=True)` translates with the new `IdentifierSelectingTranslator`. Without
the keyword, the translation selects data access objects as before; the paper's ORMatic listing test passes
unchanged. The new translation follows four rules.

1. **Identifiers.** Every selected variable and flattened collection is returned as its database id, the identity of
   the answer, and a selected attribute as its column. No data access object is built.
2. **Foreign keys stand for variables.** A variable or element is the column that already holds its id. The element
   of a collection is the target column of the association table. A variable whose first use ranges over one of its
   collections is the source column of that table. For example, `an(set_of(p, flat_variable(p.is_member_of)))` becomes
   `SELECT source_id, target_id FROM association`. A reference is its foreign key column.
3. **Tables only where needed.** A column is read by joining, on the id, only the table of the class hierarchy that
   declares it. For example, `uri` is read from `ThingDAO` alone, not from the whole chain `SymbolDAO`, `ThingDAO`,
   `PersonDAO`. A foreign key also restricts the class of the rows it refers to. A variable of class C needs no join
   when its foreign key references the table of C or of a subclass of C. When the key references the table of a
   superclass, C's own table is joined on the id. Q20 is such a case: `has_same_home_town_with` is declared on Thing,
   so `PersonDAO` is joined.
4. **Joins for membership and for existential quantifiers.** In a query that returns distinct answers, a membership
   test `contains(v.collection, c)` among the conditions that all answers satisfy, for a variable `v` that is not yet
   bound, joins the association table on its target column and binds `v` to its source column (Q22). An existential
   quantifier over a chain of collections becomes one correlated EXISTS subquery that joins the collection tables
   (Q21), instead of one nested EXISTS per table.

Every variable ranges over its rows independently, as when the first translation meets a collection. The guards of the
first translation apply unchanged. A join that would restrict rows inside `or_`, `not_` or an existential quantifier
is rejected, as are inference rules, domain objects without a database identity, and comparisons of unrelated classes.
A join that only reads a column of a bound variable on its id never restricts rows, so it is always allowed. Grouped
queries and selected aggregates are rejected in this mode. The translation relies on the foreign keys of the schema.

## Translated SQL

The statements are in `ormatic_translation.json`. Typical shapes:

- Q2, Q3, Q7, Q8, Q10, Q11: `SELECT a._source_x_id, a._target_y_id FROM <association> AS a`.
- Q4, Q5, Q12, Q13, Q14, Q19: the class's own table only, for example `SELECT p.database_id, p.has_age FROM "PersonDAO" AS p WHERE ...`.
- Q9: the association table joined with `ThingDAO` for `uri`.
- Q15, Q16: the class's own table with `EXISTS` over the association table.
- Q20: the association table joined with `PersonDAO`, which restricts the variable to persons.
- Q21: the `is_student_of` association table with one EXISTS that joins `is_part_of`, `has_college_discipline` and
  `ThingDAO`.
- Q22: `SELECT DISTINCT` over the join of the `has_dean`, `teaches_course` and `takes_course` association tables.

## Result

| Query | Answers | = EQL | = GraphDB | Translated, objects (first run) [ms] | Translated, identifiers [ms] | Hand-written, paper [ms] | evaluate, identifiers [ms] |
|---|---|---|---|---|---|---|---|
| Q2 | 7,421 | yes | yes | 75.16 | 1.73 | 1.73 | 12.37 |
| Q3 | 55 | yes | yes | 16.24 | 0.06 | 0.04 | 0.38 |
| Q4 | 2,486 | yes | yes | 2.49 | 0.66 | 1.52 | 4.15 |
| Q5 | 20 | yes | yes | 0.85 | 0.06 | 0.10 | 0.22 |
| Q7 | 1,684 | yes | yes | 33.59 | 0.46 | 0.65 | 2.90 |
| Q8 | 6 | yes | yes | 12.68 | 0.07 | 0.04 | 0.27 |
| Q9 | 0 | yes | yes | 3.52 | 0.21 | 0.23 | 0.56 |
| Q10 | 666 | yes | yes | 18.21 | 0.20 | 0.23 | 1.30 |
| Q11 | 2,422 | yes | yes | 32.70 | 0.65 | 0.57 | 4.15 |
| Q12 | 2,494 | yes | yes | 39.74 | 0.63 | 8.50 | 0.78 |
| Q13 | 0 | yes | yes | 0.72 | 0.05 | 0.59 | 0.16 |
| Q14 | 0 | yes | yes | 0.25 | 0.04 | 0.12 | 0.16 |
| Q15 | 21 | yes | yes | 3.45 | 0.13 | 0.10 | 0.46 |
| Q16 | 21 | yes | yes | 0.88 | 0.13 | 0.09 | 0.45 |
| Q19 | 858 | yes | yes | 4.33 | 0.28 | 2.17 | 0.39 |
| Q20 | 1,311,932 | yes | yes | 8,886.77 | 455.57 | 1,102.17 | 4,268.32 |
| Q21 | 145 | yes | yes | 6.02 | 0.38 | 5.45 | 1.28 |
| Q22 | 106 | yes | yes | 446.07 | 0.61 | 8.45 | 1.28 |
| Geometric mean | | | | 10.95 | 0.33 | 0.75 | |

"Translated, objects (first run)" is the median of `../results_ormatic_translation/`. "Hand-written, paper" is the
median of the hand-written SQLAlchemy queries in the paper's query run (`queries_sqlalchemy.json`). Times are medians of
10 runs without the first. `execute` is `session.execute(statement).all()` after `expunge_all`, measured as the
hand-written queries are. `evaluate` is `eql_to_sql(query, session, select_identifiers=True).evaluate()` and includes
the translation. Ids are mapped to IRIs for the comparison, outside the timing. Q20 has 1.3 million answers. Its
`evaluate` (4.3 s) is dominated by building one answer mapping per row in Python, and its statement by transferring
the rows. Q20 is the only query whose translation must join a class table (`PersonDAO`) that the hand-written query
leaves out. The hand-written query reads the whole association table, whose subjects are not restricted to persons.

## How it was run

`scripts/aamas27/ormatic_translation/run_ormatic_translation.py` in `krrood_experiments` (branch `aamas27-review6`,
uncommitted changes in that directory: `--selection identifiers|objects` with identifiers as default,
`--reuse-database`, `--translator-commit`, and the recording of the selection and versions). The run used the image
`krrood-aamas27-dev` with the worktree's `krrood/src` first on `PYTHONPATH` (SQLAlchemy 2.1.3, Python
3.12.3). The database was PostgreSQL 18.1 (image `postgres:18.1`) in a container with 6 GB of memory. Both containers were pinned to CPUs 2-15
of the i7-13700, and the machine was otherwise idle. The database was rebuilt in this run: to_dao 9.9 s, commit
47.4 s.

```
docker run --rm --network ormatic-net --cpuset-cpus=2-15 --user 1000:1000 --entrypoint bash \
  -v ~/Projects/krrood_experiments:/work -v <scratch>:/s -v <worktree>/krrood/src:/cram_src:ro \
  -v ~/krrood-aamas27-final/krrood-aamas27-supplement/state:/closure:ro \
  -v ~/Projects/krrood_aamas/planning/results/aamas27/run:/paper_run:ro \
  -e HOME=/tmp -e OUT=/s/out_final krrood-aamas27-dev /s/run.sh --translator-commit <commit>
```

`run.sh` puts `/cram_src` first on `PYTHONPATH`, links psycopg2 from the image's earlier environment, and runs the
script with `--reasoned-file /closure/owl2bench_statements_reasoned.rdf --reference-answers
/paper_run/check/answers/graphdb --paper-sqlalchemy-times /paper_run/queries/queries_sqlalchemy.json`.

## Conditions compared with the paper's query run

- **Same:** the OWL 2 RL closure of OWL2Bench (one university), PostgreSQL 18.1, the machine, and the measurement of a
  statement (`session.execute(statement).all()` after `expunge_all`, median of 10 without the first).
- **Different schema:** this run stores the current KRROOD model of the part of OWL2Bench that the queries use
  (`owl2bench_translation_model.py`, generated by the current ORMatic). The paper's run stores the earlier generated
  model of the whole ontology.
- **Different versions:** current KRROOD with SQLAlchemy 2.1.3 here; the earlier KRROOD with SQLAlchemy
  2.0.44 in the paper's run.
- **Different work per query:** the translation selects ids. The hand-written queries Q5, Q12, Q13, Q14 and Q19 select
  data access objects, and Q21 and Q22 select data access objects through joins. They therefore build ORM objects,
  which the translation does not, so on these seven queries part of the difference is that work. The other eleven
  hand-written queries select id columns (and the age in Q4), as the translation does, and the comparison is closest
  there.
- **CPUs:** this run was pinned to CPUs 2-15. The paper's query run is documented in its own `environment.json`.

## The translator's own tests

`translator_tests.log` holds the run of `test/krrood_test/test_ormatic/` before the change (at `3308cb252f`) and after
it (at `20f6990f69`), in the image's current environment plus `omegaconf`, `ruff` and `pytest-xdist`, with
`krrood/src` and `test/krrood_test` only. Before: 264 passed, 1 expected failure. After: 304 passed, 1 expected failure (40 new tests). The new tests are in
`test_eql_identifier_selection.py`. They repeat the query shapes of `test_eql_collections.py` and the shapes of
OWL2Bench Q9, Q15, Q20, Q21 and Q22 with identifiers selected, check the SQL where a join is avoided, and check that
the guards still reject the same constructs. The expected failure is the known limitation of the default translation,
in which variables of one class share a table. The identifier translation does not have this limitation, and a test
checks this.

A check run with `--selection objects` (the default translation, 2 repetitions) also returned answers equal to EQL and
GraphDB for all 18 queries (`objects_check/`).
