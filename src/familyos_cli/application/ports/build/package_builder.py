"""Port for standards-compatible Python package construction."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from familyos_cli.application.build.package_build import PackageBuildResult


class PackageBuilderPort(ABC):
    """Build a Python package without exposing subprocess details."""

    @abstractmethod
    def build(
        self,
        *,
        project_root: Path,
        output_dir: Path,
    ) -> PackageBuildResult:
        """Execute packaging and return process-level outputs."""

        raise NotImplementedError
