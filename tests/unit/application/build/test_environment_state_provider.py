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
        virtual_environment_provider=lambda: True,
        temporary_directory_provider=lambda: "/tmp/familyos",
        filesystem_encoding_provider=lambda: "utf-8",
    )

    assert provider.capture() == EnvironmentState(
        operating_system="Darwin",
        operating_system_release="24.6.0",
        machine_architecture="arm64",
        virtual_environment_active=True,
        temporary_directory="/tmp/familyos",
        filesystem_encoding="utf-8",
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

    def virtual_environment_provider() -> bool:
        calls.append("virtual-environment")
        return True

    def temporary_directory_provider() -> str:
        calls.append("temporary-directory")
        return "/tmp/familyos"

    def filesystem_encoding_provider() -> str:
        calls.append("filesystem-encoding")
        return "utf-8"

    provider = EnvironmentStateProvider(
        system_provider=system_provider,
        release_provider=release_provider,
        machine_provider=machine_provider,
        virtual_environment_provider=virtual_environment_provider,
        temporary_directory_provider=temporary_directory_provider,
        filesystem_encoding_provider=filesystem_encoding_provider,
    )

    provider.capture()

    assert calls == [
        "system",
        "release",
        "machine",
        "virtual-environment",
        "temporary-directory",
        "filesystem-encoding",
    ]


def test_environment_state_provider_detects_inactive_virtual_environment() -> None:
    provider = EnvironmentStateProvider(
        system_provider=lambda: "Linux",
        release_provider=lambda: "6.8.0",
        machine_provider=lambda: "x86_64",
        virtual_environment_provider=lambda: False,
        temporary_directory_provider=lambda: "/tmp",
        filesystem_encoding_provider=lambda: "utf-8",
    )

    assert provider.capture().virtual_environment_active is False


def test_environment_state_provider_captures_environment_capabilities() -> None:
    provider = EnvironmentStateProvider(
        system_provider=lambda: "Linux",
        release_provider=lambda: "6.8.0",
        machine_provider=lambda: "x86_64",
        virtual_environment_provider=lambda: True,
        temporary_directory_provider=lambda: "/private/tmp",
        filesystem_encoding_provider=lambda: "utf-8",
    )

    state = provider.capture()

    assert state.temporary_directory == "/private/tmp"
    assert state.filesystem_encoding == "utf-8"


def test_environment_state_provider_returns_fresh_observation() -> None:
    systems = iter(("Darwin", "Linux"))
    virtual_environments = iter((True, False))
    temporary_directories = iter(("/tmp/first", "/tmp/second"))

    provider = EnvironmentStateProvider(
        system_provider=lambda: next(systems),
        release_provider=lambda: "1.0",
        machine_provider=lambda: "arm64",
        virtual_environment_provider=lambda: next(
            virtual_environments
        ),
        temporary_directory_provider=lambda: next(
            temporary_directories
        ),
        filesystem_encoding_provider=lambda: "utf-8",
    )

    first = provider.capture()
    second = provider.capture()

    assert first.operating_system == "Darwin"
    assert first.virtual_environment_active is True
    assert first.temporary_directory == "/tmp/first"

    assert second.operating_system == "Linux"
    assert second.virtual_environment_active is False
    assert second.temporary_directory == "/tmp/second"

    assert first is not second
