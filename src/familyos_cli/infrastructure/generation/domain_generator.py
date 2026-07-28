"""Domain artifact generator."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.domain.models.domain_artifact import DomainArtifact
from familyos_cli.domain.models.project_file import ProjectFile
from familyos_cli.infrastructure.generation.file_generator import (
    FileGenerator,
)
from familyos_cli.infrastructure.generation.generation_engine import (
    GenerationEngine,
)


class DomainGenerator:
    """Generate documentation artifacts for a domain."""

    def __init__(
        self,
        generation_engine: GenerationEngine,
        file_generator: FileGenerator,
    ) -> None:
        """Initialize the domain generator."""

        self._generation_engine = generation_engine
        self._file_generator = file_generator

    def generate(
        self,
        artifact: DomainArtifact,
        root: Path,
    ) -> Path:
        """Generate a domain documentation structure."""

        target_directory = artifact.target_directory(root)

        context: dict[str, object] = {
            "name": artifact.display_name,
            "domain_name": artifact.display_name,
            "domain_description": artifact.description,
        }

        files = [
            ProjectFile(
                path="README.md",
                template="domain/README.md.j2",
            ),
            ProjectFile(
                path="API.md",
                template="domain/API.md.j2",
            ),
            ProjectFile(
                path="Capabilities.md",
                template="domain/Capabilities.md.j2",
            ),
            ProjectFile(
                path="Domain-Model.md",
                template="domain/Domain-Model.md.j2",
            ),
            ProjectFile(
                path="Responsibilities.md",
                template="domain/Responsibilities.md.j2",
            ),
            ProjectFile(
                path="Vision.md",
                template="domain/Vision.md.j2",
            ),
        ]

        self._file_generator.generate(
            destination=target_directory,
            files=files,
            context=context,
        )

        return target_directory
