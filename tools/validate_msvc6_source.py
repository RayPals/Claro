#!/usr/bin/env python3
"""Prevent VC6 handle/Win98 build-setting regressions without needing the SDK."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = (ROOT / 'src/claro.c').read_text()
    start = source.index('static int run_tests(')
    body = source[start:source.index('static int ', start + 20)]
    branches = re.search(r'#if defined\(_MSC_VER\) && _MSC_VER < 1300\s+(.*?)#else\s+(.*?)#endif\s+h = _findfirst', body, re.S)
    assert branches, 'Old MSVC needs its own long _findfirst handle before calling the CRT'
    legacy = re.sub(r'/\*.*?\*/', '', branches[1], flags=re.S)
    assert re.search(r'\blong h;', legacy) and 'intptr_t' not in legacy
    assert re.search(r'\bintptr_t h;', branches[2]), 'Preserve the modern pointer-sized handle'
    build = (ROOT / 'build98.bat').read_text()
    response = ROOT / 'build98.rsp'
    options = build + (response.read_text() if response.exists() else '')
    for option in ['/TC', '/ML', '/MACHINE:I386', '/SUBSYSTEM:CONSOLE,4.10', '/STACK:16777216']:
        assert option in options, ('Missing Windows 98 build setting', option)
    assert max(map(len, build.splitlines())) < 127, 'Keep COMMAND.COM command lines below its legacy length limit'
    assert '/Dintptr_t' not in options, 'Fix source rather than injecting a global type macro'
    for name in ['build98.bat', 'build98.rsp']:
        data = (ROOT / name).read_bytes()
        assert b'\r\n' in data and b'\n' not in data.replace(b'\r\n', b''), ('Use DOS line endings', name)
        assert len(Path(name).stem) <= 8
    assert 'cl @build98.rsp' in build
    assert not re.search(r'(?i)setlocal|exit /b|%~|\bwhere\b|&&|\|\|', build), 'Use COMMAND.COM-compatible batch syntax'
    assert 'build98.bat' in (ROOT / 'tools/build_distribution.py').read_text(), 'Include the legacy build script in source distributions'
    print('PASS: guarded VC6 CRT handle, modern handle, Win98 build settings and source packaging')


if __name__ == '__main__':
    main()
