from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ServiceDescriptor:
    name: str
    description: str

    responsibilities: list[str] = field(default_factory=list)