"""Every file handed to the participants must still run.

These tests launch the scripts in a separate process, the way a participant
would, with a chart backend that needs no screen.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RUNNABLE = sorted(
    [
        PROJECT_ROOT / "scripts" / "demo.py",
        PROJECT_ROOT / "scripts" / "report_m07.py",
        *(PROJECT_ROOT / "idioms").glob("[0-9]*.py"),
        *(PROJECT_ROOT / "traps").glob("[0-9]*.py"),
        PROJECT_ROOT / "traps" / "13_import_runs_once" / "demo.py",
        PROJECT_ROOT / "traps" / "15_relative_paths" / "demo.py",
        *(PROJECT_ROOT / "analysis").glob("[0-9]*.py"),
        PROJECT_ROOT / "exercises" / "workbook.py",
    ]
)


def run(path: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(path), *arguments],
        cwd=PROJECT_ROOT,
        env={**os.environ, "MPLBACKEND": "Agg"},
        capture_output=True,
        text=True,
        timeout=180,
    )


@pytest.mark.parametrize("path", RUNNABLE, ids=lambda p: str(p.relative_to(PROJECT_ROOT)))
def test_file_runs(path: Path):
    result = run(path)
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip()


def test_script_with_arguments_runs_and_documents_itself():
    script = PROJECT_ROOT / "scripts" / "machine_report.py"

    report = run(script, "--machine", "M03", "--hours", "48")
    assert report.returncode == 0, report.stderr
    assert "hours_before_end" in report.stdout

    usage = run(script, "--help")
    assert usage.returncode == 0
    assert "--machine" in usage.stdout

    missing = run(script)
    assert missing.returncode == 2
    assert "--machine" in missing.stderr


def test_notebook_code_still_runs(tmp_path):
    notebook = json.loads((PROJECT_ROOT / "notebooks" / "machine_report.ipynb").read_text())
    code = "\n\n".join(
        "".join(cell["source"]) for cell in notebook["cells"] if cell["cell_type"] == "code"
    )
    script = tmp_path / "notebook_code.py"
    script.write_text(code)

    result = run(script)
    assert result.returncode == 0, result.stderr


def test_shadowing_trap_fails_as_intended():
    result = run(PROJECT_ROOT / "traps" / "14_shadowing" / "demo.py")
    assert result.returncode != 0
    assert "AttributeError" in result.stderr


def test_exercise_starts_with_the_traceback_from_the_slides():
    result = run(PROJECT_ROOT / "exercises" / "run_exercise.py")
    assert result.returncode != 0
    assert "IndexError" in result.stderr
    assert "legacy_features.py" in result.stderr
