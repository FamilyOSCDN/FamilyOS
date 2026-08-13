import pytest

from familyos_cli.plugins.builtin.education.models.educational_record import (
    EducationalRecord,
)


def test_educational_record_creation() -> None:
    record = EducationalRecord(
        id="record-001",
        learner_id="learner-001",
        course_id="course-001",
        result="completed",
    )

    assert record.id == "record-001"
    assert record.learner_id == "learner-001"
    assert record.course_id == "course-001"
    assert record.result == "completed"


@pytest.mark.parametrize(
    "record_id",
    (
        "",
        "   ",
    ),
)
def test_educational_record_rejects_empty_id(
    record_id: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "EducationalRecord id "
            "cannot be empty."
        ),
    ):
        EducationalRecord(
            id=record_id,
            learner_id="learner-001",
            course_id="course-001",
            result="completed",
        )


@pytest.mark.parametrize(
    "learner_id",
    (
        "",
        "   ",
    ),
)
def test_educational_record_rejects_empty_learner_id(
    learner_id: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "EducationalRecord learner id "
            "cannot be empty."
        ),
    ):
        EducationalRecord(
            id="record-001",
            learner_id=learner_id,
            course_id="course-001",
            result="completed",
        )


@pytest.mark.parametrize(
    "course_id",
    (
        "",
        "   ",
    ),
)
def test_educational_record_rejects_empty_course_id(
    course_id: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "EducationalRecord course id "
            "cannot be empty."
        ),
    ):
        EducationalRecord(
            id="record-001",
            learner_id="learner-001",
            course_id=course_id,
            result="completed",
        )


@pytest.mark.parametrize(
    "result",
    (
        "",
        "   ",
    ),
)
def test_educational_record_rejects_empty_result(
    result: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=(
            "EducationalRecord result "
            "cannot be empty."
        ),
    ):
        EducationalRecord(
            id="record-001",
            learner_id="learner-001",
            course_id="course-001",
            result=result,
        )
