#!/usr/bin/env python3
"""Create a distributable zip archive for the skill."""

from __future__ import annotations

import sys
import zipfile
from pathlib import Path


EXCLUDED_NAMES = {
    ".DS_Store",
    "__pycache__",
    ".git",
    ".cache",
    "tmp",
    "dist",
    "listing-" + "copy.md",
}

EXCLUDED_SUFFIXES = {
    ".pyc",
    ".zip",
    ".skill",
}


def should_include(path: Path, root: Path) -> bool:
    rel_parts = path.relative_to(root).parts
    if any(part in EXCLUDED_NAMES for part in rel_parts):
        return False
    if path.suffix in EXCLUDED_SUFFIXES:
        return False
    return path.is_file()


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not (root / "SKILL.md").exists():
        print("SKILL.md not found. Run this script from the skill root or pass the skill path.")
        return 1

    dist = root / "dist"
    dist.mkdir(exist_ok=True)
    output = dist / f"{root.name}.zip"

    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(root.rglob("*")):
            if should_include(path, root):
                archive.write(path, path.relative_to(root))

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
