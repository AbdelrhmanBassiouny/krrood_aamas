# Author response, AAMAS 2027 submission 1481

Each section below is one OpenReview reply, at most 2500 characters. Post each under its review; there is no general reply. Check lengths with `python3 count.py` before posting.

---

## To Reviewer HKHa

We thank the reviewer. The final version adds a listing of the agent querying its own queries and rules (W1), states in the introduction that we claim certain answers of positive queries, not open-world reasoning (W2), reports loading with step 5 disabled (W3), and states which facts can become stale (W4).

Why unify. (1) Reflection: queries, rules and planner calls are objects of the same program as the domain knowledge, so the agent queries them with the same language, e.g. which rules derive T20CricketFan, or which decisions call the planner through CanReach. This puts the agent's own components at the level of its domain knowledge, in the spirit of Newell's knowledge level; a separate store needs a second meta-model. We add a listing. (2) Cost (Section 7.4): with GraphDB, deciding in SPARQL writes 405 values per step instead of 4; Owlready2 writes back 1.4 million inferences per step (33 s). (3) Predicates are the agent's own procedures, so reasoning calls its code directly.

Standards and reuse. KRROOD consumes OWL rather than replacing it. Ontomatic compiles an OWL 2 RL ontology into the program, preserving its entailments (Propositions 5.1, 5.2), and ORMatic stores the objects in a relational database with the same answers (Theorem 6.1). Only the second run-time copy of the world model is removed.

Open world. We do not claim it. Every answer of a positive query is a certain answer, and under the conditions of Proposition 5.2 all certain answers are returned, so for positive queries the answers equal the open-world ones. Only negation and aggregates are closed-world, as negation as failure. The introduction will state this; open-world negation is future work.

One benchmark. OWL2Bench's RL profile tests exactly the fragment our claims cover. We add loading with step 5 disabled.

Retraction. Three kinds of fact: computed predicates (all of the planner's contribution) are recomputed per query and never stale; reassigned attributes replace the old value; facts derived by property rules are not retracted, as Section 8 states. The final version states the three kinds in the main text; incremental maintenance (Motik et al., 2015) is future work.

---

## To Reviewer 7FxR

We thank the reviewer. The final version refers to one pinned release throughout (main concern), adds proof sketches to the main text, reports loading with step 5 disabled (A), and scopes the agent-loop claim (B).

Two versions. The reviewer is right: in the submission, Propositions 5.1 to 5.3 and Theorem 6.1 do not apply to the version that produced the numbers. The final version uses one pinned release of the current version for all listings, proofs and experiments, all rerun; a rerun counts only if the closure again equals GraphDB's and Nemo's assertion by assertion and every answer set equals GraphDB's. Footnotes 2 and 3 and the "earlier version's equality" clause go; Corollary 1's proof is rewritten for identity equality of roles; the 18-query check runs after the two ORMatic fixes; Table 5 reports the same release. We take the space from Section 3's vocabulary and the contribution list, as suggested.

Proofs. We add a few lines per result giving its strategy or key invariant. E.g., Proposition 5.2: step 1 adds the super-, equivalent, inverse and symmetric facts of every assertion; step 2 closes chains and the transitive properties they use; every later fact then relates individuals that already hold its property, so no rule derives a new type.

A. Step 5 is exact and general: for any symmetric and transitive property in any ontology, the closure relates exactly the members of each weakly connected component. Step 5 computes this directly instead of cubic rule chaining, as RDFox does for owl:sameAs. We agree OWL2Bench loading is dominated by this property (Section 7.2), and will report loading with step 5 disabled next to the main results.

B. Agreed. The loop measures what a second world model adds (sync code, writes, round trips) and that decisions agree in every step of five seeds; we scope the claim to that.

---

## To Reviewer sSAi

We thank the reviewer. The final version adds the citations, a novelty paragraph tied to Table 1, full sentences in Section 3 and a narrower title.

Citations. GraphDB, Nemo and Owlready2 will be cited where the introduction first names them.

Novelty. We add a paragraph tied to Table 1: KRROOD is, to our knowledge, the first framework in which the terminology, assertions, OWL 2 RL property inference, a first-order query language whose predicates are the agent's own procedures, and long-term memory share one object model. As a consequence, the agent can query its own queries, rules and planner calls with the same language; we add a listing showing this. Each row of Table 1 shows which of these a related system lacks.

Presentation. Section 3's itemized definitions become full sentences; the sentence will read "of which 1.42 million are assertions about individuals".

Title. Agreed; we narrow it to the claim, e.g. "KRROOD: The Agent's Object-Oriented Program as Its Knowledge Base".

---

## To Reviewer MnFm

We thank the reviewer. The final version states the closed-world and unique-name conditions in the introduction, reports loading with step 5 disabled, and adds Do et al. (2018).

Closed world and unique names. Neither changes the answers of positive queries under our stated conditions. Every answer is a certain answer over the ontology (Proposition 5.1), and under the conditions of Proposition 5.2 every certain answer is returned (Corollary 1). Only negation and aggregates are closed-world, as negation as failure. KRROOD does not merge individuals; after loading, a check reports every applicable equality rule (functional and inverse-functional properties, keys, max cardinalities). If none applies, no equality is entailed and no certain answer is lost. On OWL2Bench it reports none. Where the conditions fail, answers can differ from OWL entailment; Section 8 says so, and the introduction will too.

Symmetric and transitive properties. Step 5 is not a benchmark bypass. It is exact for every such property in any ontology: the closure relates exactly the members of each weakly connected component, as RDFox does for owl:sameAs. We add loading with step 5 disabled.

Joins. Working-memory EQL has no query planner, and Section 7.3 reports this on Q22. Over all 18 queries it is still 1.8 times GraphDB's geometric mean and faster than RDFLib and Owlready2. For join-heavy queries, the same EQL query translated to SQL by ORMatic is the fastest system on 14 of 18 queries, with the same answers (Theorem 6.1).

Benchmark and punning. OWL2Bench's RL profile tests exactly the fragment our propositions cover. Its 47 punned IRIs (Section 7.1) place it just outside our conditions, yet the closure and all 18 answer sets equal GraphDB's.

References. Old references are the sources of the notions we use (Reiter 1978, Vardi 1982); we trim the rest and add Do et al. (2018). Nguyen et al. (2025) concerns embeddings and multi-agent consultation, not object-oriented knowledge representation, so we do not add it.
