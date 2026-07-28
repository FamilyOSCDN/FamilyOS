"""Directory layout for FamilyOS domains."""

from __future__ import annotations

from pathlib import Path


class DirectoryLayout:
    """Describe the directory layout of a domain."""

    def root(
        self,
        domain: str,
    ) -> Path:
        """Return the root directory of a domain."""

        return Path(
            "docs/30-domains",
            domain.lower(),
        )

    def directories(
        self,
        domain: str,
    ) -> tuple[Path, ...]:
        """Return all directories required by a domain."""

        root = self.root(domain)

        return (
            root,
            root / "aggregates",
            root / "entities",
            root / "value-objects",
            root / "repositories",
            root / "services",
            root / "diagrams",
        )

    def documents(
        self,
        domain: str,
    ) -> tuple[Path, ...]:
        """Return all documentation files."""

        root = self.root(domain)

        return (
            root / "README.md",
            root / "Vision.md",
            root / "API.md",
            root / "Business-Rules.md",
            root / "Capabilities.md",
            root / "Domain-Model.md",
            root / "Use-Cases.md",
            root / "Security.md",
        )
