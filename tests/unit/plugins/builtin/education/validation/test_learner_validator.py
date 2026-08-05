from familyos_cli.plugins.builtin.education.models.learner import (
    Learner,
)
from familyos_cli.plugins.builtin.education.validation.learner_validator import (
    LearnerValidator,
)


def test_learner_validator_accepts_valid_learner() -> None:
    learner = Learner(
        id="learner-001",
        name="Alice",
        education_level="primary",
    )

    validator = LearnerValidator()

    assert validator.validate(
        learner,
    ) is True


def test_learner_validator_rejects_invalid_business_state() -> None:
    learner = Learner(
        id="learner-001",
        name="   ",
        education_level="primary",
    )

    validator = LearnerValidator()

    assert validator.validate(
        learner,
    ) is False
