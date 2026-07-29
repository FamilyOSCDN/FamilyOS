from __future__ import annotations

from dataclasses import dataclass, field

from familyos_cli.domain.models.attribute_descriptor import (
    AttributeDescriptor,
)


@dataclass(frozen=True, slots=True)
class EntityDescriptor:
    """Describe an entity."""

    name: str

    description: str = ""

    attributes: list[AttributeDescriptor] = field(
        default_factory=list,
    )

    behaviors: list[str] = field(
        default_factory=list,
    )

    business_rules: list[str] = field(
        default_factory=list,
    )

    relationships: list[str] = field(
        default_factory=list,
    )
