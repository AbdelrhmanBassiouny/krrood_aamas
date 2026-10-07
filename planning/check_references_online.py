"""
Compares every cited bibliography entry with Crossref and DBLP: the title, the authors' last names, the year and the
venue. It prints one line per entry and a list of the entries that need a look; entries that neither service lists
(W3C recommendations, software, some books) are reported as not found and must be checked by hand.

Usage: python3 planning/check_references_online.py [--cache FILE] [--json OUT]
"""
import argparse
import difflib
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path

from references_lib import citations, last_names, plain, read_bib

VENUE_FIELDS = ("journal", "booktitle", "publisher", "institution", "school", "howpublished")


def fetch(url: str, cache: dict) -> dict | None:
    if url in cache:
        return cache[url]
    request = urllib.request.Request(url, headers={"User-Agent": "krrood-reference-check/1.0"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                cache[url] = json.load(response)
                time.sleep(0.5)
                return cache[url]
        except urllib.error.HTTPError as error:
            if error.code == 404:
                cache[url] = None
                return None
            time.sleep(2 * (attempt + 1))
        except Exception:
            time.sleep(2 * (attempt + 1))
    return None


def similarity(a: str, b: str) -> float:
    a, b = re.sub(r"[^a-z0-9 ]", "", plain(a)), re.sub(r"[^a-z0-9 ]", "", plain(b))
    return difflib.SequenceMatcher(None, a, b).ratio()


def crossref_candidates(entry, cache) -> list[dict]:
    if entry.get("doi"):
        found = fetch("https://api.crossref.org/works/" + urllib.parse.quote(entry.get("doi")), cache)
        if found:
            return [found["message"]]
    query = urllib.parse.urlencode({"query.bibliographic": f"{plain(entry.get('title'))} "
                                    f"{' '.join(last_names(entry.get('author'))[:2])}", "rows": 3})
    found = fetch("https://api.crossref.org/works?" + query, cache)
    return found["message"]["items"] if found else []


def dblp_candidates(entry, cache) -> list[dict]:
    query = urllib.parse.urlencode({"q": plain(entry.get("title")), "format": "json", "h": 3})
    found = fetch("https://dblp.org/search/publ/api?" + query, cache)
    hits = (found or {}).get("result", {}).get("hits", {}).get("hit", [])
    return [h["info"] for h in hits]


def normalize(record: dict, source: str) -> dict:
    if source == "crossref":
        authors = [a.get("family", a.get("name", "")) for a in record.get("author", [])]
        year = (record.get("issued", {}).get("date-parts") or [[None]])[0][0]
        venue = " / ".join((record.get("container-title") or []) + [record.get("publisher", "")])
        return {"source": source, "title": " ".join(record.get("title") or [""]), "authors": authors,
                "year": year, "venue": venue, "doi": record.get("DOI", ""), "pages": record.get("page", ""),
                "type": record.get("type", "")}
    authors = record.get("authors", {}).get("author", [])
    authors = [authors] if isinstance(authors, dict) else authors
    return {"source": source, "title": record.get("title", ""), "authors":
            [re.sub(r"\s\d{4}$", "", a["text"]).split()[-1] for a in authors],
            "year": int(record["year"]) if record.get("year") else None, "venue": record.get("venue", ""),
            "doi": record.get("doi", ""), "pages": record.get("pages", ""), "type": record.get("type", "")}


def compare(entry, record: dict) -> dict:
    ours = [n.split()[-1] for n in last_names(entry.get("author") or entry.get("editor"))]
    theirs = [plain(a).split()[-1] for a in record["authors"] if a]
    shared = {n for n in ours if any(similarity(n, t) > 0.85 for t in theirs)}
    year = int(entry.get("year")) if entry.get("year").isdigit() else None
    return {
        "title": round(similarity(entry.get("title"), record["title"]), 2),
        "authors": f"{len(shared)}/{len(ours)} of ours, {len(theirs)} listed",
        "authors_ok": bool(ours) and len(shared) == len(ours) and (len(theirs) == len(ours)
                                                                   or "others" in entry.get("author")),
        "year_ok": year is not None and record["year"] is not None and abs(year - record["year"]) <= 1,
        "year_exact": year == record["year"],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", type=Path, default=Path("/tmp/krrood_reference_cache.json"))
    parser.add_argument("--json", type=Path)
    args = parser.parse_args()
    cache = json.loads(args.cache.read_text()) if args.cache.exists() else {}
    by_key = {e.key: e for e in read_bib()}
    report = []
    for key in sorted(citations()):
        entry = by_key[key]
        records = [normalize(r, "crossref") for r in crossref_candidates(entry, cache)]
        records += [normalize(r, "dblp") for r in dblp_candidates(entry, cache)]
        args.cache.write_text(json.dumps(cache))
        best = max(records, key=lambda r: similarity(entry.get("title"), r["title"]), default=None)
        result = {"key": key, "kind": entry.kind, "title": entry.get("title"), "year": entry.get("year"),
                  "authors": entry.get("author") or entry.get("editor"),
                  "venue": next((entry.get(f) for f in VENUE_FIELDS if entry.get(f)), ""),
                  "pages": entry.get("pages"), "doi": entry.get("doi"), "match": best}
        if best and similarity(entry.get("title"), best["title"]) >= 0.9:
            result["check"] = compare(entry, best)
            problems = [p for p, ok in (("authors", result["check"]["authors_ok"]),
                                        ("year", result["check"]["year_exact"])) if not ok]
            result["status"] = "ok" if not problems else "check " + ", ".join(problems)
        else:
            result["status"] = "not found"
        report.append(result)
        print(f"{key:<32} {result['status']:<22} "
              f"{(best or {}).get('source', '')}: {(best or {}).get('venue', '')[:60]}", flush=True)
    if args.json:
        args.json.write_text(json.dumps(report, indent=1))
    print("\nneed a look:", [r["key"] for r in report if r["status"] != "ok"])


if __name__ == "__main__":
    main()
