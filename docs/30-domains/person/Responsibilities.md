# Responsibilities

## Domain

Person

## Responsibility Statement

The Person domain is the canonical owner of Person business semantics in
FamilyOS.

It is responsible for defining and preserving the business identity,
continuity, invariants, and controlled lifecycle of an individual represented
as a Person.

These responsibilities SHALL remain separate from platform Identity,
authentication, authorization, Family Membership, plugin-specific records,
infrastructure, and presentation concerns.

## Canonical Responsibilities

### Person Business Meaning

The Person domain SHALL define what it means for an individual to exist as a
Person within FamilyOS.

It SHALL provide one canonical business interpretation of Person for all
FamilyOS consumers.

### Person Domain Identity

The Person domain SHALL own the canonical Person identity contract.

A Person SHALL retain stable domain identity independently from:

- display or presentation data;
- authentication state;
- account state;
- credentials;
- platform Identity lifecycle;
- plugin-specific records;
- membership in any particular Family.

The canonical identifier is `PersonId`.

Its concrete representation and detailed invariants SHALL be resolved by the
Person Domain Specification before implementation depends on them.

### Person Continuity

The Person domain SHALL define the rules that preserve Person continuity over
time.

Changes in authentication, Identity state, Family Membership, plugin records,
persistence technology, or interfaces SHALL NOT implicitly create a different
Person or destroy Person continuity.

### Person Invariants

The Person domain SHALL define and enforce the business invariants required to
keep Person state valid.

The complete invariant set belongs to the normative Person Domain Specification
and SHALL be resolved before canonical runtime implementation begins.

### Person Lifecycle

The Person domain SHALL own Person business lifecycle semantics.

The specification SHALL determine the valid lifecycle model, including creation,
update, archival, historical treatment, or equivalent semantics where
applicable.

Authentication and account lifecycle SHALL NOT substitute for Person lifecycle.

### Intrinsic Person Information

The Person domain SHALL determine which information is intrinsic to the
canonical Person concept.

Information SHALL NOT be absorbed into Person solely because it concerns or
references an individual.

Ownership follows business-domain boundaries.

### Person Domain Events

The Person domain SHALL own the business meaning and minimum canonical semantic
content of its domain events.

The Person domain SHALL define domain events required to communicate meaningful
Person changes to approved consumers.

Event contracts SHALL preserve Person ownership and SHALL NOT expose consumers
to implementation-specific persistence or interface details.

### Person Data Integrity

The Person domain SHALL define integrity expectations necessary to prevent
invalid or contradictory Person business state.

Infrastructure may enforce technical storage constraints, but domain validity
remains governed by Person rules.

### Person Privacy Expectations

The Person domain SHALL identify privacy expectations intrinsic to Person
business data.

Access control and authorization enforcement remain Security responsibilities.

Person privacy requirements SHALL therefore integrate with Security without
moving authorization ownership into Person.

### Application-Facing Person Operations

The Person domain SHALL define the domain capabilities required for application
workflows to manipulate Person state safely.

Application services may orchestrate these capabilities but SHALL NOT invent
Person business invariants.

### Persistence Boundary

Where persistence is required, the Person domain SHALL define the abstractions
necessary to store and retrieve Person state without depending on a concrete
storage technology.

Infrastructure SHALL implement those persistence contracts without becoming
authoritative for Person business meaning.

## Cross-Domain Responsibilities

### Identity Interaction

Person represents a business individual.

Identity represents an actor capable of interacting with FamilyOS.

The Person domain SHALL preserve this separation.

A Person MAY be associated with zero, one, or multiple Identity records subject
to the governing Identity contracts.

Person SHALL NOT:

- own authentication credentials;
- own authentication mechanisms;
- treat Identity activation or suspension as Person lifecycle;
- require an interactive Identity in order to exist.

Identity SHALL NOT redefine Person business identity or continuity.

### Family Interaction

Person SHALL remain independent from membership in any one Family.

The Family domain owns Family, Family Membership, Family Relationship, and
Family Boundary semantics.

Person SHALL provide the canonical individual reference required by those
concepts without absorbing their ownership.

Family Membership SHALL NOT become authoritative for Person identity.

### Security Interaction

Security owns authorization evaluation, roles, permissions, and enforcement.

Person MAY provide approved business facts used as Security context.

Person SHALL NOT:

- infer authorization from Person existence;
- grant permissions;
- own authorization policy;
- redefine Security decisions as Person state.

Security SHALL NOT redefine Person facts in order to make an authorization
decision.

### Official Plugin Interaction

Official domain plugins MAY reference Person through explicit contracts.

Plugin-specific records remain owned by their respective domains.

The Person domain SHALL NOT own health, finance, education, document,
communication, or other plugin-specific business behavior merely because those
records reference a Person.

Existing person-like plugin identifiers SHALL NOT become canonical Person
identity merely because they predate the canonical Person implementation.

### Infrastructure Interaction

Infrastructure is responsible for technical mechanisms required to persist,
transport, or integrate Person state.

Infrastructure SHALL NOT define Person business meaning, continuity, lifecycle,
or invariants.

### Interface Interaction

Interfaces may expose Person information and operations through approved
application contracts.

Interfaces SHALL NOT own Person invariants or introduce competing Person
semantics.

## Explicitly Excluded Responsibilities

The Person domain SHALL NOT own:

- authentication credentials;
- authentication mechanisms;
- authentication-provider integration;
- platform actor Identity semantics;
- authorization roles;
- permissions;
- authorization policy or evaluation;
- Family identity;
- Family Membership;
- Family Relationship;
- Family Boundary;
- household semantics;
- health business records;
- finance business records;
- education business records;
- document-domain records;
- communication-domain records;
- plugin-specific business models;
- persistence technology;
- transport protocols;
- presentation behavior.

These exclusions preserve the domain ownership model established by RFC-0016.

## Responsibility Invariants

The following responsibility invariants SHALL hold throughout subsequent Person
specification and implementation work:

1. Person business identity is owned by the Person domain.
2. Person and Identity are not interchangeable.
3. Person existence does not require an authentication Identity.
4. Person continuity is independent from authentication lifecycle.
5. Person continuity is independent from membership in any particular Family.
6. Family Membership does not own Person identity.
7. Person existence does not imply authorization.
8. Security may consume Person facts but does not redefine them.
9. Official domain plugins may reference Person but do not own Person identity.
10. Infrastructure may persist Person but does not own Person business meaning.
11. Interfaces may present Person but do not own Person invariants.
12. Domain-specific records remain owned by their respective domains.

## Data Lifecycle Responsibility Boundary

The Person domain SHALL preserve canonical identity continuity and historical
Person meaning while minimizing unnecessary ownership of personal information.

The Person domain SHALL define the invariant that erasure or removal of erasable
data does not, by itself, rewrite the historical fact of Person existence.

The Person domain SHALL NOT own universal retention periods, storage deletion
mechanics, anonymization technology, legal-policy interpretation, or
infrastructure purge procedures.

Those concerns SHALL remain with the applicable Data Architecture, Privacy,
Security, governance, infrastructure, or domain-specific authority.

## Deferred Responsibility Details

This document establishes responsibility boundaries without prematurely
selecting the complete implementation model.

The following remain governed by later Person specification slices:

- concrete `PersonId` representation and invariants;
- final aggregate, entity, and value-object classification;
- future lifecycle states or transitions beyond canonical creation, if later
  justified by explicit Person business semantics;
- complete Person invariant set;
- domain-event schemas;
- application operation signatures;
- persistence-port contracts;
- historical and archival mechanics.

No runtime implementation is authorized to invent these decisions.

## Normative References

- `docs/30-domains/person/README.md`
- `docs/30-domains/person/Vision.md`
- `docs/rfcs/RFC-0016-family-core-domain/RFC-0016-Family-Core-Domain.md`
- `docs/00-foundation/Domain-Architecture.md`
- `docs/00-foundation/Data-Architecture.md`
- `docs/00-foundation/Identity-Architecture.md`
