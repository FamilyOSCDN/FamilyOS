# Person Domain Specification

**Identifier:** `person`
**Title:** Person Domain Specification
**Version:** 0.1.0
**Status:** Draft
**Owner:** FamilyOS Project
**Layer:** Domain

---

## Overview

The Person Domain Specification defines the canonical FamilyOS business contract
for a person.

A Person represents a business individual known to FamilyOS.

Person is a Family Core concept and SHALL remain distinct from platform Identity,
authentication accounts, authorization policy, Family Membership, and
plugin-specific records.

This documentation set is the authoritative domain specification for Person
business meaning within FamilyOS.

---

## Purpose

The purpose of the Person Domain Specification is to establish an
implementation-ready contract for Person before canonical Person runtime
implementation begins.

The specification SHALL define the business meaning, ownership boundaries,
identity, continuity, invariants, lifecycle, domain model, capabilities,
application-facing operations, events, persistence expectations, privacy
expectations, and compatibility requirements necessary to implement Person
without inventing domain architecture in application, infrastructure, interface,
or plugin code.

---

## Scope

This specification governs the canonical FamilyOS Person concept.

It SHALL define:

- Person business responsibility;
- Person domain identity;
- Person continuity over time;
- Person invariants;
- Person lifecycle semantics;
- intrinsic Person information;
- Person aggregate, entity, and value-object boundaries;
- Person domain events;
- Person capabilities;
- application-facing Person operations;
- persistence abstractions required by the domain;
- privacy and data-integrity expectations;
- compatibility expectations for existing consumers of person-like data;
- integration boundaries with Identity, Family Membership, Security, and
  official domain plugins.

The detailed requirements are distributed across the normative documents listed
in this specification set.

---

## Authority

This documentation set is the canonical source of truth for Person business
semantics in FamilyOS.

Identity SHALL NOT redefine Person business identity.

Security SHALL NOT infer authorization merely from the existence of a Person.

Family Membership SHALL associate Person with Family without becoming
authoritative for Person identity or continuity.

Official domain plugins SHALL consume Person concepts without becoming
authoritative for Person business identity.

Infrastructure MAY persist Person state but SHALL NOT define Person business
meaning or invariants.

Interfaces MAY expose Person operations and information but SHALL NOT own Person
business rules.

---

## Normative Boundaries

The Person Domain SHALL NOT:

- own authentication credentials;
- own authentication mechanisms;
- treat account lifecycle as Person lifecycle;
- infer authorization from Person existence;
- make Person existence dependent on membership in one Family;
- make Family Membership authoritative for Person identity;
- make official domain plugins authoritative for Person identity;
- absorb plugin-specific records merely because they reference a person;
- redefine Family, Family Membership, Family Relationship, or Family Boundary.

Person and Identity SHALL remain separate concepts.

Person and Family Membership SHALL remain separate concepts.

Person SHALL retain its domain identity independently from membership in any
specific Family.

---

## Canonical Identifier

The canonical domain identifier type SHALL be named:

```text
PersonId
```

`PersonId` SHALL be modeled as a domain Value Object.

The identifier SHALL comply with the applicable FamilyOS identifier and naming
contracts.

The canonical backing representation of `PersonId` SHALL be UUID.

Canonical creation of a new `PersonId` SHALL use UUID version 4.

The UUID value SHALL remain opaque to consumers and SHALL NOT encode or imply
Person semantics, confidential information, personal information,
authentication identity, Family identity, Family Membership identity, or
plugin-specific identity.

The canonical textual representation SHALL be the standard UUID string
representation.

Existing string-based `person_id` values are compatibility inputs only and
SHALL NOT define the canonical identifier representation.

Detailed `PersonId` invariants and compatibility requirements are normative in
`Domain-Model.md`.

### Minimum Canonical Person State

The minimum canonical state required for Person existence is the canonical
`PersonId`.

No additional intrinsic Person attribute is currently mandatory.

Names, birth information, contact information, addresses, gender, locale,
profile information, Family Membership, Identity state, authorization data, and
plugin-specific records SHALL NOT be made mandatory Person state without an
explicit governed domain decision.

This minimum is a data-minimization and ownership boundary, not a permanent
prohibition on future Person attributes.

Any future intrinsic Person attribute SHALL require explicit specification of
its business meaning, ownership, invariants, optionality, lifecycle, privacy,
and compatibility semantics.

---

## Canonical Lifecycle

Canonical Person lifecycle begins with successful Person creation.

The current canonical lifecycle is continuity-based: stable `PersonId`
preserves Person identity and continuity without requiring a universal
lifecycle-state enumeration.

`ACTIVE`, `INACTIVE`, `ARCHIVED`, `DECEASED`, `DELETED`, and similar states are
not canonical Person states unless a later governed Person-domain decision
defines their business semantics and transition rules.

Archival, retention, deletion, erasure, restoration, and Person-history
mechanics remain separately governed concerns and SHALL NOT be inferred from
the absence of a lifecycle-state enumeration.

---

## Specification Documents

The Person Domain Specification consists of the following documents:

| Document | Responsibility |
|---|---|
| `README.md` | Specification authority, scope, boundaries, dependencies, and document map |
| `Vision.md` | Person domain purpose, business intent, principles, and long-term direction |
| `Responsibilities.md` | Canonical ownership and explicit exclusions |
| `Domain-Model.md` | Person identity, invariants, continuity, lifecycle, DDD classification, value objects, and events |
| `Capabilities.md` | Domain and application capabilities required to manipulate Person safely |
| `API.md` | Application-facing contracts and persistence boundaries |

The documents SHALL be interpreted together as one Person Domain Specification.

A requirement defined authoritatively in one document SHOULD be referenced
rather than redefined inconsistently in another document.

---

## Normative Dependencies

This specification is governed by and SHALL remain compatible with:

- RFC-0016 — Family Core Domain Architecture;
- SPEC-0002 — Identifier;
- SPEC-0003 — Metadata;
- SPEC-0004 — Versioning;
- SPEC-0005 — Document Format;
- SPEC-0008 — Naming Conventions;
- FamilyOS Domain Architecture;
- FamilyOS Data Architecture;
- FamilyOS Identity Architecture.

Where a platform specification owns a cross-cutting technical contract, the
Person Domain Specification SHALL reference that contract rather than redefine
it.

---

## Cross-Domain Dependencies

### Identity

Identity represents an actor capable of interacting with FamilyOS.

Person represents a business individual known to FamilyOS.

A Person MAY be associated with zero, one, or multiple Identity records subject
to the governing Identity contracts.

Person existence SHALL NOT require an authentication Identity.

### Family

Person SHALL remain independent from membership in any one Family.

Family Membership is responsible for associating a Person with a Family.

The Family Domain Specification owns Family Membership semantics.

### Security

Security MAY consume Person and Family Core facts as authorization context.

Person SHALL NOT own authorization policy.

Person existence SHALL NOT grant authorization.

### Official Domain Plugins

Official domain plugins MAY reference Person.

Plugin-specific records SHALL remain owned by their respective domains unless a
future accepted architectural decision explicitly changes that ownership.

Existing person-like identifiers or references in plugins SHALL NOT become
canonical merely because they predate the Person runtime implementation.

---

## Canonical Data Lifecycle Boundary

Person continuity and Person-data retention are distinct concerns.

Erasure, redaction, anonymization, retention expiry, or physical removal of
erasable Person data SHALL NOT by itself erase the historical fact that the
canonical Person existed or permit reuse of that Person's `PersonId`.

Conversely, preserving Person historical continuity SHALL NOT be interpreted as
a requirement to retain or disclose every Person-related datum indefinitely.

`PersonCreated` remains the immutable business fact of successful canonical
Person creation. Privacy, retention, and infrastructure processing SHALL NOT
rewrite that underlying domain fact.

No universal archive, delete, restore, erasure, or Person-history capability is
made normative by this boundary. Those operations remain separately governed.

---

## Canonical Person Event

`PersonCreated` is the only canonical Person domain event currently normative.

It records the immutable business fact that creation of one canonical Person
succeeded. Its minimum canonical semantic content is the created `PersonId` and
the timezone-aware occurrence time of successful canonical Person creation.

The occurrence time describes the domain fact and is distinct from persistence,
publication, dispatch, delivery, ingestion, or processing timestamps.

No non-canonical Person attribute, Identity state, Family Membership,
authorization data, credential, or plugin-specific record is required merely
to populate this event.

Serialization, envelope metadata, schema-version encoding, event identifiers,
correlation and causation identifiers, transport, delivery guarantees, ordering,
retry, durability, and outbox mechanics remain separately governed concerns.

## Compatibility Baseline

Existing person-like data and string-based `person_id` values are legacy
compatibility inputs and SHALL NOT define canonical Person identity.

Canonical migration SHALL use an explicit, stable, and idempotent mapping from
legacy identity to UUID-backed `PersonId`.

Migration SHALL preserve Person continuity and referential integrity. It SHALL
NOT silently reinterpret legacy strings as UUIDs, create a new Person because
identifier representation changes, merge distinct Persons, split one Person,
or guess through ambiguous identity evidence.

Legacy identifiers MAY coexist temporarily as aliases or compatibility
references, but canonical Person identity remains `PersonId`.

Plugins and existing consumers do not own canonical Person identity merely
because they contain a `person_id` field.

Detailed semantic migration invariants are normative in `Domain-Model.md` and
`API.md`. Concrete tooling, storage migration scripts, rollout sequencing, and
transport mechanics remain implementation concerns.

## Canonical Failure and Result Baseline

Person application semantics distinguish success from invalid Person input,
Person conflict, Person absence, authorization denial, privacy or disclosure
restriction, infrastructure failure, and compatibility or migration failure
whenever those outcomes are applicable.

These are semantic categories rather than a frozen Python or transport model.

Concrete exceptions, result objects, repository absence representations, HTTP
or other transport mappings, CLI exit codes, and observability details remain
implementation-contract decisions. Any chosen representation SHALL preserve the
canonical distinctions and SHALL NOT silently convert infrastructure failure,
authorization denial, or privacy restriction into ordinary Person absence.

## Specification Completion Gate

The canonical minimal Person subset defined by this specification is
implementation-ready.

The implementation-ready subset consists of the normative contracts already
established by this specification:

- `Person` as the canonical aggregate root;
- UUID-backed `PersonId`, with UUID version 4 used for canonical creation;
- `PersonId` as the only mandatory intrinsic Person state currently required;
- continuity-based Person lifecycle semantics without a universal lifecycle-state
  enumeration;
- the canonical Create Person capability and `CreatePerson` application command;
- the canonical Retrieve Person capability and `GetPerson` application query;
- the `PersonRepository` persistence boundary with canonical `save(Person)` and
  `get(PersonId)` semantics;
- the canonical `PersonCreated` domain event;
- canonical compatibility and migration invariants;
- canonical data-lifecycle and historical-continuity invariants;
- canonical failure and result semantics.

Implementation of this minimal subset SHALL preserve all Person-domain
invariants, ownership boundaries, Security and Privacy boundaries, compatibility
rules, and failure-category distinctions defined by the specification.

A future capability or data concept is not implementation-ready merely because
the minimal subset is implementation-ready. Search, listing, mutation,
archival, deletion, restoration, Person history, additional intrinsic
attributes, additional events, and other explicitly deferred features remain
non-normative until separately governed.

Implementation findings that expose a foundational contradiction SHALL return to
RFC or specification governance rather than being silently resolved in code.

## Implementation Status

The normative minimal Person runtime is implemented and validated against the
canonical Person specification.

The validated runtime baseline is Git revision `6e9a027`
(`feat(person): enforce canonical identity and creation invariants`).

The implemented minimal runtime includes:

- `Person` as the canonical aggregate root;
- UUID-backed `PersonId` with UUID version 4 canonical generation;
- strict runtime rejection of non-UUID `PersonId` backing values without
  coercion or legacy-string reinterpretation;
- `PersonCreated` with canonical `PersonId` and timezone-aware occurrence time;
- `CreatePerson` with failure-before-persistence validation ordering;
- `GetPerson` with canonical presence/absence semantics;
- `PersonRepository` with canonical `save(Person)` and `get(PersonId)`
  operations;
- `PersonConflictError` preserving canonical creation-conflict semantics;
- `InMemoryPersonRepository` with atomic create-only persistence semantics for
  canonical Person identity;
- integration coverage for create, retrieve, absence, distinct identities, and
  duplicate-creation conflict.

Current validation evidence for this runtime baseline is:

- Person-focused test suite: `40 passed`;
- unit regression suite: `1727 passed`;
- integration regression suite: `20 passed`;
- canonical FamilyOS validation: `PASSED`;
- Ruff: `PASSED`;
- MyPy: `PASSED`;
- deferred Person capabilities detected in the minimal runtime: `NONE`.

The current implementation has also completed an adversarial conformance review
covering runtime identifier invariants, legacy-string rejection, duplicate
canonical creation, atomic persistence conflict handling, failure-category
separation, and deferred-capability boundaries.

This status establishes that the implementation-ready minimal Person subset is
implemented and conformant to the current canonical specification.

This status SHALL NOT be interpreted as implementation or authorization of the
explicitly deferred Person scope. Search, listing, mutation, archival, deletion,
restoration, Person history, future intrinsic attributes, additional domain
events, migration tooling, transport contracts, Security integration, Privacy
integration, event delivery, transaction technology, and other separately
governed concerns remain non-normative or implementation-specific until their
applicable contracts explicitly authorize them.

Runtime evolution SHALL continue to preserve RFC-0016 and the normative Person
specification. Any future implementation need that requires a currently
deferred Person-domain semantic SHALL return to specification or architectural
governance before that semantic becomes canonical.

## Documents

- [Vision](Vision.md)
- [Responsibilities](Responsibilities.md)
- [Domain Model](Domain-Model.md)
- [Capabilities](Capabilities.md)
- [API](API.md)

---

## Deferred Decisions

The following remain intentionally deferred because the current minimal
canonical Person subset does not depend on them:

- future intrinsic Person attributes and their Value Objects;
- future Person lifecycle states or transitions, if justified by explicit
  Person business semantics;
- additional Entities inside the Person aggregate, if justified;
- concrete Person mutation operations;
- searchable Person attributes, search, and listing semantics;
- archival, deletion, erasure, restoration, and Person-history capabilities;
- additional Person domain events and event payloads beyond `PersonCreated`;
- concrete failure representation, exception hierarchy, or universal result
  wrapper;
- concrete repository technology and Python method signatures;
- concrete transaction mechanisms;
- event dispatch, delivery, transport, and infrastructure mechanics;
- transport-specific contracts and mappings;
- field-level disclosure rules;
- concrete retention, deletion, erasure, anonymization, and restoration
  mechanisms.

These deferred concerns SHALL NOT be invented by runtime code. If implementation
requires one of them, the applicable Person specification or cross-cutting
architecture SHALL govern it first.

## References

- RFC-0016 — Family Core Domain Architecture
- SPEC-0002 — Identifier
- SPEC-0003 — Metadata
- SPEC-0004 — Versioning
- SPEC-0005 — Document Format
- SPEC-0008 — Naming Conventions
- FamilyOS Domain Architecture
- FamilyOS Data Architecture
- FamilyOS Identity Architecture
