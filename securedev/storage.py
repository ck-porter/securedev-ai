import json
from pathlib import Path


class Storage:

    def save_findings(self, findings, file_path):
        path = Path(file_path)

        # Create the parent directory if it doesn't exist.
        path.parent.mkdir(parents=True, exist_ok=True)

        # Save findings as readable JSON.
        with path.open("w", encoding="utf-8") as file:
            json.dump(findings, file, indent=2)

    def load_findings(self, file_path):
        path = Path(file_path)

        # No previous scan exists on the first run.
        if not path.exists():
            return []

        # Load existing findings from JSON.
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)