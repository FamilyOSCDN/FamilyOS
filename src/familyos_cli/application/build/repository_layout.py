"""Canonical repository-layout contract for Build Framework execution."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class RepositoryLayout:
    """Canonical repository paths relevant to build execution."""

    project_root: Path
    source_dir: Path
    tests_dir: Path
    documentation_dir: Path
    scripts_dir: Path
    automation_dir: Path
    specifications_dir: Path
    templates_dir: Path
    project_configuration: Path
    dependency_lock: Path
    default_output_dir: Path
    default_build_dir: Path
    generated_dir: Path

    @classmethod
    def from_project_root(
        cls,
        project_root: Path,
    ) -> RepositoryLayout:
        """Derive the canonical repository layout from one project root."""

        return cls(
            project_root=project_root,
            source_dir=project_root / "src",
            tests_dir=project_root / "tests",
            documentation_dir=project_root / "docs",
            scripts_dir=project_root / "scripts",
            automation_dir=project_root / ".github",
            specifications_dir=project_root / "specifications",
            templates_dir=project_root / "templates",
            project_configuration=project_root / "pyproject.toml",
            dependency_lock=project_root / "requirements.txt",
            default_output_dir=project_root / "dist",
            default_build_dir=project_root / "build",
            generated_dir=project_root / "generated",
        )

    @property
    def authoritative_directories(self) -> tuple[Path, ...]:
        """Return canonical authoritative repository directories."""

        return (
            self.source_dir,
            self.tests_dir,
            self.documentation_dir,
            self.scripts_dir,
            self.automation_dir,
            self.specifications_dir,
            self.templates_dir,
        )

    @property
    def authoritative_files(self) -> tuple[Path, ...]:
        """Return canonical authoritative build-control files."""

        return (
            self.project_configuration,
            self.dependency_lock,
        )

    @property
    def authoritative_paths(self) -> tuple[Path, ...]:
        """Return canonical paths protected from build-output placement."""

        return (
            *self.authoritative_directories,
            *self.authoritative_files,
        )

    @property
    def derived_directories(self) -> tuple[Path, ...]:
        """Return canonical repository-local derived-state directories."""

        return (
            self.default_output_dir,
            self.default_build_dir,
            self.generated_dir,
        )
