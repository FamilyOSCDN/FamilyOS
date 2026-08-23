"""Validate canonical repository structure for build execution."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.build.repository_layout import RepositoryLayout
from familyos_cli.application.build.repository_layout_validation import (
    RepositoryLayoutValidationResult,
)


class RepositoryLayoutValidator:
    """Prevent build outputs from conflicting with authoritative repository state."""

    def validate_output_dir(
        self,
        *,
        layout: RepositoryLayout,
        output_dir: Path,
    ) -> RepositoryLayoutValidationResult:
        """Validate one resolved build output location."""

        resolved_output = self._resolve(layout, output_dir)
        project_root = layout.project_root.resolve(strict=False)

        if resolved_output == project_root:
            return RepositoryLayoutValidationResult(
                successful=False,
                diagnostic=(
                    "build output directory must not be the repository root"
                ),
            )

        if self._overlaps_authoritative_directory(layout, resolved_output):
            return RepositoryLayoutValidationResult(
                successful=False,
                diagnostic=(
                    "build output directory must not overlap "
                    "authoritative repository content"
                ),
            )

        if self._replaces_authoritative_file(layout, resolved_output):
            return RepositoryLayoutValidationResult(
                successful=False,
                diagnostic=(
                    "build output directory must not replace "
                    "authoritative repository files"
                ),
            )

        return RepositoryLayoutValidationResult(
            successful=True,
        )

    def validate_evidence_output(
        self,
        *,
        layout: RepositoryLayout,
        evidence_output: Path | None,
        package_output_dir: Path,
    ) -> RepositoryLayoutValidationResult:
        """Validate one optional evidence file against canonical layout."""

        if evidence_output is None:
            return RepositoryLayoutValidationResult(successful=True)

        resolved_evidence = self._resolve(layout, evidence_output)
        project_root = layout.project_root.resolve(strict=False)

        if resolved_evidence == project_root:
            return RepositoryLayoutValidationResult(
                successful=False,
                diagnostic=(
                    "build evidence output must not be the repository root"
                ),
            )

        if self._overlaps_authoritative_directory(layout, resolved_evidence):
            return RepositoryLayoutValidationResult(
                successful=False,
                diagnostic=(
                    "build evidence output must not overlap "
                    "authoritative repository content"
                ),
            )

        if self._replaces_authoritative_file(layout, resolved_evidence):
            return RepositoryLayoutValidationResult(
                successful=False,
                diagnostic=(
                    "build evidence output must not replace "
                    "authoritative repository files"
                ),
            )

        resolved_package_output = self._resolve(
            layout,
            package_output_dir,
        )

        if (
            resolved_evidence == resolved_package_output
            or resolved_evidence.is_relative_to(resolved_package_output)
            or resolved_package_output.is_relative_to(resolved_evidence)
        ):
            return RepositoryLayoutValidationResult(
                successful=False,
                diagnostic=(
                    "build evidence output must not overlap "
                    "package output directory"
                ),
            )

        if resolved_evidence.is_dir():
            return RepositoryLayoutValidationResult(
                successful=False,
                diagnostic="build evidence output must be a file path",
            )

        return RepositoryLayoutValidationResult(successful=True)

    @staticmethod
    def _resolve(layout: RepositoryLayout, path: Path) -> Path:
        resolved_path = (
            path
            if path.is_absolute()
            else layout.project_root / path
        )
        return resolved_path.resolve(strict=False)

    @staticmethod
    def _overlaps_authoritative_directory(
        layout: RepositoryLayout,
        path: Path,
    ) -> bool:
        return any(
            path == authoritative_directory.resolve(strict=False)
            or path.is_relative_to(
                authoritative_directory.resolve(strict=False),
            )
            for authoritative_directory in layout.authoritative_directories
        )

    @staticmethod
    def _replaces_authoritative_file(
        layout: RepositoryLayout,
        path: Path,
    ) -> bool:
        return any(
            path == authoritative_file.resolve(strict=False)
            for authoritative_file in layout.authoritative_files
        )
