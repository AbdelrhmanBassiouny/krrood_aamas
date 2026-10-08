# ORMatic's translation of the 18 OWL2Bench queries

Data: the OWL 2 RL closure of OWL2Bench (one university) computed by GraphDB, the pre-reasoned input of the experiments, restricted to the classes and properties of owl2bench_translation_model.py and stored by ORMatic in postgresql

Selection: identifiers

| Query | Translated | = EQL | = GraphDB | Answers | Translated SQL [ms] | Hand-written SQL, paper [ms] | evaluate [ms] |
|---|---|---|---|---|---|---|---|
| Q2 | yes | yes | yes | 7421 | 1.73 | 1.73 | 12.37 |
| Q3 | yes | yes | yes | 55 | 0.06 | 0.04 | 0.38 |
| Q4 | yes | yes | yes | 2486 | 0.66 | 1.52 | 4.15 |
| Q5 | yes | yes | yes | 20 | 0.06 | 0.10 | 0.22 |
| Q7 | yes | yes | yes | 1684 | 0.46 | 0.65 | 2.90 |
| Q8 | yes | yes | yes | 6 | 0.07 | 0.04 | 0.27 |
| Q9 | yes | yes | yes | 0 | 0.21 | 0.23 | 0.56 |
| Q10 | yes | yes | yes | 666 | 0.20 | 0.23 | 1.30 |
| Q11 | yes | yes | yes | 2422 | 0.65 | 0.57 | 4.15 |
| Q12 | yes | yes | yes | 2494 | 0.63 | 8.50 | 0.78 |
| Q13 | yes | yes | yes | 0 | 0.05 | 0.59 | 0.16 |
| Q14 | yes | yes | yes | 0 | 0.04 | 0.12 | 0.16 |
| Q15 | yes | yes | yes | 21 | 0.13 | 0.10 | 0.46 |
| Q16 | yes | yes | yes | 21 | 0.13 | 0.09 | 0.45 |
| Q19 | yes | yes | yes | 858 | 0.28 | 2.17 | 0.39 |
| Q20 | yes | yes | yes | 1311932 | 455.57 | 1,102.17 | 4,268.32 |
| Q21 | yes | yes | yes | 145 | 0.38 | 5.45 | 1.28 |
| Q22 | yes | yes | yes | 106 | 0.61 | 8.45 | 1.28 |

Translated: 18/18; equal to EQL: 18/18; equal to GraphDB: 18/18.
