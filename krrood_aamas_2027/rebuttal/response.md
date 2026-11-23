# Author response, AAMAS 2027 submission 1481

Each section below is one OpenReview reply. Post the general reply first, then the one under each review. Check the reply form's character limit before posting.

---

## To all reviewers

We thank the reviewers for careful reviews. The final version will contain the following changes.

1. **One version** (7FxR, main concern). Every listing, proposition and number refers to one pinned release of the current KRROOD. We rerun every experiment on it and accept the rerun only if KRROOD's closure again equals GraphDB's and Nemo's assertion by assertion and every answer set again equals GraphDB's.
2. **Proof sketches in the main text** (7FxR). For Propositions 5.1 to 5.3, Corollary 1 and Theorem 6.1, we state each proof's strategy or key invariant.
3. **Step 5 made explicit** (7FxR A, MnFm). Next to the main loading results, we report loading with step 5 disabled. We also state that step 5 is exact for every property that is both symmetric and transitive, in any ontology.
4. **Reflection** (HKHa, sSAi). A listing in which an EQL query inspects the agent's own queries, rules and planner calls. These are objects of the same program as its domain knowledge.
5. **Scope of the claims** (HKHa, MnFm, 7FxR B). We state in the introduction and the discussion that we claim certain answers of positive queries, not open-world reasoning. We state which kinds of fact can become stale, and we scope the agent-loop claim to what it measures.
6. **Presentation** (sSAi, MnFm). Citations for GraphDB, Nemo and Owlready2 in the introduction, full sentences in Section 3, a novelty paragraph tied to Table 1, a narrower title, and the related work the reviewers point to.

**What we will not change, and why.**

- **We keep OWL2Bench as the benchmark.** It is built for the OWL 2 profiles, so its RL profile tests exactly the fragment that Ontomatic and our propositions cover. Its predecessor LUBM, for example, uses class equivalences with existential right-hand sides, which lie outside OWL 2 RL. The concern behind a second benchmark, that one benchmark-specific property drives the results, is answered by change 3.
- **Open-world semantics for negation, incremental retraction of rule-derived facts, and a query planner** are research problems of their own. The paper names them as limitations, and the final version names them as future work.

---

## To Reviewer HKHa

**Why unify the two models.** First, reflection. In KRROOD, the agent's queries, rules and planner calls are objects of the same program as its domain knowledge, so the agent can query them with the same language. For example, it can ask which rules derive `T20CricketFan`, or which decisions call the planner through `CanReach`. Its own components are then accessible at the same level as its domain knowledge, in the spirit of Newell's knowledge level. With a separate store, this needs a second meta-model. The final version adds a listing that shows this. Second, cost. Section 7.4 measures what a second world model adds. The GraphDB build needs synchronization code, writes and round trips on every step. When SPARQL alone decides, it writes 405 values per step instead of 4. The Owlready2 build writes 1.4 million inferences back on every step, which takes 33 s. Third, much of what a robot knows is computed from its own data. In KRROOD, the predicates of a query are the agent's own procedures, so reasoning calls that code directly, with no export.

**Standard formalisms, modularity and reuse.** KRROOD does not replace OWL as a standard. It consumes it. Ontomatic compiles an OWL 2 RL ontology into the program, so the ontology remains the reusable, standard artefact, and its OWL 2 RL entailments are preserved (Propositions 5.1 and 5.2). ORMatic stores the same objects in a standard relational database and translates EQL queries to SQL with the same answers (Theorem 6.1). What KRROOD removes is the second copy of the world model at run time, not the standard formalisms.

**Open-world reasoning.** We agree that open-world reasoning matters, and we do not claim it. Every answer of a positive EQL query is a certain answer over the ontology (Proposition 5.1). Under the conditions of Proposition 5.2, every certain answer is returned. So for positive queries, KRROOD's answers are the open-world answers. Only negation and aggregates are closed-world, as negation as failure, which the agent's decisions need. The final version states this in the introduction and the discussion. Open-world semantics for negation is future work, outside this paper's scope.

**One benchmark.** Please see the general reply. OWL2Bench's RL profile tests exactly the fragment our claims cover, and the final version reports loading with step 5 disabled.

**Retraction of inferred facts.** We agree that this matters. KRROOD handles three kinds of fact differently:

- Facts computed by predicates, such as `CanReach`, are recomputed on every query, so they are never stale. In the agent loop, everything the planner contributes is of this kind.
- An asserted attribute value that is reassigned replaces the old value.
- Facts derived by property rules on assignment are not retracted. This is the limitation stated in Section 8.

The final version states these three kinds in the main text, so that a developer knows which facts can become stale. Incremental maintenance of inferences (Motik et al., 2015) is future work.

---

## To Reviewer 7FxR

**Main concern: two versions.** The reviewer is right that, in the submission, Propositions 5.1 to 5.3 and Theorem 6.1 do not apply to the version that produced the numbers. The final version has one version (general reply, change 1). All listings, proofs and experiments refer to one pinned release of the current version. Footnotes 2 and 3 and the "earlier version's equality" clause are removed, and the proof of Corollary 1 is rewritten for identity equality of roles. The 18-query check runs after the two ORMatic fixes, and Table 5 reports the robot on the same release. We take the space from the places the reviewer suggests: the vocabulary in Section 3 and the list of contributions.

**Proofs in the main text.** We will add a sketch of a few lines per result, stating its proof strategy or key invariant. For example, Proposition 5.2 rests on one invariant, already stated after it. Step 1 adds the super-, equivalent, inverse and symmetric facts of every assertion. Step 2 closes the chains and the transitive properties that class expressions and chains use. Every later fact then relates individuals that already hold its property, so no rule derives a new type.

**A. Step 5.** Step 5 is exact and general, not specific to OWL2Bench. For any property that is both symmetric and transitive, in any ontology, its closure relates exactly the members of each weakly connected component of the property's graph. Step 5 computes this directly, where rule-by-rule chaining does cubic work in the size of a component. RDFox treats `owl:sameAs` the same way. We agree that the loading comparison on OWL2Bench is dominated by this one property, and Section 7.2 says so. The final version reports loading with step 5 disabled next to the main results, so that the reader sees the design's cost both with and without it.

**B. Size of the agent loop.** We agree that one scenario with few writes per step cannot show that one world model never costs more. The loop measures what a second world model adds (synchronization code, writes and round trips) and checks that decisions agree in every step of five seeds. We will scope the claim to this.

---

## To Reviewer sSAi

**Citations.** The final version cites GraphDB, Nemo and Owlready2 where the introduction first names them.

**Related work and novelty.** We will add a paragraph that states the novelty against Table 1. KRROOD is, to our knowledge, the first framework in which the terminology, the assertions, OWL 2 RL property inference, a first-order query language whose predicates are the agent's own procedures, and long-term memory share one object model. Because they share it, the agent can also query its own queries, rules and planner calls (general reply, change 4). Each row of Table 1 shows which of these a related system lacks, and the paragraph will explain why it matters.

**Presentation.** We will rewrite Section 3's itemized definitions, such as the one the reviewer quotes, as full sentences. "1.42 million of them assertions" will read "of which 1.42 million are assertions about individuals".

**Title.** We agree that it is broad. We will narrow it to the paper's claim, for example "KRROOD: The Agent's Object-Oriented Program as Its Knowledge Base".

---

## To Reviewer MnFm

**Closed-world and unique-name assumptions.** Neither assumption changes the answers of positive queries under the conditions we state.

- **Closed world.** Every answer of a positive query is a certain answer over the OWL ontology (Proposition 5.1). Under the conditions of Proposition 5.2, every certain answer is returned (Corollary 1). Only negation and aggregates are closed-world, deliberately, as negation as failure.
- **Unique names.** KRROOD does not merge individuals. After loading, a check reports every application of an equality rule (functional and inverse-functional properties, keys, maximum cardinalities). If none applies, no equality between distinct names is entailed, so keeping individuals apart loses no certain answer. On OWL2Bench, the check reports no equality and no inconsistency.

Where these conditions fail, an answer can contradict OWL entailment. Section 8 states this, and the final version makes it explicit in the introduction. We do not claim open-world reasoning.

**Symmetric and transitive properties.** Step 5 is not a bypass tuned to the benchmark. It applies to every property that is both symmetric and transitive, in any ontology, and it is exact: the closure of such a property relates exactly the members of each weakly connected component. Its facts are then propagated to super-properties, inverses, equivalent properties and chains like any other fact. RDFox handles `owl:sameAs` the same way. The final version reports loading with step 5 disabled. At run time, transitivity of these properties is not maintained on assignment, and Proposition 5.3 states this exception.

**Joins.** EQL in working memory has no query planner, and Section 7.3 reports that this makes it slow on large joins (Q22). In geometric mean over the 18 queries, it still takes 1.8 times GraphDB's time and is faster than RDFLib and Owlready2. ORMatic provides a second path for join-heavy queries. The same EQL query, translated to SQL, is the fastest of all systems on 14 of the 18 queries, and Theorem 6.1 proves that it returns the same answers for the stated fragment. A query planner for working memory is future work.

**One benchmark, and punning.** We chose OWL2Bench because its RL profile tests exactly the fragment that our propositions cover (see the general reply). Section 7.1 states that 47 IRIs are used both as classes and as individuals, which places the benchmark just outside our propositions' conditions. The closure and all 18 answer sets nevertheless coincide with GraphDB's, so this does not affect the reported results.

**References.** The older references are the sources of the notions we use, such as the closed-world assumption (Reiter, 1978) and the complexity of first-order queries (Vardi, 1982). We will trim references that the argument does not need, and add the rela-model work of Do et al. (2018) to the related work on object-oriented knowledge models. We will not add the Legal BERT and ReAct consulting system (Nguyen et al., 2025), since it concerns embeddings and multi-agent consultation, not object-oriented knowledge representation.
