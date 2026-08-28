"""Canonical Family domain model."""

from familyos_cli.domain.family.events import FamilyCreated
from familyos_cli.domain.family.family import Family
from familyos_cli.domain.family.family_id import FamilyId
from familyos_cli.domain.family.membership import (
    InvalidMembershipTransitionError,
    Membership,
)
from familyos_cli.domain.family.membership_events import (
    FamilyMembershipActivated,
    FamilyMembershipCreated,
    FamilyMembershipEnded,
    FamilyMembershipReactivated,
    FamilyMembershipSuspended,
)
from familyos_cli.domain.family.membership_state import MembershipState
from familyos_cli.domain.family.relationship import (
    InvalidRelationshipTransitionError,
    Relationship,
)
from familyos_cli.domain.family.relationship_events import (
    FamilyRelationshipEnded,
    FamilyRelationshipEstablished,
)
from familyos_cli.domain.family.relationship_state import RelationshipState
from familyos_cli.domain.family.relationship_type import RelationshipType

__all__ = [
    "Family",
    "FamilyCreated",
    "FamilyId",
    "FamilyMembershipActivated",
    "FamilyMembershipCreated",
    "FamilyMembershipEnded",
    "FamilyMembershipReactivated",
    "FamilyMembershipSuspended",
    "FamilyRelationshipEnded",
    "FamilyRelationshipEstablished",
    "InvalidMembershipTransitionError",
    "InvalidRelationshipTransitionError",
    "Membership",
    "MembershipState",
    "Relationship",
    "RelationshipState",
    "RelationshipType",
]
