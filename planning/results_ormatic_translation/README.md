# ORMatic's translation of the 18 OWL2Bench queries (8 October 2026)

What the paper's Section 6 states: the translations of all 18 benchmark queries return the same answers as EQL. Run by
`scripts/aamas27/ormatic_translation/run_ormatic_translation.py` (see its docstring) with the current version of
KRROOD, whose `krrood.ormatic.eql_interface.eql_to_sql` the paper describes (the supplement's `code/current`).

## Data

The OWL 2 RL closure of OWL2Bench with one university that GraphDB computed: the pre-reasoned input of the
experiments. This is the file the final reproduction run exported, because `resources/owl2bench_statements_reasoned.rdf`
in this repository predates the `T20CricketFan` axiom and has no T20CricketFan memberships. From the closure, the
script builds the objects of `owl2bench_translation_model.py`, which is the model of the paper's ORMatic listing with
string ages. The script reads 3,664 typed individuals and 1,338,232 statements of the model's 16 properties, and
builds 5,329 objects:

- 3,462 objects of 3,455 individuals. The 7 research groups that the closure also makes persons each get a second
  object, a Person, as Ontomatic gives it.
- 1,867 roles: 989 Student, 858 Faculty and 20 T20CricketFan.

No statement was dropped. ORMatic stored the objects in PostgreSQL 18.1: 23 s to convert them, 103 s to commit.

## Result

All 18 queries were translated. On every query, the answer set of the translation equals that of EQL in working
memory and GraphDB's answer set of the paper's run (`summary.md`, `ormatic_translation.json`).

Rewrites:
- Every query is written in the current EQL syntax: `variable_from` over a collection is now `flat_variable`.
- Q21: `exists_on(so, condition)` of the earlier version is now `exists(cd, condition)`.

Two behaviours of the translator showed up:
- **Database ids for objects.** When a `set_of` selects a variable together with one of its attributes (Q4), the
  translation returns the variable's database id instead of its data access object. The script maps the id to the IRI.
- **Eager loading.** The generated interface loads every relationship eagerly (`selectin`), so loading one answer
  loads everything reachable from it, here the whole benchmark. A first attempt spent more than 10 minutes on Q2.
  The answers and times were therefore taken with `lazyload('*')` added to the translated statement. The interface of
  the query experiment loads lazily.

## Time

The translated statements are slower than the hand-written SQLAlchemy queries of the paper's run on every query.
Their geometric mean is 10.9 ms against 0.75 ms, 14.6 times as high. Q22 takes 446 ms against 8.5 ms, and Q20
8.9 s against 1.1 s.

The two are not measured under equal conditions:
- **Columns and tables.** Several hand-written queries read only the association table or selected columns (Q3, for
  example, reads the `is_part_of` association table alone). The translation loads the data access objects through
  their joined-inheritance tables (`SymbolDAO`, `ThingDAO`, `PersonDAO`, ...).
- **Schema.** The schemas differ: the earlier generated model against this one.
- **Cores.** This run used cores 16-23 of the i7-13700, which are efficiency cores, while other experiments ran on
  the machine.

The translation was written for correctness, not speed. Its times show that it is usable.

## The translator's own tests

`test/krrood_test/test_ormatic/test_eql_collections.py` in the repository of the code's version (the
supplement's `code/current`) checks OWL2Bench query shapes (Q9, Q15, Q21, Q22) on a small academy
dataset. Run with the image's current environment, plus `omegaconf` and `ruff`, which the tests need: 26 passed and
1 expected failure (`translator_tests.log`).

The expected failure is a known limitation. Without a collection between them, two variables of one class share a
table unless an equality relates them, so comparing them by value compares a row with itself. None of the 18 queries
has this shape.
