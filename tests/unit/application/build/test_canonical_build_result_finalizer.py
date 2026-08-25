"""Tests for canonical Build Result finalization."""

from pathlib import Path
from typing import cast

from familyos_cli.application.build.artifact_discovery import (
    CanonicalPackageBuildResult,
)
from familyos_cli.application.build.build_validation import (
    BuildValidationResult,
)


def test_finalizer_preserves_canonical_build_authorities() -> None:
    from familyos_cli.application.build.canonical_build_result_finalizer import (
        CanonicalBuildResultFinalizer,
    )

    package_result = cast(CanonicalPackageBuildResult, object())
    validation_result = cast(BuildValidationResult, object())
    evidence_reference = Path("/tmp/build-evidence.json")

    result = CanonicalBuildResultFinalizer().finalize(
        package_result=package_result,
        validation_result=validation_result,
        evidence_reference=evidence_reference,
    )

    assert result.package_result is package_result
    assert result.validation_result is validation_result
    assert result.evidence_reference is evidence_reference


def test_finalizer_allows_absent_post_execution_authorities() -> None:
    from familyos_cli.application.build.canonical_build_result_finalizer import (
        CanonicalBuildResultFinalizer,
    )

    package_result = cast(CanonicalPackageBuildResult, object())

    result = CanonicalBuildResultFinalizer().finalize(
        package_result=package_result,
        validation_result=None,
        evidence_reference=None,
    )

    assert result.package_result is package_result
    assert result.validation_result is None
    assert result.evidence_reference is None
