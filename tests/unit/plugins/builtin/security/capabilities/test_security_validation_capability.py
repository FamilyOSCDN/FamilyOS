from familyos_cli.plugins.builtin.security.capabilities.security_validation_capability import (
    SecurityValidationCapability,
)


def test_security_validation_capability_has_expected_identifier() -> None:
    capability = SecurityValidationCapability.create()

    assert str(capability.id) == "familyos.security.validation"


def test_security_validation_capability_has_security_metadata() -> None:
    capability = SecurityValidationCapability.create()

    assert capability.display_name == "Security Validation"
    assert capability.metadata["domain"] == "security"
    assert capability.metadata["version"] == "1.0.0"