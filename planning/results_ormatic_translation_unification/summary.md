# ORMatic's translation of the 18 OWL2Bench queries

Data: the OWL 2 RL closure of OWL2Bench (one university) computed by GraphDB, the pre-reasoned input of the experiments, restricted to the classes and properties of owl2bench_translation_model.py and stored by ORMatic in postgresql

Selection: iris

| Query | Translated | = EQL | = GraphDB | Answers | Translated SQL [ms] | Hand-written SQL, paper [ms] | evaluate [ms] |
|---|---|---|---|---|---|---|---|
| Q2 | yes | yes | yes | 7421 | 3.16 | 1.73 | 13.69 |
| Q3 | yes | yes | yes | 55 | 0.63 | 0.04 | 1.12 |
| Q4 | yes | yes | yes | 2486 | 1.02 | 1.52 | 4.62 |
| Q5 | yes | yes | yes | 20 | 0.40 | 0.10 | 0.70 |
| Q7 | yes | yes | yes | 1684 | 1.26 | 0.65 | 3.93 |
| Q8 | yes | yes | yes | 6 | 0.69 | 0.04 | 1.13 |
| Q9 | yes | yes | yes | 0 | 0.17 | 0.23 | 0.58 |
| Q10 | yes | yes | yes | 666 | 0.80 | 0.23 | 2.09 |
| Q11 | yes | yes | yes | 2422 | 1.67 | 0.57 | 5.33 |
| Q12 | yes | yes | yes | 2494 | 1.21 | 8.50 | 1.47 |
| Q13 | yes | yes | yes | 0 | 0.10 | 0.59 | 0.32 |
| Q14 | yes | yes | yes | 0 | 0.12 | 0.12 | 0.54 |
| Q15 | yes | yes | yes | 21 | 0.40 | 0.10 | 0.82 |
| Q16 | yes | yes | yes | 21 | 0.28 | 0.09 | 0.69 |
| Q19 | yes | yes | yes | 858 | 0.71 | 2.17 | 1.07 |
| Q20 | yes | yes | yes | 1311932 | 654.16 | 1,102.17 | 4,602.05 |
| Q21 | yes | yes | yes | 145 | 0.67 | 5.45 | 1.83 |
| Q22 | yes | yes | yes | 106 | 2.08 | 8.45 | 3.03 |

Translated: 18/18; equal to EQL: 18/18; equal to GraphDB: 18/18.
