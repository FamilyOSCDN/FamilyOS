"""Immutable canonical Build Evidence."""

from __future__ import annotations

from dataclasses import dataclass

from familyos_cli.application.build.artifact_integrity import ArtifactIntegrity
from familyos_cli.application.build.artifact_manifest import ArtifactManifest
from familyos_cli.application.build.build_execution_observation import (
    BuildExecutionObservation,
)
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_validation import (
    BuildValidationProfile,
    BuildValidationResult,
)
from familyos_cli.application.build.dependency_state import DependencyState
from familyos_cli.application.build.effective_build_configuration_view import (
    EffectiveBuildConfigurationView,
)
from familyos_cli.application.build.environment_state import EnvironmentState
from familyos_cli.application.build.source_state import SourceState
from familyos_cli.application.build.toolchain_state import ToolchainState


@dataclass(frozen=True, slots=True)
class BuildEvidence:
    """Evidence authorities associated with one canonical build."""

    build_id: BuildId
    source_state: SourceState
    runtime_version: str
    dependency_state: DependencyState
    toolchain_state: ToolchainState
    environment_state: EnvironmentState
    effective_configuration: EffectiveBuildConfigurationView
    execution_observations: tuple[BuildExecutionObservation, ...]
    validation_result: BuildValidationResult
    artifact_manifest: ArtifactManifest
    artifact_integrities: tuple[ArtifactIntegrity, ...]

    def __post_init__(self) -> None:
        """Reject incomplete evidence or evidence from different builds."""

        if self.source_state.revision is None:
            raise ValueError(
                "Build Evidence requires a captured source revision"
            )

        if self.validation_result.build_id != self.build_id:
            raise ValueError(
                "validation result build ID does not match Build Evidence"
            )

        if (
            self.effective_configuration.profile.value
            != self.validation_result.profile.value
        ):
            raise ValueError(
                "effective configuration profile does not match "
                "Build Evidence validation profile"
            )

        if self.artifact_manifest.build_id != self.build_id:
            raise ValueError(
                "artifact manifest build ID does not match Build Evidence"
            )

        manifest_entries = {
            (
                entry.logical_name,
                entry.artifact_type,
                entry.version,
                entry.size,
                entry.path,
                entry.digest_algorithm,
                entry.digest,
            )
            for entry in self.artifact_manifest.entries
        }

        for integrity in self.artifact_integrities:
            identity = integrity.artifact_identity

            if identity.build_id != self.build_id:
                raise ValueError(
                    "artifact integrity build ID does not match Build Evidence"
                )

            integrity_entry = (
                identity.logical_name,
                identity.artifact_type,
                identity.version,
                identity.size,
                identity.path,
                integrity.algorithm,
                integrity.digest,
            )

            if integrity_entry not in manifest_entries:
                raise ValueError(
                    "artifact integrity is not represented by artifact manifest"
                )

    @property
    def source_revision(self) -> str:
        """Return the source revision captured for this build."""

        revision = self.source_state.revision
        if revision is None:
            raise RuntimeError(
                "Build Evidence source revision invariant was violated"
            )

        return revision

    @property
    def source_dirty(self) -> bool | None:
        """Return the captured source dirty state for this build."""

        return self.source_state.dirty

    @property
    def profile(self) -> BuildValidationProfile:
        """Return the validation profile associated with this build."""

        return self.validation_result.profile
