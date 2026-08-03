from familyos_cli.plugins.builtin.health.validation.health_validation_result import (
    HealthValidationResult,
)


def test_success_result_is_valid() -> None:
    result = HealthValidationResult.success()

    assert result.valid
    assert result.errors == ()


def test_failure_result_contains_errors() -> None:
    result = HealthValidationResult.failure(
        (
            "Invalid health record.",
        ),
    )

    assert not result.valid
    assert result.errors == (
        "Invalid health record.",
    )
