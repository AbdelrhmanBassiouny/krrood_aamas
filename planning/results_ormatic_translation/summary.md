# ORMatic's translation of the 18 OWL2Bench queries

Data: the OWL 2 RL closure of OWL2Bench (one university) computed by GraphDB, the pre-reasoned input of the experiments, restricted to the classes and properties of owl2bench_translation_model.py and stored by ORMatic in postgresql

| Query | Translated | = EQL | = GraphDB | Answers | Translated SQL [ms] | Hand-written SQL, paper [ms] | evaluate [ms] |
|---|---|---|---|---|---|---|---|
| Q2 | yes | yes | yes | 7421 | 75.16 | 1.73 | 93.31 |
| Q3 | yes | yes | yes | 55 | 16.24 | 0.04 | 18.11 |
| Q4 | yes | yes | yes | 2486 | 2.49 | 1.52 | 8.01 |
| Q5 | yes | yes | yes | 20 | 0.85 | 0.10 | 0.98 |
| Q7 | yes | yes | yes | 1684 | 33.59 | 0.65 | 39.14 |
| Q8 | yes | yes | yes | 6 | 12.68 | 0.04 | 14.24 |
| Q9 | yes | yes | yes | 0 | 3.52 | 0.23 | 4.91 |
| Q10 | yes | yes | yes | 666 | 18.21 | 0.23 | 20.76 |
| Q11 | yes | yes | yes | 2422 | 32.70 | 0.57 | 39.85 |
| Q12 | yes | yes | yes | 2494 | 39.74 | 8.50 | 39.39 |
| Q13 | yes | yes | yes | 0 | 0.72 | 0.59 | 0.79 |
| Q14 | yes | yes | yes | 0 | 0.25 | 0.12 | 0.32 |
| Q15 | yes | yes | yes | 21 | 3.45 | 0.10 | 3.75 |
| Q16 | yes | yes | yes | 21 | 0.88 | 0.09 | 1.09 |
| Q19 | yes | yes | yes | 858 | 4.33 | 2.17 | 4.42 |
| Q20 | yes | yes | yes | 1311932 | 8,886.77 | 1,102.17 | 14,557.48 |
| Q21 | yes | yes | yes | 145 | 6.02 | 5.45 | 11.03 |
| Q22 | yes | yes | yes | 106 | 446.07 | 8.45 | 450.46 |

Translated: 18/18; equal to EQL: 18/18; equal to GraphDB: 18/18.
