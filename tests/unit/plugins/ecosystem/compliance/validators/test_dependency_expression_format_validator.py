"""Tests for the PLUGIN-DEP-001 validator."""

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.validators.dependency_expression_format_validator import (
    DependencyExpressionFormatValidator,
)
from tests.unit.plugins.ecosystem.compliance.validators.validator_fixtures import (
    make_context,
)


def test_not_applicable_when_no_dependencies_declared(tmp_path: Path) -> None:
    """NOT_APPLICABLE when the manifest declares no dependencies."""

    context = make_context(tmp_path, manifest={})
    validator = DependencyExpressionFormatValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.NOT_APPLICABLE


def test_pass_for_well_formed_dependencies(tmp_path: Path) -> None:
    """PASS when every declared dependency expression is well-formed."""

    context = make_context(
        tmp_path,
        manifest={"dependencies": ["familyos.documentation>=1.0.0"]},
    )
    validator = DependencyExpressionFormatValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.PASS


def test_fail_for_malformed_dependency(tmp_path: Path) -> None:
    """FAIL when a declared dependency expression is malformed."""

    context = make_context(
        tmp_path,
        manifest={"dependencies": ["!!!not-valid!!!"]},
    )
    validator = DependencyExpressionFormatValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.FAIL
