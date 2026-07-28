"""YAML domain specification loader."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from familyos_cli.domain.models.aggregate_descriptor import (
    AggregateDescriptor,
)
from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
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
from familyos_cli.infrastructure.specifications.domain_specification_loader import (
    DomainSpecificationLoader,
)


class YamlDomainSpecificationLoader(
    DomainSpecificationLoader,
):
    """Load domain specifications from YAML."""

    def load(
        self,
        path: Path,
    ) -> DomainSpecification:
        """Load a domain specification from YAML."""

        with path.open(
            encoding="utf-8",
        ) as file:
            data: dict[str, Any] = yaml.safe_load(file)

        domain = data["domain"]

        return DomainSpecification(
            name=domain["name"],
            entities=[
                EntityDescriptor(
                    **entity,
                )
                for entity in data.get(
                    "entities",
                    [],
                )
            ],
            aggregates=[
                AggregateDescriptor(
                    **aggregate,
                )
                for aggregate in data.get(
                    "aggregates",
                    [],
                )
            ],
            repositories=[
                RepositoryDescriptor(
                    **repository,
                )
                for repository in data.get(
                    "repositories",
                    [],
                )
            ],
            services=[
                ServiceDescriptor(
                    **service,
                )
                for service in data.get(
                    "services",
                    [],
                )
            ],
            business_rules=domain.get(
                "business_rules",
                [],
            ),
        )
