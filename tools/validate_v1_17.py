#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXE = ROOT / ("claro.exe" if os.name == "nt" else "claro")
SRC = ROOT / "src" / "claro.c"
ZIG_CC = Path.home() / "AppData" / "Local" / "hermes" / "tools" / "zig-x86_64-windows-0.14.1" / "zig.exe"


def run(cmd):
    print("$", " ".join(str(c) for c in cmd))
    result = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(result.stdout, end="")
    if result.returncode != 0:
        raise SystemExit(result.returncode)
    return result.stdout


def compiler_cmd():
    env_cc = os.environ.get("CLARO_CC")
    if env_cc:
        parts = env_cc.split()
        return parts + ["-std=c89", "-pedantic-errors", "-Werror=implicit-function-declaration", "src/claro.c", "-O0", "-o", str(EXE), "-lm"]
    if ZIG_CC.exists():
        return [str(ZIG_CC), "cc", "-std=c89", "-pedantic-errors", "-Werror=implicit-function-declaration", "src/claro.c", "-O0", "-o", str(EXE), "-lm"]
    return ["gcc", "-std=c89", "-pedantic-errors", "-Werror=implicit-function-declaration", "src/claro.c", "-O0", "-o", str(EXE), "-lm"]


def build():
    if not SRC.exists():
        raise SystemExit("Missing src/claro.c")
    run(compiler_cmd())


def main():
    build()
    run([sys.executable, "tools/validate_c89.py"])
    run([sys.executable, "tools/validate_msvc6_source.py"])
    out = run([str(EXE), "--version"])
    if "Claro v2026.10.20.223203" not in out:
        raise SystemExit("Wrong version string")
    run([str(EXE), "test"])
    run([str(EXE), "validate"])
    run([sys.executable, "tools/validate_first_hour.py"])
    run([sys.executable, "tools/validate_learning_syntax.py"])
    run([sys.executable, "tools/validate_ide_metadata.py"])
    run([sys.executable, "tools/validate_lsp_helper.py"])
    run([sys.executable, "tools/validate_concurrency.py"])
    run([sys.executable, "tools/validate_package_security.py"])
    run([sys.executable, "tools/validate_typecheck_diagnostics.py"])
    run([sys.executable, "tools/validate_reliability.py"])
    run([sys.executable, "tools/validate_version_convention.py"])
    run([sys.executable, "tools/validate_documentation_status.py"])
    run([str(EXE), "examples/networking.claro"])
    print("v2026.10.20.223203 validation complete")

if __name__ == "__main__":
    main()
