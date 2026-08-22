"""Tests for canonical build environment state."""

from __future__ import annotations

import pytest

from familyos_cli.application.build.environment_state import EnvironmentState


def test_environment_state_preserves_canonical_platform_properties() -> None:
    state = EnvironmentState(
        operating_system="Darwin",
        operating_system_release="24.6.0",
        machine_architecture="arm64",
    )

    assert state.operating_system == "Darwin"
    assert state.operating_system_release == "24.6.0"
    assert state.machine_architecture == "arm64"


@pytest.mark.parametrize(
    ("field", "message"),
    (
        ("operating_system", "operating system must not be empty"),
        (
            "operating_system_release",
            "operating system release must not be empty",
        ),
        ("machine_architecture", "machine architecture must not be empty"),
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
    }
    values[field] = ""

    with pytest.raises(ValueError, match=message):
        EnvironmentState(**values)


def test_environment_state_is_immutable() -> None:
    state = EnvironmentState(
        operating_system="Darwin",
        operating_system_release="24.6.0",
        machine_architecture="arm64",
    )

    with pytest.raises(AttributeError):
        state.operating_system = "Linux"  # type: ignore[misc]
