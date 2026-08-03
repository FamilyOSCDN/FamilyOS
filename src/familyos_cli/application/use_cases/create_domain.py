"""Create domain use case."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.generation.domain_generation_pipeline import (
    DomainGenerationPipeline,
)
from familyos_cli.application.generation.generation_request_factory import (
    GenerationRequestFactory,
)
from familyos_cli.application.generation.generation_specification import (
    GenerationSpecification,
)
from familyos_cli.application.use_cases.get_domain_specification import (
    GetDomainSpecificationUseCase,
)
from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
)


class CreateDomainUseCase:
    """Creates a domain."""

    def __init__(
        self,
        pipeline: DomainGenerationPipeline,
        get_specification: GetDomainSpecificationUseCase,
        request_factory: GenerationRequestFactory,
    ) -> None:
        """Initialize the use case."""

        self._pipeline = pipeline

        self._get_specification = get_specification

        self._request_factory = request_factory

    def execute(
        self,
        domain_name: str,
        destination: Path,
        recipe_name: str | None = None,
        preset: GenerationPresetId | None = None,
    ) -> GenerationSpecification | None:
        """Generate a domain."""

        request = self._request_factory.create(
            domain_name=domain_name,
            recipe_name=recipe_name,
            preset=preset,
        )

        specification = self._get_specification.execute(
            request.domain_name,
        )

        if specification is None:
            return None

        return self._pipeline.generate(
            request=request,
            specification=specification,
            destination=destination,
        )
