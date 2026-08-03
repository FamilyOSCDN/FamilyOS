import pytest

from familyos_cli.plugins.builtin.health.metrics.health_metric import (
    HealthMetric,
)


def test_health_metric_can_be_created() -> None:
    metric = HealthMetric(
        id="metric-001",
        record_id="record-001",
        metric_type="weight",
        value="75",
        unit="kg",
        recorded_at="2026-08-03",
    )

    assert metric.id == "metric-001"
    assert metric.record_id == "record-001"
    assert metric.metric_type == "weight"
    assert metric.value == "75"
    assert metric.unit == "kg"


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


def test_health_metric_requires_id() -> None:
    with pytest.raises(
        ValueError,
        match="Health metric id cannot be empty.",
    ):
        HealthMetric(
            id="",
            record_id="record-001",
            metric_type="weight",
            value="75",
            unit="kg",
            recorded_at="2026-08-03",
        )


def test_health_metric_requires_record_id() -> None:
    with pytest.raises(
        ValueError,
        match="Health metric record id cannot be empty.",
    ):
        HealthMetric(
            id="metric-001",
            record_id="",
            metric_type="weight",
            value="75",
            unit="kg",
            recorded_at="2026-08-03",
        )
