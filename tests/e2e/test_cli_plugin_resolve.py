"""End-to-end tests for the plugin resolution CLI."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from familyos_cli.interfaces.cli.app import app

runner = CliRunner()


def write_plugin_manifest(
    plugin_directory: Path,
    *,
    plugin_id: str,
    name: str,
    version: str = "1.0.0",
) -> None:
    """Write a canonical plugin manifest for CLI resolution tests."""

    plugin_directory.mkdir(
        parents=True,
    )

    (plugin_directory / "plugin.yaml").write_text(
        (
            f"id: {plugin_id}\n"
            f"name: {name}\n"
            f"version: {version}\n"
            "author: FamilyOS Team\n"
            "description: E2E plugin resolution fixture.\n"
            f"module: tests.fixtures.{plugin_id}.plugin\n"
            "class: TestPlugin\n"
            "enabled: true\n"
        ),
        encoding="utf-8",
    )


def test_cli_plugin_resolve_should_resolve_local_plugin(
    tmp_path: Path,
) -> None:
    """CLI should resolve a canonical plugin from a local repository."""

    write_plugin_manifest(
        tmp_path / "communication",
        plugin_id="familyos.communication",
        name="FamilyOS Communication Plugin",
    )

    result = runner.invoke(
        app,
        [
            "plugin",
            "resolve",
            "familyos.communication",
            "--repository-name",
            "E2E Repository",
            "--repository-url",
            str(tmp_path),
            "--repository-type",
            "local",
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output

    assert (
        "Plugin resolution completed successfully: "
        "1 package(s) selected."
        in result.output
    )

    assert "Traceback" not in result.output


def test_cli_plugin_resolve_should_render_missing_dependency_diagnostic(
    tmp_path: Path,
) -> None:
    """CLI should fail cleanly when a required plugin is missing."""

    result = runner.invoke(
        app,
        [
            "plugin",
            "resolve",
            "familyos.missing",
            "--repository-name",
            "E2E Repository",
            "--repository-url",
            str(tmp_path),
            "--repository-type",
            "local",
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 1, result.output

    assert "ERROR: Missing plugin dependency" in result.output

    assert (
        "A required plugin dependency is not available."
        in result.output
    )

    assert "Suggestions:" in result.output

    assert (
        "Install the missing plugin or enable a repository."
        in result.output
    )

    assert "Traceback" not in result.output


def test_cli_plugin_resolve_should_report_noncanonical_plugin_identifier(
    tmp_path: Path,
) -> None:
    """CLI should reject a noncanonical Plugin Identifier cleanly."""

    result = runner.invoke(
        app,
        [
            "plugin",
            "resolve",
            "communication",
            "--repository-name",
            "E2E Repository",
            "--repository-url",
            str(tmp_path),
            "--repository-type",
            "local",
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 1, result.output

    assert "Invalid Plugin Identifier" in result.output
    assert "communication" in result.output

    assert "Traceback" not in result.output
