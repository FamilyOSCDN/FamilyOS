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

        resolved_output = (
            output_dir
            if output_dir.is_absolute()
            else layout.project_root / output_dir
        )

        resolved_output = resolved_output.resolve(strict=False)
        project_root = layout.project_root.resolve(strict=False)

        if resolved_output == project_root:
            return RepositoryLayoutValidationResult(
                successful=False,
                diagnostic=(
                    "build output directory must not be the repository root"
                ),
            )

        for authoritative_directory in layout.authoritative_directories:
            resolved_authoritative_directory = (
                authoritative_directory.resolve(strict=False)
            )

            if (
                resolved_output == resolved_authoritative_directory
                or resolved_output.is_relative_to(
                    resolved_authoritative_directory,
                )
            ):
                return RepositoryLayoutValidationResult(
                    successful=False,
                    diagnostic=(
                        "build output directory must not overlap "
                        "authoritative repository content"
                    ),
                )

        for authoritative_file in layout.authoritative_files:
            if resolved_output == authoritative_file.resolve(strict=False):
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
