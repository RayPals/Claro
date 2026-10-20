#!/usr/bin/env python3
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / ("claro.exe" if os.name == "nt" else "claro")
EXPECTED_VERSION = "Claro v2026.10.20.155641"


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
        for phrase in ["manifest-version: 1", "name: StarterApp", "main: main.claro", "version: v2026.10.20.155641", "packages:"]:
            if phrase not in starter_project:
                fail(f"claro new project file missing {phrase!r}:\n{starter_project}")
        starter_lock = read(starter / "claro.lock")
        for phrase in ["lock-version: 1", "version: v2026.10.20.155641"]:
            if phrase not in starter_lock:
                fail(f"claro new lockfile missing {phrase!r}:\n{starter_lock}")

        (work / "main.claro").write_text('SAY "Package security demo"\n', encoding="utf-8")

        rc, out = run([str(EXE), "package", "init"], work)
        if rc != 0:
            fail(out)
        project = read(work / "claro.project")
        for phrase in ["manifest-version: 1", "name: ClaroProject", "main: main.claro", "version: v2026.10.20.155641", "packages:"]:
            if phrase not in project:
                fail(f"claro.project missing {phrase!r}:\n{project}")

        (work / "claro.project").write_text(
            project.replace("manifest-version: 1", "manifest-version: 10", 1),
            encoding="utf-8",
        )
        rc, out = run([str(EXE), "package", "doctor"], work)
        if rc == 0:
            fail("package doctor must reject a project manifest version that only starts with the supported version")
        if "BAD project manifest version: expected 1" not in out:
            fail(f"Package project manifest-version diagnostic was unclear:\n{out}")
        (work / "claro.project").write_text(project, encoding="utf-8")

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
        for phrase in ["lock-version: 1", "version: v2026.10.20.155641", "package: math-tools", "checksum:"]:
            if phrase not in lock:
                fail(f"claro.lock missing {phrase!r}:\n{lock}")

        for version_line in ["lock-version: 1", "  LOCK-VERSION: \t1 \t"]:
            valid_lock = lock.replace("lock-version: 1", version_line, 1)
            (work / "claro.lock").write_text(valid_lock, encoding="utf-8")
            rc, out = run([str(EXE), "package", "doctor"], work)
            if rc != 0 or "Package/project files look ready." not in out:
                fail(f"package doctor must accept a supported lock format version:\n{out}")
            if read(work / "claro.lock") != valid_lock:
                fail("package doctor must not rewrite a valid lockfile")
        (work / "claro.lock").write_text(lock, encoding="utf-8")

        for version_lines in ["", "lock-version: 10", "lock-version:",
                              "lock-version: 1\nlock-version: 1",
                              "lock-version: 1\nlock-version: 10",
                              "lock-version: 10\nlock-version: 1"]:
            invalid_lock = lock.replace("lock-version: 1", version_lines, 1)
            (work / "claro.lock").write_text(invalid_lock, encoding="utf-8")
            rc, out = run([str(EXE), "package", "doctor"], work)
            if rc == 0:
                fail(f"package doctor must reject invalid lock format versions: {version_lines!r}")
            if "BAD lock version: expected exactly one lock-version: 1 line" not in out:
                fail(f"Lock format-version diagnostic was unclear:\n{out}")
            if read(work / "claro.lock") != invalid_lock:
                fail("package doctor must not rewrite an invalid lock format version")
        invalid_release_lock = lock.replace("version: v2026.10.20.155641", "version: v1.18.25", 1)
        (work / "claro.lock").write_text(invalid_release_lock, encoding="utf-8")
        rc, out = run([str(EXE), "package", "doctor"], work)
        if rc == 0:
            fail("package doctor must reject a lockfile for a different Claro release")
        if "BAD lock release version: expected exactly one version: v2026.10.20.155641 line" not in out:
            fail(f"Lock release-version diagnostic was unclear:\n{out}")
        if read(work / "claro.lock") != invalid_release_lock:
            fail("package doctor must not rewrite an invalid lock release version")
        (work / "claro.lock").write_text(lock, encoding="utf-8")

        (work / "claro.lock").write_text(
            lock.replace("checksum:", "checksum: bad", 1),
            encoding="utf-8",
        )
        rc, out = run([str(EXE), "package", "doctor"], work)
        if rc == 0:
            fail("package doctor must reject stale lockfile checksums")
        if "BAD lock checksum: math-tools" not in out:
            fail(f"package doctor stale-lock diagnostic was unclear:\n{out}")
        (work / "claro.lock").write_text(lock, encoding="utf-8")

        for sums in [(checksum, checksum), (checksum, "bad"), ("bad", checksum)]:
            duplicate_lock = lock.replace(
                "checksum: " + checksum,
                "\n".join("checksum: " + value for value in sums),
                1,
            )
            (work / "claro.lock").write_text(duplicate_lock, encoding="utf-8")
            rc, out = run([str(EXE), "package", "doctor"], work)
            if rc == 0:
                fail(f"package doctor must reject duplicate lock checksums: {sums}")
            if "BAD lock checksum: math-tools" not in out:
                fail(f"Duplicate lock checksum diagnostic was unclear:\n{out}")
            if read(work / "claro.lock") != duplicate_lock:
                fail("package doctor must not rewrite a lockfile with duplicate checksums")
        (work / "claro.lock").write_text(lock, encoding="utf-8")

        checksum_line = next((line for line in manifest.splitlines() if line.startswith("checksum:")), "")
        checksum = checksum_line.split(":", 1)[1].strip()
        project_with_package = read(work / "claro.project")
        manifest_path.write_text(manifest.replace("checksum: " + checksum, "checksum: " + checksum + "-extra"), encoding="utf-8")
        rc, out = run([str(EXE), "package", "doctor"], work)
        if rc == 0:
            fail("package doctor must reject a manifest checksum with trailing data")
        if "BAD package checksum: math-tools" not in out:
            fail(f"Package manifest checksum diagnostic was unclear:\n{out}")
        manifest_path.write_text(manifest, encoding="utf-8")
        for format_lines in ["", "manifest-version:", "manifest-version: 10",
                             "manifest-version: 1\nmanifest-version: 1",
                             "manifest-version: 1\nmanifest-version: 10",
                             "manifest-version: 10\nmanifest-version: 1"]:
            invalid_manifest = manifest.replace("manifest-version: 1", format_lines, 1)
            manifest_path.write_text(invalid_manifest, encoding="utf-8")
            rc, out = run([str(EXE), "package", "doctor"], work)
            if rc == 0:
                fail(f"package doctor must reject an invalid package manifest format: {format_lines!r}")
            diagnostic = ("BAD package manifest version: math-tools. Keep exactly one "
                          "manifest-version: 1 line in packages/math-tools/claro.package.")
            if diagnostic not in out or "MISSING package manifest: math-tools" in out:
                fail(f"Package manifest-version diagnostic was unclear:\n{out}")
            if read(manifest_path) != invalid_manifest:
                fail("package doctor must not rewrite an invalid package manifest")
        manifest_path.write_text(manifest, encoding="utf-8")
        duplicate_version_manifest = manifest + "version: 1\n"
        manifest_path.write_text(duplicate_version_manifest, encoding="utf-8")
        rc, out = run([str(EXE), "package", "doctor"], work)
        if rc == 0:
            fail("package doctor must reject duplicate package manifest versions")
        if "BAD package version: math-tools" not in out:
            fail(f"Package duplicate manifest-version diagnostic was unclear:\n{out}")
        manifest_path.write_text(manifest, encoding="utf-8")
        manifest_path.write_text(manifest.replace("version: 1", "version: 10"), encoding="utf-8")
        rc, out = run([str(EXE), "package", "doctor"], work)
        if rc == 0:
            fail("package doctor must reject a package version that only starts with the supported version")
        if "BAD package version: math-tools" not in out:
            fail(f"Package manifest version diagnostic was unclear:\n{out}")
        manifest_path.write_text(manifest, encoding="utf-8")

        manifest_path.write_text(manifest.replace("source: local", "source: local-extra"), encoding="utf-8")
        rc, out = run([str(EXE), "package", "doctor"], work)
        if rc == 0:
            fail("package doctor must reject a package source that only starts with the supported source")
        if "BAD package source: math-tools" not in out:
            fail(f"Package manifest source diagnostic was unclear:\n{out}")
        manifest_path.write_text(manifest, encoding="utf-8")

        for sources in [("local", "local"), ("local", "remote"), ("remote", "local")]:
            duplicate_source_manifest = manifest.replace(
                "source: local", "\n".join("source: " + source for source in sources), 1
            )
            manifest_path.write_text(duplicate_source_manifest, encoding="utf-8")
            rc, out = run([str(EXE), "package", "doctor"], work)
            if rc == 0:
                fail(f"package doctor must reject duplicate package manifest sources: {sources}")
            if "BAD package source: math-tools" not in out:
                fail(f"Package duplicate source diagnostic was unclear:\n{out}")
            if read(manifest_path) != duplicate_source_manifest:
                fail("package doctor must not rewrite a manifest with duplicate sources")
        manifest_path.write_text(manifest, encoding="utf-8")

        duplicate_name_manifest = manifest + "name: other-tools\n"
        manifest_path.write_text(duplicate_name_manifest, encoding="utf-8")
        rc, out = run([str(EXE), "package", "doctor"], work)
        if rc == 0:
            fail("package doctor must reject duplicate package manifest names")
        if "BAD package manifest name: math-tools" not in out:
            fail(f"Package duplicate manifest-name diagnostic was unclear:\n{out}")
        manifest_path.write_text(manifest, encoding="utf-8")

        duplicate_checksum_manifest = manifest + "checksum: " + checksum + "\n"
        manifest_path.write_text(duplicate_checksum_manifest, encoding="utf-8")
        rc, out = run([str(EXE), "package", "doctor"], work)
        if rc == 0:
            fail("package doctor must reject duplicate package manifest checksums")
        if "BAD package checksum: math-tools" not in out:
            fail(f"Package duplicate checksum diagnostic was unclear:\n{out}")
        manifest_path.write_text(manifest, encoding="utf-8")

        rc, out = run([str(EXE), "package", "doctor"], work)
        if rc != 0:
            fail(out)
        for phrase in ["OK package manifest: math-tools", "OK package checksum: math-tools", "OK lock checksum: math-tools", "Package/project files look ready."]:
            if phrase not in out:
                fail(f"package doctor output missing {phrase!r}:\n{out}")

        manifest_path.unlink()
        rc, out = run([str(EXE), "package", "doctor"], work)
        if rc == 0:
            fail("package doctor must reject a listed package whose manifest is missing")
        if "MISSING package manifest: math-tools" not in out:
            fail(f"package doctor missing-manifest diagnostic was unclear:\n{out}")
        manifest_path.write_text(manifest.replace("name: math-tools", "name: other-tools"), encoding="utf-8")
        rc, out = run([str(EXE), "package", "doctor"], work)
        if rc == 0:
            fail("package doctor must reject a manifest whose name does not match the project package")
        if "BAD package manifest name: math-tools" not in out:
            fail(f"package doctor manifest-name diagnostic was unclear:\n{out}")
        manifest_path.write_text(manifest.replace("name: math-tools", "name: math-tools-extra"), encoding="utf-8")
        rc, out = run([str(EXE), "package", "doctor"], work)
        if rc == 0:
            fail("package doctor must reject a manifest name that only starts with the project package name")
        if "BAD package manifest name: math-tools" not in out:
            fail(f"Package manifest prefix-match diagnostic was unclear:\n{out}")
        manifest_path.write_text(manifest, encoding="utf-8")

        (work / "claro.lock").write_text(
            lock + "package: ghost\nchecksum: 12345678\n",
            encoding="utf-8",
        )
        rc, out = run([str(EXE), "package", "doctor"], work)
        if rc == 0:
            fail("package doctor must reject lockfile packages that are not listed in claro.project")
        if "BAD lock package not in claro.project: ghost" not in out:
            fail(f"package doctor orphan-lock diagnostic was unclear:\n{out}")
        (work / "claro.lock").write_text(lock, encoding="utf-8")

        (work / "claro.lock").write_text(
            lock + "package: math-tools\nchecksum: " + checksum + "\n",
            encoding="utf-8",
        )
        rc, out = run([str(EXE), "package", "doctor"], work)
        if rc == 0:
            fail("package doctor must reject duplicate lockfile package entries")
        if "DUPLICATE lock package: math-tools" not in out:
            fail(f"package doctor duplicate-lock diagnostic was unclear:\n{out}")
        (work / "claro.lock").write_text(lock, encoding="utf-8")
        (work / "claro.project").write_text(project_with_package, encoding="utf-8")

        (work / "claro.project").write_text(
            project_with_package.replace("name: ClaroProject", "name:", 1),
            encoding="utf-8",
        )
        rc, out = run([str(EXE), "package", "doctor"], work)
        if rc == 0:
            fail("package doctor must reject a project manifest with an empty name")
        if "BAD project manifest name: expected a non-empty name" not in out:
            fail(f"Package project-name diagnostic was unclear:\n{out}")
        (work / "claro.project").write_text(project, encoding="utf-8")
        duplicate_project_manifest = project_with_package + "manifest-version: 1\n"
        (work / "claro.project").write_text(duplicate_project_manifest, encoding="utf-8")
        rc, out = run([str(EXE), "package", "doctor"], work)
        if rc == 0:
            fail("package doctor must reject duplicate project manifest versions")
        if "BAD project manifest version: expected 1" not in out:
            fail(f"Package duplicate project manifest-version diagnostic was unclear:\n{out}")
        (work / "claro.project").write_text(project, encoding="utf-8")

        (work / "claro.project").write_text(
            project + "package: math-tools\npackage: math-tools\n",
            encoding="utf-8",
        )
        rc, out = run([str(EXE), "package", "doctor"], work)
        if rc == 0:
            fail("package doctor must reject duplicate package entries in claro.project")
        if "DUPLICATE package: math-tools" not in out:
            fail(f"Package duplicate diagnostic was unclear:\n{out}")
        (work / "claro.project").write_text(project, encoding="utf-8")

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
            "manifest-version: 1\nname: ClaroProject\nmain: main.claro\nversion: v2026.10.20.155641\npackages:\npackage: ../bad\n",
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

        rc, out = run([str(EXE), "package", "list"], work)
        if rc == 0:
            fail("package list must reject unsafe package names already present in claro.project")
        if "BAD package name: ../bad" not in out:
            fail(f"package list unsafe-name diagnostic was unclear:\n{out}")

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
            "manifest-version: 1\nname: ClaroProject\nmain: main.claro\nversion: v2026.10.20.155641\npackages:\npackage: math-tools\npackage: ../bad\n",
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
