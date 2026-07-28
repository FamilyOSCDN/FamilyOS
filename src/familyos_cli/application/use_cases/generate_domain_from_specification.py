from __future__ import annotations

from pathlib import Path

from familyos_cli.application.generation.domain_generation_pipeline import (
    DomainGenerationPipeline,
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
    ) -> None:
        self._loader = loader
        self._validator = validator
        self._pipeline = pipeline

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

        self._pipeline.generate(
            specification=specification,
            destination=destination,
        )
