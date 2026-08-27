# Person Domain Capabilities

## Domain

`person`

## Purpose

This document defines the canonical business capabilities exposed by the
FamilyOS Person domain.

Capabilities describe what the Person domain must allow approved application
and domain consumers to accomplish.

They do not define Python method signatures, CLI commands, transport endpoints,
repository interfaces, persistence technology, or authorization policy.

This capability contract is governed by RFC-0016 and the canonical Person
domain model.

## Capability Model

The initial canonical Person capability set is:

```text
CreatePerson
RetrievePerson
EvolvePerson
ReferencePerson
```

These names identify business capabilities rather than implementation classes.

A runtime implementation MAY use different application-layer type names when
required by established FamilyOS conventions, provided the canonical capability
meaning and boundaries remain unchanged.

The initial capability set is intentionally minimal.

Capabilities SHALL NOT be added merely to reproduce generic CRUD semantics.

## Create Person

### Capability

`CreatePerson`

### Intent

Create a new canonical Person representing one business individual known to
FamilyOS.

### Required Semantics

Create Person SHALL:

- establish a new canonical Person identity;
- create exactly one Person;
- preserve all Person domain invariants;
- establish Person continuity independently from Identity, Family Membership,
  authorization, and plugin-specific records;
- produce the canonical `PersonCreated` domain event when creation succeeds;
- avoid requiring an interactive Identity merely for Person existence;
- avoid requiring Family Membership merely for Person existence.

Create Person SHALL NOT:

- create authentication credentials as Person state;
- grant authorization merely because a Person was created;
- create Family Membership implicitly unless a separately governed application
  workflow explicitly coordinates that operation;
- create plugin-specific records as intrinsic Person state;
- expose or depend on the internal representation of `PersonId`.

The concrete `PersonId` generation strategy remains deferred until the canonical
identifier representation is resolved.

### Failure Semantics

Creation SHALL fail rather than produce invalid Person state.

The complete taxonomy and representation of creation failures remain an
application-contract decision for a later specification slice.

## Retrieve Person

### Capability

`RetrievePerson`

### Intent

Obtain the canonical Person associated with a known canonical Person identity.

### Required Semantics

Retrieve Person SHALL:

- address a Person through the canonical Person identity contract;
- preserve the distinction between Person and Identity;
- return Person business state without transferring ownership of Person
  invariants to the caller;
- avoid interpreting plugin-specific identifiers as canonical Person identity
  unless an explicit compatibility or migration contract establishes that
  mapping.

Retrieval SHALL NOT imply authorization.

Security remains responsible for determining whether a caller may perform a
particular retrieval in an operational context.

### Absence Semantics

The capability SHALL distinguish successful retrieval from absence of the
requested Person.

The concrete result type, exception model, optional-value representation, and
transport mapping remain application/API decisions for later specification.

## Evolve Person

### Capability

`EvolvePerson`

### Intent

Apply a specified, valid Person-domain change while preserving canonical Person
identity, continuity, ownership boundaries, and invariants.

### Required Semantics

Evolve Person SHALL:

- preserve the Person's canonical `PersonId`;
- accept only changes whose business meaning is owned by the Person domain;
- preserve Person continuity;
- preserve all Person invariants;
- reject changes that attempt to move external-domain state into the Person
  aggregate;
- use explicitly specified business operations once intrinsic Person attributes
  and lifecycle transitions become normative.

`EvolvePerson` is a capability category.

It SHALL NOT be interpreted as authorization for an unrestricted generic patch
or arbitrary field update operation.

No runtime implementation SHALL introduce a generic `UpdatePerson` operation
that can mutate unspecified Person state merely because this capability exists.

### Current Limitation

P3 intentionally defers the exact intrinsic Person attributes and explicit
Person lifecycle states.

Therefore P4 does not yet make any concrete Person mutation operation normative
beyond the requirement that future valid Person-domain changes be governed by
this capability boundary.

Concrete mutation commands SHALL be introduced only after their business
semantics and invariants are specified.

## Reference Person

### Capability

`ReferencePerson`

### Intent

Allow approved FamilyOS domains and components to refer to a canonical Person
without acquiring ownership of Person business identity or invariants.

### Required Semantics

Reference Person SHALL:

- use the canonical Person identity contract;
- preserve `PersonId` as opaque to consumers;
- permit Family Membership and approved domain records to associate with a
  Person through stable identity;
- preserve Person ownership inside the Person domain;
- prevent external domains from redefining Person identity.

Reference Person SHALL NOT:

- imply that the referencing domain owns Person;
- imply authorization;
- imply Family Membership;
- imply an interactive Identity;
- convert plugin-specific person-like identifiers into canonical `PersonId`
  without an explicit compatibility or migration contract.

This capability establishes a domain-reference boundary, not a persistence
foreign-key design.

## Capability Invariants

All canonical Person capabilities SHALL preserve these invariants:

1. Person and Identity remain distinct.
2. Person existence does not imply authorization.
3. Person identity remains independent from Family Membership.
4. Family Membership does not own Person identity.
5. Official domain plugins may reference Person but do not own Person identity.
6. `PersonId` remains the canonical Person identity contract.
7. Consumers SHALL NOT depend on the internal representation of `PersonId`.
8. Capabilities SHALL preserve Person continuity.
9. Capabilities SHALL preserve Person domain invariants.
10. Capabilities SHALL NOT move external-domain state into the Person aggregate
    merely for implementation convenience.
11. Security remains authoritative for authorization decisions.
12. Infrastructure remains non-authoritative for Person business meaning.
13. Interface and transport concerns SHALL NOT redefine Person capabilities.
14. Deferred Person semantics SHALL NOT be silently invented by application or
    runtime code.

## Cross-Domain Capability Boundaries

### Identity

Person capabilities MAY coordinate with Identity through separately governed
application workflows.

Person capabilities SHALL NOT make authentication or Identity lifecycle part of
Person business state.

### Family

The Family domain MAY reference Person when establishing or evaluating Family
Membership according to the Family Domain Specification.

Person capabilities SHALL NOT own Family Membership lifecycle or validity.

### Security

Security MAY authorize invocation of Person capabilities.

Authorization policy SHALL NOT become part of the Person capability contract.

### Official Domain Plugins

Official domain plugins MAY reference canonical Person identity through approved
integration contracts.

Plugin capabilities SHALL NOT redefine Person identity, continuity, lifecycle,
or invariants.

## Explicitly Non-Normative Capabilities

The following plausible operations are not canonical Person capabilities in this
P4 slice:

```text
SearchPerson
ListPersons
ArchivePerson
DeletePerson
RestorePerson
PersonHistory
```

Their omission is intentional.

### Search and List

The specification has not yet established:

- searchable canonical Person attributes;
- query ownership;
- filtering semantics;
- ordering semantics;
- pagination semantics;
- visibility rules;
- cross-family query semantics.

`SearchPerson` and `ListPersons` SHALL therefore remain deferred.

### Archive, Delete, and Restore

P3 does not define canonical Person lifecycle states or the business semantics
of archival, deletion, erasure, restoration, or equivalent transitions.

`ArchivePerson`, `DeletePerson`, and `RestorePerson` SHALL therefore remain
deferred.

Their semantics SHALL be reconciled with Person continuity, historical meaning,
privacy, retention, erasure, Data Architecture, and Security requirements
before they become normative.

### Person History

The Person domain requires preservation of historical meaning where necessary,
but the canonical history model has not yet been specified.

`PersonHistory` SHALL therefore remain deferred until temporal and historical
contracts are defined.

## Application Boundary

The application layer SHALL orchestrate canonical Person capabilities without
becoming authoritative for Person business meaning.

Later application-contract specification SHALL determine, where required:

- use-case or handler names;
- command and query structures;
- input and output models;
- failure contracts;
- transaction boundaries;
- domain-event dispatch responsibilities;
- coordination with Identity, Family, Security, and plugins.

This P4 document SHALL NOT freeze Python `execute(...)` signatures or equivalent
application implementation details.

## Persistence Boundary

Canonical capabilities may require persistence, but persistence is an
infrastructure concern behind domain/application abstractions.

P4 does not define a repository interface.

A later specification slice SHALL determine the minimum persistence port
required by the normative Person capabilities.

Persistence contracts SHALL preserve canonical Person identity, continuity, and
invariants without making storage technology authoritative for Person business
meaning.

This document SHALL NOT prescribe database schemas, ORM models, tables,
collections, foreign keys, or storage engines.

## Deferred Capability Decisions

The following capability decisions remain intentionally deferred:

- concrete Person mutation operations;
- searchable Person attributes;
- search and listing semantics;
- explicit archival capability;
- explicit deletion or erasure capability;
- explicit restoration capability;
- Person history/query capability;
- concrete failure taxonomy;
- application command/query names and structures;
- concrete application method signatures;
- persistence repository/port contract;
- authorization mapping for individual capabilities;
- transaction boundaries;
- event dispatch mechanics;
- compatibility mapping from legacy string-based `person_id` values to
  canonical `PersonId`.

Deferred decisions SHALL be resolved before runtime implementation depends on
them.

Runtime code SHALL NOT silently convert a deferred capability into a canonical
contract.

## Implementation Gate

This P4 document establishes the canonical Person capability baseline.

It does not, by itself, make the complete Person Domain Specification
implementation-ready.

Canonical Person runtime implementation SHALL remain blocked until the
specification completion gate in `README.md` is satisfied.

In particular, subsequent specification work must still establish the
application/API contract, persistence boundary, compatibility/migration
requirements, unresolved identifier representation, and any additional
domain-model semantics required by those contracts.

## Normative References

- `docs/30-domains/person/README.md`
- `docs/30-domains/person/Vision.md`
- `docs/30-domains/person/Responsibilities.md`
- `docs/30-domains/person/Domain-Model.md`
- `docs/rfcs/RFC-0016-family-core-domain/RFC-0016-Family-Core-Domain.md`
- `docs/00-foundation/Domain-Architecture.md`
- `docs/00-foundation/Data-Architecture.md`
- `docs/00-foundation/Identity-Architecture.md`
