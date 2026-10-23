# SecureDev AI - Security Report

Generated: 2026-10-23T15:38:53.184960+00:00

## Total Findings: 1

## Finding 1

**Rule:** python.lang.security.audit.subprocess-shell-true.subprocess-shell-true

**File:** C:\Users\CK\securedev-ai\examples\vulnerable_sample.py

**Line:** 8

**Severity:** ERROR

**Description:** Found 'subprocess' function 'run' with 'shell=True'. This is dangerous because this call will spawn the command using a shell process. Doing so propagates current shell settings and variables, which makes it much easier for a malicious actor to execute commands. Use 'shell=False' instead.

---
