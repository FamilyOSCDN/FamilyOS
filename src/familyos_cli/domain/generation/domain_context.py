"""Context used during domain generation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(
    frozen=True,
    slots=True,
)
class DomainContext:
    """Represents the context required to generate a domain."""

    name: str
    slug: str
    namespace: str
    title: str
    description: str = ""
