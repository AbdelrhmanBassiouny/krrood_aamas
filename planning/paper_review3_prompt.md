Handle my 21 review comments on draft 3 of the KRROOD paper (AAMAS 2027, Hanoi). Discuss and challenge them; don't apply them blindly. The deadline is 2026-10-08.

## Files
- Paper: /home/bass/Projects/krrood_aamas/krrood_aamas_2027/main.tex, plus references.bib, figures/overview.tex (TikZ standalone source of figures/overview.pdf) and tables/*.tex (placeholders: red \tbd marks the numbers from tomorrow's experiment run; leave them).
- Annotated draft: /home/bass/Projects/krrood_aamas/planning/krrood_aamas27_draft_review3.pdf
- Scratchpad of the previous session (read and run from it, don't delete anything): SP=/tmp/claude-1000/-home-bass-Projects-krrood-aamas/33ba4645-d3a6-450c-b474-694a7d4a326f/scratchpad
  - Extract the comments: `env -u PYTHONPATH $SP/venv/bin/python $SP/annots.py <pdf>`. #4 is an empty text note; look at where it sits.
  - Build: `bash $SP/build.sh`. It uses an isolated texmf with the libertine, inconsolata and newtx fonts, and writes $SP/build/main.pdf. A build passes when there are no "!" errors and "undefined refs: 0". The content must fit in 8 pages, with references after; currently "Future work" ends on page 8.
  - Code the listings must match (origin/main syntax): worktree $SP/cram_main with venv $SP/venv_main. Listing tests: `cd $SP/listings && env -u PYTHONPATH PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 $SP/venv_main/bin/python -m pytest -q test_listings.py` (14 pass, 3 strict xfail on known EQL bugs being fixed elsewhere). If you change or add a listing, add or adjust its test.
  - Ontomatic as used in the experiments: $SP/exp/cram (branch aamas27-experiments), file krrood/src/krrood/ontomatic/ontology_to_python/owl_instances_loader.py and property_descriptor/property_descriptor_relation.py. These are READ ONLY: another session is changing them.
  - Backups of earlier paper versions: $SP/main.orig.tex, $SP/main.before_review3.tex.

## How to work
1. Extract all comments. For each one, write a short response: what you'll change, or why you disagree, grounded in the code or the literature (verify every reference you add; no invented citations).
2. Comments #1, #2 and #3 change the framing: robots and cognitive architectures as the motivation, ORMatic as its own contribution with EQL-to-SQL, and computable predicates as the reason for the design. Present a concrete plan for them first: the new abstract and intro outline, the contribution list, and what moves or gets cut to stay within 8 pages. Wait for my answer before applying them. Apply the other comments directly.
3. Every claim must be true of the code and of what was measured:
   - The experiments' SQL queries were hand-written with SQLAlchemy; they were not produced by the EQL-to-SQL translator.
   - The translator (grep for EQLTranslator in $SP/cram_main/krrood/src/krrood) supports only a subset of EQL. Check what it supports before claiming anything about it. Any new performance claim needs a measurement or a citation.
   - #19 asks whether the loading listing (lst:loading) is faithful to owl_instances_loader.py. Check it line by line against that file and explain or fix it.
4. Constraints:
   - Keep one theme: how ontological knowledge is represented in KRROOD and reasoned with.
   - Clean, correct, smooth reading, no clutter, explained with examples.
   - Double-blind: no identifying self-citations or "our previous work".
   - American spelling.
   - Keep the conventions already in use: booktabs tables, captions above tables, the eql listing style.
   - #5 (the figure): edit figures/overview.tex, rebuild overview.pdf with pdflatex using the same TEXMFHOME/TEXMFVAR/TEXMFCONFIG exports as build.sh, and look at the result as an image before keeping it.
5. Coordination: another session is fixing Ontomatic so that every derived fact is stored on an object of its individual that declares the property. Do NOT rewrite these two passages; I'll bring their new text from the other session:
   - the 4th bullet of "The converse, completeness, does not hold in general, for four reasons";
   - the sentences about the 4,037 property assertions in Section "Correctness".

   You may move them or shorten the text around them.
6. When done:
   - build;
   - check page count, overfull boxes and undefined references;
   - run the listing tests;
   - save the PDF as /home/bass/Projects/krrood_aamas/planning/krrood_aamas27_draft_review4.pdf and send it to me;
   - give me a table of comment number, what changed, and any pushback.

   Don't commit or push anything without asking.
