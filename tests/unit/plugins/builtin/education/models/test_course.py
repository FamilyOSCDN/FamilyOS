from pytest import raises

from familyos_cli.plugins.builtin.education.models.course import (
    Course,
)


def test_course_creation() -> None:
    course = Course(
        id="course-001",
        title="Mathematics",
        description="Basic mathematics",
        category="science",
    )

    assert course.id == "course-001"

    assert course.title == "Mathematics"

    assert course.category == "science"


def test_course_rejects_empty_id() -> None:
    with raises(
        ValueError,
        match="Course id cannot be empty.",
    ):
        Course(
            id="",
            title="Math",
            description="Basic",
            category="science",
        )


def test_course_rejects_empty_title() -> None:
    with raises(
        ValueError,
        match="Course title cannot be empty.",
    ):
        Course(
            id="course-001",
            title="",
            description="Basic",
            category="science",
        )


def test_course_rejects_empty_category() -> None:
    with raises(
        ValueError,
        match="Course category cannot be empty.",
    ):
        Course(
            id="course-001",
            title="Math",
            description="Basic",
            category="",
        )
