from familyos_cli.plugins.builtin.security.capabilities.security_policy_capability import (
    SecurityPolicyCapability,
)


def test_security_policy_capability_has_expected_identifier() -> None:
    capability = SecurityPolicyCapability.create()

    assert str(capability.id) == "familyos.security.policy"


def test_security_policy_capability_has_security_metadata() -> None:
    capability = SecurityPolicyCapability.create()

    assert capability.display_name == "Security Policy"
    assert capability.metadata["domain"] == "security"
    assert capability.metadata["version"] == "1.0.0"