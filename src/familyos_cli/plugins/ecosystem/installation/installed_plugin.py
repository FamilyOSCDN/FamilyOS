"""Installed plugin model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class InstalledPlugin:
    """Represents an installed FamilyOS plugin."""

    name: str
    version: str
    location: str

    def identifier(self) -> str:
        """Return installed plugin identifier."""

        return f"{self.name}@{self.version}"
