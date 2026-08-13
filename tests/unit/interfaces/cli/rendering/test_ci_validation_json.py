"""Tests for deterministic canonical CI validation JSON."""

from familyos_cli.application.validation import (
    CiValidationResult,
    GateResult,
    ValidationStatus,
)
from familyos_cli.interfaces.cli.rendering.ci_validation_json import (
    CiValidationJsonRenderer,
)


def test_serialization_is_deterministic_and_newline_terminated() -> None:
    result = CiValidationResult(
        gates=(
            GateResult("dependency-freshness", ValidationStatus.PASSED, 0),
            GateResult("dependency-consistency", ValidationStatus.PASSED, 0),
        ),
    )
    renderer = CiValidationJsonRenderer()

    first = renderer.render(result)
    second = renderer.render(result)

    assert first == second
    assert first.endswith("\n")
    assert '"schema_version": "1.0.0"' in first
    assert '"status": "passed"' in first
