"""Application orchestration for governed Quality check execution."""

from __future__ import annotations

from familyos_cli.application.quality.quality_check_result import QualityCheckResult
from familyos_cli.application.quality.quality_execution_binding import (
    QualityExecutionBinding,
)
from familyos_cli.application.quality.quality_profile_resolver import (
    QualityProfileResolver,
)
from familyos_cli.domain.quality import QualityCheckId, QualityTarget


class QualityExecutionService:
    """Resolve a profile and execute its required checks in profile order."""

    def __init__(
        self,
        profile_resolver: QualityProfileResolver,
        bindings: tuple[QualityExecutionBinding, ...],
    ) -> None:
        if not isinstance(profile_resolver, QualityProfileResolver):
            raise TypeError("profile_resolver must be a QualityProfileResolver")
        if not isinstance(bindings, tuple) or not all(
            isinstance(binding, QualityExecutionBinding) for binding in bindings
        ):
            raise TypeError("bindings must be a tuple of QualityExecutionBinding")

        check_ids = tuple(binding.check_id for binding in bindings)
        if len(set(check_ids)) != len(check_ids):
            raise ValueError("bindings must contain unique check_ids")

        self._profile_resolver = profile_resolver
        self._bindings = {binding.check_id: binding for binding in bindings}

    def execute(self, target: QualityTarget) -> tuple[QualityCheckResult, ...]:
        if not isinstance(target, QualityTarget):
            raise TypeError("target must be a QualityTarget")

        profile = self._profile_resolver.resolve(target)
        results: list[QualityCheckResult] = []

        for check_id in profile.required_checks:
            binding = self._binding_for(check_id)
            result = binding.executor.execute(
                check_id=check_id,
                rule=binding.rule,
                target=target,
            )
            if result.check_id != check_id:
                raise ValueError(
                    "executor result check_id must match the required QualityCheckId"
                )
            results.append(result)

        return tuple(results)

    def _binding_for(self, check_id: QualityCheckId) -> QualityExecutionBinding:
        try:
            return self._bindings[check_id]
        except KeyError as exc:
            raise ValueError(
                f"No QualityExecutionBinding exists for required check {check_id}"
            ) from exc
