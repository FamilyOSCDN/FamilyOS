"""Tests for HealthRecord."""

import pytest

from familyos_cli.plugins.builtin.health.records.health_record import (
    HealthRecord,
)


def create_record(
    **overrides: str,
) -> HealthRecord:
    """Create a health record for tests."""

    values = {
        "id": "record-001",
        "profile_id": "health-001",
        "record_type": "consultation",
        "recorded_at": "2026-08-03",
    }
    values.update(
        overrides,
    )

    return HealthRecord(
        id=values["id"],
        profile_id=values["profile_id"],
        record_type=values["record_type"],
        recorded_at=values["recorded_at"],
    )


def test_health_record_can_be_created() -> None:
    record = create_record()

    assert record.id == "record-001"
    assert record.profile_id == "health-001"
    assert record.record_type == "consultation"
    assert record.recorded_at == "2026-08-03"


def test_health_record_supports_metadata() -> None:
    record = HealthRecord(
        id="record-001",
        profile_id="health-001",
        record_type="measurement",
        recorded_at="2026-08-03",
        metadata={
            "source": "doctor",
        },
    )

    assert record.metadata["source"] == "doctor"


@pytest.mark.parametrize(
    ("field", "message"),
    [
        (
            "id",
            "Health record id cannot be empty.",
        ),
        (
            "profile_id",
            "Health record profile id cannot be empty.",
        ),
        (
            "record_type",
            "Health record type cannot be empty.",
        ),
        (
            "recorded_at",
            "Health record date cannot be empty.",
        ),
    ],
)
@pytest.mark.parametrize(
    "invalid_value",
    [
        "",
        "   ",
    ],
)
def test_health_record_rejects_empty_required_fields(
    field: str,
    message: str,
    invalid_value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=message,
    ):
        create_record(
            **{
                field: invalid_value,
            },
        )
