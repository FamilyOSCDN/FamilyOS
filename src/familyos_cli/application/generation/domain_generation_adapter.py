"""Adapter domain generation plans to project specifications."""

from __future__ import annotations

from familyos_cli.domain.generation.domain_generation_plan import (
    DomainGenerationPlan,
)
from familyos_cli.domain.models.project_file import (
    ProjectFile,
)
from familyos_cli.domain.models.project_specification import (
    ProjectSpecification,
)


class DomainGenerationAdapter:
    """Convert domain generation plans into project specifications."""

    def adapt(
        self,
        plan: DomainGenerationPlan,
    ) -> ProjectSpecification:
        """Create a project specification from a domain plan."""

        files = [
            ProjectFile(
                path=artifact.target_path,
                template=artifact.template,
            )
            for artifact in plan.artifacts
        ]

        return ProjectSpecification(
            files=files,
        )