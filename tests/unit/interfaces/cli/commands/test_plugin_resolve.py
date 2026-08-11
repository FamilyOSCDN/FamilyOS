from __future__ import annotations

from unittest.mock import Mock, patch

from familyos_cli.interfaces.cli.commands.plugin_resolve import (
    parse_plugin_dependency,
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


def test_should_parse_dependency_without_constraint() -> None:
    dependency = parse_plugin_dependency(
        "familyos.documentation",
    )

    assert dependency.name == "familyos.documentation"
    assert dependency.constraint_set is None


def test_should_parse_dependency_with_constraint_set() -> None:
    dependency = parse_plugin_dependency(
        "familyos.calendar>=1.0.0,<2.0.0",
    )

    assert dependency.name == "familyos.calendar"
    assert dependency.constraint_set is not None
    assert str(dependency.constraint_set) == ">=1.0.0,<2.0.0"


@patch(
    "familyos_cli.interfaces.cli.commands.plugin_resolve.CommandContext",
)
@patch(
    "familyos_cli.interfaces.cli.commands.plugin_resolve.Output.success",
)
def test_should_resolve_plugins_through_pipeline(
    mock_success: Mock,
    mock_context_type: Mock,
) -> None:
    pipeline = Mock()
    pipeline.resolve.return_value = ResolutionPlan(
        ordered_packages=[
            PluginPackage(
                plugin_id="familyos.documentation",
                version="1.0.0",
                source="official",
            ),
        ],
    )

    context = Mock()
    context.plugin_resolution_pipeline = pipeline
    mock_context_type.return_value = context

    plugin_resolve(
        dependencies=[
            "familyos.documentation>=1.0.0",
        ],
        repository_name="official",
        repository_url="https://plugins.familyos.dev",
        repository_type="remote",
    )

    pipeline.resolve.assert_called_once()

    call = pipeline.resolve.call_args

    repository = call.kwargs["repository"]
    dependencies = call.kwargs["dependencies"]

    assert repository.name == "official"
    assert repository.url == "https://plugins.familyos.dev"
    assert repository.repository_type == "remote"

    assert len(dependencies) == 1
    assert dependencies[0].name == "familyos.documentation"
    assert str(dependencies[0].constraint_set) == ">=1.0.0"

    mock_success.assert_called_once_with(
        ("Plugin resolution completed successfully: 1 package(s) selected."),
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
    resolution_plan = ResolutionPlan(
        diagnostics=[
            ResolutionDiagnostic(
                plugin="familyos.missing",
                message=("Required plugin dependency is not available."),
            ),
        ],
    )

    resolution_pipeline = Mock()
    resolution_pipeline.resolve.return_value = resolution_plan

    context = Mock()
    context.plugin_resolution_pipeline = resolution_pipeline
    mock_context_type.return_value = context

    diagnostic = PluginResolutionDiagnostic(
        kind=DiagnosticKind.MISSING_DEPENDENCY,
        severity=DiagnosticSeverity.ERROR,
        message=("Required plugin dependency is not available."),
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

    plugin_resolve(
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
    )


@patch(
    "familyos_cli.interfaces.cli.commands.plugin_resolve.CommandContext",
)
@patch(
    "familyos_cli.interfaces.cli.commands.plugin_resolve.Output.error",
)
def test_should_report_invalid_dependency_expression(
    mock_error: Mock,
    mock_context_type: Mock,
) -> None:
    plugin_resolve(
        dependencies=[
            "familyos.documentation-invalid-constraint?",
        ],
        repository_name="official",
        repository_url="https://plugins.familyos.dev",
        repository_type="remote",
    )

    mock_context_type.assert_not_called()
    mock_error.assert_called_once()
