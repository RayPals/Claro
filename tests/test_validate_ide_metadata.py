import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_ide_metadata_lists_current_typed_function_keywords():
    result = subprocess.run(
        ["python3", "tools/validate_ide_metadata.py"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    assert result.returncode == 0, result.stdout
    assert result.stdout.strip() == "IDE metadata validation OK"


def test_ide_metadata_is_valid_json_with_keyword_list():
    result = subprocess.run(
        ["./claro", "ide"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=True,
    )
    metadata = json.loads(result.stdout)

    assert "RETURNS" in metadata["keywords"]
    assert "CHECK" in metadata["keywords"]
    assert "TYPE" in metadata["keywords"]
