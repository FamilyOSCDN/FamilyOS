"""Tests for the plugin resolution command."""

from __future__ import annotations

from unittest.mock import Mock, patch

from familyos_cli.interfaces.cli.commands.plugin_resolve import (
    EXIT_FAILURE,
    EXIT_SUCCESS,
    plugin_resolve,
)
from familyos_cli.plugins.ecosystem.diagnostics import (
    DiagnosticKind,
    DiagnosticReport,
    DiagnosticSeverity,
    PluginResolutionDiagnostic,
)
from familyos_cli.plugins.ecosystem.package import PluginPackage
from familyos_cli.plugins.ecosystem.resolution import (
    ResolutionDiagnostic,
    ResolutionPlan,
)


@patch(
    "familyos_cli.interfaces.cli.commands.plugin_resolve.CommandContext",
)
@patch(
    "familyos_cli.interfaces.cli.commands.plugin_resolve.Output.success",
)
def test_should_delegate_resolution_to_application_use_case(
    mock_success: Mock,
    mock_context_type: Mock,
) -> None:
    """CLI should delegate plugin resolution to the application layer."""

    resolve_plugins = Mock()
    resolve_plugins.execute.return_value = ResolutionPlan(
        ordered_packages=[
            PluginPackage(
                plugin_id="familyos.documentation",
                version="1.0.0",
                source="official",
            ),
        ],
    )

    context = Mock()
    context.resolve_plugins = resolve_plugins
    mock_context_type.return_value = context

    result = plugin_resolve(
        dependencies=[
            "familyos.documentation>=1.0.0",
        ],
        repository_name="official",
        repository_url="https://plugins.familyos.dev",
        repository_type="remote",
    )

    assert result == EXIT_SUCCESS

    resolve_plugins.execute.assert_called_once_with(
        dependencies=[
            "familyos.documentation>=1.0.0",
        ],
        repository_name="official",
        repository_url="https://plugins.familyos.dev",
        repository_type="remote",
    )

    mock_success.assert_called_once_with(
        (
            "Plugin resolution completed successfully: "
            "1 package(s) selected."
        ),
    )


@patch(
    "familyos_cli.interfaces.cli.commands.plugin_resolve.Output.diagnostic",
)
@patch(
    "familyos_cli.interfaces.cli.commands.plugin_resolve.DiagnosticCliRenderer",
)
@patch(
    "familyos_cli.interfaces.cli.commands.plugin_resolve.ResolutionExplainer",
)
@patch(
    "familyos_cli.interfaces.cli.commands.plugin_resolve.DiagnosticPipeline",
)
@patch(
    "familyos_cli.interfaces.cli.commands.plugin_resolve.CommandContext",
)
def test_should_build_explain_render_and_display_diagnostics(
    mock_context_type: Mock,
    mock_diagnostic_pipeline_type: Mock,
    mock_explainer_type: Mock,
    mock_renderer_type: Mock,
    mock_output_diagnostic: Mock,
) -> None:
    """CLI should render application resolution diagnostics."""

    resolution_plan = ResolutionPlan(
        diagnostics=[
            ResolutionDiagnostic(
                plugin="familyos.missing",
                message=(
                    "Required plugin dependency is not available."
                ),
            ),
        ],
    )

    resolve_plugins = Mock()
    resolve_plugins.execute.return_value = resolution_plan

    context = Mock()
    context.resolve_plugins = resolve_plugins
    mock_context_type.return_value = context

    diagnostic = PluginResolutionDiagnostic(
        kind=DiagnosticKind.MISSING_DEPENDENCY,
        severity=DiagnosticSeverity.ERROR,
        message=(
            "Required plugin dependency is not available."
        ),
        plugin="familyos.missing",
    )

    diagnostic_report = DiagnosticReport(
        diagnostics=(diagnostic,),
    )

    diagnostic_pipeline = Mock()
    diagnostic_pipeline.build.return_value = diagnostic_report
    mock_diagnostic_pipeline_type.return_value = diagnostic_pipeline

    explanation = Mock()

    explainer = Mock()
    explainer.explain.return_value = explanation
    mock_explainer_type.return_value = explainer

    renderer = Mock()
    renderer.render.return_value = "Rendered missing dependency."
    mock_renderer_type.return_value = renderer

    result = plugin_resolve(
        dependencies=[
            "familyos.missing",
        ],
        repository_name="official",
        repository_url="https://plugins.familyos.dev",
        repository_type="remote",
    )

    assert result == EXIT_FAILURE

    resolve_plugins.execute.assert_called_once_with(
        dependencies=[
            "familyos.missing",
        ],
        repository_name="official",
        repository_url="https://plugins.familyos.dev",
        repository_type="remote",
    )

    diagnostic_pipeline.build.assert_called_once_with(
        resolution_plan,
    )

    explainer.explain.assert_called_once_with(
        diagnostic,
    )

    renderer.render.assert_called_once_with(
        explanation,
    )

    mock_output_diagnostic.assert_called_once_with(
        "Rendered missing dependency.",
        styled=True,
    )


@patch(
    "familyos_cli.interfaces.cli.commands.plugin_resolve.CommandContext",
)
@patch(
    "familyos_cli.interfaces.cli.commands.plugin_resolve.Output.error",
)
def test_should_report_application_input_error(
    mock_error: Mock,
    mock_context_type: Mock,
) -> None:
    """CLI should report application boundary validation failures."""

    resolve_plugins = Mock()
    resolve_plugins.execute.side_effect = ValueError(
        "Invalid Plugin Identifier: documentation",
    )

    context = Mock()
    context.resolve_plugins = resolve_plugins
    mock_context_type.return_value = context

    result = plugin_resolve(
        dependencies=[
            "documentation",
        ],
        repository_name="official",
        repository_url="https://plugins.familyos.dev",
        repository_type="remote",
    )

    assert result == EXIT_FAILURE

    mock_error.assert_called_once_with(
        "Invalid Plugin Identifier: documentation",
    )
