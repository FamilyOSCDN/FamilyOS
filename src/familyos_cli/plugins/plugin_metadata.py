from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PluginMetadata:
    """Describes a FamilyOS plugin."""

    name: str
    version: str

    author: str = ""
    description: str = ""
    homepage: str = ""
    license: str = ""
    api_version: str = "1.0"
