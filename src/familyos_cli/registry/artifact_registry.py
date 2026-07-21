"""Artifact registry."""

from familyos_cli.registry.loader import RegistryLoader
from familyos_cli.registry.models import (
    ArtifactDefinition,
    Registry,
)


class ArtifactRegistry:
    """Provide access to registered artifacts."""

    def __init__(self) -> None:
        """Initialize the registry."""

        self._loader = RegistryLoader()
        self.reload()

    def reload(self) -> None:
        """Reload the registry."""

        self._registry: Registry = self._loader.load()

    def list(self) -> list[ArtifactDefinition]:
        """Return all registered artifacts."""

        return self._registry.artifacts

    def exists(
        self,
        artifact_id: str,
    ) -> bool:
        """Return whether an artifact exists."""

        return any(
            artifact.id == artifact_id
            for artifact in self._registry.artifacts
        )

    def get(
        self,
        artifact_id: str,
    ) -> ArtifactDefinition:
        """Return one artifact."""

        for artifact in self._registry.artifacts:
            if artifact.id == artifact_id:
                return artifact

        raise ValueError(
            f'Unknown artifact "{artifact_id}".',
        )

    def validate(self) -> None:
        """Validate the registry."""

        ids: set[str] = set()

        for artifact in self._registry.artifacts:
            if artifact.id in ids:
                raise ValueError(
                    f'Duplicate artifact "{artifact.id}".',
                )

            ids.add(artifact.id)