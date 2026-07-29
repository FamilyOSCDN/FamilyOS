from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class AttributeDescriptor:
    """Describe an attribute of a domain model."""

    name: str

    type: str = "str"

    required: bool = False

    description: str = ""
