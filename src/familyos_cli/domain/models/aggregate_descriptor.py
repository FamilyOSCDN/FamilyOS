from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class AggregateDescriptor:
    name: str
    description: str

    root_entity: str

    entities: list[str] = field(default_factory=list)

    invariants: list[str] = field(default_factory=list)
