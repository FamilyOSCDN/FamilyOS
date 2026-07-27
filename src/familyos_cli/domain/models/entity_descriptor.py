from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class EntityDescriptor:
    name: str
    description: str

    attributes: list[str] = field(default_factory=list)

    behaviors: list[str] = field(default_factory=list)