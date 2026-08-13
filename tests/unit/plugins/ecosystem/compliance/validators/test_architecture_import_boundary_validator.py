"""Tests for the PLUGIN-ARCH-001 validator."""

from pathlib import Path

from familyos_cli.plugins.ecosystem.compliance.rule_outcome import RuleOutcome
from familyos_cli.plugins.ecosystem.compliance.validators.architecture_import_boundary_validator import (
    ArchitectureImportBoundaryValidator,
)
from tests.unit.plugins.ecosystem.compliance.validators.validator_fixtures import (
    make_context,
)


def test_not_applicable_when_no_domain_subpackage(tmp_path: Path) -> None:
    """NOT_APPLICABLE when the plugin has no domain/ subpackage."""

    context = make_context(tmp_path, manifest={})
    validator = ArchitectureImportBoundaryValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.NOT_APPLICABLE


def test_pass_when_domain_imports_are_clean(tmp_path: Path) -> None:
    """PASS when domain/ files do not import outer architectural layers."""

    domain_dir = tmp_path / "domain"
    domain_dir.mkdir()
    (domain_dir / "model.py").write_text(
        "from dataclasses import dataclass\n",
        encoding="utf-8",
    )

    context = make_context(tmp_path, manifest={})
    validator = ArchitectureImportBoundaryValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.PASS


def test_fail_when_domain_imports_interfaces(tmp_path: Path) -> None:
    """FAIL when a domain/ file imports familyos_cli.interfaces."""

    domain_dir = tmp_path / "domain"
    domain_dir.mkdir()
    (domain_dir / "model.py").write_text(
        "from familyos_cli.interfaces.cli.output import Output\n",
        encoding="utf-8",
    )

    context = make_context(tmp_path, manifest={})
    validator = ArchitectureImportBoundaryValidator()

    run_result = validator.validate(context)

    assert validator.check(run_result.evidence) is RuleOutcome.FAIL
