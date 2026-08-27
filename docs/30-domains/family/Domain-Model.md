# Domain Model

## Domain

The Family domain defines the canonical Family Core model established by
RFC-0016.

This model governs the business meaning, identity, continuity, invariants,
lifecycle, and relationships of:

- Family;
- Family Membership;
- Family Relationship;
- Family Boundary.

The model consumes canonical Person identity through the Person domain contract
and SHALL NOT redefine Person.

## Conceptual Model

The canonical conceptual model is:

```text
PersonId
   |
   v
Family Membership --------------------> Family
   |                                     |
   |                                     v
   |                               Family Boundary
   |
   +---- semantically distinct ----> Family Relationship
                                         |
                                         v
                                      PersonId
```

Security may consume approved Family Core facts, but authorization remains a
Security concern.

The diagram is conceptual and does not require aggregate nesting, database
embedding, or transport-specific representation.

## Family

A `Family` is the canonical aggregate root for one governed Family business
context.

A Family SHALL have exactly one canonical Family identity.

A Family SHALL remain the same Family independently from:

- its current Membership set;
- any single Person;
- Family Relationship changes;
- display information;
- household composition;
- authentication state;
- Security policy;
- plugin records;
- persistence representation;
- infrastructure storage.

A Family SHALL NOT be inferred solely from:

- biological relationships;
- legal relationships;
- genealogical relationships;
- social relationships;
- shared residence;
- household composition;
- Security policy;
- plugin grouping.

Removing, adding, suspending, or otherwise changing one Membership SHALL NOT by
itself replace canonical Family identity.

## Family Identity

Every Family SHALL have exactly one canonical domain identity named `FamilyId`.

`FamilyId` SHALL be:

- stable for the lifetime and historical continuity of the Family;
- opaque to consumers;
- independent from mutable Family attributes;
- independent from Membership;
- independent from Person identity;
- independent from Identity and authentication;
- independent from Security policy;
- independent from plugin-specific identifiers;
- independent from persistence keys and storage location.

### Canonical Representation

The canonical runtime representation of `FamilyId` is a UUID value.

New canonical Family identities SHALL be generated using UUID version 4.

The UUID value is a technical identity mechanism only.

Consumers SHALL NOT infer Family meaning, household meaning, Membership,
Relationship, authorization, chronology, or storage location from the UUID.

Canonical string serialization SHALL use the standard textual UUID
representation.

Runtime construction SHALL reject non-UUID backing values rather than silently
coerce strings, integers, plugin identifiers, legacy identifiers, or storage
keys into canonical `FamilyId`.

Legacy or external family-like identifiers SHALL require explicit compatibility
mapping before they may reference a canonical Family.

### FamilyId Invariants

1. Every canonical Family has exactly one `FamilyId`.
2. One `FamilyId` identifies at most one canonical Family.
3. `FamilyId` is stable across Membership changes.
4. `FamilyId` is stable across Relationship changes.
5. `FamilyId` is independent from Person identity.
6. `FamilyId` is independent from Security and authorization state.
7. `FamilyId` SHALL NOT encode household semantics.
8. `FamilyId` SHALL NOT be silently replaced by a persistence identity.
9. Legacy identifiers SHALL NOT become canonical `FamilyId` by implicit
   coercion.
10. A canonical `FamilyId` SHALL NOT be reused for another Family after
    archival, retention, erasure, deletion, migration, or equivalent processing.

## DDD Classification

The initial canonical classification is:

| Concept | Classification | Ownership |
| --- | --- | --- |
| Family | Aggregate root | Family domain |
| FamilyId | Value object | Family domain |
| Family Membership | Entity | Family domain |
| PersonId reference in Membership | External identity reference | Person domain |
| Family Relationship | Entity | Family domain |
| PersonId references in Relationship | External identity references | Person domain |
| Family Boundary | Derived domain concept / value semantics | Family domain |
| Authorization | External policy concern | Security |
| Household | Deferred concept | Unresolved / future governance |

This classification is normative for ownership and semantic boundaries.

It does not freeze persistence embedding or transport representation.

## Family Intrinsic State

The minimal canonical Family state required by the initial implementation-ready
Family subset is:

- `FamilyId`.

No display name, household data, Membership collection, Relationship collection,
Security policy, plugin record, account identity, or infrastructure identifier
is mandatory intrinsic Family state merely because it may be useful to a future
application.

Future Family attributes SHALL require explicit specification of:

- business meaning;
- ownership;
- optionality;
- invariants;
- lifecycle;
- privacy expectations;
- compatibility requirements.

Runtime code SHALL NOT invent intrinsic Family attributes.

## Family Continuity

Canonical Family continuity is established by stable `FamilyId`.

Family continuity SHALL NOT depend on:

- the existence of a particular Person;
- the number of current Memberships;
- a particular Membership state;
- Family Relationship facts;
- Security authorization;
- shared residence;
- household composition;
- plugin records;
- persistence technology.

A Family MAY have zero valid Memberships at a particular point in time if the
governing lifecycle rules permit it.

The absence of valid Membership SHALL NOT by itself mean that the Family never
existed.

## Family Lifecycle

The minimal canonical Family lifecycle required by the initial subset is:

```text
NONEXISTENT
    |
    | CreateFamily
    v
EXISTING
```

The initial canonical model does not define universal `ACTIVE`, `INACTIVE`,
`ARCHIVED`, `DELETED`, `SUSPENDED`, or equivalent Family states.

Those states SHALL remain non-normative unless a separately governed Family
business requirement justifies them.

Creation establishes one new canonical Family identity.

Creation SHALL NOT require:

- a Membership;
- a Person;
- authentication Identity state;
- Security authorization data as Family state;
- Household;
- plugin-specific records.

Authorization to invoke creation remains a Security concern outside the Family
aggregate.

## FamilyCreated

The initial canonical Family event is `FamilyCreated`.

`FamilyCreated` represents the immutable business fact that creation of exactly
one new canonical Family succeeded.

The canonical payload is:

- `family_id: FamilyId`;
- `occurred_at: datetime`.

`occurred_at` SHALL represent an unambiguous timezone-aware instant.

`FamilyCreated` SHALL NOT contain Membership, Relationship, Security,
Household, plugin, Identity, credential, or transport-specific state merely to
make the event convenient for consumers.

A failed Family creation SHALL NOT produce a successful `FamilyCreated` result.

The event fact remains distinct from delivery technology.

## Family Creation Invariants

1. Family creation establishes exactly one new canonical `FamilyId`.
2. Creation SHALL fail if the proposed canonical Family identity is already
   established.
3. Duplicate creation SHALL NOT silently replace an existing Family.
4. Duplicate creation SHALL NOT produce a second successful `FamilyCreated`
   fact.
5. Identity generation failure SHALL prevent persistence.
6. Invalid event occurrence time SHALL prevent persistence.
7. Persistence failure SHALL prevent successful creation result.
8. Family creation SHALL NOT implicitly create Membership.
9. Family creation SHALL NOT implicitly create Relationship.
10. Family creation SHALL NOT infer Household.
11. Family creation SHALL NOT grant authorization.

## Family Membership

Family Membership is a canonical Family-domain entity representing an explicit
business association between exactly one canonical Person and exactly one
canonical Family.

A Membership is not:

- the Person;
- the Family;
- a Family Relationship;
- authentication;
- authorization;
- a role;
- a permission;
- a plugin-local association.

### Membership Identity Decision

The initial canonical Membership model does **not** introduce a dedicated stable
Membership identifier.

For the initial implementation-ready subset, Membership identity is the
composite business key:

```text
(FamilyId, PersonId)
```

This decision means that, within one Family context, there is at most one
canonical Membership continuity for one canonical Person.

The composite key SHALL NOT imply that Membership is a value object.

Membership remains an entity because it has independent lifecycle and historical
continuity.

A future dedicated Membership identifier MAY be introduced only through an
explicit governed specification change if demonstrated business requirements
cannot be represented safely by the composite identity contract.

#### Membership Canonical Continuity Rule

Within the initial canonical Family model, the composite business key
`(FamilyId, PersonId)` identifies one and only one canonical Membership
continuity.

A Membership whose lifecycle state becomes `ENDED` SHALL continue to reserve
that composite business key for its historical continuity. `ENDED` SHALL NOT
make `(FamilyId, PersonId)` available for creation of a second canonical
Membership.

Therefore:

- a second Membership for the same `(FamilyId, PersonId)` SHALL be rejected;
- this rule applies regardless of whether the existing Membership is `PENDING`,
  `ACTIVE`, `SUSPENDED`, or `ENDED`;
- ending Membership SHALL preserve rather than replace its canonical identity;
- implementations SHALL NOT model re-establishment by silently creating a new
  Membership with the same composite business key.

Re-establishment of Family membership after `ENDED` remains a deferred domain
decision. Until a future governed specification defines that semantic,
attempting such re-establishment SHALL fail closed rather than create a new
canonical Membership continuity.

This rule does not introduce a dedicated Membership identifier.

### Membership References

Every Membership SHALL reference:

- exactly one canonical `FamilyId`;
- exactly one canonical `PersonId`.

The `PersonId` reference SHALL use the Person domain contract.

The Family domain SHALL NOT create, reinterpret, or mutate canonical Person
identity.

### Membership Lifecycle

The initial canonical Membership lifecycle states are:

```text
PENDING
   |
   | ActivateMembership
   v
ACTIVE
   |
   | SuspendMembership
   v
SUSPENDED
   |
   | ReactivateMembership
   v
ACTIVE
   |
   | EndMembership
   v
ENDED
```

A Membership MAY also transition directly:

```text
PENDING -> ENDED
```

when the association is cancelled or rejected before activation.

`ENDED` is terminal in the initial canonical model.

A new Membership SHALL begin in `PENDING` unless a separately governed
application contract proves that immediate activation is valid for the invoking
operation.

### Membership State Semantics

`PENDING` means:

- the Membership association has been established as a canonical Family-domain
  fact;
- it is not yet valid for business decisions that require active participation.

`ACTIVE` means:

- the Membership is currently valid as Family-domain participation context.

`SUSPENDED` means:

- the Membership remains historically established;
- it is temporarily not valid for business decisions requiring active
  participation.

`ENDED` means:

- the Membership remains part of historical Family-domain truth;
- it is no longer valid as current participation.

Membership validity for ordinary current Family participation is:

```text
state == ACTIVE
```

Security MAY consume this validity as context, but Membership validity SHALL NOT
itself grant authorization.

### Membership Transition Invariants

Allowed transitions are:

- `PENDING -> ACTIVE`;
- `PENDING -> ENDED`;
- `ACTIVE -> SUSPENDED`;
- `ACTIVE -> ENDED`;
- `SUSPENDED -> ACTIVE`;
- `SUSPENDED -> ENDED`.

No other Membership transition is canonical in the initial model.

In particular:

- `ENDED -> ACTIVE` is forbidden;
- `ENDED -> PENDING` is forbidden;
- duplicate activation of `ACTIVE` SHALL NOT create a new Membership fact;
- suspension SHALL NOT change Person identity;
- ending Membership SHALL NOT change Family identity;
- ending Membership SHALL NOT delete Person;
- ending Membership SHALL NOT erase Membership history.

### Membership Temporal Semantics

Membership history SHALL preserve at least:

- when the Membership was canonically established;
- the current canonical lifecycle state;
- the effective time of lifecycle transitions required by the implementation
  contract.

The exact historical event-storage mechanism remains an implementation concern.

Canonical business history SHALL NOT be silently rewritten to make a Membership
appear never to have existed.

## Membership Domain Events

The initial canonical Membership event set is:

- `FamilyMembershipCreated`;
- `FamilyMembershipActivated`;
- `FamilyMembershipSuspended`;
- `FamilyMembershipReactivated`;
- `FamilyMembershipEnded`.

Each Membership event SHALL identify the Membership through:

- `family_id: FamilyId`;
- `person_id: PersonId`;
- `occurred_at: datetime`.

Lifecycle-transition events SHALL communicate the resulting canonical state
where required by the application contract.

All event occurrence times SHALL be timezone-aware.

Events SHALL NOT grant authorization.

## Membership Invariants

1. One Membership references exactly one Family.
2. One Membership references exactly one Person.
3. Membership is distinct from Person.
4. Membership is distinct from Family.
5. Membership is distinct from Relationship.
6. Membership is not authorization.
7. Membership lifecycle is owned by the Family domain.
8. Current business validity requires `ACTIVE`.
9. `ENDED` Membership is not currently valid.
10. Membership state changes SHALL NOT redefine Person identity.
11. Membership state changes SHALL NOT redefine Family identity.
12. One `(FamilyId, PersonId)` pair SHALL have at most one canonical Membership
    continuity in the initial model.
13. Historical Membership SHALL NOT be silently recreated as an unrelated second
    Membership merely because the previous Membership ended.
14. Membership SHALL NOT imply a biological, legal, genealogical, or social
    Relationship taxonomy.
15. Membership SHALL NOT create authorization.

## Family Relationship

Family Relationship is a canonical Family-domain entity representing explicit
family relationship knowledge between two canonical Persons.

Relationship remains semantically independent from Family Membership.

A Relationship MAY exist even when neither Person currently has an ACTIVE
Membership in the same Family.

### Relationship Scope

The initial Family Relationship model is Family-contextual.

Every canonical Relationship SHALL reference:

- exactly one `FamilyId`;
- exactly one source `PersonId`;
- exactly one target `PersonId`;
- one canonical relationship type.

This Family-contextual scope prevents unrelated Family contexts from silently
sharing one Relationship fact.

Future cross-family or global relationship semantics require separate
specification.

### Relationship Identity Decision

The initial canonical Relationship model does **not** introduce a dedicated
stable Relationship identifier.

Its initial business identity is the governed tuple:

```text
(
    FamilyId,
    source PersonId,
    target PersonId,
    relationship type
)
```

Directionality rules determine whether source and target order is meaningful.

A future dedicated Relationship identifier MAY be introduced only through an
explicit governed specification change.

#### Relationship Canonical Continuity Rule

A Family Relationship SHALL have one canonical semantic continuity for one
canonical relationship fact within one `FamilyId`.

Inverse relationship expressions SHALL NOT create independent canonical
Relationship continuities. `PARENT_OF` and `CHILD_OF` are inverse views of the
same canonical parent-child fact.

Accordingly, if Person A is canonically `PARENT_OF` Person B, the expression
that Person B is `CHILD_OF` Person A SHALL be derived from that same canonical
Relationship continuity. An implementation SHALL NOT persist those inverse
expressions as two independent canonical Relationship facts.

For canonical identity purposes, the parent-child relationship SHALL be
normalized to the `PARENT_OF` orientation:

`(FamilyId, parent PersonId, PARENT_OF, child PersonId)`

The inverse `CHILD_OF` expression SHALL resolve to that same canonical
continuity.

Symmetric relationship expressions SHALL likewise identify one canonical
Relationship continuity. For `SPOUSE_OF` and `SIBLING_OF`, reversing the two
Persons SHALL NOT create a second canonical Relationship.

For canonical identity purposes, symmetric endpoints SHALL be normalized using
a deterministic total ordering of the two canonical `PersonId` UUID values.
The lower ordered canonical UUID SHALL occupy the first endpoint and the higher
ordered canonical UUID SHALL occupy the second endpoint.

The resulting canonical symmetric business key is therefore conceptually:

`(FamilyId, lower PersonId, relationship type, higher PersonId)`

The ordering rule is an identity-normalization rule only. It SHALL NOT imply
seniority, authority, direction, ownership, preference, or any other domain
meaning between the two Persons.

Relationship state transitions, inverse views, and symmetric views SHALL all
preserve this canonical continuity rather than create replacement
Relationships.

A Relationship whose state becomes `ENDED` SHALL retain its canonical
historical continuity. Re-establishment after `ENDED` remains deferred.
Until governed semantics define whether re-establishment resumes the existing
continuity or establishes another explicitly distinguishable historical fact,
implementations SHALL fail closed rather than invent a second canonical
Relationship.

This rule does not introduce a dedicated Relationship identifier.

### Initial Relationship Taxonomy

The initial canonical taxonomy is deliberately minimal:

- `PARENT_OF`;
- `CHILD_OF`;
- `SPOUSE_OF`;
- `SIBLING_OF`.

This taxonomy exists to support demonstrated core family semantics without
claiming exhaustive biological, legal, genealogical, cultural, or social
coverage.

Additional relationship types SHALL require governed specification evolution.

### Directionality and Symmetry

`PARENT_OF` is directional.

If:

```text
A PARENT_OF B
```

then the inverse semantic fact is:

```text
B CHILD_OF A
```

`CHILD_OF` is directional and inverse to `PARENT_OF`.

`SPOUSE_OF` is symmetric.

If:

```text
A SPOUSE_OF B
```

then:

```text
B SPOUSE_OF A
```

represents the same canonical Relationship meaning.

`SIBLING_OF` is symmetric.

For symmetric Relationship types, source/target ordering SHALL NOT create two
distinct canonical Relationship facts.

#### Canonical Direction and Symmetry Invariants

The directionality taxonomy and canonical identity rules SHALL be interpreted
together.

For inverse types:

- `PARENT_OF` is the canonical stored orientation of the parent-child fact;
- `CHILD_OF` is its inverse semantic view;
- querying or expressing the inverse SHALL NOT create another canonical fact;
- lifecycle state belongs to the single canonical parent-child continuity.

For symmetric types:

- `SPOUSE_OF(A, B)` and `SPOUSE_OF(B, A)` denote the same canonical fact;
- `SIBLING_OF(A, B)` and `SIBLING_OF(B, A)` denote the same canonical fact;
- endpoint ordering SHALL be normalized before canonical identity comparison;
- duplicate creation through reversed endpoints SHALL be rejected as the same
  canonical Relationship.

These normalization rules SHALL be scoped by `FamilyId`. An otherwise identical
relationship fact in another Family context is a distinct Family-domain fact
and SHALL NOT share canonical continuity across Family boundaries.

### Relationship Self-Reference

A Person SHALL NOT have a canonical Family Relationship to itself for any of the
initial relationship types.

### Relationship Lifecycle

The initial canonical Relationship lifecycle is:

```text
NONEXISTENT
    |
    | EstablishRelationship
    v
ESTABLISHED
    |
    | EndRelationship
    v
ENDED
```

`ENDED` is terminal for one canonical Relationship continuity.

Ending a Relationship SHALL NOT:

- end Membership;
- change Family identity;
- change Person identity;
- grant or revoke authorization.

A later re-establishment of the same semantic Relationship requires explicit
historical semantics and therefore remains deferred in the initial runtime
subset.

### Relationship Temporal Semantics

A canonical Relationship SHALL preserve the historical fact that it was
established.

The initial contract requires:

- establishment time;
- current lifecycle state;
- end time when ended.

The exact persistence mechanism remains implementation-specific.

### Relationship Domain Events

The initial canonical Relationship event set is:

- `FamilyRelationshipEstablished`;
- `FamilyRelationshipEnded`.

Each event SHALL identify:

- `family_id: FamilyId`;
- source `person_id: PersonId`;
- target `person_id: PersonId`;
- relationship type;
- timezone-aware `occurred_at`.

Relationship events SHALL NOT create, mutate, or authorize Membership.

### Relationship Invariants

1. Relationship is distinct from Membership.
2. Relationship is not authorization.
3. Every Relationship belongs to exactly one Family context in the initial
   model.
4. Every Relationship references exactly two canonical Persons.
5. A Person SHALL NOT relate to itself under the initial taxonomy.
6. Directional Relationship types preserve source/target meaning.
7. Symmetric Relationship types SHALL NOT be duplicated merely by reversing
   source and target.
8. `PARENT_OF` and `CHILD_OF` are inverse semantics.
9. `SPOUSE_OF` is symmetric.
10. `SIBLING_OF` is symmetric.
11. Ending Relationship SHALL NOT change Membership.
12. Relationship history SHALL NOT be silently rewritten.
13. Relationship SHALL NOT imply Security permission.

## Family Boundary

Family Boundary is the canonical business-isolation semantics associated with
one Family.

Family Boundary is derived from canonical `FamilyId`.

The minimal derivation rule is:

```text
Family Boundary identity == FamilyId
```

This does not make Family Boundary a second aggregate or a second persistent
identity.

It means that one canonical Family defines one canonical business boundary.

### Boundary Semantics

Within the initial model:

- Family-owned Membership belongs to exactly one Family Boundary;
- Family-contextual Relationship belongs to exactly one Family Boundary;
- plugin records MAY reference Family Boundary through canonical Family
  contracts;
- unrelated Family contexts SHALL remain distinct.

Family Boundary SHALL NOT be interpreted as authorization policy.

### Cross-Family Rules

A Person MAY participate in more than one Family through separate Memberships.

Participation in Family A SHALL NOT implicitly establish:

- Membership in Family B;
- Relationship in Family B;
- access to Family B;
- permission over Family B resources;
- shared plugin scope with Family B.

Cross-family authorization requires explicit Security policy.

Cross-family business behavior beyond independent Memberships remains deferred
unless separately specified.

### Boundary Invariants

1. Every Family has exactly one canonical Family Boundary.
2. Family Boundary derives from `FamilyId`.
3. Boundary does not own authorization policy.
4. Membership belongs to one Family Boundary through its `FamilyId`.
5. Family-contextual Relationship belongs to one Family Boundary through its
   `FamilyId`.
6. Membership in one Family does not imply Membership in another.
7. Relationship in one Family does not imply Relationship in another.
8. Shared Person identity does not merge Family Boundaries.
9. Shared infrastructure does not merge Family Boundaries.
10. Shared plugin data does not merge Family Boundaries.

## Security Boundary

Family Core defines Family, Membership, Relationship, and Boundary facts.

Security owns:

- authentication;
- authorization policy;
- roles;
- permissions;
- authorization decisions;
- enforcement.

Security MAY consume approved Family Core facts.

Security SHALL NOT redefine Family Core facts merely to produce an authorization
decision.

Family Core SHALL NOT embed authorization results as canonical Family,
Membership, Relationship, or Boundary state.

## Person Boundary

Person is external to the Family aggregate.

Family Core SHALL reference Person only through canonical `PersonId`.

Family Core SHALL NOT:

- construct alternate Person identity;
- mutate Person identity;
- derive Person continuity from Membership;
- redefine Person lifecycle;
- require Membership for Person existence.

Membership lifecycle and Relationship lifecycle SHALL NOT alter canonical Person
identity.

## Identity Boundary

Platform Identity remains distinct from Family Core.

Authentication Identity MAY reference or consume Family context through
separately governed contracts.

Identity SHALL NOT become the source of truth for Family, Membership,
Relationship, or Boundary semantics.

## Plugin Boundary

Official plugins MAY reference Family Core through approved contracts.

Plugin-owned records SHALL remain owned by their respective domains.

Plugin identifiers SHALL NOT become canonical Family, Membership, or
Relationship identity by implicit adoption.

## Privacy and Data Integrity

Family Core data SHALL preserve the integrity of:

- `FamilyId`;
- canonical `PersonId` references;
- Membership lifecycle;
- Relationship semantics;
- Family Boundary isolation;
- required historical facts.

Privacy, disclosure, retention, erasure, and security-sensitive presentation
mechanics remain governed by their applicable contracts.

Privacy processing SHALL NOT silently rewrite canonical Family Core historical
truth.

## Historical Continuity

Canonical Family Core historical facts SHALL remain distinguishable from current
state.

At minimum:

- Family creation remains a historical fact;
- Membership creation and lifecycle changes remain historical facts;
- Relationship establishment and ending remain historical facts.

Retention or erasure of erasable associated data SHALL NOT silently reinterpret
those business facts as though the canonical events never occurred.

Canonical identifiers SHALL NOT be reused for unrelated domain continuities.

## Compatibility Boundary

Existing family-like, membership-like, or relationship-like plugin and legacy
identifiers are compatibility inputs only.

They SHALL NOT become canonical Family Core identity merely because they
predate this model.

Compatibility mapping SHALL:

- be explicit;
- preserve canonical Family and Person identity boundaries;
- fail closed on ambiguity;
- avoid silently merging distinct Family contexts;
- avoid silently splitting one canonical Family continuity;
- avoid inferring authorization;
- avoid inferring Household equivalence.

Concrete migration mechanics remain deferred.

## Canonical Failure Categories

The Family domain model establishes the following semantic categories for future
application contracts:

1. **Invalid Family Input** — proposed Family Core input violates canonical
   invariants.
2. **Family Conflict** — an operation conflicts with established canonical
   Family state or uniqueness.
3. **Family Not Found** — a valid canonical `FamilyId` does not resolve to a
   Family.
4. **Membership Conflict** — requested Membership creation or transition
   conflicts with established Membership continuity or state.
5. **Membership Not Found** — the canonical Membership key does not resolve.
6. **Invalid Membership Transition** — the requested lifecycle transition is not
   canonical.
7. **Relationship Conflict** — requested Relationship establishment conflicts
   with established Relationship continuity or invariants.
8. **Relationship Not Found** — the canonical Relationship business key does not
   resolve.
9. **Invalid Relationship Transition** — the requested Relationship lifecycle
   change is not canonical.
10. **Authorization Denial** — Security denies the operation.
11. **Privacy or Disclosure Restriction** — policy prevents disclosure or use.
12. **Infrastructure Failure** — persistence, transaction, transport, or other
    technical execution fails.
13. **Compatibility or Migration Failure** — legacy evidence cannot be mapped
    safely.

These categories are semantic distinctions.

Concrete exception classes, result objects, transport mappings, and status codes
remain application and interface contract decisions until separately specified.

## Failure Separation Invariants

1. Family absence SHALL remain distinct from invalid `FamilyId`.
2. Family absence SHALL remain distinct from authorization denial.
3. Family absence SHALL remain distinct from infrastructure failure.
4. Membership absence SHALL remain distinct from invalid Membership transition.
5. Relationship absence SHALL remain distinct from invalid Relationship
   transition.
6. Family conflict SHALL NOT become ordinary absence.
7. Membership conflict SHALL NOT become authorization denial.
8. Relationship conflict SHALL NOT become authorization denial.
9. Infrastructure failure SHALL NOT become a Family Core business fact merely
   because persistence failed.
10. Security disclosure decisions SHALL NOT redefine internal Family Core
    semantic categories.

## Household

`Household` is not part of the canonical initial Family domain model.

Household remains explicitly deferred.

Family SHALL NOT be inferred from shared residence or household composition.

No runtime model, persistence schema, adapter, plugin, or interface SHALL create
Household semantics implicitly.

## Deferred Domain-Model Decisions

The following remain deferred beyond the initial implementation-ready subset:

- Family attributes beyond `FamilyId`;
- universal Family archival, deletion, restoration, or status models;
- dedicated Membership identifier;
- Membership lifecycle states beyond `PENDING`, `ACTIVE`, `SUSPENDED`, and
  `ENDED`;
- Membership re-establishment semantics after `ENDED`;
- dedicated Relationship identifier;
- Relationship taxonomy beyond the initial four types;
- re-establishment of an ended Relationship;
- cross-family Relationship semantics;
- global Relationship semantics independent from Family context;
- Relationship evidence/provenance models;
- additional Family Boundary mechanics;
- Household;
- universal historical-query APIs;
- migration implementation details;
- persistence technology;
- transaction technology;
- event delivery technology;
- Security policy;
- Privacy policy implementation.

These deferred decisions SHALL NOT be silently frozen by runtime code.

## Implementation Gate

The Family domain model now specifies enough semantics for implementation of
only the following candidate minimal subset, subject to reconciliation with
Capabilities.md and API.md:

- `FamilyId`;
- minimal `Family`;
- `FamilyCreated`;
- Family creation and retrieval;
- Family persistence abstraction;
- Family Membership with the lifecycle defined above;
- Membership lifecycle events defined above;
- Family Relationship using the initial taxonomy and lifecycle defined above;
- Relationship events defined above;
- Family Boundary derivation from `FamilyId`.

This document alone does not authorize runtime implementation.

Capabilities, application contracts, persistence boundaries, failure/result
representation, compatibility boundaries, and final cross-document consistency
must also satisfy the RFC-0016 specification-to-implementation gate.

## Normative References

- `docs/30-domains/family/README.md`
- `docs/30-domains/family/Vision.md`
- `docs/30-domains/family/Responsibilities.md`
- `docs/30-domains/person/README.md`
- `docs/30-domains/person/Domain-Model.md`
- `docs/rfcs/RFC-0016-family-core-domain/RFC-0016-Family-Core-Domain.md`
- `docs/00-foundation/Domain-Architecture.md`
- `docs/00-foundation/Data-Architecture.md`
- `docs/00-foundation/Identity-Architecture.md`
- `docs/00-foundation/Security-Architecture.md`
- `docs/04-reference/Naming-Conventions.md`
- `docs/06-specifications/SPEC-0008-Naming-Conventions.md`
