"""Document model."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.plugins.builtin.documents.models.document_type import (
    DocumentType,
)
from familyos_cli.plugins.builtin.documents.models.document_version import (
    DocumentVersion,
)


@dataclass(frozen=True)
class Document:
    """Represents a family document."""

    identifier: str
    title: str
    document_type: DocumentType
    owner: str
    version: DocumentVersion

    def __post_init__(
        self,
    ) -> None:
        """Validate document invariants."""

        if not self.identifier.strip():
            raise ValueError(
                "Document identifier must not be empty.",
            )

        if not self.title.strip():
            raise ValueError(
                "Document title must not be empty.",
            )

        if not self.owner.strip():
            raise ValueError(
                "Document owner must not be empty.",
            )

    def is_private(self) -> bool:
        """Return whether document belongs to a private owner."""

        return bool(self.owner)
