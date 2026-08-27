# Vision

## Domain

The Family domain is the canonical Family Core domain responsible for the
business meaning, continuity, and governed context of Family, Family Membership,
Family Relationship, and Family Boundary.

It builds on the canonical Person domain and on RFC-0016, Family Core Domain
Architecture.

The Family domain SHALL reference canonical Persons through the Person contract
and SHALL NOT redefine Person identity, continuity, or lifecycle.

## Mission

The mission of the Family domain is to provide one coherent, durable, and
technology-independent model for family context across FamilyOS.

The domain exists so that FamilyOS can reason about:

- what constitutes one canonical Family context;
- how a canonical Person participates in a Family;
- how explicit family relationships are represented independently from
  Membership;
- how Family business boundaries isolate unrelated Family contexts;
- how Family Core facts may be consumed by Security without becoming
  authorization policy.

The Family domain SHALL remain authoritative for its business facts while
remaining independent from authentication, authorization policy, plugin-local
models, storage technology, and presentation concerns.

## Long-Term Vision

FamilyOS should provide a stable Family Core that allows multiple domains,
applications, interfaces, and future intelligent capabilities to share the same
family meaning without creating competing definitions.

The long-term Family model should support controlled evolution of:

- Family identity and continuity;
- Family Membership lifecycle;
- Family Relationship semantics;
- Family Boundary semantics;
- historical family context;
- privacy-aware Family Core data handling;
- explicit cross-domain integration.

That evolution SHALL remain governed by specification.

Runtime code SHALL NOT invent unresolved Family semantics merely because an
implementation needs a convenient representation.

## Desired Outcomes

The Family domain should make the following outcomes possible:

- one canonical Family identity contract;
- stable Family continuity independent from mutable membership composition;
- explicit association between one Person and one Family through Membership;
- Membership lifecycle semantics capable of determining business validity;
- explicit Relationship semantics distinct from Membership;
- explicit Family Boundary semantics distinct from authorization policy;
- consistent use of canonical `PersonId` references;
- clear Security and Privacy boundaries;
- controlled migration from legacy family-like or membership-like concepts;
- safe future extension without forcing currently deferred concepts into the
  initial model.

## Architectural Principles

### Family Is a First-Class Business Context

A Family is not merely a collection of Persons.

A Family is a canonical business context with its own stable identity,
continuity, invariants, and governed semantics.

A Family SHALL NOT be inferred solely from:

- biological relationship;
- legal relationship;
- genealogical relationship;
- shared residence;
- household composition;
- one current member;
- plugin-local grouping;
- authorization policy.

### Stable Family Identity

A Family SHALL retain stable domain identity independently from changes in its
membership composition, display information, authentication state,
authorization state, plugin records, infrastructure representation, or storage
location.

The canonical Family identity name is `FamilyId`.

Its concrete representation SHALL be resolved by the Family Domain
Specification before runtime implementation relies on it.

### Person Independence

The Person and Family domains are coordinated but distinct.

Family-owned concepts MAY reference canonical Person identity.

The Family domain SHALL NOT:

- create an alternate Person model;
- derive Person identity from Membership;
- mutate Person identity through Family lifecycle;
- redefine Person continuity;
- replace `PersonId` with a Family-owned identifier.

### Membership Is an Explicit Association

Family Membership represents an explicit association between exactly one
canonical Person and exactly one canonical Family context.

Membership SHALL remain semantically distinct from both Person and Family.

Membership SHALL also remain distinct from Family Relationship and from
authorization.

The Family domain owns Membership validity and lifecycle semantics.

Security MAY consume valid Membership facts as authorization context, but valid
Membership SHALL NOT itself mean that an operation is authorized.

### Relationship Is Business Knowledge, Not Membership

Family Relationship represents explicit family relationship knowledge between
Persons.

Relationship SHALL remain independent from Membership.

A Relationship SHALL NOT automatically:

- create Membership;
- activate Membership;
- revoke Membership;
- modify Membership;
- grant authorization.

Relationship directionality, symmetry, taxonomy, temporal validity, identity
requirements, and historical behavior SHALL be governed explicitly before any
runtime model depends on them.

### Boundary Is Business Isolation, Not Security Policy

Family Boundary expresses the business isolation associated with an explicit
Family context.

Family Boundary SHALL prevent unrelated Family contexts from being treated as
one shared Family scope.

Family Boundary SHALL remain distinct from Security authorization policy.

Security owns the decision whether an actor may perform an operation across or
within a Family Boundary.

### Security Separation

Family Core provides business facts.

Security owns:

- authentication;
- roles;
- permissions;
- authorization policy;
- authorization decisions;
- enforcement.

Membership, Relationship, Family existence, and Family Boundary SHALL NOT be
treated as permissions.

### Privacy and Data Integrity

Family Core information may contain sensitive personal and family business
context.

The Family domain SHALL identify the business semantics and integrity
expectations of Family-owned information.

Concrete privacy policy, consent, disclosure decisions, retention mechanisms,
erasure mechanisms, and access enforcement SHALL remain governed by their
applicable Privacy, Security, Data Architecture, and infrastructure contracts.

### Household Is Not Family

`Household` is not part of the initial canonical Family model.

Current FamilyOS evidence does not justify treating Household as synonymous with
Family.

Household SHALL remain explicitly deferred unless a future governed
specification establishes independent business semantics and ownership.

No implementation SHALL introduce Household merely as an alias, container, or
technical shortcut for Family.

### Technology Independence

Family business semantics SHALL remain independent from:

- database technology;
- ORM models;
- event-bus technology;
- HTTP or RPC transport;
- CLI representation;
- serialization format;
- plugin implementation;
- UI structure;
- workflow engine;
- AI implementation.

Technology choices SHALL implement Family semantics rather than define them.

### Controlled Evolution

The Family domain will evolve as FamilyOS gains demonstrated business needs.

Evolution SHALL occur through governed specification changes.

The Family specification SHALL distinguish:

- normative semantics required by an implementation-ready subset;
- implementation choices that may remain open;
- future concepts that remain explicitly deferred.

If implementation work exposes a foundational contradiction or unresolved
business invariant, the issue SHALL return to specification or architectural
governance before the runtime contract is changed.

## Domain Boundary Vision

The intended conceptual boundary is:

```text
Canonical Person Domain
        |
        | PersonId
        v
Family Membership ---------> Family
        |                       |
        |                       v
        |                 Family Boundary
        |
        +---- distinct from ---- Family Relationship
                                  |
                                  v
                               PersonId

Security
   ^
   |
   +---- consumes approved Family Core facts
         but remains authoritative for authorization
```

This diagram is conceptual.

It does not authorize concrete aggregate nesting, identifier types for
Membership or Relationship, lifecycle states, event catalogs, persistence
schemas, or runtime implementation details that have not yet been specified.

## Success Condition

The Family Domain Specification succeeds when FamilyOS can implement a governed
Family Core subset without inventing business semantics in application,
infrastructure, interface, plugin, or persistence code.

Before an applicable Family runtime slice is authorized, the specification must
make it possible to answer, for that slice:

- what concept owns each business invariant;
- what canonical identity contracts are required;
- how Person is referenced;
- what lifecycle semantics apply;
- what makes Membership valid;
- how Relationship semantics behave;
- how Family Boundary is derived and preserved;
- which domain events are required;
- which failure categories must remain distinct;
- which Security and Privacy concerns remain external;
- which capabilities and semantics are intentionally deferred.

Family runtime implementation SHALL remain closed until the applicable
specification gate is satisfied.

## Normative References

- `docs/30-domains/family/README.md`
- `docs/30-domains/person/README.md`
- `docs/30-domains/person/Domain-Model.md`
- `docs/rfcs/RFC-0016-family-core-domain/RFC-0016-Family-Core-Domain.md`
- `docs/00-foundation/Domain-Architecture.md`
- `docs/00-foundation/Data-Architecture.md`
- `docs/00-foundation/Identity-Architecture.md`
- `docs/00-foundation/Security-Architecture.md`
- `docs/04-reference/Naming-Conventions.md`
- `docs/06-specifications/SPEC-0008-Naming-Conventions.md`
