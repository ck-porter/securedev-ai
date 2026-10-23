import json
import subprocess
from pathlib import Path


def run_scan(target_directory):
    """Run Semgrep against a directory and return its findings."""

    target = Path(target_directory).resolve()

    if not target.is_dir():
        raise ValueError(f"Invalid scan directory: {target}")

    command = [
        "semgrep",
        "scan",
        "--config",
        "p/security-audit",
        "--json",
        "--metrics=off",
        str(target),
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            shell=False,
            timeout=120,
            check=False,
        )

    except FileNotFoundError as error:
        raise RuntimeError(
            "Semgrep could not be found. "
            "Install it and ensure it is available on PATH."
        ) from error

    except subprocess.TimeoutExpired as error:
        raise RuntimeError(
            "Semgrep scan timed out after 120 seconds."
        ) from error

    if result.returncode != 0:
        details = result.stderr.strip() or "No error details provided."
        raise RuntimeError(f"Semgrep scan failed: {details}")

    try:
        scan_data = json.loads(result.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError(
            "Semgrep returned invalid JSON output."
        ) from error

    if not isinstance(scan_data, dict):
        raise RuntimeError(
            "Semgrep returned an unexpected JSON structure."
        )

    errors = scan_data.get("errors", [])

    if errors:
        raise RuntimeError(
            f"Semgrep reported scan errors: {errors}"
        )

    findings = scan_data.get("results")

    if not isinstance(findings, list):
        raise RuntimeError(
            "Semgrep output did not contain a valid results list."
        )

    return findings