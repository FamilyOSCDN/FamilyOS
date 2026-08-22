"""Tests for canonical critical build-toolchain state."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

import familyos_cli.application.build.toolchain_state_provider as provider_module
from familyos_cli.application.build.toolchain_state import (
    ToolchainState,
    ToolchainVersion,
)
from familyos_cli.application.build.toolchain_state_provider import (
    ToolchainStateProvider,
)

_VERSIONS = {
    "build": "1.5.0",
    "pip-tools": "7.6.1",
    "setuptools": "84.0.0",
    "wheel": "0.48.0",
}


def test_provider_captures_critical_versions_in_deterministic_order(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        provider_module,
        "distribution_version",
        _VERSIONS.__getitem__,
    )

    state = ToolchainStateProvider().capture()

    assert tuple(
        (component.distribution, component.version)
        for component in state.critical_versions
    ) == tuple(_VERSIONS.items())


def test_provider_is_deterministic(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        provider_module,
        "distribution_version",
        _VERSIONS.__getitem__,
    )
    provider = ToolchainStateProvider()

    assert provider.capture() == provider.capture()


def test_provider_rejects_unavailable_critical_distribution(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from importlib.metadata import PackageNotFoundError

    def unavailable(distribution: str) -> str:
        raise PackageNotFoundError(distribution)

    monkeypatch.setattr(
        provider_module,
        "distribution_version",
        unavailable,
    )

    with pytest.raises(
        ValueError,
        match="critical toolchain distribution 'build' is unavailable",
    ):
        ToolchainStateProvider().capture()


@pytest.mark.parametrize(
    ("distribution", "version", "message"),
    (
        ("", "1.0.0", "toolchain distribution must not be empty"),
        ("build", "", "toolchain version must not be empty"),
    ),
)
def test_toolchain_version_rejects_incomplete_identity(
    distribution: str,
    version: str,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        ToolchainVersion(
            distribution=distribution,
            version=version,
        )


def test_toolchain_state_rejects_empty_critical_versions() -> None:
    with pytest.raises(
        ValueError,
        match="critical toolchain versions must not be empty",
    ):
        ToolchainState(critical_versions=())


def test_toolchain_state_rejects_duplicate_distributions() -> None:
    component = ToolchainVersion(
        distribution="build",
        version="1.5.0",
    )

    with pytest.raises(
        ValueError,
        match="critical toolchain distributions must be unique",
    ):
        ToolchainState(critical_versions=(component, component))


def test_toolchain_state_is_immutable() -> None:
    state = ToolchainState(
        critical_versions=(
            ToolchainVersion(
                distribution="build",
                version="1.5.0",
            ),
        ),
    )

    with pytest.raises(FrozenInstanceError):
        state.critical_versions = ()  # type: ignore[misc]
