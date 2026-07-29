from __future__ import annotations

from dataclasses import dataclass, field

from familyos_cli.domain.models.attribute_descriptor import (
    AttributeDescriptor,
)


@dataclass(frozen=True, slots=True)
class ValueObjectDescriptor:
    """Describe a value object."""

    name: str

    description: str

    attributes: list[AttributeDescriptor] = field(
        default_factory=list,
    )

    immutable: bool = True
