import pytest

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
    assert learner.education_level == "primary"


@pytest.mark.parametrize(
    "learner_id",
    (
        "",
        "   ",
    ),
)
def test_learner_rejects_empty_id(
    learner_id: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="Learner id cannot be empty.",
    ):
        Learner(
            id=learner_id,
            name="Alice",
            education_level="primary",
        )


@pytest.mark.parametrize(
    "name",
    (
        "",
        "   ",
    ),
)
def test_learner_rejects_empty_name(
    name: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="Learner name cannot be empty.",
    ):
        Learner(
            id="learner-001",
            name=name,
            education_level="primary",
        )


@pytest.mark.parametrize(
    "education_level",
    (
        "",
        "   ",
    ),
)
def test_learner_rejects_empty_education_level(
    education_level: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "Learner education level "
            "cannot be empty."
        ),
    ):
        Learner(
            id="learner-001",
            name="Alice",
            education_level=education_level,
        )
