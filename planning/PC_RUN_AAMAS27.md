# AAMAS 2027: the measured run

Everything for the run is in the supplementary zip, `planning/krrood-aamas27-supplement.zip`: the code, the data,
the Docker set-up and the instructions (`README.md` in the zip). Anyone, us or a reviewer, follows that README.
This file only says how we use it.

## Run (on the Ubuntu PC, i7-11700K, 32 GB RAM)

```bash
unzip -DD krrood-aamas27-supplement.zip && cd krrood-aamas27-supplement
bash run_ubuntu.sh            # set up, then the full run in the background (9-13 h)
bash run_ubuntu.sh status     # any time
```

Then Protégé by hand (README, "Protégé (by hand)"), and `bash run_ubuntu.sh tables`.

Rules for a Claude Code session on the PC: change no file of the bundle, don't change limits or repetitions,
don't use the machine during the run, and stop and report if a step fails.

## Hand back and import

The results are one file, `krrood-aamas27-supplement/state/aamas27_results.tgz`. Copy it to the laptop (Google
Drive or USB stick), then:

```bash
bash planning/import_results.sh /path/to/aamas27_results.tgz
```

It checks the run, prints the BUNDLE id (it must be the zip's, `environment/BUNDLE`) and copies the two LaTeX
tables into `krrood_aamas_2027/tables/`. The final zip is built with
`make_supplement.py <out> --results planning/results/aamas27/run` from `supplement/` of the experiments repository
(branch `aamas27-experiments`).
