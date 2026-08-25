"""Map established validation results to Build Validation checks."""

from __future__ import annotations

from familyos_cli.application.build.artifact_discovery import (
    CanonicalPackageBuildResult,
)
from familyos_cli.application.build.build_evidence import BuildEvidence
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_input_validation import (
    BuildInputValidationResult,
)
from familyos_cli.application.build.build_validation import (
    BuildValidationCheckResult,
    BuildValidationDomain,
    BuildValidationRequirement,
    BuildValidationStatus,
)
from familyos_cli.application.build.effective_configuration_validation import (
    EffectiveConfigurationValidationResult,
)
from familyos_cli.application.build.environment_validation import (
    EnvironmentValidationResult,
)
from familyos_cli.application.build.toolchain_validation import (
    ToolchainValidationResult,
)
from familyos_cli.application.validation import (
    GateResult,
    ValidationStatus,
)

_DEPENDENCY_GATE_IDS = frozenset(
    {
        "dependency-freshness",
        "dependency-consistency",
    }
)


class BuildValidationCheckFactory:
    """Create normalized Build Validation checks from established results."""

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

    def from_source_validation(
        self,
        *,
        revision_identified: bool,
        working_tree_clean: bool,
        revision_diagnostic: str | None = None,
        working_tree_diagnostic: str | None = None,
    ) -> tuple[BuildValidationCheckResult, ...]:
        """Map explicit source-state observations to validation checks."""

        return (
            BuildValidationCheckResult(
                check_id="source-revision",
                domain=BuildValidationDomain.SOURCE,
                requirement=BuildValidationRequirement.REQUIRED,
                status=(
                    BuildValidationStatus.PASSED
                    if revision_identified
                    else BuildValidationStatus.FAILED
                ),
                diagnostic=(
                    None
                    if revision_identified
                    else revision_diagnostic
                ),
            ),
            BuildValidationCheckResult(
                check_id="source-working-tree",
                domain=BuildValidationDomain.SOURCE,
                requirement=BuildValidationRequirement.REQUIRED,
                status=(
                    BuildValidationStatus.PASSED
                    if working_tree_clean
                    else BuildValidationStatus.FAILED
                ),
                diagnostic=(
                    None
                    if working_tree_clean
                    else working_tree_diagnostic
                ),
            ),
        )

    def from_input_validation_result(
        self,
        result: BuildInputValidationResult,
    ) -> tuple[BuildValidationCheckResult, ...]:
        """Project established canonical build-input validation authority."""

        return tuple(
            BuildValidationCheckResult(
                check_id=check.input_name,
                domain=BuildValidationDomain.INPUT,
                requirement=BuildValidationRequirement.REQUIRED,
                status=(
                    BuildValidationStatus.PASSED
                    if check.successful
                    else BuildValidationStatus.FAILED
                ),
                diagnostic=(
                    None
                    if check.successful
                    else check.diagnostic
                ),
            )
            for check in result.checks
        )

    def from_configuration_validation_result(
        self,
        result: EffectiveConfigurationValidationResult,
    ) -> tuple[BuildValidationCheckResult, ...]:
        """Project established effective-configuration authority."""

        return (
            BuildValidationCheckResult(
                check_id="effective-configuration",
                domain=BuildValidationDomain.CONFIGURATION,
                requirement=BuildValidationRequirement.REQUIRED,
                status=(
                    BuildValidationStatus.PASSED
                    if result.successful
                    else BuildValidationStatus.FAILED
                ),
                diagnostic=(
                    None
                    if result.successful
                    else result.diagnostic
                ),
            ),
        )

    def from_toolchain_validation_result(
        self,
        result: ToolchainValidationResult,
    ) -> tuple[BuildValidationCheckResult, ...]:
        """Project established canonical toolchain authority."""

        return (
            BuildValidationCheckResult(
                check_id="canonical-toolchain",
                domain=BuildValidationDomain.TOOLCHAIN,
                requirement=BuildValidationRequirement.REQUIRED,
                status=(
                    BuildValidationStatus.PASSED
                    if result.successful
                    else BuildValidationStatus.FAILED
                ),
                diagnostic=(
                    None
                    if result.successful
                    else result.diagnostic
                ),
            ),
        )

    def from_environment_validation_result(
        self,
        result: EnvironmentValidationResult,
    ) -> tuple[BuildValidationCheckResult, ...]:
        """Project established canonical environment authority."""

        return (
            BuildValidationCheckResult(
                check_id="canonical-environment",
                domain=BuildValidationDomain.ENVIRONMENT,
                requirement=BuildValidationRequirement.REQUIRED,
                status=(
                    BuildValidationStatus.PASSED
                    if result.successful
                    else BuildValidationStatus.FAILED
                ),
                diagnostic=(
                    None
                    if result.successful
                    else result.diagnostic
                ),
            ),
        )

    def from_testing_validation(
        self,
        gate: GateResult,
    ) -> tuple[BuildValidationCheckResult, ...]:
        """Project canonical pytest gate authority into Build Validation."""

        if gate.gate_id != "pytest":
            raise ValueError(
                "release-readiness testing requires canonical pytest gate"
            )

        successful = gate.status is ValidationStatus.PASSED

        if successful and gate.testing_evidence is None:
            raise ValueError(
                "release-readiness testing requires canonical "
                "Testing Evidence"
            )

        return (
            BuildValidationCheckResult(
                check_id="release-readiness-testing",
                domain=BuildValidationDomain.TESTING,
                requirement=BuildValidationRequirement.REQUIRED,
                status=(
                    BuildValidationStatus.PASSED
                    if successful
                    else BuildValidationStatus.FAILED
                ),
                diagnostic=(
                    None
                    if successful
                    else gate.diagnostic
                ),
            ),
        )

    def from_dependency_validation(
        self,
        gates: tuple[GateResult, ...],
    ) -> tuple[BuildValidationCheckResult, ...]:
        """Map existing canonical dependency gates without re-executing them."""

        checks: list[BuildValidationCheckResult] = []

        for gate in gates:
            if gate.gate_id not in _DEPENDENCY_GATE_IDS:
                raise ValueError(
                    "Unsupported dependency validation gate: "
                    f"{gate.gate_id}"
                )

            checks.append(
                BuildValidationCheckResult(
                    check_id=gate.gate_id,
                    domain=BuildValidationDomain.DEPENDENCY,
                    requirement=BuildValidationRequirement.REQUIRED,
                    status=self._from_gate_status(gate.status),
                    diagnostic=gate.diagnostic,
                )
            )

        return tuple(checks)

    def from_toolchain_validation(
        self,
        *,
        python_compatible: bool,
        build_available: bool,
        python_diagnostic: str | None = None,
        build_diagnostic: str | None = None,
    ) -> tuple[BuildValidationCheckResult, ...]:
        """Map explicit canonical build-toolchain observations to checks."""

        return (
            BuildValidationCheckResult(
                check_id="python-toolchain",
                domain=BuildValidationDomain.TOOLCHAIN,
                requirement=BuildValidationRequirement.REQUIRED,
                status=(
                    BuildValidationStatus.PASSED
                    if python_compatible
                    else BuildValidationStatus.FAILED
                ),
                diagnostic=None if python_compatible else python_diagnostic,
            ),
            BuildValidationCheckResult(
                check_id="python-build-tool",
                domain=BuildValidationDomain.TOOLCHAIN,
                requirement=BuildValidationRequirement.REQUIRED,
                status=(
                    BuildValidationStatus.PASSED
                    if build_available
                    else BuildValidationStatus.FAILED
                ),
                diagnostic=None if build_available else build_diagnostic,
            ),
        )

    def from_environment_validation(
        self,
        *,
        project_root_available: bool,
        output_environment_available: bool,
        project_diagnostic: str | None = None,
        output_diagnostic: str | None = None,
    ) -> tuple[BuildValidationCheckResult, ...]:
        """Map explicit canonical build-environment observations to checks."""

        return (
            BuildValidationCheckResult(
                check_id="project-environment",
                domain=BuildValidationDomain.ENVIRONMENT,
                requirement=BuildValidationRequirement.REQUIRED,
                status=(
                    BuildValidationStatus.PASSED
                    if project_root_available
                    else BuildValidationStatus.FAILED
                ),
                diagnostic=(
                    None
                    if project_root_available
                    else project_diagnostic
                ),
            ),
            BuildValidationCheckResult(
                check_id="output-environment",
                domain=BuildValidationDomain.ENVIRONMENT,
                requirement=BuildValidationRequirement.REQUIRED,
                status=(
                    BuildValidationStatus.PASSED
                    if output_environment_available
                    else BuildValidationStatus.FAILED
                ),
                diagnostic=(
                    None
                    if output_environment_available
                    else output_diagnostic
                ),
            ),
        )

    def from_input_validation(
        self,
        *,
        output_dir_valid: bool,
        functional_validation_valid: bool,
        output_dir_diagnostic: str | None = None,
        functional_validation_diagnostic: str | None = None,
    ) -> tuple[BuildValidationCheckResult, ...]:
        """Map explicit canonical build-request input observations to checks."""

        return (
            BuildValidationCheckResult(
                check_id="output-dir-input",
                domain=BuildValidationDomain.INPUT,
                requirement=BuildValidationRequirement.REQUIRED,
                status=(
                    BuildValidationStatus.PASSED
                    if output_dir_valid
                    else BuildValidationStatus.FAILED
                ),
                diagnostic=(
                    None
                    if output_dir_valid
                    else output_dir_diagnostic
                ),
            ),
            BuildValidationCheckResult(
                check_id="functional-validation-input",
                domain=BuildValidationDomain.INPUT,
                requirement=BuildValidationRequirement.REQUIRED,
                status=(
                    BuildValidationStatus.PASSED
                    if functional_validation_valid
                    else BuildValidationStatus.FAILED
                ),
                diagnostic=(
                    None
                    if functional_validation_valid
                    else functional_validation_diagnostic
                ),
            ),
        )

    def from_configuration_validation(
        self,
        *,
        package_configuration_valid: bool,
        dependency_configuration_valid: bool,
        package_diagnostic: str | None = None,
        dependency_diagnostic: str | None = None,
    ) -> tuple[BuildValidationCheckResult, ...]:
        """Map explicit canonical build-configuration observations to checks."""

        return (
            BuildValidationCheckResult(
                check_id="package-configuration",
                domain=BuildValidationDomain.CONFIGURATION,
                requirement=BuildValidationRequirement.REQUIRED,
                status=(
                    BuildValidationStatus.PASSED
                    if package_configuration_valid
                    else BuildValidationStatus.FAILED
                ),
                diagnostic=(
                    None
                    if package_configuration_valid
                    else package_diagnostic
                ),
            ),
            BuildValidationCheckResult(
                check_id="dependency-configuration",
                domain=BuildValidationDomain.CONFIGURATION,
                requirement=BuildValidationRequirement.REQUIRED,
                status=(
                    BuildValidationStatus.PASSED
                    if dependency_configuration_valid
                    else BuildValidationStatus.FAILED
                ),
                diagnostic=(
                    None
                    if dependency_configuration_valid
                    else dependency_diagnostic
                ),
            ),
        )

    def from_evidence_validation(
        self,
        evidence: BuildEvidence | None,
        *,
        build_id: BuildId,
    ) -> tuple[BuildValidationCheckResult, ...]:
        """Map canonical Build Evidence availability to a required check."""

        if evidence is None:
            return (
                BuildValidationCheckResult(
                    check_id="build-evidence",
                    domain=BuildValidationDomain.EVIDENCE,
                    requirement=BuildValidationRequirement.REQUIRED,
                    status=BuildValidationStatus.FAILED,
                    diagnostic="Build Evidence is unavailable",
                ),
            )

        if evidence.build_id != build_id:
            return (
                BuildValidationCheckResult(
                    check_id="build-evidence",
                    domain=BuildValidationDomain.EVIDENCE,
                    requirement=BuildValidationRequirement.REQUIRED,
                    status=BuildValidationStatus.FAILED,
                    diagnostic=(
                        "Build Evidence build ID does not match "
                        "validation build"
                    ),
                ),
            )

        return (
            BuildValidationCheckResult(
                check_id="build-evidence",
                domain=BuildValidationDomain.EVIDENCE,
                requirement=BuildValidationRequirement.REQUIRED,
                status=BuildValidationStatus.PASSED,
                diagnostic=None,
            ),
        )

    @staticmethod
    def _from_gate_status(
        status: ValidationStatus,
    ) -> BuildValidationStatus:
        """Translate canonical gate status into Build Validation semantics."""

        if status is ValidationStatus.PASSED:
            return BuildValidationStatus.PASSED

        return BuildValidationStatus.FAILED
