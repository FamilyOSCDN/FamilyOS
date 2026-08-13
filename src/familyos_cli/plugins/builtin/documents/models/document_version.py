"""Document version model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentVersion:
    """Represents a document revision."""

    version: int
    checksum: str

    def __post_init__(
        self,
    ) -> None:
        """Validate document version invariants."""

        if self.version < 1:
            raise ValueError(
                "Document version must be greater than zero.",
            )

        if not self.checksum.strip():
            raise ValueError(
                "Document version checksum must not be empty.",
            )

    def is_initial(self) -> bool:
        """Return whether this is the first version."""

        return self.version == 1
