# Paper edits from the Ontomatic changes (fact placement, remaining OWL 2 RL rules)

These replace passages of `main.tex` that describe Ontomatic's rules, completeness and the correctness results. They
describe CRAM branch `aamas27-experiments` at `ec7c922b9f`. Apply them after the review-3 edits; the paper session
owns `main.tex`.

Verified on the development machine against GraphDB's OWL 2 RL closure (`owl2-rl-optimized`, raw data):
- class memberships: 0 not entailed, 0 missing (17,558 memberships of 3,667 individuals);
- object-property assertions: 0 not entailed, 0 missing (1,385,869);
- data-property assertions: 0 not entailed, 0 missing (20,933; before ec7c922b9f, 2,487 were missing because
  `hasCode` is equivalent to `hasID`);
- `check_owl2_rl()`: no equality between different individuals, no inconsistency;
- EQL and SQL over ORMatic return GraphDB's answer sets on all 18 queries.

Facts checked for the wording below (details in `RUNBOOK_AAMAS27.md`, section 2.1):
- The rule names and the rule set are those of the W3C OWL 2 Profiles recommendation, Section 4.3, Tables 4-9.
- OWL2Bench prescribes no rule set; its RL TBox is an OWL 2 RL ontology (OWL API profile checker: no violation).
- Our ontology file is the OWL2Bench RL TBox of March 2020 plus our role markers and the T20CricketFan definition. The
  role markers (`C SubClassOf roleFor some D`, 15 classes) are the only axioms outside OWL 2 RL; every marked class is
  already a subclass of `D`, so they change no entailment over the benchmark's vocabulary.
- OWL2Bench uses 47 IRIs both as classes and as individuals (college disciplines): punning, which Theorem PR1 excludes.

## 1. Section "Ontomatic", the paragraph that walks through Listing lst:loading

(a) Replace "Step~2 adds the domains and ranges of these properties and the classes whose axioms the proxy satisfies,
until no new type arises." with:

> Step~2 adds the domains and ranges of these properties, the classes whose axioms the proxy satisfies, and what the
> necessary conditions of its classes require: the named classes of an intersection (\texttt{cls-int2}), the value of
> a \texttt{hasValue} restriction (\texttt{cls-hv1}) and the class of the values of an \texttt{allValuesFrom}
> restriction (\texttt{cls-avf}). The values it considers include those derived through transitivity and property
> chains, for the properties that a class expression or a chain uses. It repeats until no new type or value arises.

(b) After the sentence that says assigning the property values through the descriptors triggers the property rules,
add:

> Every fact, asserted or inferred, is stored on the object of its subject's individual that declares the property:
> the role taker or one of its roles (\texttt{declaring} in Listing~\ref{lst:loading}).

(If the listing changes, keep the reference to `declaring`. The listing could gain a line for the necessary
conditions, e.g. `apply(necessary_conditions(c), x)` in step 2.)

## 2. Table tab:rl

Replace the row "Restriction in superclass position & specialized attribute type & not used (\texttt{cls-hv1},
\texttt{cls-avf}) & ---" with:

> Restriction or intersection in superclass position & necessary condition, read from the ontology &
> \texttt{cls-int2}, \texttt{cls-hv1}, \texttt{cls-avf} & load \\

Change the `domain, range` row's rules to "\texttt{prp-dom}, \texttt{prp-rng} (also for data properties)", and the
`subPropertyOf` and `equivalentProperty` rows' second column to mention data properties if space allows.

Replace the last two rows (below `\midrule`) with:

> Disjointness, irreflexivity, asymmetry, complements, negative assertions, $\leq 0$ & checked after loading &
> \texttt{cax-dw}, \texttt{cax-adc}, \texttt{prp-irp}, \texttt{prp-asyp}, \texttt{prp-pdw}, \texttt{prp-npa1/2},
> \texttt{cls-com}, \texttt{cls-maxc1}, \dots & check \\
> Functional, inverse-functional, keys, $\leq 1$ & checked after loading; unique names entailed if none applies &
> \texttt{prp-fp}, \texttt{prp-ifp}, \texttt{prp-key}, \texttt{cls-maxc2}, \texttt{cls-maxqc3/4} & check \\

Caption: add "``Check'' rules are evaluated after loading (Section~\ref{sec:ontomatic}). The equality rules
\texttt{eq-*} are not needed when the check finds no equality, and the datatype rules \texttt{dt-*} derive no
assertion about an individual."

## 3. Section "Ontomatic", soundness and completeness

(a) In the paragraph after Proposition prop:soundness, replace "Since \ac{krrood} does not check consistency, the
guarantee is vacuous for an inconsistent $\mathcal{O}$." with:

> For an inconsistent $\mathcal{O}$ the guarantee is vacuous; the check below reports such an $\mathcal{O}$.

(b) Replace everything from "The converse, completeness, does not hold in general, for four reasons:" to the end of
the itemize with:

> After loading, Ontomatic checks the RL/RDF rules that it does not apply. It evaluates on $\mathcal{A}^*$ the rules
> that derive the equality of two individuals (\texttt{prp-fp}, \texttt{prp-ifp}, \texttt{prp-key},
> \texttt{cls-maxc2}, \texttt{cls-maxqc3/4}) and those that derive an inconsistency (Table~\ref{tab:rl}), and reports
> every application. If none applies, the closure equates no two different individuals, so the unique-name assumption
> is entailed rather than assumed.
>
> \begin{proposition}[Completeness]
> \label{prop:completeness}
> Let $\mathcal{O}$ be an OWL~2~RL ontology without punning that uses only the constructs of Table~\ref{tab:rl}, and
> let the check report no equality and no inconsistency. Then every class assertion $C(a)$, with $C$ a named class,
> and every object-property assertion $P(a,b)$ entailed by $\mathcal{O}$ holds in $\mathcal{I}_{\mathcal{A}^*}$.
> \end{proposition}
>
> By Theorem PR1, such an assertion follows from the RL/RDF rules. As no equality between different individuals
> arises, the equality rules only add reflexive \texttt{sameAs} facts, and no inconsistency rule applies. Every other
> rule that derives a class or property assertion is applied: the property rules to every fact, and the typing rules
> to every fact that can add a type before the objects are created. A fact derived by transitivity relates an
> individual that already has a fact of the property to an existing value of it, so it can only add a type through a
> class expression or a property chain, and step~2 closes exactly these properties.

(Optional, if space is short: keep only the proposition and the first two sentences of the argument.)

## 4. Section "Experiments", subsection "Correctness"

Replace everything from "We also compared the knowledge base produced by Ontomatic ..." to the end of that paragraph
with:

> We also compared the knowledge base produced by Ontomatic with GraphDB's OWL~2~RL closure, assertion by assertion.
> For all 3,667 individuals, the class memberships, the object-property assertions and the data-property assertions
> coincide with the closure: \ac{krrood} derives none that the closure lacks and misses none. The check of
> Section~\ref{sec:ontomatic} finds no equality and no inconsistency. Proposition~\ref{prop:completeness} does not
> apply to the benchmark directly: OWL2Bench uses 47 IRIs both as classes and as individuals, and our role markers
> ($C \sqsubseteq \exists\texttt{roleFor}.D$) lie outside OWL~2~RL. Every marked class is already a subclass of $D$,
> so the markers change no entailment over the benchmark's vocabulary, and the reference of the comparison is the
> RL/RDF closure itself.

## 5. Section "Limitations" (or wherever the bullet "Ontomatic targets OWL~2~RL. Constructs outside RL, and RL rules
other than those of Table~\ref{tab:rl}, are not supported, so completeness is not guaranteed" is)

Replace that bullet with:

> Ontomatic targets OWL~2~RL. Constructs outside RL, and RL constructs that the generator does not compile (such as
> \texttt{oneOf}), are not supported. \ac{krrood} does not merge individuals: if the check finds an entailed equality,
> it reports it, and the knowledge base may then miss facts.

## 6. Optional, in the Q12 paragraph about research groups (if it is kept)

After the sentence saying KRROOD represents the entailment as an `Employee` role of the research group, you may add:

> The research group's projects are then also its \texttt{hasWork} values, stored on that role.

## 7. Loading time

On the development machine, the new rules do not change KRROOD's loading time on the raw input (17.68 ± 0.27 s before,
17.41 ± 0.58 s after, 5 interleaved runs; peak memory 326 MB and 339 MB), and halve it on the pre-reasoned input
(381 s to 180 s, one run each). The table values come from the run on the original machine.
