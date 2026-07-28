"""Project file model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class ProjectFile:
    """Represent a file to generate."""

    path: str

    template: str

    context: dict[str, object] = field(
        default_factory=dict,
    )
