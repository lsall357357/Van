#!/usr/bin/env python3
"""Lightweight validation for the early-stage startup problem finder skill."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_FILES = [
    "SKILL.md",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "SECURITY.md",
    "agents/openai.yaml",
    "examples/test-prompts.md",
    "references/output-recipes.md",
    "references/bp-screening-rubric.md",
    "references/file-input-guide.md",
    "references/follow-up-routing.md",
    "references/funding-path-map.md",
    "references/fundraising-meeting-playbook.md",
    "references/investor-question-bank.md",
    "references/narrative-recipes.md",
    "references/restricted-finance-questions.md",
    "references/safety-rules.md",
]

FORBIDDEN_PATH_NAMES = {
    "listing-" + "copy.md",
    ".DS_Store",
}

FORBIDDEN_TEXT = [
    "Red" + "Hub",
    "小" + "红书",
    "会话" + "ID",
    "会话 " + "ID",
    "019" + "e",
    "listing-" + "copy.md",
]

LOCAL_WORKSPACE_PREFIX = str(Path.home()) + "/Documents/Codex/media"

REQUIRED_TEXT = [
    "material-grounded intake",
    "价值锚点",
    "商业模式",
    "融资故事",
    "Must not write BP copy",
    "references/output-recipes.md",
    "references/safety-rules.md",
]

SKIP_DIRS = {
    ".git",
    ".cache",
    "__pycache__",
    "dist",
    "tmp",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def iter_source_files(root: Path):
    for path in root.rglob("*"):
        rel_parts = path.relative_to(root).parts
        if any(part in SKIP_DIRS for part in rel_parts):
            continue
        yield path


def validate_frontmatter(skill_md: Path, errors: list[str]) -> None:
    text = read_text(skill_md)
    if not text.startswith("---\n"):
        errors.append("SKILL.md must start with YAML frontmatter.")
        return
    try:
        _, frontmatter, _ = text.split("---", 2)
    except ValueError:
        errors.append("SKILL.md frontmatter is not closed.")
        return
    if "name: early-stage-startup-problem-finder" not in frontmatter:
        errors.append("SKILL.md frontmatter name is missing or incorrect.")
    if "description:" not in frontmatter:
        errors.append("SKILL.md frontmatter description is missing.")
    if "[TODO" in text:
        errors.append("SKILL.md still contains TODO text.")


def validate_references(root: Path, errors: list[str]) -> None:
    text = read_text(root / "SKILL.md")
    refs = sorted(set(re.findall(r"`(references/[^`]+)`", text)))
    for ref in refs:
        if not (root / ref).exists():
            errors.append(f"Missing referenced file: {ref}")


def validate_files(root: Path, errors: list[str]) -> None:
    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            errors.append(f"Missing required file: {rel}")
    for path in iter_source_files(root):
        if path.name in FORBIDDEN_PATH_NAMES:
            errors.append(f"Forbidden file present: {path.relative_to(root)}")
        if path.is_file() and path.suffix in {".zip", ".skill"}:
            errors.append(f"Generated archive should not be committed: {path.relative_to(root)}")


def validate_content(root: Path, errors: list[str]) -> None:
    combined_parts = []
    for path in iter_source_files(root):
        if path.is_file() and path.suffix in {".md", ".yaml", ".py", ""}:
            try:
                combined_parts.append(read_text(path))
            except UnicodeDecodeError:
                errors.append(f"Non-UTF-8 file: {path.relative_to(root)}")
    combined = "\n".join(combined_parts)
    for needle in FORBIDDEN_TEXT:
        if needle in combined:
            errors.append(f"Forbidden text found: {needle}")
    if LOCAL_WORKSPACE_PREFIX in combined:
        errors.append("Forbidden local workspace path found.")
    for needle in REQUIRED_TEXT:
        if needle not in combined:
            errors.append(f"Required text missing: {needle}")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    errors: list[str] = []
    validate_files(root, errors)
    if (root / "SKILL.md").exists():
        validate_frontmatter(root / "SKILL.md", errors)
        validate_references(root, errors)
    validate_content(root, errors)

    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Skill package validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
