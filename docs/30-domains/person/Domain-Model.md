# Person Domain Model

## Domain

`person`

## Purpose

This document defines the canonical domain model for the FamilyOS Person domain.

It specifies Person identity, continuity, lifecycle semantics, DDD
classification, invariants, value objects, domain events, and cross-domain
boundaries required by RFC-0016.

This document defines domain architecture only. It does not authorize canonical
Person runtime implementation by itself.

## Canonical Model

```text
Person
  |
  +-- identity --> PersonId
```

`Person` is the Aggregate Root and canonical Entity representing one business
individual known to FamilyOS.

`PersonId` is the canonical Value Object identifying that Person.

The initial aggregate deliberately remains minimal. No additional Entity or
Value Object SHALL enter the canonical Person aggregate without a business
invariant or ownership requirement that justifies it.

## Aggregate

### Person Aggregate

The Person aggregate SHALL be named `Person`.

`Person` SHALL be the Aggregate Root.

The aggregate owns the business meaning and continuity of one Person within
FamilyOS. All changes to canonical Person state SHALL preserve the Person
invariants defined by this specification.

The Person aggregate SHALL NOT become a container for every piece of information
that concerns an individual.

Information belongs inside the aggregate only when the Person domain is its
canonical business owner and that information is required to preserve Person
invariants or continuity.

### Aggregate Boundary

The Person aggregate SHALL NOT own:

- authentication credentials or sessions;
- platform Identity lifecycle;
- authorization policy;
- Family, Family Membership, Family Relationship, or Family Boundary;
- plugin-specific Health, Finance, Education, Documents, or Communication
  records;
- infrastructure persistence details;
- interface or presentation state.

Those concerns remain owned by their respective domains or architectural layers.

## Entity

### Person

A `Person` represents exactly one business individual known to FamilyOS.

A Person SHALL have stable domain identity and SHALL remain the same Person when
mutable information about that Person changes.

Person continuity SHALL NOT depend on display or presentation data,
authentication or account state, credentials, platform Identity lifecycle,
membership in a particular Family, plugin-specific records, persistence
technology, or interface representation.

A Person MAY exist without an interactive FamilyOS Identity.

A Person MAY participate in zero, one, or multiple Family contexts subject to
the Family Domain Specification.

Person existence SHALL NOT imply authorization.

### Entity Naming

The canonical entity name SHALL remain `Person`.

Implementations SHALL NOT introduce an alternative canonical name such as
`PersonEntity` merely to encode the DDD classification in the type name.

## Person Identity

Every Person SHALL have exactly one canonical Person domain identity.

The canonical identifier type SHALL be named `PersonId`.

A Person's `PersonId` SHALL remain stable for the continuity of that Person.

Changing authentication data, account data, Family Membership, plugin records,
display information, persistence technology, or interfaces SHALL NOT implicitly
change `PersonId`.

`PersonId` SHALL NOT derive its identity from an authentication account,
platform Identity, Family, Family Membership, plugin-specific record, or mutable
Person attribute.

## Value Objects

### PersonId

`PersonId` SHALL be a domain Value Object.

`PersonId` SHALL be opaque, immutable after creation, stable for Person
continuity, comparable by value, independent from persistence technology,
authentication providers and any particular Family, and free from encoded
confidential or personal information.

Consumers SHALL treat `PersonId` as an identifier rather than interpreting its
internal representation.

### PersonId Representation

`PersonId` SHALL use UUID as its canonical backing representation.

Canonical creation of a new `PersonId` SHALL use UUID version 4.

The UUID representation is a technical identity mechanism only. Consumers SHALL
treat the value as opaque and SHALL NOT infer Person semantics, chronology,
Family membership, authentication identity, storage location, or any other
business meaning from the UUID value.

The canonical textual representation of `PersonId` SHALL be the standard UUID
string representation.

`PersonId` SHALL be immutable and comparable by value.

The representation SHALL NOT encode confidential information, personal
information, authentication data, Family identity, Family Membership identity,
plugin-specific identity, or mutable Person attributes.

UUID generation SHALL remain independent from persistence technology,
authentication providers, Family membership, and plugin infrastructure.

Existing string-based `person_id` fields are compatibility inputs only. Values
such as `person-001` SHALL NOT define or constrain the canonical `PersonId`
representation.

Compatibility and migration code SHALL make conversion between legacy
string-based identifiers and canonical `PersonId` explicit. Runtime code SHALL
NOT silently reinterpret arbitrary legacy strings as canonical UUID-backed
`PersonId` values.

The UUID backing representation is normative. The exact Python implementation,
constructor surface, dependency-injection mechanism for UUID generation, and
legacy migration mechanism remain implementation concerns subject to the
contracts in this specification.

## Intrinsic Person State

The Person domain SHALL own only information intrinsically belonging to the
canonical Person business concept.

Current specification evidence does not yet justify a final canonical set of
intrinsic Person attributes.

This P3 model therefore does not declare any of the following mandatory
canonical Person state:

- display, legal, preferred, given, or family name;
- email address or phone number;
- postal address;
- date of birth;
- gender;
- locale;
- profile information.

Their ownership and invariants SHALL be resolved before runtime implementation
depends on them.

`PersonId` is the only canonical Person Value Object fixed by this P3
domain-model slice.

## Person Continuity

The following continuity rules SHALL hold:

1. Stable `PersonId` establishes canonical Person identity.
2. Mutable presentation information SHALL NOT determine Person continuity.
3. Authentication or account lifecycle SHALL NOT determine Person continuity.
4. Family Membership changes SHALL NOT determine Person continuity.
5. Plugin-record lifecycle SHALL NOT determine Person continuity.
6. Persistence migration SHALL NOT create a new Person merely because storage
   representation changes.
7. Interface or transport representation SHALL NOT determine Person continuity.

A new Person SHALL NOT be created merely because one of these external or
mutable concerns changes.

## Person Lifecycle

The Person domain owns Person business lifecycle semantics.

The lifecycle begins when a new canonical Person is created. Subsequent Person
changes SHALL preserve stable identity and domain continuity unless a future
accepted specification explicitly defines different business semantics.

Person lifecycle SHALL remain independent from authentication, account, Family
Membership, and plugin-specific lifecycle state.

### Explicit Lifecycle States

This P3 slice does not introduce a canonical Person lifecycle enumeration.

Current evidence does not justify states such as `ACTIVE`, `INACTIVE`,
`ARCHIVED`, `DECEASED`, `DELETED`, or equivalent as universal canonical Person
states.

Such states SHALL NOT be invented by runtime implementation.

If explicit states become necessary, their meaning, invariants, transitions,
historical treatment, and compatibility implications SHALL be specified before
implementation depends on them.

### Historical Meaning

Person lifecycle evolution SHALL preserve historical meaning where Person data
or references must remain understandable over time.

Detailed archival, retention, deletion, erasure, restoration, and historical
mechanics remain governed by later specification work and applicable Data,
Privacy, and Security contracts.

## Domain Invariants

The canonical Person model SHALL preserve these invariants:

1. A Person represents exactly one business individual known to FamilyOS.
2. Every Person has exactly one canonical `PersonId`.
3. `PersonId` remains stable throughout Person continuity.
4. Person and Identity are not interchangeable.
5. Person existence does not require an interactive Identity.
6. Person continuity does not depend on authentication lifecycle.
7. Person continuity does not depend on membership in any particular Family.
8. Family Membership does not own or redefine Person identity.
9. Person existence does not imply authorization.
10. Security may consume Person facts but does not own Person business identity.
11. Official domain plugins may reference Person but do not own Person identity.
12. Plugin-specific records do not become canonical Person state merely because
    they reference a Person.
13. Infrastructure may persist Person but does not own Person business meaning.
14. Interfaces may present Person but do not own Person invariants.
15. `PersonId` SHALL NOT encode confidential or personal information.
16. Mutable display or profile information SHALL NOT implicitly create a new
    Person.
17. A Person SHALL NOT require Family Membership to retain Person identity.
18. Runtime code SHALL NOT invent unresolved lifecycle states or intrinsic
    attributes as a substitute for domain specification.

## Family Membership Boundary

Family Membership is not part of the Person aggregate.

It associates a Person with a Family and is owned by the Family domain.

A Person SHALL retain identity independently from any Membership. Membership
changes SHALL NOT implicitly create, replace, or destroy the associated Person.

The Person domain SHALL NOT own Membership validity, Membership lifecycle, or
Family authorization semantics.

## Identity Boundary

Person and Identity are separate domain concepts.

Person represents a business individual known to FamilyOS. Identity represents
an actor capable of interacting with FamilyOS.

A Person MAY be associated with zero, one, or multiple Identity records subject
to governing Identity contracts.

Creating, changing, disabling, or removing an Identity SHALL NOT implicitly
change canonical Person identity.

Authentication credentials and authentication state SHALL NOT be Person state.

## Security Boundary

Security MAY consume approved Person facts as authorization context.

The Person domain SHALL NOT define authorization policy, grant permissions
because a Person exists, infer authorization from Person identity, own
authentication credentials, or redefine Security decisions as Person state.

Authorization remains a Security responsibility.

## Plugin Boundary

Official domain plugins MAY reference Person through approved Person contracts.

A plugin SHALL NOT become authoritative for canonical Person identity merely
because it stores a person-like identifier or Person-related record.

Domain-specific records remain owned by their respective domains.

Existing plugin `person_id` fields remain compatibility inputs until an explicit
migration contract integrates them with canonical `PersonId`.

## Domain Events

### PersonCreated

The canonical Person domain SHALL define the event name `PersonCreated`.

`PersonCreated` represents successful creation of a new canonical Person and
SHALL identify that Person through the canonical Person identity contract.

Final payload, metadata, versioning, timestamp semantics, and transport
representation remain governed by later event-contract specification and
applicable FamilyOS cross-cutting specifications.

### Additional Person Events

No additional Person domain event is normative in this P3 slice.

`PersonUpdated`, `PersonArchived`, `PersonDeleted`, `PersonRestored`,
`PersonDeactivated`, and `PersonReactivated` SHALL NOT be treated as canonical
merely because they are plausible.

Additional events SHALL be introduced only when a specified Person business
transition requires them.

## Data Integrity

Person state SHALL remain valid according to Person domain invariants.

Application, infrastructure, interface, Security, Identity, Family, and plugin
components SHALL NOT bypass or redefine those invariants.

Technical storage constraints MAY reinforce Person integrity but SHALL NOT
replace domain validation.

## Privacy

Person information is potentially personal information and SHALL follow
FamilyOS privacy and data-protection principles.

The Person aggregate SHALL minimize unnecessary ownership of personal
information.

Information SHALL NOT be added to canonical Person state merely for convenience
when another domain is its rightful business owner.

`PersonId` SHALL NOT encode confidential or personal information.

Authorization and access-control enforcement remain Security responsibilities.

## DDD Classification

| Concept | Classification | Canonical Owner |
|---|---|---|
| `Person` | Aggregate Root and Entity | Person domain |
| `PersonId` | Value Object | Person domain |
| `PersonCreated` | Domain Event | Person domain |
| Identity association | Cross-domain relationship | Person / Identity integration |
| Family Membership | External domain concept | Family domain |
| Authorization | External policy concern | Security |
| Plugin-specific Person records | External domain records | Respective plugin domain |

No additional Person Entity or Value Object is currently normative.

## Deferred Domain-Model Decisions

The following remain intentionally deferred:

- exact intrinsic Person attributes;
- Value Objects required for future intrinsic attributes;
- explicit Person lifecycle states, if any;
- lifecycle transition matrix;
- detailed archival and historical mechanics;
- retention, deletion, erasure, and restoration semantics;
- complete domain-event set and detailed payload schemas;
- timestamps and temporal Value Objects, if required;
- additional Entities inside the Person aggregate, if justified;
- persistence-port contracts;
- application-facing operation signatures;
- migration mechanics for legacy string-based `person_id` consumers.

These decisions SHALL be resolved by the appropriate Person specification slice
before implementation depends on them.

Runtime code SHALL NOT silently resolve a deferred domain decision.

## Implementation Gate

This P3 document establishes the canonical Person domain-model baseline.

It does not, by itself, make the complete Person Domain Specification
implementation-ready.

Canonical Person runtime implementation SHALL remain blocked until the complete
Person specification resolves the implementation decisions required by RFC-0016
and the completion gate in `README.md`.

Later specification work must still establish required capabilities,
application-facing contracts, persistence boundaries, compatibility
expectations, and any domain-model details those contracts require.

## Normative References

- `docs/30-domains/person/README.md`
- `docs/30-domains/person/Vision.md`
- `docs/30-domains/person/Responsibilities.md`
- `docs/rfcs/RFC-0016-family-core-domain/RFC-0016-Family-Core-Domain.md`
- `docs/00-foundation/Domain-Architecture.md`
- `docs/00-foundation/Data-Architecture.md`
- `docs/00-foundation/Identity-Architecture.md`
- `docs/04-reference/Naming-Conventions.md`
- `docs/04-reference/Reserved-Words.md`
- `docs/06-specifications/SPEC-0008-Naming-Conventions.md`
