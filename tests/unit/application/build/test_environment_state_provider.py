"""Tests for canonical build environment-state capture."""

from __future__ import annotations

from familyos_cli.application.build.environment_state import EnvironmentState
from familyos_cli.application.build.environment_state_provider import (
    EnvironmentStateProvider,
)


def test_environment_state_provider_captures_platform_properties() -> None:
    provider = EnvironmentStateProvider(
        system_provider=lambda: "Darwin",
        release_provider=lambda: "24.6.0",
        machine_provider=lambda: "arm64",
    )

    assert provider.capture() == EnvironmentState(
        operating_system="Darwin",
        operating_system_release="24.6.0",
        machine_architecture="arm64",
    )


def test_environment_state_provider_captures_each_property_once() -> None:
    calls: list[str] = []

    def system_provider() -> str:
        calls.append("system")
        return "Darwin"

    def release_provider() -> str:
        calls.append("release")
        return "24.6.0"

    def machine_provider() -> str:
        calls.append("machine")
        return "arm64"

    provider = EnvironmentStateProvider(
        system_provider=system_provider,
        release_provider=release_provider,
        machine_provider=machine_provider,
    )

    provider.capture()

    assert calls == [
        "system",
        "release",
        "machine",
    ]


def test_environment_state_provider_returns_fresh_observation() -> None:
    systems = iter(("Darwin", "Linux"))

    provider = EnvironmentStateProvider(
        system_provider=lambda: next(systems),
        release_provider=lambda: "1.0",
        machine_provider=lambda: "arm64",
    )

    first = provider.capture()
    second = provider.capture()

    assert first.operating_system == "Darwin"
    assert second.operating_system == "Linux"
    assert first is not second
