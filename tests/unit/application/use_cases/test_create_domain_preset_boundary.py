"""Tests for the CreateDomain preset boundary."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import Mock

from familyos_cli.application.use_cases.create_domain import (
    CreateDomainUseCase,
)
from familyos_cli.domain.generation.generation_preset_id import (
    GenerationPresetId,
)
from familyos_cli.domain.generation.generation_request import (
    GenerationRequest,
)


def test_create_domain_normalizes_string_preset_before_request_factory() -> None:
    """Primitive interface presets should become domain preset identifiers."""

    pipeline = Mock()

    get_specification = Mock()
    get_specification.execute.return_value = None

    request_factory = Mock()
    request_factory.create.return_value = GenerationRequest(
        domain_name="Person",
        recipe_name="full_domain_documentation",
    )

    use_case = CreateDomainUseCase(
        pipeline=pipeline,
        get_specification=get_specification,
        request_factory=request_factory,
    )

    result = use_case.execute(
        domain_name="Person",
        destination=Path("."),
        preset="complete",
    )

    assert result is None

    request_factory.create.assert_called_once()

    preset = request_factory.create.call_args.kwargs[
        "preset"
    ]

    assert isinstance(
        preset,
        GenerationPresetId,
    )

    assert preset.value == "complete"


def test_create_domain_preserves_normalized_preset_identifier() -> None:
    """Already normalized preset identifiers should remain unchanged."""

    pipeline = Mock()

    get_specification = Mock()
    get_specification.execute.return_value = None

    request_factory = Mock()
    request_factory.create.return_value = GenerationRequest(
        domain_name="Person",
        recipe_name="full_domain_documentation",
    )

    use_case = CreateDomainUseCase(
        pipeline=pipeline,
        get_specification=get_specification,
        request_factory=request_factory,
    )

    preset = GenerationPresetId(
        "complete",
    )

    result = use_case.execute(
        domain_name="Person",
        destination=Path("."),
        preset=preset,
    )

    assert result is None

    request_factory.create.assert_called_once_with(
        domain_name="Person",
        recipe_name=None,
        preset=preset,
    )
