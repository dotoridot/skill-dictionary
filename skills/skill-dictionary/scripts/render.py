"""Render one portable Korean skill dictionary from an edited JSON catalog."""

import argparse
import base64
from bisect import bisect_left
import html
import json
import re
import unicodedata
from pathlib import Path
from urllib.parse import urlsplit


def required_text(record, key):
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key}: expected non-empty text")
    return value


def check_source(record, key):
    if key not in record or record[key] == "":
        return
    value = required_text(record, key)
    if "\\" in value or any(c.isspace() or unicodedata.category(c) in {"Cc", "Cf"} for c in value):
        raise ValueError(f"{key}: invalid character in URL")
    url = urlsplit(value)
    # Reading port checks both its numeric syntax and its range.
    if (url.port == 0 or url.scheme != "https" or not url.hostname
            or any(c in url.netloc for c in "@%<>^|")):
        raise ValueError(f"{key}: expected an HTTPS source without credentials")


def validate(catalog):
    required_text(catalog, "title")
    required_text(catalog, "id")
    items = catalog.get("items")
    if not isinstance(items, list) or not items:
        raise ValueError("items: expected a non-empty list")
    ids = set()
    for item in items:
        item_id = required_text(item, "id")
        if item_id in ids:
            raise ValueError(f"duplicate item id: {item_id}")
        ids.add(item_id)
        for field in ("name", "summary", "category"):
            required_text(item, field)
        for field in ("when", "example", "result", "avoid", "comparison"):
            if field in item and not isinstance(item[field], str):
                raise ValueError(f"{item_id}.{field}: expected text")
        for field in ("keywords", "related"):
            values = item.get(field, [])
            if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
                raise ValueError(f"{item_id}.{field}: expected a list of strings")
        check_source(item, "source")
        check_source(item, "exampleSource")
    for item in items:
        missing = set(item.get("related", [])) - ids
        if missing:
            raise ValueError(f"{item['id']}: unknown related id {sorted(missing)}")
    for scenario in catalog.get("scenarios", []):
        required_text(scenario, "title")
        check_source(scenario, "source")
        if not scenario.get("steps"):
            raise ValueError("scenario needs at least one step")
        for step in scenario["steps"]:
            if step["id"] not in ids:
                raise ValueError(f"unknown scenario step: {step['id']}")
            required_text(step, "note")


ASSETS = Path(__file__).resolve().parent.parent / "assets"


def style_document(page):
    # Embed the supplied font subsets so a downloaded dictionary works offline.
    def embed_font(match):
        raw = (ASSETS / match[1]).read_bytes()
        return "url(data:font/woff2;base64," + base64.b64encode(raw).decode("ascii") + ")"

    points = sorted({ord(char) for char in page})

    def used(rule):
        ranges = re.search(r"unicode-range:([^} ;]+)", rule)
        if not ranges:
            return True
        for span in ranges[1].split(","):
            ends = span.removeprefix("U+").split("-")
            start = bisect_left(points, int(ends[0], 16))
            if start < len(points) and points[start] <= int(ends[-1], 16):
                return True
        return False

    font_css = (ASSETS / "fonts.css").read_text(encoding="utf-8")
    rules = (rule for rule in re.findall(r"@font-face\s*\{[^}]+\}", font_css) if used(rule))
    fonts = re.sub(r"url\((fonts/[^)]+)\)", embed_font, "\n".join(rules))
    licenses = "\n".join(p.read_text(encoding="utf-8") for p in sorted((ASSETS / "fonts").glob("OFL-*.txt")))
    tokens = (ASSETS / "tokens.css").read_text(encoding="utf-8")
    theme = (ASSETS / "theme.js").read_text(encoding="utf-8")
    icon = base64.b64encode((ASSETS / "favicon.png").read_bytes()).decode("ascii")
    favicon = f'<link rel="icon" type="image/png" href="data:image/png;base64,{icon}">'
    head = f"{favicon}\n<style>/*{licenses}*/\n{fonts}\n{tokens}</style>\n<script>{theme}</script>"
    return page.replace("<!--DOCPILOT_HEAD-->", head, 1)


def render(catalog):
    validate(catalog)
    template = (Path(__file__).resolve().parent.parent / "assets" / "dictionary.html").read_text(encoding="utf-8")
    item_fields = (
        "id", "name", "summary", "category", "when", "example", "result", "avoid",
        "comparison", "related", "keywords", "source", "exampleSource",
    )
    public_data = {
        "items": [{key: item[key] for key in item_fields if key in item} for item in catalog["items"]],
        "scenarios": [],
    }
    if catalog.get("home") == "../":
        public_data["home"] = "../"
    for scenario in catalog.get("scenarios", []):
        public_scenario = {key: scenario[key] for key in ("title", "source") if key in scenario}
        public_scenario["steps"] = [{"id": step["id"], "note": step["note"]} for step in scenario["steps"]]
        public_data["scenarios"].append(public_scenario)
    replacements = {
        "TITLE": html.escape(catalog["title"]),
        "DESCRIPTION": html.escape(catalog.get("description", "")),
        "DATA": json.dumps(public_data, ensure_ascii=False, separators=(",", ":")).replace("<", r"\u003c"),
    }
    return style_document(re.sub(r"@@(TITLE|DESCRIPTION|DATA)@@", lambda token: replacements[token[1]], template))


def main():
    args = argparse.ArgumentParser(description=__doc__)
    args.add_argument("catalog", type=Path)
    args.add_argument("output", type=Path)
    options = args.parse_args()
    try:
        document = render(json.loads(options.catalog.read_text(encoding="utf-8")))
    except (ValueError, KeyError, TypeError) as error:
        args.error(str(error))
    options.output.parent.mkdir(parents=True, exist_ok=True)
    options.output.write_text(document, encoding="utf-8")


if __name__ == "__main__":
    main()
