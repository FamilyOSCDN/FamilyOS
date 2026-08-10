"""Document profile registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.documents.profiles.document_profile import (
    DocumentProfile,
)


class DocumentProfileRegistry:
    """Registry for FamilyOS document profiles."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._profiles: dict[str, DocumentProfile] = {}

    def register(
        self,
        profile: DocumentProfile,
    ) -> None:
        """Register a document profile."""

        self._profiles[profile.id] = profile

    def get(
        self,
        profile_id: str,
    ) -> DocumentProfile | None:
        """Return a profile by identifier."""

        return self._profiles.get(
            profile_id,
        )

    def list(
        self,
    ) -> tuple[DocumentProfile, ...]:
        """Return registered profiles."""

        return tuple(
            self._profiles.values(),
        )