"""Create domain use case."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.generation.domain_generation_pipeline import (
    DomainGenerationPipeline,
)
from familyos_cli.application.generation.generation_specification import (
    GenerationSpecification,
)
from familyos_cli.application.use_cases.get_domain_specification import (
    GetDomainSpecificationUseCase,
)


class CreateDomainUseCase:
    """Creates a domain."""

    def __init__(
        self,
        pipeline: DomainGenerationPipeline,
        get_specification: GetDomainSpecificationUseCase,
    ) -> None:
        self._pipeline = pipeline
        self._get_specification = get_specification

    def execute(
        self,
        domain_name: str,
        destination: Path,
    ) -> GenerationSpecification | None:
        """Generate a domain."""

        specification = self._get_specification.execute(
            domain_name,
        )

        if specification is None:
            return None

        return self._pipeline.generate(
            specification=specification,
            destination=destination,
        )
