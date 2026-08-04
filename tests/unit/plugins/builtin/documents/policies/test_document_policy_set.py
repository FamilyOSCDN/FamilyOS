import pytest

from familyos_cli.plugins.builtin.documents.policies.document_policy import (
    DocumentPolicy,
)
from familyos_cli.plugins.builtin.documents.policies.document_policy_set import (
    DocumentPolicySet,
)


def create_policy(
    policy_id: str,
) -> DocumentPolicy:
    return DocumentPolicy(
        id=policy_id,
        name="Document Policy",
        version="1.0.0",
    )


def test_document_policy_set_is_empty_by_default() -> None:
    policy_set = DocumentPolicySet()

    assert policy_set.list() == ()


def test_document_policy_set_preserves_order() -> None:
    first = create_policy(
        "documents.policy.first",
    )

    second = create_policy(
        "documents.policy.second",
    )

    policy_set = DocumentPolicySet(
        policies=(
            first,
            second,
        ),
    )

    assert policy_set.list() == (
        first,
        second,
    )


def test_document_policy_set_returns_policy_by_id() -> None:
    policy = create_policy(
        "documents.policy.retention",
    )

    policy_set = DocumentPolicySet(
        policies=(policy,),
    )

    assert policy_set.get(
        "documents.policy.retention",
    ) is policy


def test_document_policy_set_returns_none_for_unknown_id() -> None:
    policy_set = DocumentPolicySet()

    assert policy_set.get(
        "documents.policy.unknown",
    ) is None


def test_document_policy_set_rejects_duplicate_ids() -> None:
    first = create_policy(
        "documents.policy.retention",
    )

    duplicate = create_policy(
        "documents.policy.retention",
    )

    with pytest.raises(
        ValueError,
        match="must be unique",
    ):
        DocumentPolicySet(
            policies=(
                first,
                duplicate,
            ),
        )
