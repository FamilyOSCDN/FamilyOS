from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class PluginContext:
    """Context provided to plugins by the FamilyOS CLI."""

    project_name: str
    output_directory: str
    variables: dict[str, Any] = field(default_factory=dict)
