"""Finalize canonical Build Result from established authorities."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.build.artifact_discovery import (
    CanonicalPackageBuildResult,
)
from familyos_cli.application.build.build_validation import (
    BuildValidationResult,
)
from familyos_cli.application.build.canonical_build_result import (
    CanonicalBuildResult,
)


class CanonicalBuildResultFinalizer:
    """Assemble the final canonical Build Result without recalculation."""

    def finalize(
        self,
        *,
        package_result: CanonicalPackageBuildResult,
        validation_result: BuildValidationResult | None,
        evidence_reference: Path | None,
    ) -> CanonicalBuildResult:
        """Return one final result from already established authorities."""

        return CanonicalBuildResult(
            package_result=package_result,
            validation_result=validation_result,
            evidence_reference=evidence_reference,
        )
