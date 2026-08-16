"""Construct artifact identities from successful package validation."""

from __future__ import annotations

from familyos_cli.application.build.artifact_identity import ArtifactIdentity
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.package_validation import (
    PythonPackageStructuralValidationResult,
)


class BuildArtifactIdentitiesUseCase:
    """Create explicit identities for structurally validated candidates."""

    def execute(
        self,
        validation: PythonPackageStructuralValidationResult,
        *,
        build_id: BuildId,
        source_revision: str | None,
    ) -> tuple[ArtifactIdentity, ...]:
        """Return deterministic identity metadata for valid candidates."""

        identities: list[ArtifactIdentity] = []

        for result in validation.candidate_results:
            if not result.successful or result.package_identity is None:
                continue

            candidate = result.candidate
            identities.append(
                ArtifactIdentity(
                    logical_name=result.package_identity.name,
                    artifact_type=candidate.artifact_class,
                    version=result.package_identity.version,
                    source_revision=source_revision,
                    build_id=build_id,
                    path=candidate.path,
                    size=candidate.path.stat().st_size,
                )
            )

        return tuple(
            sorted(
                identities,
                key=lambda identity: (
                    identity.artifact_type.value,
                    identity.path.name,
                ),
            )
        )
