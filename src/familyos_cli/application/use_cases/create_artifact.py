"""Create artifact use case."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.ports.generation.artifact_generator import (
    ArtifactGenerator,
)
from familyos_cli.domain.contracts.domain_generator import (
    DomainGeneratorContract,
)
from familyos_cli.domain.models.domain_artifact import (
    DomainArtifact,
)
from familyos_cli.infrastructure.generation.artifact_generator import (
    ArtifactGenerator as InfrastructureArtifactGenerator,
)
from familyos_cli.infrastructure.generation.domain_generator import (
    DomainGenerator as InfrastructureDomainGenerator,
)
from familyos_cli.infrastructure.generation.file_generator import (
    FileGenerator,
)
from familyos_cli.infrastructure.generation.generation_engine import (
    GenerationEngine,
)


class CreateArtifactUseCase:
    """Create an artifact."""

    def __init__(
        self,
        generator: ArtifactGenerator | None = None,
        domain_generator: DomainGeneratorContract | None = None,
    ) -> None:
        """Initialize use case."""

        if generator is None:
            generator = InfrastructureArtifactGenerator()

        if domain_generator is None:
            domain_generator = InfrastructureDomainGenerator(
                generation_engine=GenerationEngine(),
                file_generator=FileGenerator(),
            )

        self.generator = generator
        self._domain_generator = domain_generator

    def execute(
        self,
        artifact_type: str,
        name: str,
    ) -> None:
        """Create artifact."""

        if artifact_type == "domain":
            artifact = DomainArtifact(
                name=name,
            )

            self._domain_generator.generate(
                artifact=artifact,
                root=Path("."),
            )
            return

        self.generator.generate(
            artifact_type=artifact_type,
            name=name,
        )
