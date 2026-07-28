"""Generate domain from specification use case."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.generation.domain_generation_pipeline import (
    DomainGenerationPipeline,
)
from familyos_cli.application.generation.generation_request_factory import (
    GenerationRequestFactory,
)
from familyos_cli.application.specifications.domain_specification_loader_service import (
    DomainSpecificationLoaderService,
)
from familyos_cli.domain.specifications.domain_specification_validator import (
    DomainSpecificationValidator,
)


class GenerateDomainFromSpecificationUseCase:
    """Generate an entire domain from a specification."""

    def __init__(
        self,
        loader: DomainSpecificationLoaderService,
        validator: DomainSpecificationValidator,
        pipeline: DomainGenerationPipeline,
        request_factory: GenerationRequestFactory,
    ) -> None:
        """Initialize the use case."""

        self._loader = loader

        self._validator = validator

        self._pipeline = pipeline

        self._request_factory = request_factory

    def execute(
        self,
        specification_path: Path,
        destination: Path,
    ) -> None:
        """Load, validate and generate a domain."""

        specification = self._loader.load(
            specification_path,
        )

        self._validator.validate(
            specification,
        )

        request = self._request_factory.create(
            specification.name,
        )

        self._pipeline.generate(
            request=request,
            specification=specification,
            destination=destination,
        )
