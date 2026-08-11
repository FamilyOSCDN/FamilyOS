"""Tests for plugin dependencies."""

import pytest

from familyos_cli.plugins.ecosystem.resolution import (
    PluginDependency,
)
from familyos_cli.plugins.ecosystem.resolution.constraint_set import (
    ConstraintSet,
)
from familyos_cli.plugins.ecosystem.resolution.version_constraint import (
    VersionConstraint,
)


def test_dependency_without_constraint_identifier() -> None:
    """A dependency without constraints should expose its canonical ID."""

    dependency = PluginDependency(
        plugin_id="familyos.notification",
    )

    assert dependency.plugin_id == "familyos.notification"
    assert dependency.name == "familyos.notification"
    assert dependency.constraint_set is None
    assert dependency.constraint is None
    assert dependency.minimum_version == ""
    assert dependency.identifier() == "familyos.notification"


def test_dependency_supports_legacy_minimum_version() -> None:
    """The legacy minimum-version API should remain compatible."""

    dependency = PluginDependency(
        plugin_id="familyos.notification",
        minimum_version="1.0.0",
    )

    assert dependency.constraint_set == ConstraintSet.parse(
        ">=1.0.0",
    )
    assert dependency.constraint == VersionConstraint.parse(
        ">=1.0.0",
    )
    assert dependency.minimum_version == "1.0.0"
    assert dependency.identifier() == "familyos.notification>=1.0.0"


def test_dependency_supports_typed_constraint() -> None:
    """A dependency should accept a typed atomic constraint."""

    dependency = PluginDependency(
        plugin_id="familyos.notification",
        constraint=VersionConstraint.parse(
            "==2.0.0",
        ),
    )

    assert dependency.constraint_set == ConstraintSet.parse(
        "==2.0.0",
    )
    assert dependency.constraint == VersionConstraint.parse(
        "==2.0.0",
    )
    assert dependency.minimum_version == ""
    assert dependency.identifier() == "familyos.notification==2.0.0"


def test_dependency_supports_constraint_set() -> None:
    """A dependency should accept multiple typed constraints."""

    dependency = PluginDependency(
        plugin_id="familyos.notification",
        constraint_set=ConstraintSet.parse(
            ">=1.2.0,<2.0.0",
        ),
    )

    assert dependency.constraint_set == ConstraintSet.parse(
        ">=1.2.0,<2.0.0",
    )
    assert dependency.constraint is None
    assert dependency.minimum_version == ""
    assert dependency.identifier() == "familyos.notification>=1.2.0,<2.0.0"


@pytest.mark.parametrize(
    (
        "minimum_version",
        "constraint",
        "constraint_set",
    ),
    [
        (
            "1.0.0",
            VersionConstraint.parse(
                ">=2.0.0",
            ),
            None,
        ),
        (
            "1.0.0",
            None,
            ConstraintSet.parse(
                ">=2.0.0",
            ),
        ),
        (
            "",
            VersionConstraint.parse(
                ">=1.0.0",
            ),
            ConstraintSet.parse(
                "<2.0.0",
            ),
        ),
    ],
)
def test_dependency_rejects_multiple_constraint_inputs(
    minimum_version: str,
    constraint: VersionConstraint | None,
    constraint_set: ConstraintSet | None,
) -> None:
    """Constraint compatibility APIs should not be combined."""

    with pytest.raises(
        ValueError,
        match=("Specify only one of minimum_version, constraint or constraint_set."),
    ):
        PluginDependency(
            name="notification",
            minimum_version=minimum_version,
            constraint=constraint,
            constraint_set=constraint_set,
        )


def test_plugin_dependency_exposes_canonical_plugin_id() -> None:
    """Dependency should expose an explicit canonical Plugin Identifier."""

    dependency = PluginDependency(
        plugin_id="familyos.documentation",
    )

    assert dependency.plugin_id == "familyos.documentation"
    assert dependency.name == "familyos.documentation"
    assert dependency.identifier() == "familyos.documentation"


def test_plugin_dependency_accepts_legacy_name_argument() -> None:
    """Legacy name argument should remain compatible."""

    dependency = PluginDependency(
        name="familyos.documentation",
    )

    assert dependency.plugin_id == "familyos.documentation"
    assert dependency.name == "familyos.documentation"


def test_plugin_dependency_rejects_conflicting_identity_arguments() -> None:
    """Canonical and legacy identity inputs must not disagree."""

    import pytest

    with pytest.raises(
        ValueError,
        match="same Plugin Identifier",
    ):
        PluginDependency(
            name="documentation",
            plugin_id="familyos.documentation",
        )


def test_plugin_dependency_rejects_invalid_explicit_plugin_id() -> None:
    """Explicit Plugin Identifiers should satisfy the canonical contract."""

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        PluginDependency(
            plugin_id="notification",
        )


def test_plugin_dependency_rejects_invalid_legacy_name_identity() -> None:
    """Legacy name construction must still use canonical Plugin IDs."""

    with pytest.raises(
        ValueError,
        match="Invalid Plugin Identifier",
    ):
        PluginDependency(
            name="notification",
        )
