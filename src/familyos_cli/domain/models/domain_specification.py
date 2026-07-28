from __future__ import annotations

from dataclasses import dataclass, field

from familyos_cli.domain.models.aggregate_descriptor import (
    AggregateDescriptor,
)
from familyos_cli.domain.models.entity_descriptor import (
    EntityDescriptor,
)
from familyos_cli.domain.models.repository_descriptor import (
    RepositoryDescriptor,
)
from familyos_cli.domain.models.service_descriptor import (
    ServiceDescriptor,
)


@dataclass(frozen=True, slots=True)
class DomainSpecification:
    """Defines a complete domain generation specification."""

    name: str

    entities: list[EntityDescriptor] = field(
        default_factory=list,
    )

    aggregates: list[AggregateDescriptor] = field(
        default_factory=list,
    )

    repositories: list[RepositoryDescriptor] = field(
        default_factory=list,
    )

    services: list[ServiceDescriptor] = field(
        default_factory=list,
    )

    business_rules: list[str] = field(
        default_factory=list,
    )
