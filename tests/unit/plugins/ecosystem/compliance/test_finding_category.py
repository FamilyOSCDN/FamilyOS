"""Tests for compliance finding categories."""

from familyos_cli.plugins.ecosystem.compliance.finding_category import (
    FindingCategory,
)


def test_finding_category_values() -> None:
    """Finding categories expose stable serialized values."""

    assert FindingCategory.VIOLATION.value == "violation"
    assert FindingCategory.INCOMPLETE.value == "incomplete"
    assert FindingCategory.VALIDATION_ERROR.value == "validation_error"
    assert FindingCategory.GOVERNANCE.value == "governance"
    assert FindingCategory.ADVISORY.value == "advisory"
