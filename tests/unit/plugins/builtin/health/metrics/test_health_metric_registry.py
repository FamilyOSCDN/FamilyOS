import pytest

from familyos_cli.plugins.builtin.health.metrics.health_metric import (
    HealthMetric,
)
from familyos_cli.plugins.builtin.health.metrics.health_metric_registry import (
    HealthMetricRegistry,
)


def create_metric() -> HealthMetric:
    return HealthMetric(
        id="metric-001",
        record_id="record-001",
        metric_type="weight",
        value="75",
        unit="kg",
        recorded_at="2026-08-03",
    )


def test_registry_registers_metric() -> None:
    registry = HealthMetricRegistry()

    metric = create_metric()

    registry.register(
        metric,
    )

    assert registry.contains(
        "metric-001",
    )


def test_registry_returns_metric() -> None:
    registry = HealthMetricRegistry()

    metric = create_metric()

    registry.register(
        metric,
    )

    assert registry.get(
        "metric-001",
    ) == metric


def test_registry_rejects_duplicate_metric() -> None:
    registry = HealthMetricRegistry()

    metric = create_metric()

    registry.register(
        metric,
    )

    with pytest.raises(
        ValueError,
        match="already registered",
    ):
        registry.register(
            metric,
        )
