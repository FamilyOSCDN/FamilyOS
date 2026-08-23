"""Construct canonical Build Evidence from established build authorities."""

from __future__ import annotations

from familyos_cli.application.build.artifact_discovery import (
    CanonicalPackageBuildResult,
)
from familyos_cli.application.build.build_evidence import BuildEvidence
from familyos_cli.application.build.build_validation import BuildValidationResult


class BuildEvidenceFactory:
    """Assemble Build Evidence without recalculating canonical authorities."""

    def from_package_build(
        self,
        package_result: CanonicalPackageBuildResult,
        validation_result: BuildValidationResult,
    ) -> BuildEvidence:
        """Build evidence from one canonical build and its validation result."""

        if validation_result.build_id != package_result.build_id:
            raise ValueError(
                "validation result build ID does not match package build"
            )

        if package_result.source_state.revision is None:
            raise ValueError(
                "package build does not contain a captured source revision"
            )

        if package_result.build_context is None:
            raise ValueError(
                "package build does not contain Build Context"
            )

        if package_result.artifact_manifest is None:
            raise ValueError(
                "package build does not contain an artifact manifest"
            )

        return BuildEvidence(
            build_id=package_result.build_id,
            source_state=package_result.source_state,
            dependency_state=package_result.build_context.dependency_state,
            validation_result=validation_result,
            artifact_manifest=package_result.artifact_manifest,
            artifact_integrities=package_result.artifact_integrities,
        )
