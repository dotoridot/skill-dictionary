"""Build the library and its standalone dictionaries."""
import html
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "public"
RENDERER = ROOT / "skills/skill-dictionary/scripts/render.py"


def build():
    library = []
    seen = set()
    for path in sorted((ROOT / "catalogs").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        slug = data["id"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or slug in seen:
            raise ValueError(f"Invalid or duplicate collection id in {path.name}")
        seen.add(slug)
        directory = OUTPUT / slug
        directory.mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, RENDERER, path, directory / "index.html"], check=True)
        library.append({key: data[key] for key in ("id", "title", "description")} | {
            "items": [{key: item.get(key) for key in ("id", "name", "summary", "category", "keywords")} for item in data["items"]]
        })
    if not library:
        raise ValueError("No catalogs found")
    template = (ROOT / "site/index.html").read_text(encoding="utf-8")
    encoded = json.dumps(library, ensure_ascii=False).replace("<", r"\u003c")
    links = "".join(f'<a class="collection" href="{d["id"]}/index.html"><span><strong>{html.escape(d["title"])}</strong><small>{html.escape(d["description"])}</small></span><b>{len(d["items"])}개 ↗</b></a>' for d in library)
    page = template.replace("<!--COLLECTIONS-->", links).replace("/*CATALOGS*/", encoded)
    (OUTPUT / "index.html").write_text(page, encoding="utf-8")


if __name__ == "__main__":
    build()
