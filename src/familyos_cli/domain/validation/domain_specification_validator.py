from __future__ import annotations

from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class DomainSpecificationValidator:
    """Validates domain specifications before generation."""

    def validate(
        self,
        specification: DomainSpecification,
    ) -> None:
        self._validate_name(specification)
        self._validate_entities(specification)
        self._validate_aggregates(specification)
        self._validate_repositories(specification)
        self._validate_services(specification)

    def _validate_name(
        self,
        specification: DomainSpecification,
    ) -> None:
        if not specification.name.strip():
            raise ValueError("Domain name cannot be empty.")

    def _validate_entities(
        self,
        specification: DomainSpecification,
    ) -> None:
        names = [entity.name for entity in specification.entities]

        if len(names) != len(set(names)):
            raise ValueError("Duplicate entity names detected.")

    def _validate_aggregates(
        self,
        specification: DomainSpecification,
    ) -> None:
        entity_names = {entity.name for entity in specification.entities}

        for aggregate in specification.aggregates:
            if aggregate.root_entity not in entity_names:
                raise ValueError(
                    f"Unknown aggregate root entity: {aggregate.root_entity}"
                )

    def _validate_repositories(
        self,
        specification: DomainSpecification,
    ) -> None:
        aggregate_names = {aggregate.name for aggregate in specification.aggregates}

        for repository in specification.repositories:
            if repository.aggregate not in aggregate_names:
                raise ValueError(f"Unknown aggregate reference: {repository.aggregate}")

    def _validate_services(
        self,
        specification: DomainSpecification,
    ) -> None:
        names = [service.name for service in specification.services]

        if len(names) != len(set(names)):
            raise ValueError("Duplicate service names detected.")
