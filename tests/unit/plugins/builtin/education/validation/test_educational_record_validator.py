"""Tests for EducationalRecordValidator."""

from familyos_cli.plugins.builtin.education.models.educational_record import (
    EducationalRecord,
)
from familyos_cli.plugins.builtin.education.validation.educational_record_validator import (
    EducationalRecordValidator,
)


def test_educational_record_validator_accepts_valid_record() -> None:
    """Valid educational records should pass validation."""

    record = EducationalRecord(
        id="record-001",
        learner_id="learner-001",
        course_id="course-001",
        result="completed",
    )

    validator = EducationalRecordValidator()

    assert validator.validate(
        record,
    ) is True


def test_educational_record_validator_accepts_valid_result() -> None:
    """Alternative non-empty educational results should pass validation."""

    record = EducationalRecord(
        id="record-001",
        learner_id="learner-001",
        course_id="course-001",
        result="in-progress",
    )

    validator = EducationalRecordValidator()

    assert validator.validate(
        record,
    ) is True
