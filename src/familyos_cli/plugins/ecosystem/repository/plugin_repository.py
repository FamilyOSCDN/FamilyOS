"""Plugin repository model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PluginRepository:
    """Represents a source of FamilyOS plugins."""

    name: str
    url: str
    repository_type: str
    enabled: bool = True

    def identifier(self) -> str:
        """Return repository identifier."""

        return self.name.lower().replace(" ", "-")
