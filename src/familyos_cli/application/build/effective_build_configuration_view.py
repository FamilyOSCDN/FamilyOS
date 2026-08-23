"""Inspectable projection of resolved non-sensitive build configuration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from familyos_cli.application.build.build_context import (
    BuildContext,
    BuildProfile,
    BuildTarget,
)
from familyos_cli.application.build.build_profile_definition import (
    BuildProfileDefinition,
)


@dataclass(frozen=True, slots=True)
class EffectiveBuildConfigurationView:
    """Derived inspection view; never a configuration authority."""

    profile: BuildProfile
    target: BuildTarget
    output_dir: Path
    functional_validation: bool
    evidence_output: Path | None
    evidence_required: bool
    target_supported: bool

    @classmethod
    def from_context(
        cls,
        context: BuildContext,
        profile_definition: BuildProfileDefinition,
    ) -> EffectiveBuildConfigurationView:
        """Project one resolved context and its canonical profile policy."""

        if context.profile is not profile_definition.profile:
            raise ValueError(
                "resolved build profile does not match inspection policy: "
                f"context={context.profile.value}, "
                f"definition={profile_definition.profile.value}"
            )

        return cls(
            profile=context.profile,
            target=context.target,
            output_dir=context.output_dir,
            functional_validation=(
                context.effective_configuration.functional_validation
            ),
            evidence_output=context.evidence_output,
            evidence_required=profile_definition.evidence_required,
            target_supported=(
                context.target in profile_definition.supported_targets
            ),
        )

    @property
    def evidence_requested(self) -> bool:
        """Return whether this invocation selected an evidence destination."""

        return self.evidence_output is not None
