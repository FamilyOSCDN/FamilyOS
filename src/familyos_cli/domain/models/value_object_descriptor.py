from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class ValueObjectDescriptor:
    """Describe a value object."""

    name: str
    description: str

    attributes: list[str] = field(default_factory=list)

    immutable: bool = True
