"""Tests for PluginResolver package selector integration."""

from collections.abc import Sequence

from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)
from familyos_cli.plugins.ecosystem.resolution import (
    PluginDependency,
    PluginPackageSelector,
    PluginResolver,
)


class RecordingPluginPackageSelector(
    PluginPackageSelector,
):
    """Record package selection calls."""

    def __init__(
        self,
        selected_package: PluginPackage | None,
    ) -> None:
        """Initialize the recording package selector."""

        self.selected_package = selected_package
        self.calls: list[
            tuple[
                PluginDependency,
                tuple[PluginPackage, ...],
            ]
        ] = []

    def select(
        self,
        dependency: PluginDependency,
        candidates: Sequence[PluginPackage],
    ) -> PluginPackage | None:
        """Record a selection call and return the configured package."""

        self.calls.append(
            (
                dependency,
                tuple(candidates),
            ),
        )

        return self.selected_package


def test_resolver_delegates_package_selection() -> None:
    dependency = PluginDependency(
        plugin_id="familyos.identity",
    )
    identity_v1 = PluginPackage(
        plugin_id="familyos.identity",
        version="1.0.0",
        source="official",
    )
    identity_v2 = PluginPackage(
        plugin_id="familyos.identity",
        version="2.0.0",
        source="official",
    )
    selector = RecordingPluginPackageSelector(
        selected_package=identity_v2,
    )
    resolver = PluginResolver(
        package_selector=selector,
    )

    plan = resolver.resolve(
        dependencies=[
            dependency,
        ],
        available_packages=[
            identity_v1,
            identity_v2,
        ],
    )

    assert selector.calls == [
        (
            dependency,
            (
                identity_v1,
                identity_v2,
            ),
        ),
    ]
    assert plan.ordered_packages == [
        identity_v2,
    ]


def test_resolver_does_not_call_selector_without_candidates() -> None:
    selector = RecordingPluginPackageSelector(
        selected_package=None,
    )
    resolver = PluginResolver(
        package_selector=selector,
    )

    plan = resolver.resolve(
        dependencies=[
            PluginDependency(
                plugin_id="familyos.identity",
            ),
        ],
        available_packages=[],
    )

    assert selector.calls == []
    assert plan.ordered_packages == []
    assert len(plan.diagnostics) == 1
    assert plan.diagnostics[0].message == "Required plugin dependency is not available."


def test_resolver_reports_unresolved_selection() -> None:
    dependency = PluginDependency(
        plugin_id="familyos.identity",
        minimum_version="3.0.0",
    )
    identity_package = PluginPackage(
        plugin_id="familyos.identity",
        version="2.0.0",
        source="official",
    )
    selector = RecordingPluginPackageSelector(
        selected_package=None,
    )
    resolver = PluginResolver(
        package_selector=selector,
    )

    plan = resolver.resolve(
        dependencies=[
            dependency,
        ],
        available_packages=[
            identity_package,
        ],
    )

    assert selector.calls == [
        (
            dependency,
            (identity_package,),
        ),
    ]
    assert plan.ordered_packages == []
    assert plan.skipped_packages == [
        identity_package,
    ]
    assert len(plan.diagnostics) == 1
    assert plan.diagnostics[0].plugin == "familyos.identity"
    assert plan.diagnostics[0].message == (
        "No available plugin version satisfies constraint set '>=3.0.0'."
    )


def test_resolver_preserves_invalid_version_diagnostic() -> None:
    dependency = PluginDependency(
        plugin_id="familyos.identity",
    )
    invalid_package = PluginPackage(
        plugin_id="familyos.identity",
        version="invalid",
        source="official",
    )
    selector = RecordingPluginPackageSelector(
        selected_package=None,
    )
    resolver = PluginResolver(
        package_selector=selector,
    )

    plan = resolver.resolve(
        dependencies=[
            dependency,
        ],
        available_packages=[
            invalid_package,
        ],
    )

    assert selector.calls == [
        (
            dependency,
            (invalid_package,),
        ),
    ]
    assert plan.ordered_packages == []
    assert plan.skipped_packages == [
        invalid_package,
    ]
    assert len(plan.diagnostics) == 2
    assert plan.diagnostics[0].message == "Plugin package version 'invalid' is invalid."
    assert (
        plan.diagnostics[1].message
        == "No package with a valid semantic version is available."
    )


def test_resolver_does_not_skip_lower_compatible_package() -> None:
    dependency = PluginDependency(
        plugin_id="familyos.identity",
        minimum_version="1.0.0",
    )
    identity_v1 = PluginPackage(
        plugin_id="familyos.identity",
        version="1.0.0",
        source="official",
    )
    identity_v2 = PluginPackage(
        plugin_id="familyos.identity",
        version="2.0.0",
        source="official",
    )
    selector = RecordingPluginPackageSelector(
        selected_package=identity_v2,
    )
    resolver = PluginResolver(
        package_selector=selector,
    )

    plan = resolver.resolve(
        dependencies=[
            dependency,
        ],
        available_packages=[
            identity_v1,
            identity_v2,
        ],
    )

    assert plan.ordered_packages == [
        identity_v2,
    ]
    assert plan.skipped_packages == []
    assert plan.diagnostics == []


def test_resolver_skips_only_incompatible_candidates() -> None:
    dependency = PluginDependency(
        plugin_id="familyos.identity",
        minimum_version="2.0.0",
    )
    incompatible_package = PluginPackage(
        plugin_id="familyos.identity",
        version="1.0.0",
        source="official",
    )
    selected_package = PluginPackage(
        plugin_id="familyos.identity",
        version="2.0.0",
        source="official",
    )
    selector = RecordingPluginPackageSelector(
        selected_package=selected_package,
    )
    resolver = PluginResolver(
        package_selector=selector,
    )

    plan = resolver.resolve(
        dependencies=[
            dependency,
        ],
        available_packages=[
            incompatible_package,
            selected_package,
        ],
    )

    assert plan.ordered_packages == [
        selected_package,
    ]
    assert plan.skipped_packages == [
        incompatible_package,
    ]
    assert plan.diagnostics == []


def test_resolver_uses_default_package_selector() -> None:
    resolver = PluginResolver()

    plan = resolver.resolve(
        dependencies=[
            PluginDependency(
                plugin_id="familyos.identity",
            ),
        ],
        available_packages=[
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
        ],
    )

    assert len(plan.ordered_packages) == 1
    assert plan.ordered_packages[0].version == "2.0.0"
    assert plan.skipped_packages == []
    assert plan.diagnostics == []
