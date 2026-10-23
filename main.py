from securedev.scanner import run_scan
from securedev.reporter import generate_report


def main():

    print("SecureDev AI - Security Scanner")
    print("--------------------------------")

    findings = run_scan("examples")

    print(f"Found {len(findings)} potential vulnerabilities.")

    report_path = generate_report(findings)

    print(f"Security report generated: {report_path}")


if __name__ == "__main__":
    main()