# Author response, AAMAS 2027 submission 1481

Each section below is one OpenReview reply, at most 2500 characters. Post each under its review with that review's rebuttal button; there is no general reply. Each answer starts with the reviewer's words, quoted; in this public copy the quotes are placeholders, and the version to post, with the quotes, is kept outside the repository. Check lengths with `python3 count.py` before posting.

---

## To Reviewer HKHa

We thank the reviewer for the careful review.

> [HKHa W1, quoted]

Unifying has two aspects. The first is accessibility of knowledge: the agent's procedures, queries and rules are objects of the same program as its domain knowledge, so the agent can reflect on its reasoning. E.g., this EQL query finds the agent's queries that call its path planner, CanReach:

```python
q = variable(Query, domain=agent_queries)
part = flat_variable(node_descendants(q))
uses_planner = an(entity(q).where(node_type(part) == CanReach))
```

With two world models, this reflection cannot be complete: each process hides its reasoning from the other, which sees only results passed through their interface. The second is practicality, which we measured: in our robot experiment, deciding in SPARQL alone writes 405 values into GraphDB per step instead of 4. We acknowledge that we did not evaluate the first aspect. OWL stays the standard: Ontomatic compiles OWL ontologies into the program.

> [HKHa W2, quoted]

We agree; it seems we did not make clear how much is kept. Under open-world semantics, a query's answers are its certain answers: those true in every model of the ontology. For positive queries, KRROOD returns only certain answers (Proposition 5.1) and, under the conditions of Proposition 5.2, all of them (Corollary 1), so its answers equal an open-world reasoner's. The closed world only matters for negation and aggregates, which ask what is not known.

> [HKHa W3, quoted]

We chose OWL2Bench as its RL profile tests exactly the fragment our propositions cover. We agree, though, that its loading is dominated by one property, handled by step 5 of Ontomatic's loading.

> [HKHa W4, quoted]

Of KRROOD's three kinds of fact, only one can become stale: computed predicates are recomputed per query and reassigned attributes replace old values, but rule-derived facts are not retracted.

We will change:

1. W1: add this listing to the paper.
2. W2: explain certain answers in the introduction.
3. W3: give the full loading time without step 5 in Table 2.
4. W4: state which facts can become stale.

We will not change:

- The benchmark (see W3).
- Open-world negation and retraction of rule-derived facts (future work).

---

## To Reviewer 7FxR

We thank the reviewer for the thorough review, the kind words on the related work, and the concrete suggestions, which we are happy to follow.

> [7FxR 1, quoted]

We agree that every result must come from the version of KRROOD that the listings show. We will therefore pin one release of KRROOD for all listings, proofs and experiments, and rerun every experiment, the delivery robot included. A rerun counts only if KRROOD's closure of OWL2Bench again equals GraphDB's and Nemo's and every query's answer set equals GraphDB's. Footnotes 2 and 3 and the earlier version's equality in Corollary 1 are then no longer needed. As suggested, the space comes from Section 3 and the contribution list.

> [7FxR 2, quoted]

We agree, and will state the proof strategy and key invariant of Propositions 5.1–5.3 and Corollary 1 in the main text.

> [7FxR A, quoted]

We agree that step 5 of Ontomatic's loading dominates loading on OWL2Bench. Step 5, however, handles a general class of properties: for any symmetric and transitive property, the closure relates exactly the members of each weakly connected component, so step 5 is exact in any ontology, much as RDFox treats owl:sameAs. On OWL2Bench, this class happens to contain hasSameHomeTownWith, 92% of the closure. Section 7.2 gives the loading time without step 5 only as "over two hours"; we will report it in full.

> [7FxR B, quoted]

We agree, and will scope that claim to what the delivery-robot scenario measures: the synchronization that a second world model adds, and that all five robot builds make the same decision in every step.

In summary, we will change:

1. One pinned release of KRROOD for everything, with every experiment rerun.
2. Proof strategies and key invariants in the main text.
3. The full loading time and memory without step 5, in Table 2.
4. The claim on the cost of one world model, scoped as above.

We will not change:

- Step 5 itself, since it is exact for every symmetric, transitive property.

---

## To Reviewer sSAi

We thank the reviewer for the helpful comments, and are glad the running examples make the paper easier to read. We agree with all points.

> [sSAi comment 1, quoted]

We will cite GraphDB, Nemo and Owlready2 there.

> [sSAi comment 2, quoted]

We will state, for each group of related systems, what KRROOD adds.

> [sSAi comment 3, quoted]

We will rewrite such expressions as full sentences, starting with the closed-world definition in Section 3, and check the rest of the paper likewise.

> [sSAi comment 4, quoted]

The sentence in Section 7 will read "1.42 million of which are assertions".

> [sSAi comment 5, quoted]

It seems we did not state the novelty clearly. In general, our novelty is that the agent's object-oriented program is its knowledge base. Concretely, KRROOD is, to our knowledge, the first framework where terminology, assertions, OWL 2 RL inference, a query language whose predicates are the agent's own procedures, and long-term memory share one object model. We will state this in a paragraph tied to Table 1, and narrow the title accordingly, e.g. "KRROOD: The Agent's Object-Oriented Program as Its Knowledge Base".

---

## To Reviewer MnFm

We thank the reviewer for the detailed review. It seems several of our results were not clear; we clarify them in the order raised.

> [MnFm comment 1, quoted]

Answers to positive queries do not contradict OWL: every answer is a certain answer (Proposition 5.1), and under the conditions of Proposition 5.2 all certain answers are returned (Corollary 1). Unique names are checked, not silently assumed: after loading, Ontomatic reports every application of an OWL equality rule. On OWL2Bench it reports none.

> [MnFm comment 2, quoted]

Step 5 of Ontomatic's loading is a general rule for this class of properties: for any such property, the closure relates exactly the members of each weakly connected component, so step 5 is exact in any ontology, much as RDFox treats owl:sameAs.

> [MnFm comment 3, quoted]

We agree for some joins, such as OWL2Bench query Q22. Such queries are what ORMatic's SQL translation of the same EQL query is for: translated, EQL is fastest on 14 of the 18 OWL2Bench queries, with the same answers (Theorem 6.1).

> [MnFm comment 4, quoted]

We agree that OWL2Bench's 47 IRIs used both as classes and as individuals lie outside the conditions of Proposition 5.2. This is why we compared KRROOD's whole closure: it equals GraphDB's and Nemo's assertion by assertion.

> [MnFm comment 5, quoted]

We agree to add Do et al. (2018) and trim old references. Nguyen et al. (2025), however, concerns embeddings and multi-agent consultation rather than object-oriented knowledge representation.

We will change:

1. State the closed-world and unique-name conditions in the introduction, not only in Section 8.
2. Report the full loading time without step 5 in Table 2, not only as "over two hours" (Section 7.2).
3. Add Do et al. (2018) and trim old references.

We will not change:

- The benchmark, whose OWL 2 RL profile tests exactly the fragment our propositions cover.
- Nguyen et al. (2025), as explained above.
- A query planner for working-memory evaluation, which we name as future work.
