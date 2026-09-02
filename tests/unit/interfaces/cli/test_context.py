"""Tests for CLI command context."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock

from familyos_cli.interfaces.cli.context import CommandContext


def test_should_initialize_command_context() -> None:
    """Command context should expose core application capabilities."""

    context = CommandContext()

    assert context.create_project is not None
    assert context.create_artifact is not None
    assert context.resolve_plugins is not None


def test_should_expose_plugin_resolution_use_case_from_container() -> None:
    """Plugin resolution should cross the CLI boundary as a use case."""

    container = Mock()

    resolve_plugins = Mock()

    container.resolve_plugins_use_case.return_value = resolve_plugins

    context = CommandContext(
        container=container,
    )

    assert context.resolve_plugins is resolve_plugins

    container.resolve_plugins_use_case.assert_called_once_with()


def test_command_context_propagates_explicit_project_root(
    tmp_path: Path,
) -> None:
    """CLI composition preserves the explicitly selected repository root."""
    context = CommandContext(project_root=tmp_path)

    assert context.project_root == tmp_path.resolve()


def test_quality_execution_is_exposed_and_cached(tmp_path: Path) -> None:
    from familyos_cli.application.quality.quality_execution_service import (
        QualityExecutionService,
    )

    context = CommandContext(project_root=tmp_path)
    first = context.quality_execution
    second = context.quality_execution
    assert isinstance(first, QualityExecutionService)
    assert second is first
