"""Version-controlled initial Quality Framework profile definitions."""

from familyos_cli.application.quality.domain_boundary_quality_policy import (
    ARCHITECTURE_CHECK_ID,
)
from familyos_cli.application.quality.quality_profile_definition import (
    QualityProfileDefinition,
)
from familyos_cli.application.quality.quality_profile_registry import (
    QualityProfileRegistry,
)
from familyos_cli.domain.quality import QualityCheckId, QualityProfile, QualityProfileId

RUFF_CHECK_ID = QualityCheckId("QLT-CHECK-RUFF")
MYPY_CHECK_ID = QualityCheckId("QLT-CHECK-MYPY")
PYTEST_CHECK_ID = QualityCheckId("QLT-CHECK-PYTEST")
DOCUMENTATION_CHECK_ID = QualityCheckId("QLT-CHECK-DOC")
PLUGIN_COMPLIANCE_CHECK_ID = QualityCheckId("QLT-CHECK-PLUGIN-COMPLIANCE")

INITIAL_KNOWN_CHECK_IDS = (
    RUFF_CHECK_ID,
    MYPY_CHECK_ID,
    PYTEST_CHECK_ID,
    DOCUMENTATION_CHECK_ID,
    PLUGIN_COMPLIANCE_CHECK_ID,
    ARCHITECTURE_CHECK_ID,
)

REPOSITORY_PROFILE = QualityProfile(
    id=QualityProfileId("QLT-PROFILE-REPOSITORY"),
    version="1.1.0",
    target_types=("repository",),
    required_checks=(RUFF_CHECK_ID, MYPY_CHECK_ID, PYTEST_CHECK_ID, DOCUMENTATION_CHECK_ID, ARCHITECTURE_CHECK_ID),
    required_domains=(),
    severity_policy=(),
)

OFFICIAL_PLUGIN_PROFILE = QualityProfile(
    id=QualityProfileId("QLT-PROFILE-OFFICIAL-PLUGIN"),
    version="1.0.0",
    target_types=("plugin",),
    required_checks=(
        RUFF_CHECK_ID,
        MYPY_CHECK_ID,
        PYTEST_CHECK_ID,
        DOCUMENTATION_CHECK_ID,
        PLUGIN_COMPLIANCE_CHECK_ID,
    ),
    required_domains=(),
    severity_policy=(),
)

DOCUMENTATION_PROFILE = QualityProfile(
    id=QualityProfileId("QLT-PROFILE-DOCUMENTATION"),
    version="1.0.0",
    target_types=("documentation",),
    required_checks=(DOCUMENTATION_CHECK_ID,),
    required_domains=(),
    severity_policy=(),
)

INITIAL_PROFILE_DEFINITIONS = (
    QualityProfileDefinition(REPOSITORY_PROFILE, INITIAL_KNOWN_CHECK_IDS),
    QualityProfileDefinition(OFFICIAL_PLUGIN_PROFILE, INITIAL_KNOWN_CHECK_IDS),
    QualityProfileDefinition(DOCUMENTATION_PROFILE, INITIAL_KNOWN_CHECK_IDS),
)


def build_default_quality_profile_registry() -> QualityProfileRegistry:
    """Build a fresh deterministic registry containing governed profiles."""
    registry = QualityProfileRegistry()
    for definition in INITIAL_PROFILE_DEFINITIONS:
        registry.register(definition.profile)
    return registry
