"""Document rule model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class DocumentRule:
    """Describe a FamilyOS document rule."""

    id: str

    name: str

    version: str

    severity: str

    description: str = ""

    def __post_init__(self) -> None:
        """Validate the document rule."""

        if not self.id.strip():
            raise ValueError(
                "Document rule id must not be empty."
            )

        if not self.name.strip():
            raise ValueError(
                "Document rule name must not be empty."
            )

        if not self.version.strip():
            raise ValueError(
                "Document rule version must not be empty."
            )

        if not self.severity.strip():
            raise ValueError(
                "Document rule severity must not be empty."
            )
