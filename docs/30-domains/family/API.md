# Family Domain API

## Domain

`family`

## Purpose

This document defines the canonical application-facing API and persistence
boundary for the FamilyOS Family domain.

It translates the canonical Family capabilities into application contracts
without introducing transport protocols, database technology, framework
bindings, generic CRUD semantics, or authorization policy.

This contract is governed by RFC-0016 and SHALL be interpreted together with
the canonical Family specification, especially `Domain-Model.md` and
`Capabilities.md`.

## Contract Model

The initial application contract exposes the following canonical operations:

```text
CreateFamily
GetFamily

EstablishMembership
GetMembership
ActivateMembership
SuspendMembership
EndMembership

EstablishRelationship
GetRelationship
EndRelationship

ResolveFamilyBoundary
```

`GetFamily`, `GetMembership`, and `GetRelationship` are application query names
realizing the corresponding canonical Retrieve capabilities.

The initial persistence abstractions are conceptually named:

```text
FamilyRepository
MembershipRepository
RelationshipRepository
```

These names describe semantic persistence boundaries only.

This specification does not mandate Python ABCs, `Protocol`, base classes,
module paths, dependency-injection frameworks, ORM repositories, or concrete
adapter technology.

## Application Boundary

The application layer SHALL orchestrate Family capabilities while the Family
domain remains authoritative for Family business meaning and invariants.

Application operations SHALL:

- accept application-facing inputs;
- resolve canonical domain identities;
- invoke canonical Family-domain behavior;
- coordinate persistence through governed persistence abstractions;
- preserve lifecycle and historical continuity;
- preserve failure-category separation;
- maintain atomicity where partial success would violate domain invariants;
- coordinate with Person and Security without absorbing their ownership.

Application operations SHALL NOT:

- redefine `FamilyId`;
- redefine `PersonId`;
- invent Membership or Relationship identifiers;
- reinterpret Household as Family;
- treat authorization policy as Family state;
- make storage representations authoritative for Family business identity;
- introduce generic CRUD operations not authorized by `Capabilities.md`;
- silently implement deferred Family semantics.

This specification defines semantic contracts. It does not freeze concrete
Python `execute(...)` signatures, constructors, DTO implementation classes,
framework annotations, CLI commands, HTTP routes, RPC methods, or equivalent
interface details.

## Create Family

### Command

`CreateFamily`

### Input Semantics

Create Family requires no canonical intrinsic Family input beyond the authority
to request creation.

The caller SHALL NOT provide a canonical `FamilyId` for normal creation.

Canonical `FamilyId` generation belongs to the application/domain creation
workflow and SHALL produce UUID version 4 identity according to
`Domain-Model.md`.

Creation input SHALL NOT require:

- Membership;
- Person;
- Household;
- authentication Identity as Family state;
- Security authorization data as Family state;
- plugin-specific identifiers or records.

### Application Ordering

Create Family SHALL order failure-sensitive work so that no successful
persistence is observable before all pre-persistence canonical values required
for the successful result are valid.

The conceptual ordering is:

```text
generate FamilyId
construct canonical Family
obtain and validate FamilyCreated occurrence time
construct canonical FamilyCreated
persist Family atomically as new canonical identity
return successful creation result
```

If identity generation fails, persistence SHALL NOT occur.

If Family construction fails, persistence SHALL NOT occur.

If event occurrence time is invalid or unavailable, persistence SHALL NOT
occur.

If persistence fails, a successful creation result SHALL NOT be returned.

### Result Semantics

Successful Create Family SHALL provide:

- the created canonical Family;
- the canonical `FamilyCreated` domain event or an application result preserving
  that event fact.

The exact concrete result type remains an implementation decision until runtime
implementation is authorized.

### Conflict Semantics

If the generated or proposed canonical `FamilyId` conflicts with an established
Family identity, creation SHALL fail with Family conflict semantics.

Conflict SHALL NOT silently overwrite or replace an existing Family.

## Get Family

### Query

`GetFamily`

### Input Semantics

Get Family requires one canonical `FamilyId`.

Application code SHALL NOT silently coerce legacy strings, plugin identifiers,
storage keys, or other external identifiers into canonical `FamilyId`.

### Result Semantics

Get Family has three semantically distinct execution categories:

```text
Family present
Family absent
Execution failure
```

Family absence is an ordinary query outcome.

Family absence SHALL remain distinct from:

- invalid `FamilyId`;
- authorization denial;
- privacy/disclosure restriction;
- persistence failure;
- compatibility or migration failure.

The concrete application representation of absence remains open. A runtime
implementation MAY use `None`, an explicit result type, or another governed
representation provided the semantic distinction is preserved.

## Establish Membership

### Command

`EstablishMembership`

### Input Semantics

Establish Membership requires:

- one canonical `FamilyId`;
- one canonical `PersonId`.

The application layer SHALL verify or otherwise resolve the required Family and
Person references through governed contracts before successful establishment is
committed.

Person existence verification SHALL NOT transfer Person ownership to Family.

### Canonical Identity

Membership identity is the composite business key:

```text
(FamilyId, PersonId)
```

No dedicated canonical Membership identifier is introduced.

### Application Ordering

The operation SHALL establish all preconditions before successful Membership
persistence becomes observable.

Conceptually:

```text
validate FamilyId
validate PersonId
resolve required Family existence
resolve required Person existence
check canonical Membership-key conflict
construct canonical PENDING Membership
obtain and validate event occurrence time
construct FamilyMembershipCreated
persist Membership atomically as new composite identity
return successful establishment result
```

If required Family or Person resolution fails, Membership persistence SHALL NOT
occur.

If the composite key already exists in any canonical Membership state,
including `ENDED`, establishment SHALL fail with Membership conflict semantics.

If event construction fails, Membership persistence SHALL NOT occur.

If persistence fails, a successful establishment result SHALL NOT be returned.

### Result Semantics

Success SHALL return or otherwise preserve:

- the canonical Membership;
- the canonical `FamilyMembershipCreated` event.

Re-establishment after `ENDED` remains deferred and SHALL fail closed.

## Get Membership

### Query

`GetMembership`

### Input Semantics

Get Membership requires:

- one canonical `FamilyId`;
- one canonical `PersonId`.

The pair SHALL be interpreted as the canonical Membership business key.

### Result Semantics

Get Membership SHALL distinguish:

```text
Membership present
Membership absent
Execution failure
```

An `ENDED` Membership remains present historical Membership state and SHALL NOT
be reported as absent merely because it is no longer currently valid.

Membership absence SHALL remain distinct from:

- Family absence;
- Person absence;
- invalid canonical input;
- authorization denial;
- invalid lifecycle transition;
- persistence failure.

Retrieval SHALL NOT create or reactivate Membership.

## Activate Membership

### Command

`ActivateMembership`

Activate Membership operates on one existing canonical Membership identified by
`(FamilyId, PersonId)`.

The application layer SHALL:

- retrieve the canonical Membership;
- preserve Membership identity;
- validate that the current state permits activation according to
  `Domain-Model.md`;
- obtain and validate the canonical event occurrence time;
- apply the canonical lifecycle transition;
- persist the new Membership state and required event outcome atomically;
- return successful transition semantics only after persistence succeeds.

The operation SHALL NOT create a replacement Membership.

An `ENDED` Membership SHALL NOT be activated.

## Suspend Membership

### Command

`SuspendMembership`

Suspend Membership operates on one existing canonical Membership identified by
`(FamilyId, PersonId)`.

The operation SHALL:

- require the canonical source state authorized by `Domain-Model.md`;
- preserve Membership identity and historical continuity;
- construct the canonical `FamilyMembershipSuspended` fact;
- persist the state transition atomically;
- avoid modifying Family identity, Person identity, or Relationship facts.

Invalid source state SHALL remain distinct from Membership absence.

## End Membership

### Command

`EndMembership`

End Membership applies the canonical terminal Membership transition.

The operation SHALL:

- operate on the existing canonical Membership continuity;
- validate an allowed source state;
- preserve `(FamilyId, PersonId)` permanently as the historical composite key;
- construct the canonical `FamilyMembershipEnded` event;
- persist the terminal state atomically;
- preserve the Family even if no active Membership remains.

`ENDED` SHALL remain terminal.

End Membership SHALL NOT free the composite key for reuse.

End Membership SHALL NOT delete Family, Person, or Relationship facts.

## Establish Relationship

### Command

`EstablishRelationship`

### Input Semantics

Establish Relationship requires:

- one canonical `FamilyId`;
- one source canonical `PersonId`;
- one target canonical `PersonId`;
- one canonical relationship type from the initial taxonomy.

The two Person identifiers SHALL be distinct.

Required Family and Person references SHALL be resolved through governed
contracts before successful Relationship persistence.

### Canonicalization

The application layer SHALL normalize Relationship identity before conflict
detection and persistence.

For parent-child semantics:

```text
PARENT_OF(parent, child)
```

is the canonical orientation.

An input expressed as:

```text
CHILD_OF(child, parent)
```

SHALL normalize to the same canonical parent-child continuity.

For symmetric types:

```text
SPOUSE_OF
SIBLING_OF
```

the two canonical `PersonId` UUID values SHALL be deterministically ordered
according to `Domain-Model.md`.

Endpoint ordering is identity normalization only and SHALL NOT create business
meaning.

### Application Ordering

Conceptually:

```text
validate FamilyId
validate source PersonId
validate target PersonId
validate relationship type
reject self-relationship
resolve required Family existence
resolve required Person existence
normalize canonical Relationship business key
check canonical Relationship conflict
construct ESTABLISHED Relationship
obtain and validate occurrence time
construct FamilyRelationshipEstablished
persist Relationship atomically
return successful establishment result
```

Inverse or reversed-symmetric duplicate creation SHALL fail with Relationship
conflict semantics.

### Result Semantics

Success SHALL preserve:

- the canonical normalized Relationship;
- the canonical `FamilyRelationshipEstablished` event.

No dedicated canonical Relationship identifier is introduced.

## Get Relationship

### Query

`GetRelationship`

Get Relationship requires enough canonical input to derive the canonical
Relationship business key inside one `FamilyId`.

The query SHALL apply exactly the same normalization algorithm used by
Establish Relationship.

Therefore:

- `PARENT_OF(parent, child)` and `CHILD_OF(child, parent)` resolve to the same
  canonical continuity;
- `SPOUSE_OF(A, B)` and `SPOUSE_OF(B, A)` resolve to the same canonical
  continuity;
- `SIBLING_OF(A, B)` and `SIBLING_OF(B, A)` resolve to the same canonical
  continuity.

An `ENDED` Relationship remains present historical Relationship state.

Relationship absence SHALL remain distinct from Family absence, Person absence,
invalid input, authorization denial, Relationship conflict, and persistence
failure.

## End Relationship

### Command

`EndRelationship`

End Relationship SHALL:

- derive the canonical Relationship business key using the governed
  normalization rules;
- retrieve the existing Relationship continuity;
- validate the allowed lifecycle source state;
- obtain and validate event occurrence time;
- construct the canonical `FamilyRelationshipEnded` event;
- persist the terminal transition atomically;
- preserve historical continuity.

`ENDED` is terminal for the current Relationship continuity.

Re-establishment after `ENDED` remains deferred and SHALL fail closed.

Ending Relationship SHALL NOT mutate Membership, Family identity, Person
identity, or Security authorization.

## Resolve Family Boundary

### Query

`ResolveFamilyBoundary`

Resolve Family Boundary requires one canonical `FamilyId`.

The result SHALL preserve the domain rule:

```text
Family Boundary identity == FamilyId
```

No separate Family Boundary identifier is introduced.

Boundary resolution SHALL NOT depend on:

- Membership composition;
- Relationship composition;
- Household;
- authentication Identity;
- authorization policy;
- persistence representation.

Boundary resolution provides Family-domain business context only.

It SHALL NOT itself grant or deny authorization.

## Persistence Boundary

Family application operations require persistence abstractions that preserve
canonical identity, lifecycle, conflict, historical, and absence semantics.

The initial conceptual persistence abstractions are:

```text
FamilyRepository
MembershipRepository
RelationshipRepository
```

Persistence abstractions are application ports.

Infrastructure provides adapters.

The application/domain contract remains authoritative for semantics.

## Family Repository Contract

The minimum conceptual Family persistence operations are:

```text
save(Family)
get(FamilyId)
```

### `save(Family)`

For canonical creation, `save(Family)` SHALL provide create-only semantics.

Saving a Family whose `FamilyId` already exists SHALL produce Family conflict
rather than overwrite the existing Family.

### `get(FamilyId)`

`get(FamilyId)` SHALL return either:

- the canonical Family; or
- ordinary Family absence.

Persistence failure SHALL NOT be translated into ordinary absence.

No canonical Family `list`, `search`, `update`, `archive`, `delete`, `restore`,
or history operation is introduced by this contract.

## Membership Repository Contract

The minimum conceptual Membership persistence operations are:

```text
save(Membership)
get(FamilyId, PersonId)
```

### `save(Membership)`

The persistence contract SHALL distinguish:

- initial create-only Membership persistence;
- persistence of a valid lifecycle transition on the existing canonical
  Membership continuity.

Initial save SHALL reject an already established `(FamilyId, PersonId)` key in
every lifecycle state, including `ENDED`.

Lifecycle save SHALL update only the same canonical Membership continuity and
SHALL NOT silently create a second Membership.

### `get(FamilyId, PersonId)`

The operation SHALL return either:

- the canonical Membership, including `ENDED`; or
- ordinary Membership absence.

Persistence failure SHALL remain distinct from Membership absence.

No canonical Membership search, list, delete, history, or re-establishment
repository operation is established here.

## Relationship Repository Contract

The minimum conceptual Relationship persistence operations are:

```text
save(Relationship)
get(canonical relationship business key)
```

The application/domain boundary owns Relationship normalization.

Infrastructure SHALL NOT implement a competing normalization algorithm.

### `save(Relationship)`

Initial persistence SHALL be create-only for the canonical normalized
Relationship business key.

Inverse parent-child expressions and reversed symmetric endpoints SHALL collide
with the same canonical key rather than create duplicate records.

Lifecycle persistence SHALL update only the same canonical Relationship
continuity.

An `ENDED` canonical Relationship key SHALL remain reserved.

### `get(...)`

Retrieval SHALL use the canonical normalized business key and return either:

- the canonical Relationship, including `ENDED`; or
- ordinary Relationship absence.

Persistence failure SHALL remain distinct from Relationship absence.

No canonical Relationship list, search, delete, re-establish, global, or
cross-family repository operation is introduced.

## Persistence Invariants

Persistence SHALL preserve:

1. canonical UUIDv4 `FamilyId`;
2. canonical `PersonId` references;
3. Family identity uniqueness;
4. Membership composite-key uniqueness;
5. reservation of Membership identity after `ENDED`;
6. Relationship canonicalization;
7. inverse parent-child single continuity;
8. symmetric Relationship single continuity;
9. reservation of Relationship continuity after `ENDED`;
10. Family Boundary isolation by `FamilyId`;
11. historical state required by the canonical lifecycle;
12. absence-versus-failure distinctions.

Persistence SHALL NOT:

- use database identity as canonical Family identity;
- invent Membership or Relationship identifiers;
- silently overwrite create-only canonical identity;
- collapse Family, Membership, and Relationship;
- treat `ENDED` as absence;
- erase historical continuity as part of an ordinary lifecycle operation;
- introduce Household;
- encode Security policy as Family Core state.

## Persistence Absence Semantics

Ordinary persistence absence is a query result, not an infrastructure failure.

The following distinctions SHALL be preserved:

```text
Family absent != Family repository failure
Membership absent != Membership repository failure
Relationship absent != Relationship repository failure
```

Infrastructure adapters SHALL NOT convert connection errors, corruption,
serialization failures, transaction failures, or equivalent technical failures
into ordinary domain absence.

## Transaction Boundary

Operations that modify canonical Family state SHALL be atomic with respect to
the business invariants they establish.

At minimum:

- Create Family SHALL not expose successful Family persistence without the
  application being able to produce its successful canonical result;
- Establish Membership SHALL not expose partial establishment;
- Membership lifecycle transitions SHALL not expose a new state if the
  operation ultimately reports failure;
- Establish Relationship SHALL not expose partial establishment;
- Relationship lifecycle transitions SHALL not expose a new state if the
  operation ultimately reports failure.

The concrete transaction mechanism remains an infrastructure decision.

This specification does not mandate database transactions, unit-of-work
frameworks, event sourcing, distributed transactions, or any particular
technology.

## Domain Event Boundary

The application layer SHALL preserve canonical domain-event meaning.

Canonical events in the current Family model include:

```text
FamilyCreated
FamilyMembershipCreated
FamilyMembershipActivated
FamilyMembershipSuspended
FamilyMembershipReactivated
FamilyMembershipEnded
FamilyRelationshipEstablished
FamilyRelationshipEnded
```

Successful application operations SHALL construct or preserve the applicable
canonical event fact before reporting success.

Event delivery is separate from event meaning.

This document does not mandate:

- an event bus;
- synchronous or asynchronous delivery;
- outbox technology;
- broker technology;
- event serialization;
- retry policy;
- event ordering guarantees across aggregates;
- event retention technology.

Delivery failure semantics remain separately governed and SHALL NOT silently
rewrite the underlying canonical domain fact.

## Family Core Temporal Persistence Contract

Application operations that establish or transition canonical Membership or
Relationship lifecycle state SHALL preserve the occurrence time required by
`Domain-Model.md` as part of the successful persistence outcome.

For the initial contract:

- `FamilyMembershipCreated.occurred_at` is the canonical Membership
  establishment occurrence time;
- Membership lifecycle event `occurred_at` values are the canonical effective
  occurrence times for the corresponding transitions;
- `FamilyRelationshipEstablished.occurred_at` is the canonical Relationship
  establishment occurrence time;
- `FamilyRelationshipEnded.occurred_at` is the canonical Relationship end
  occurrence time.

A successful state-changing operation SHALL NOT report success if the required
temporal fact for that same transition cannot be durably preserved.

The lifecycle continuity update and its required temporal occurrence fact SHALL
therefore share one governed atomic success boundary. The concrete transaction,
storage, and representation mechanism remains an infrastructure decision.

The minimum `save(...)` / `get(...)` repository descriptions in this document
remain semantic baselines rather than a prohibition on a later governed port
extension required to satisfy this temporal persistence contract.

This contract does not require domain entities to expose timestamp fields and
does not require event sourcing, an event store, an outbox, event retention, or
event delivery infrastructure.

No `FamilyHistory`, Membership history-query, Relationship history-query, list,
search, delete, or re-establishment operation is introduced by this contract.
Those capabilities remain deferred where already identified by the Family
specification.

## Failure and Result Boundary

Application contracts SHALL preserve the semantic failure categories established
by `Domain-Model.md`.

The minimum application-visible distinctions are:

- invalid Family input;
- invalid Person reference;
- Family absence;
- Family conflict;
- Membership absence;
- Membership conflict;
- invalid Membership transition;
- Relationship absence;
- Relationship conflict;
- invalid Relationship transition;
- authorization denial;
- privacy or disclosure restriction where applicable;
- compatibility or migration failure where applicable;
- infrastructure failure.

These categories are semantic contracts.

This document does not mandate a concrete exception hierarchy.

It does not mandate result enums, discriminated unions, HTTP status codes, CLI
exit codes, error codes, or message formats.

Runtime implementation MAY choose concrete representations only if the semantic
distinctions above remain observable where applicable.

## Security Boundary

Family application operations are subject to Security authorization in their
operational context.

Family Core defines business facts and lifecycle behavior.

Security remains authoritative for:

- authorization policy;
- roles;
- permissions;
- access decisions;
- enforcement.

Therefore:

```text
Family exists != caller is authorized
Membership ACTIVE != caller is authorized
Relationship exists != caller is authorized
Family Boundary resolved != caller is authorized
```

Authorization denial SHALL remain semantically distinct from canonical domain
absence.

This API does not define concrete roles, permissions, tokens, policy
expressions, or authorization-engine interfaces.

## Privacy and Disclosure Boundary

Family Core may contain sensitive family context.

Application and interface layers SHALL expose only information authorized for
the applicable operation and context.

A successful internal `GetFamily`, `GetMembership`, or `GetRelationship`
resolution SHALL NOT by itself require unrestricted external disclosure of the
entire canonical object.

Privacy/disclosure decisions SHALL NOT redefine canonical Family Core identity
or lifecycle semantics.

Concrete field-level disclosure, consent, retention, and erasure policies
remain separately governed.

## Person Integration Boundary

Family application operations MAY resolve canonical Person references through
the Person domain's governed application/reference contract.

Family SHALL NOT:

- create an alternate Person;
- redefine `PersonId`;
- reinterpret Person absence as Family absence;
- mutate Person lifecycle as a side effect of Family operations.

A missing required Person reference SHALL remain distinguishable from
Membership or Relationship conflict.

The exact cross-domain lookup mechanism remains an application integration
decision.

## Infrastructure Boundary

Infrastructure MAY provide:

- repository adapters;
- transaction support;
- serialization;
- storage;
- caches where governed;
- event delivery;
- compatibility adapters.

Infrastructure SHALL NOT own:

- Family identity;
- Membership identity semantics;
- Relationship canonicalization;
- Family lifecycle meaning;
- Membership lifecycle meaning;
- Relationship lifecycle meaning;
- Family Boundary meaning;
- authorization policy.

This specification does not prescribe SQL, NoSQL, files, YAML, JSON, ORM
technology, cloud services, cache technology, or database schema.

## Transport Boundary

CLI, HTTP, RPC, messaging, UI, plugin interfaces, and other transports are
adapters around the application contract.

Transport adapters MAY define transport-specific representations.

They SHALL NOT redefine canonical Family semantics.

This document does not mandate:

- CLI commands;
- HTTP endpoints;
- REST resources;
- GraphQL schemas;
- RPC methods;
- transport DTO classes;
- status codes;
- serialization formats.

## Compatibility and Migration Boundary

Legacy family-like, membership-like, relationship-like, plugin-local, or storage
identifiers are compatibility inputs only.

They SHALL NOT be treated as canonical Family Core identity by implicit
conversion.

Compatibility mapping SHALL be explicit and SHALL preserve:

- canonical `FamilyId`;
- canonical `PersonId`;
- Membership composite identity;
- Relationship canonicalization;
- Family Boundary isolation;
- historical continuity.

Compatibility handling SHALL fail closed on ambiguity.

Migration SHALL NOT silently:

- merge distinct Families;
- split one canonical Family continuity;
- recreate an `ENDED` Membership as a new Membership;
- recreate an `ENDED` Relationship as a new Relationship;
- create Household semantics;
- infer authorization.

Concrete migration mechanisms remain deferred.

## Explicitly Non-Normative API

The following operations are not canonical Family application API in the
current baseline:

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

No interface, repository, application service, or infrastructure adapter SHALL
make these operations canonical merely because they are common CRUD or query
patterns.

## Deferred API Decisions

The following decisions remain intentionally deferred:

- Family search and listing application contracts;
- Membership collection-query contracts;
- Relationship collection-query contracts;
- Family mutation beyond canonical creation;
- Family archival, deletion, restoration, and additional lifecycle operations;
- Membership re-establishment after `ENDED`;
- Relationship re-establishment after `ENDED`;
- dedicated Membership identifier;
- dedicated Relationship identifier;
- relationship taxonomy expansion;
- cross-family Relationship API;
- global Relationship API;
- Household API;
- universal historical-query API;
- concrete application request and result classes;
- concrete exception hierarchy;
- concrete Python method signatures;
- concrete repository interface technology;
- concrete transaction technology;
- event dispatch and delivery mechanics;
- concrete Security authorization mapping per operation;
- field-level privacy and disclosure rules;
- concrete retention and erasure workflows;
- compatibility and migration mechanisms;
- transport contracts.

Deferred decisions SHALL be resolved before runtime implementation depends on
them.

Runtime code SHALL NOT silently convert a deferred API or persistence decision
into a canonical Family contract.

## Implementation Gate

This document establishes the canonical initial Family application API and
persistence boundary for the current candidate minimal subset.

It does not, by itself, authorize Family runtime implementation.

Before runtime implementation begins, the Family specification SHALL undergo
final cross-document reconciliation against:

- RFC-0016;
- `README.md`;
- `Vision.md`;
- `Responsibilities.md`;
- `Domain-Model.md`;
- `Capabilities.md`;
- this API contract;
- applicable Person, Security, Data Architecture, Event Architecture,
  compatibility, migration, and privacy requirements.

Runtime implementation SHALL remain blocked if that reconciliation identifies a
foundational ambiguity, contradictory invariant, missing required application
contract, or unresolved persistence/failure semantic needed by the candidate
runtime slice.

No application, infrastructure, interface, plugin, or migration code SHALL
invent unresolved Family semantics merely to begin implementation early.

## Normative References

- `docs/30-domains/family/README.md`
- `docs/30-domains/family/Vision.md`
- `docs/30-domains/family/Responsibilities.md`
- `docs/30-domains/family/Domain-Model.md`
- `docs/30-domains/family/Capabilities.md`
- `docs/30-domains/person/README.md`
- `docs/30-domains/person/Domain-Model.md`
- `docs/30-domains/person/API.md`
- `docs/rfcs/RFC-0016-family-core-domain/RFC-0016-Family-Core-Domain.md`
- `docs/00-foundation/Application-Architecture.md`
- `docs/00-foundation/API-Architecture.md`
- `docs/00-foundation/Domain-Architecture.md`
- `docs/00-foundation/Data-Architecture.md`
- `docs/00-foundation/Event-Architecture.md`
- `docs/00-foundation/Identity-Architecture.md`
- `docs/00-foundation/Security-Architecture.md`
- `docs/04-reference/Naming-Conventions.md`
- `docs/06-specifications/SPEC-0008-Naming-Conventions.md`
