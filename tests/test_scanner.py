import json
import subprocess
from unittest.mock import Mock, patch

import pytest

from securedev.scanner import run_scan


def test_scan_returns_findings_for_valid_output(tmp_path):
    source_file = tmp_path / "example.py"
    source_file.write_text("print('hello')", encoding="utf-8")

    findings = [
        {"check_id": "example.rule", "path": "example.py"}
    ]

    result = Mock()
    result.returncode = 0
    result.stdout = json.dumps({"results": findings, "errors": []})
    result.stderr = ""

    with patch("securedev.scanner.subprocess.run", return_value=result):
        assert run_scan(tmp_path) == findings


def test_scan_returns_empty_list_when_no_findings(tmp_path):
    result = Mock()
    result.returncode = 0
    result.stdout = json.dumps({"results": [], "errors": []})
    result.stderr = ""

    with patch("securedev.scanner.subprocess.run", return_value=result):
        assert run_scan(tmp_path) == []


def test_scan_rejects_invalid_directory(tmp_path):
    missing_directory = tmp_path / "missing"

    with pytest.raises(ValueError, match="Invalid scan directory"):
        run_scan(missing_directory)


def test_scan_raises_when_semgrep_fails(tmp_path):
    result = Mock()
    result.returncode = 2
    result.stdout = ""
    result.stderr = "Configuration error"

    with patch("securedev.scanner.subprocess.run", return_value=result):
        with pytest.raises(RuntimeError, match="Configuration error"):
            run_scan(tmp_path)


def test_scan_raises_when_output_is_invalid_json(tmp_path):
    result = Mock()
    result.returncode = 0
    result.stdout = "not valid json"
    result.stderr = ""

    with patch("securedev.scanner.subprocess.run", return_value=result):
        with pytest.raises(RuntimeError, match="invalid JSON"):
            run_scan(tmp_path)


def test_scan_raises_when_semgrep_times_out(tmp_path):
    error = subprocess.TimeoutExpired(
        cmd="semgrep",
        timeout=120,
    )

    with patch(
        "securedev.scanner.subprocess.run",
        side_effect=error,
    ):
        with pytest.raises(RuntimeError, match="timed out"):
            run_scan(tmp_path)