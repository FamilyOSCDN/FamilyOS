"""Tests for HealthMetric."""

import pytest

from familyos_cli.plugins.builtin.health.metrics.health_metric import (
    HealthMetric,
)


def create_metric(
    **overrides: str,
) -> HealthMetric:
    """Create a health metric for tests."""

    values = {
        "id": "metric-001",
        "record_id": "record-001",
        "metric_type": "weight",
        "value": "75",
        "unit": "kg",
        "recorded_at": "2026-08-03",
    }
    values.update(
        overrides,
    )

    return HealthMetric(
        id=values["id"],
        record_id=values["record_id"],
        metric_type=values["metric_type"],
        value=values["value"],
        unit=values["unit"],
        recorded_at=values["recorded_at"],
    )


def test_health_metric_can_be_created() -> None:
    metric = create_metric()

    assert metric.id == "metric-001"
    assert metric.record_id == "record-001"
    assert metric.metric_type == "weight"
    assert metric.value == "75"
    assert metric.unit == "kg"
    assert metric.recorded_at == "2026-08-03"


def test_health_metric_supports_metadata() -> None:
    metric = HealthMetric(
        id="metric-001",
        record_id="record-001",
        metric_type="temperature",
        value="36.8",
        unit="celsius",
        recorded_at="2026-08-03",
        metadata={
            "source": "device",
        },
    )

    assert metric.metadata["source"] == "device"


@pytest.mark.parametrize(
    ("field", "message"),
    [
        (
            "id",
            "Health metric id cannot be empty.",
        ),
        (
            "record_id",
            "Health metric record id cannot be empty.",
        ),
        (
            "metric_type",
            "Health metric type cannot be empty.",
        ),
        (
            "value",
            "Health metric value cannot be empty.",
        ),
        (
            "unit",
            "Health metric unit cannot be empty.",
        ),
        (
            "recorded_at",
            "Health metric date cannot be empty.",
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
def test_health_metric_rejects_empty_required_fields(
    field: str,
    message: str,
    invalid_value: str,
) -> None:
    with pytest.raises(
        ValueError,
        match=message,
    ):
        create_metric(
            **{
                field: invalid_value,
            },
        )
