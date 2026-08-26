# RFC-0016: Family Core Domain Architecture

| Field | Value |
|------|------|
| RFC | RFC-0016 |
| Title | Family Core Domain Architecture |
| Status | Draft |
| Authors | FamilyOS Architecture Team |
| Created | 2026-08-26 |
| Updated | 2026-08-26 |
| Target Release | TBD |
| Supersedes | None |
| Superseded By | None |

---

# Executive Summary

RFC-0016 defines the architectural baseline for the canonical FamilyOS Family
Core Domain.

The Family Core establishes the business concepts required to represent people,
families, family membership, family relationships, and explicit family
boundaries across FamilyOS.

The RFC exists because current FamilyOS architecture and domain plugins already
refer to Person and Family concepts, while no canonical implemented domain model
currently owns those concepts.

This RFC defines the architectural boundaries and responsibilities of the Family
Core before implementation begins.

---

# Context

FamilyOS has completed its initial platform foundation, plugin ecosystem,
official plugin portfolio, engineering frameworks, and platform validation
baseline.

The current architecture already references business concepts that require a
canonical Family Core.

`Domain-Architecture.md` identifies both:

- Person Domain Specification;
- Family Domain Specification.

`Data-Architecture.md` identifies the same domain specifications as part of the
information architecture.

`Identity-Architecture.md` explicitly distinguishes a business Person from a
platform Identity and states that the Identity component must not replace the
Person Domain.

Existing FamilyOS domains and frameworks also refer to concepts including:

- person;
- family member;
- family unit;
- family membership;
- family relationship;
- family boundary.

However, the current source tree does not contain a canonical runtime
implementation for those business concepts.

The existing `docs/30-domains/person/` documentation is only a placeholder
baseline and does not define a complete Person domain contract.

Historical root-level `Person/` documentation was also inspected and contained
no substantive reusable business model.

---

# Architecture Assessment

The current FamilyOS architecture contains a gap between its domain-level
contracts and its implemented runtime model.

FamilyOS already defines rich domain capabilities for:

- Security;
- Health;
- Finance;
- Education;
- Documents;
- Communication.

Several of those domains depend conceptually on people, family members, family
units, membership, ownership, or family relationships.

Those concepts currently do not have one canonical business owner in the
runtime.

The Identity Architecture provides actor and identity semantics, but explicitly
does not own Person business meaning or family business rules.

The Security Framework defines authorization and family-boundary requirements,
but security policy must not become the source of truth for family membership or
family relationships.

The Family Core therefore represents a missing domain boundary rather than an
extension of Identity, Security, or any existing official plugin.

---

# Problem Statement

FamilyOS currently lacks a canonical domain model for the business concepts that
identify people and organize them into family contexts.

Without such a model:

- plugins may define incompatible interpretations of a person or family member;
- family membership semantics may become duplicated across domains;
- security policies may depend on family concepts without a canonical business
  source of truth;
- ownership and relationship semantics may diverge between Health, Finance,
  Education, Documents, and Communication;
- future knowledge, intelligence, event, workflow, and automation capabilities
  would lack a stable family context.

FamilyOS therefore requires a canonical Family Core Domain before higher-level
family intelligence and controlled automation are implemented.

---

# Decision Drivers

- Domain-driven design
- Explicit business ownership
- Architectural consistency
- Stable family context
- Separation of Person and Identity
- Security boundary correctness
- Cross-domain interoperability
- Extensibility
- Long-term knowledge preservation
- Testability

---

# Goals

RFC-0016 intends to:

- define the canonical responsibility of the Family Core Domain;
- define the canonical distinction between Person and Identity;
- establish Family as a first-class business concept;
- define the architectural role of family membership;
- define the architectural role of family relationships;
- define explicit family-boundary semantics;
- establish ownership boundaries for family-related business concepts;
- provide a stable contract for existing and future FamilyOS domains;
- provide the normative basis for future Person and Family domain
  specifications;
- provide the architectural basis for a future Family Core implementation EPIC.

---

# Non Goals

RFC-0016 does not:

- define authentication mechanisms;
- define credentials or authentication providers;
- replace the Identity Architecture;
- replace the Security Framework;
- define detailed authorization policy;
- define Health, Finance, Education, Documents, or Communication business
  behavior;
- define AI or family intelligence behavior;
- define memory or knowledge-processing implementation;
- define event-processing infrastructure;
- define workflow or automation infrastructure;
- define persistence technology or database schemas;
- define presentation-layer behavior;
- define household semantics unless a separate household concept is proven
  necessary;
- implement the Family Core runtime.

---

# Architectural Decision

FamilyOS SHALL introduce a canonical Family Core Domain responsible for the
business meaning and invariants of people, families, family membership, family
relationships, and family boundaries.

The Family Core SHALL remain independent from authentication technology,
infrastructure storage, presentation concerns, plugin implementation details,
and AI behavior.

The Family Core SHALL be the canonical source of business truth for family
membership and family relationships.

Identity SHALL remain a separate architectural concern.

A Person SHALL represent a business individual.

An Identity SHALL represent an actor recognized by the FamilyOS platform.

A Person and an Identity SHALL NOT be treated as the same concept.

Security MAY consume Family Core information for authorization decisions, but
Security SHALL NOT become the source of truth for family membership or family
relationships.

Existing and future FamilyOS domains SHALL reference canonical Family Core
concepts rather than creating incompatible local definitions where shared
family meaning is required.

---

# Proposed Design

The initial conceptual architecture is:

```text
                        FamilyOS Domain Layer

                             Family
                                ^
                                |
                         Family Membership
                                |
                                v
                             Person

Person -------------------- Relationship -------------------- Person

                             Family
                                |
                                v
                         Family Boundary
```

This diagram represents architectural concepts only.

It does not yet define final aggregate boundaries, cardinalities, persistence
models, lifecycle rules, or implementation classes.

The following concepts are candidates for normative definition during this RFC:

- Person;
- Family;
- Family Membership;
- Family Relationship;
- Family Boundary.

The following concept remains intentionally unresolved:

- Household.

Household SHALL NOT be treated as equivalent to Family unless its business
semantics and lifecycle are explicitly defined.

## Person Boundary

Person represents a business individual known to FamilyOS.

Person business meaning belongs to the Domain layer.

Person SHALL remain independent from authentication mechanisms.

## Identity Boundary

Identity represents an actor capable of interacting with FamilyOS.

Identity MAY reference a Person where appropriate.

Not every Person is required to have an interactive Identity.

Identity lifecycle and authentication remain governed by the Identity and
Security architectures.

## Family Boundary

Family represents a governed family context within which FamilyOS business
information may be organized.

Family membership and family relationships require explicit domain semantics.

A family relationship SHALL NOT automatically imply unrestricted authorization.

Security policy remains responsible for authorization decisions.

## Cross-Domain Integration

Existing domain plugins MAY reference Family Core concepts through explicit
contracts.

The Family Core SHALL NOT depend on those plugins in order to preserve domain
independence.

Target dependency direction:

```text
Family Core
    ^
    |
    +---- Health
    +---- Finance
    +---- Education
    +---- Documents
    +---- Communication

Identity <---- Person reference boundary

Security <---- Family / Membership / Relationship context
```

## Canonical Semantic Model

The Family Core SHALL distinguish identity, participation, relationship, family
context, and authorization as separate semantic concerns.

The canonical semantic model is:

```text
Person
   |
   | participates through
   v
Family Membership --------------------> Family
   |                                      |
   | lifecycle                            | establishes
   |                                      v
   |                                Family Boundary
   |
   +---- does not grant permissions

Person <---------- Family Relationship ----------> Person
                    |
                    +---- does not grant permissions

Family Core
    |
    +---- provides authoritative family business context
    |
    v
Security
    |
    +---- evaluates authorization
```

The following distinctions are normative:

```text
Person != Identity
Family Membership != Family Relationship
Family Membership != Permission
Family Relationship != Permission
Family Boundary != Authorization Policy
```

These distinctions SHALL remain explicit in domain specifications,
implementation contracts, and cross-domain integrations.

## Person Semantics

A Person represents one business individual known to FamilyOS.

Person SHALL own business meaning about the existence and continuity of that
individual within the FamilyOS domain model.

A Person SHALL have a stable domain identity independent from:

- display name;
- authentication state;
- account state;
- credentials;
- plugin-specific records;
- membership in any particular Family.

A Person MAY exist without an interactive FamilyOS Identity.

A Person MAY participate in zero, one, or multiple Family contexts where future
domain rules permit such participation.

A Person SHALL NOT derive its business identity from a Family Membership.

A Person SHALL NOT implicitly gain authorization merely because it exists in the
Family Core.

The technical representation and syntax of the future Person identifier are
intentionally deferred to the Person Domain Specification. The canonical
implementation name is expected to follow existing FamilyOS naming conventions,
including `PersonId`.

## Family Semantics

A Family represents an explicit governed family context in FamilyOS.

A Family SHALL have a stable domain identity independent from:

- its display name;
- its current members;
- any single Person;
- authentication mechanisms;
- plugin-specific data;
- infrastructure storage.

A Family SHALL define the business context within which Family Membership is
evaluated.

A Family SHALL NOT be inferred solely from biological, legal, social, or
genealogical relationships between Persons.

A Family SHALL NOT be inferred solely from shared residence.

Removing or changing one Family Membership SHALL NOT by itself change the
identity of the Family.

The technical representation and syntax of the future Family identifier are
intentionally deferred to the Family Domain Specification. The canonical
implementation name is expected to follow existing FamilyOS naming conventions,
including `FamilyId`.

## Family Membership Semantics

Family Membership represents an explicit business association between one Person
and one Family.

Membership SHALL be modeled independently from both Person and Family so that
its own business lifecycle and invariants can be represented explicitly.

A Membership SHALL identify exactly one participating Person and exactly one
Family context.

A Membership SHALL have explicit lifecycle semantics.

Membership lifecycle SHALL support determining whether the association is valid
for a given business decision without requiring Security to own membership
state.

The exact lifecycle states, transitions, timestamps, and technical
representation are intentionally deferred to the Family Domain Specification.

A Membership SHALL NOT:

- represent authentication;
- represent credentials;
- represent a family relationship taxonomy;
- automatically grant authorization;
- imply unrestricted access to Family resources.

Security MAY use valid Membership information as authorization context.

Security SHALL remain responsible for evaluating whether a particular action is
permitted.

The technical representation of a future Membership identifier, if a dedicated
identifier is required, is intentionally deferred.

## Family Relationship Semantics

Family Relationship represents explicit business knowledge about a relationship
between Persons.

Relationship SHALL remain semantically distinct from Family Membership.

A Relationship MAY describe family meaning that exists independently from
membership in a particular Family context.

A Relationship SHALL NOT automatically create, activate, revoke, or otherwise
modify a Family Membership.

A Relationship SHALL NOT automatically grant authorization.

Relationship directionality, symmetry, taxonomy, temporal validity, evidence,
and lifecycle rules are intentionally deferred to the relevant domain
specification.

This RFC does not assume that all family relationships are biological, legal,
genealogical, residential, or symmetric.

The technical representation of a future Relationship identifier, if a
dedicated identifier is required, is intentionally deferred.

## Family Boundary Semantics

A Family Boundary represents the isolation boundary associated with an explicit
Family context.

The Family Core SHALL provide the authoritative business context from which a
Family Boundary can be established.

A Family Boundary SHALL prevent accidental interpretation of unrelated Family
contexts as one shared business scope.

Family Boundary semantics SHALL remain distinct from authorization policy.

The existence of a Family Boundary does not itself determine whether an actor
may perform a specific action.

Security SHALL consume Family, Membership, and other approved Family Core
context when evaluating access across or within Family boundaries.

Cross-family access SHALL require explicit Security policy and SHALL NOT arise
implicitly from:

- Person existence;
- Family Membership in another Family;
- Family Relationship;
- shared plugin data;
- shared infrastructure.

## Person and Identity Interaction

Person and Identity are separate architectural concepts with different
ownership.

The Family Core owns Person business semantics.

The Identity architecture owns platform actor identity.

An Identity MAY reference a Person through an explicit integration contract.

Such a reference SHALL NOT transfer ownership of Person business invariants to
Identity.

Identity activation MAY require Family Membership validation as defined by
Security architecture, but the membership fact itself SHALL originate from the
Family Core.

Authentication state SHALL NOT determine whether the corresponding Person
exists as a business individual.

## Family Core and Security Interaction

The Family Core SHALL be authoritative for:

- Person business identity;
- Family business identity;
- Family Membership facts and lifecycle;
- Family Relationship facts;
- Family Boundary business context.

Security SHALL be authoritative for:

- authentication;
- authorization evaluation;
- role and permission enforcement;
- access decisions;
- denial behavior;
- security audit requirements.

Family Core information MAY be an input to Security decisions.

Security decisions SHALL NOT redefine the underlying Family Core facts.

A valid Membership therefore means that the business association is valid
according to Family Core rules. It does not mean that every operation is
authorized.

A Relationship therefore describes business context. It does not constitute a
permission.

## Semantic Invariants

The following invariants SHALL govern subsequent Family Core specifications and
implementation:

1. A Person and an Identity are not interchangeable.
2. A Person retains its domain identity independently from Family Membership.
3. A Family retains its domain identity independently from any individual
   member.
4. A Membership associates exactly one Person with exactly one Family.
5. Membership lifecycle is owned by the Family Core, not Security.
6. Membership validity does not imply unrestricted authorization.
7. Relationship and Membership are separate business concepts.
8. Relationship does not imply authorization.
9. Family Boundary and authorization policy are separate concerns.
10. Security may consume Family Core facts but does not own or redefine them.
11. Family Core does not depend on official domain plugins to establish its
    business truth.
12. Household is not assumed to be synonymous with Family.

## Intentionally Deferred Semantic Decisions

R2 establishes the canonical semantic distinctions but intentionally does not
freeze implementation-level design.

The following remain deferred:

- final aggregate boundaries;
- final entity versus value-object classification;
- identifier storage representation;
- UUID or other runtime identifier strategy;
- Membership lifecycle state names and transition graph;
- Relationship taxonomy;
- Relationship directionality and symmetry rules;
- temporal and historical representation;
- domain-event catalog;
- repository contracts;
- persistence ports and adapters;
- serialization formats;
- Household semantics;
- authorization policy details.

These decisions SHALL be addressed by the Person and Family domain
specifications or by later governed design work before implementation requires
them.

## Domain Ownership Contract

Family Core ownership SHALL be explicit so that shared family concepts do not
drift into Identity, Security, infrastructure, or official domain plugins.

The canonical ownership model is:

| Concern | Canonical Owner | Consumers / Integrators |
|---|---|---|
| Person business identity and continuity | Family Core | Identity, Security, domain plugins |
| Family business identity and continuity | Family Core | Security, domain plugins |
| Family Membership facts and lifecycle | Family Core | Identity, Security, domain plugins |
| Family Relationship facts and semantics | Family Core | Security, domain plugins |
| Family Boundary business context | Family Core | Security, domain plugins |
| Platform actor identity | Identity | Family Core, Security |
| Authentication | Security / Identity architecture | Platform interfaces and applications |
| Authorization evaluation | Security | Applications, interfaces, domain integrations |
| Role and permission enforcement | Security | Applications and interfaces |
| Health business behavior | Health domain | Family Core references where required |
| Finance business behavior | Finance domain | Family Core references where required |
| Education business behavior | Education domain | Family Core references where required |
| Documents business behavior | Documents domain | Family Core references where required |
| Communication business behavior | Communication domain | Family Core references where required |
| Persistence technology | Infrastructure | Family Core through explicit ports |
| Presentation behavior | Interfaces | Family Core through application contracts |

Ownership means responsibility for the business meaning, evolution, invariants,
and lifecycle of the owned concept.

Consumption of a Family Core concept SHALL NOT transfer ownership of that
concept to the consumer.

Identity SHALL NOT redefine Person business identity.

Security SHALL NOT redefine Membership, Relationship, Family, or Person facts in
order to make an authorization decision.

Official domain plugins SHALL NOT create competing canonical definitions for
shared Person, Family, Membership, Relationship, or Family Boundary semantics.

Infrastructure SHALL persist Family Core state without becoming authoritative
for its business meaning.

Interfaces SHALL present Family Core information without owning its invariants.

## Specification Responsibility Boundary

RFC-0016 defines architecture, semantic distinctions, ownership, and mandatory
specification outcomes.

RFC-0016 SHALL NOT freeze implementation details that require domain-specific
analysis.

The Person Domain Specification and Family Domain Specification SHALL translate
this RFC into implementation-ready domain contracts.

Those specifications SHALL preserve every normative distinction established by
RFC-0016.

A specification MAY refine a concept where this RFC intentionally defers a
decision.

A specification SHALL NOT contradict RFC-0016 without a governed update to this
RFC or a superseding architectural decision.

The specification boundary is:

```text
RFC-0016
    |
    +---- architecture
    +---- canonical semantics
    +---- ownership
    +---- cross-domain boundaries
    +---- required specification outcomes
    |
    v
Person Domain Specification
Family Domain Specification
    |
    +---- domain model decisions
    +---- invariants
    +---- lifecycle decisions
    +---- identifier contracts
    +---- event contracts
    +---- implementation-facing domain boundaries
    |
    v
Family Core implementation EPIC
```

## Person Domain Specification Requirements

The Person Domain Specification SHALL define an implementation-ready contract
for Person while preserving the Person and Identity separation established by
this RFC.

At minimum, the Person Domain Specification SHALL define:

- the normative definition and responsibility of Person;
- the Person domain identity contract;
- the rules governing Person continuity over time;
- Person invariants;
- the Person lifecycle, including whether explicit lifecycle states are
  required;
- the information that belongs intrinsically to Person versus information owned
  by another domain;
- the boundary between Person and Identity;
- the boundary between Person and Family Membership;
- the boundary between Person and plugin-specific records;
- the aggregate, entity, and value-object classification required for the Person
  model;
- the canonical identifier naming and representation required by implementation;
- creation, update, archival, historical, or equivalent lifecycle semantics
  where applicable;
- the domain events required to communicate meaningful Person changes;
- privacy and data-integrity expectations relevant to Person business data;
- application-facing operations required to manipulate Person safely;
- persistence abstractions required by the domain, if persistence is needed;
- compatibility expectations for existing consumers of person-like data.

The Person Domain Specification SHALL explicitly state which candidate concerns
are intentionally excluded from Person ownership.

The Person Domain Specification SHALL NOT:

- model authentication credentials as Person state;
- treat account or authentication lifecycle as Person lifecycle;
- infer authorization from Person existence;
- make a Person dependent on membership in one specific Family;
- make official domain plugins authoritative for Person identity.

The Person Domain Specification SHALL resolve the representation of the
canonical `PersonId` before implementation relies on that identifier.

## Family Domain Specification Requirements

The Family Domain Specification SHALL define an implementation-ready contract
for Family, Family Membership, Family Relationship, and Family Boundary.

At minimum, the Family Domain Specification SHALL define:

- the normative definition and responsibility of Family;
- the Family domain identity contract;
- Family invariants and continuity rules;
- the aggregate, entity, and value-object boundaries required for the Family
  model;
- the canonical identifier naming and representation required by implementation;
- Family lifecycle semantics;
- Family Membership identity requirements, if a dedicated identity is required;
- Family Membership invariants;
- Family Membership lifecycle states and valid transitions;
- the rules that determine Membership validity for business decisions;
- historical expectations for Membership changes;
- Family Relationship identity requirements, if a dedicated identity is
  required;
- Family Relationship semantics and invariants;
- Relationship directionality and symmetry rules;
- the initial Relationship taxonomy or the governed mechanism by which that
  taxonomy is defined;
- temporal or historical semantics for Relationships where required;
- Family Boundary derivation and invariants;
- cross-family business-context rules;
- the boundary between Family Core facts and Security authorization decisions;
- the domain events required to communicate meaningful Family, Membership,
  Relationship, and Boundary changes;
- privacy and data-integrity expectations for family business data;
- application-facing operations required to manipulate Family Core state
  safely;
- persistence abstractions required by the domain, if persistence is needed;
- compatibility expectations for existing family-like or membership-like
  concepts.

The Family Domain Specification SHALL preserve the invariant that Membership
does not itself grant authorization.

The Family Domain Specification SHALL preserve the invariant that Relationship
does not itself grant authorization.

The Family Domain Specification SHALL explicitly decide whether Household is:

- a distinct Family Core concept;
- a concept owned by another domain;
- a future concept intentionally deferred;
- unnecessary for the canonical model.

Household SHALL NOT become synonymous with Family merely as an implementation
shortcut.

The Family Domain Specification SHALL resolve the representation of the
canonical `FamilyId` before implementation relies on that identifier.

Any dedicated Membership or Relationship identifier SHALL be specified before
implementation treats it as a stable public or persisted domain identity.

## Cross-Specification Consistency Contract

The Person Domain Specification and Family Domain Specification SHALL be
designed as coordinated contracts.

They SHALL agree on:

- how Person is referenced by Family Membership;
- identifier boundaries between Person and Family concepts;
- ownership of shared terminology;
- historical-reference expectations;
- lifecycle interactions;
- domain-event integration points;
- privacy and data-integrity assumptions;
- compatibility expectations.

The Family Domain Specification SHALL reference Person through the Person
contract rather than redefining Person.

The Person Domain Specification SHALL reference Family participation through
the Family Membership contract rather than embedding Family ownership into
Person.

Neither specification SHALL make Security the owner of Family Core business
facts.

## Specification-to-Implementation Gate

Family Core implementation SHALL proceed only from sufficiently specified domain
contracts.

Before implementation of a Family Core concept begins, the specification
governing that concept SHALL define every decision required to implement its
business invariants without inventing architecture inside application,
infrastructure, or interface code.

At minimum, implementation SHALL NOT freeze any of the following unless the
governing domain specification has resolved them:

- aggregate boundaries;
- entity and value-object classification;
- stable identifier contracts;
- lifecycle states and transitions where applicable;
- relationship semantics required by the implementation;
- domain-event contracts required by the implementation;
- domain ownership boundaries;
- Security integration boundaries.

Implementation MAY proceed incrementally when only a subset of the Family Core
is required, provided the implemented subset is fully specified and does not
prejudge unresolved semantics of later concepts.

An implementation EPIC SHALL consume the accepted RFC and the applicable domain
specifications as normative inputs.

Implementation findings that expose a foundational contradiction SHALL return to
RFC or specification governance rather than being silently resolved in code.

---

# Architectural Consequences

Positive consequences include:

- one canonical source of truth for shared family concepts;
- clearer ownership boundaries;
- reduced semantic duplication across plugins;
- stronger Identity and Security separation;
- a stable basis for family knowledge management;
- a stable context for future AI and automation capabilities;
- improved interoperability between official domains.

Negative consequences include:

- new domain contracts must be designed and governed;
- existing plugins may require future integration work;
- legacy assumptions about person or family concepts may require migration;
- aggregate and lifecycle boundaries require careful modeling before
  implementation.

---

# Rejected Decisions

## Use Identity as the Person Model

Rejected.

Identity represents platform actors and authentication-related context.

The FamilyOS Identity Architecture explicitly separates Identity from Person
business meaning.

## Let Each Plugin Define Its Own Person or Family Concepts

Rejected.

This would create incompatible definitions of shared family concepts and weaken
cross-domain interoperability.

## Put Family Membership Inside Security

Rejected.

Security consumes family context for authorization but must not own the
underlying family business truth.

## Start With AI or Automation

Rejected.

Family intelligence, workflow, and automation require stable domain knowledge
and family context first.

---

# Alternatives Considered

## Person-Only Domain

A Person-only implementation would resolve part of the current architecture gap
but would not establish canonical family membership, relationships, or family
boundaries.

It is therefore insufficient as the complete Family Core architecture.

## Family as a Plugin

A Family plugin would preserve extensibility but would incorrectly make the
central FamilyOS family context optional and plugin-owned.

The Family Core is a platform business-domain concern rather than an optional
extension.

## Household as the Primary Aggregate

Not selected.

The current repository does not provide sufficient normative evidence that
Household and Family represent the same business concept.

Household remains future work pending explicit domain analysis.

---

# Migration Strategy

Migration SHALL be incremental.

Initial work will:

1. define and accept the Family Core architecture;
2. create canonical Person and Family domain specifications;
3. define domain primitives and invariants;
4. implement the Family Core independently from existing plugins;
5. integrate Identity and Security through explicit contracts;
6. migrate official plugins toward canonical Family Core references where
   necessary;
7. add application and presentation capabilities only after domain behavior is
   stable.

Existing plugins SHALL remain functional during migration.

No existing public plugin identifier SHALL be changed by this RFC.

---

# Backward Compatibility

RFC-0016 introduces a new domain boundary.

It does not require immediate breaking changes to existing official plugin
contracts.

Existing plugin-specific models may remain temporarily supported while canonical
Family Core integration is introduced incrementally.

Any future public contract migration SHALL require compatibility analysis before
implementation.

---

# Risks

## Over-modeling the Family Domain

Mitigation:

Keep the initial model limited to concepts required by demonstrated
cross-domain needs.

## Mixing Identity and Person

Mitigation:

Maintain an explicit normative separation between business Person and platform
Identity.

## Turning Relationships Into Authorization

Mitigation:

Family relationships provide business context only. Authorization remains a
Security responsibility.

## Premature Household Modeling

Mitigation:

Keep Household outside the initial normative model until its independent
business semantics are demonstrated.

## Plugin Coupling

Mitigation:

Family Core remains independent. Plugins depend on explicit Family Core
contracts rather than the inverse.

---

# Acceptance Criteria

The RFC is considered complete when all criteria below are satisfied.

- [ ] Family Core responsibility is explicitly defined.
- [ ] Person responsibility and boundaries are explicitly defined.
- [ ] Family responsibility and boundaries are explicitly defined.
- [ ] Person and Identity are explicitly separated.
- [ ] Family Membership semantics are defined.
- [ ] Family Relationship semantics are defined.
- [ ] Family Boundary semantics are defined.
- [ ] Domain ownership boundaries are explicit.
- [ ] Security integration boundaries are explicit.
- [ ] Existing plugin integration boundaries are explicit.
- [ ] Household treatment is explicitly decided or intentionally deferred.
- [ ] Migration expectations are documented.
- [ ] Compatibility implications are documented.
- [ ] Person Domain Specification requirements are established.
- [ ] Family Domain Specification requirements are established.
- [ ] No implementation-specific architecture is required to understand the
      decision.
- [ ] RFC review identifies no unresolved foundational ambiguity.
- [ ] RFC status can progress from Draft to Accepted through normal FamilyOS
      governance.

---

# Future Work

Future work may include:

- Person Domain Specification;
- Family Domain Specification;
- canonical family-domain identifiers;
- detailed family membership lifecycle;
- relationship taxonomy;
- family lifecycle;
- household modeling;
- domain events;
- application use cases;
- persistence ports and adapters;
- Identity integration;
- Security integration;
- official plugin migration;
- family knowledge management;
- controlled automation;
- family intelligence and AI capabilities.

A future implementation EPIC is expected to implement the accepted Family Core
contract.

The provisional implementation identifier is:

```text
EPIC-FAM-001 — Family Core Domain
```

This identifier is not created or considered active by this RFC baseline.

---

# Related Documents

## Foundation

- `docs/00-foundation/Domain-Architecture.md`
- `docs/00-foundation/Data-Architecture.md`
- `docs/00-foundation/Identity-Architecture.md`
- `docs/00-foundation/AI-Architecture.md`
- `docs/00-foundation/Roadmap.md`

## RFCs

- RFC-0010 — Security Plugin
- RFC-0011 — Health Plugin
- RFC-0012 — Finance Plugin
- RFC-0013 — Education Plugin
- RFC-0014 — Documents Plugin
- RFC-0015 — Official Communication Plugin

## ADRs

- ADR-0008 — Specification-Driven Platform
- ADR-0009 — Normative Validation Architecture

## Specifications

- SPEC-0002 — Identifier

---

# References

- FamilyOS Domain Architecture
- FamilyOS Data Architecture
- FamilyOS Identity Architecture
- FamilyOS Security Framework
- FamilyOS Roadmap

---

# Decision Record

| Field | Value |
|------|------|
| Decision | Draft |
| Architectural Impact | High |
| Breaking Change | No |
| Migration Required | Yes |
| Implementation Status | Not Started |
| Priority | High |
| Target Version | TBD |
