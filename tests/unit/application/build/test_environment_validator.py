"""Tests for canonical observable build-environment validation."""

from __future__ import annotations

from pathlib import Path

from familyos_cli.application.build.environment_state import EnvironmentState
from familyos_cli.application.build.environment_validation import (
    EnvironmentValidationStatus,
)
from familyos_cli.application.build.environment_validator import (
    EnvironmentValidator,
)


def _state(
    *,
    temporary_directory: Path,
    virtual_environment_active: bool = True,
) -> EnvironmentState:
    return EnvironmentState(
        operating_system="TestOS",
        operating_system_release="1.0",
        machine_architecture="test-machine",
        virtual_environment_active=virtual_environment_active,
        temporary_directory=str(temporary_directory),
        filesystem_encoding="utf-8",
    )


def test_valid_observable_environment_succeeds(
    tmp_path: Path,
) -> None:
    result = EnvironmentValidator().validate(
        state=_state(
            temporary_directory=tmp_path,
        )
    )

    assert result.status is EnvironmentValidationStatus.SUCCEEDED
    assert result.successful is True
    assert result.findings == ()
    assert result.diagnostic is None


def test_inactive_virtual_environment_is_observable_but_not_rejected(
    tmp_path: Path,
) -> None:
    result = EnvironmentValidator().validate(
        state=_state(
            temporary_directory=tmp_path,
            virtual_environment_active=False,
        )
    )

    assert result.successful is True
    assert result.findings == ()


def test_unavailable_temporary_directory_fails(
    tmp_path: Path,
) -> None:
    unavailable = tmp_path / "missing"

    result = EnvironmentValidator().validate(
        state=_state(
            temporary_directory=unavailable,
        )
    )

    assert result.status is EnvironmentValidationStatus.FAILED
    assert result.successful is False
    assert len(result.findings) == 1
    assert result.findings[0].component == "temporary-storage"
    assert result.findings[0].diagnostic == (
        f"temporary directory is unavailable: {unavailable}"
    )
    assert result.diagnostic == (
        f"temporary directory is unavailable: {unavailable}"
    )


def test_existing_non_default_temporary_directory_is_accepted(
    tmp_path: Path,
) -> None:
    temporary_directory = tmp_path / "environment-temp"
    temporary_directory.mkdir()

    result = EnvironmentValidator().validate(
        state=_state(
            temporary_directory=temporary_directory,
        )
    )

    assert result.successful is True
