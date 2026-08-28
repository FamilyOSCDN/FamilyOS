# Family Domain Capabilities

## Domain

`family`

## Purpose

This document defines the canonical business capabilities exposed by the
FamilyOS Family domain.

Capabilities describe what approved application and domain consumers may ask
Family Core to accomplish. They do not define Python classes, method
signatures, CLI commands, transport endpoints, database schemas, repository
technology, authorization policy, or event-delivery mechanisms.

This capability contract is governed by RFC-0016 and SHALL be interpreted
together with the canonical Family domain specification, especially
`Domain-Model.md`.

## Capability Model

The initial canonical Family capability set is:

```text
CreateFamily
RetrieveFamily
EstablishMembership
RetrieveMembership
ActivateMembership
SuspendMembership
EndMembership
EstablishRelationship
RetrieveRelationship
EndRelationship
ResolveFamilyBoundary
```

These names identify business capabilities rather than required implementation
class names.

A runtime implementation MAY use application-layer names consistent with
FamilyOS conventions provided that the canonical capability meaning, identity,
lifecycle, failure, and ownership boundaries remain unchanged.

The initial capability set is intentionally narrow. Capabilities SHALL NOT be
added merely to reproduce generic CRUD behavior.

## Create Family

### Capability

`CreateFamily`

### Intent

Create one new canonical Family context with one newly generated canonical
`FamilyId`.

### Required Semantics

Create Family SHALL:

- create exactly one canonical Family;
- establish a new UUID version 4 `FamilyId` according to the canonical Family
  domain model;
- preserve Family identity and continuity invariants;
- produce the canonical `FamilyCreated` domain event when creation succeeds;
- establish Family independently from Membership, Relationship, Household,
  Identity, authorization, and plugin-local records;
- fail before successful persistence is observable when canonical creation
  invariants are not satisfied.

Create Family SHALL NOT:

- infer Family from shared residence, household composition, biological,
  genealogical, legal, social, account, or authorization facts;
- create Membership implicitly;
- create Relationship implicitly;
- create Household;
- create authentication Identity;
- grant authorization;
- create plugin-specific records as canonical Family state.

Authorization to invoke this capability remains a Security concern.

## Retrieve Family

### Capability

`RetrieveFamily`

### Intent

Retrieve the canonical Family associated with a known canonical `FamilyId`.

### Required Semantics

Retrieve Family SHALL:

- address Family through canonical `FamilyId`;
- preserve Family continuity independently from current Membership composition;
- distinguish successful retrieval from canonical Family absence;
- avoid treating authorization denial as Family absence;
- avoid interpreting plugin-local, account, transport, or legacy identifiers as
  canonical `FamilyId` without an explicit compatibility contract.

Retrieval SHALL NOT imply authorization.

The concrete result representation and application/API mapping remain governed
by the later application contract.

## Establish Membership

### Capability

`EstablishMembership`

### Intent

Establish the single canonical Membership continuity associating exactly one
canonical Person with exactly one canonical Family context.

### Required Semantics

Establish Membership SHALL:

- require one canonical `FamilyId`;
- require one canonical `PersonId`;
- preserve Person ownership in the Person domain;
- use `(FamilyId, PersonId)` as the canonical Membership composite business key;
- reject creation when a Membership continuity already exists for that
  `(FamilyId, PersonId)` pair;
- treat an existing `ENDED` Membership as still reserving the same canonical
  composite business key;
- establish the initial Membership lifecycle state defined by the canonical
  Family domain model;
- preserve Family continuity independently from the new Membership;
- produce the applicable canonical Membership domain event when establishment
  succeeds.

Establish Membership SHALL NOT:

- create or redefine Person;
- create a dedicated canonical Membership identifier;
- infer Membership from Relationship, residence, Household, authentication,
  authorization, or plugin-local state;
- grant authorization;
- silently re-establish an `ENDED` Membership by creating a second Membership
  continuity.

Membership re-establishment after `ENDED` remains deferred and SHALL fail
closed until governed semantics explicitly define it.

## Retrieve Membership

### Capability

`RetrieveMembership`

### Intent

Retrieve the canonical Membership continuity identified by one canonical
`FamilyId` and one canonical `PersonId`.

### Required Semantics

Retrieve Membership SHALL:

- address Membership by `(FamilyId, PersonId)`;
- preserve the complete canonical Membership lifecycle state, including
  `ENDED`;
- distinguish Membership absence from Person absence, Family absence,
  authorization denial, and lifecycle conflict;
- avoid creating Membership as a side effect of retrieval.

Retrieval of Membership SHALL NOT itself imply that the Membership is currently
valid for a particular business decision or that an operation is authorized.

## Activate Membership

### Capability

`ActivateMembership`

### Intent

Apply the canonical transition that makes an existing Membership `ACTIVE` where
the domain model permits that transition.

### Required Semantics

Activate Membership SHALL:

- operate on the existing canonical Membership continuity;
- preserve `(FamilyId, PersonId)` identity;
- permit only transitions explicitly authorized by `Domain-Model.md`;
- reject invalid source states;
- produce the applicable canonical Membership lifecycle event on success;
- preserve historical continuity.

Activation SHALL NOT create a replacement Membership.

Activation SHALL NOT grant Security authorization merely because Membership
becomes `ACTIVE`.

## Suspend Membership

### Capability

`SuspendMembership`

### Intent

Apply the canonical transition that makes an eligible Membership `SUSPENDED`.

### Required Semantics

Suspend Membership SHALL:

- operate on the existing canonical Membership continuity;
- preserve `(FamilyId, PersonId)` identity;
- permit only the transition semantics defined by `Domain-Model.md`;
- preserve Family identity and continuity;
- preserve historical Membership meaning;
- produce the applicable canonical Membership lifecycle event on success.

Suspension SHALL NOT delete Membership, revoke Person identity, mutate
Relationship facts, or itself define Security authorization.

## End Membership

### Capability

`EndMembership`

### Intent

Apply the canonical terminal transition to `ENDED`.

### Required Semantics

End Membership SHALL:

- operate on the existing canonical Membership continuity;
- preserve `(FamilyId, PersonId)` permanently as the identity of that
  historical Membership continuity;
- make `ENDED` terminal according to the current domain model;
- preserve Family identity even when no active Membership remains;
- preserve historical Membership meaning;
- produce the applicable canonical Membership lifecycle event on success.

End Membership SHALL NOT:

- free the composite key for another Membership;
- delete the canonical historical Membership fact;
- end or delete Family automatically;
- end Relationship facts automatically;
- delete or mutate Person;
- revoke or grant Security authorization as Family-domain semantics.

## Establish Relationship

### Capability

`EstablishRelationship`

### Intent

Establish one canonical Family Relationship fact between two canonical Persons
inside one canonical Family context using the initial governed relationship
taxonomy.

### Required Semantics

Establish Relationship SHALL:

- require one canonical `FamilyId`;
- require two distinct canonical `PersonId` values;
- accept only relationship types authorized by the initial taxonomy;
- preserve Relationship and Membership as distinct concepts;
- normalize inverse parent-child expressions to the canonical `PARENT_OF`
  orientation;
- treat `CHILD_OF` as the inverse semantic view of the same canonical
  parent-child continuity;
- normalize endpoints for `SPOUSE_OF` and `SIBLING_OF` using the deterministic
  canonical UUID ordering defined by `Domain-Model.md`;
- reject duplicate creation through inverse or reversed symmetric expression;
- scope canonical Relationship identity to the applicable `FamilyId`;
- establish the lifecycle state required by the canonical domain model;
- produce the applicable canonical Relationship domain event on success.

Establish Relationship SHALL NOT:

- create a dedicated canonical Relationship identifier;
- create or activate Membership merely because a Relationship exists;
- infer authorization or Security permission;
- create a cross-family or global Relationship fact;
- infer Relationship merely from common Membership;
- allow a self-Relationship.

The ordering used for symmetric Relationship identity SHALL remain an identity
normalization mechanism only and SHALL carry no business ranking or authority.

## Retrieve Relationship

### Capability

`RetrieveRelationship`

### Intent

Retrieve the canonical Relationship continuity corresponding to one canonical
relationship fact within one `FamilyId`.

### Required Semantics

Retrieve Relationship SHALL:

- apply the same inverse and symmetric normalization rules used when canonical
  Relationship identity is established;
- resolve `CHILD_OF` to the same canonical parent-child continuity represented
  in `PARENT_OF` orientation;
- resolve reversed `SPOUSE_OF` and `SIBLING_OF` endpoints to the same canonical
  Relationship continuity;
- preserve `ENDED` Relationship history;
- distinguish Relationship absence from Person absence, Family absence,
  authorization denial, and Relationship conflict.

Retrieval SHALL NOT create or mutate Relationship, Membership, Person, or
authorization state.

## End Relationship

### Capability

`EndRelationship`

### Intent

Apply the canonical terminal transition to an existing Family Relationship.

### Required Semantics

End Relationship SHALL:

- resolve the target through canonical Relationship normalization;
- preserve the existing canonical Relationship continuity;
- transition only where permitted by the domain model;
- preserve historical Relationship meaning;
- produce the applicable canonical Relationship lifecycle event on success.

End Relationship SHALL NOT:

- free the canonical Relationship business key for silent replacement;
- automatically end Membership;
- automatically alter Family identity;
- mutate Person;
- imply Security authorization changes.

Re-establishment of an ended Relationship remains deferred. Until governed
semantics define whether re-establishment resumes an existing continuity or
creates an explicitly distinguishable historical fact, runtime behavior SHALL
fail closed rather than invent a new canonical Relationship.

## Resolve Family Boundary

### Capability

`ResolveFamilyBoundary`

### Intent

Resolve the canonical Family business boundary associated with a known
canonical `FamilyId`.

### Required Semantics

Resolve Family Boundary SHALL:

- derive boundary identity from canonical `FamilyId`;
- preserve one Family context as distinct from every other Family context;
- preserve the fact that one Person may participate in multiple Family
  contexts without merging those contexts;
- expose Family-domain boundary facts without converting them into Security
  policy;
- avoid deriving boundary identity from Membership composition,
  Relationship composition, Household, Identity, authorization, or storage
  representation.

The canonical Family Boundary identity is the applicable `FamilyId`; this
capability SHALL NOT introduce a separate boundary identifier.

Boundary resolution SHALL NOT itself grant or deny an operation. Security
remains authoritative for authorization decisions.

## Capability Invariants

All canonical Family capabilities SHALL preserve these invariants:

1. `FamilyId` remains the canonical Family identity.
2. Family continuity is independent from Membership composition.
3. Family creation does not imply Membership or Relationship creation.
4. Family and Household remain distinct; Household remains deferred.
5. Canonical Person identity remains owned by the Person domain.
6. Family capabilities SHALL use canonical `PersonId` without redefining it.
7. Membership identity is the canonical `(FamilyId, PersonId)` composite
   business key.
8. One composite Membership key identifies one canonical Membership continuity.
9. `ENDED` Membership preserves and continues to reserve that composite key.
10. Relationship remains distinct from Membership.
11. Parent-child inverse expressions identify one canonical Relationship
    continuity.
12. Symmetric Relationship endpoint reversal identifies one canonical
    Relationship continuity.
13. Relationship canonicalization is scoped by `FamilyId`.
14. Relationship ordering used for identity normalization carries no business
    meaning.
15. Family Boundary is derived from `FamilyId` and remains distinct from
    authorization policy.
16. Membership and Relationship facts do not themselves grant authorization.
17. Security remains authoritative for authorization decisions.
18. Infrastructure remains non-authoritative for Family business meaning.
19. Interfaces and transports SHALL NOT redefine canonical capability
    semantics.
20. Deferred Family semantics SHALL NOT be silently invented by application or
    runtime code.

## Cross-Domain Capability Boundaries

### Person

Family capabilities MAY reference canonical Persons through `PersonId`.

Family capabilities SHALL NOT create, redefine, merge, split, archive, delete,
or otherwise mutate canonical Person identity or Person lifecycle merely to
satisfy Family operations.

Person absence and invalid Person reference semantics SHALL remain distinct from
Family, Membership, and Relationship failures.

### Identity

Family capabilities SHALL NOT require an interactive platform Identity merely
for canonical Family or Person business existence unless a separately governed
workflow explicitly requires Identity participation.

Authentication and Identity lifecycle remain external to this capability
contract.

### Security

Security MAY authorize invocation of Family capabilities and MAY consume
approved Family, Membership, Relationship, and Boundary facts.

Family capabilities SHALL NOT own authorization policy, roles, permissions, or
access decisions.

Authorization denial SHALL remain distinct from Family-domain absence,
validation, lifecycle, and conflict semantics.

### Privacy and Governance

Privacy and governance rules MAY constrain disclosure, retention, erasure, and
processing of Family Core information.

Those rules SHALL NOT silently redefine Family identity, Membership continuity,
Relationship meaning, or Family Boundary semantics.

### Official Domain Plugins

Official plugins MAY consume canonical Family capabilities through governed
application contracts.

Plugins SHALL NOT redefine canonical Family identity, Membership lifecycle,
Relationship semantics, or Family Boundary meaning.

Plugin-local identifiers SHALL NOT become canonical Family Core identifiers
without an explicit compatibility and migration contract.

## Explicitly Deferred Capabilities

The following plausible capabilities are not authorized by this capability
baseline:

```text
SearchFamilies
ListFamilies
UpdateFamily
ArchiveFamily
DeleteFamily
RestoreFamily
FamilyHistory
ListMemberships
SearchMemberships
ReestablishMembership
DeleteMembership
ListRelationships
SearchRelationships
ReestablishRelationship
DeleteRelationship
CreateCrossFamilyRelationship
CreateGlobalRelationship
CreateHousehold
ResolveHousehold
```

Their omission is intentional.

### Search and Listing

Search and listing remain deferred because the specification does not yet
establish canonical filtering, ordering, pagination, visibility, disclosure,
cross-family query, or historical-query semantics.

This includes generic Family, Membership, and Relationship collection-query
capabilities.

### Generic Family Mutation

`UpdateFamily` remains deferred.

The current minimal Family aggregate has no canonical mutable attributes beyond
its stable identity contract. A generic update capability would therefore
invent unspecified Family state.

### Archive, Delete, and Restore

Family archival, deletion, restoration, and equivalent lifecycle capabilities
remain deferred because the canonical Family lifecycle does not currently
define those states or transitions.

Storage deletion SHALL NOT be treated as a substitute for a canonical Family
business lifecycle decision.

### Membership Re-establishment and Deletion

`ReestablishMembership` remains deferred because the domain model intentionally
leaves post-`ENDED` re-establishment semantics unresolved.

`DeleteMembership` is not a canonical capability. Historical Membership
continuity SHALL NOT be erased merely to simplify persistence.

Any future erasure requirement must reconcile Family history with applicable
Privacy, Data Architecture, and governance contracts.

### Relationship Re-establishment and Deletion

`ReestablishRelationship` remains deferred because post-`ENDED` Relationship
semantics remain unresolved.

`DeleteRelationship` is not a canonical capability. Ending a Relationship and
erasing its historical meaning are distinct concerns.

### Cross-Family and Global Relationships

Cross-family Relationship semantics and global Relationship semantics
independent from a Family context remain deferred.

The initial Relationship capability set SHALL operate only inside one canonical
`FamilyId`.

### Household

Household capabilities remain deferred.

No capability in this document SHALL infer Household from Family, shared
residence, Membership, Relationship, or any other Family Core fact.

## Application Boundary

The application layer SHALL orchestrate canonical Family capabilities without
becoming authoritative for Family business meaning.

`API.md` SHALL determine the concrete application-facing contract required by
the implementation-ready subset, including where applicable:

- command and query structures;
- use-case or handler names;
- input and output models;
- failure and result contracts;
- persistence ports;
- transaction expectations;
- domain-event handling responsibilities;
- coordination with Person and Security;
- compatibility and migration boundaries.

This document SHALL NOT freeze Python `execute(...)` signatures, CLI syntax,
HTTP routes, RPC methods, or equivalent implementation details.

## Persistence Boundary

Canonical Family capabilities require persistence where their business
semantics depend on durable identity, lifecycle, conflict detection, or
historical continuity.

The concrete persistence port belongs to the later application/API contract.

Persistence SHALL preserve:

- canonical `FamilyId`;
- Family continuity;
- canonical Person references;
- Membership composite identity and lifecycle;
- terminal Membership continuity;
- Membership temporal lifecycle facts required by `Domain-Model.md`;
- Relationship canonicalization and lifecycle;
- terminal Relationship continuity;
- Relationship establishment and end times required by `Domain-Model.md`;
- Family Boundary isolation;
- atomic conflict semantics required by the applicable capability.

Persistence SHALL NOT:

- invent dedicated Membership or Relationship identifiers;
- collapse Membership and Relationship;
- reinterpret storage absence as authorization denial;
- make database identity authoritative for Family Core identity;
- silently discard historical `ENDED` facts;
- introduce Household or Security policy as Family state.

This document does not prescribe database schemas, ORM models, tables,
collections, foreign keys, indexes, storage engines, or transaction technology.

### Temporal Persistence Boundary

Temporal persistence for the implementation-ready subset SHALL preserve the
business occurrence facts required by `Domain-Model.md` without making their
concrete storage representation canonical.

A conforming implementation MAY use entity fields, persistence metadata,
durable canonical event records, or an equivalent governed representation,
provided lifecycle state and the temporal fact produced by the same successful
operation cannot become observably inconsistent.

This temporal persistence requirement SHALL NOT be interpreted as authorization
for `FamilyHistory`, historical collection queries, event sourcing, event-store
technology, post-`ENDED` re-establishment, or Relationship evidence/provenance
capabilities.

## Failure Boundary

Capabilities SHALL preserve the canonical failure-category separations defined
by `Domain-Model.md`.

At minimum, application contracts SHALL NOT collapse:

- invalid canonical input;
- invalid Person reference;
- Family absence;
- Membership absence;
- Relationship absence;
- Membership conflict;
- Relationship conflict;
- invalid Membership transition;
- invalid Relationship transition;
- authorization denial;
- persistence or infrastructure failure.

This document does not define concrete exception classes, result objects,
transport status codes, CLI exit codes, or error serialization.

Those representations belong to `API.md` and applicable interface contracts.

## Deferred Capability Decisions

The following capability decisions remain intentionally deferred:

- Family search and listing semantics;
- Membership collection-query semantics;
- Relationship collection-query semantics;
- Family attributes beyond `FamilyId`;
- generic Family mutation;
- Family archival, deletion, restoration, and additional lifecycle states;
- Membership lifecycle states beyond the canonical initial set;
- Membership re-establishment after `ENDED`;
- dedicated Membership identifier;
- Relationship taxonomy beyond the canonical initial set;
- Relationship re-establishment after `ENDED`;
- dedicated Relationship identifier;
- cross-family Relationship semantics;
- global Relationship semantics;
- Relationship evidence and provenance capabilities;
- universal Family history/query capabilities;
- Household capabilities;
- concrete authorization mapping for individual operations;
- concrete Privacy, retention, disclosure, and erasure workflows;
- compatibility and migration mechanisms;
- concrete transaction mechanics;
- event dispatch and delivery mechanics;
- persistence technology.

Deferred decisions SHALL be resolved through specification or architectural
governance before runtime implementation depends on them.

Runtime code SHALL NOT silently convert a deferred capability into a canonical
Family contract.

## Implementation Gate

This document establishes the canonical Family capability baseline for the
current candidate minimal subset.

It does not, by itself, authorize Family runtime implementation.

Before any Family runtime slice proceeds, `API.md` and the applicable
cross-document reconciliation SHALL establish the remaining application-facing,
persistence, failure/result, compatibility, migration, and integration
contracts required by that slice.

The implementation-ready subset SHALL remain limited to capabilities whose
identity, lifecycle, invariants, failure semantics, persistence expectations,
and cross-domain boundaries are completely specified.

No runtime implementation SHALL use this capability document as authority to
implement an explicitly deferred capability.

## Normative References

- `docs/30-domains/family/README.md`
- `docs/30-domains/family/Vision.md`
- `docs/30-domains/family/Responsibilities.md`
- `docs/30-domains/family/Domain-Model.md`
- `docs/30-domains/person/README.md`
- `docs/30-domains/person/Domain-Model.md`
- `docs/30-domains/person/Capabilities.md`
- `docs/rfcs/RFC-0016-family-core-domain/RFC-0016-Family-Core-Domain.md`
- `docs/00-foundation/Domain-Architecture.md`
- `docs/00-foundation/Data-Architecture.md`
- `docs/00-foundation/Identity-Architecture.md`
- `docs/00-foundation/Security-Architecture.md`
- `docs/04-reference/Naming-Conventions.md`
- `docs/06-specifications/SPEC-0008-Naming-Conventions.md`
