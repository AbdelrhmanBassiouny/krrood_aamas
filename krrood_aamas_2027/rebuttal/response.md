# Author response, AAMAS 2027 submission 1481

Each section below is one OpenReview reply, at most 2500 characters. Post each under its review; there is no general reply. Check lengths with `python3 count.py` before posting.

---

## To Reviewer HKHa

We thank the reviewer for the careful reading and the constructive questions.

W1. Answering the question of what unifying the program and the knowledge base buys, we mean two things. First, reflection: queries, rules and planner calls are objects of the same program as the domain knowledge, so the agent can ask, e.g., which rules derive T20CricketFan. This is in the spirit of Newell's knowledge level; a separate store would need a second meta-model. Second, no synchronization: with GraphDB, deciding in SPARQL writes 405 values per step instead of 4 (Section 7.4). OWL stays the standard: Ontomatic compiles it into the program and preserves its entailments. We agree that the paper does not show reflection concretely, so we will add a listing in which the agent queries its own queries, rules and planner calls with EQL.

W2. It seems that our semantic claim was not clear, and we want to clarify it. Every answer of a positive query is a certain answer, and under Proposition 5.2's conditions all are returned, so these answers equal the open-world ones. Only negation and aggregates are closed-world. We will state in the introduction that we claim certain answers of positive queries, not open-world reasoning. Open-world negation is a research problem of its own, which we name as future work.

W3. We agree that the effect of step 5 should be visible, so we will report loading with step 5 disabled. We would keep the benchmark, since OWL2Bench's RL profile tests exactly the fragment our claims cover.

W4. Answering the question regarding retraction, we mean three kinds of fact. Computed predicates are recomputed per query, and reassigned attributes replace old values, so neither becomes stale. Only facts derived by property rules are not retracted (Section 8). We will state explicitly which facts can become stale, and name retraction of rule-derived facts as future work.

---

## To Reviewer 7FxR

We thank the reviewer for the thorough review.

We agree with the main concern, so we will use one pinned release for all listings, proofs and experiments, and rerun all of them. A rerun counts only if the closure again equals GraphDB's and Nemo's, and every answer set equals GraphDB's. Footnotes 2 and 3 and the earlier equality clause go, and Corollary 1's proof is rewritten. As suggested, the space comes from Section 3 and the contribution list.

We also agree that the proofs should be checkable from the main text, so we will add a short sketch with the key invariant for each result there.

A. It seems that step 5 read as specific to the benchmark; we want to clarify that it is exact and general: for any symmetric and transitive property, the closure relates exactly the members of each weakly connected component. RDFox treats owl:sameAs the same way. We therefore keep step 5, and we will report loading with step 5 disabled next to the main results, so its effect can be seen.

B. We agree that the agent-loop claim should match the experiment, so we will scope it to what it measures, namely the synchronization a second world model adds and that decisions agree in every step.

---

## To Reviewer sSAi

We thank the reviewer for the helpful comments on the presentation. We agree with them and will change the paper accordingly.

We agree that the related systems should appear earlier, so we will cite GraphDB, Nemo and Owlready2 in the introduction.

It seems that our novelty was not stated clearly enough, so we will clarify it in a paragraph tied to Table 1: KRROOD is, to our knowledge, the first framework where terminology, assertions, OWL 2 RL inference, a query language whose predicates are the agent's own procedures, and long-term memory share one object model.

We agree that Section 3's itemized definitions read poorly, so we will rewrite them as full sentences, and we will fix the "1.42 million" sentence.

We also agree that the title is too broad and will narrow it, e.g. "KRROOD: The Agent's Object-Oriented Program as Its Knowledge Base".

---

## To Reviewer MnFm

We thank the reviewer for the detailed technical questions.

Closed world and unique names. It seems that the scope of our claims was not clear, and we want to clarify it. For positive queries, every answer is a certain answer (Proposition 5.1), and under our conditions all are returned (Corollary 1). A check after loading reports any applicable equality rule; on OWL2Bench there is none, so no answer is lost. We agree that these conditions belong up front, so we will state them in the introduction, not only in Section 8.

Step 5. Answering the question whether step 5 bypasses reasoning: it does not. It is exact for every symmetric and transitive property in any ontology. To make this visible, we will report loading with step 5 disabled.

Joins. Answering the question regarding join-heavy queries, we mean the SQL path for them: there, the same EQL query is fastest on 14 of 18 queries, with the same answers (Theorem 6.1). A query planner for working memory is future work.

Punning. The 47 punned IRIs place OWL2Bench just outside our conditions, yet all results equal GraphDB's.

Benchmark. We would keep OWL2Bench, since its RL profile tests exactly the fragment our propositions cover; LUBM, for example, is outside OWL 2 RL.

References. We agree, and will add Do et al. (2018) and trim references the argument does not need. We would not add Nguyen et al. (2025), since it concerns embeddings and multi-agent consultation, not object-oriented knowledge representation.
