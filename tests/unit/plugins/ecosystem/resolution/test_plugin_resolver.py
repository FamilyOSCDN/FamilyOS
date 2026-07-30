"""Tests for plugin resolver."""

from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)
from familyos_cli.plugins.ecosystem.resolution import (
    PluginDependency,
    PluginResolver,
)


def test_resolver_finds_matching_packages() -> None:
    """Resolver should include matching packages in the resolution plan."""

    packages = [
        PluginPackage(
            name="notification",
            version="1.0.0",
            source="official",
        ),
        PluginPackage(
            name="calendar",
            version="1.0.0",
            source="official",
        ),
    ]

    dependencies = [
        PluginDependency(
            name="notification",
        ),
    ]

    resolver = PluginResolver()

    plan = resolver.resolve(
        dependencies,
        packages,
    )

    assert len(plan.ordered_packages) == 1
    assert plan.ordered_packages[0].name == "notification"
    assert plan.skipped_packages == []
    assert plan.diagnostics == []


def test_resolver_reports_missing_dependency() -> None:
    """Resolver should report a dependency that is unavailable."""

    dependencies = [
        PluginDependency(
            name="notification",
        ),
    ]

    resolver = PluginResolver()

    plan = resolver.resolve(
        dependencies,
        available_packages=[],
    )

    assert plan.ordered_packages == []
    assert plan.skipped_packages == []
    assert len(plan.diagnostics) == 1
    assert plan.diagnostics[0].plugin == "notification"
    assert (
        plan.diagnostics[0].message
        == "Required plugin dependency is not available."
    )
