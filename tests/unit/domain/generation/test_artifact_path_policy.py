from __future__ import annotations

import pytest

from familyos_cli.domain.generation.artifact_kind import (
    ArtifactKind,
)
from familyos_cli.domain.generation.artifact_path_policy import (
    DefaultArtifactPathPolicy,
)


@pytest.mark.parametrize(
    ("kind", "name", "expected"),
    [
        (
            ArtifactKind.ENTITY,
            "Person",
            "models/person.py",
        ),
        (
            ArtifactKind.VALUE_OBJECT,
            "EmailAddress",
            "value_objects/email_address.py",
        ),
        (
            ArtifactKind.AGGREGATE,
            "FamilyMembership",
            "aggregates/family_membership.py",
        ),
        (
            ArtifactKind.REPOSITORY,
            "PersonRepository",
            "repositories/person_repository.py",
        ),
        (
            ArtifactKind.SERVICE,
            "PersonRegistrationService",
            "services/person_registration_service.py",
        ),
        (
            ArtifactKind.README,
            "Person",
            "README.md",
        ),
        (
            ArtifactKind.DOCUMENTATION,
            "Business Rules",
            "docs/business-rules.md",
        ),
        (
            ArtifactKind.TEST,
            "PersonService",
            "tests/person_service.py",
        ),
        (
            ArtifactKind.TEMPLATE,
            "PersonEntity",
            "templates/person_entity.jinja",
        ),
    ],
)
def test_artifact_path_policy_builds_target_path(
    kind: ArtifactKind,
    name: str,
    expected: str,
) -> None:
    policy = DefaultArtifactPathPolicy()

    assert policy.path_for(
        kind=kind,
        name=name,
    ) == expected


def test_artifact_path_policy_handles_acronyms() -> None:
    policy = DefaultArtifactPathPolicy()

    path = policy.path_for(
        kind=ArtifactKind.SERVICE,
        name="HTTPClientService",
    )

    assert path == "services/http_client_service.py"


def test_artifact_path_policy_handles_existing_separators() -> None:
    policy = DefaultArtifactPathPolicy()

    path = policy.path_for(
        kind=ArtifactKind.ENTITY,
        name="Family Member",
    )

    assert path == "models/family_member.py"
