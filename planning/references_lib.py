"""
Reads the paper's bibliography and its citations, for the reference checks (test_references.py and
check_references_online.py).
"""
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

PAPER = Path(__file__).resolve().parent.parent / "krrood_aamas_2027"
MAIN = PAPER / "main.tex"
BIB = PAPER / "references.bib"
CITE = re.compile(r"\\cite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{([^}]*)\}")


@dataclass
class Entry:
    key: str
    kind: str
    fields: dict[str, str] = field(default_factory=dict)

    def get(self, name: str) -> str:
        return self.fields.get(name, "").strip()


def _balanced(text: str, start: int) -> int:
    """Index just after the brace group or quoted string that starts at ``start``."""
    if text[start] == '"':
        return text.index('"', start + 1) + 1
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i + 1
    raise ValueError(f"unbalanced braces from {start}")


def _fields(body: str) -> dict[str, str]:
    fields, i = {}, 0
    while True:
        match = re.compile(r"\s*,?\s*([A-Za-z_-]+)\s*=\s*").match(body, i)
        if not match:
            return fields
        name, i = match.group(1).lower(), match.end()
        if body[i] in '{"':
            end = _balanced(body, i)
            value = body[i + 1:end - 1]
        else:
            end = re.compile(r"[^,}\s]*").match(body, i).end()
            value = body[i:end]
        fields[name] = re.sub(r"\s+", " ", value).strip()
        i = end


def read_bib(path: Path = BIB) -> list[Entry]:
    text = path.read_text()
    entries = []
    for match in re.finditer(r"@([A-Za-z]+)\s*\{\s*([^,\s]+)\s*,", text):
        kind = match.group(1).lower()
        if kind in ("comment", "string", "preamble"):
            continue
        end = _balanced(text, match.end() - len(match.group(0)) + match.group(0).index("{"))
        entries.append(Entry(match.group(2), kind, _fields(text[match.end():end - 1])))
    return entries


def citations(path: Path = MAIN) -> dict[str, list[str]]:
    """Every cited key with the sentences that cite it (LaTeX comments removed)."""
    text = "\n".join(re.sub(r"(?<!\\)%.*", "", line) for line in path.read_text().split("\n"))
    contexts: dict[str, list[str]] = {}
    for match in CITE.finditer(text):
        start = max(text.rfind(". ", 0, match.start()), text.rfind("\n\n", 0, match.start())) + 1
        stops = [i for i in (text.find(". ", match.end()), text.find("\n\n", match.end())) if i != -1]
        sentence = re.sub(r"\s+", " ", text[start:min(stops) + 1 if stops else len(text)]).strip()
        for key in match.group(1).split(","):
            contexts.setdefault(key.strip(), []).append(sentence)
    return contexts


def plain(value: str) -> str:
    """A field value without LaTeX braces, accents and commands, in lower case."""
    value = re.sub(r"\\(ss|ae|oe|aa|o|O|l|L|i|j)(?![A-Za-z])", lambda m: m.group(1), value)
    value = re.sub(r"\\[`'^\"~=.uvHtcdbk]\{?([A-Za-z])\}?", r"\1", value)
    value = re.sub(r"\\[A-Za-z]+\s*", " ", value)
    value = unicodedata.normalize("NFKD", value.replace("ß", "ss"))
    value = "".join(c for c in value if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[{}$\\]", "", value)).strip().lower()


def last_names(authors: str) -> list[str]:
    names = []
    for author in re.split(r"\s+and\s+", authors):
        author = plain(author)
        if not author or author == "others":
            continue
        names.append(author.split(",")[0].strip() if "," in author else author.split()[-1])
    return names
