# Family Domain Specification

## Status

This directory defines the normative Family domain specification for FamilyOS.

The specification is governed by RFC-0016, **Family Core Domain Architecture**,
and is developed from the canonical Person-domain baseline established before
this Family specification branch was created.

The Family domain specification SHALL be completed to the level required by the
RFC-0016 specification-to-implementation gate before runtime code is permitted
to define Family-domain semantics that are not already fully specified.

## Purpose

The Family domain owns the canonical business meaning of a family and the facts
that describe how canonical Persons participate in, relate within, and are
bounded by that family context.

Its purpose is to provide one authoritative semantic model for Family Core
without allowing application services, infrastructure adapters, plugins,
Security, Privacy, transport layers, or persistence technologies to invent
competing definitions of family structure.

## Normative Authority

The normative authority for this specification is, in order:

1. RFC-0016 — Family Core Domain Architecture;
2. the documents in this directory for Family-owned semantics;
3. the canonical Person Domain Specification for Person-owned semantics and
   `PersonId` references;
4. applicable cross-cutting architecture, Security, Privacy, and compatibility
   contracts where RFC-0016 assigns responsibility outside Family Core.

When an implementation need exposes a semantic question that is not resolved by
these authorities, the question SHALL return to specification or architectural
governance. It SHALL NOT be silently resolved in runtime code.

## Domain Ownership

Family Core owns the canonical semantics and invariants of:

- `Family`;
- `FamilyId`;
- Family Membership;
- Family Relationship;
- Family Boundary;
- Family-owned lifecycle rules for those concepts;
- Family-owned domain facts and events that are explicitly authorized by this
  specification.

Family Core references canonical Persons through Person-domain identity. It
SHALL NOT redefine Person, duplicate Person identity, or absorb Person-owned
intrinsic semantics.

## Canonical Concepts

### Family

A `Family` is a first-class domain concept with stable canonical identity.

A Family SHALL NOT be inferred solely from residence, household composition,
biological relationship, legal relationship, social relationship, account
membership, authorization state, or any other external representation.

The exact lifecycle, invariants, and creation semantics of Family are defined by
the Family domain model before implementation is authorized.

### FamilyId

`FamilyId` is the canonical identity of one Family.

Its concrete representation, generation contract, validation rules, and
compatibility semantics SHALL be specified explicitly before runtime
implementation. No application or infrastructure layer may choose those
semantics independently.

### Family Membership

Family Membership represents the canonical association of exactly one Person
with exactly one Family.

Membership is a distinct domain concept. It is not the Person, not the Family,
not a Family Relationship, and not an authorization or permission assignment.

The Family domain owns membership validity and lifecycle semantics. Person Core
remains authoritative for the referenced Person and its `PersonId`.

### Family Relationship

Family Relationship represents Family-owned relationship semantics between
canonical Persons where such semantics are explicitly defined by this
specification.

Relationship is distinct from Membership. A relationship SHALL NOT imply Family
Membership unless an explicit normative rule says so, and it SHALL NOT imply
Security permission or authorization.

### Family Boundary

Family Boundary represents the business boundary associated with canonical
Family semantics.

It is not an authorization policy. Security may consume Family facts when
making authorization decisions, but Security owns authorization semantics and
Family Core SHALL NOT encode permissions as Family facts.

## Person Boundary

The canonical Person domain is an external domain dependency of Family Core.

Family-owned concepts that refer to a Person SHALL use the canonical Person
identity contract. Family Core SHALL NOT create a second Person model or
reinterpret legacy strings, plugin-local identifiers, account identifiers, or
transport identifiers as canonical `PersonId` values.

Family Membership is not part of the Person aggregate. Its validity and
lifecycle belong to Family Core even though it references a canonical Person.

## Security and Privacy Boundary

Family Core defines family business facts. It does not own authorization.

Security may consume Family, Membership, Relationship, and Boundary facts, but
Security SHALL remain authoritative for permissions, roles, access decisions,
and authorization policy.

Privacy concerns that require policy, consent, disclosure, retention, or other
cross-cutting governance SHALL remain governed by their applicable contracts.
Family Core SHALL define only the domain semantics that RFC-0016 assigns to it.

## Household Decision

`Household` is not introduced as a canonical Family Core concept by this
specification baseline.

Current architectural evidence does not justify treating Household as
synonymous with Family or silently embedding household semantics into Family,
Membership, Relationship, or Boundary.

Household therefore remains explicitly deferred until a future specification or
architectural decision defines whether it is a separate domain concept, a
projection, an external context, or otherwise related to Family Core.

## Specification Scope

The Family specification SHALL define, before applicable runtime implementation:

- Family identity and lifecycle;
- Family invariants;
- Family creation and retrieval semantics where authorized;
- Membership identity requirements, if any;
- Membership lifecycle and invariants;
- Relationship identity requirements, if any;
- Relationship lifecycle, directionality, cardinality, and invariants;
- Family Boundary semantics and invariants;
- domain events that are required for the implementation-ready subset;
- repository and application-facing contracts required by that subset;
- failure and result semantics;
- compatibility and migration boundaries;
- interactions with canonical Person identity;
- Security and Privacy responsibility boundaries;
- explicitly deferred capabilities and semantics.

The specification SHALL distinguish required canonical semantics from optional
implementation mechanisms.

## Deferred Scope

Until explicitly specified and authorized, the following SHALL NOT be inferred
from this baseline:

- search or listing capabilities;
- arbitrary Family mutation;
- archival, deletion, restoration, or historical reconstruction;
- Household semantics;
- roles or permissions disguised as Membership or Relationship facts;
- Security authorization policy;
- Privacy policy implementation;
- transport or API technology;
- persistence technology;
- event transport or delivery guarantees;
- migration tooling;
- plugin-local extensions becoming canonical Family semantics;
- identifiers for Membership or Relationship merely because an implementation
  would find such identifiers convenient.

Additional deferred concerns may be identified by the detailed specification.

## Specification-to-Implementation Gate

Runtime implementation may proceed incrementally only for a subset whose
semantics are completely specified and whose implementation does not pre-empt
open decisions in the remaining Family domain.

Before a Family runtime slice is authorized, the applicable specification SHALL
provide enough normative detail to determine:

- what the concept means;
- who owns it;
- how it is identified, if identity is required;
- its lifecycle and invariants;
- valid and invalid state transitions;
- required references to canonical Person or Family identity;
- observable results and failure categories;
- persistence expectations where persistence is part of the slice;
- relevant cross-domain boundaries;
- explicitly deferred behavior.

Application, infrastructure, interface, plugin, and persistence code SHALL NOT
be used as the place where unresolved Family-domain semantics become canonical.

## Documents

The Family Domain Specification is organized as follows:

- `README.md` — normative scope, authority, ownership, boundaries, and
  implementation gate;
- `Vision.md` — domain vision and architectural principles;
- `Responsibilities.md` — responsibility ownership and exclusions;
- `Domain-Model.md` — canonical Family, Membership, Relationship, Boundary,
  lifecycle, identity, invariants, and events;
- `Capabilities.md` — authorized domain/application capabilities and deferred
  capability boundaries;
- `API.md` — application-facing contracts, persistence ports, result/failure
  semantics, and integration boundaries.

## Implementation Status

Family runtime implementation is not authorized merely by the existence of this
README.

This document establishes the specification boundary and structure. Detailed
normative contracts remain to be completed and reconciled across the Family
specification documents before the RFC-0016 implementation gate can be declared
satisfied for any runtime subset.

No Family runtime implementation is established by this document.
