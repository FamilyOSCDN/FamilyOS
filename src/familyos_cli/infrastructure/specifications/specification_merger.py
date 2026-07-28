"""Generation specification merger."""

from __future__ import annotations

from familyos_cli.application.generation.generation_specification import (
    GenerationSpecification,
)


class SpecificationMerger:
    """Merge multiple generation specifications."""

    def merge(
        self,
        specifications: list[GenerationSpecification],
    ) -> GenerationSpecification:
        """Merge specifications into one."""

        if not specifications:
            return GenerationSpecification()

        directories: list[str] = []

        artifacts = []

        for specification in specifications:
            directories.extend(
                specification.directories,
            )

            artifacts.extend(
                specification.artifacts,
            )

        return GenerationSpecification(
            directories=directories,
            artifacts=artifacts,
        )
