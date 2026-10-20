#!/usr/bin/env python3
"""Build clean source/Linux-musl/Windows-x64 archives from the current tree."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DIRECTORIES = ['.forgejo', 'src', 'docs', 'lessons', 'examples', 'lib', 'tests', 'tools', 'assets', 'support']
FILES = ['README.md', 'LICENSE', 'CHANGELOG.md', 'CONTRIBUTING.md', 'Makefile', 'build.bat', 'build.ps1', 'build98.bat', 'build98.rsp', 'run_tests.bat']
FLAGS = ['-std=c89', '-pedantic-errors', '-Werror=implicit-function-declaration', '-O2', '-static']


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target', required=True, choices=['source', 'linux-x86_64', 'windows-x86_64'])
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    match = re.search(r'#define CLARO_VERSION "Claro (v[^"]+)"', (ROOT / 'src/claro.c').read_text())
    if match is None:
        raise SystemExit('Cannot read the runtime version from src/claro.c')
    version = match[1]
    args.output.mkdir(parents=True, exist_ok=True)
    name = f'Claro-{version}-{args.target}'
    destination = args.output / (name + '.zip')
    if destination.exists():
        raise SystemExit(f'Refusing to replace existing archive: {destination}')
    with tempfile.TemporaryDirectory(prefix='claro-package-', dir=os.environ.get('TMPDIR')) as tmp:
        stage = Path(tmp) / name
        stage.mkdir()
        for directory in DIRECTORIES:
            for source in sorted((ROOT / directory).rglob('*')):
                if not source.is_file() or source.is_symlink() or '__pycache__' in source.parts or source.suffix in ['.pyc', '.o']:
                    continue
                target = stage / source.relative_to(ROOT)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
        for filename in FILES:
            shutil.copy2(ROOT / filename, stage / filename)
        command = []
        compiler = None
        if args.target != 'source':
            if args.target == 'linux-x86_64':
                if platform.machine().lower() not in ['x86_64', 'amd64']:
                    raise SystemExit('Linux x64 package requires an x86-64 musl toolchain')
                compiler, executable = 'musl-gcc', 'claro'
                notices = {'musl.txt': '/usr/share/doc/musl/copyright', 'GCC-runtime.txt': '/usr/share/doc/gcc-15-base/copyright'}
            else:
                compiler, executable = 'x86_64-w64-mingw32-gcc', 'claro.exe'
                notices = {'MinGW-runtime.txt': '/usr/share/doc/mingw-w64-common/copyright', 'GCC-runtime.txt': '/usr/share/doc/gcc-mingw-w64-x86-64-win32/copyright'}
            if not shutil.which(compiler):
                raise SystemExit(f'Missing distribution compiler: {compiler}')
            command = [compiler] + FLAGS + ['src/claro.c', '-o', executable, '-lm']
            if args.target == 'windows-x86_64':
                command += ['-Wl,--stack,16777216']
            subprocess.run(command, cwd=stage, check=True)
            third_party = stage / 'THIRD_PARTY_NOTICES'
            third_party.mkdir()
            for filename, source in notices.items():
                if not Path(source).is_file():
                    raise SystemExit(f'Missing required toolchain notice: {source}')
                shutil.copy2(source, third_party / filename)
        metadata = {'version': version, 'target': args.target, 'source_sha256': sha256(stage / 'src/claro.c'), 'build_command': command}
        if compiler:
            metadata['compiler'] = subprocess.check_output([compiler, '--version'], text=True).splitlines()[0]
        (stage / 'DISTRIBUTION.json').write_text(json.dumps(metadata, indent=2) + '\n')
        start = 'Extract this entire archive before using Claro. Open a terminal in the extracted folder.\n\n'
        if args.target == 'windows-x86_64':
            start += 'Run: .\\claro.exe lessons\\01_hello.claro\nThis is a genuine Windows x64 executable, not the Linux build with an .exe suffix.\n'
        elif args.target == 'linux-x86_64':
            start += 'Run: ./claro lessons/01_hello.claro\nIf extraction removed execute permission: chmod +x claro\nThis is a static musl build; it does not require the builder host glibc.\n'
        else:
            start += 'Build: make\nOr compile src/claro.c directly with the strict C89 command in README.md.\nOn Windows, use build.bat/build.ps1; the executable needs the documented stack reserve.\n'
        start += '\nRead docs/QUICK_START.md and docs/PORTABILITY.md. Run only trusted scripts.\nReal HTTP requires curl; the basic lessons and offline networking need no network.\n'
        (stage / 'START_HERE.txt').write_text(start)
        entries = {str(path.relative_to(stage)).replace(os.sep, '/'): sha256(path) for path in sorted(stage.rglob('*')) if path.is_file()}
        (stage / 'MANIFEST.json').write_text(json.dumps({'sha256': entries}, indent=2) + '\n')
        with zipfile.ZipFile(destination, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(stage.rglob('*')):
                if path.is_file():
                    archive.write(path, path.relative_to(stage.parent))
    print(json.dumps({'archive': str(destination.resolve()), 'sha256': sha256(destination), 'target': args.target}, indent=2))


if __name__ == '__main__':
    main()
