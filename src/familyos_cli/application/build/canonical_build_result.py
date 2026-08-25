"""Final canonical Build Result authority aggregation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from familyos_cli.application.build.artifact_discovery import (
    CanonicalPackageBuildResult,
)
from familyos_cli.application.build.artifact_manifest import ArtifactManifest
from familyos_cli.application.build.build_context import (
    BuildProfile,
    BuildTarget,
)
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_validation import (
    BuildValidationRequirement,
    BuildValidationResult,
    BuildValidationStatus,
)
from familyos_cli.application.build.package_build import PackageBuildStatus


@dataclass(frozen=True, slots=True)
class CanonicalBuildResult:
    """Aggregate final canonical build authorities without recalculation."""

    package_result: CanonicalPackageBuildResult
    validation_result: BuildValidationResult | None
    evidence_reference: Path | None
    @property
    def build_id(self) -> BuildId:
        """Return the canonical Build ID."""

        return self.package_result.build_id

    @property
    def profile(self) -> BuildProfile:
        """Return the canonical build profile."""

        context = self.package_result.build_context
        if context is None:
            raise RuntimeError(
                "Canonical Build Result does not contain Build Context"
            )

        return context.profile

    @property
    def target(self) -> BuildTarget:
        """Return the canonical build target."""

        context = self.package_result.build_context
        if context is None:
            raise RuntimeError(
                "Canonical Build Result does not contain Build Context"
            )

        return context.target
    @property
    def execution_status(self) -> PackageBuildStatus:
        """Return the canonical package execution status."""

        return self.package_result.status

    @property
    def validation_status(self) -> BuildValidationStatus | None:
        """Return the final Build Validation status when available."""

        if self.validation_result is None:
            return None

        return self.validation_result.status
    @property
    def artifact_manifest(self) -> ArtifactManifest | None:
        """Return the canonical artifact manifest when available."""

        return self.package_result.artifact_manifest

    @property
    def diagnostic(self) -> str | None:
        """Return the authoritative final build diagnostic."""

        validation_result = self.validation_result

        if validation_result is not None:
            for check in validation_result.checks:
                if (
                    check.requirement
                    is BuildValidationRequirement.REQUIRED
                    and check.status is BuildValidationStatus.FAILED
                    and check.diagnostic is not None
                ):
                    return check.diagnostic

        return self.package_result.diagnostic
