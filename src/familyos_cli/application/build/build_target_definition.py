"""Canonical build-target contract definitions."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.application.build.artifact_type import ArtifactClass
from familyos_cli.application.build.build_context import BuildTarget


@dataclass(frozen=True, slots=True)
class BuildTargetDefinition:
    """Describe the stable contract for one supported build target."""

    target: BuildTarget
    owner: str
    required_inputs: tuple[str, ...]
    expected_artifacts: tuple[ArtifactClass, ...]
    requires_structural_validation: bool

    def __post_init__(self) -> None:
        """Reject incomplete target definitions."""

        if not self.owner:
            raise ValueError("build target owner must not be empty")

        if not self.required_inputs:
            raise ValueError("build target must define required inputs")

        if not self.expected_artifacts:
            raise ValueError("build target must define expected artifacts")
