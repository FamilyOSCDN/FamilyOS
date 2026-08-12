"""Tests for the plugin resolution use case."""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from familyos_cli.application.use_cases.resolve_plugins import (
    ResolvePluginsUseCase,
)
from familyos_cli.plugins.ecosystem.resolution import (
    ResolutionPlan,
)


def test_should_resolve_dependency_without_constraint() -> None:
    """Use case should parse a canonical plugin dependency."""

    pipeline = Mock()
    pipeline.resolve.return_value = ResolutionPlan()

    use_case = ResolvePluginsUseCase(
        pipeline=pipeline,
    )

    result = use_case.execute(
        dependencies=[
            "familyos.documentation",
        ],
        repository_name="official",
        repository_url="https://plugins.familyos.dev",
        repository_type="remote",
    )

    assert result is pipeline.resolve.return_value

    pipeline.resolve.assert_called_once()

    call = pipeline.resolve.call_args

    repository = call.kwargs["repository"]
    dependencies = call.kwargs["dependencies"]

    assert repository.name == "official"
    assert repository.url == "https://plugins.familyos.dev"
    assert repository.repository_type == "remote"

    assert len(dependencies) == 1

    dependency = dependencies[0]

    assert dependency.plugin_id == "familyos.documentation"
    assert dependency.name == "familyos.documentation"
    assert dependency.constraint_set is None


def test_should_preserve_dependency_constraint_set() -> None:
    """Use case should parse version constraints."""

    pipeline = Mock()
    pipeline.resolve.return_value = ResolutionPlan()

    use_case = ResolvePluginsUseCase(
        pipeline=pipeline,
    )

    use_case.execute(
        dependencies=[
            "familyos.calendar>=1.0.0,<2.0.0",
        ],
        repository_name="official",
        repository_url="https://plugins.familyos.dev",
        repository_type="remote",
    )

    dependencies = (
        pipeline.resolve.call_args.kwargs[
            "dependencies"
        ]
    )

    assert len(dependencies) == 1

    dependency = dependencies[0]

    assert dependency.plugin_id == "familyos.calendar"
    assert dependency.name == "familyos.calendar"
    assert dependency.constraint_set is not None
    assert str(dependency.constraint_set) == ">=1.0.0,<2.0.0"


def test_should_reject_short_plugin_identifier() -> None:
    """Use case should reject noncanonical Plugin Identifiers."""

    pipeline = Mock()

    use_case = ResolvePluginsUseCase(
        pipeline=pipeline,
    )

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        use_case.execute(
            dependencies=[
                "documentation",
            ],
            repository_name="official",
            repository_url="https://plugins.familyos.dev",
            repository_type="remote",
        )

    pipeline.resolve.assert_not_called()


def test_should_reject_unknown_short_plugin_identifier() -> None:
    """Unknown short identifiers must not bypass canonical validation."""

    pipeline = Mock()

    use_case = ResolvePluginsUseCase(
        pipeline=pipeline,
    )

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        use_case.execute(
            dependencies=[
                "notification",
            ],
            repository_name="official",
            repository_url="https://plugins.familyos.dev",
            repository_type="remote",
        )

    pipeline.resolve.assert_not_called()


def test_should_reject_invalid_constraint() -> None:
    """Malformed version constraints should fail before resolution."""

    pipeline = Mock()

    use_case = ResolvePluginsUseCase(
        pipeline=pipeline,
    )

    with pytest.raises(ValueError):
        use_case.execute(
            dependencies=[
                "familyos.documentation-invalid-constraint?",
            ],
            repository_name="official",
            repository_url="https://plugins.familyos.dev",
            repository_type="remote",
        )

    pipeline.resolve.assert_not_called()
