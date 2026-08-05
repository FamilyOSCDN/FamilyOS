from familyos_cli.plugins.builtin.education.capabilities.education_course_capability import (
    EducationCourseCapability,
)


def test_education_course_capability_creation() -> None:
    capability = (
        EducationCourseCapability.create()
    )

    assert str(capability.id) == (
        "familyos.education.course"
    )

    assert capability.display_name == (
        "Education Course"
    )

    assert (
        "course management"
        in capability.description
    )
