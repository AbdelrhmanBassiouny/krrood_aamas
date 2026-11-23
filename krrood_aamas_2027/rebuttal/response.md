# Author response, AAMAS 2027 submission 1481

Each section below is one OpenReview reply, at most 2500 characters. Post each under its review; there is no general reply. Check lengths with `python3 count.py` before posting.

---

## To Reviewer HKHa

We thank the reviewer.

We will change:
1. W1: add a listing in which the agent queries its own queries, rules and planner calls with EQL.
2. W2: state in the introduction that we claim certain answers of positive queries, not open-world reasoning.
3. W3: report loading with step 5 disabled.
4. W4: state which facts can become stale.

We will not change:
- The benchmark. OWL2Bench's RL profile tests exactly the fragment our claims cover.
- Open-world negation and retraction of rule-derived facts. Both are research problems of their own; we name them as future work.

W1. Unifying gives reflection: queries, rules and planner calls are objects of the same program as the domain knowledge, so the agent can ask, e.g., which rules derive T20CricketFan. This is in the spirit of Newell's knowledge level; a separate store needs a second meta-model. It also removes synchronization: with GraphDB, deciding in SPARQL writes 405 values per step instead of 4 (Section 7.4). OWL stays the standard: Ontomatic compiles it into the program and preserves its entailments.

W2. Every answer of a positive query is a certain answer, and under Proposition 5.2's conditions all are returned, so these answers equal the open-world ones. Only negation and aggregates are closed-world.

W4. Computed predicates are recomputed per query, and reassigned attributes replace old values. Only facts derived by property rules are not retracted (Section 8).

---

## To Reviewer 7FxR

We thank the reviewer.

We will change:
1. Main concern: one pinned release for all listings, proofs and experiments, all rerun. A rerun counts only if the closure again equals GraphDB's and Nemo's, and every answer set equals GraphDB's. Footnotes 2 and 3 and the earlier equality clause go, and Corollary 1's proof is rewritten. The space comes from Section 3 and the contribution list, as suggested.
2. Proofs: a short sketch with the key invariant for each result in the main text.
3. A: report loading with step 5 disabled next to the main results.
4. B: scope the agent-loop claim to what it measures, namely the synchronization a second world model adds and that decisions agree in every step.

We will not change step 5 itself. It is exact and general: for any symmetric and transitive property, the closure relates exactly the members of each weakly connected component. RDFox treats owl:sameAs the same way.

---

## To Reviewer sSAi

We thank the reviewer.

We will change:
1. Cite GraphDB, Nemo and Owlready2 in the introduction.
2. Add a novelty paragraph tied to Table 1. KRROOD is, to our knowledge, the first framework where terminology, assertions, OWL 2 RL inference, a query language whose predicates are the agent's own procedures, and long-term memory share one object model.
3. Rewrite Section 3's itemized definitions as full sentences, and fix the "1.42 million" sentence.
4. Narrow the title, e.g. "KRROOD: The Agent's Object-Oriented Program as Its Knowledge Base".

---

## To Reviewer MnFm

We thank the reviewer.

We will change:
1. State the closed-world and unique-name conditions in the introduction, not only in Section 8.
2. Report loading with step 5 disabled.
3. Add Do et al. (2018) and trim references the argument does not need.

We will not change:
- The benchmark. OWL2Bench's RL profile tests exactly the fragment our propositions cover; LUBM, for example, is outside OWL 2 RL.
- Nguyen et al. (2025). It concerns embeddings and multi-agent consultation, not object-oriented knowledge representation.

Closed world and unique names. For positive queries, every answer is a certain answer (Proposition 5.1), and under our conditions all are returned (Corollary 1). A check after loading reports any applicable equality rule; on OWL2Bench there is none, so no answer is lost.

Step 5 is not a bypass. It is exact for every symmetric and transitive property in any ontology.

Joins. On SQL, the same EQL query is fastest on 14 of 18 queries, with the same answers (Theorem 6.1). A query planner for working memory is future work.

Punning. The 47 punned IRIs place OWL2Bench just outside our conditions, yet all results equal GraphDB's.
