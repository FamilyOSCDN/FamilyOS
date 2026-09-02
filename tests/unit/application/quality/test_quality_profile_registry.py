import pytest

from familyos_cli.application.quality import QualityProfileRegistry
from familyos_cli.domain.quality import (
    QualityCheckId,
    QualityDomain,
    QualityProfile,
    QualityProfileId,
    QualitySeverity,
)


def profile(profile_id: str = "QLT-PROFILE-REPOSITORY", version: str = "1") -> QualityProfile:
    return QualityProfile(
        id=QualityProfileId(profile_id),
        version=version,
        target_types=("repository",),
        required_checks=(QualityCheckId("QLT-CHECK-RUFF"),),
        required_domains=(QualityDomain("QLT-DOM-COR"),),
        severity_policy=((QualitySeverity.HIGH, True),),
    )

def test_register_and_get_exact_identity_version() -> None:
    registry = QualityProfileRegistry()
    expected = profile()
    registry.register(expected)
    assert registry.get(expected.id, expected.version) is expected

def test_registry_rejects_non_profile() -> None:
    with pytest.raises(TypeError, match="QualityProfile values only"):
        QualityProfileRegistry().register(object())  # type: ignore[arg-type]

def test_duplicate_identity_version_is_rejected() -> None:
    registry = QualityProfileRegistry()
    registry.register(profile())
    with pytest.raises(ValueError, match="already registered"):
        registry.register(profile())

def test_same_identity_with_distinct_versions_can_be_governed() -> None:
    registry = QualityProfileRegistry()
    first, second = profile(version="1"), profile(version="2")
    registry.register(second)
    registry.register(first)
    assert registry.get(first.id, "1") is first
    assert registry.get(second.id, "2") is second

def test_get_rejects_unregistered_exact_reference() -> None:
    with pytest.raises(ValueError, match="is not registered"):
        QualityProfileRegistry().get(QualityProfileId("QLT-PROFILE-REPOSITORY"), "1")

def test_get_validates_reference_types() -> None:
    registry = QualityProfileRegistry()
    with pytest.raises(TypeError, match="profile_id"):
        registry.get("QLT-PROFILE-REPOSITORY", "1")  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="version must be a str"):
        registry.get(QualityProfileId("QLT-PROFILE-REPOSITORY"), 1)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="version must be non-empty"):
        registry.get(QualityProfileId("QLT-PROFILE-REPOSITORY"), "")

def test_list_is_deterministic_independent_of_registration_order() -> None:
    first = profile("QLT-PROFILE-A", "2")
    second = profile("QLT-PROFILE-A", "1")
    third = profile("QLT-PROFILE-B", "1")
    registry = QualityProfileRegistry()
    for value in (third, first, second):
        registry.register(value)
    assert registry.list() == (second, first, third)
