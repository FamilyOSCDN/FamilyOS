"""Project specification merger."""

from __future__ import annotations

from familyos_cli.domain.models.project_specification import (
    ProjectSpecification,
)


class SpecificationMerger:
    """Merge multiple project specifications."""

    def merge(
        self,
        specifications: list[ProjectSpecification],
    ) -> ProjectSpecification:
        """Merge specifications into one."""

        if not specifications:
            return ProjectSpecification(
                directories=[],
                files=[],
            )

        directories: list[str] = []
        files = []

        for specification in specifications:
            directories.extend(
                specification.directories,
            )
            files.extend(
                specification.files,
            )

        return ProjectSpecification(
            directories=directories,
            files=files,
        )