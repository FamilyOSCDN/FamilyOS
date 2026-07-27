from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class RepositoryDescriptor:
    name: str
    description: str

    aggregate: str

    operations: list[str] = field(default_factory=list)