"""Tests for EducationLevel."""

from familyos_cli.plugins.builtin.education.domain.education_level import (
    EducationLevel,
)


def test_education_levels_exist() -> None:
    """Education levels are available."""

    assert EducationLevel.BASIC.value == "basic"
    assert EducationLevel.STANDARD.value == "standard"
    assert EducationLevel.ADVANCED.value == "advanced"
    assert EducationLevel.CRITICAL.value == "critical"
