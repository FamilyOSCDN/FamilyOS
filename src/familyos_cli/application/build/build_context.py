"""Immutable effective context for one canonical build execution."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path

from familyos_cli.application.build.dependency_state import DependencyState
from familyos_cli.application.build.source_state import SourceState
from familyos_cli.application.build.toolchain_state import ToolchainState


class BuildProfile(StrEnum):
    """Explicit execution profiles for canonical Build Framework behavior."""

    DEVELOPMENT = "development"
    VALIDATION = "validation"
    CI = "ci"
    RELEASE_CANDIDATE = "release-candidate"


class BuildTarget(StrEnum):
    """Explicit build targets currently supported by the Build Framework."""

    FAMILYOS_CLI_PACKAGE = "familyos-cli-package"


@dataclass(frozen=True, slots=True)
class BuildEffectiveConfiguration:
    """Non-sensitive effective configuration resolved for one build."""

    functional_validation: bool


@dataclass(frozen=True, slots=True)
class BuildContext:
    """Stable effective context resolved before significant build execution."""

    source_state: SourceState
    dependency_state: DependencyState
    toolchain_state: ToolchainState
    profile: BuildProfile
    target: BuildTarget
    runtime_version: str
    effective_configuration: BuildEffectiveConfiguration
    output_dir: Path
