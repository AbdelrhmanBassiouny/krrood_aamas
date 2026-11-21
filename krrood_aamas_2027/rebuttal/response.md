# Author response, AAMAS 2027 submission 1481

Each section below is one OpenReview reply. Post the general reply first, then the one under each review.

---

## To all reviewers

We thank the reviewers for careful reviews. Below we answer the points raised, and list what the final version will contain.

**One version.** In the final version, every listing, proposition and number refers to one version of KRROOD, the current one, pinned at a single release. This removes the split that Reviewer 7FxR identified (footnotes 2 and 3, "the earlier version's equality" in Corollary 1). Ontomatic's loader on the current version applies the same rules that the supplement's lemmas describe. We rerun every experiment on that release: the closure check, Tables 2 to 5 for one to eight universities, the 18-query check of the SQL translation after the two ORMatic fixes of Section 6, and the agent loop. We accept the rerun only if KRROOD's closure again equals GraphDB's and Nemo's assertion by assertion, and every answer set again equals GraphDB's.

**What we claim about the closed world.** We do not claim open-world reasoning. The claim is narrower, and Propositions 5.1 and 5.2 and Corollary 1 state it. Every answer of a positive EQL query is a certain answer over the OWL ontology. Under the conditions we state, every certain answer is returned. For positive queries, the closed-world reading therefore gives the same answers as OWL's open-world entailment. Negation and aggregates are deliberately closed-world, as negation as failure. The final version states this distinction in the introduction and the discussion rather than only in Section 5.

**Changes promised for the final version:**
1. One pinned version for all listings, proofs and experiments, with every experiment rerun (above).
2. A proof sketch, or the key invariant, in the main text for Propositions 5.1 to 5.3, Corollary 1 and Theorem 6.1.
3. A second benchmark, LUBM: closure checked against GraphDB's OWL 2 RL closure, loading, and its 14 queries. LUBM has no property that is both symmetric and transitive, so step 5 does not apply to it.
4. A variant of the agent loop in which perceived facts change and disappear (students drop courses, fans stop being fans). It measures the three kinds of retraction separately (see the reply to Reviewer HKHa).
5. A listing in which an EQL query inspects the agent's own queries and rules, as evidence for the reflection argument.
6. Presentation: citations for GraphDB, Nemo and Owlready2 in the introduction, full sentences in Section 3, a novelty paragraph tied to Table 1, a narrower title, and the related work the reviewers point to.

---

## To Reviewer HKHa

**Why unify the two models.** With two world models, the program's objects must be copied into the store and the results mapped back on every step. Section 7.4 measures what this costs. The GraphDB build needs synchronization code, writes and round trips on every step. When SPARQL alone decides, it writes 405 values per step instead of 4. The Owlready2 build exports its quadstore to Pellet and writes 1.4 million inferences back on every step, which takes 33 s. KRROOD's robot makes the same decision in every step without any of this. A second reason is that much of what a robot knows is computed from its own data (Section 1). In KRROOD, the predicates of a query are the agent's own procedures, so reasoning calls that code directly, with no export. A third reason is reflection. Queries, axioms and rules are objects of the same program, so the agent can query its own queries and rules: for example, which rules derive `T20CricketFan`, or which decisions call `CanReach`. The final version adds a listing that shows this (promise 5).

**Standard formalisms, modularity and reuse.** KRROOD does not replace OWL as a standard. It consumes it. Ontomatic compiles an OWL 2 RL ontology into the program, so the ontology remains the reusable, standard artefact, and its OWL 2 RL entailments are preserved (Propositions 5.1 and 5.2). ORMatic stores the same objects in a standard relational database and translates EQL queries to SQL with the same answers (Theorem 6.1). What KRROOD removes is the second copy of the world model at run time, not the standard formalisms.

**Open-world reasoning.** We agree that open-world reasoning matters, and we do not claim it. Our claim is about positive queries (see the general reply). Their answers are certain answers over the ontology, and, under the stated conditions, all certain answers are returned. So for these queries, KRROOD's answers are the open-world answers. The closed world affects only negation and aggregates, which the agent's decisions need and which we make explicit as negation as failure. The final version states this in the introduction and the discussion, and keeps the limitation: where the conditions of Proposition 5.2 do not hold, an answer can differ from OWL entailment. Adding an open-world semantics for negation is a direction we will name in future work. It is outside the scope of this paper.

**One benchmark.** The final version adds LUBM (promise 3).

**Retraction of inferred facts.** We agree that this matters and will treat it explicitly. KRROOD handles three kinds of fact differently:
- Facts that predicates compute, such as `CanReach`, are recomputed on every query, so they are never stale.
- An asserted attribute value that is reassigned replaces the old value.
- Facts derived by property rules on assignment are not retracted. This is the limitation, and it is stated in Section 8.

The new agent-loop variant (promise 4) measures the three kinds separately. It compares the robot's decisions with Nemo's, which recomputes the closure on every step, and reports every stale rule-derived fact. Incremental maintenance of inferences (Motik et al., 2015) remains future work.

---

## To Reviewer 7FxR

**Main concern: two versions.** The reviewer is right that, in the submission, Propositions 5.1 to 5.3 and Theorem 6.1 do not apply to the version that produced every number. The final version has one version (general reply, promise 1). All listings, proofs and experiments refer to one pinned release of the current version. Footnotes 2 and 3 and the "earlier version's equality" clause are removed, and the proof of Corollary 1 is rewritten for identity equality of roles. The 18-query check runs after the two ORMatic fixes, and Table 5 reports the robot on the same release. We will take the space from the places the reviewer suggests: the vocabulary in Section 3 and the list of contributions.

**Proofs in the main text.** We will add a sketch of a few lines per result, stating its proof strategy or key invariant (promise 2). For example, Proposition 5.2 rests on one invariant, already stated after it. Step 1 adds the super-, equivalent, inverse and symmetric facts of every assertion. Step 2 closes the chains and the transitive properties that class expressions and chains use. Every later fact then relates individuals that already hold its property, so no rule derives a new type.

**A. Step 5.** Step 5 is exact and general, not specific to OWL2Bench. For any property that is both symmetric and transitive, in any ontology, its closure relates exactly the members of each weakly connected component of the property's graph. Step 5 computes this directly, where rule-by-rule chaining does cubic work in the size of a component. RDFox treats `owl:sameAs` the same way. We agree that the loading comparison on OWL2Bench is dominated by this one property, and the paper says so in Section 7.2. LUBM has no property that is both symmetric and transitive, so its loading results (promise 3) measure the design without step 5.

**B. Size of the agent loop.** We agree that one scenario with few writes per step cannot show that one world model never costs more. The loop is meant to measure what a second world model adds: synchronization code, writes and round trips. It also checks that decisions agree in every step of five seeds. We will scope the claim accordingly. The retraction variant (promise 4) adds a scenario in which perceived facts change and disappear on every step.

---

## To Reviewer sSAi

**Citations.** The final version cites GraphDB, Nemo and Owlready2 where the introduction first names them.

**Related work and novelty.** We will add a paragraph that states the novelty against Table 1. KRROOD is, to our knowledge, the first framework in which the terminology, the assertions, OWL 2 RL property inference, a first-order query language whose predicates are the agent's own procedures, and long-term memory share one object model. It also gives one semantics to the queries that long-term memory answers. Each row of Table 1 shows which of these a related system lacks, and the paragraph will explain why it matters.

**Presentation.** We will rewrite Section 3's itemized definitions, such as the one the reviewer quotes, as full sentences. "1.42 million of them assertions" will read "of which 1.42 million are assertions about individuals".

**Title.** We agree that it is broad. We will narrow it to the paper's claim, for example "KRROOD: The Agent's Object-Oriented Program as Its Knowledge Base".

---

## To Reviewer MnFm

**Closed-world and unique-name assumptions.** Neither assumption changes the answers of positive queries under the conditions we state.
- **Closed world.** Every answer of a positive query is a certain answer over the OWL ontology (Proposition 5.1). Under the conditions of Proposition 5.2, every certain answer is returned (Corollary 1). Only negation and aggregates are closed-world, deliberately, as negation as failure.
- **Unique names.** KRROOD does not merge individuals. After loading, a check reports every application of an equality rule (functional and inverse-functional properties, keys, maximum cardinalities). If none applies, no equality between distinct names is entailed, so keeping individuals apart loses no certain answer. On OWL2Bench, the check reports no equality and no inconsistency.

Where these conditions fail, an answer can contradict OWL entailment. Section 8 states this, and the final version makes it explicit in the introduction. We do not claim open-world reasoning.

**Symmetric and transitive properties.** Step 5 is not a bypass tuned to the benchmark. It applies to every property that is both symmetric and transitive, in any ontology, and it is exact: the closure of such a property relates exactly the members of each weakly connected component. Its facts are then propagated to super-properties, inverses, equivalent properties and chains like any other fact. RDFox handles `owl:sameAs` the same way. At run time, transitivity of these properties is not maintained on assignment. Proposition 5.3 states this exception.

**Joins.** EQL in working memory has no query planner, and Section 7.3 reports that this makes it slow on large joins (Q22). In geometric mean over the 18 queries, it still takes 1.8 times GraphDB's time and is faster than RDFLib and Owlready2. ORMatic provides a second path for join-heavy queries. The same EQL query, translated to SQL, is the fastest of all systems on 14 of the 18 queries. Theorem 6.1 proves that it returns the same answers for the stated fragment. A query planner for working memory is future work.

**One benchmark, and punning.** The final version adds LUBM (closure, loading and 14 queries). We state the fragment it covers, since LUBM's class equivalences with existential right-hand sides lie outside OWL 2 RL. On OWL2Bench, the paper states in Section 7.1 that 47 IRIs are used both as classes and as individuals, which places the benchmark just outside our propositions' conditions. The closure and all 18 answer sets nevertheless coincide with GraphDB's.

**References.** The older references are the sources of the notions we use, such as the closed-world assumption (Reiter, 1978) and the complexity of first-order queries (Vardi, 1982). We will trim references that the argument does not need. We will add the rela-model work of Do et al. (2018) to the related work on object-oriented knowledge models. We will not add the Legal BERT and ReAct consulting system (Nguyen et al., 2025): it concerns embeddings and multi-agent consultation, not object-oriented knowledge representation.
