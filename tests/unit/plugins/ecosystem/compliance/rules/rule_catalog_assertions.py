"""Shared consistency assertions for compliance rule catalog tests."""

from __future__ import annotations

import re

from familyos_cli.plugins.ecosystem.compliance.compliance_rule import (
    ComplianceRule,
)
from familyos_cli.plugins.ecosystem.compliance.validators.default_validator_registry import (
    build_default_validator_registry,
)

_RULE_ID_PATTERN = re.compile(r"^PLUGIN-[A-Z]+-\d{3}$")

_DEFAULT_VALIDATOR_REGISTRY = build_default_validator_registry()


def assert_rule_catalog_is_consistent(
    rules: tuple[ComplianceRule, ...],
) -> None:
    """Assert structural and cross-reference consistency for a rule set."""

    seen_ids: set[str] = set()

    for rule in rules:
        assert _RULE_ID_PATTERN.fullmatch(rule.id), rule.id
        assert rule.id not in seen_ids, f"duplicate rule id: {rule.id}"
        seen_ids.add(rule.id)

        assert rule.requirement.strip()
        assert rule.remediation.strip()
        assert rule.title.strip()
        assert rule.description.strip()
        assert rule.rationale.strip()

        assert rule.validator_id in _DEFAULT_VALIDATOR_REGISTRY.list(), (
            f"{rule.id} references unregistered validator "
            f"'{rule.validator_id}'"
        )
