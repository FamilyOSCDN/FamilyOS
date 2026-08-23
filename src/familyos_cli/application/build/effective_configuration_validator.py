"""Validate one resolved effective build configuration."""

from __future__ import annotations

from familyos_cli.application.build.build_context import BuildContext
from familyos_cli.application.build.build_profile_definition import (
    BuildProfileDefinition,
)
from familyos_cli.application.build.effective_configuration_validation import (
    EffectiveConfigurationValidationFinding,
    EffectiveConfigurationValidationResult,
    EffectiveConfigurationValidationStatus,
)
from familyos_cli.application.build.repository_layout_validation import (
    RepositoryLayoutValidationResult,
)


class EffectiveConfigurationValidator:
    """Validate consistency after canonical configuration resolution."""

    def validate(
        self,
        *,
        context: BuildContext,
        profile_definition: BuildProfileDefinition,
        output_layout_validation: RepositoryLayoutValidationResult,
        evidence_layout_validation: RepositoryLayoutValidationResult,
    ) -> EffectiveConfigurationValidationResult:
        """Validate a resolved context without resolving or observing it again."""

        findings: list[EffectiveConfigurationValidationFinding] = []

        if context.profile is not profile_definition.profile:
            findings.append(
                EffectiveConfigurationValidationFinding(
                    component="profile",
                    diagnostic=(
                        "resolved build profile does not match canonical "
                        "profile definition: "
                        f"context={context.profile.value}, "
                        f"definition={profile_definition.profile.value}"
                    ),
                )
            )

        if context.target not in profile_definition.supported_targets:
            findings.append(
                EffectiveConfigurationValidationFinding(
                    component="target",
                    diagnostic=(
                        "resolved build target is unsupported by profile: "
                        f"{context.profile.value}/{context.target.value}"
                    ),
                )
            )

        if not isinstance(
            context.effective_configuration.functional_validation,
            bool,
        ):
            findings.append(
                EffectiveConfigurationValidationFinding(
                    component="functional-validation",
                    diagnostic=(
                        "resolved functional-validation setting must be a boolean"
                    ),
                )
            )

        if not output_layout_validation.successful:
            findings.append(
                EffectiveConfigurationValidationFinding(
                    component="output-directory",
                    diagnostic=(
                        output_layout_validation.diagnostic
                        or "resolved output directory failed repository-layout validation"
                    ),
                )
            )

        if (
            profile_definition.evidence_required
            and context.evidence_output is None
        ):
            findings.append(
                EffectiveConfigurationValidationFinding(
                    component="evidence",
                    diagnostic=(
                        "build profile requires an evidence output: "
                        f"{context.profile.value}"
                    ),
                )
            )

        if not evidence_layout_validation.successful:
            findings.append(
                EffectiveConfigurationValidationFinding(
                    component="evidence-output",
                    diagnostic=(
                        evidence_layout_validation.diagnostic
                        or "resolved evidence output failed repository-layout validation"
                    ),
                )
            )

        if findings:
            return EffectiveConfigurationValidationResult(
                status=EffectiveConfigurationValidationStatus.FAILED,
                findings=tuple(findings),
            )

        return EffectiveConfigurationValidationResult(
            status=EffectiveConfigurationValidationStatus.SUCCEEDED,
        )
