"""Project specification loader."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from familyos_cli.domain.models.project_file import ProjectFile
from familyos_cli.domain.models.project_specification import (
    ProjectSpecification,
)
from familyos_cli.infrastructure.specifications.specification_merger import (
    SpecificationMerger,
)


class SpecificationLoader:
    """Load project specifications from YAML."""

    def __init__(self) -> None:
        """Initialize the specification loader."""
        self._merger = SpecificationMerger()

    def load(
        self,
        path: Path,
    ) -> ProjectSpecification:
        """Load a project specification."""

        with path.open(encoding="utf-8") as file:
            data: dict[str, Any] = yaml.safe_load(file)

        project = data["project"]

        files = []

        for file in project["files"]:
            if isinstance(file, str):
                files.append(
                    ProjectFile(
                        path=file,
                        template=file,
                    ),
                )
            else:
                files.append(
                    ProjectFile(
                        path=file["destination"],
                        template=file["template"],
                    ),
                )

        return ProjectSpecification(
            directories=project["directories"],
            files=files,
        )

    def load_all(
        self,
        paths: list[Path],
    ) -> ProjectSpecification:
        """Load and merge multiple specifications."""

        specifications = [
            self.load(path)
            for path in paths
        ]

        return self._merger.merge(
            specifications,
        )