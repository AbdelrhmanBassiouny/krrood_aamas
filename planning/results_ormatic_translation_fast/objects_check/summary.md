# ORMatic's translation of the 18 OWL2Bench queries

Data: the OWL 2 RL closure of OWL2Bench (one university) computed by GraphDB, the pre-reasoned input of the experiments, restricted to the classes and properties of owl2bench_translation_model.py and stored by ORMatic in postgresql

Selection: objects

| Query | Translated | = EQL | = GraphDB | Answers | Translated SQL [ms] | Hand-written SQL, paper [ms] | evaluate [ms] |
|---|---|---|---|---|---|---|---|
| Q2 | yes | yes | yes | 7421 | 99.30 | 1.73 | 56.31 |
| Q3 | yes | yes | yes | 55 | 9.10 | 0.04 | 9.86 |
| Q4 | yes | yes | yes | 2486 | 1.67 | 1.52 | 5.14 |
| Q5 | yes | yes | yes | 20 | 0.49 | 0.10 | 0.59 |
| Q7 | yes | yes | yes | 1684 | 28.38 | 0.65 | 27.81 |
| Q8 | yes | yes | yes | 6 | 8.21 | 0.04 | 8.79 |
| Q9 | yes | yes | yes | 0 | 2.59 | 0.23 | 3.66 |
| Q10 | yes | yes | yes | 666 | 12.17 | 0.23 | 13.55 |
| Q11 | yes | yes | yes | 2422 | 18.86 | 0.57 | 23.38 |
| Q12 | yes | yes | yes | 2494 | 22.77 | 8.50 | 22.56 |
| Q13 | yes | yes | yes | 0 | 0.52 | 0.59 | 0.59 |
| Q14 | yes | yes | yes | 0 | 0.25 | 0.12 | 0.32 |
| Q15 | yes | yes | yes | 21 | 2.31 | 0.10 | 2.58 |
| Q16 | yes | yes | yes | 21 | 0.87 | 0.09 | 0.95 |
| Q19 | yes | yes | yes | 858 | 2.60 | 2.17 | 2.63 |
| Q20 | yes | yes | yes | 1311932 | 5,045.14 | 1,102.17 | 8,594.64 |
| Q21 | yes | yes | yes | 145 | 3.95 | 5.45 | 7.31 |
| Q22 | yes | yes | yes | 106 | 272.17 | 8.45 | 277.63 |

Translated: 18/18; equal to EQL: 18/18; equal to GraphDB: 18/18.
