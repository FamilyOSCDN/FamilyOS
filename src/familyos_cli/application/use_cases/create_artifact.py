"""Create artifact use case."""

from pathlib import Path

from familyos_cli.domain.contracts.artifact_generator import (
    ArtifactGeneratorContract,
)
from familyos_cli.domain.contracts.domain_generator import (
    DomainGeneratorContract,
)
from familyos_cli.domain.models.artifact import Artifact
from familyos_cli.domain.models.domain_artifact_factory import (
    DomainArtifactFactory,
)
from familyos_cli.infrastructure.generation.artifact_generator import (
    ArtifactGenerator,
)
from familyos_cli.infrastructure.generation.domain_generator import (
    DomainGenerator,
)
from familyos_cli.infrastructure.generation.file_generator import (
    FileGenerator,
)
from familyos_cli.infrastructure.generation.generation_engine import (
    GenerationEngine,
)


class CreateArtifactUseCase:
    """Create a new FamilyOS artifact."""

    def __init__(
        self,
        generator: ArtifactGeneratorContract | None = None,
        domain_generator: DomainGeneratorContract | None = None,
    ) -> None:
        """Initialize the use case."""

        if generator is None:
            generator = ArtifactGenerator()

        if domain_generator is None:
            domain_generator = DomainGenerator(
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
        """Execute the use case."""

        if artifact_type == "domain":
            domain_artifact = DomainArtifactFactory.create(
                name=name,
            )

            self._domain_generator.generate(
                artifact=domain_artifact,
                root=Path("."),
            )

            return

        artifact = Artifact(
            type=artifact_type,
            name=name,
        )

        self.generator.generate(
            artifact_type=artifact.type,
            name=artifact.name,
        )