"""Generation specification loader."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from familyos_cli.application.generation.generation_artifact import (
    GenerationArtifact,
)
from familyos_cli.application.generation.generation_specification import (
    GenerationSpecification,
)
from familyos_cli.infrastructure.specifications.specification_merger import (
    SpecificationMerger,
)


class SpecificationLoader:
    """Load generation specifications from YAML."""

    def __init__(self) -> None:
        """Initialize the specification loader."""

        self._merger = SpecificationMerger()

    def load(
        self,
        path: Path,
    ) -> GenerationSpecification:
        """Load a generation specification."""

        with path.open(
            encoding="utf-8",
        ) as file:
            data: dict[str, Any] = yaml.safe_load(
                file,
            )

        project = data["project"]

        artifacts = []

        for file_definition in project["files"]:
            if isinstance(
                file_definition,
                str,
            ):
                artifacts.append(
                    GenerationArtifact(
                        destination=file_definition,
                        template=file_definition,
                    ),
                )
            else:
                artifacts.append(
                    GenerationArtifact(
                        destination=file_definition["destination"],
                        template=file_definition["template"],
                    ),
                )

        return GenerationSpecification(
            directories=project["directories"],
            artifacts=artifacts,
        )

    def load_all(
        self,
        paths: list[Path],
    ) -> GenerationSpecification:
        """Load and merge multiple specifications."""

        specifications = [
            self.load(path)
            for path in paths
        ]

        return self._merger.merge(
            specifications,
        )
