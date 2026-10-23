from securedev.scanner import run_scan
from securedev.analyzer import analyze_finding
from securedev.reporter import generate_report


class SecurityReviewAgent:

    def __init__(self, target_directory):
        self.target_directory = target_directory
        self.findings = []

    def scan(self):
        print("[Agent] Running security scan...")

        self.findings = run_scan(self.target_directory)

        print(f"[Agent] Found {len(self.findings)} findings.")

    def analyze(self):
        print("[Agent] Analyzing vulnerabilities...")

        assessments = []

        for finding in self.findings:

            print(
                f"[Agent] Reviewing: {finding['check_id']}"
            )

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

        self.scan()

        if not self.findings:
            print("[Agent] No vulnerabilities detected by Semgrep.")
            return generate_report([])

        assessments = self.analyze()

        report_path = generate_report(self.findings)

        with open(report_path, "a", encoding="utf-8") as report:

            report.write("\n# AI Security Assessments\n\n")

            for index, assessment in enumerate(assessments, start=1):

                report.write(
                    f"## AI Assessment {index}\n\n"
                )

                report.write(assessment["analysis"])
                report.write("\n\n---\n\n")

        print(f"[Agent] Report generated: {report_path}")

        return report_path