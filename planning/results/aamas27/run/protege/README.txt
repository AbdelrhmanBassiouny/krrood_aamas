Protégé 5.6.7 + Pellet 2.2.0, run by hand on 2026-10-07 on the same PC (i7-13700, 64 GB, Ubuntu 24.04), outside
Docker, with the bundled OpenJDK 11.0.25, -Xmx28G (as README.md says) and a G1 GC log. Plug-ins: Pellet Reasoner
Plug-in 2.2.0 and Snap SPARQL Query 6.0.0 from the official Protégé plug-in registry, copied into plugins/
(checksums in plugins.sha256). Inputs: owl2bench_statements_unreasoned.rdf (sha256 8d387e66...) and
state/owl2bench_statements_reasoned.rdf (sha256 2e359818...), copied as 1_raw.rdf and 2_reasoned.rdf.

Each folder is one fresh Protégé started by measure.sh: protege.log (Protégé's log of the session), time.txt (GNU time,
peak RSS), rss.txt (RSS every 50 ms), gc.log (G1 GC log), jvm.conf, stdout.log.

  raw/              File -> Open 1_raw.rdf; Reasoner -> Pellet -> Start reasoner (loading 539 ms, Pellet 4023 ms).
  reasoned/         The same with 2_reasoned.rdf (loading 4084 ms, Pellet 12603 ms).
  queries/          2_reasoned.rdf, Start reasoner, then the queries in Snap SPARQL one at a time, in the order of
                    queries_for_snap_sparql.txt. Snap SPARQL logs "Evaluated BGP in N ms" per query (the time excludes
                    showing the results); cpu.txt (CPU time every 20 ms) was a fallback before this was found.
                    Q9 is rejected by Snap SPARQL's parser ("Encountered owl2bench:NonScience ... Expected one of:
                    Variable, Individual name"), as NonScience is declared as a class; tried several times, it is not
                    a copy error. Q20 (hasSameHomeTownWith) was still evaluating after more than 280 s at 100 % CPU and
                    13.4 GB RSS; Protégé was stopped (timeout; the limit is 60 s).
  queries_21_22/    A fresh Protégé for Q21 and Q22 (Pellet 13456 ms, Q21 46300 ms as the first query, Q22 616 ms).
  raw_rss_only/     A first raw session without the GC log (loading 510 ms, Pellet 4000 ms, peak RSS 5.39 GiB); not
                    used, as RSS with a 28 GB heap shows how lazily the JVM collects rather than what Pellet needs.
  raw_aborted_no_reasoner/  A session closed before the reasoner was started; not used.

The numbers of results that Snap SPARQL showed were noted by hand: all 16 answered queries return GraphDB's number
of answers (Q2 7421, Q3 55, Q4 2486, Q5 20, Q7 1684, Q8 6, Q10 666, Q11 2422, Q12 2494, Q13 0, Q14 0, Q15 21, Q16 21,
Q19 858, Q21 145, Q22 106). The answer sets themselves were not compared, as Protégé has no programmatic interface.

protege_heap_from_gc.py computes the times and the heap increase (heap after the last GC pause before the file is
opened, to the largest heap after a GC pause until Pellet has finished; an upper bound, as for GraphDB);
make_protege_json.py writes ../protege.json from it and the query log lines. Memory in the paper is the heap increase:
raw 20 -> 2975 MiB (+2955), reasoned 19 -> 3213 MiB (+3194).
