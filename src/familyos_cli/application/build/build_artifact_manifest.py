"""Construct canonical artifact manifests from established build metadata."""

from __future__ import annotations

from familyos_cli.application.build.artifact_integrity import ArtifactIntegrity
from familyos_cli.application.build.artifact_manifest import (
    ArtifactManifest,
    ArtifactManifestEntry,
)
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.package_validation import (
    PythonPackageStructuralValidationResult,
)


class BuildArtifactManifestUseCase:
    """Create a structured manifest without recalculating artifact metadata."""

    def execute(
        self,
        artifact_integrities: tuple[ArtifactIntegrity, ...],
        validation: PythonPackageStructuralValidationResult,
        *,
        build_id: BuildId,
    ) -> ArtifactManifest:
        """Return a complete deterministic manifest for canonical artifacts."""

        validation_by_path = {
            result.candidate.path: result
            for result in validation.candidate_results
        }

        if len(validation_by_path) != len(validation.candidate_results):
            raise ValueError(
                "Artifact manifest is incomplete: structural validation "
                "contains duplicate artifact paths"
            )

        integrity_paths = tuple(
            integrity.artifact_identity.path
            for integrity in artifact_integrities
        )

        if len(set(integrity_paths)) != len(integrity_paths):
            raise ValueError(
                "Artifact manifest is incomplete: integrity metadata "
                "contains duplicate artifact paths"
            )

        if set(integrity_paths) != set(validation_by_path):
            raise ValueError(
                "Artifact manifest is incomplete: integrity and structural "
                "validation artifact sets differ"
            )

        entries: list[ArtifactManifestEntry] = []

        for integrity in artifact_integrities:
            identity = integrity.artifact_identity
            validation_result = validation_by_path[identity.path]

            if identity.build_id != build_id:
                raise ValueError(
                    "Artifact identity Build ID does not match manifest "
                    f"Build ID: {identity.path}"
                )

            if (
                identity.artifact_type
                is not validation_result.candidate.artifact_class
            ):
                raise ValueError(
                    "Artifact identity type does not match structural "
                    f"validation candidate: {identity.path}"
                )

            entries.append(
                ArtifactManifestEntry(
                    logical_name=identity.logical_name,
                    artifact_type=identity.artifact_type,
                    version=identity.version,
                    size=identity.size,
                    path=identity.path,
                    digest_algorithm=integrity.algorithm,
                    digest=integrity.digest,
                    structural_validation_status=validation_result.status,
                )
            )

        return ArtifactManifest(
            build_id=build_id,
            entries=tuple(entries),
        )
