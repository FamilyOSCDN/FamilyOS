"""Application policy for discovering current Python package artifacts."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.build.artifact_discovery import (
    ArtifactClass,
    ArtifactDiscoveryResult,
    ArtifactDiscoveryStatus,
    DiscoveredArtifact,
    ExpectedArtifactDefinition,
)

PACKAGE_ARTIFACT_DEFINITIONS = (
    ExpectedArtifactDefinition(
        artifact_class=ArtifactClass.PYTHON_WHEEL,
        filename_suffix=".whl",
        required_count=1,
    ),
    ExpectedArtifactDefinition(
        artifact_class=ArtifactClass.SOURCE_DISTRIBUTION,
        filename_suffix=".tar.gz",
        required_count=1,
    ),
)


class DiscoverPackageArtifactsUseCase:
    """Compare raw current outputs with the canonical package contract."""

    def execute(
        self,
        *,
        output_dir: Path,
        current_outputs: tuple[Path, ...],
    ) -> ArtifactDiscoveryResult:
        """Classify the exact expected wheel and source distribution."""

        remaining = list(sorted(set(current_outputs), key=lambda path: path.name))
        candidates: list[DiscoveredArtifact] = []
        missing: list[ArtifactClass] = []
        unexpected: list[Path] = []

        for definition in PACKAGE_ARTIFACT_DEFINITIONS:
            matches = [
                path
                for path in remaining
                if path.parent == output_dir and definition.accepts(path)
            ]
            accepted = matches[: definition.required_count]
            candidates.extend(
                DiscoveredArtifact(
                    path=path,
                    artifact_class=definition.artifact_class,
                )
                for path in accepted
            )
            if len(matches) < definition.required_count:
                missing.append(definition.artifact_class)
            unexpected.extend(matches[definition.required_count :])
            remaining = [path for path in remaining if path not in matches]

        unexpected.extend(remaining)
        ordered_candidates = tuple(
            sorted(candidates, key=lambda artifact: artifact.path.name)
        )
        ordered_unexpected = tuple(
            sorted(set(unexpected), key=lambda path: path.name)
        )
        if missing or ordered_unexpected:
            diagnostic_parts = [
                *(f"missing {artifact_class.value}" for artifact_class in missing),
                *(
                    f"unexpected {path.name}"
                    for path in ordered_unexpected
                ),
            ]
            return ArtifactDiscoveryResult(
                status=ArtifactDiscoveryStatus.FAILED,
                output_dir=output_dir,
                candidates=ordered_candidates,
                missing_expectations=tuple(missing),
                unexpected_outputs=ordered_unexpected,
                diagnostic="Artifact discovery failed: "
                + "; ".join(diagnostic_parts),
            )

        return ArtifactDiscoveryResult(
            status=ArtifactDiscoveryStatus.SUCCEEDED,
            output_dir=output_dir,
            candidates=ordered_candidates,
        )
