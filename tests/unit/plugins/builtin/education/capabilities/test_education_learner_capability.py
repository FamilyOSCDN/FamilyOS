from familyos_cli.plugins.builtin.education.capabilities.education_learner_capability import (
    EducationLearnerCapability,
)


def test_education_learner_capability_creation() -> None:
    capability = (
        EducationLearnerCapability.create()
    )

    assert str(capability.id) == (
        "familyos.education.learner"
    )

    assert capability.display_name == (
        "Education Learner"
    )

    assert (
        "learner management"
        in capability.description
    )
