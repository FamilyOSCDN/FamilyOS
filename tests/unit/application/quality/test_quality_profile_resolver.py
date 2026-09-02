import pytest

from familyos_cli.application.quality import (
    QualityProfileRegistry,
    QualityProfileResolver,
)
from familyos_cli.domain.quality import (
    QualityCheckId,
    QualityDomain,
    QualityProfile,
    QualityProfileId,
    QualitySeverity,
    QualityTarget,
)


def profile(
    profile_id: str, *, version: str = "1",
    target_types: tuple[str, ...], check_id: str = "QLT-CHECK-RUFF",
) -> QualityProfile:
    return QualityProfile(
        id=QualityProfileId(profile_id),
        version=version,
        target_types=target_types,
        required_checks=(QualityCheckId(check_id),),
        required_domains=(QualityDomain("QLT-DOM-COR"),),
        severity_policy=((QualitySeverity.HIGH, True),),
    )

def target(target_type: str) -> QualityTarget:
    return QualityTarget(target_type=target_type, identifier="target")

def test_resolves_exactly_one_applicable_profile() -> None:
    repository = profile("QLT-PROFILE-REPOSITORY", target_types=("repository",))
    registry = QualityProfileRegistry()
    registry.register(profile("QLT-PROFILE-DOCUMENTATION", target_types=("documentation",)))
    registry.register(repository)
    resolved = QualityProfileResolver(registry).resolve(target("repository"))
    assert resolved is repository
    assert resolved.reference == "QLT-PROFILE-REPOSITORY@1"

def test_zero_applicable_profiles_fails_explicitly() -> None:
    registry = QualityProfileRegistry()
    registry.register(profile("QLT-PROFILE-DOCUMENTATION", target_types=("documentation",)))
    with pytest.raises(ValueError, match="No QualityProfile applies"):
        QualityProfileResolver(registry).resolve(target("repository"))

def test_multiple_applicable_profiles_fail_as_ambiguous() -> None:
    registry = QualityProfileRegistry()
    registry.register(profile("QLT-PROFILE-A", target_types=("repository",)))
    registry.register(profile("QLT-PROFILE-B", target_types=("repository",)))
    with pytest.raises(ValueError, match="Ambiguous QualityProfile resolution"):
        QualityProfileResolver(registry).resolve(target("repository"))

def test_same_identity_multiple_applicable_versions_are_ambiguous() -> None:
    registry = QualityProfileRegistry()
    registry.register(profile("QLT-PROFILE-REPOSITORY", version="1", target_types=("repository",)))
    registry.register(profile("QLT-PROFILE-REPOSITORY", version="2", target_types=("repository",)))
    with pytest.raises(ValueError, match="Ambiguous QualityProfile resolution"):
        QualityProfileResolver(registry).resolve(target("repository"))

def test_resolution_outcome_is_registration_order_independent() -> None:
    profiles = (
        profile("QLT-PROFILE-B", target_types=("repository",)),
        profile("QLT-PROFILE-A", target_types=("repository",)),
    )
    messages: list[str] = []
    for ordered in (profiles, tuple(reversed(profiles))):
        registry = QualityProfileRegistry()
        for value in ordered:
            registry.register(value)
        with pytest.raises(ValueError) as error:
            QualityProfileResolver(registry).resolve(target("repository"))
        messages.append(str(error.value))
    assert messages[0] == messages[1]

def test_applicability_uses_only_exact_target_type() -> None:
    registry = QualityProfileRegistry()
    registry.register(profile("QLT-PROFILE-REPOSITORY", target_types=("repository",)))
    with pytest.raises(ValueError, match="No QualityProfile applies"):
        QualityProfileResolver(registry).resolve(target("Repository"))

def test_namespace_valid_unknown_check_is_not_globally_rejected() -> None:
    expected = profile(
        "QLT-PROFILE-REPOSITORY",
        target_types=("repository",),
        check_id="QLT-CHECK-NOT-GLOBALLY-CATALOGED",
    )
    registry = QualityProfileRegistry()
    registry.register(expected)
    assert QualityProfileResolver(registry).resolve(target("repository")) is expected

def test_resolver_rejects_invalid_registry_and_target_types() -> None:
    with pytest.raises(TypeError, match="QualityProfileRegistry"):
        QualityProfileResolver(object())  # type: ignore[arg-type]
    resolver = QualityProfileResolver(QualityProfileRegistry())
    with pytest.raises(TypeError, match="QualityTarget"):
        resolver.resolve(object())  # type: ignore[arg-type]
