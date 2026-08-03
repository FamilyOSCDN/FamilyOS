"""Health metric registry."""

from __future__ import annotations

from familyos_cli.plugins.builtin.health.metrics.health_metric import (
    HealthMetric,
)


class HealthMetricRegistry:
    """Registry of health metrics."""

    def __init__(
        self,
    ) -> None:
        """Initialize registry."""

        self._metrics: dict[str, HealthMetric] = {}

    def register(
        self,
        metric: HealthMetric,
    ) -> None:
        """Register health metric."""

        if metric.id in self._metrics:
            raise ValueError(
                f"Health metric '{metric.id}' already registered.",
            )

        self._metrics[
            metric.id
        ] = metric

    def get(
        self,
        metric_id: str,
    ) -> HealthMetric:
        """Return health metric."""

        try:
            return self._metrics[
                metric_id
            ]
        except KeyError as error:
            raise ValueError(
                f"Health metric '{metric_id}' not found.",
            ) from error

    def contains(
        self,
        metric_id: str,
    ) -> bool:
        """Return whether metric exists."""

        return metric_id in self._metrics

    def list(
        self,
    ) -> tuple[HealthMetric, ...]:
        """Return all metrics."""

        return tuple(
            self._metrics.values(),
        )

    def clear(
        self,
    ) -> None:
        """Clear registry."""

        self._metrics.clear()
