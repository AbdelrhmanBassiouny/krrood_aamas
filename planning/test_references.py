"""
Offline checks of the paper's references: every citation resolves, and every cited entry has the fields that the
ACM reference format prints for its type, without placeholder values. Whether an entry describes the right paper is
checked against Crossref and DBLP by check_references_online.py.

Usage: python3 -m pytest planning/test_references.py
"""
import re

import pytest

from references_lib import citations, read_bib, plain

ENTRIES = read_bib()
BY_KEY = {e.key: e for e in ENTRIES}
CITED = citations()
CITED_ENTRIES = [BY_KEY[k] for k in sorted(CITED) if k in BY_KEY]

# Fields the ACM reference format needs to print a complete reference, per entry type; "a|b" means either.
REQUIRED = {
    "article": ["author", "title", "journal", "year"],
    "inproceedings": ["author", "title", "booktitle", "year"],
    "incollection": ["author", "title", "booktitle", "publisher", "year"],
    "book": ["author|editor", "title", "publisher", "year"],
    "inbook": ["author|editor", "title", "chapter|pages", "publisher", "year"],
    "techreport": ["author", "title", "institution", "year"],
    "phdthesis": ["author", "title", "school", "year"],
    "misc": ["author|editor|key", "title", "year", "howpublished|url|note|eprint"],
    "software": ["author|editor|key", "title", "year", "url|howpublished"],
}
PLACEHOLDERS = re.compile(r"^(english|unknown|n/?a|tbd|todo|\?+)$", re.IGNORECASE)


def test_bibliography_has_no_duplicate_keys():
    keys = [e.key for e in ENTRIES]
    assert sorted({k for k in keys if keys.count(k) > 1}) == []


def test_every_citation_resolves():
    assert sorted(k for k in CITED if k not in BY_KEY) == []


@pytest.mark.parametrize("entry", CITED_ENTRIES, ids=lambda e: e.key)
def test_entry_type_is_known(entry):
    assert entry.kind in REQUIRED, f"{entry.key}: unchecked type @{entry.kind}"


@pytest.mark.parametrize("entry", CITED_ENTRIES, ids=lambda e: e.key)
def test_entry_has_required_fields(entry):
    missing = [f for f in REQUIRED.get(entry.kind, []) if not any(entry.get(a) for a in f.split("|"))]
    assert missing == [], f"{entry.key} (@{entry.kind}) lacks {missing}"


@pytest.mark.parametrize("entry", CITED_ENTRIES, ids=lambda e: e.key)
def test_entry_has_no_placeholder_values(entry):
    bad = {n: v for n, v in entry.fields.items() if not v.strip() or PLACEHOLDERS.match(plain(v))}
    assert bad == {}, f"{entry.key}: placeholder values {bad}"


@pytest.mark.parametrize("entry", CITED_ENTRIES, ids=lambda e: e.key)
def test_year_is_plausible(entry):
    assert re.fullmatch(r"(18|19|20)\d\d", entry.get("year")), f"{entry.key}: year {entry.get('year')!r}"
    assert int(entry.get("year")) <= 2026


@pytest.mark.parametrize("entry", [e for e in CITED_ENTRIES if e.get("pages")], ids=lambda e: e.key)
def test_page_range_is_well_formed(entry):
    pages = entry.get("pages")
    match = re.fullmatch(r"([A-Za-z]?\d+)(?:\s*--?\s*([A-Za-z]?\d+))?", pages)
    assert match, f"{entry.key}: pages {pages!r}"
    first, last = match.groups()
    if last and first.isdigit() and last.isdigit():
        assert int(first) < int(last), f"{entry.key}: page range {pages!r} is empty or reversed"


@pytest.mark.parametrize("entry", [e for e in CITED_ENTRIES if e.get("doi")], ids=lambda e: e.key)
def test_doi_is_bare(entry):
    assert re.fullmatch(r"10\.\d{4,9}/\S+", entry.get("doi")), f"{entry.key}: doi {entry.get('doi')!r}"


def test_cited_titles_are_distinct():
    titles = [plain(e.get("title")) for e in CITED_ENTRIES]
    assert sorted({t for t in titles if titles.count(t) > 1}) == []


@pytest.mark.parametrize("entry", CITED_ENTRIES, ids=lambda e: e.key)
def test_publisher_is_not_given_as_organization(entry):
    # The ACM format prints the publisher, not the organization (Google Scholar exports use the latter).
    assert not (entry.get("organization") and not entry.get("publisher")), f"{entry.key}: organization without publisher"


@pytest.mark.parametrize("entry", CITED_ENTRIES, ids=lambda e: e.key)
def test_preprints_and_web_pages_are_not_journals(entry):
    assert "arxiv" not in entry.get("journal").lower(), f"{entry.key}: arXiv given as a journal"
    assert not (entry.kind == "misc" and entry.get("journal")), f"{entry.key}: @misc with a journal field"


@pytest.mark.parametrize("entry", [e for e in CITED_ENTRIES if e.kind in ("article", "inproceedings", "incollection")],
                         ids=lambda e: e.key)
def test_published_work_has_doi_or_url(entry):
    # Venues that assign no DOIs (VLDB 1990, SEKE 2004, DBKDA 2015, the QR 2026 workshop) are listed explicitly.
    without_doi = {"hull1990ilog", "kalyanpur2004automatic", "ireland2015exposing", "bassiouny2026roles"}
    assert entry.get("doi") or entry.get("url") or entry.key in without_doi, f"{entry.key}: no DOI or URL"
