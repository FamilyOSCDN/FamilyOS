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
