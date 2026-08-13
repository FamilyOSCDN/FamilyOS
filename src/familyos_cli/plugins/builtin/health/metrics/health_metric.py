"""Health metric model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(
    frozen=True,
    slots=True,
)
class HealthMetric:
    """Represent a measurable health value."""

    id: str

    record_id: str

    metric_type: str

    value: str

    unit: str

    recorded_at: str

    metadata: dict[str, str] = field(
        default_factory=dict,
    )

    def __post_init__(
        self,
    ) -> None:
        """Validate health metric."""

        if not self.id.strip():
            raise ValueError(
                "Health metric id cannot be empty.",
            )

        if not self.record_id.strip():
            raise ValueError(
                "Health metric record id cannot be empty.",
            )

        if not self.metric_type.strip():
            raise ValueError(
                "Health metric type cannot be empty.",
            )

        if not self.value.strip():
            raise ValueError(
                "Health metric value cannot be empty.",
            )

        if not self.unit.strip():
            raise ValueError(
                "Health metric unit cannot be empty.",
            )

        if not self.recorded_at.strip():
            raise ValueError(
                "Health metric date cannot be empty.",
            )
