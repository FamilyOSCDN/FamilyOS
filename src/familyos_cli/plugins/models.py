"""Plugin models."""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PluginDescriptor:
    """Describe an installed plugin."""

    id: str
    name: str
    version: str
    author: str
    description: str
    path: Path