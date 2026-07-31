"""Tests for plugin dependency resolution."""

from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)
from familyos_cli.plugins.ecosystem.resolution.constraint_set import (
    ConstraintSet,
)
from familyos_cli.plugins.ecosystem.resolution.plugin_dependency import (
    PluginDependency,
)
from familyos_cli.plugins.ecosystem.resolution.plugin_resolver import (
    PluginResolver,
)


def make_package(
    name: str,
    version: str,
) -> PluginPackage:
    """Create a plugin package for resolver tests."""

    return PluginPackage(
        name=name,
        version=version,
        source="test",
    )


def test_resolve_empty_dependencies_returns_empty_plan() -> None:
    resolver = PluginResolver()

    plan = resolver.resolve(
        dependencies=[],
        available_packages=[],
    )

    assert plan.ordered_packages == []
    assert plan.skipped_packages == []
    assert plan.diagnostics == []


def test_resolve_dependency_without_constraint() -> None:
    package = make_package(
        name="documentation",
        version="1.0.0",
    )
    resolver = PluginResolver()

    plan = resolver.resolve(
        dependencies=[
            PluginDependency(
                name="documentation",
            ),
        ],
        available_packages=[
            package,
        ],
    )

    assert plan.ordered_packages == [
        package,
    ]
    assert plan.skipped_packages == []
    assert plan.diagnostics == []


def test_resolve_selects_highest_available_version() -> None:
    version_1 = make_package(
        name="documentation",
        version="1.0.0",
    )
    version_2 = make_package(
        name="documentation",
        version="2.0.0",
    )
    version_3 = make_package(
        name="documentation",
        version="1.5.0",
    )
    resolver = PluginResolver()

    plan = resolver.resolve(
        dependencies=[
            PluginDependency(
                name="documentation",
            ),
        ],
        available_packages=[
            version_1,
            version_2,
            version_3,
        ],
    )

    assert plan.ordered_packages == [
        version_2,
    ]
    assert plan.skipped_packages == []
    assert plan.diagnostics == []


def test_resolve_selects_highest_compatible_version() -> None:
    version_1 = make_package(
        name="documentation",
        version="1.0.0",
    )
    version_2 = make_package(
        name="documentation",
        version="1.8.0",
    )
    version_3 = make_package(
        name="documentation",
        version="2.0.0",
    )
    resolver = PluginResolver()

    plan = resolver.resolve(
        dependencies=[
            PluginDependency(
                name="documentation",
                constraint_set=ConstraintSet.parse(
                    ">=1.0.0,<2.0.0",
                ),
            ),
        ],
        available_packages=[
            version_1,
            version_2,
            version_3,
        ],
    )

    assert plan.ordered_packages == [
        version_2,
    ]
    assert plan.skipped_packages == [
        version_3,
    ]
    assert plan.diagnostics == []


def test_resolve_reports_missing_dependency() -> None:
    resolver = PluginResolver()

    plan = resolver.resolve(
        dependencies=[
            PluginDependency(
                name="missing-plugin",
            ),
        ],
        available_packages=[],
    )

    assert plan.ordered_packages == []
    assert plan.skipped_packages == []
    assert len(plan.diagnostics) == 1
    assert plan.diagnostics[0].plugin == "missing-plugin"
    assert (
        plan.diagnostics[0].message
        == "Required plugin dependency is not available."
    )


def test_resolve_reports_invalid_package_version() -> None:
    invalid_package = make_package(
        name="documentation",
        version="invalid-version",
    )
    resolver = PluginResolver()

    plan = resolver.resolve(
        dependencies=[
            PluginDependency(
                name="documentation",
            ),
        ],
        available_packages=[
            invalid_package,
        ],
    )

    assert plan.ordered_packages == []
    assert plan.skipped_packages == [
        invalid_package,
    ]
    assert len(plan.diagnostics) == 2
    assert (
        plan.diagnostics[0].message
        == "Plugin package version 'invalid-version' is invalid."
    )
    assert (
        plan.diagnostics[1].message
        == "No package with a valid semantic version is available."
    )


def test_resolve_reports_unsatisfied_constraint_set() -> None:
    package = make_package(
        name="documentation",
        version="2.0.0",
    )
    resolver = PluginResolver()

    plan = resolver.resolve(
        dependencies=[
            PluginDependency(
                name="documentation",
                constraint_set=ConstraintSet.parse(
                    ">=1.0.0,<2.0.0",
                ),
            ),
        ],
        available_packages=[
            package,
        ],
    )

    assert plan.ordered_packages == []
    assert plan.skipped_packages == [
        package,
    ]
    assert len(plan.diagnostics) == 1
    assert (
        plan.diagnostics[0].message
        == (
            "No available plugin version satisfies constraint set "
            "'>=1.0.0,<2.0.0'."
        )
    )


def test_resolve_keeps_valid_candidate_when_another_is_invalid() -> None:
    invalid_package = make_package(
        name="documentation",
        version="invalid",
    )
    valid_package = make_package(
        name="documentation",
        version="1.5.0",
    )
    resolver = PluginResolver()

    plan = resolver.resolve(
        dependencies=[
            PluginDependency(
                name="documentation",
                constraint_set=ConstraintSet.parse(
                    "^1.0.0",
                ),
            ),
        ],
        available_packages=[
            invalid_package,
            valid_package,
        ],
    )

    assert plan.ordered_packages == [
        valid_package,
    ]
    assert plan.skipped_packages == [
        invalid_package,
    ]
    assert len(plan.diagnostics) == 1
    assert (
        plan.diagnostics[0].message
        == "Plugin package version 'invalid' is invalid."
    )


def test_resolve_multiple_dependencies() -> None:
    documentation = make_package(
        name="documentation",
        version="1.5.0",
    )
    security = make_package(
        name="security",
        version="2.1.0",
    )
    resolver = PluginResolver()

    plan = resolver.resolve(
        dependencies=[
            PluginDependency(
                name="documentation",
                constraint_set=ConstraintSet.parse(
                    "^1.0.0",
                ),
            ),
            PluginDependency(
                name="security",
                minimum_version="2.0.0",
            ),
        ],
        available_packages=[
            security,
            documentation,
        ],
    )

    assert plan.ordered_packages == [
        documentation,
        security,
    ]
    assert plan.skipped_packages == []
    assert plan.diagnostics == []
