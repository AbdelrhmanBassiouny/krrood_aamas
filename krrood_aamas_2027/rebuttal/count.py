"""Print the character count of each reply in response.md (limit 2500)."""
import re, pathlib
text = (pathlib.Path(__file__).parent / "response.md").read_text()
for part in re.split(r"\n## ", text)[1:]:
    title, _, body = part.partition("\n")
    body = body.split("\n---")[0].strip()
    print(f"{len(body):5d} {'OK ' if len(body) <= 2500 else 'OVER'} {title}")
