"""Cleanup canonical build workspaces after unsuccessful execution."""

from __future__ import annotations

import shutil

from familyos_cli.application.build.build_workspace import BuildWorkspace


class BuildWorkspaceCleaner:
    """Remove one canonical Build-ID-scoped workspace."""

    def clean(
        self,
        *,
        workspace: BuildWorkspace,
    ) -> None:
        """Remove the complete canonical workspace if it still exists."""

        shutil.rmtree(
            workspace.root,
            ignore_errors=True,
        )
