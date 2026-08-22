"""Canonical build-profile contract definitions."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.application.build.build_context import (
    BuildProfile,
    BuildTarget,
)


@dataclass(frozen=True, slots=True)
class BuildProfileDefinition:
    """Describe the stable contract for one supported build profile."""

    profile: BuildProfile
    purpose: str
    supported_targets: tuple[BuildTarget, ...]
    validation_scope: tuple[str, ...]
    evidence_required: bool
    environment_requirements: tuple[str, ...]
    artifact_expectations: tuple[str, ...]

    def __post_init__(self) -> None:
        """Reject incomplete canonical profile definitions."""

        if not self.purpose:
            raise ValueError("build profile purpose must not be empty")

        if not self.supported_targets:
            raise ValueError("build profile must support at least one target")

        if not self.validation_scope:
            raise ValueError("build profile must define validation scope")

        if not self.environment_requirements:
            raise ValueError(
                "build profile must define environment requirements"
            )

        if not self.artifact_expectations:
            raise ValueError(
                "build profile must define artifact expectations"
            )
