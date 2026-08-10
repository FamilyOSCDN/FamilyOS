"""Plugin resolution command."""

from __future__ import annotations

import re

from familyos_cli.interfaces.cli.context import CommandContext
from familyos_cli.interfaces.cli.output import Output
from familyos_cli.plugins.ecosystem.diagnostics import (
    DiagnosticCliRenderer,
    DiagnosticPipeline,
    ResolutionExplainer,
)
from familyos_cli.plugins.ecosystem.repository import PluginRepository
from familyos_cli.plugins.ecosystem.resolution import (
    ConstraintSet,
    PluginDependency,
)

_DEPENDENCY_PATTERN = re.compile(
    r"^(?P<name>[A-Za-z0-9][A-Za-z0-9._-]*)(?P<constraint>.*)$",
)


def parse_plugin_dependency(
    value: str,
) -> PluginDependency:
    """Parse a CLI dependency expression.

    Supported examples include:

    - ``documentation``
    - ``documentation>=1.0.0``
    - ``security^2.0.0``
    - ``calendar>=1.0.0,<2.0.0``

    Args:
        value: Dependency expression supplied by the user.

    Returns:
        Parsed plugin dependency.

    Raises:
        ValueError: If the dependency expression is invalid.
    """

    normalized_value = value.strip()

    match = _DEPENDENCY_PATTERN.fullmatch(
        normalized_value,
    )

    if match is None:
        raise ValueError(
            f"Invalid plugin dependency: {value!r}.",
        )

    plugin_id = match.group("name")
    constraint_value = match.group("constraint").strip()

    if not constraint_value:
        return PluginDependency(
            name=plugin_id,
        )

    return PluginDependency(
        name=plugin_id,
        constraint_set=ConstraintSet.parse(
            constraint_value,
        ),
    )


def plugin_resolve(
    *,
    dependencies: list[str],
    repository_name: str,
    repository_url: str,
    repository_type: str,
) -> None:
    """Resolve plugin dependencies from a repository."""

    try:
        parsed_dependencies = [
            parse_plugin_dependency(
                dependency,
            )
            for dependency in dependencies
        ]
    except ValueError as error:
        Output.error(
            str(error),
        )
        return

    repository = PluginRepository(
        name=repository_name,
        url=repository_url,
        repository_type=repository_type,
    )

    context = CommandContext()

    plan = context.plugin_resolution_pipeline.resolve(
        repository=repository,
        dependencies=parsed_dependencies,
    )

    diagnostic_report = DiagnosticPipeline().build(
        plan,
    )

    if not diagnostic_report.is_empty():
        explainer = ResolutionExplainer()
        renderer = DiagnosticCliRenderer()

        for diagnostic in diagnostic_report.diagnostics:
            explanation = explainer.explain(
                diagnostic,
            )

            rendered_diagnostic = renderer.render(
                explanation,
            )

            Output.diagnostic(
                rendered_diagnostic,
            )

        return

    Output.success(
        (
            "Plugin resolution completed successfully: "
            f"{len(plan.ordered_packages)} package(s) selected."
        ),
    )
