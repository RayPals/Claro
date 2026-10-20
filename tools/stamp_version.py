#!/usr/bin/env python3
"""Stamp a development/release run once, using its current UTC date and time.

Run before building: python3 tools/stamp_version.py && make
Ordinary rebuilds and validation retain the stamp for reproducibility.
Historical release notes and changelog entries are deliberately not rewritten.
"""
from datetime import datetime, timezone
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CURRENT_DOCS = (
    "CURRENT_STATUS.md", "CLASSROOM_READINESS.md", "CLI.md", "SPEC.md",
    "FINAL_RELEASE_CHECKLIST.md", "WEB_SERVER_PLAN.md", "GRAPHICS.md",
    "PERFORMANCE.md", "COMPLETE_PLATFORM_ROADMAP.md", "SDL12.md",
    "V1_16_PACKAGES_PROJECTS.md",
)


def main():
    source = ROOT / "src/claro.c"
    match = re.search(r'#define CLARO_VERSION "Claro ([^"\n]+)"', source.read_text())
    if not match:
        raise SystemExit("Cannot find CLARO_VERSION; no files changed")
    previous = match.group(1)
    version = datetime.now(timezone.utc).strftime("v%Y.%m.%d.%H%M%S")
    paths = [source, ROOT / "README.md"]
    paths += sorted((ROOT / "tools").glob("*.py"))
    paths += [ROOT / "docs" / name for name in CURRENT_DOCS]
    updates = []
    for path in paths:
        if path == Path(__file__).resolve() or not path.exists():
            continue
        old = path.read_text(encoding="utf-8")
        new = old.replace(previous, version)
        if new != old:
            updates.append((path, new))
    for path, content in updates:
        path.write_text(content, encoding="utf-8")
    print(f"Claro {version} (UTC); updated {len(updates)} current source/docs/validator files")


if __name__ == "__main__":
    main()
