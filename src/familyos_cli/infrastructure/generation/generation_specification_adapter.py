"""Generation specification adapter."""

from __future__ import annotations

from familyos_cli.application.generation.generation_specification import (
    GenerationSpecification,
)
from familyos_cli.domain.models.project_file import (
    ProjectFile,
)
from familyos_cli.domain.models.project_specification import (
    ProjectSpecification,
)


class GenerationSpecificationAdapter:
    """Adapt execution specifications to filesystem specifications."""

    def adapt(
        self,
        specification: GenerationSpecification,
    ) -> ProjectSpecification:
        """Convert generation specification into project specification."""

        files = [
            ProjectFile(
                path=artifact.destination,
                template=artifact.template,
            )
            for artifact in specification.artifacts
        ]

        return ProjectSpecification(
            directories=specification.directories,
            files=files,
        )
