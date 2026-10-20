#!/usr/bin/env python3
"""Keep the release build free of known path-truncation warnings."""
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            ["gcc", "-std=c89", "-pedantic-errors", "-Werror=implicit-function-declaration", "-O0", "-c", "src/claro.c", "-o", str(Path(tmp) / "claro.o")],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
    if result.returncode != 0:
        raise SystemExit(result.stderr or "compiler warning validation could not compile src/claro.c")
    if "format-truncation" in result.stderr:
        raise SystemExit("compiler warning validation found -Wformat-truncation warnings:\n" + result.stderr)
    print("Compiler warning validation complete")


if __name__ == "__main__":
    main()
