"""Render one portable Korean skill dictionary from an edited JSON catalog."""

import argparse
import html
import json
import re
from pathlib import Path
from urllib.parse import urlsplit


def required_text(record, key):
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key}: expected non-empty text")
    return value


def check_source(record, key):
    if record.get(key):
        url = urlsplit(required_text(record, key))
        if url.scheme != "https" or not url.hostname or url.username or url.password:
            raise ValueError(f"{key}: expected a public HTTPS source")


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


def render(catalog):
    validate(catalog)
    template = (Path(__file__).resolve().parent.parent / "assets" / "dictionary.html").read_text(encoding="utf-8")
    replacements = {
        "TITLE": html.escape(catalog["title"]),
        "DESCRIPTION": html.escape(catalog.get("description", "")),
        "DATA": json.dumps(catalog, ensure_ascii=False, separators=(",", ":")).replace("<", r"\u003c"),
    }
    return re.sub(r"@@(TITLE|DESCRIPTION|DATA)@@", lambda token: replacements[token[1]], template)


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
