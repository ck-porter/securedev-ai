\# SecureDev AI



\*\*AI-assisted application security analysis using static analysis and local language models.\*\*



SecureDev AI combines Semgrep static analysis with a locally hosted language model to help developers understand potential vulnerabilities, evaluate their impact, and explore remediation options.



The tool also tracks findings between scans, making it easier to identify newly detected issues and findings that are no longer detected.



\## Features



\- \*\*Static analysis:\*\* Uses Semgrep security rules to identify potential vulnerabilities in source code.

\- \*\*AI-assisted analysis:\*\* Uses a locally hosted Ollama model to explain findings and suggest remediation approaches.

\- \*\*Scan comparison:\*\* Identifies findings that persist, appear for the first time, or are no longer detected compared with a previous scan.

\- \*\*Report generation:\*\* Produces Markdown reports containing scan findings and AI-generated assessments.

\- \*\*Scan history:\*\* Stores findings as JSON for comparison across subsequent runs.

\- \*\*Automated tests:\*\* Includes pytest coverage for scan comparison and finding storage.



\## Architecture



The project separates scanning, analysis, comparison, storage, and reporting into individual modules.



| Module | Responsibility |

|---|---|

| `scanner.py` | Runs Semgrep and processes its results. |

| `analyzer.py` | Sends findings to a locally hosted Ollama model for analysis. |

| `verification.py` | Compares findings between scans. |

| `storage.py` | Saves and loads scan history. |

| `reporter.py` | Generates Markdown security reports. |

| `agent.py` | Coordinates the security review workflow. |

| `main.py` | Provides the application entry point. |



\## Requirements



\- Python 3.10 or newer

\- Semgrep

\- Ollama

\- A compatible Ollama model, such as `llama3.2:1b`



The exact Python version and dependency requirements should be verified against the project's configuration.



\## Setup



Clone the repository and enter the project directory:



```bash

git clone https://github.com/ck-porter/securedev-ai.git

cd securedev-ai

```



Create and activate a virtual environment.



\*\*Windows PowerShell:\*\*



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

```



Install the Python dependencies:



```powershell

python -m pip install -r requirements.txt

```



Install and configure Semgrep and Ollama if they are not already available. Pull the configured Ollama model:



```bash

ollama pull llama3.2:1b

```



Ensure Ollama is available locally before running an AI-assisted review.



\## Usage



Run a security review against a target directory:



```bash

python main.py examples

```



The workflow runs a Semgrep scan, compares the findings with the previous scan, requests AI-assisted assessments, and generates a Markdown report.



Generated reports and scan history are stored locally under `reports/`.



\## Testing



Run the automated tests:



```bash

python -m pytest -v

```



The current tests cover finding comparisons and JSON storage behavior.



\## Security Considerations



SecureDev AI is a development aid, not a replacement for professional security review.



\- Static analysis can produce false positives and miss vulnerabilities.

\- AI-generated explanations and remediation suggestions may be incorrect and should be reviewed before use.

\- A finding that disappears from a later scan is considered no longer detected, not automatically confirmed as fixed.

\- Scanning untrusted repositories and sending source code to analysis tools can carry security and privacy risks. This project uses a locally hosted language model for AI analysis.

\- The example vulnerable source code is intentionally insecure and should only be used for testing.



\## Project Status



This is a personal security engineering project exploring static analysis, local AI-assisted vulnerability analysis, scan history, and automated reporting. Features and test coverage are evolving.

