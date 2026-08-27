# Person Domain API

## Domain

`person`

## Purpose

This document defines the canonical application-facing API and persistence
boundary for the FamilyOS Person domain.

It translates the canonical Person capabilities into application contracts
without introducing runtime implementation details, transport protocols,
storage technology, or generic CRUD semantics.

This contract is governed by RFC-0016 and the canonical Person specification.

## Contract Model

The initial application contract exposes two concrete application operations:

```text
CreatePerson
GetPerson
```

`CreatePerson` realizes the canonical Create Person capability.

`GetPerson` is the application query realizing the canonical Retrieve Person
capability. The capability name and application operation name intentionally
differ because FamilyOS naming conventions use `Get...` for retrieval queries.

`EvolvePerson` remains a capability category. No unrestricted generic
`UpdatePerson` command is normative.

`ReferencePerson` remains a cross-domain reference capability rather than a
standalone CRUD operation.

The initial persistence contract is conceptually named:

```text
PersonRepository
```

The name describes the required Person persistence abstraction. This
specification does not mandate a Python ABC, `Protocol`, base class, concrete
interface shape, or module path.

## Application Boundary

The application layer SHALL orchestrate Person capabilities while the Person
domain remains authoritative for Person business meaning and invariants.

Application operations SHALL:

- accept application-facing inputs;
- invoke canonical Person-domain behavior;
- preserve Person invariants and continuity;
- coordinate persistence through the Person persistence abstraction;
- distinguish business, absence, authorization, and infrastructure outcomes
  where those distinctions are relevant;
- avoid moving domain rules into interface or infrastructure code.

Application operations SHALL NOT:

- redefine `PersonId`;
- redefine Person invariants;
- treat authentication Identity as Person;
- infer authorization from Person existence;
- make storage representations authoritative for Person;
- expose generic mutation merely for implementation convenience.

This specification defines semantic contracts. It does not freeze Python
`execute(...)` signatures, constructors, dependency-injection mechanics, DTO
classes, framework annotations, or interface adapters.

## Create Person

### Command

`CreatePerson`

`CreatePerson` is the canonical application command for creating a new Person.

### Input Semantics

The command SHALL accept only information whose business meaning is valid for
canonical Person creation.

The exact intrinsic Person attributes remain deferred by the domain model.
Therefore this specification does not yet define a final concrete request DTO
or field list.

Creation input SHALL NOT require:

- authentication credentials as Person state;
- an interactive Identity;
- Family Membership;
- authorization data as Person state;
- plugin-specific records.

The caller SHALL NOT provide or depend on the internal backing representation of
`PersonId`.

The concrete `PersonId` generation strategy remains deferred.

### Success Semantics

Successful `CreatePerson` execution SHALL result in exactly one valid canonical
Person being established and persisted.

Success SHALL preserve:

- canonical Person identity;
- Person continuity;
- Person invariants;
- Person ownership boundaries;
- separation from Identity;
- separation from Family Membership;
- separation from authorization policy;
- separation from plugin-owned records.

The successful application outcome SHALL make the created Person, or an
application representation sufficient to identify the created Person,
available to the caller.

The exact result type remains an implementation-contract decision.

### Failure Semantics

Creation SHALL fail rather than persist invalid Person state.

The application contract SHALL distinguish, when applicable:

- invalid Person-domain input;
- conflict with canonical Person identity or creation invariants;
- authorization denial;
- infrastructure or persistence failure.

These categories are semantic distinctions.

This specification does not mandate Python exception classes, result unions,
error codes, HTTP status codes, CLI exit codes, or transport error envelopes.

### Event Semantics

Successful Person creation SHALL carry the canonical `PersonCreated` domain
event semantics defined by the Person domain model.

Persistence and event handling SHALL preserve the rule that a failed creation
must not be represented externally as a successfully created Person.

This P5 slice does not mandate:

- an event bus;
- an outbox;
- synchronous or asynchronous dispatch;
- a transaction framework;
- broker technology;
- event transport;
- final event payload representation;
- final event metadata or versioning representation.

Those mechanics SHALL be specified before runtime implementation depends on
them.

## Get Person

### Query

`GetPerson`

`GetPerson` is the canonical application query realizing the Retrieve Person
capability.

### Input Semantics

`GetPerson` SHALL address the requested Person through the canonical `PersonId`
contract.

Consumers SHALL treat `PersonId` as opaque.

Legacy string-based `person_id` values SHALL NOT determine the canonical
`PersonId` representation.

### Success Semantics

When the requested Person exists and the operation is permitted in its
operational context, `GetPerson` SHALL produce the canonical Person business
state, or an application representation preserving the required canonical
meaning.

Successful retrieval SHALL NOT transfer ownership of Person invariants to the
caller.

Successful retrieval SHALL NOT imply that every Person attribute is appropriate
for every caller or transport representation.

### Absence Semantics

`GetPerson` SHALL distinguish absence of the requested Person from successful
retrieval.

A not-found outcome SHALL remain semantically distinct from:

- an invalid Person identifier;
- authorization denial;
- privacy-based disclosure restrictions;
- infrastructure failure;
- persistence corruption.

This P5 slice does not mandate whether the application represents not-found as
`None`, an optional value, a result object, a typed failure, or an exception.

Transport layers SHALL map the semantic outcome without redefining it.

### Failure Semantics

Retrieval failures SHALL preserve the distinction between domain/application
meaning and infrastructure failure.

The application layer SHALL NOT expose storage-engine errors as canonical Person
business semantics.

Concrete error classes and transport mappings remain deferred.

## Evolve Person Boundary

`EvolvePerson` remains a canonical capability category but does not become a
concrete generic application command in this P5 slice.

No application API SHALL introduce an unrestricted `UpdatePerson` command or
generic patch contract.

Concrete Person mutation commands MAY be added only after the governing Person
specification defines:

- the intrinsic state being changed;
- the business intent of the change;
- applicable invariants;
- lifecycle implications;
- event semantics;
- compatibility implications.

The absence of a concrete mutation command in P5 is intentional.

## Reference Person Boundary

`ReferencePerson` allows approved FamilyOS domains and components to refer to a
canonical Person through `PersonId` without acquiring ownership of Person.

A reference contract SHALL:

- preserve `PersonId` as opaque;
- preserve Person ownership inside the Person domain;
- avoid embedding authentication semantics;
- avoid implying Family Membership;
- avoid implying authorization;
- avoid redefining Person through plugin-specific identifiers.

This P5 slice does not require a standalone `ReferencePerson` command or query.

Cross-domain consumers MAY carry canonical `PersonId` references according to
their own governed domain contracts.

Reference semantics SHALL NOT require disclosure of the complete Person
aggregate.

## Persistence Boundary

Persistence supports canonical Person capabilities but SHALL remain subordinate
to Person domain semantics.

The application layer SHALL depend on a Person persistence abstraction rather
than a concrete storage technology.

Infrastructure SHALL implement that abstraction without becoming authoritative
for:

- Person identity meaning;
- Person invariants;
- Person continuity;
- Person lifecycle;
- Person capability semantics.

## Person Repository Contract

The initial canonical persistence abstraction is conceptually named
`PersonRepository`.

Its minimum normative semantic operations are:

```text
save(Person)
get(PersonId)
```

These signatures are semantic notation only.

They SHALL NOT be interpreted as frozen Python signatures.

No `exists`, `list`, `search`, `delete`, `archive`, `restore`, or history
operation is normative in this P5 slice.

Additional repository operations SHALL be introduced only when required by an
accepted canonical capability or application contract.

## Save Person

The persistence abstraction SHALL support saving canonical Person state.

Save semantics SHALL:

- preserve canonical `PersonId`;
- preserve Person invariants;
- preserve Person continuity;
- persist a state that represents the successful canonical domain operation;
- avoid generating competing Person business identity in infrastructure;
- avoid silently translating invalid domain state into valid persisted state.

Storage-specific serialization, schema, concurrency, locking, optimistic
versioning, and transaction mechanics remain deferred unless required by a
later normative contract.

## Get Person From Persistence

The persistence abstraction SHALL support retrieving a Person by canonical
`PersonId`.

Retrieval semantics SHALL:

- use canonical Person identity;
- reconstruct or return Person state without changing its business meaning;
- distinguish presence from absence;
- avoid making storage identifiers canonical Person identifiers;
- avoid interpreting storage absence as authorization denial.

The concrete repository-level absence representation remains deferred.

## Persistence Invariants

Every Person persistence adapter SHALL preserve these invariants:

1. Canonical `PersonId` remains stable across persistence round trips.
2. Infrastructure does not redefine Person identity.
3. Persisted Person state cannot bypass domain invariants.
4. Persistence does not merge Person with Identity.
5. Persistence does not make Family Membership intrinsic Person state.
6. Persistence does not encode authorization as Person business truth.
7. Plugin-specific identifiers do not replace canonical `PersonId`.
8. Storage technology remains replaceable without changing Person business
   meaning.
9. Absence remains distinguishable from infrastructure failure.
10. Deferred domain decisions are not silently fixed by persistence design.

## Persistence Absence Semantics

The persistence boundary SHALL represent the difference between:

```text
Person present
Person absent
Persistence failure
```

The exact technical representation remains deferred.

Application code SHALL translate repository outcomes into application semantics
without converting infrastructure failures into ordinary not-found outcomes.

## Transaction Boundary

A successful Person operation SHALL not expose a state that contradicts the
canonical result of that operation.

For creation, persistence and externally observable successful creation
semantics SHALL remain consistent.

P5 does not mandate a concrete unit-of-work implementation, database
transaction, distributed transaction, locking strategy, or consistency
technology.

A later implementation contract SHALL define transaction mechanics if they are
required to preserve the normative semantics.

## Domain Event Boundary

Domain events describe meaningful Person-domain facts.

`PersonCreated` is the only canonical Person domain event currently normative.

Application orchestration SHALL preserve its domain meaning.

Infrastructure MAY transport or persist domain events only through governed
adapters.

Infrastructure SHALL NOT redefine a domain event as an infrastructure event
merely because it delivers that event.

Final event dispatch, durability, ordering, retry, metadata, and versioning
contracts remain deferred.

## Security Boundary

Person application operations are subject to Security authorization in their
operational context.

Person SHALL define business capabilities and facts.

Security SHALL remain authoritative for authorization evaluation.

Therefore:

```text
Person exists != caller is authorized
Person retrievable in principle != caller may retrieve Person
Person reference != authorization grant
Family Membership != unrestricted authorization
```

Authorization denial SHALL remain distinguishable from Person absence wherever
the applicable Security and privacy contract permits that distinction to be
observable.

P5 does not define concrete roles, permissions, policy expressions, tokens, or
authorization-engine APIs.

## Privacy Boundary

Person data is family-sensitive personal information and SHALL be handled
according to FamilyOS privacy, security, and data-governance requirements.

Application and interface layers SHALL expose only Person information required
for the approved operation and context.

`GetPerson` SHALL NOT be interpreted as a requirement to disclose every
persisted Person attribute to every authorized consumer.

Reference-only consumers SHOULD use `PersonId` or an approved minimal
representation rather than requiring the complete Person aggregate.

Concrete field-level disclosure rules remain deferred until canonical intrinsic
Person attributes and applicable privacy policies are specified.

## Infrastructure Boundary

Infrastructure MAY provide:

- repository adapters;
- serialization;
- storage;
- transaction support;
- event delivery;
- caching where governed.

Infrastructure SHALL NOT own:

- Person business identity;
- Person invariants;
- Person continuity;
- Person lifecycle meaning;
- Person capability meaning;
- authorization policy.

This P5 specification does not prescribe SQL, NoSQL, files, YAML, JSON, ORM
technology, cloud storage, cache technology, or database schema.

## Transport Boundary

CLI, HTTP, RPC, messaging, UI, plugin interfaces, and other transports are
adapters around the application contract.

Transport adapters MAY define transport-specific request and response
representations.

They SHALL NOT redefine canonical Person semantics.

This P5 slice does not mandate:

- HTTP endpoints;
- REST resources;
- GraphQL schemas;
- CLI commands;
- RPC methods;
- status codes;
- transport DTOs;
- serialization formats.

## Compatibility Boundary

Existing person-like data and string-based `person_id` fields are compatibility
inputs only.

In particular, existing official plugin models SHALL NOT determine canonical
Person identity representation or ownership.

A future compatibility and migration contract SHALL define how legacy
person-like references map to canonical `PersonId`.

Until that mapping is specified:

- legacy identifiers SHALL NOT be assumed to equal canonical `PersonId`;
- migration SHALL NOT silently rewrite identity semantics;
- plugins SHALL NOT become authoritative for Person identity;
- canonical runtime implementation SHALL NOT depend on an undocumented mapping.

## Explicitly Non-Normative API

The following operations are not normative Person application API in P5:

```text
UpdatePerson
SearchPerson
ListPersons
ArchivePerson
DeletePerson
RestorePerson
PersonHistory
```

`UpdatePerson` is excluded because `EvolvePerson` is not a generic mutation
contract.

The remaining operations are deferred by the canonical capability
specification.

No interface or infrastructure implementation SHALL make these operations
canonical merely because they are common CRUD patterns.

## Deferred API Decisions

The following decisions remain intentionally deferred:

- final intrinsic Person creation fields;
- concrete `PersonId` backing representation;
- concrete `PersonId` generation strategy;
- concrete Create Person request type;
- concrete Create Person result type;
- concrete Get Person result type;
- concrete not-found representation;
- concrete application error classes;
- concrete repository interface technology;
- concrete Python method signatures;
- concrete transaction mechanism;
- event dispatch mechanism;
- event payload and metadata representation;
- concrete mutation commands;
- search and listing contracts;
- archival, deletion, erasure, and restoration contracts;
- Person history contract;
- transport contracts;
- field-level disclosure rules;
- legacy `person_id` to canonical `PersonId` migration mapping.

Deferred decisions SHALL be resolved before runtime implementation depends on
them.

Runtime code SHALL NOT silently convert a deferred API or persistence decision
into a canonical contract.

## Implementation Gate

This P5 document establishes the canonical initial application API and
persistence boundary for Person.

It does not, by itself, authorize canonical Person runtime implementation.

Canonical Person runtime implementation SHALL remain blocked until the complete
Person Domain Specification completion gate in `README.md` is satisfied.

Subsequent specification work SHALL reconcile remaining identifier,
compatibility, migration, privacy, lifecycle, event, and implementation-readiness
decisions required by that gate.

No application, infrastructure, interface, or plugin code SHALL invent those
decisions merely to begin implementation early.

## Normative References

- `docs/30-domains/person/README.md`
- `docs/30-domains/person/Vision.md`
- `docs/30-domains/person/Responsibilities.md`
- `docs/30-domains/person/Domain-Model.md`
- `docs/30-domains/person/Capabilities.md`
- `docs/rfcs/RFC-0016-family-core-domain/RFC-0016-Family-Core-Domain.md`
- `docs/00-foundation/Application-Architecture.md`
- `docs/00-foundation/API-Architecture.md`
- `docs/00-foundation/Data-Architecture.md`
- `docs/00-foundation/Event-Architecture.md`
- `docs/00-foundation/Security-Architecture.md`
- `docs/04-reference/Naming-Conventions.md`
