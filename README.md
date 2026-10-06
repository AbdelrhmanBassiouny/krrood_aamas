  # KRROOD — AAMAS 2027

LaTeX sources for the AAMAS 2027 submission of KRROOD (*Implementing Knowledge Representation and Reasoning with Object Oriented Design*), ported from the arXiv version ([arXiv:2601.14840](https://arxiv.org/abs/2601.14840)) into the AAMAS 2027 template.

## Layout

- [krrood_aamas_2027/main.tex](krrood_aamas_2027/main.tex) — paper source (AAMAS 2027 template, `sigconf,anonymous`)
- [krrood_aamas_2027/references.bib](krrood_aamas_2027/references.bib) — bibliography
- [krrood_aamas_2027/figures/](krrood_aamas_2027/figures/) — figures
- [krrood_aamas_2027/aamas.cls](krrood_aamas_2027/aamas.cls), [krrood_aamas_2027/ACM-Reference-Format.bst](krrood_aamas_2027/ACM-Reference-Format.bst), [krrood_aamas_2027/by.pdf](krrood_aamas_2027/by.pdf) — AAMAS 2027 style files
- [aamas_2027_template/](aamas_2027_template/) — the unmodified AAMAS 2027 template, kept for reference
- [krrood_ijcai/](krrood_ijcai/) — earlier IJCAI and DKE sources the paper was ported from
- [krrood_arxiv.pdf](krrood_arxiv.pdf) — the arXiv version the content follows

The submission is anonymized via the `anonymous` class option. For the camera-ready version, remove that option and set `\acmSubmissionID`.

## Building locally

Requires a TeX Live installation with `latexmk`:

```bash
cd krrood_aamas_2027
latexmk -pdf main.tex
```

## Continuous integration

[.github/workflows/build-paper.yml](.github/workflows/build-paper.yml) compiles `krrood_aamas_2027/main.tex` on every push and pull request and uploads the resulting PDF as a build artifact. On pushes to `main` it also publishes the PDF to GitHub Pages.

Once Pages is enabled (Settings → Pages → Source: "GitHub Actions"), the compiled paper is always available, up to date with `main`, at:

https://sorinar329.github.io/krrood_aamas/
