"""Tests for the PLUGIN-DEP-002 validator."""

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.validators.dependency_no_self_dependency_validator import (
    DependencyNoSelfDependencyValidator,
)
from tests.unit.plugins.ecosystem.compliance.validators.validator_fixtures import (
    make_context,
)


def test_not_applicable_when_no_dependencies_declared(tmp_path: Path) -> None:
    """NOT_APPLICABLE when the manifest declares no dependencies."""

    context = make_context(tmp_path, manifest={})
    validator = DependencyNoSelfDependencyValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.NOT_APPLICABLE


def test_pass_when_no_self_dependency(tmp_path: Path) -> None:
    """PASS when no declared dependency references the plugin's own id."""

    context = make_context(
        tmp_path,
        manifest={"dependencies": ["familyos.documentation>=1.0.0"]},
        plugin_id="familyos.fixture",
    )
    validator = DependencyNoSelfDependencyValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.PASS


def test_fail_when_self_dependency_declared(tmp_path: Path) -> None:
    """FAIL when a declared dependency references the plugin's own id."""

    context = make_context(
        tmp_path,
        manifest={"dependencies": ["familyos.fixture>=1.0.0"]},
        plugin_id="familyos.fixture",
    )
    validator = DependencyNoSelfDependencyValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.FAIL
