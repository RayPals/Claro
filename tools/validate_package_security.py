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
        root = Path(td)
        work = root / "work"
        work.mkdir()

        rc, out = run([str(EXE), "new", "../bad"], work)
        if rc == 0:
            fail("Unsafe project names with path separators must be rejected")
        if "Project names may use only" not in out:
            fail(f"Unsafe project-name diagnostic was unclear:\n{out}")
        if (root / "bad").exists():
            fail("Unsafe project name should not create a folder outside the current project area")

        long_project_name = "P" * 65
        rc, out = run([str(EXE), "new", long_project_name], work)
        if rc == 0:
            fail("Project names longer than 64 characters must be rejected before paths are created")
        if "Project names must be 64 characters or fewer" not in out:
            fail(f"Long project-name diagnostic was unclear:\n{out}")
        if (work / long_project_name).exists():
            fail("Long project name should not create a project folder")

        rc, out = run([str(EXE), "new", "StarterApp"], work)
        if rc != 0:
            fail(out)
        starter = work / "StarterApp"
        starter_project = read(starter / "claro.project")
        for phrase in ["manifest-version: 1", "name: StarterApp", "main: main.claro", "version: v1.18.26", "packages:"]:
            if phrase not in starter_project:
                fail(f"claro new project file missing {phrase!r}:\n{starter_project}")
        starter_lock = read(starter / "claro.lock")
        for phrase in ["lock-version: 1", "version: v1.18.26"]:
            if phrase not in starter_lock:
                fail(f"claro new lockfile missing {phrase!r}:\n{starter_lock}")

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

        long_name = "a" * 65
        rc, out = run([str(EXE), "package", "add", long_name], work)
        if rc == 0:
            fail("Package names longer than 64 characters must be rejected before paths are created")
        if "Package names must be 64 characters or fewer" not in out:
            fail(f"Long package-name diagnostic was unclear:\n{out}")
        if (work / "packages" / long_name).exists():
            fail("Long package name should not create a package folder")

        (work / "claro.project").write_text(
            "manifest-version: 1\nname: ClaroProject\nmain: main.claro\nversion: v1.18.26\npackages:\npackage: ../bad\n",
            encoding="utf-8",
        )
        rc, out = run([str(EXE), "package", "doctor"], work)
        if rc == 0:
            fail("package doctor must reject unsafe package names already present in claro.project")
        if "BAD package name: ../bad" not in out:
            fail(f"package doctor unsafe-name diagnostic was unclear:\n{out}")

        rc, out = run([str(EXE), "package", "lock"], work)
        if rc == 0:
            fail("package lock must reject unsafe package names already present in claro.project")
        if "BAD package name: ../bad" not in out:
            fail(f"package lock unsafe-name diagnostic was unclear:\n{out}")

        rc, out = run([str(EXE), "package", "init"], work)
        if rc == 0:
            fail("package init must not report success while unsafe package names remain in claro.project")
        if "BAD package name: ../bad" not in out:
            fail(f"package init existing unsafe-name diagnostic was unclear:\n{out}")

        rc, out = run([str(EXE), "package", "add", "science"], work)
        if rc == 0:
            fail("package add must not report success while unsafe package names remain in claro.project")
        if "BAD package name: ../bad" not in out:
            fail(f"package add existing unsafe-name diagnostic was unclear:\n{out}")
        project_after_failed_add = read(work / "claro.project")
        if "package: science" in project_after_failed_add:
            fail("package add should not append a package while unsafe names remain in claro.project")
        if (work / "packages" / "science").exists():
            fail("package add should not create a package folder while unsafe names remain in claro.project")

        (work / "claro.project").write_text(
            "manifest-version: 1\nname: ClaroProject\nmain: main.claro\nversion: v1.18.26\npackages:\npackage: math-tools\npackage: ../bad\n",
            encoding="utf-8",
        )
        rc, out = run([str(EXE), "package", "remove", "math-tools"], work)
        if rc == 0:
            fail("package remove must not report success while unsafe package names remain in claro.project")
        if "BAD package name: ../bad" not in out:
            fail(f"package remove unsafe-name diagnostic was unclear:\n{out}")

        rc, out = run([str(EXE), "package", "remove", "../bad"], work)
        if rc != 0:
            fail(f"package remove should let learners remove an unsafe package entry from claro.project:\n{out}")
        if "Removed package from project: ../bad" not in out:
            fail(f"package remove unsafe-entry recovery output was unclear:\n{out}")
        project_after_bad_remove = read(work / "claro.project")
        if "package: ../bad" in project_after_bad_remove:
            fail("package remove should remove the unsafe package entry from claro.project")
        lock_after_bad_remove = read(work / "claro.lock")
        if "package: ../bad" in lock_after_bad_remove:
            fail("package remove should not keep unsafe package entries in claro.lock after recovery")

    print("Package security validation OK")


if __name__ == "__main__":
    main()
