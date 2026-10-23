from securedev.storage import Storage


def test_save_and_load_findings(tmp_path):
    storage = Storage()
    file_path = tmp_path / "reports" / "findings.json"

    findings = [
        {
            "check_id": "python.lang.security.audit",
            "path": "examples/vulnerable.py",
            "start": {"line": 5},
            "extra": {
                "severity": "WARNING",
                "message": "Potential command injection"
            }
        }
    ]

    # Save the findings.
    storage.save_findings(findings, file_path)

    # Load them back.
    loaded_findings = storage.load_findings(file_path)

    # Verify the saved data matches the original.
    assert loaded_findings == findings


def test_load_missing_file_returns_empty_list(tmp_path):
    storage = Storage()
    file_path = tmp_path / "missing.json"

    result = storage.load_findings(file_path)

    assert result == []


def test_save_creates_parent_directories(tmp_path):
    storage = Storage()
    file_path = tmp_path / "new_folder" / "nested" / "findings.json"

    storage.save_findings([], file_path)

    assert file_path.exists()