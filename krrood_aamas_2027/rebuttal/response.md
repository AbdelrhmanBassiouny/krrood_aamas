# Author response, AAMAS 2027 submission 1481

Each section below is one OpenReview reply, at most 2500 characters. Post each under its review with that review's rebuttal button; there is no general reply. Check lengths with `python3 count.py` before posting.

---

## To Reviewer HKHa

We thank the reviewer for the careful review and for appreciating our formal and scaling results. All four weaknesses concern our central idea, a single world model that keeps OWL's meaning where it matters most.

W1. Unifying the two models matters because the agent's own procedures can then take part in reasoning, and nothing has to be kept in sync. In KRROOD, a query can call the planner as a predicate, and, in the spirit of Newell's knowledge level, the agent can query its own rules, e.g. which of them derive T20CricketFan. With a separate store, each decision is split by hand into SPARQL and Python. In our robot, deciding in SPARQL alone writes 405 values per step instead of 4 (Section 7.4). We agree that standard formalisms make methods modular and reusable, and KRROOD keeps this: Ontomatic compiles an OWL ontology into the program and preserves its entailments.

W2. We agree that losing open-world reasoning would be serious, and it seems we did not make clear how much of it is kept. In general, the closed world only matters where a query asks what is not known, i.e. for negation and aggregates. For positive queries, every answer is a certain answer (Proposition 5.1), and under our conditions all certain answers are returned (Corollary 1), so closed- and open-world answers coincide.

W3. We agree broader evidence would strengthen the claims. We chose OWL2Bench because its RL profile tests exactly the fragment our claims cover, and let us compare its whole closure with GraphDB's and Nemo's. On it, however, one symmetric, transitive property dominates loading, so the results should not rest on step 5 alone, which handles such properties.

W4. Similarly, the extent of non-retraction may not have been clear. Of KRROOD's three kinds of fact, only one can become stale. Computed predicates are recomputed per query and reassigned attributes replace old values; only facts derived by property rules are not retracted (Section 8).

Based on this, we will change:

1. W1: add a listing in which the agent queries its own queries, rules and planner calls.
2. W2: state in the introduction that we claim certain answers of positive queries, not open-world reasoning.
3. W3: report loading with step 5 disabled.
4. W4: state which facts can become stale.

We will not change:

- The benchmark, for the reason given under W3.
- Open-world negation and retraction of rule-derived facts, each a research problem of its own; we name them as future work.

---

## To Reviewer 7FxR

We thank the reviewer for the thorough review, the kind words on the related work, and the concrete suggestions, which we are happy to follow.

Regarding the main concern, we agree that every result must come from the version the paper describes. We will therefore pin one release for all listings, proofs and experiments, and rerun every experiment, the robot included. A rerun counts only if the closure again equals GraphDB's and Nemo's and every answer set equals GraphDB's. Concretely, footnotes 2 and 3 and the earlier version's equality in Corollary 1 are then no longer needed, and the propositions and Theorem 6.1 apply to the artefact behind the numbers. As suggested, the space comes from Section 3 and the contribution list.

Regarding the proofs, we agree that the claims should be assessable from the main text alone, and will state there the proof strategy and key invariant of Propositions 5.1-5.3 and Corollary 1.

Regarding A, we agree that step 5 dominates loading on OWL2Bench. It handles, however, a general class of properties rather than this benchmark: for any symmetric and transitive property, the closure relates exactly the members of each weakly connected component, so step 5 is exact in any ontology, much as RDFox treats owl:sameAs. On OWL2Bench, this class happens to contain hasSameHomeTownWith, which makes up 92% of the closure. To make the general cost visible, we will also report loading with step 5 disabled.

Regarding B, we agree that the scenario is small for a general cost claim, and will scope the claim to what it measures: the synchronization a second world model adds, and that all builds decide the same in every step.

In summary, we will change:

1. One pinned release for everything, with every experiment rerun.
2. Proof strategies and key invariants in the main text.
3. Loading times with step 5 disabled, next to the main results.
4. The agent-loop claim, scoped as above.

We will not change:

- Step 5 itself, since it is exact and general.

---

## To Reviewer sSAi

We thank the reviewer for the helpful comments, and are glad the running examples make the paper easier to read. We agree with all points. Most concern the presentation; the last concerns the novelty, which it seems we did not state clearly. In general, our novelty is that the agent's program is its knowledge base. Concretely, KRROOD is, to our knowledge, the first framework where terminology, assertions, OWL 2 RL inference, a query language whose predicates are the agent's own procedures, and long-term memory share one object model.

We will therefore change:

1. Cite GraphDB, Nemo and Owlready2 in the introduction.
2. Strengthen related work by stating, for each group of systems, what KRROOD adds.
3. Rewrite expressions such as the closed-world definition in Section 3 as full sentences, and check the rest of the paper likewise.
4. Fix the sentence to "1.42 million of which are assertions".
5. State the novelty above in a paragraph tied to Table 1.
6. Narrow the title accordingly, e.g. "KRROOD: The Agent's Object-Oriented Program as Its Knowledge Base".

---

## To Reviewer MnFm

We thank the reviewer for the detailed review. It seems several of our results were not clear, and we would like to clarify them in the order raised.

Regarding the closed-world and unique-name assumptions, KRROOD keeps OWL's meaning wherever a query asks only what is known. Concretely, answers to positive queries do not contradict OWL: every answer is a certain answer (Proposition 5.1), and under our conditions all are returned (Corollary 1). Moreover, unique names are not silently assumed but checked: after loading, a check reports every application of an equality rule. On OWL2Bench it reports none, so keeping individuals apart loses no answer.

Regarding step 5, it is a general rule for a class of properties rather than a hardcoded bypass. For any symmetric and transitive property, the closure relates exactly the members of each weakly connected component, so step 5 is exact in any ontology, much as RDFox treats owl:sameAs. On OWL2Bench, this class contains hasSameHomeTownWith.

Regarding joins, KRROOD evaluates the same EQL query in two ways: in working memory and, translated by ORMatic, in SQL. We agree that working memory is slow on some joins, such as Q22; such queries are what the SQL path is for. There, the same query is fastest on 14 of 18 queries, with the same answers (Theorem 6.1).

Regarding the benchmark, we agree that OWL2Bench lies just outside our conditions, as it uses 47 IRIs both as classes and as individuals. This is why we did not rely on the propositions alone but compared the whole closure: it equals GraphDB's and Nemo's assertion by assertion, and every answer set equals GraphDB's.

Finally, regarding references, we agree to add Do et al. (2018) and trim old ones. Nguyen et al. (2025), however, concerns embeddings and multi-agent consultation rather than object-oriented knowledge representation.

Accordingly, we will change:

1. State the closed-world and unique-name conditions in the introduction, not only in Section 8.
2. Report loading with step 5 disabled.
3. Add Do et al. (2018) and trim old references.

We will not change:

- The benchmark, whose RL profile tests exactly the fragment our propositions cover.
- Nguyen et al. (2025), as explained above.
- The lack of a query planner for working memory, which we name as future work.
