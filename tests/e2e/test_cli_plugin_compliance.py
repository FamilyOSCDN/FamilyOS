"""End-to-end tests for the plugin compliance CLI."""

from __future__ import annotations

import json

from typer.testing import CliRunner

from familyos_cli.interfaces.cli.app import app

runner = CliRunner()


def test_cli_plugin_compliance_check_text_format() -> None:
    """CLI should report the bundled security plugin as compliant (text)."""

    result = runner.invoke(
        app,
        [
            "plugin",
            "compliance",
            "check",
            "familyos.security",
            "--format",
            "text",
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output

    assert "Status: COMPLIANT" in result.output
    assert "Plugin: familyos.security" in result.output

    assert "Traceback" not in result.output


def test_cli_plugin_compliance_check_json_format() -> None:
    """CLI should report the bundled security plugin as compliant (JSON)."""

    result = runner.invoke(
        app,
        [
            "plugin",
            "compliance",
            "check",
            "familyos.security",
            "--format",
            "json",
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 0, result.output

    payload = json.loads(result.output)

    assert payload["status"] == "compliant"
    assert payload["plugin_id"] == "familyos.security"
    assert "schema_version" in payload

    assert "Traceback" not in result.output


def test_cli_plugin_compliance_check_reports_unknown_plugin() -> None:
    """CLI should fail cleanly when the plugin id is not discoverable."""

    result = runner.invoke(
        app,
        [
            "plugin",
            "compliance",
            "check",
            "familyos.does-not-exist",
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 1, result.output

    assert "was not found" in result.output

    assert "Traceback" not in result.output


def test_cli_plugin_compliance_check_rejects_unsupported_format() -> None:
    """CLI should reject an unsupported --format value cleanly."""

    result = runner.invoke(
        app,
        [
            "plugin",
            "compliance",
            "check",
            "familyos.security",
            "--format",
            "xml",
        ],
        catch_exceptions=False,
    )

    assert result.exit_code == 1, result.output

    assert "Unsupported format" in result.output

    assert "Traceback" not in result.output
