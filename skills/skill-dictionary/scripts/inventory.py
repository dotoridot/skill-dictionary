"""List source hashes for editorial reconciliation. Never executes source skills."""
import argparse
import hashlib
import json
from pathlib import Path


def collect(root):
    root = root.resolve(strict=True)
    rows = {}
    for source in sorted(root.rglob("SKILL.md")):
        relative = source.relative_to(root)
        if any(part.startswith(".") or part in {"node_modules", "__pycache__"} for part in relative.parts):
            continue
        if not source.resolve().is_relative_to(root):
            continue
        rows[relative.as_posix()] = hashlib.sha256(source.read_bytes()).hexdigest()
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    args = parser.parse_args()
    print(json.dumps(collect(args.root), ensure_ascii=False, indent=2))
