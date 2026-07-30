"""Plugin package model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PluginPackage:
    """Represents a distributable FamilyOS plugin package."""

    name: str
    version: str
    source: str
    checksum: str = ""
    signature: str = ""

    def identifier(self) -> str:
        """Return unique package identifier."""

        return f"{self.name}@{self.version}"
