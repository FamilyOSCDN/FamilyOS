"""Domain template provider."""

from __future__ import annotations


class TemplateProvider:
    """Provide templates required for domain generation."""

    def templates(self) -> tuple[str, ...]:
        """Return domain templates."""

        return (
            "README.md.j2",
            "Vision.md.j2",
            "API.md.j2",
            "Business-Rules.md.j2",
            "Capabilities.md.j2",
            "Domain-Model.md.j2",
            "Use-Cases.md.j2",
            "Security.md.j2",
        )