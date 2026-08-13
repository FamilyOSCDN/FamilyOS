"""YAML domain specification loader."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from familyos_cli.domain.models.aggregate_descriptor import (
    AggregateDescriptor,
)
from familyos_cli.domain.models.attribute_descriptor import (
    AttributeDescriptor,
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
from familyos_cli.domain.models.value_object_descriptor import (
    ValueObjectDescriptor,
)


class YamlDomainSpecificationLoader:
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
                self._load_entity(
                    entity,
                )
                for entity in data.get(
                    "entities",
                    [],
                )
            ],
            value_objects=[
                self._load_value_object(
                    value_object,
                )
                for value_object in data.get(
                    "value_objects",
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

    def _load_entity(
        self,
        entity: dict[str, Any],
    ) -> EntityDescriptor:
        """Load an entity descriptor."""

        return EntityDescriptor(
            name=entity["name"],
            description=entity.get(
                "description",
                "",
            ),
            attributes=self._normalize_attributes(
                entity.get(
                    "attributes",
                    [],
                ),
            ),
            behaviors=entity.get(
                "behaviors",
                [],
            ),
            business_rules=entity.get(
                "business_rules",
                [],
            ),
            relationships=entity.get(
                "relationships",
                [],
            ),
        )

    def _load_value_object(
        self,
        value_object: dict[str, Any],
    ) -> ValueObjectDescriptor:
        """Load a value object descriptor."""

        return ValueObjectDescriptor(
            name=value_object["name"],
            description=value_object.get(
                "description",
                "",
            ),
            attributes=self._normalize_attributes(
                value_object.get(
                    "attributes",
                    [],
                ),
            ),
            immutable=value_object.get(
                "immutable",
                True,
            ),
        )

    def _normalize_attributes(
        self,
        attributes: list[Any],
    ) -> list[AttributeDescriptor]:
        """Normalize attribute definitions."""

        normalized: list[AttributeDescriptor] = []

        for attribute in attributes:
            if isinstance(
                attribute,
                str,
            ):
                normalized.append(
                    AttributeDescriptor(
                        name=attribute,
                    ),
                )

            elif isinstance(
                attribute,
                dict,
            ):
                normalized.append(
                    AttributeDescriptor(
                        name=attribute["name"],
                        type=attribute.get(
                            "type",
                            "str",
                        ),
                        required=attribute.get(
                            "required",
                            False,
                        ),
                        description=attribute.get(
                            "description",
                            "",
                        ),
                    ),
                )

        return normalized
