"""Plugin dependency model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PluginDependency:
    """Represents a plugin dependency requirement."""

    name: str
    minimum_version: str = ""

    def identifier(self) -> str:
        """Return dependency identifier."""

        if self.minimum_version:
            return f"{self.name}>={self.minimum_version}"

        return self.name
