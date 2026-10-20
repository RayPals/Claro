#!/usr/bin/env python3
"""Run the maintained ownership, malformed-input, nesting and safety regressions."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXTRA = ['validate_learning_ownership.py', 'validate_value_ownership.py', 'validate_call_depth_guard.py',
         'validate_nesting_guards.py', 'validate_http_hardening.py',
         'validate_trusted_command_docs.py']


def main():
    scripts = sorted((ROOT / 'tools').glob('validate_*cleanup.py'))
    scripts += [ROOT / 'tools' / name for name in EXTRA]
    assert len(scripts) == len(set(scripts)), 'Duplicate reliability checks'
    assert all(path.is_file() and path.stat().st_size for path in scripts), 'Missing or empty reliability check'
    logs = Path(tempfile.mkdtemp(prefix='claro-reliability-', dir=os.environ.get('TMPDIR')))

    def run(path):
        try:
            result = subprocess.run([sys.executable, str(path)], cwd=ROOT, text=True, capture_output=True, timeout=180)
            output = result.stdout + result.stderr
            status = result.returncode
        except subprocess.TimeoutExpired as error:
            output = f'TIMEOUT: {error}'
            status = 124
        log = logs / (path.stem + '.log')
        log.write_text(output, encoding='utf-8')
        return {'test': path.name, 'exit': status, 'log': str(log), 'skipped': output.startswith('SKIP:')}

    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(run, scripts))
    (logs / 'results.json').write_text(json.dumps(results, indent=2), encoding='utf-8')
    for result in results:
        status = 'FAIL' if result['exit'] else ('SKIP' if result['skipped'] else 'PASS')
        print(status + ': ' + result['test'])
        if result['exit']:
            print(Path(result['log']).read_text()[-6000:])
    failed = sum(result['exit'] != 0 for result in results)
    skipped = sum(result['skipped'] for result in results)
    print(f'Reliability checks: {len(results)} total, {failed} failed, {skipped} skipped')
    print('Results:', logs / 'results.json')
    return 1 if failed else 0


if __name__ == '__main__':
    raise SystemExit(main())
