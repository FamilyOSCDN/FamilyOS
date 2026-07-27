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
from familyos_cli.domain.models.value_object_descriptor import (
    ValueObjectDescriptor,
)


@dataclass(slots=True)
class DomainDescriptor:
    name: str
    title: str
    description: str

    owner: str = "FamilyOS Team"
    version: str = "1.0.0"

    aggregates: list[AggregateDescriptor] = field(default_factory=list)
    entities: list[EntityDescriptor] = field(default_factory=list)
    value_objects: list[ValueObjectDescriptor] = field(default_factory=list)
    repositories: list[RepositoryDescriptor] = field(default_factory=list)
    services: list[ServiceDescriptor] = field(default_factory=list)

    events: list[str] = field(default_factory=list)
    commands: list[str] = field(default_factory=list)

    tags: list[str] = field(default_factory=list)