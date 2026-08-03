import pytest

from familyos_cli.plugins.builtin.health.records.health_record import (
    HealthRecord,
)
from familyos_cli.plugins.builtin.health.validation.health_validator import (
    HealthValidator,
)


def create_record() -> HealthRecord:
    return HealthRecord(
        id="record-001",
        profile_id="health-001",
        record_type="consultation",
        recorded_at="2026-08-03",
    )


def test_validator_accepts_valid_record() -> None:
    validator = HealthValidator()

    result = validator.validate_record(
        create_record(),
    )

    assert result.valid
    assert result.errors == ()


def test_validator_result_can_report_failure() -> None:
    result = HealthValidator().validate_record(
        create_record(),
    )

    assert result.valid


def test_health_record_structure_rejects_invalid_type() -> None:
    with pytest.raises(
        ValueError,
        match="Health record type cannot be empty.",
    ):
        HealthRecord(
            id="record-001",
            profile_id="health-001",
            record_type="",
            recorded_at="2026-08-03",
        )
