# Camera-ready promises in the response (internal, not for posting)

Every promise in `response.md` and the plan item that delivers it (plan `krrood-aamas27-rebuttal`).
No new numbers are in the response: any number not ready by the evening of 23 November is promised, never estimated.

| Promise | Where in the response | Delivered by |
|---|---|---|
| 1. One pinned version for listings, proofs and experiments; every experiment rerun | 7FxR | `revision-commits-to-main`, `ontomatic-on-main`, `ontomatic-paper-check`, `experiments-on-current-version`, `owl2bench-rerun`, `proofs-on-current-version` |
| 2. Proof sketch or key invariant in the main text | 7FxR | `proofs-on-current-version`, `paper-revision` |
| 3. Full loading time and memory without step 5, in Table 2 (Section 7.2 gives only "over two hours") | 7FxR (A), MnFm, HKHa | `owl2bench-rerun` (the eager-closure ablation flag already exists in Ontomatic) |
| 4. Reflection listing (EQL over the agent's own queries, rules and planner calls), framed by Newell's knowledge level. The response shows its core, a query that finds the agent's queries calling CanReach; tested on the fork's `aamas27-unification-revision` (krrood 26.7.0) | HKHa, sSAi | `reflection-listing` |
| 5. Closed-world claim stated in the introduction and the discussion; three kinds of fact and which can become stale; agent-loop claim scoped | HKHa, MnFm, 7FxR (B) | `paper-revision` |
| 6. Citations in the introduction, related work stating what KRROOD adds per group of systems, full sentences in Section 3 and elsewhere, novelty paragraph, narrower title, "1.42 million of which are assertions", rela-model citation, trimmed references | sSAi, MnFm | `paper-revision` |

Not promised (the benchmark and future-work points are argued in the replies to HKHa, 7FxR and MnFm):

- A second benchmark. The replies defend OWL2Bench and do not mention LUBM, which no reviewer raised. No LUBM numbers exist, the LUBM test is skipped on the current code, it waits on the Ontomatic port, and LUBM lies outside OWL 2 RL. `lubm-evaluation` can still be done for the camera-ready if time allows, as a bonus, not a promise.
- The retraction variant of the agent loop. Replaced by stating the three kinds of fact in the paper. `retraction-agent-loop` becomes optional.
- Open-world semantics, a query planner, incremental retraction (future work), and the Legal BERT reference (declined).
