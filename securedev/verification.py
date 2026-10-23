def get_finding_id(finding):
    """
    Generate an identifier for comparing security findings
    across scans.
    """

    extra = finding.get("extra", {})

    # Prefer Semgrep's fingerprint when available.
    fingerprint = extra.get("fingerprint")

    if fingerprint:
        return fingerprint

    # Fallback identifier for findings without a fingerprint.
    return (
        f"{finding.get('check_id', 'unknown')}:"
        f"{finding.get('path', 'unknown')}:"
        f"{finding.get('start', {}).get('line', 0)}"
    )


def compare_findings(previous_findings, current_findings):
    """
    Compare two sets of scan results.

    Returns findings that persist, findings no longer detected,
    and findings newly detected.
    """

    previous = {
        get_finding_id(finding): finding
        for finding in previous_findings
    }

    current = {
        get_finding_id(finding): finding
        for finding in current_findings
    }

    previous_ids = set(previous)
    current_ids = set(current)

    return {
        "persisting": [
            current[finding_id]
            for finding_id in previous_ids & current_ids
        ],
        "resolved": [
            previous[finding_id]
            for finding_id in previous_ids - current_ids
        ],
        "new": [
            current[finding_id]
            for finding_id in current_ids - previous_ids
        ]
    }