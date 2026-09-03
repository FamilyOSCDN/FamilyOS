import pytest

from familyos_cli.application.quality.default_quality_profile_registry import (
    DOCUMENTATION_PROFILE,
    INITIAL_KNOWN_CHECK_IDS,
    INITIAL_PROFILE_DEFINITIONS,
    OFFICIAL_PLUGIN_PROFILE,
    REPOSITORY_PROFILE,
    build_default_quality_profile_registry,
)
from familyos_cli.application.quality.quality_profile_resolver import (
    QualityProfileResolver,
)
from familyos_cli.domain.quality import QualityProfileId, QualityTarget


def test_initial_profiles_are_version_controlled_and_deterministic() -> None:
    assert tuple(definition.profile for definition in INITIAL_PROFILE_DEFINITIONS) == (
        REPOSITORY_PROFILE,
        OFFICIAL_PLUGIN_PROFILE,
        DOCUMENTATION_PROFILE,
    )
    assert REPOSITORY_PROFILE.reference == "QLT-PROFILE-REPOSITORY@1.1.0"
    assert OFFICIAL_PLUGIN_PROFILE.reference == "QLT-PROFILE-OFFICIAL-PLUGIN@1.0.0"
    assert DOCUMENTATION_PROFILE.reference == "QLT-PROFILE-DOCUMENTATION@1.0.0"


def test_initial_known_check_authority_is_explicit() -> None:
    assert tuple(str(value) for value in INITIAL_KNOWN_CHECK_IDS) == (
        "QLT-CHECK-RUFF", "QLT-CHECK-MYPY", "QLT-CHECK-PYTEST",
        "QLT-CHECK-DOC", "QLT-CHECK-PLUGIN-COMPLIANCE", "QLT-CHECK-ARCHITECTURE",
    )


def test_repository_profile_contract() -> None:
    assert REPOSITORY_PROFILE.target_types == ("repository",)
    assert tuple(str(value) for value in REPOSITORY_PROFILE.required_checks) == (
        "QLT-CHECK-RUFF", "QLT-CHECK-MYPY", "QLT-CHECK-PYTEST", "QLT-CHECK-DOC", "QLT-CHECK-ARCHITECTURE",
    )
    assert REPOSITORY_PROFILE.required_domains == ()
    assert REPOSITORY_PROFILE.severity_policy == ()


def test_official_plugin_profile_contract() -> None:
    assert OFFICIAL_PLUGIN_PROFILE.target_types == ("plugin",)
    assert tuple(str(value) for value in OFFICIAL_PLUGIN_PROFILE.required_checks) == (
        "QLT-CHECK-RUFF", "QLT-CHECK-MYPY", "QLT-CHECK-PYTEST",
        "QLT-CHECK-DOC", "QLT-CHECK-PLUGIN-COMPLIANCE",
    )


def test_documentation_profile_contract() -> None:
    assert DOCUMENTATION_PROFILE.target_types == ("documentation",)
    assert tuple(str(value) for value in DOCUMENTATION_PROFILE.required_checks) == ("QLT-CHECK-DOC",)


def test_default_registry_contains_exact_initial_profile_set() -> None:
    registry = build_default_quality_profile_registry()
    assert {profile.reference for profile in registry.list()} == {
        "QLT-PROFILE-REPOSITORY@1.1.0",
        "QLT-PROFILE-OFFICIAL-PLUGIN@1.0.0",
        "QLT-PROFILE-DOCUMENTATION@1.0.0",
    }


@pytest.mark.parametrize(
    ("target_type", "expected_id"),
    (
        ("repository", "QLT-PROFILE-REPOSITORY"),
        ("plugin", "QLT-PROFILE-OFFICIAL-PLUGIN"),
        ("documentation", "QLT-PROFILE-DOCUMENTATION"),
    ),
)
def test_default_profiles_resolve_for_canonical_target_types(
    target_type: str, expected_id: str
) -> None:
    resolver = QualityProfileResolver(build_default_quality_profile_registry())
    resolved = resolver.resolve(QualityTarget(target_type, "target"))
    assert resolved.id == QualityProfileId(expected_id)


def test_default_registry_is_fresh_per_build() -> None:
    first = build_default_quality_profile_registry()
    second = build_default_quality_profile_registry()
    assert first is not second
    assert first.list() == second.list()


def test_unknown_target_remains_explicit_resolution_failure() -> None:
    resolver = QualityProfileResolver(build_default_quality_profile_registry())
    with pytest.raises(ValueError, match="No QualityProfile applies"):
        resolver.resolve(QualityTarget("package", "target"))
