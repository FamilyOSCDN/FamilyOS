from familyos_cli.plugins.builtin.security.rules.security_rule import (
    SecurityRule,
)
from familyos_cli.plugins.builtin.security.validation.security_validation_result import (
    SecurityValidationResult,
)
from familyos_cli.plugins.builtin.security.validation.security_validator import (
    SecurityValidator,
)


def create_rule() -> SecurityRule:
    """Create a test security rule."""

    return SecurityRule(
        id="security.rule.password-policy",
        name="Password Policy Rule",
        version="1.0.0",
        severity="HIGH",
        description="Checks password requirements.",
    )


def test_security_validation_result_can_be_created() -> None:
    result = SecurityValidationResult(
        valid=True,
        message="Validation succeeded.",
    )

    assert result.valid is True
    assert result.message == (
        "Validation succeeded."
    )


def test_security_validator_returns_valid_result() -> None:
    validator = SecurityValidator()

    result = validator.validate(
        create_rule(),
    )

    assert result.valid is True


def test_security_validator_result_contains_rule_identifier() -> None:
    validator = SecurityValidator()

    result = validator.validate(
        create_rule(),
    )

    assert (
        "security.rule.password-policy"
        in result.message
    )
