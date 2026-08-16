#!/usr/bin/env python3
"""Validate Cursor user rule .mdc files under .cursor/rules/."""

from __future__ import annotations

import sys
from pathlib import Path

RULES_DIR = Path(".cursor/rules")


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing opening frontmatter delimiter")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("missing closing frontmatter delimiter")

    data: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line!r}")
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip()
    return data


def main() -> int:
    if not RULES_DIR.is_dir():
        print(f"ERROR: {RULES_DIR} not found", file=sys.stderr)
        return 1

    rules = sorted(RULES_DIR.glob("*.mdc"))
    if not rules:
        print(f"ERROR: no .mdc files in {RULES_DIR}", file=sys.stderr)
        return 1

    failed = False
    for path in rules:
        try:
            frontmatter = parse_frontmatter(path.read_text(encoding="utf-8"))
        except ValueError as exc:
            print(f"FAIL {path}: {exc}", file=sys.stderr)
            failed = True
            continue

        missing = [key for key in ("description", "alwaysApply") if key not in frontmatter]
        if missing:
            print(f"FAIL {path}: missing keys: {', '.join(missing)}", file=sys.stderr)
            failed = True
            continue

        if frontmatter["alwaysApply"] not in {"true", "false"}:
            print(
                f"FAIL {path}: alwaysApply must be true or false, got {frontmatter['alwaysApply']!r}",
                file=sys.stderr,
            )
            failed = True
            continue

        if not frontmatter["description"]:
            print(f"FAIL {path}: description must not be empty", file=sys.stderr)
            failed = True
            continue

        print(f"OK {path}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
