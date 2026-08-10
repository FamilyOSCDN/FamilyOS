"""Contract tests for official FamilyOS plugin identifiers."""

from pathlib import Path

from familyos_cli.plugins.builtin.communication.plugin import (
    CommunicationPlugin,
)
from familyos_cli.plugins.builtin.documents.plugin import (
    DocumentsPlugin,
)
from familyos_cli.plugins.builtin.education.plugin import (
    EducationPlugin,
)
from familyos_cli.plugins.builtin.finance.plugin import (
    FinancePlugin,
)
from familyos_cli.plugins.builtin.health.plugin import (
    HealthPlugin,
)
from familyos_cli.plugins.builtin.security.plugin import (
    SecurityPlugin,
)
from familyos_cli.plugins.plugin_loader import PluginLoader


def builtin_plugins_path() -> Path:
    """Return the builtin plugins directory."""

    return (
        Path(__file__).parents[4]
        / "src"
        / "familyos_cli"
        / "plugins"
        / "builtin"
    )


def test_official_plugin_descriptor_ids_are_stable() -> None:
    """Official plugin descriptor identifiers follow the current contract."""

    loader = PluginLoader()

    descriptors = loader.discover(
        builtin_plugins_path(),
    )

    descriptor_ids = {
        descriptor.class_name: descriptor.id
        for descriptor in descriptors
    }

    assert descriptor_ids["SecurityPlugin"] == (
        "familyos.security"
    )
    assert descriptor_ids["HealthPlugin"] == (
        "familyos.health"
    )
    assert descriptor_ids["FinancePlugin"] == (
        "familyos.finance"
    )
    assert descriptor_ids["EducationPlugin"] == (
        "education"
    )
    assert descriptor_ids["DocumentsPlugin"] == (
        "documents"
    )
    assert descriptor_ids["CommunicationPlugin"] == (
        "communication"
    )


def test_security_capability_ids_are_stable() -> None:
    """Security capability identifiers follow their established contract."""

    identifiers = {
        str(capability.id)
        for capability in SecurityPlugin().capabilities()
    }

    assert identifiers == {
        "security.policy",
        "security.validation",
    }


def test_health_capability_ids_are_stable() -> None:
    """Health capability identifiers follow their established contract."""

    identifiers = {
        str(capability.id)
        for capability in HealthPlugin().capabilities()
    }

    assert identifiers == {
        "familyos.health.profile",
        "familyos.health.record",
    }


def test_finance_capability_ids_are_stable() -> None:
    """Finance capability identifiers follow their established contract."""

    identifiers = {
        str(capability.id)
        for capability in FinancePlugin().capabilities()
    }

    assert identifiers == {
        "familyos.finance.account",
        "familyos.finance.transaction",
        "familyos.finance.asset",
        "familyos.finance.liability",
        "familyos.finance.budget",
    }


def test_education_capability_ids_are_stable() -> None:
    """Education capability identifiers follow their established contract."""

    identifiers = {
        str(capability.id)
        for capability in EducationPlugin().capabilities()
    }

    assert identifiers == {
        "familyos.education.learner",
        "familyos.education.course",
        "familyos.education.record",
    }


def test_documents_capability_ids_are_stable() -> None:
    """Documents capability identifiers follow their established contract."""

    identifiers = {
        str(capability.id)
        for capability in DocumentsPlugin().capabilities()
    }

    assert identifiers == {
        "familyos.documents.document",
        "familyos.documents.archive",
    }


def test_communication_capability_ids_are_stable() -> None:
    """Communication capability identifiers follow their established contract."""

    identifiers = {
        str(capability.id)
        for capability in CommunicationPlugin().capabilities()
    }

    assert identifiers == {
        "familyos.communication.messaging",
        "familyos.communication.archive",
    }
