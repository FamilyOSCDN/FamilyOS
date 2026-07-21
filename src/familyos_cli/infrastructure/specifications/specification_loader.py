"""Project specification loader."""

from pathlib import Path
from typing import Any

import yaml

from familyos_cli.domain.models.project_file import ProjectFile
from familyos_cli.domain.models.project_specification import (
    ProjectSpecification,
)


class SpecificationLoader:
    """Load project specifications from YAML."""

    def load(self, path: Path) -> ProjectSpecification:
        """Load a project specification."""

        with path.open(encoding="utf-8") as file:
            data: dict[str, Any] = yaml.safe_load(file)

        project = data["project"]

        files = [
            ProjectFile(
                path=file["destination"],
                template=file["template"],
            )
            for file in project["files"]
        ]

        return ProjectSpecification(
            directories=project["directories"],
            files=files,
        )