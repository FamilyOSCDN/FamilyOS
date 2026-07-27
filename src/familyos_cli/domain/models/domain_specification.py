from __future__ import annotations

from dataclasses import dataclass

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
    entities: list[EntityDescriptor]
    aggregates: list[AggregateDescriptor]
    repositories: list[RepositoryDescriptor]
    services: list[ServiceDescriptor]