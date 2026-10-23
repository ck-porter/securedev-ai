import json
import subprocess
from pathlib import Path


def run_scan(target_directory):
    """
    Run Semgrep against a directory and return its findings.
    """

    target = Path(target_directory).resolve()

    if not target.is_dir():
        raise ValueError(f"Invalid directory: {target}")

    command = [
        "semgrep",
        "scan",
        "--config", "p/security-audit",
        "--json",
        "--metrics=off",
        str(target)
    ]

    result = subprocess.run(
          command,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        shell=False,
        timeout=120
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"Semgrep failed: {result.stderr}"
        )

    scan_data = json.loads(result.stdout)

    if scan_data.get("errors"):
        raise RuntimeError(
            f"Semgrep reported scan errors: {scan_data['errors']}"
        )

    return scan_data.get("results", [])