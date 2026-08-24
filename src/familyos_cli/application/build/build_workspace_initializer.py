"""Initialize canonical filesystem workspace for one build execution."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_workspace import BuildWorkspace


class BuildWorkspaceInitializer:
    """Create the isolated filesystem workspace for one canonical build."""

    def initialize(
        self,
        *,
        build_id: BuildId,
        temporary_directory: Path,
    ) -> BuildWorkspace:
        """Create and return the canonical workspace layout."""

        temporary_root = temporary_directory.resolve()
        workspace_root = temporary_root / "familyos-build" / str(build_id)
        staging_dir = workspace_root / "staging"
        intermediate_dir = workspace_root / "intermediate"

        staging_dir.mkdir(parents=True, exist_ok=False)
        intermediate_dir.mkdir()

        return BuildWorkspace(
            root=workspace_root,
            staging_dir=staging_dir,
            intermediate_dir=intermediate_dir,
        )
