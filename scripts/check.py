#!/usr/bin/env python3
"""Validate the lean-thinking skill package using only the standard library."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
SKILL = ROOT / "skills" / "lean-thinking" / "SKILL.md"
REQUIRED_FILES = (README, SKILL, ROOT / "LICENSE", ROOT / "assets" / "banner.png")
REQUIRED_README_TEXT = (
    ".agents/skills",
    ".claude/skills",
    "$lean-thinking",
    "python3 scripts/check.py",
)
REQUIRED_LINKS = {"assets/banner.png"}


def parse_frontmatter(text: str, failures: list[str]) -> tuple[dict[str, str], str]:
    match = re.match(r"\A---\n(?P<meta>.*?)\n---\n(?P<body>.*)\Z", text, re.DOTALL)
    if not match:
        failures.append("SKILL.md must have complete YAML frontmatter")
        return {}, text

    metadata: dict[str, str] = {}
    for line in match.group("meta").splitlines():
        if not line.strip():
            continue
        if ":" not in line:
            failures.append(f"invalid frontmatter line: {line!r}")
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key or not value:
            failures.append(f"empty frontmatter key or value: {line!r}")
            continue
        if key in metadata:
            failures.append(f"duplicate frontmatter key: {key}")
        metadata[key] = value
    return metadata, match.group("body")


def local_markdown_links(text: str) -> list[str]:
    links = re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text)
    return [link for link in links if not re.match(r"(?:https?://|mailto:|#)", link)]


def main() -> int:
    failures: list[str] = []

    for path in REQUIRED_FILES:
        if not path.is_file():
            failures.append(f"missing required file: {path.relative_to(ROOT)}")

    if not README.is_file() or not SKILL.is_file():
        return report(failures)

    readme = README.read_text(encoding="utf-8")
    skill = SKILL.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(skill, failures)

    if metadata.get("name") != "lean-thinking":
        failures.append("frontmatter name must be lean-thinking")
    description = metadata.get("description", "")
    if not description or "Use when" not in description:
        failures.append("frontmatter description must explain behavior and when to use it")
    if not body.strip():
        failures.append("SKILL.md needs nonempty instructions")

    for expected in REQUIRED_README_TEXT:
        if expected not in readme:
            failures.append(f"README.md is missing required text: {expected}")

    links = local_markdown_links(readme)
    for expected in REQUIRED_LINKS:
        if expected not in links:
            failures.append(f"README.md must link to {expected}")
    for link in links:
        path_text = unquote(link.split("#", 1)[0].split("?", 1)[0])
        if not path_text:
            continue
        target = ROOT / path_text
        if not target.exists():
            failures.append(f"broken local README link: {link}")

    for label, text in (("README.md", readme), ("SKILL.md", skill)):
        if "/Users/" in text:
            failures.append(f"{label} contains a private absolute path")
        if re.search(r"\b(?:TODO|TBD|FIXME)\b|<[^>]+>", text):
            failures.append(f"{label} contains an unfinished placeholder")

    return report(failures)


def report(failures: list[str]) -> int:
    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1
    print("PASS: lean-thinking package checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
