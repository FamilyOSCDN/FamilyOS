"""Shared dependency expression parsing for compliance validators.

Mirrors the parsing behavior of
familyos_cli.application.use_cases.resolve_plugins.ResolvePluginsUseCase,
which is not reused directly because that logic is a private
implementation detail (module-level regex plus a private static method)
of an unrelated use case.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from familyos_cli.plugins.ecosystem.resolution import ConstraintSet
from familyos_cli.plugins.identity import PluginId

_DEPENDENCY_PATTERN = re.compile(
    r"^(?P<plugin_id>[A-Za-z0-9][A-Za-z0-9._-]*)(?P<constraint>.*)$",
)


@dataclass(frozen=True, slots=True)
class ParsedDependency:
    """Represent a successfully parsed plugin dependency expression."""

    plugin_id: str
    constraint: str


def parse_dependency_expression(value: str) -> ParsedDependency:
    """Parse a plugin dependency expression.

    Raises:
        ValueError: If the expression is malformed, the plugin id is not
            canonical, or the constraint (when present) is invalid.
    """

    normalized_value = value.strip()

    match = _DEPENDENCY_PATTERN.fullmatch(normalized_value)

    if match is None:
        raise ValueError(f"Invalid plugin dependency: {value!r}.")

    plugin_id = PluginId(match.group("plugin_id")).value

    constraint_value = match.group("constraint").strip()

    if constraint_value:
        ConstraintSet.parse(constraint_value)

    return ParsedDependency(plugin_id=plugin_id, constraint=constraint_value)
