#!/usr/bin/env python3
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / ("claro.exe" if os.name == "nt" else "claro")
EXPECTED_VERSION = "Claro v1.18.26"


def fail(message):
    raise SystemExit(message)


def run(cmd, cwd):
    result = subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return result.returncode, result.stdout


def read(path):
    return path.read_text(encoding="utf-8")


def main():
    if not EXE.exists():
        fail(f"Missing executable: {EXE}")

    rc, out = run([str(EXE), "--version"], ROOT)
    if rc != 0 or EXPECTED_VERSION not in out:
        fail(f"Expected {EXPECTED_VERSION}, got:\n{out}")

    with tempfile.TemporaryDirectory() as td:
        work = Path(td)
        (work / "main.claro").write_text('SAY "Package security demo"\n', encoding="utf-8")

        rc, out = run([str(EXE), "package", "init"], work)
        if rc != 0:
            fail(out)
        project = read(work / "claro.project")
        for phrase in ["manifest-version: 1", "name: ClaroProject", "main: main.claro", "version: v1.18.26", "packages:"]:
            if phrase not in project:
                fail(f"claro.project missing {phrase!r}:\n{project}")

        rc, out = run([str(EXE), "package", "add", "math-tools"], work)
        if rc != 0:
            fail(out)
        manifest_path = work / "packages" / "math-tools" / "claro.package"
        manifest = read(manifest_path)
        for phrase in ["manifest-version: 1", "name: math-tools", "version: 1", "source: local", "checksum:"]:
            if phrase not in manifest:
                fail(f"claro.package missing {phrase!r}:\n{manifest}")
        checksum_line = next((line for line in manifest.splitlines() if line.startswith("checksum:")), "")
        checksum = checksum_line.split(":", 1)[1].strip()
        if len(checksum) < 8 or checksum == "TODO":
            fail(f"Package checksum should be a stable non-placeholder value, got {checksum!r}")

        lock = read(work / "claro.lock")
        for phrase in ["lock-version: 1", "version: v1.18.26", "package: math-tools", "checksum:"]:
            if phrase not in lock:
                fail(f"claro.lock missing {phrase!r}:\n{lock}")

        rc, out = run([str(EXE), "package", "doctor"], work)
        if rc != 0:
            fail(out)
        for phrase in ["OK package manifest: math-tools", "OK package checksum: math-tools", "Package/project files look ready."]:
            if phrase not in out:
                fail(f"package doctor output missing {phrase!r}:\n{out}")

        rc, out = run([str(EXE), "package", "add", "../bad"], work)
        if rc == 0:
            fail("Unsafe package names with path separators must be rejected")
        if "Package names may use only" not in out:
            fail(f"Unsafe package diagnostic was unclear:\n{out}")

    print("Package security validation OK")


if __name__ == "__main__":
    main()
