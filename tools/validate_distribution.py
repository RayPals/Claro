#!/usr/bin/env python3
"""Extract a distribution, verify hashes, and execute its actual payload."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shlex
import shutil
import stat
import struct
import subprocess
import sys
import tempfile
import zipfile


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('--wine-prefix', type=Path)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    if args.report.exists():
        raise SystemExit('Refusing to replace existing verification report')
    results = {'archive': str(args.archive.resolve()), 'sha256': digest(args.archive), 'checks': []}
    logs = args.report.parent / (args.report.stem + '-logs')
    logs.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ)

    def run(label, command, cwd, timeout=180):
        result = subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
        log = logs / (label + '.log')
        log.write_text(result.stdout + result.stderr, encoding='utf-8')
        results['checks'].append({'name': label, 'exit': result.returncode, 'log': str(log.resolve())})
        assert result.returncode == 0, (label, result.returncode, (result.stdout + result.stderr)[-3000:])
        print('PASS:', label)
        return result.stdout

    try:
        with tempfile.TemporaryDirectory(prefix='claro-unpack-', dir=os.environ.get('TMPDIR')) as tmp:
            work = Path(tmp) / 'unpacked package with spaces'
            work.mkdir()
            with zipfile.ZipFile(args.archive) as archive:
                names = archive.namelist()
                assert len(names) == len(set(names)), 'Duplicate archive entries'
                assert len({PurePosixPath(name).parts[0] for name in names}) == 1, 'Expected one archive root'
                for info in archive.infolist():
                    path = PurePosixPath(info.filename)
                    assert not path.is_absolute() and '..' not in path.parts and '\\' not in info.filename, 'Unsafe archive path'
                    mode = info.external_attr >> 16
                    assert not stat.S_ISLNK(mode), 'Archive must not contain symlinks'
                    target = work.joinpath(*path.parts)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(archive.read(info))
                    if os.name != 'nt' and mode:
                        target.chmod(mode & 0o777)
            root = next(work.iterdir())
            manifest = json.loads((root / 'MANIFEST.json').read_text())['sha256']
            actual = {str(p.relative_to(root)).replace(os.sep, '/'): digest(p) for p in root.rglob('*') if p.is_file() and p.name != 'MANIFEST.json'}
            assert actual == manifest, 'Package manifest mismatch'
            assert not any('__pycache__' in name or name.endswith('.pyc') or 'claro-asan' in name for name in actual), 'Development leftovers in package'
            metadata = json.loads((root / 'DISTRIBUTION.json').read_text())
            assert metadata['source_sha256'] == digest(root / 'src/claro.c')
            results.update(target=metadata['target'], version=metadata['version'], manifest_files=len(manifest), source_sha256=metadata['source_sha256'])
            print('PASS: archive inventory, source hash and manifest')
            target = metadata['target']
            if target == 'source':
                assert not (root / 'claro').exists() and not (root / 'claro.exe').exists()
                isolated = work / 'standalone'
                isolated.mkdir()
                shutil.copy2(root / 'src/claro.c', isolated / 'claro.c')
                run('isolated-c89-build', ['gcc', '-std=c89', '-pedantic-errors', '-Werror=implicit-function-declaration', 'claro.c', '-o', 'claro', '-lm'], isolated)
                run('isolated-version', [str(isolated / 'claro'), '--version'], isolated)
                run('source-make', ['make', '-s', 'all'], root)
                executable = root / ('claro.exe' if os.name == 'nt' else 'claro')
                runner = [str(executable)]
            elif target == 'linux-x86_64':
                executable = root / 'claro'
                assert not (root / 'claro.exe').exists(), 'Linux archive contains misleading .exe'
                data = executable.read_bytes()
                assert data[:5] == b'\x7fELF\x02' and struct.unpack_from('<H', data, 18)[0] == 62
                headers = run('elf-inspection', ['readelf', '-l', str(executable)], root)
                assert 'INTERP' not in headers, 'Linux release is not static'
                runner = [str(executable)]
            elif target == 'windows-x86_64':
                executable = root / 'claro.exe'
                assert not (root / 'claro').exists()
                data = executable.read_bytes()
                assert data[:2] == b'MZ'
                pe = struct.unpack_from('<I', data, 60)[0]
                assert data[pe:pe+4] == b'PE\0\0' and struct.unpack_from('<H', data, pe+4)[0] == 0x8664
                reserve = struct.unpack_from('<Q', data, pe+24+72)[0]
                assert reserve >= 16777216, 'Windows recursion guard requires a sufficient stack reserve'
                results['windows_stack_reserve'] = reserve
                pe_text = run('pe-inspection', ['x86_64-w64-mingw32-objdump', '-p', str(executable)], root)
                results['windows_dll_imports'] = re.findall(r'DLL Name:\s*(\S+)', pe_text)
                if os.name == 'nt':
                    runner = [str(executable)]
                else:
                    assert args.wine_prefix and args.wine_prefix.is_dir(), 'Supply an initialized isolated --wine-prefix'
                    env.update(WINEPREFIX=str(args.wine_prefix.resolve()), WINEDEBUG='-all')
                    runner = ['wine', str(executable)]
            else:
                raise AssertionError('Unknown distribution target')
            version = run('version', runner + ['--version'], root)
            assert metadata['version'] in version
            standalone = work / 'single executable with spaces'
            standalone.mkdir()
            isolated_binary = standalone / executable.name
            shutil.copy2(executable, isolated_binary)
            (standalone / 'hello.claro').write_text('SAY "Standalone Claro works"\n')
            isolated_runner = (['wine', str(isolated_binary)] if runner[0] == 'wine' else [str(isolated_binary)])
            output = run('standalone-runtime', isolated_runner + ['hello.claro'], standalone)
            assert output == 'Standalone Claro works\n'
            run('doctor', runner + ['doctor'], root)
            golden = run('golden-tests', runner + ['test'], root)
            results['golden_pass_count'] = len(re.findall(r'^PASS tests/', golden, re.M))
            assert results['golden_pass_count'] == len(list((root / 'tests').glob('*.out'))), 'Golden runner did not cover all packaged fixtures'
            run('builtin-validation', runner + ['validate'], root)
            if runner[0] == 'wine':
                launcher = work / 'wine-launcher'
                launcher.write_text('#!/bin/sh\nexec wine ' + shlex.quote(str(executable)) + ' "$@"\n')
                launcher.chmod(0o755)
                env['CLARO_EXE'] = str(launcher)
            else:
                env['CLARO_EXE'] = str(executable)
            run('learning-path', [sys.executable, str(root / 'tools/validate_learning_syntax.py')], root, timeout=600 if runner[0] == 'wine' else 180)
            run('first-hour', [sys.executable, str(root / 'tools/validate_first_hour.py')], root)
            if target == 'source':
                run('full-source-validation', [sys.executable, str(root / 'tools/validate_v1_17.py')], root, timeout=360)
            results['status'] = 'passed'
    except Exception as error:
        results.update(status='failed', error=str(error))
        raise
    finally:
        args.report.write_text(json.dumps(results, indent=2) + '\n', encoding='utf-8')
    print('Verified:', args.report)


if __name__ == '__main__':
    main()
