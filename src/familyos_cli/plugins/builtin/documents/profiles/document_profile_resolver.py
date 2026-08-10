"""Document profile resolver."""

from __future__ import annotations

from familyos_cli.plugins.builtin.documents.domain.document_level import (
    DocumentLevel,
)
from familyos_cli.plugins.builtin.documents.profiles.document_profile import (
    DocumentProfile,
)


class DocumentProfileResolver:
    """Resolve document profiles."""

    def resolve(
        self,
        profile: DocumentProfile,
    ) -> DocumentLevel:
        """Resolve profile level."""

        return DocumentLevel(
            profile.level.lower(),
        )