"""Canonical FamilyOS package-build command."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from familyos_cli.application.build import (
    BuildEvidenceFactory,
    CanonicalPackageBuildResult,
)
from familyos_cli.application.build.build_context import BuildProfile
from familyos_cli.application.build.build_profile_registry import (
    get_build_profile_definition,
)
from familyos_cli.application.build.build_validation import (
    BuildValidationProfile,
    BuildValidationRequirement,
)
from familyos_cli.application.build.build_validation_checks import (
    BuildValidationCheckFactory,
)
from familyos_cli.application.build.build_validation_orchestrator import (
    BuildValidationOrchestrator,
)
from familyos_cli.application.build.canonical_build_result import (
    CanonicalBuildResult,
)
from familyos_cli.application.build.canonical_build_result_finalizer import (
    CanonicalBuildResultFinalizer,
)
from familyos_cli.application.build.effective_build_configuration_view import (
    EffectiveBuildConfigurationView,
)
from familyos_cli.application.build.source_state_validator import (
    SourceStateValidator,
)
from familyos_cli.application.testing import (
    EvaluateTestingEvidenceFreshnessUseCase,
    TestingEvidenceFreshness,
)
from familyos_cli.application.validation import GateResult
from familyos_cli.interfaces.cli.context import CommandContext
from familyos_cli.interfaces.cli.rendering.build_evidence_json import (
    BuildEvidenceJsonRenderer,
)
from familyos_cli.interfaces.cli.rendering.ci_validation_json_loader import (
    CiValidationJsonLoader,
)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1
DEFAULT_OUTPUT_DIR = Path("dist")

_VALIDATION_PROFILE_BY_BUILD_PROFILE = {
    BuildProfile.DEVELOPMENT: BuildValidationProfile.DEVELOPMENT,
    BuildProfile.VALIDATION: BuildValidationProfile.VALIDATION,
    BuildProfile.CI: BuildValidationProfile.CI,
    BuildProfile.RELEASE_CANDIDATE: (
        BuildValidationProfile.RELEASE_CANDIDATE
    ),
}


def _testing_evidence_freshness_authority(
    *,
    project_root: Path,
) -> EvaluateTestingEvidenceFreshnessUseCase:
    """Return canonical Testing Evidence freshness authority."""
    return CommandContext(
        project_root=project_root,
    ).testing_evidence_freshness


def run_package_build(
    output_dir: Path,
    *,
    functional_validation: bool,
    profile: BuildProfile = BuildProfile.DEVELOPMENT,
    evidence_output: Path | None = None,
    testing_validation_gate: GateResult | None = None,
    plugin_compliance_validation_gate: GateResult | None = None,
) -> int:
    """Execute and render the canonical package build."""

    result = CommandContext(
        project_root=Path.cwd(),
    ).run_package_build.execute(
        output_dir,
        validate_functionally=functional_validation,
        profile=profile,
        evidence_output=evidence_output,
    )

    _render_result(result)

    if not result.successful:
        canonical_result = CanonicalBuildResultFinalizer().finalize(
            package_result=result,
            validation_result=None,
            evidence_reference=None,
        )
        _render_failure_classification(canonical_result)
        return EXIT_FAILURE

    if evidence_output is not None:
        if (
            result.build_context is None
            or result.build_context.evidence_output is None
        ):
            raise RuntimeError(
                "successful evidence-producing build lacks an evidence output"
            )

        resolved_evidence_output = result.build_context.evidence_output
        functional_requirement = (
            BuildValidationRequirement.REQUIRED
            if functional_validation
            else BuildValidationRequirement.OPTIONAL
        )

        check_factory = BuildValidationCheckFactory()

        checks = check_factory.from_package_build(
            result,
            functional_requirement=functional_requirement,
        )

        if profile is BuildProfile.RELEASE_CANDIDATE:
            source_validation = SourceStateValidator().validate(
                result.source_state
            )

            source_checks = check_factory.from_source_validation(
                revision_identified=(
                    source_validation.revision_identified
                ),
                working_tree_clean=(
                    source_validation.working_tree_clean
                ),
                revision_diagnostic=(
                    source_validation.revision_diagnostic
                ),
                working_tree_diagnostic=(
                    source_validation.working_tree_diagnostic
                ),
            )

            input_validation = result.input_validation
            configuration_validation = (
                result.effective_configuration_validation
            )
            toolchain_validation = result.toolchain_validation
            environment_validation = result.environment_validation

            if input_validation is None:
                raise RuntimeError(
                    "release-candidate build lacks canonical "
                    "input validation authority"
                )

            if configuration_validation is None:
                raise RuntimeError(
                    "release-candidate build lacks canonical "
                    "effective-configuration validation authority"
                )

            if toolchain_validation is None:
                raise RuntimeError(
                    "release-candidate build lacks canonical "
                    "toolchain validation authority"
                )

            if environment_validation is None:
                raise RuntimeError(
                    "release-candidate build lacks canonical "
                    "environment validation authority"
                )

            input_checks = (
                check_factory.from_input_validation_result(
                    input_validation
                )
            )
            configuration_checks = (
                check_factory.from_configuration_validation_result(
                    configuration_validation
                )
            )
            toolchain_checks = (
                check_factory.from_toolchain_validation_result(
                    toolchain_validation
                )
            )
            environment_checks = (
                check_factory.from_environment_validation_result(
                    environment_validation
                )
            )

            if testing_validation_gate is None:
                raise RuntimeError(
                    "release-candidate build lacks canonical "
                    "pytest validation authority"
                )

            testing_checks = check_factory.from_testing_validation(
                testing_validation_gate
            )

            if plugin_compliance_validation_gate is None:
                raise RuntimeError(
                    "release-candidate build lacks canonical "
                    "official plugin compliance authority"
                )

            compliance_checks = (
                check_factory.from_plugin_compliance_validation(
                    plugin_compliance_validation_gate
                )
            )

            checks = (
                checks
                + source_checks
                + input_checks
                + configuration_checks
                + toolchain_checks
                + environment_checks
                + testing_checks
                + compliance_checks
            )

        validation_result = BuildValidationOrchestrator().execute(
            build_id=result.build_id,
            profile=_VALIDATION_PROFILE_BY_BUILD_PROFILE[profile],
            checks=checks,
        )

        evidence = BuildEvidenceFactory().from_package_build(
            result,
            validation_result,
        )

        rendered = BuildEvidenceJsonRenderer().render(evidence)

        resolved_evidence_output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )
        resolved_evidence_output.write_text(
            rendered,
            encoding="utf-8",
        )

        CanonicalBuildResultFinalizer().finalize(
            package_result=result,
            validation_result=validation_result,
            evidence_reference=resolved_evidence_output,
        )
    else:
        CanonicalBuildResultFinalizer().finalize(
            package_result=result,
            validation_result=None,
            evidence_reference=None,
        )

    return EXIT_SUCCESS


def _render_result(result: CanonicalPackageBuildResult) -> None:
    """Render process-level build output without trust claims."""

    typer.echo(f"Canonical Package Build: {result.status.value.upper()}")
    typer.echo(f"Build ID: {result.build_id}")

    if result.build_context is not None:
        context = result.build_context
        environment = context.environment_state
        configuration = EffectiveBuildConfigurationView.from_context(
            context,
            get_build_profile_definition(context.profile),
        )

        typer.echo(f"Build Profile: {configuration.profile.value}")
        typer.echo(f"Build Target: {configuration.target.value}")
        typer.echo(
            "Profile Supports Target: "
            f"{configuration.target_supported}"
        )
        typer.echo(f"Runtime Version: {context.runtime_version}")
        typer.echo(f"Operating System: {environment.operating_system}")
        typer.echo(
            "Operating System Release: "
            f"{environment.operating_system_release}"
        )
        typer.echo(
            "Machine Architecture: "
            f"{environment.machine_architecture}"
        )
        typer.echo(
            "Virtual Environment Active: "
            f"{environment.virtual_environment_active}"
        )
        typer.echo(
            f"Temporary Directory: {environment.temporary_directory}"
        )
        typer.echo(
            f"Filesystem Encoding: {environment.filesystem_encoding}"
        )

        for component in context.toolchain_state.critical_versions:
            typer.echo(
                f"Toolchain {component.distribution}: {component.version}"
            )

        typer.echo(f"Output Directory: {configuration.output_dir}")
        typer.echo(
            f"Evidence Required: {configuration.evidence_required}"
        )
        typer.echo(
            f"Evidence Requested: {configuration.evidence_requested}"
        )
        typer.echo(
            "Evidence Output: "
            f"{configuration.evidence_output or 'not requested'}"
        )
        typer.echo(
            "Functional Validation Requested: "
            f"{configuration.functional_validation}"
        )

    if result.execution_observations:
        typer.echo("Execution Stages:")

        for observation in result.execution_observations:
            line = (
                f"- {observation.stage.value}: "
                f"{observation.status.value.upper()} "
                f"({observation.duration_seconds:.6f}s)"
            )

            if observation.diagnostic:
                line += f" — {observation.diagnostic}"

            typer.echo(line)

    for artifact in result.candidates:
        typer.echo(
            f"- {artifact.artifact_class.value}: {artifact.path}"
        )

    if result.validation:
        typer.echo(
            "Python Package Structural Validation: "
            f"{result.validation.status.value.upper()}"
        )

    if result.functional_validation:
        typer.echo(
            "Python Wheel Functional Validation: "
            f"{result.functional_validation.status.value.upper()}"
        )

    if result.diagnostic:
        typer.echo(
            result.diagnostic,
            err=True,
        )


def _render_failure_classification(
    result: CanonicalBuildResult,
) -> None:
    """Render canonical failure classification and corrective direction."""

    if result.failure_category is not None:
        typer.echo(
            f"Failure Category: {result.failure_category.value}",
            err=True,
        )

    if result.corrective_information is not None:
        typer.echo(
            f"Corrective Action: {result.corrective_information}",
            err=True,
        )


def build(
    output_dir: Annotated[
        Path,
        typer.Option(
            "--output-dir",
            help="Directory for package-build outputs.",
        ),
    ] = DEFAULT_OUTPUT_DIR,
    functional_validation: Annotated[
        bool,
        typer.Option(
            "--functional-validation",
            help=(
                "Install and smoke-test the wheel in a clean temporary "
                "environment after static validation."
            ),
        ),
    ] = False,
    profile: Annotated[
        BuildProfile,
        typer.Option(
            "--profile",
            help="Explicit canonical build-purpose profile.",
        ),
    ] = BuildProfile.DEVELOPMENT,
    evidence_output: Annotated[
        Path | None,
        typer.Option(
            "--evidence-output",
            help=(
                "Write canonical Build Evidence as JSON after a "
                "successful build."
            ),
        ),
    ] = None,
    validation_evidence: Annotated[
        Path | None,
        typer.Option(
            "--validation-evidence",
            help=(
                "Canonical CI validation evidence providing "
                "release-candidate testing authority."
            ),
        ),
    ] = None,

) -> None:
    """Build the FamilyOS wheel and source distribution without publishing."""

    testing_validation_gate = None
    plugin_compliance_validation_gate = None

    if validation_evidence is not None:
        validation_result = CiValidationJsonLoader().load(
            validation_evidence.read_text(encoding="utf-8")
        )

        testing_validation_gate = next(
            (
                gate
                for gate in validation_result.gates
                if gate.gate_id == "pytest"
            ),
            None,
        )

        plugin_compliance_validation_gate = next(
            (
                gate
                for gate in validation_result.gates
                if gate.gate_id == "builtin-plugin-compliance"
            ),
            None,
        )

        if (
            profile is BuildProfile.RELEASE_CANDIDATE
            and testing_validation_gate is None
        ):
            typer.echo(
                "release-candidate build lacks canonical "
                "pytest validation authority"
            )
            raise typer.Exit(code=EXIT_FAILURE)

        if (
            profile is BuildProfile.RELEASE_CANDIDATE
            and plugin_compliance_validation_gate is None
        ):
            typer.echo(
                "release-candidate build lacks canonical "
                "official plugin compliance authority"
            )
            raise typer.Exit(code=EXIT_FAILURE)

    if (
        profile is BuildProfile.RELEASE_CANDIDATE
        and testing_validation_gate is not None
    ):
        testing_evidence = testing_validation_gate.testing_evidence

        if testing_evidence is None:
            typer.echo(
                "release-candidate build lacks canonical "
                "pytest validation authority"
            )
            raise typer.Exit(code=EXIT_FAILURE)

        testing_evidence_freshness = (
            _testing_evidence_freshness_authority(
                project_root=Path.cwd(),
            ).evaluate(
                project_root=Path.cwd(),
                evidence=testing_evidence,
            )
        )

        if (
            testing_evidence_freshness
            is TestingEvidenceFreshness.STALE
        ):
            typer.echo(
                "release-candidate testing evidence is stale"
            )
            raise typer.Exit(code=EXIT_FAILURE)

        if (
            testing_evidence_freshness
            is not TestingEvidenceFreshness.FRESH
        ):
            typer.echo(
                "release-candidate testing evidence freshness "
                "cannot be established"
            )
            raise typer.Exit(code=EXIT_FAILURE)

    exit_code = run_package_build(
        output_dir,
        functional_validation=functional_validation,
        profile=profile,
        evidence_output=evidence_output,
        testing_validation_gate=testing_validation_gate,
        plugin_compliance_validation_gate=(
            plugin_compliance_validation_gate
        ),
    )

    if exit_code != EXIT_SUCCESS:
        raise typer.Exit(code=exit_code)
