"""Tests for LearnerValidator."""

from familyos_cli.plugins.builtin.education.models.learner import (
    Learner,
)
from familyos_cli.plugins.builtin.education.validation.learner_validator import (
    LearnerValidator,
)


def test_learner_validator_accepts_valid_learner() -> None:
    """Valid learner domain objects should pass validation."""

    learner = Learner(
        id="learner-001",
        name="Alice",
        education_level="primary",
    )

    validator = LearnerValidator()

    assert validator.validate(
        learner,
    ) is True


def test_learner_validator_accepts_different_education_level() -> None:
    """Valid education level values should pass validation."""

    learner = Learner(
        id="learner-001",
        name="Alice",
        education_level="secondary",
    )

    validator = LearnerValidator()

    assert validator.validate(
        learner,
    ) is True
