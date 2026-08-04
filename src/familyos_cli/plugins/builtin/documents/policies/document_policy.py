"""Document policy model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class DocumentPolicy:
    """Describe a FamilyOS document policy."""

    id: str

    name: str

    version: str

    description: str = ""

    def __post_init__(self) -> None:
        """Validate the document policy."""

        if not self.id.strip():
            raise ValueError(
                "Document policy id must not be empty."
            )

        if not self.name.strip():
            raise ValueError(
                "Document policy name must not be empty."
            )

        if not self.version.strip():
            raise ValueError(
                "Document policy version must not be empty."
            )
