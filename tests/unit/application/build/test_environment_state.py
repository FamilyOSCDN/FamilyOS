"""Tests for canonical build environment state."""

from __future__ import annotations

import pytest

from familyos_cli.application.build.environment_state import EnvironmentState


def test_environment_state_preserves_canonical_platform_properties() -> None:
    state = EnvironmentState(
        operating_system="Darwin",
        operating_system_release="24.6.0",
        machine_architecture="arm64",
        virtual_environment_active=True,
        temporary_directory="/tmp/familyos",
        filesystem_encoding="utf-8",
    )

    assert state.operating_system == "Darwin"
    assert state.operating_system_release == "24.6.0"
    assert state.machine_architecture == "arm64"
    assert state.virtual_environment_active is True
    assert state.temporary_directory == "/tmp/familyos"
    assert state.filesystem_encoding == "utf-8"


@pytest.mark.parametrize(
    ("field", "message"),
    (
        ("operating_system", "operating system must not be empty"),
        (
            "operating_system_release",
            "operating system release must not be empty",
        ),
        ("machine_architecture", "machine architecture must not be empty"),
        ("temporary_directory", "temporary directory must not be empty"),
        ("filesystem_encoding", "filesystem encoding must not be empty"),
    ),
)
def test_environment_state_rejects_empty_canonical_property(
    field: str,
    message: str,
) -> None:
    values = {
        "operating_system": "Darwin",
        "operating_system_release": "24.6.0",
        "machine_architecture": "arm64",
        "temporary_directory": "/tmp/familyos",
        "filesystem_encoding": "utf-8",
    }
    values[field] = ""

    with pytest.raises(ValueError, match=message):
        EnvironmentState(
            operating_system=values["operating_system"],
            operating_system_release=values["operating_system_release"],
            machine_architecture=values["machine_architecture"],
            virtual_environment_active=True,
            temporary_directory=values["temporary_directory"],
            filesystem_encoding=values["filesystem_encoding"],
        )


def test_environment_state_defaults_to_no_virtual_environment() -> None:
    state = EnvironmentState(
        operating_system="Linux",
        operating_system_release="6.8.0",
        machine_architecture="x86_64",
    )

    assert state.virtual_environment_active is False


def test_environment_state_rejects_invalid_virtual_environment_state() -> None:
    with pytest.raises(
        ValueError,
        match="virtual environment state must be a boolean",
    ):
        EnvironmentState(
            operating_system="Darwin",
            operating_system_release="24.6.0",
            machine_architecture="arm64",
            virtual_environment_active="yes",  # type: ignore[arg-type]
        )


def test_environment_state_rejects_whitespace_temporary_directory() -> None:
    with pytest.raises(
        ValueError,
        match="temporary directory must not be empty",
    ):
        EnvironmentState(
            operating_system="Darwin",
            operating_system_release="24.6.0",
            machine_architecture="arm64",
            temporary_directory=" ",
        )


def test_environment_state_rejects_whitespace_filesystem_encoding() -> None:
    with pytest.raises(
        ValueError,
        match="filesystem encoding must not be empty",
    ):
        EnvironmentState(
            operating_system="Darwin",
            operating_system_release="24.6.0",
            machine_architecture="arm64",
            filesystem_encoding=" ",
        )


def test_environment_state_is_immutable() -> None:
    state = EnvironmentState(
        operating_system="Darwin",
        operating_system_release="24.6.0",
        machine_architecture="arm64",
        virtual_environment_active=True,
    )

    with pytest.raises(AttributeError):
        state.operating_system = "Linux"  # type: ignore[misc]
