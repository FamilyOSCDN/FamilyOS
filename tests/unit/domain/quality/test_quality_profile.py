from dataclasses import FrozenInstanceError

import pytest

from familyos_cli.domain.quality import (
    QualityCheckId,
    QualityDomain,
    QualityProfile,
    QualityProfileId,
    QualitySeverity,
)


def profile() -> QualityProfile:
    return QualityProfile(
        id=QualityProfileId("QLT-PROFILE-REPOSITORY"),
        version="1.0.0",
        target_types=("repository",),
        required_checks=(
            QualityCheckId("QLT-CHECK-RUFF"),
            QualityCheckId("QLT-CHECK-MYPY"),
            QualityCheckId("QLT-CHECK-PYTEST"),
        ),
        required_domains=(
            QualityDomain("QLT-DOM-COR"),
            QualityDomain("QLT-DOM-TST"),
        ),
        severity_policy=(
            (QualitySeverity.HIGH, True),
            (QualitySeverity.MEDIUM, False),
        ),
    )


def test_profile_model() -> None:
    value = profile()
    assert str(value.id) == "QLT-PROFILE-REPOSITORY"
    assert value.version == "1.0.0"
    assert value.applies_to("repository")
    assert not value.applies_to("plugin")
    assert value.reference == "QLT-PROFILE-REPOSITORY@1.0.0"


def test_profile_id_namespace() -> None:
    with pytest.raises(ValueError):
        QualityProfileId("QLT-CHECK-REPOSITORY")


def test_profile_is_immutable() -> None:
    value = profile()
    with pytest.raises(FrozenInstanceError):
        value.version = "2.0.0"  # type: ignore[misc]


def test_profile_version_must_be_non_empty() -> None:
    with pytest.raises(ValueError):
        QualityProfile(
            QualityProfileId("QLT-PROFILE-REPOSITORY"), "", (), (), (), ()
        )


def test_profile_rejects_duplicate_target_types() -> None:
    with pytest.raises(ValueError, match="target_types.*duplicates"):
        QualityProfile(
            QualityProfileId("QLT-PROFILE-REPOSITORY"), "1",
            ("repository", "repository"), (), (), ()
        )


def test_profile_rejects_duplicate_checks() -> None:
    check = QualityCheckId("QLT-CHECK-RUFF")
    with pytest.raises(ValueError, match="required_checks.*duplicates"):
        QualityProfile(
            QualityProfileId("QLT-PROFILE-REPOSITORY"), "1",
            ("repository",), (check, check), (), ()
        )


def test_profile_rejects_duplicate_domains() -> None:
    domain = QualityDomain("QLT-DOM-COR")
    with pytest.raises(ValueError, match="required_domains.*duplicates"):
        QualityProfile(
            QualityProfileId("QLT-PROFILE-REPOSITORY"), "1",
            ("repository",), (), (domain, domain), ()
        )


def test_profile_rejects_duplicate_severity_policy() -> None:
    with pytest.raises(ValueError, match="duplicate severities"):
        QualityProfile(
            QualityProfileId("QLT-PROFILE-REPOSITORY"), "1",
            ("repository",), (), (),
            ((QualitySeverity.HIGH, True), (QualitySeverity.HIGH, False)),
        )


def test_profile_stable_serialization() -> None:
    assert profile().to_dict() == {
        "id": "QLT-PROFILE-REPOSITORY",
        "version": "1.0.0",
        "target_types": ["repository"],
        "required_checks": [
            "QLT-CHECK-RUFF", "QLT-CHECK-MYPY", "QLT-CHECK-PYTEST"
        ],
        "required_domains": ["QLT-DOM-COR", "QLT-DOM-TST"],
        "severity_policy": [
            {"severity": "HIGH", "blocking": True},
            {"severity": "MEDIUM", "blocking": False},
        ],
    }


def test_profile_rejects_invalid_id_type() -> None:
    with pytest.raises(TypeError, match="id must be a QualityProfileId"):
        QualityProfile(
            "QLT-PROFILE-REPOSITORY",  # type: ignore[arg-type]
            "1",
            ("repository",),
            (),
            (),
            (),
        )


def test_profile_version_must_be_a_string() -> None:
    with pytest.raises(TypeError, match="version must be a str"):
        QualityProfile(
            QualityProfileId("QLT-PROFILE-REPOSITORY"),
            1,  # type: ignore[arg-type]
            ("repository",),
            (),
            (),
            (),
        )


def test_profile_target_types_must_be_a_tuple() -> None:
    with pytest.raises(TypeError, match="target_types must be a tuple"):
        QualityProfile(
            QualityProfileId("QLT-PROFILE-REPOSITORY"),
            "1",
            ["repository"],  # type: ignore[arg-type]
            (),
            (),
            (),
        )


def test_profile_target_type_entries_must_be_non_empty_strings() -> None:
    with pytest.raises(ValueError, match="target_types entries must be non-empty"):
        QualityProfile(
            QualityProfileId("QLT-PROFILE-REPOSITORY"),
            "1",
            ("",),
            (),
            (),
            (),
        )


def test_profile_required_checks_require_canonical_ids() -> None:
    with pytest.raises(TypeError, match="required_checks"):
        QualityProfile(
            QualityProfileId("QLT-PROFILE-REPOSITORY"),
            "1",
            ("repository",),
            ("QLT-CHECK-RUFF",),  # type: ignore[arg-type]
            (),
            (),
        )


def test_profile_required_domains_require_canonical_domains() -> None:
    with pytest.raises(TypeError, match="required_domains"):
        QualityProfile(
            QualityProfileId("QLT-PROFILE-REPOSITORY"),
            "1",
            ("repository",),
            (),
            ("QLT-DOM-COR",),  # type: ignore[arg-type]
            (),
        )


def test_profile_severity_policy_must_be_a_tuple() -> None:
    with pytest.raises(TypeError, match="severity_policy must be a tuple"):
        QualityProfile(
            QualityProfileId("QLT-PROFILE-REPOSITORY"),
            "1",
            ("repository",),
            (),
            (),
            [],  # type: ignore[arg-type]
        )


def test_profile_severity_policy_requires_pair_entries() -> None:
    with pytest.raises(TypeError, match="severity_policy entries"):
        QualityProfile(
            QualityProfileId("QLT-PROFILE-REPOSITORY"),
            "1",
            ("repository",),
            (),
            (),
            ((QualitySeverity.HIGH,),),  # type: ignore[arg-type]
        )


def test_profile_severity_policy_requires_canonical_severity() -> None:
    with pytest.raises(TypeError, match="severity_policy severity"):
        QualityProfile(
            QualityProfileId("QLT-PROFILE-REPOSITORY"),
            "1",
            ("repository",),
            (),
            (),
            (("HIGH", True),),  # type: ignore[arg-type]
        )


def test_profile_severity_policy_requires_boolean_blocking_value() -> None:
    with pytest.raises(TypeError, match="blocking value must be a bool"):
        QualityProfile(
            QualityProfileId("QLT-PROFILE-REPOSITORY"),
            "1",
            ("repository",),
            (),
            (),
            ((QualitySeverity.HIGH, "yes"),),  # type: ignore[arg-type]
        )
