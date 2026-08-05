from pytest import raises

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


def test_educational_record_rejects_empty_id() -> None:
    with raises(
        ValueError,
        match=(
            "EducationalRecord id "
            "cannot be empty."
        ),
    ):
        EducationalRecord(
            id="",
            learner_id="learner-001",
            course_id="course-001",
            result="completed",
        )


def test_educational_record_rejects_empty_learner_id() -> None:
    with raises(
        ValueError,
        match=(
            "EducationalRecord learner id "
            "cannot be empty."
        ),
    ):
        EducationalRecord(
            id="record-001",
            learner_id="",
            course_id="course-001",
            result="completed",
        )


def test_educational_record_rejects_empty_course_id() -> None:
    with raises(
        ValueError,
        match=(
            "EducationalRecord course id "
            "cannot be empty."
        ),
    ):
        EducationalRecord(
            id="record-001",
            learner_id="learner-001",
            course_id="",
            result="completed",
        )


def test_educational_record_rejects_empty_result() -> None:
    with raises(
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
            result="",
        )
