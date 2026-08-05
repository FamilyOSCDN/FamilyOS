from pytest import raises

from familyos_cli.plugins.builtin.education.models.learner import (
    Learner,
)


def test_learner_creation() -> None:
    learner = Learner(
        id="learner-001",
        name="Alice",
        education_level="primary",
    )

    assert learner.id == "learner-001"

    assert learner.name == "Alice"

    assert (
        learner.education_level
        == "primary"
    )


def test_learner_rejects_empty_id() -> None:
    with raises(
        ValueError,
        match="Learner id cannot be empty.",
    ):
        Learner(
            id="",
            name="Alice",
            education_level="primary",
        )


def test_learner_rejects_empty_name() -> None:
    with raises(
        ValueError,
        match="Learner name cannot be empty.",
    ):
        Learner(
            id="learner-001",
            name="",
            education_level="primary",
        )


def test_learner_rejects_empty_education_level() -> None:
    with raises(
        ValueError,
        match=(
            "Learner education level "
            "cannot be empty."
        ),
    ):
        Learner(
            id="learner-001",
            name="Alice",
            education_level="",
        )
