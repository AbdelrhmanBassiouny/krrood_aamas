# ORMatic's translation of the 18 OWL2Bench queries

Data: the OWL 2 RL closure of OWL2Bench (one university) computed by GraphDB, the pre-reasoned input of the experiments, restricted to the classes and properties of owl2bench_translation_model.py and stored by ORMatic in postgresql

Selection: iris

| Query | Translated | = EQL | = GraphDB | Answers | Translated SQL [ms] | Hand-written SQL, paper [ms] | evaluate [ms] |
|---|---|---|---|---|---|---|---|
| Q2 | yes | yes | yes | 7421 | 3.07 | 1.73 | 13.40 |
| Q3 | yes | yes | yes | 55 | 0.71 | 0.04 | 1.14 |
| Q4 | yes | yes | yes | 2486 | 1.02 | 1.52 | 4.50 |
| Q5 | yes | yes | yes | 20 | 0.42 | 0.10 | 0.68 |
| Q7 | yes | yes | yes | 1684 | 1.23 | 0.65 | 3.76 |
| Q8 | yes | yes | yes | 6 | 0.69 | 0.04 | 1.04 |
| Q9 | yes | yes | yes | 0 | 0.18 | 0.23 | 0.59 |
| Q10 | yes | yes | yes | 666 | 0.90 | 0.23 | 2.16 |
| Q11 | yes | yes | yes | 2422 | 1.63 | 0.57 | 5.23 |
| Q12 | yes | yes | yes | 2494 | 1.21 | 8.50 | 1.43 |
| Q13 | yes | yes | yes | 0 | 0.06 | 0.59 | 0.24 |
| Q14 | yes | yes | yes | 0 | 0.07 | 0.12 | 0.44 |
| Q15 | yes | yes | yes | 21 | 0.31 | 0.10 | 0.68 |
| Q16 | yes | yes | yes | 21 | 0.19 | 0.09 | 0.56 |
| Q19 | yes | yes | yes | 858 | 0.62 | 2.17 | 0.93 |
| Q20 | yes | yes | yes | 1311932 | 637.62 | 1,102.17 | 4,456.82 |
| Q21 | yes | yes | yes | 145 | 0.72 | 5.45 | 1.84 |
| Q22 | yes | yes | yes | 106 | 2.03 | 8.45 | 2.97 |

Translated: 18/18; equal to EQL: 18/18; equal to GraphDB: 18/18.
