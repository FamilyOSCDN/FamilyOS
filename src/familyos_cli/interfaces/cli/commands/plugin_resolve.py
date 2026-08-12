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
from familyos_cli.plugins.identity import PluginId

_DEPENDENCY_PATTERN = re.compile(
    r"^(?P<plugin_id>[A-Za-z0-9][A-Za-z0-9._-]*)(?P<constraint>.*)$",
)

EXIT_SUCCESS = 0
EXIT_FAILURE = 1


def parse_plugin_dependency(
    value: str,
) -> PluginDependency:
    """Parse a CLI dependency expression.

    Supported examples include:

    - ``familyos.documentation``
    - ``familyos.documentation>=1.0.0``
    - ``familyos.security^2.0.0``
    - ``familyos.calendar>=1.0.0,<2.0.0``

    Args:
        value: Dependency expression supplied by the user.

    Returns:
        Parsed plugin dependency.

    Raises:
        ValueError: If the dependency expression is invalid or if the
            Plugin Identifier is not canonical.
    """

    normalized_value = value.strip()

    match = _DEPENDENCY_PATTERN.fullmatch(
        normalized_value,
    )

    if match is None:
        raise ValueError(
            f"Invalid plugin dependency: {value!r}.",
        )

    plugin_id = match.group("plugin_id")

    # The CLI boundary requires canonical Plugin Identifiers.
    # Legacy aliases may be accepted by lower-level compatibility APIs,
    # but they must never enter the resolution pipeline through this CLI.
    canonical_plugin_id = PluginId(
        plugin_id,
    ).value

    constraint_value = match.group("constraint").strip()

    if not constraint_value:
        return PluginDependency(
            plugin_id=canonical_plugin_id,
        )

    return PluginDependency(
        plugin_id=canonical_plugin_id,
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
) -> int:
    """Resolve plugin dependencies from a repository.

    Returns:
        Zero when resolution succeeds and one when an expected
        input or resolution failure is presented to the user.
    """

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

        return EXIT_FAILURE

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

        rendered_diagnostics: list[str] = []

        for diagnostic in diagnostic_report.diagnostics:
            explanation = explainer.explain(
                diagnostic,
            )

            rendered_diagnostics.append(
                renderer.render(
                    explanation,
                ),
            )

        for rendered_diagnostic in rendered_diagnostics:
            Output.diagnostic(
                rendered_diagnostic,
            )

        return EXIT_FAILURE

    Output.success(
        (
            "Plugin resolution completed successfully: "
            f"{len(plan.ordered_packages)} package(s) selected."
        ),
    )

    return EXIT_SUCCESS
