# Author response, AAMAS 2027 submission 1481

Each section below is one OpenReview reply, at most 2500 characters. Post each under its review with that review's rebuttal button; there is no general reply. Check lengths with `python3 count.py` before posting.

---

## To Reviewer HKHa

We thank the reviewer for the careful review.

W1. Answering why unifying the two models matters: the agent's procedures take part in reasoning. A query calls the planner as a predicate, and the agent can query its own queries, rules and planner calls, e.g. which rules derive T20CricketFan, in the spirit of Newell's knowledge level. With a separate store, each decision is split by hand into SPARQL and Python and two world models are kept in sync; deciding in SPARQL alone writes 405 values per step instead of 4 (Section 7.4). We agree standard formalisms give modularity and reuse, and KRROOD keeps them: Ontomatic compiles an OWL ontology into the program and preserves its entailments.

W2. We agree losing open-world reasoning would be a big deal; it seems we did not make clear how much is kept. For positive queries, every answer is a certain answer (Proposition 5.1), and under our conditions all certain answers are returned (Corollary 1), so closed- and open-world answers coincide. Only negation and aggregates read the closed world.

W4. We want to clarify the extent of this. Computed predicates are recomputed per query, and reassigned attributes replace their old values, so neither becomes stale. Only facts derived by property rules are not retracted (Section 8).

We will change:

1. W1: add a listing in which the agent queries its own queries, rules and planner calls with EQL.
2. W2: state in the introduction that we claim certain answers of positive queries, not open-world reasoning.
3. W3: report loading with step 5 disabled, so the results do not rest on one property of the benchmark.
4. W4: state which facts can become stale.

We will not change:

- The benchmark. OWL2Bench's RL profile tests exactly the fragment our claims cover, and we compared its whole closure, assertion by assertion, with GraphDB's and Nemo's.
- Open-world negation and retraction of rule-derived facts. We agree both are valuable, but each is a research problem of its own; we name them as future work.

---

## To Reviewer 7FxR

We thank the reviewer for the thorough review and the concrete suggestions.

A. We agree step 5 dominates loading on OWL2Bench, but want to clarify that it is not tied to the benchmark: for any symmetric and transitive property, the closure relates exactly the members of each weakly connected component, so step 5 is exact for every such property in any ontology. RDFox treats owl:sameAs the same way.

We will change:

1. Main concern: we agree, and will pin one release for all listings, proofs and experiments and rerun every experiment, the robot included. A rerun counts only if the closure again equals GraphDB's and Nemo's, and every answer set equals GraphDB's. Footnotes 2 and 3 and the earlier version's equality in Corollary 1 go, so the propositions and Theorem 6.1 apply to the artefact behind the numbers. The space comes from Section 3 and the contribution list, as suggested.
2. Proofs: state the proof strategy and key invariant of Propositions 5.1-5.3 and Corollary 1 in the main text.
3. A: report loading with step 5 disabled next to the main results.
4. B: we agree the scenario is small for a general cost claim, and will scope it to what it measures: the synchronization a second world model adds, and that all builds decide the same in every step.

We will not change:

- Step 5 itself, since it is exact and general (see A).

---

## To Reviewer sSAi

We thank the reviewer, and are glad the running examples help. We agree with all points and will change:

1. Cite GraphDB, Nemo and Owlready2 in the introduction.
2. Strengthen related work by stating, for each group of systems, what KRROOD adds.
3. Novelty: it seems it was not clear, so we will state it in a paragraph tied to Table 1. KRROOD is, to our knowledge, the first framework where terminology, assertions, OWL 2 RL inference, a query language whose predicates are the agent's own procedures, and long-term memory share one object model.
4. Rewrite expressions such as the closed-world definition in Section 3 as full sentences, and check the rest of the paper likewise.
5. Fix the sentence to "1.42 million of which are assertions".
6. Narrow the title, e.g. "KRROOD: The Agent's Object-Oriented Program as Its Knowledge Base".

---

## To Reviewer MnFm

We thank the reviewer. It seems several of our results were not clear, and we want to clarify them.

Closed world and unique names. For positive queries, answers do not contradict OWL: every answer is a certain answer (Proposition 5.1), and under our conditions all are returned (Corollary 1). Unique names are checked, not silently assumed: a check after loading reports every application of an equality rule; on OWL2Bench it reports none, so keeping individuals apart loses no answer.

Step 5. Answering the concern that it is a hardcoded bypass: it is a general rule. For any symmetric and transitive property, the closure relates exactly the members of each weakly connected component, so step 5 is exact in any ontology; RDFox treats owl:sameAs the same way.

Joins. We agree working-memory EQL is slow on some joins (Q22). For those we mean the SQL path: the same EQL query, translated by ORMatic, is fastest on 14 of 18 queries, with the same answers (Theorem 6.1).

Punning. We agree the 47 punned IRIs place OWL2Bench just outside our conditions. This is why we compared the whole closure: it equals GraphDB's and Nemo's assertion by assertion, and every answer set equals GraphDB's.

We will change:

1. State the closed-world and unique-name conditions in the introduction, not only in Section 8.
2. Report loading with step 5 disabled.
3. Add Do et al. (2018) and trim old references the argument does not need.

We will not change:

- The benchmark. OWL2Bench's RL profile tests exactly the fragment our propositions cover.
- Nguyen et al. (2025). It concerns embeddings and multi-agent consultation, not object-oriented knowledge representation.
- A query planner for working memory; we name it as future work.
