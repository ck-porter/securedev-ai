from datetime import datetime, timezone
from pathlib import Path


def generate_report(findings, output_path="reports/security-report.md"):

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    report = [
        "# SecureDev AI - Security Report",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        f"## Total Findings: {len(findings)}",
        ""
    ]

    for index, finding in enumerate(findings, start=1):

        extra = finding.get("extra", {})

        report.extend([
            f"## Finding {index}",
            "",
            f"**Rule:** {finding.get('check_id', 'Unknown')}",
            "",
            f"**File:** {finding.get('path', 'Unknown')}",
            "",
            f"**Line:** {finding.get('start', {}).get('line', '?')}",
            "",
            f"**Severity:** {extra.get('severity', 'Unknown')}",
            "",
            f"**Description:** {extra.get('message', 'N/A')}",
            "",
            "---",
            ""
        ])

    if not findings:
        report.append(
            "No findings were reported by the configured scanner rules."
        )

    output.write_text(
        "\n".join(report),
        encoding="utf-8"
    )

    return output