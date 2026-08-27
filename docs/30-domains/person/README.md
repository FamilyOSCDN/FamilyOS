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

## Specification Completion Gate

The Person Domain Specification is not implementation-ready until the
documentation set has resolved every decision required by RFC-0016 for the
implemented Person subset.

Before canonical Person implementation begins, the specification SHALL resolve
at minimum:

- the representation and invariants of `PersonId`;
- Person continuity rules;
- Person invariants;
- Person lifecycle semantics;
- intrinsic Person information;
- aggregate, entity, and value-object classification;
- meaningful Person domain events;
- privacy and data-integrity expectations;
- application-facing operations;
- persistence abstractions where required;
- compatibility expectations and migration boundaries.

Implementation findings that expose a foundational contradiction SHALL return to
RFC or specification governance rather than being silently resolved in code.

---

## Implementation Status

Canonical Person runtime implementation has not started.

This specification SHALL precede implementation.

No source-code implementation is authorized merely by the creation of this P1
baseline.

---

## Documents

- [Vision](Vision.md)
- [Responsibilities](Responsibilities.md)
- [Domain Model](Domain-Model.md)
- [Capabilities](Capabilities.md)
- [API](API.md)

---

## Deferred Decisions

The following decisions remain intentionally unresolved by P1:

- complete Person intrinsic-data model;
- canonical lifecycle model, including the explicit decision that no universal
  Person lifecycle-state enumeration is currently required;
- complete Person invariant set;
- complete Person value-object model;
- Person domain-event catalog;
- application operation signatures;
- persistence port contracts;

These decisions SHALL be resolved by subsequent Person Domain Specification
slices before implementation depends on them.

---

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
