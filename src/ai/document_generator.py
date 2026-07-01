"""Document generation orchestrator."""
from typing import Dict, List, Optional
from .llm_client import LLMClient, LLMProvider
from .prompts import build_readme_prompt, build_contributing_prompt, LICENSE_TEMPLATES


class DocumentGenerator:
    """Generates project documentation using AI."""

    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client

    def generate_readme(self, project_context: str) -> str:
        """Generate README.md content."""
        system, prompt = build_readme_prompt(project_context)
        return self.llm.generate(prompt, system)

    def generate_contributing(self, project_context: str) -> str:
        """Generate CONTRIBUTING.md content."""
        system, prompt = build_contributing_prompt(project_context)
        return self.llm.generate(prompt, system)

    def generate_license(self, license_type: str = "mit", author: str = "", year: int = 2026) -> str:
        """Generate LICENSE file content."""
        template = LICENSE_TEMPLATES.get(license_type.lower(), LICENSE_TEMPLATES["mit"])
        return template.format(year=year, author=author or "[Your Name]")

    def generate_all(self, project_context: str, options: Dict) -> Dict[str, str]:
        """Generate all requested documents."""
        documents = {}

        if options.get("readme", True):
            documents["README.md"] = self.generate_readme(project_context)

        if options.get("contributing", False):
            documents["CONTRIBUTING.md"] = self.generate_contributing(project_context)

        if options.get("license", False):
            documents["LICENSE"] = self.generate_license(
                options.get("license_type", "mit"),
                options.get("author", "")
            )

        return documents
