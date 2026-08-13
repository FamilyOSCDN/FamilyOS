import pytest

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


@pytest.mark.parametrize(
    "course_id",
    (
        "",
        "   ",
    ),
)
def test_course_rejects_empty_id(
    course_id: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="Course id cannot be empty.",
    ):
        Course(
            id=course_id,
            title="Math",
            description="Basic",
            category="science",
        )


@pytest.mark.parametrize(
    "title",
    (
        "",
        "   ",
    ),
)
def test_course_rejects_empty_title(
    title: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="Course title cannot be empty.",
    ):
        Course(
            id="course-001",
            title=title,
            description="Basic",
            category="science",
        )


@pytest.mark.parametrize(
    "category",
    (
        "",
        "   ",
    ),
)
def test_course_rejects_empty_category(
    category: str,
) -> None:
    with pytest.raises(
        ValueError,
        match="Course category cannot be empty.",
    ):
        Course(
            id="course-001",
            title="Math",
            description="Basic",
            category=category,
        )
