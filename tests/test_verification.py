from securedev.verification import compare_findings


def make_finding(rule, path, line):
    return {
        "check_id": rule,
        "path": path,
        "start": {"line": line},
        "extra": {
            "severity": "WARNING",
            "message": f"Finding for {rule}"
        }
    }


def test_persisting_finding():
    """A finding present in both scans should persist."""

    previous = [
        make_finding("rule-a", "app.py", 10)
    ]

    current = [
        make_finding("rule-a", "app.py", 10)
    ]

    result = compare_findings(previous, current)

    assert len(result["persisting"]) == 1
    assert len(result["resolved"]) == 0
    assert len(result["new"]) == 0


def test_resolved_finding():
    """A finding absent from the second scan is no longer detected."""

    previous = [
        make_finding("rule-a", "app.py", 10)
    ]

    current = []

    result = compare_findings(previous, current)

    assert len(result["resolved"]) == 1
    assert len(result["persisting"]) == 0
    assert len(result["new"]) == 0


def test_new_finding():
    """A finding appearing in the second scan is new."""

    previous = []

    current = [
        make_finding("rule-b", "app.py", 20)
    ]

    result = compare_findings(previous, current)

    assert len(result["new"]) == 1
    assert len(result["persisting"]) == 0
    assert len(result["resolved"]) == 0