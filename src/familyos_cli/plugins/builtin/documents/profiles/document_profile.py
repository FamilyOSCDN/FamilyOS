"""Document profile model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.builtin.documents.domain.document_level import (
    DocumentLevel,
)


@dataclass(
    frozen=True,
    slots=True,
)
class DocumentProfile:
    """Describe a FamilyOS document profile."""

    id: str

    name: str

    version: str

    level: str

    description: str = ""

    def __post_init__(
        self,
    ) -> None:
        """Validate document profile invariants."""

        if not self.id.strip():
            raise ValueError(
                "Document profile id cannot be empty.",
            )

        if not self.name.strip():
            raise ValueError(
                "Document profile name cannot be empty.",
            )

        if not self.version.strip():
            raise ValueError(
                "Document profile version cannot be empty.",
            )

        if not self.level.strip():
            raise ValueError(
                "Document profile level cannot be empty.",
            )

        try:
            DocumentLevel(
                self.level.lower(),
            )
        except ValueError as error:
            raise ValueError(
                f"Unsupported document profile level: {self.level}.",
            ) from error
