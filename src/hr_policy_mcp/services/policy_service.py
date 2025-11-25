from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List

import PyPDF2


logger = logging.getLogger(__name__)


class PolicyService:
    """Service for loading and reading HR policy PDF files."""

    def __init__(self, policy_dir: Path) -> None:
        self.policy_dir = policy_dir
        self.policies: Dict[str, Path] = {}
        self._load_policies()

    def _load_policies(self) -> None:
        """Load all PDF policy files from the policy directory."""
        if not self.policy_dir.exists():
            logger.warning("Policy directory not found: %s", self.policy_dir)
            return

        for pdf_file in sorted(self.policy_dir.glob("*.pdf")):
            policy_name = pdf_file.stem.replace("_", " ").title()
            self.policies[policy_name] = pdf_file
            logger.info("Loaded policy: %s", policy_name)

    def get_policy_names(self) -> List[str]:
        """Return the available policy names."""
        return list(self.policies.keys())

    def get_policy_content(self, policy_name: str) -> str:
        """Return the text content of a policy by name."""
        pdf_path = self.policies.get(policy_name)
        if pdf_path is None:
            raise ValueError(f"Policy '{policy_name}' not found")
        try:
            with pdf_path.open("rb") as policy_file:
                reader = PyPDF2.PdfReader(policy_file)
                return "\n\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as exc:
            logger.error("Failed to read policy '%s' from %s: %s", policy_name, pdf_path, exc)
            raise
