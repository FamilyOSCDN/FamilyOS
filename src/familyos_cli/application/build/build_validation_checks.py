"""Map established canonical package-build results to Build Validation checks."""

from __future__ import annotations

from familyos_cli.application.build.artifact_discovery import (
    CanonicalPackageBuildResult,
)
from familyos_cli.application.build.build_validation import (
    BuildValidationCheckResult,
    BuildValidationDomain,
    BuildValidationRequirement,
    BuildValidationStatus,
)


class BuildValidationCheckFactory:
    """Create normalized Build Validation checks from canonical build results."""

    def from_package_build(
        self,
        result: CanonicalPackageBuildResult,
        *,
        functional_requirement: BuildValidationRequirement,
    ) -> tuple[BuildValidationCheckResult, ...]:
        """Map performed canonical build stages to explicit validation checks."""

        checks: list[BuildValidationCheckResult] = []

        checks.append(
            BuildValidationCheckResult(
                check_id="build-execution",
                domain=BuildValidationDomain.EXECUTION,
                requirement=BuildValidationRequirement.REQUIRED,
                status=(
                    BuildValidationStatus.PASSED
                    if result.execution.successful
                    else BuildValidationStatus.FAILED
                ),
                diagnostic=result.execution.diagnostic,
            )
        )

        checks.append(
            BuildValidationCheckResult(
                check_id="artifact-discovery",
                domain=BuildValidationDomain.ARTIFACT,
                requirement=BuildValidationRequirement.REQUIRED,
                status=(
                    BuildValidationStatus.PASSED
                    if result.discovery is not None and result.discovery.successful
                    else BuildValidationStatus.FAILED
                ),
                diagnostic=(
                    result.discovery.diagnostic
                    if result.discovery is not None
                    else "artifact discovery was not completed"
                ),
            )
        )

        checks.append(
            BuildValidationCheckResult(
                check_id="artifact-structural-validation",
                domain=BuildValidationDomain.ARTIFACT,
                requirement=BuildValidationRequirement.REQUIRED,
                status=(
                    BuildValidationStatus.PASSED
                    if result.validation is not None and result.validation.successful
                    else BuildValidationStatus.FAILED
                ),
                diagnostic=(
                    result.validation.diagnostic
                    if result.validation is not None
                    else "artifact structural validation was not completed"
                ),
            )
        )

        checks.append(
            BuildValidationCheckResult(
                check_id="artifact-metadata",
                domain=BuildValidationDomain.METADATA,
                requirement=BuildValidationRequirement.REQUIRED,
                status=(
                    BuildValidationStatus.PASSED
                    if result.artifact_manifest is not None
                    else BuildValidationStatus.FAILED
                ),
                diagnostic=(
                    None
                    if result.artifact_manifest is not None
                    else "artifact manifest metadata was not established"
                ),
            )
        )

        integrity_complete = (
            result.artifact_manifest is not None
            and bool(result.artifact_integrities)
            and len(result.artifact_integrities)
            == len(result.artifact_manifest.entries)
        )

        checks.append(
            BuildValidationCheckResult(
                check_id="artifact-integrity",
                domain=BuildValidationDomain.INTEGRITY,
                requirement=BuildValidationRequirement.REQUIRED,
                status=(
                    BuildValidationStatus.PASSED
                    if integrity_complete
                    else BuildValidationStatus.FAILED
                ),
                diagnostic=(
                    None
                    if integrity_complete
                    else "artifact integrity metadata is incomplete"
                ),
            )
        )

        if result.functional_validation is None:
            functional_status = BuildValidationStatus.SKIPPED
            functional_diagnostic = "functional artifact validation was not executed"
        elif result.functional_validation.successful:
            functional_status = BuildValidationStatus.PASSED
            functional_diagnostic = None
        else:
            functional_status = BuildValidationStatus.FAILED
            functional_diagnostic = result.functional_validation.diagnostic

        checks.append(
            BuildValidationCheckResult(
                check_id="functional-artifact-validation",
                domain=BuildValidationDomain.FUNCTIONAL_ARTIFACT,
                requirement=functional_requirement,
                status=functional_status,
                diagnostic=functional_diagnostic,
            )
        )

        return tuple(checks)
