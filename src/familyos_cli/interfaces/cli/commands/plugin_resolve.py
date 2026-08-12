"""Plugin resolution command."""

from __future__ import annotations

from familyos_cli.interfaces.cli.context import CommandContext
from familyos_cli.interfaces.cli.output import Output
from familyos_cli.plugins.ecosystem.diagnostics import (
    DiagnosticCliRenderer,
    DiagnosticPipeline,
    ResolutionExplainer,
)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def plugin_resolve(
    *,
    dependencies: list[str],
    repository_name: str,
    repository_url: str,
    repository_type: str,
) -> int:
    """Resolve plugin dependencies from a repository.

    Returns:
        Zero when resolution succeeds and one when an expected
        input or resolution failure is presented to the user.
    """

    context = CommandContext()

    try:
        plan = context.resolve_plugins.execute(
            dependencies=dependencies,
            repository_name=repository_name,
            repository_url=repository_url,
            repository_type=repository_type,
        )
    except ValueError as error:
        Output.error(
            str(error),
        )

        return EXIT_FAILURE

    diagnostic_report = DiagnosticPipeline().build(
        plan,
    )

    if not diagnostic_report.is_empty():
        explainer = ResolutionExplainer()
        renderer = DiagnosticCliRenderer()

        rendered_diagnostics = [
            renderer.render(
                explainer.explain(
                    diagnostic,
                ),
            )
            for diagnostic in diagnostic_report.diagnostics
        ]

        for rendered_diagnostic in rendered_diagnostics:
            Output.diagnostic(
                rendered_diagnostic,
                styled=True,
            )

        return EXIT_FAILURE

    Output.success(
        (
            "Plugin resolution completed successfully: "
            f"{len(plan.ordered_packages)} package(s) selected."
        ),
    )

    return EXIT_SUCCESS
