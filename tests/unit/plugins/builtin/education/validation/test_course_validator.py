from familyos_cli.plugins.builtin.education.models.course import (
    Course,
)
from familyos_cli.plugins.builtin.education.validation.course_validator import (
    CourseValidator,
)


def test_course_validator_accepts_valid_course() -> None:
    course = Course(
        id="course-001",
        title="Mathematics",
        description="Basic mathematics",
        category="science",
    )

    validator = CourseValidator()

    assert validator.validate(
        course,
    ) is True


def test_course_validator_rejects_invalid_business_state() -> None:
    course = Course(
        id="course-001",
        title="   ",
        description="Basic mathematics",
        category="science",
    )

    validator = CourseValidator()

    assert validator.validate(
        course,
    ) is False
