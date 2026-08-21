"""Tests for canonical Build Evidence construction."""

from __future__ import annotations

from pathlib import Path
from uuid import UUID

import pytest

from familyos_cli.application.build.artifact_discovery import (
    CanonicalPackageBuildResult,
)
from familyos_cli.application.build.artifact_manifest import ArtifactManifest
from familyos_cli.application.build.build_evidence_factory import (
    BuildEvidenceFactory,
)
from familyos_cli.application.build.build_id import BuildId
from familyos_cli.application.build.build_validation import (
    BuildValidationProfile,
    BuildValidationResult,
    BuildValidationStatus,
)
from familyos_cli.application.build.package_build import (
    PackageBuildResult,
    PackageBuildStatus,
)
from familyos_cli.application.build.source_state import SourceState

_BUILD_ID = BuildId(
    UUID("01234567-89ab-4cde-8f01-23456789abcd")
)

_OTHER_BUILD_ID = BuildId(
    UUID("11234567-89ab-4cde-8f01-23456789abcd")
)

_SOURCE_STATE = SourceState(
    revision="0123456789abcdef0123456789abcdef01234567",
    dirty=False,
)


def _package_result() -> CanonicalPackageBuildResult:
    return CanonicalPackageBuildResult(
        status=PackageBuildStatus.SUCCEEDED,
        execution=PackageBuildResult(
            status=PackageBuildStatus.SUCCEEDED,
            outputs=(Path("dist/familyos_cli-0.1.0-py3-none-any.whl"),),
        ),
        source_state=_SOURCE_STATE,
        build_id=_BUILD_ID,
        artifact_integrities=(),
        artifact_manifest=ArtifactManifest(
            build_id=_BUILD_ID,
            entries=(),
        ),
    )


def _validation_result(
    *,
    build_id: BuildId = _BUILD_ID,
) -> BuildValidationResult:
    return BuildValidationResult(
        build_id=build_id,
        profile=BuildValidationProfile.VALIDATION,
        checks=(),
        status=BuildValidationStatus.PASSED,
    )


def test_factory_preserves_canonical_package_build_authorities() -> None:
    package_result = _package_result()
    validation_result = _validation_result()

    evidence = BuildEvidenceFactory().from_package_build(
        package_result,
        validation_result,
    )

    assert evidence.build_id == package_result.build_id
    assert evidence.source_state is package_result.source_state
    assert evidence.validation_result is validation_result
    assert evidence.artifact_manifest is package_result.artifact_manifest
    assert evidence.artifact_integrities is package_result.artifact_integrities


def test_factory_preserves_validation_profile() -> None:
    evidence = BuildEvidenceFactory().from_package_build(
        _package_result(),
        _validation_result(),
    )

    assert evidence.profile is BuildValidationProfile.VALIDATION


def test_factory_rejects_mismatched_validation_build_id() -> None:
    with pytest.raises(
        ValueError,
        match="validation result build ID does not match package build",
    ):
        BuildEvidenceFactory().from_package_build(
            _package_result(),
            _validation_result(build_id=_OTHER_BUILD_ID),
        )


def test_factory_requires_artifact_manifest() -> None:
    package_result = _package_result()

    package_result = CanonicalPackageBuildResult(
        status=package_result.status,
        execution=package_result.execution,
        source_state=package_result.source_state,
        build_id=package_result.build_id,
        artifact_integrities=package_result.artifact_integrities,
    )

    with pytest.raises(
        ValueError,
        match="package build does not contain an artifact manifest",
    ):
        BuildEvidenceFactory().from_package_build(
            package_result,
            _validation_result(),
        )


def test_factory_requires_captured_source_revision() -> None:
    package_result = _package_result()

    package_result = CanonicalPackageBuildResult(
        status=package_result.status,
        execution=package_result.execution,
        source_state=SourceState(
            revision=None,
            dirty=False,
        ),
        build_id=package_result.build_id,
        artifact_integrities=package_result.artifact_integrities,
        artifact_manifest=package_result.artifact_manifest,
    )

    with pytest.raises(
        ValueError,
        match="package build does not contain a captured source revision",
    ):
        BuildEvidenceFactory().from_package_build(
            package_result,
            _validation_result(),
        )
