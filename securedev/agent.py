from securedev.scanner import run_scan
from securedev.analyzer import analyze_finding
from securedev.reporter import generate_report
from securedev.storage import Storage
from securedev.verification import compare_findings


class SecurityReviewAgent:
    def __init__(self, target_directory):
        self.target_directory = target_directory
        self.findings = []
        self.storage = Storage()
        self.history_path = "reports/previous_findings.json"

    def scan(self):
        print("[Agent] Running security scan...")

        self.findings = run_scan(self.target_directory)

        print(f"[Agent] Found {len(self.findings)} findings.")

    def compare(self, previous_findings):
        comparison = compare_findings(
            previous_findings,
            self.findings,
        )

        print(
            f"[Agent] Persisting: {len(comparison['persisting'])}"
        )
        print(
            f"[Agent] No longer detected: {len(comparison['resolved'])}"
        )
        print(f"[Agent] New findings: {len(comparison['new'])}")

        return comparison

    def analyze(self):
        print("[Agent] Analyzing vulnerabilities...")

        assessments = []

        for finding in self.findings:
            rule_id = finding.get("check_id", "Unknown")
            print(f"[Agent] Reviewing: {rule_id}")

            try:
                result = analyze_finding(finding)
                analysis = result["analysis"]
                complete = result["complete"]

                status = "completed" if complete else "truncated"

            except Exception as error:
                print(f"[Agent] AI analysis failed: {error}")
                analysis = (
                    "AI analysis unavailable. "
                    "Review the original scanner finding manually."
                )
                status = "failed"

            assessments.append({
                "finding": finding,
                "analysis": analysis,
                "status": status,
            })

        return assessments

    def run(self):
        previous_findings = self.storage.load_findings(
            self.history_path
        )

        # Do not update history unless the scan succeeds.
        self.scan()

        comparison = self.compare(previous_findings)

        assessments = self.analyze() if self.findings else []

        report_path = generate_report(self.findings)

        with open(report_path, "a", encoding="utf-8") as report:
            report.write("\n# Scan Comparison\n\n")
            report.write(
                f"- Persisting findings: "
                f"{len(comparison['persisting'])}\n"
            )
            report.write(
                f"- No longer detected: "
                f"{len(comparison['resolved'])}\n"
            )
            report.write(
                f"- New findings: {len(comparison['new'])}\n"
            )

            if assessments:
                report.write("\n# AI-Assisted Assessments\n\n")
                report.write(
                    "These assessments are AI-generated suggestions "
                    "and require human review.\n\n"
                )

                for index, assessment in enumerate(
                    assessments,
                    start=1,
                ):
                    report.write(f"## Assessment {index}\n\n")
                    report.write(
                        f"**Status:** {assessment['status']}\n\n"
                    )
                    if assessment["status"] == "truncated":
                        report.write(
                            "**Warning:** The AI response reached its generation limit "
                            "and may be incomplete.\n\n"
                        )

                    report.write(assessment["analysis"])
                    report.write("\n\n---\n\n")

        # Save history only after the scan and report succeed.
        self.storage.save_findings(
            self.findings,
            self.history_path,
        )

        print(f"[Agent] Report generated: {report_path}")

        return report_path