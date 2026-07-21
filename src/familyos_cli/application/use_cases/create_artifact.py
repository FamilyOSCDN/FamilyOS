"""Create artifact use case."""

from familyos_cli.domain.models.artifact import Artifact
from familyos_cli.infrastructure.generation.artifact_generator import (
    ArtifactGenerator,
)


class CreateArtifactUseCase:
    """Create a new FamilyOS artifact."""

    def __init__(self) -> None:
        """Initialize the use case."""
        self.generator = ArtifactGenerator()

    def execute(
        self,
        artifact_type: str,
        name: str,
    ) -> None:
        """Execute the use case."""

        artifact = Artifact(
            type=artifact_type,
            name=name,
        )

        self.generator.generate(artifact)