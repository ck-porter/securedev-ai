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
        print("[Agent] Comparing findings with previous scan...")

        comparison = compare_findings(
            previous_findings,
            self.findings
        )

        print(
            f"[Agent] Persisting: "
            f"{len(comparison['persisting'])}"
        )
        print(
            f"[Agent] No longer detected: "
            f"{len(comparison['resolved'])}"
        )
        print(
            f"[Agent] New findings: "
            f"{len(comparison['new'])}"
        )

        return comparison

    def analyze(self):
        print("[Agent] Analyzing vulnerabilities...")

        assessments = []

        for finding in self.findings:
            print(f"[Agent] Reviewing: {finding['check_id']}")

            try:
                analysis = analyze_finding(finding)

            except Exception as error:
                print(f"[Agent] AI analysis failed: {error}")

                analysis = (
                    "AI analysis unavailable. "
                    "Review the Semgrep finding manually."
                )

            assessments.append({
                "finding": finding,
                "analysis": analysis
            })

        return assessments

    def run(self):
        previous_findings = self.storage.load_findings(
            self.history_path
        )

        self.scan()

        comparison = self.compare(previous_findings)

        self.storage.save_findings(
            self.findings,
            self.history_path
        )

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
                f"- New findings: "
                f"{len(comparison['new'])}\n"
            )

            if assessments:
                report.write("\n# AI Security Assessments\n\n")

                for index, assessment in enumerate(
                    assessments,
                    start=1
                ):
                    report.write(
                        f"## AI Assessment {index}\n\n"
                    )
                    report.write(assessment["analysis"])
                    report.write("\n\n---\n\n")

        print(f"[Agent] Report generated: {report_path}")

        return report_path