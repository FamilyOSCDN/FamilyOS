from __future__ import annotations

from familyos_cli.domain.models.domain_specification import (
    DomainSpecification,
)


class DomainSpecificationValidator:
    """Validates a domain specification."""

    def validate(
        self,
        specification: DomainSpecification,
    ) -> None:
        """Validate a domain specification."""

        if not specification.name.strip():
            raise ValueError(
                "Domain name cannot be empty.",
            )

        if not specification.entities:
            raise ValueError(
                "A domain must define at least one entity.",
            )

        entity_names = {entity.name for entity in specification.entities}

        if len(entity_names) != len(
            specification.entities,
        ):
            raise ValueError(
                "Duplicate entity names are not allowed.",
            )
