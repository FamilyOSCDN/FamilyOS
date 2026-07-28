from __future__ import annotations

import pytest

from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.generation.artifact_template_policy import (
    DefaultArtifactTemplatePolicy,
)


@pytest.mark.parametrize(
    ("kind", "expected"),
    [
        (
            ArtifactKind.ENTITY,
            "entity.py.jinja",
        ),
        (
            ArtifactKind.VALUE_OBJECT,
            "value_object.py.jinja",
        ),
        (
            ArtifactKind.AGGREGATE,
            "aggregate.py.jinja",
        ),
        (
            ArtifactKind.REPOSITORY,
            "repository.py.jinja",
        ),
        (
            ArtifactKind.SERVICE,
            "service.py.jinja",
        ),
    ],
)
def test_artifact_template_policy_selects_default_template(
    kind: ArtifactKind,
    expected: str,
) -> None:
    policy = DefaultArtifactTemplatePolicy()

    assert policy.template_for(kind) == expected


def test_artifact_template_policy_preserves_existing_template() -> None:
    policy = DefaultArtifactTemplatePolicy()

    template = policy.template_for(
        kind=ArtifactKind.DOCUMENTATION,
        current_template="custom-documentation.md.jinja",
    )

    assert template == "custom-documentation.md.jinja"


def test_artifact_template_policy_returns_empty_template_when_unknown() -> None:
    policy = DefaultArtifactTemplatePolicy()

    assert (
        policy.template_for(
            kind=ArtifactKind.README,
        )
        == ""
    )
