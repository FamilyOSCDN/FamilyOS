from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class PluginContext:
    """Context provided to plugins by the FamilyOS CLI."""

    project_name: str
    output_directory: str
    plugin_directory: Path | None = None
    variables: dict[str, Any] = field(default_factory=dict)
