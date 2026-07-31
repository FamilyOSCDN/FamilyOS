"""Tests for plugin versions."""

import pytest

from familyos_cli.plugins.ecosystem.resolution.plugin_version import (
    PluginVersion,
)


def test_plugin_version_parse() -> None:
    """A stable semantic version should be parsed."""

    version = PluginVersion.parse(
        "1.2.3",
    )

    assert version.major == 1
    assert version.minor == 2
    assert version.patch == 3
    assert version.pre_release == ()
    assert version.build_metadata == ()
    assert version.is_pre_release is False
    assert str(version) == "1.2.3"


def test_plugin_version_parses_pre_release() -> None:
    """Pre-release identifiers should be preserved."""

    version = PluginVersion.parse(
        "1.2.3-alpha.1",
    )

    assert version.pre_release == (
        "alpha",
        "1",
    )
    assert version.is_pre_release is True
    assert str(version) == "1.2.3-alpha.1"


def test_plugin_version_parses_build_metadata() -> None:
    """Build metadata should be preserved."""

    version = PluginVersion.parse(
        "1.2.3+build.45",
    )

    assert version.build_metadata == (
        "build",
        "45",
    )
    assert str(version) == "1.2.3+build.45"


def test_plugin_version_parses_complete_semantic_version() -> None:
    """Pre-release and build metadata may coexist."""

    version = PluginVersion.parse(
        "2.0.0-rc.1+build.2026",
    )

    assert version.pre_release == (
        "rc",
        "1",
    )
    assert version.build_metadata == (
        "build",
        "2026",
    )
    assert str(version) == "2.0.0-rc.1+build.2026"


@pytest.mark.parametrize(
    (
        "lower",
        "higher",
    ),
    [
        (
            "1.0.0-alpha",
            "1.0.0-alpha.1",
        ),
        (
            "1.0.0-alpha.1",
            "1.0.0-alpha.beta",
        ),
        (
            "1.0.0-alpha.beta",
            "1.0.0-beta",
        ),
        (
            "1.0.0-beta",
            "1.0.0-beta.2",
        ),
        (
            "1.0.0-beta.2",
            "1.0.0-beta.11",
        ),
        (
            "1.0.0-beta.11",
            "1.0.0-rc.1",
        ),
        (
            "1.0.0-rc.1",
            "1.0.0",
        ),
        (
            "1.9.9",
            "2.0.0",
        ),
    ],
)
def test_plugin_versions_follow_semantic_precedence(
    lower: str,
    higher: str,
) -> None:
    """Versions should follow semantic precedence rules."""

    assert (
        PluginVersion.parse(lower)
        < PluginVersion.parse(higher)
    )


def test_build_metadata_does_not_change_precedence() -> None:
    """Build metadata should be ignored during comparison."""

    first = PluginVersion.parse(
        "1.2.3+build.1",
    )
    second = PluginVersion.parse(
        "1.2.3+build.2",
    )

    assert first == second
    assert first >= second
    assert first <= second


@pytest.mark.parametrize(
    "value",
    [
        "",
        "1",
        "1.2",
        "1.2.3.4",
        "01.2.3",
        "1.02.3",
        "1.2.03",
        "1.two.3",
        "-1.0.0",
        "1.0.0-",
        "1.0.0-alpha..1",
        "1.0.0-01",
        "1.0.0+",
        "1.0.0+build..1",
        "v1.2.3",
    ],
)
def test_invalid_plugin_versions_are_rejected(
    value: str,
) -> None:
    """Invalid semantic versions should be rejected."""

    with pytest.raises(
        ValueError,
    ):
        PluginVersion.parse(value)
