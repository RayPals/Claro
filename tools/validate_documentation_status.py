#!/usr/bin/env python3
"""Check active status/navigation without treating historical claims as current."""
import ast
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = (
    'README.md', 'docs/README.md', 'docs/CURRENT_STATUS.md',
    'docs/RELEASE_STATUS.md', 'docs/FINAL_RELEASE_CHECKLIST.md',
    'docs/CLASSROOM_READINESS.md', 'docs/TESTING.md', 'docs/HARDENING.md',
    'docs/PORTABILITY.md', 'docs/RELIABILITY.md',
    'docs/history/CURRENT_STATUS_BEFORE_STATUS_CLEANUP.md',
    'docs/history/HARDENING_BEFORE_STATUS_CLEANUP.md',
)


def validate():
    match = re.search(r'#define CLARO_VERSION "Claro ([^"]+)"',
                      (ROOT / 'src/claro.c').read_text())
    assert match, 'Missing runtime version'
    version = match.group(1)
    readme = (ROOT / 'README.md').read_text()
    assert 'Current release:' not in readme, 'A development stamp is not a published release'
    assert f'Development version: **{version}**' in readme, 'README must match the runtime development stamp'
    status = (ROOT / 'docs/CURRENT_STATUS.md').read_text()
    assert version in status and 'RELEASE_STATUS.md' in status
    assert len(status.splitlines()) <= 100, 'Keep the current status concise; archive detailed history'
    assert 'not a sandbox' in status.lower()
    release = (ROOT / 'docs/RELEASE_STATUS.md').read_text()
    assert 'not published' in release.lower() and 'wine' in release.lower()
    assert 'unverified' in release.lower() and 'MSVC600' in release
    checklist = (ROOT / 'docs/FINAL_RELEASE_CHECKLIST.md').read_text()
    assert 'v1.xx.yy' not in checklist and 'vYYYY.MM.DD.HHMMSS' in checklist
    assert '[ ]' in checklist, 'Release actions must be explicit, unchecked gates'
    classroom = (ROOT / 'docs/CLASSROOM_READINESS.md').read_text().lower()
    assert 'learner testing' in classroom and 'not yet validated' in classroom
    hardening = (ROOT / 'docs/HARDENING.md').read_text()
    assert 'historical' in hardening.lower() and 'RELIABILITY.md' in hardening
    for name in ['CURRENT_STATUS_BEFORE_STATUS_CLEANUP.md', 'HARDENING_BEFORE_STATUS_CLEANUP.md']:
        assert (ROOT / 'docs/history' / name).is_file(), ('Missing historical record', name)
    tree = ast.parse((ROOT / 'tools/stamp_version.py').read_text())
    current_docs = next(ast.literal_eval(n.value) for n in tree.body
                        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'CURRENT_DOCS' for t in n.targets))
    assert 'RELEASE_STATUS.md' not in current_docs, 'Do not re-stamp immutable verification checkpoints'
    checked = 0
    for name in ACTIVE:
        path = ROOT / name
        text = re.sub(r'```.*?```', '', path.read_text(), flags=re.S)
        for target in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)\)', text):
            url = urlsplit(target)
            if url.scheme or url.netloc or not url.path:
                continue
            destination = (path.parent / unquote(url.path)).resolve()
            assert destination.is_relative_to(ROOT), (name, 'Link leaves the repository', target)
            assert destination.exists(), (name, 'Broken local link', target)
            checked += 1
    print(f'PASS: development/release separation, archived history, claim scope, and {checked} local documentation links')


if __name__ == '__main__':
    validate()
