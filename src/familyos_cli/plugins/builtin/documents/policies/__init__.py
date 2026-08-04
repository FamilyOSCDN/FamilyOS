"""Documents plugin policy models."""

from familyos_cli.plugins.builtin.documents.policies.document_policy import (
    DocumentPolicy,
)
from familyos_cli.plugins.builtin.documents.policies.document_policy_set import (
    DocumentPolicySet,
)

__all__ = [
    "DocumentPolicy",
    "DocumentPolicySet",
]
