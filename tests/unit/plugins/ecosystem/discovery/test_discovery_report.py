"""Tests for plugin discovery report."""

from familyos_cli.plugins.ecosystem.discovery import (
    PluginDiscoveryReport,
)
from familyos_cli.plugins.ecosystem.package import (
    PluginPackage,
)
from familyos_cli.plugins.ecosystem.repository import (
    PluginRepository,
)


def test_discovery_report_creation() -> None:
    """Discovery report should expose repository and packages."""

    repository = PluginRepository(
        name="Official",
        url="https://plugins.familyos.dev",
        repository_type="official",
    )

    package = PluginPackage(
        plugin_id="familyos.calendar",
        version="1.0.0",
        source="Official",
    )

    report = PluginDiscoveryReport(
        repository=repository,
        packages=(package,),
    )

    assert report.repository is repository
    assert report.package_count == 1
    assert report.successful is True
    assert report.has_errors is False
    assert report.has_warnings is False


def test_discovery_report_with_errors() -> None:
    """Discovery report should expose errors."""

    repository = PluginRepository(
        name="Official",
        url="https://plugins.familyos.dev",
        repository_type="official",
    )

    report = PluginDiscoveryReport(
        repository=repository,
        packages=(),
        errors=("Repository unavailable",),
    )

    assert report.successful is False
    assert report.has_errors is True
    assert report.package_count == 0


def test_discovery_report_with_warnings() -> None:
    """Discovery report should expose warnings."""

    repository = PluginRepository(
        name="Official",
        url="https://plugins.familyos.dev",
        repository_type="official",
    )

    report = PluginDiscoveryReport(
        repository=repository,
        packages=(),
        warnings=("Plugin ignored",),
    )

    assert report.has_warnings is True
    assert report.successful is True
