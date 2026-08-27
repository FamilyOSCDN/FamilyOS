# Responsibilities

## Domain

The Family domain owns the canonical business meaning, continuity, invariants,
and lifecycle semantics of Family, Family Membership, Family Relationship, and
Family Boundary.

It is part of the Family Core established by RFC-0016 and consumes the canonical
Person contract without redefining Person.

The Family domain SHALL remain independent from authentication technology,
authorization policy, plugin-local models, persistence technology, transport
representation, and presentation concerns.

## Core Responsibilities

### Family Identity and Continuity

The Family domain SHALL own the canonical Family identity contract.

A Family SHALL retain stable domain identity independently from:

- its current Membership set;
- any single Person;
- display information;
- household composition;
- authentication state;
- authorization state;
- plugin-owned records;
- persistence representation;
- infrastructure storage.

The canonical implementation name of Family identity is `FamilyId`.

The concrete representation and runtime invariants of `FamilyId` SHALL be
defined by the Family domain model before runtime implementation depends on it.

Changing Membership, Relationship, Security policy, or plugin records SHALL NOT
implicitly replace or redefine canonical Family identity.

### Family Membership

The Family domain SHALL own Family Membership semantics.

Family Membership represents the explicit association of exactly one canonical
Person with exactly one canonical Family context.

The Family domain SHALL define:

- the Membership business invariant set;
- Membership lifecycle states and valid transitions;
- the rules that determine whether Membership is valid for a business decision;
- temporal and historical expectations for Membership;
- interaction between Membership lifecycle and Family continuity;
- application-facing behavior required to establish or evolve Membership;
- persistence expectations required by normative Membership behavior.

Membership SHALL remain semantically distinct from:

- Person;
- Family;
- Family Relationship;
- authentication Identity;
- authorization;
- role or permission assignment;
- plugin-local association records.

The Family domain SHALL NOT redefine canonical Person identity in order to
represent Membership.

Membership validity SHALL NOT itself mean that an action is authorized.

### Family Relationship

The Family domain SHALL own Family Relationship semantics.

Family Relationship represents explicit family relationship knowledge between
canonical Persons where such meaning is governed by the Family specification.

The Family domain SHALL define, before applicable runtime implementation:

- Relationship semantics and invariants;
- directionality rules;
- symmetry or asymmetry rules;
- the initial taxonomy or the governed mechanism by which taxonomy is defined;
- temporal validity where required;
- historical expectations where required;
- identity requirements if a dedicated stable Relationship identity becomes
  necessary;
- domain events required by normative Relationship behavior.

Relationship SHALL remain semantically distinct from Membership.

A Relationship SHALL NOT automatically:

- create Membership;
- activate Membership;
- revoke Membership;
- mutate Membership;
- establish authorization;
- establish a Security role or permission.

The Family domain SHALL NOT infer a Relationship merely because two Persons are
members of the same Family.

### Family Boundary

The Family domain SHALL own the business semantics of Family Boundary.

Family Boundary represents the business isolation associated with one canonical
Family context.

The Family domain SHALL define:

- how a Family Boundary is derived from canonical Family Core facts;
- Family Boundary invariants;
- the meaning of cross-family business context;
- the circumstances under which Family contexts remain isolated;
- the Family facts that Security may consume when evaluating access across or
  within a Family Boundary.

Family Boundary SHALL remain distinct from authorization policy.

The existence of a Family Boundary SHALL NOT by itself grant or deny any
specific operation.

Security remains responsible for authorization decisions.

### Family Lifecycle

The Family domain SHALL define the lifecycle semantics required to preserve
Family continuity.

Family lifecycle SHALL remain distinct from:

- Membership lifecycle;
- Relationship lifecycle;
- Identity lifecycle;
- account lifecycle;
- Security policy lifecycle;
- persistence lifecycle.

Removing or changing one Membership SHALL NOT by itself change canonical Family
identity.

The Family domain SHALL explicitly determine whether additional Family lifecycle
states are required before runtime implementation introduces them.

No adapter or application workflow SHALL invent generic `ACTIVE`, `ARCHIVED`,
`DELETED`, or equivalent Family states merely because they are common storage or
CRUD patterns.

### Family Events

The Family domain SHALL own the business meaning of canonical Family Core domain
events.

The specification SHALL define the events required by an implementation-ready
subset before runtime code emits or persists those events as canonical facts.

Event transport, envelopes, brokers, dispatch technology, retries, and delivery
mechanisms remain infrastructure or application concerns unless separately
governed.

No implementation SHALL invent a canonical Family, Membership, Relationship, or
Boundary event merely to satisfy an infrastructure integration.

### Family Data Integrity

The Family domain SHALL define integrity expectations intrinsic to Family-owned
business facts.

At minimum, Family-owned facts SHALL preserve:

- canonical Family identity;
- canonical Person references where applicable;
- Membership validity semantics;
- Relationship semantic distinctions;
- Family Boundary isolation semantics;
- historical meaning where required by the applicable lifecycle contract.

Persistence or migration SHALL NOT silently rewrite Family Core business truth
to satisfy storage convenience.

### Family Privacy Expectations

Family Core information may be sensitive because it describes family context,
membership, relationships, and family boundaries.

The Family domain SHALL identify privacy expectations intrinsic to the business
meaning of Family-owned data.

Concrete privacy policy, consent, lawful basis, disclosure rules, retention
periods, erasure mechanisms, access enforcement, and security-sensitive
presentation remain governed by the applicable Privacy, Security, Data
Architecture, governance, and infrastructure contracts.

The Family domain SHALL NOT make authorization policy intrinsic Family state.

## Cross-Domain Responsibilities

### Person Interaction

The Person domain owns canonical Person identity, continuity, and Person
lifecycle.

The Family domain MAY reference a Person only through the governed canonical
Person contract.

Family Membership SHALL reference canonical Person identity rather than create a
Family-owned Person identity.

The Family domain SHALL NOT:

- redefine `PersonId`;
- create a second canonical Person model;
- derive Person identity from Membership;
- mutate Person identity through Family lifecycle;
- treat Family participation as intrinsic Person state;
- make Person existence dependent on Membership.

Person and Family specifications SHALL remain consistent on historical
references, lifecycle interactions, privacy assumptions, compatibility
expectations, and domain-event integration points.

### Identity Interaction

Identity represents a platform actor recognized by FamilyOS.

Family Core business facts MAY be associated with platform Identity through
separately governed integration contracts.

The Family domain SHALL NOT:

- own authentication credentials;
- treat account activation as Family lifecycle;
- make Identity the source of truth for Family Membership;
- make Identity the source of truth for Family Relationship;
- infer canonical Family facts from authentication state.

Identity SHALL NOT redefine Family Core business truth.

### Security Interaction

Security owns authorization evaluation, policy, roles, permissions, and
enforcement.

Family Core MAY provide approved Family, Membership, Relationship, and Boundary
facts as Security context.

The Family domain SHALL NOT:

- treat Membership as permission;
- treat Relationship as permission;
- treat Family existence as permission;
- treat Family Boundary as an authorization decision;
- encode Security roles as Family facts;
- redefine denied or allowed Security decisions as Family lifecycle.

Security SHALL NOT redefine Family Core facts merely to make an authorization
decision.

### Privacy and Governance Interaction

Privacy and governance authorities own applicable privacy policy, disclosure
policy, retention requirements, erasure requirements, consent rules, and
regulatory obligations.

The Family domain owns the business semantics that those policies act upon.

Privacy processing SHALL NOT silently reinterpret canonical Family identity,
Membership history, Relationship meaning, or Family Boundary semantics.

The exact mechanics remain separately governed.

### Official Plugin Interaction

Official domain plugins MAY reference canonical Family Core concepts through
approved contracts.

Plugin-specific records remain owned by their respective domains.

A plugin SHALL NOT become authoritative for:

- canonical Family identity;
- Membership lifecycle;
- Relationship semantics;
- Family Boundary semantics.

Existing plugin-local family-like, member-like, or relationship-like identifiers
SHALL NOT become canonical Family Core identity merely because they predate the
Family Core implementation.

Compatibility and migration SHALL be explicit.

### Infrastructure Interaction

Infrastructure SHALL persist and transport Family Core state without becoming
authoritative for its business meaning.

Infrastructure MAY select implementation technology where the specification
leaves representation open.

Infrastructure SHALL NOT:

- create competing Family identity;
- collapse Membership and Relationship;
- reinterpret storage absence as Family business semantics;
- turn authorization policy into Family state;
- invent lifecycle states;
- infer Household as Family.

### Interface Interaction

Interfaces SHALL present and accept Family Core information through governed
application contracts.

CLI, HTTP, RPC, messaging, UI, plugin interfaces, and other transports SHALL NOT
own Family business invariants.

Transport-specific representations SHALL preserve the canonical semantic
distinctions defined by the Family specification.

## Explicitly Excluded Responsibilities

The Family domain does not own:

- canonical Person identity or Person lifecycle;
- platform actor Identity;
- authentication credentials;
- authentication mechanisms;
- Security roles;
- permissions;
- authorization policy;
- authorization enforcement;
- plugin-specific business records;
- generic user or account profiles;
- database schemas;
- ORM models;
- transport protocols;
- UI state;
- workflow-engine semantics;
- AI behavior;
- household semantics in the initial canonical model;
- universal retention or erasure policy;
- universal storage deletion semantics.

These exclusions preserve the ownership boundaries established by RFC-0016.

## Responsibility Invariants

The following responsibility invariants are normative:

1. Family business identity is owned by the Family domain.
2. `FamilyId` is the canonical Family identity name.
3. Person identity remains owned by the Person domain.
4. Family Membership references Person but does not own Person identity.
5. One Membership associates exactly one Person with exactly one Family context.
6. Membership lifecycle is owned by the Family domain.
7. Membership validity does not itself grant authorization.
8. Family Relationship is distinct from Membership.
9. Relationship does not itself grant authorization.
10. Family Boundary is distinct from authorization policy.
11. Security may consume Family Core facts but does not own or redefine them.
12. Identity may integrate with Family Core but does not own Membership or
    Relationship truth.
13. Official plugins may reference Family Core but do not own canonical Family
    Core semantics.
14. Infrastructure persists Family Core state but does not define its business
    meaning.
15. Household is not synonymous with Family and remains deferred.
16. Runtime code SHALL NOT resolve a genuinely deferred Family-domain semantic
    without specification governance.

## Household Responsibility Boundary

`Household` is not part of the initial canonical Family Core model.

Current architectural evidence is insufficient to determine whether Household
is:

- a distinct Family Core concept;
- owned by another domain;
- a future Family concept;
- unnecessary for FamilyOS.

Household therefore remains intentionally deferred.

No Family implementation SHALL:

- alias Household to Family;
- infer Family from shared residence;
- introduce Household as an implicit aggregate;
- derive Membership from household composition.

A future governed specification MAY revisit Household without changing the
current Family identity and ownership contracts unless that future analysis
requires an explicit architectural update.

## Identifier Responsibility Boundary

The Family domain owns the canonical `FamilyId` contract.

The Family specification SHALL resolve `FamilyId` representation and runtime
invariants before implementation relies on it.

No dedicated canonical Membership identifier is established by this document.

No dedicated canonical Relationship identifier is established by this
document.

If future Membership or Relationship semantics require stable public or
persisted identity, that identity SHALL be specified explicitly before runtime
code treats it as canonical.

Application, infrastructure, plugin, or persistence code SHALL NOT invent stable
Membership or Relationship identifiers merely for implementation convenience.

## Deferred Responsibility Details

The following responsibility decisions remain intentionally deferred until
required by an implementation-ready Family subset:

- exact `FamilyId` runtime representation;
- Family lifecycle states beyond the continuity rules already established;
- dedicated Membership identity, if any;
- exact Membership lifecycle state names and transitions;
- dedicated Relationship identity, if any;
- Relationship directionality and symmetry rules;
- Relationship taxonomy;
- Relationship temporal and historical mechanics;
- detailed Family Boundary derivation mechanics;
- complete Family Core event catalog;
- concrete application command/query shapes;
- concrete persistence port technology;
- transaction mechanics;
- event-dispatch mechanics;
- compatibility mapping mechanisms;
- concrete privacy, retention, erasure, and disclosure mechanisms.

These items SHALL NOT be silently frozen by runtime implementation.

## Implementation Responsibility Gate

The responsibility boundaries established by this document are necessary but
not sufficient by themselves to authorize Family runtime implementation.

Before an applicable Family runtime slice proceeds, the Family specification
must also define the domain model, invariants, identifiers, lifecycle behavior,
events, capabilities, failure semantics, persistence expectations, and other
contracts required by that slice.

Implementation MAY proceed incrementally only for a fully specified subset.

Runtime code SHALL NOT invent unresolved business responsibilities.

## Normative References

- `docs/30-domains/family/README.md`
- `docs/30-domains/family/Vision.md`
- `docs/30-domains/person/README.md`
- `docs/30-domains/person/Domain-Model.md`
- `docs/30-domains/person/Responsibilities.md`
- `docs/rfcs/RFC-0016-family-core-domain/RFC-0016-Family-Core-Domain.md`
- `docs/00-foundation/Domain-Architecture.md`
- `docs/00-foundation/Data-Architecture.md`
- `docs/00-foundation/Identity-Architecture.md`
- `docs/00-foundation/Security-Architecture.md`
- `docs/04-reference/Naming-Conventions.md`
- `docs/06-specifications/SPEC-0008-Naming-Conventions.md`
