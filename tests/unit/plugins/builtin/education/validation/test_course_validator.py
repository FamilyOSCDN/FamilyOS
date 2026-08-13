"""Tests for CourseValidator."""

from familyos_cli.plugins.builtin.education.models.course import (
    Course,
)
from familyos_cli.plugins.builtin.education.validation.course_validator import (
    CourseValidator,
)


def test_course_validator_accepts_valid_course() -> None:
    """Valid course domain objects should pass validation."""

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


def test_course_validator_accepts_course_without_description() -> None:
    """Optional course descriptions should not affect validation."""

    course = Course(
        id="course-001",
        title="Mathematics",
        description="",
        category="science",
    )

    validator = CourseValidator()

    assert validator.validate(
        course,
    ) is True
