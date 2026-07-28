"""Registry loader."""

from pathlib import Path
from typing import Any

import yaml

from familyos_cli.registry.models import (
    ArtifactDefinition,
    Registry,
)


class RegistryLoader:
    """Load the artifact registry."""

    def load(
        self,
        path: Path = Path("specifications/registry.yaml"),
    ) -> Registry:
        """Load the registry."""

        with path.open(encoding="utf-8") as file:
            data: dict[str, Any] = yaml.safe_load(file)

        artifacts = [
            ArtifactDefinition(
                id=artifact["id"],
                specification=artifact["specification"],
            )
            for artifact in data["artifacts"]
        ]

        return Registry(
            version=data["version"],
            artifacts=artifacts,
        )
