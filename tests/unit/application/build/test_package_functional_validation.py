"""Tests for immutable Python wheel functional-validation results."""

from pathlib import Path

from familyos_cli.application.build import (
    ArtifactClass,
    DiscoveredArtifact,
    PackageFunctionalValidationStatus,
    PythonWheelFunctionalValidationResult,
    WheelFunctionalValidationFinding,
    WheelFunctionalValidationStage,
)


def test_valid_functional_result_has_no_stronger_artifact_semantics(
    tmp_path: Path,
) -> None:
    candidate = DiscoveredArtifact(
        tmp_path / "familyos_cli-0.1.0-py3-none-any.whl",
        ArtifactClass.PYTHON_WHEEL,
    )
    result = PythonWheelFunctionalValidationResult(
        candidate=candidate,
        status=PackageFunctionalValidationStatus.VALID,
        environment_root=tmp_path / "clean-environment",
        imported_module_path=(
            tmp_path
            / "clean-environment"
            / "lib"
            / "python3.13"
            / "site-packages"
            / "familyos_cli"
            / "main.py"
        ),
    )

    assert result.successful
    assert result.diagnostic is None
    assert result.candidate is candidate
    for field in (
        "trusted",
        "integrity_verified",
        "release_ready",
        "digest",
        "build_id",
        "provenance",
    ):
        assert not hasattr(result, field)


def test_invalid_functional_result_renders_stage_specific_diagnostics(
    tmp_path: Path,
) -> None:
    candidate = DiscoveredArtifact(
        tmp_path / "familyos_cli-0.1.0-py3-none-any.whl",
        ArtifactClass.PYTHON_WHEEL,
    )
    result = PythonWheelFunctionalValidationResult(
        candidate=candidate,
        status=PackageFunctionalValidationStatus.INVALID,
        findings=(
            WheelFunctionalValidationFinding(
                WheelFunctionalValidationStage.CLI_SMOKE,
                "installed entry point returned exit code 1",
            ),
        ),
    )

    assert not result.successful
    assert result.diagnostic == (
        "Python wheel functional validation failed: python-wheel "
        "familyos_cli-0.1.0-py3-none-any.whl: installed CLI smoke: "
        "installed entry point returned exit code 1"
    )
