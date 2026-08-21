"""Canonical Build Validation decision orchestration."""

from __future__ import annotations

from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_validation import (
    BuildValidationCheckResult,
    BuildValidationProfile,
    BuildValidationRequirement,
    BuildValidationResult,
    BuildValidationStatus,
)


class BuildValidationOrchestrator:
    """Produce an explicit validation decision from classified checks."""

    def execute(
        self,
        *,
        build_id: BuildId,
        profile: BuildValidationProfile,
        checks: tuple[BuildValidationCheckResult, ...],
    ) -> BuildValidationResult:
        """Aggregate classified checks without executing validation itself."""

        blocking_required = any(
            check.requirement is BuildValidationRequirement.REQUIRED
            and check.status in (
                BuildValidationStatus.FAILED,
                BuildValidationStatus.SKIPPED,
            )
            for check in checks
        )

        status = (
            BuildValidationStatus.FAILED
            if blocking_required
            else BuildValidationStatus.PASSED
        )

        return BuildValidationResult(
            build_id=build_id,
            profile=profile,
            checks=checks,
            status=status,
        )
