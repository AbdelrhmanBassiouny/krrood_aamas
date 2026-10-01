= Motivation

On the utility of object-oriented access to knowledge: "domain-specific applications require adequate architecture for data authoring and validation, typically using the object-oriented paradigm." @ledvinka2020comparison

On the adoption of ontologies in mainstream development: "Despite the many integration tools proposed, developers are still reluctant to incorporate ontologies into their code repositories" @baset2018object

"The more we move towards domain-aware application development the more it becomes important to abandon generic access and to provide the developer with a transparent means to access and manipulate the content of the ontology." @baset2018object

On OWL reasoners: "Many systems are almost black boxes to their users, with poor documentation, outdated dependencies and no support from their developers. OWL reasoners such as HermiT are still widely used, although they are being abandoned, because there are not many alternatives available." @abicht2023owl -> The consequence is that even modular, standalone systems, if they are not extensible, maintainable and documented, will not be extended, maintained or used -> We approach KR&R not from a capabilities-first perspective, but from a usability- and extensibility-first perspective

Unlce Bob says that what will eventually matter is implementing the details, and that will have to be done in a fully-featured programming language [CITATION]
- When you have generic reasoners operating on a knowledge description like OWL, you lose the ability to perform complex computations as part of that reasoning

= Concepts

== Intellectual tradition

=== Newell's symbol level
Newell: The symbol level implements the knowledge level -> With KRROOD, the knowledge level and the symbol level are implemented by the same technical system, just at different levels of abstraction

According to ChatGPT: The is a *computational reification* of the knowledge level — a system where the objects of reasoning are also the objects of computation.

Or even better: Your framework can be seen as a computational realization (reduction) of knowledge-level constructs within a lower (symbol-level) architecture, while preserving the explanatory vocabulary of the knowledge level. Hence, if you design a symbol-level system whose entities and operations mirror knowledge-level constructs—knowledge, goals, inference, belief—you are indeed performing the kind of reduction that Newell’s framework allows.
You are not violating the hierarchy; you are making the realization explicit and inspectable.

=== Minsky's Frames
- Minsky's "frames" @minsky1974framework as foundational notion for object-oriented representational thinking (frames as structured objects)
- Minsky’s frames (1974) and subsequent frame-based systems (FRL, KRL, KL-ONE) already anticipated the object-oriented view: structured entities with slots, inheritance, and procedural attachment.
  - Hewitt (1977): Actors — concurrent objects communicating via messages.
  - Pat Hayes (1985): Second Naïve Physics Manifesto — modeling physical reasoning in terms of structured entities.

== General idea
"In an ontology-based application, usually multiple representation languages are used for different pur-poses. The backbone is a description logic language for deﬁning the terminological part (e.g. in OWL 2syntax [29]), which is often extended with other logical languages for the assertional part, such as, for in-stance, logic programming rules, the region connection calculus for aspects of spatial reasoning, or Allen’s interval algebra for aspects of temporal reasoning" @haarslev2012racerpro -> We do this too, but all languages we use share the same underlying a) OOP philosophy and b) Python syntax & implementation for interoperability

"Ontology development support is still the most-important application area of description logic reasoning systems." @haarslev2012racerpro -> KRROOD makes this aspect, developing ontologies (knowledge bases), available / more intuitive / more accessible / more scalable through OOD patterns & native IDE integration: Any IDE that supports Pythonic development patterns also supports KRROOD

Future work for RacerPro calls for "Development of software abstractions for build-ing adaptive and ﬂexible reasoning engines using a compositional approach" @haarslev2012racerpro, which is what KRROOD enables


== Alternative Paradigm: Loosely coupling two systems / representations
"There exists a well-known trade off between imperative and declarative languages. Imperative languages such as Java are suitable to describe processes and how these processes should be done. Declarative languages such as OWL are used to describe systems and what is available in them. Each one has advantages and disadvantages and each one is more convenient in some circumstances than in others. For example, graphical interfaces might be easily implemented using the Java language whereas the description of the state of a system might be easily described in the OWL language. Hence, this proposal describes a binding process between Java and OWL to provide an architecture enabling the usage of both languages during software development and at run-time." @alcaraz2012towards

== Tooling for KR&R

=== Categories of tools

Taxonomy from @holanda2017object

1. Ontology editors
2. Ontology reasoners
3. Triple store tools
4. RDF Frameworks
5. Object Triple Mapping Systems

"Particularly, OTM systems are of utmost importance for the
effective development of ontology-based applications, since they allow
the development of these applications under the object-oriented
paradigm" @holanda2017object

== Open questions

=== Open world vs. closed world

"While OWL follows the open world assumption, Java follows the closed world assumption. Essentially, the open world assumption states that new, unforeseen knowledge can be incorporated to the reasoning process in the future. This fact makes OWL suitable to be used in open environments where domain descriptions are not closed, application knowledge may not be complete, and applications can exchange knowledge without having to know each other in advance." @alcaraz2012towards

= Original Related Work

- RacerPro @haarslev2012racerpro is a well-established description logic inference system
  - OWL TBox & ABox + SWRL rules
  - Client-server architecture: Clients make queries to KR&R server to manipulate and reason about knowledge
  - Also have option to store ABoxes in a triple store
  - Description logic supported: SHIQ (which is apparently the same as ALCQHI_𝑅+
  - Racer Query Language (nRQL): "conjunctive queries with variables ranging over named domain objects, negation as failure, a projection operator, as well as group-by and aggregation operators"
    - Also supports SPARQL
  - "Abduction for Abox queries is a unique feature of RacerPro"
  - Internally, uses an AllegroGraph triple store
  - "The RacerPro inference server can be programmed in a functional language called miniLisp."
  - Has a plugin interface for extensibility
  - Is closed-source
  - Apparently stopped being developed / published on in 2012
- Flora-2/ErgoAI
  - ErgoAI @kifer2018ergoai is next-gen version of Flora-2 @noauthor_flora-2_nodate, with enterprise‐scale capabilities (connectors to relational DBs, JSON, RDF/OWL, graph databases, etc)
  - The language of FLORA-2 is a dialect of F-logic with numerous extensions, including meta-programming in the style of HiLog and logical updates in the style of Transaction Logic 
  - Uses XSB Prolog as inference engine
  - ErgoAI is open source
- KnowRob 2
  - Semisymbolic reasoning engine implemented in Prolog
  - KnowRob Query Language based on Prolog
  - MongoDB backend that stores both RDF triples and subsymbolic data (robot trajectories, ...)
  - Interfaces via Rosprolog, binary plugin system
- Standalone reasoners operating on OWL
  - MORe (Modular Reasoner) combines multiple reasoners (e.g., HermiT, ELK, RDFox) to classify ontologies by delegating to the most appropriate module @armas2012more
  
- Embedding Semantic Web data into object-oriented languages @OREN2008191 TODO 
- Supporting Object-Oriented Programming of Semantic-Web Software @quasthoff2011supporting TODO
- How To Simplify Building Semantic Web Applications @quasthoff2009simplify TODO
- Object-ontological mapping (OOM)
  - Surveys: @baset2018object @ledvinka2020comparison
  - Object-triple-mapping "defines the contract between the application and the underlying knowledge structure" @ledvinka2020comparison
  - Java OWL Persistence API (JOPA) @ledvinka2015jopa @ledvinka2016jopa does object-ontological mapping in Java
    - Has OntoDriver software layer that provides "object-oriented access to different storages" @ledvinka2015object
    - Object-UOBM benchmark for object-ontological mapping & storage performance @ledvinka2015object
  - Jastor @szekely2009jastor, based on the Jena @carroll2004jena semantic web framework, converts OWL to Java Objects
  - JASB (Java Architecture for Semantic Binding) @alcaraz2012towards 
  - KOMMA @wenzel2010komma
  - JOINT @HOLANDA20136469
  - Sapphire @stevenson2011sapphire 
  - RDFAlchemy in Python @DjangordftoolsRDFAlchemy2023, abandoned since 2012
- There is no currently maintained OOM tool or object-oriented KR&R framework in Python
- Example applications
  - Ontology-enabled planning for robotic disassembly (uses OTM to interface with knowledge): @hoebert2023ros

General phenomenon observed in literature research is that much of the technical KR&R infrastructure is not usable and/or maintained anymore @abicht2023owl, with some notable exceptions (e.g. JOPA @noauthor_kbss-cvutjopa_2025)

Todo: 
Add OWLAPY, OWLReady2, OWLAPI

#bibliography("bibliography.bib")