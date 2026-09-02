"""Deterministic resolver for canonical Quality Framework profiles."""
from familyos_cli.application.quality.quality_profile_registry import (
    QualityProfileRegistry,
)
from familyos_cli.domain.quality import QualityProfile, QualityTarget


class QualityProfileResolver:
    """Resolve exactly one directly applicable governed Quality Profile."""

    def __init__(self, registry: QualityProfileRegistry) -> None:
        if not isinstance(registry, QualityProfileRegistry):
            raise TypeError("registry must be a QualityProfileRegistry")
        self._registry = registry

    def resolve(self, target: QualityTarget) -> QualityProfile:
        if not isinstance(target, QualityTarget):
            raise TypeError("target must be a QualityTarget")
        applicable = tuple(
            profile for profile in self._registry.list()
            if profile.applies_to(target.target_type)
        )
        if not applicable:
            raise ValueError(
                f"No QualityProfile applies to target type '{target.target_type}'"
            )
        if len(applicable) > 1:
            references = ", ".join(profile.reference for profile in applicable)
            raise ValueError(
                "Ambiguous QualityProfile resolution for target type "
                f"'{target.target_type}': {references}"
            )
        return applicable[0]
