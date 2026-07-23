"""Plugin models."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(
    frozen=True,
    slots=True,
)
class PluginDescriptor:
    """Describe an installed plugin."""

    id: str
    name: str
    version: str

    author: str
    description: str

    module: str
    class_name: str

    path: Path

    enabled: bool = True