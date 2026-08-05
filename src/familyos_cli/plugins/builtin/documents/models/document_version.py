"""Document version model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentVersion:
    """Represents a document revision."""

    version: int
    checksum: str

    def is_initial(self) -> bool:
        """Return whether this is the first version."""

        return self.version == 1
