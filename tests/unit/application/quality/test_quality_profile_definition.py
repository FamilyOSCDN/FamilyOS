import pytest

from familyos_cli.application.quality.quality_profile_definition import (
    QualityProfileDefinition,
)
from familyos_cli.domain.quality import QualityCheckId, QualityProfile, QualityProfileId


def profile(*checks: QualityCheckId) -> QualityProfile:
    return QualityProfile(
        id=QualityProfileId("QLT-PROFILE-TEST"),
        version="1.0.0",
        target_types=("repository",),
        required_checks=checks,
        required_domains=(),
        severity_policy=(),
    )


def test_known_required_checks_are_accepted() -> None:
    known = QualityCheckId("QLT-CHECK-RUFF")
    assert QualityProfileDefinition(profile(known), (known,)).profile.required_checks == (known,)


def test_namespace_valid_unknown_required_check_is_rejected_locally() -> None:
    known = QualityCheckId("QLT-CHECK-RUFF")
    unknown = QualityCheckId("QLT-CHECK-EXTERNAL")
    with pytest.raises(ValueError, match="unknown required checks: QLT-CHECK-EXTERNAL"):
        QualityProfileDefinition(profile(unknown), (known,))


def test_namespace_valid_unknown_check_remains_constructible_globally() -> None:
    assert str(QualityCheckId("QLT-CHECK-EXTERNAL")) == "QLT-CHECK-EXTERNAL"


def test_duplicate_known_check_ids_are_rejected() -> None:
    check_id = QualityCheckId("QLT-CHECK-RUFF")
    with pytest.raises(ValueError, match="must not contain duplicates"):
        QualityProfileDefinition(profile(check_id), (check_id, check_id))


def test_definition_dependencies_are_validated() -> None:
    with pytest.raises(TypeError, match="profile must be a QualityProfile"):
        QualityProfileDefinition("bad", ())  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="known_check_ids"):
        QualityProfileDefinition(profile(), ("bad",))  # type: ignore[arg-type]
