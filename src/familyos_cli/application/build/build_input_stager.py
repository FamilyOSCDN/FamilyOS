"""Materialize canonical package-build inputs into a build workspace."""

from __future__ import annotations

import shutil
from pathlib import Path

from familyos_cli.application.build.build_staging import StagedBuildInputs
from familyos_cli.application.build.build_workspace import BuildWorkspace


class BuildInputStager:
    """Copy authoritative package-build inputs into isolated staging."""

    _ROOT_FILES = (
        "pyproject.toml",
        "README.md",
        "LICENSE",
        "requirements.txt",
    )

    def stage(
        self,
        *,
        project_root: Path,
        workspace: BuildWorkspace,
    ) -> StagedBuildInputs:
        """Materialize the canonical package-build input set."""

        staged_project_root = workspace.staging_dir / "project"

        if staged_project_root.exists():
            raise FileExistsError(
                f"staged project already exists: {staged_project_root}"
            )

        staged_project_root.mkdir()

        for filename in self._ROOT_FILES:
            shutil.copy2(
                project_root / filename,
                staged_project_root / filename,
            )

        source = project_root / "src" / "familyos_cli"
        destination = staged_project_root / "src" / "familyos_cli"
        destination.parent.mkdir(parents=True)

        shutil.copytree(
            source,
            destination,
            ignore=shutil.ignore_patterns(
                "__pycache__",
                "*.pyc",
                "*.pyo",
            ),
        )

        return StagedBuildInputs(
            project_root=staged_project_root.resolve(),
        )
