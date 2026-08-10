"""Tests for the plugin package selector."""

from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)
from familyos_cli.plugins.ecosystem.resolution import (
    ConstraintSet,
    PluginDependency,
    PluginPackageSelector,
)


def test_select_returns_none_for_empty_candidates() -> None:
    selector = PluginPackageSelector()

    selected_package = selector.select(
        dependency=PluginDependency(
            plugin_id="familyos.identity",
        ),
        candidates=(),
    )

    assert selected_package is None


def test_select_returns_single_valid_package() -> None:
    selector = PluginPackageSelector()

    package = PluginPackage(
        plugin_id="familyos.identity",
        version="1.0.0",
        source="official",
    )

    selected_package = selector.select(
        dependency=PluginDependency(
            plugin_id="familyos.identity",
        ),
        candidates=(package,),
    )

    assert selected_package == package


def test_select_returns_highest_valid_package() -> None:
    selector = PluginPackageSelector()

    selected_package = selector.select(
        dependency=PluginDependency(
            plugin_id="familyos.identity",
        ),
        candidates=(
            PluginPackage(
                plugin_id="familyos.identity",
                version="1.0.0",
                source="official",
            ),
            PluginPackage(
                plugin_id="familyos.identity",
                version="2.1.0",
                source="official",
            ),
            PluginPackage(
                plugin_id="familyos.identity",
                version="2.0.0",
                source="official",
            ),
        ),
    )

    assert selected_package is not None
    assert selected_package.version == "2.1.0"


def test_select_applies_minimum_version_constraint() -> None:
    selector = PluginPackageSelector()

    selected_package = selector.select(
        dependency=PluginDependency(
            plugin_id="familyos.identity",
            minimum_version="2.0.0",
        ),
        candidates=(
            PluginPackage(
                plugin_id="familyos.identity",
                version="1.5.0",
                source="official",
            ),
            PluginPackage(
                plugin_id="familyos.identity",
                version="2.0.0",
                source="official",
            ),
            PluginPackage(
                plugin_id="familyos.identity",
                version="2.3.0",
                source="official",
            ),
        ),
    )

    assert selected_package is not None
    assert selected_package.version == "2.3.0"


def test_select_applies_constraint_set() -> None:
    selector = PluginPackageSelector()

    selected_package = selector.select(
        dependency=PluginDependency(
            plugin_id="familyos.identity",
            constraint_set=ConstraintSet.parse(
                ">=2.0.0,<3.0.0",
            ),
        ),
        candidates=(
            PluginPackage(
                plugin_id="familyos.identity",
                version="1.9.0",
                source="official",
            ),
            PluginPackage(
                plugin_id="familyos.identity",
                version="2.0.0",
                source="official",
            ),
            PluginPackage(
                plugin_id="familyos.identity",
                version="2.8.0",
                source="official",
            ),
            PluginPackage(
                plugin_id="familyos.identity",
                version="3.0.0",
                source="official",
            ),
        ),
    )

    assert selected_package is not None
    assert selected_package.version == "2.8.0"


def test_select_returns_none_when_no_version_is_compatible() -> None:
    selector = PluginPackageSelector()

    selected_package = selector.select(
        dependency=PluginDependency(
            plugin_id="familyos.identity",
            minimum_version="3.0.0",
        ),
        candidates=(
            PluginPackage(
                plugin_id="familyos.identity",
                version="1.0.0",
                source="official",
            ),
            PluginPackage(
                plugin_id="familyos.identity",
                version="2.0.0",
                source="official",
            ),
        ),
    )

    assert selected_package is None


def test_select_ignores_invalid_semantic_versions() -> None:
    selector = PluginPackageSelector()

    valid_package = PluginPackage(
        plugin_id="familyos.identity",
        version="2.0.0",
        source="official",
    )

    selected_package = selector.select(
        dependency=PluginDependency(
            plugin_id="familyos.identity",
        ),
        candidates=(
            PluginPackage(
                plugin_id="familyos.identity",
                version="invalid",
                source="official",
            ),
            valid_package,
        ),
    )

    assert selected_package == valid_package


def test_select_returns_none_when_all_versions_are_invalid() -> None:
    selector = PluginPackageSelector()

    selected_package = selector.select(
        dependency=PluginDependency(
            plugin_id="familyos.identity",
        ),
        candidates=(
            PluginPackage(
                plugin_id="familyos.identity",
                version="invalid",
                source="official",
            ),
            PluginPackage(
                plugin_id="familyos.identity",
                version="1.0",
                source="official",
            ),
        ),
    )

    assert selected_package is None


def test_select_prefers_stable_release_over_pre_release() -> None:
    selector = PluginPackageSelector()

    selected_package = selector.select(
        dependency=PluginDependency(
            plugin_id="familyos.identity",
        ),
        candidates=(
            PluginPackage(
                plugin_id="familyos.identity",
                version="2.0.0-rc.1",
                source="official",
            ),
            PluginPackage(
                plugin_id="familyos.identity",
                version="2.0.0",
                source="official",
            ),
        ),
    )

    assert selected_package is not None
    assert selected_package.version == "2.0.0"


def test_select_accepts_sequence_input() -> None:
    selector = PluginPackageSelector()

    candidates = [
        PluginPackage(
            plugin_id="familyos.identity",
            version="1.0.0",
            source="official",
        ),
        PluginPackage(
            plugin_id="familyos.identity",
            version="2.0.0",
            source="official",
        ),
    ]

    selected_package = selector.select(
        dependency=PluginDependency(
            plugin_id="familyos.identity",
        ),
        candidates=candidates,
    )

    assert selected_package is not None
    assert selected_package.version == "2.0.0"
