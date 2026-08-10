# Release Framework

# 10 Release Candidates

## Overview

EPIC-REL-001 — Release Framework defines a Release Candidate as the exact release configuration submitted for final release qualification.

A Release Candidate is not merely a label attached to ongoing development.

It is a controlled engineering object that binds together:

* release intent;
* source revision;
* intended version;
* artifact set;
* build identity;
* dependency state;
* release metadata;
* validation scope;
* documentation state;
* provenance evidence.

The Release Candidate establishes the precise subject of final release validation.

Its purpose is to ensure that the object being validated is the same object ultimately considered for approval and publication.

---

# Purpose

The Release Candidate model establishes:

* candidate identity;
* candidate creation;
* candidate numbering;
* candidate scope;
* candidate immutability;
* candidate evidence;
* candidate provenance;
* candidate validation boundaries;
* candidate invalidation;
* candidate iteration;
* candidate promotion;
* candidate rejection;
* candidate retention.

The model prevents release validation from being applied to an ambiguous or changing target.

---

# Candidate Principle

The central principle is:

> Final release validation must apply to an explicitly identified candidate.

A release process must not rely on a vague concept such as:

```text id="i5pfjy"
current source
```

or:

```text id="49zfge"
latest build
```

Instead, the release system should identify:

```text id="avfktk"
candidate
source revision
artifact set
version intent
validation evidence
```

as one coherent release object.

---

# Lifecycle Position

Release Candidate creation occurs after Release Readiness.

The lifecycle relationship is:

```text id="5avqga"
PREPARED
   ↓
READY
   ↓
[ CREATE RELEASE CANDIDATE ]
   ↓
CANDIDATE
   ↓
RELEASE VALIDATION
   ↓
VALIDATED
```

Candidate creation establishes a stronger release identity boundary.

---

# Candidate Definition

A Release Candidate is a stable configuration of release-relevant inputs and outputs intended for final qualification.

A conceptual candidate contains:

```text id="3sy953"
ReleaseCandidate
├── candidate identifier
├── release subject
├── target version
├── release type
├── target channel
├── source revision
├── build identity
├── artifact inventory
├── dependency state
├── configuration state
├── provenance
├── documentation state
└── validation scope
```

Not every implementation must materialize this exact structure immediately.

The semantics must remain available.

---

# Candidate Identity

Every formal candidate SHOULD have an unambiguous candidate identifier.

A canonical candidate version may use:

```text id="9eek67"
MAJOR.MINOR.PATCH-rc.N
```

Examples:

```text id="8ut5qr"
4.8.0-rc.1
4.8.0-rc.2
4.8.0-rc.3
```

Candidate identity must distinguish materially different candidate configurations.

---

# Candidate Numbering

Candidate numbers SHOULD normally increase monotonically.

Example:

```text id="59tgky"
4.8.0-rc.1
   ↓
change required
   ↓
4.8.0-rc.2
```

A candidate identifier SHOULD NOT be reused for a materially different candidate.

---

# Candidate and Target Version

The candidate version identifies a pre-release form of the intended stable version.

Example:

```text id="50nfys"
Candidate:
4.8.0-rc.2

Target Stable:
4.8.0
```

The candidate and stable release belong to the same intended release line.

---

# Candidate Creation Preconditions

A candidate SHOULD only be created after applicable Release Readiness requirements pass.

Typical preconditions include:

* scope sufficiently stable;
* release type selected;
* target version valid;
* source revision identifiable;
* build outputs available where applicable;
* required documentation sufficiently prepared;
* blocking readiness issues resolved;
* major dependencies known;
* release profile selected.

---

# Candidate Creation Gate

The transition:

```text id="vmnasn"
READY → CANDIDATE
```

should establish:

```text id="5rqn6k"
candidate identity
source identity
artifact identity
version intent
release metadata
validation scope
```

This gate marks the beginning of final candidate qualification.

---

# Candidate Source Revision

A candidate MUST map to a specific controlled source revision.

For Git-based FamilyOS releases, this normally means a specific commit.

Example:

```text id="mkhh74"
Candidate:
4.8.0-rc.1

Source Revision:
abc123def456
```

A moving branch name alone is insufficient candidate identity.

---

# Candidate Branch Context

A branch may provide useful lineage.

Example:

```text id="80y0hi"
Branch:
feature/foundation-engineering-docs

Commit:
abc123def456
```

The commit remains the stronger source identity.

Branches may continue moving after candidate creation.

---

# Candidate Build Identity

Where build artifacts exist, the candidate should identify the build that produced them.

Example:

```text id="yd8uhk"
Candidate:
4.8.0-rc.1

Build:
ci-3241
```

This allows the release system to distinguish multiple builds from the same development period.

---

# Candidate Artifact Set

The candidate must identify the exact artifact set intended for validation.

Conceptually:

```text id="ze2x1i"
Candidate Artifact Set
├── familyos-cli package
├── source archive
├── plugin package
├── release manifest
└── documentation bundle
```

Final release validation should operate on this exact set where practical.

---

# Candidate Artifact Identity

Artifacts should be identifiable through sufficient metadata.

Possible identity elements include:

* artifact name;
* version;
* checksum;
* build identifier;
* source revision;
* package metadata;
* platform target.

Filenames alone should not be the only identity mechanism where stronger evidence is practical.

---

# Candidate Dependency State

A candidate should preserve or reference its relevant dependency state.

Examples include:

* lockfile state;
* plugin compatibility dependencies;
* platform dependency versions;
* build dependencies;
* package dependency graph.

A material dependency change may invalidate candidate evidence.

---

# Candidate Configuration State

Release-relevant configuration must remain identifiable.

Examples include:

* build configuration;
* feature flags;
* target platform;
* release profile;
* packaging options;
* publication configuration where it affects artifacts.

A candidate cannot be considered stable if its artifact-producing configuration is changing invisibly.

---

# Candidate Documentation State

Release documentation associated with the candidate should be sufficiently mature for final validation.

This may include:

* changelog;
* release notes;
* compatibility notes;
* migration guidance;
* known issues;
* security notes.

Candidate documentation may receive non-material editorial corrections later.

Material changes must remain consistent with the actual release.

---

# Candidate Provenance

Candidate provenance should establish the relationship:

```text id="bf8ra5"
Source Revision
      ↓
Build
      ↓
Artifacts
      ↓
Candidate
```

The Release Framework must make it possible to reconstruct this relationship.

---

# Candidate Evidence

A candidate may accumulate evidence such as:

```text id="jlaowa"
source verification
build evidence
test evidence
quality evidence
security evidence
compliance evidence
artifact checksums
documentation validation
compatibility validation
```

Evidence must identify the candidate to which it applies.

---

# Candidate Stability

Once final validation begins, the candidate should be treated as stable.

The preferred rule is:

> Do not materially mutate a candidate under active qualification.

A candidate may still receive changes if the release process explicitly invalidates or refreshes affected evidence.

However, the default response to material change should be creation of a new candidate.

---

# Candidate Freeze

Candidate creation usually establishes a candidate freeze.

This may include:

* source freeze;
* artifact freeze;
* scope freeze;
* dependency freeze;
* version freeze.

The freeze does not mean that no correction is possible.

It means that corrections require controlled requalification.

---

# Material Change

A material candidate change is one that can alter release behavior, compatibility, artifact identity, security, or validation conclusions.

Examples include:

* source code change;
* dependency change;
* build configuration change;
* artifact replacement;
* schema change;
* compatibility change;
* release version change affecting artifact content;
* security correction.

Material changes require renewed qualification.

---

# Non-Material Change

Some changes may be non-material to the candidate.

Examples may include:

* spelling correction in release notes;
* formatting correction;
* metadata annotation that does not alter artifact identity;
* clarification of known issue wording.

Whether a change is material depends on release policy and context.

---

# Candidate Mutation Rule

The safest rule is:

```text id="b694hc"
material change
      ↓
candidate invalidated
      ↓
new candidate
```

For example:

```text id="zb88c2"
4.8.0-rc.1
      ↓
source correction
      ↓
4.8.0-rc.2
```

---

# Candidate Invalidation

A candidate becomes invalid when its validated identity no longer corresponds to the intended release.

Possible invalidation triggers include:

* source revision changed;
* artifact set changed;
* build changed;
* dependency state changed materially;
* compatibility state changed;
* release profile changed;
* significant security status changed;
* target version changed materially.

---

# Partial Evidence Invalidation

Not every change must necessarily invalidate every evidence domain.

Example:

```text id="dntqew"
release notes wording changed

source evidence          VALID
build evidence           VALID
test evidence            VALID
documentation evidence   RECHECK
```

A mature system should support dependency-aware evidence invalidation.

---

# Full Candidate Invalidation

Full invalidation is appropriate when:

* source revision changes;
* executable artifact changes;
* dependency graph changes materially;
* build configuration changes;
* candidate version changes in artifact-sensitive ways.

This normally requires new candidate identity.

---

# Candidate Iteration

A release may produce several candidates.

Example:

```text id="x23i67"
4.8.0-rc.1
  ↓
validation defect found
  ↓
fix
  ↓
4.8.0-rc.2
  ↓
security validation passes
  ↓
4.8.0-rc.3
  ↓
final qualification
```

Candidate iteration is expected behavior.

It must remain traceable.

---

# Candidate Rejection

A candidate may be rejected due to:

* validation failure;
* security finding;
* compatibility failure;
* documentation defect;
* artifact integrity failure;
* quality regression;
* release risk;
* governance decision.

Rejected candidates must not be promoted as stable releases.

---

# Rejected Candidate History

A rejected candidate MAY remain part of engineering history.

It may be useful for:

* debugging;
* validation history;
* security analysis;
* release process improvement.

It must not be confused with an official stable release.

---

# Candidate Withdrawal

A candidate may be withdrawn before final publication.

Reasons may include:

* release postponed;
* scope changed;
* better candidate created;
* dependency unavailable;
* risk unacceptable.

Candidate withdrawal is distinct from withdrawing an already published release.

---

# Candidate Promotion

Candidate promotion occurs when a candidate satisfies final release requirements and progresses toward stable identity.

Conceptually:

```text id="334k6t"
CANDIDATE
   ↓
VALIDATED
   ↓
APPROVED
   ↓
stable release identity
```

Promotion should preserve the validated candidate contents where practical.

---

# Promote, Do Not Rebuild

The preferred model is:

```text id="n760ad"
build candidate artifacts
        ↓
validate
        ↓
approve
        ↓
promote same artifacts
```

This provides stronger confidence that published artifacts are the ones actually validated.

---

# Rebuild Before Stable Release

Sometimes a rebuild may be unavoidable.

If stable artifacts are rebuilt after candidate validation:

```text id="f4x1g2"
candidate artifacts A
        ↓
validated
        ↓
stable artifacts B
```

then artifact B must receive sufficient renewed verification to establish equivalence or renewed validation.

The stable release must not inherit evidence blindly from artifacts A.

---

# Candidate-to-Stable Equivalence

The strongest candidate promotion model is:

```text id="wdxt4i"
candidate artifact checksum
=
stable artifact checksum
```

where the packaging and release process allows it.

This provides direct artifact identity continuity.

---

# Candidate Version Promotion

A candidate such as:

```text id="xkuv6b"
4.8.0-rc.2
```

may promote to:

```text id="y0k4bh"
4.8.0
```

when all stable release requirements pass.

The stable version is a distinct release identity, but it should represent the same validated release content where practical.

---

# Candidate Tags

FamilyOS MAY use candidate Git tags where useful.

Examples:

```text id="zyi055"
v4.8.0-rc.1
v4.8.0-rc.2
```

Candidate tags are optional unless required by the release profile.

Official stable tagging rules are defined separately.

---

# Candidate Tag Immutability

If candidate tags are used as validation anchors, they SHOULD be treated as immutable.

Moving a candidate tag destroys confidence in the evidence associated with it.

A changed candidate should receive a new tag.

---

# Candidate Branches

A dedicated release candidate branch MAY be used.

Example:

```text id="lh8il4"
release/4.8
```

However, the Release Framework does not require a release-branch model.

Candidate identity must not depend solely on a mutable branch reference.

---

# Candidate Manifest

A future FamilyOS release implementation may define a machine-readable candidate manifest.

Conceptually:

```text id="y2c9jk"
candidate:
  id: 4.8.0-rc.2
  target_version: 4.8.0

source:
  revision: abc123

build:
  id: ci-3241

artifacts:
  - name: familyos-cli
    checksum: ...

validation:
  profile: platform-stable
```

This is illustrative rather than a current schema requirement.

---

# Candidate Fingerprint

A future implementation MAY derive a candidate fingerprint from critical candidate inputs.

For example:

```text id="yfizjb"
source revision
+
build configuration
+
artifact checksums
+
dependency state
```

could produce a stable candidate fingerprint.

This could help detect accidental mutation.

---

# Candidate Storage

Candidate metadata may initially exist in:

* Git tags;
* CI/CD artifacts;
* repository files;
* release manifests;
* package metadata.

Future FamilyOS tooling may provide a dedicated candidate store.

The semantic model must remain independent from storage technology.

---

# Candidate Retention

Candidate retention policy may vary.

Final release candidates should generally retain sufficient evidence to reconstruct how the stable release was qualified.

Intermediate failed candidates may use shorter retention depending on governance.

---

# Final Candidate

The Final Candidate is the candidate that successfully passes final validation and receives release approval.

For example:

```text id="h40xfn"
4.8.0-rc.1   rejected
4.8.0-rc.2   rejected
4.8.0-rc.3   final candidate
```

The stable release should trace back to `4.8.0-rc.3`.

---

# Candidate Validation Scope

The applicable validation scope is determined by release profile.

For example, a framework candidate may require:

```text id="napk8s"
structure validation
documentation completeness
cross-reference validation
control document validation
Git state validation
```

A plugin candidate may require:

```text id="4xoszz"
build
unit tests
integration tests
plugin compliance
platform compatibility
artifact validation
```

---

# Candidate Security

Candidate handling is part of release security.

Candidate artifacts should be protected against:

* unauthorized replacement;
* ambiguous rebuild;
* dependency substitution;
* provenance loss;
* unauthorized promotion.

High-risk release candidates may require stronger controls.

---

# Candidate Access Control

Candidate publication or promotion authority may differ from candidate creation authority.

Conceptually:

```text id="kgf8rn"
create candidate
validate candidate
approve candidate
publish release
```

may be separate permissions.

This supports least privilege.

---

# Candidate Risk

A candidate may reveal new release risks during validation.

For example:

* unexpected compatibility issue;
* operational instability;
* performance regression;
* security concern;
* migration complexity.

Candidate risk changes may invalidate approval assumptions.

---

# Candidate and Release Notes

Release notes must eventually describe the Final Candidate accurately.

The release process should avoid situations where:

```text id="kdc7nc"
release notes describe rc.1
```

while:

```text id="53mt6f"
published release derives from rc.3
```

without documentation being updated accordingly.

---

# Candidate and Changelog

The changelog entry should reflect the final release scope.

Changes removed from later candidates should not remain represented as released functionality.

---

# Candidate and Known Issues

Known issues discovered during candidate qualification must be classified.

Possible outcomes include:

```text id="ms2e4a"
BLOCK
FIX IN NEXT CANDIDATE
ACCEPT
DOCUMENT
REQUIRE EXCEPTION
```

The final candidate must have an explicit known-issue state.

---

# Candidate and Compatibility

Compatibility validation should apply to the actual candidate.

A compatibility result from an earlier candidate may not remain valid after material change.

---

# Candidate and Security Validation

Security validation should identify the candidate being assessed.

If candidate contents change materially, affected security evidence must be refreshed.

---

# Candidate and Compliance

Compliance evaluation should likewise identify candidate scope.

For plugin candidates, this may include:

* manifest state;
* capabilities;
* policies;
* rules;
* metadata;
* compatibility.

---

# Candidate and Build Framework

EPIC-BLD-001 provides build outputs.

The candidate model selects the exact build outputs intended for release.

The relationship is:

```text id="09q2yz"
Build Framework
      ↓
Build Outputs
      ↓
Candidate Selection
      ↓
Release Candidate
```

---

# Candidate and Testing Framework

EPIC-TST-001 provides testing evidence.

The candidate model ensures that relevant test evidence applies to the correct release state.

---

# Candidate and Quality Framework

EPIC-QLT-001 provides quality evidence.

Quality status must correspond to the candidate or its source/artifact state.

---

# Candidate and Documentation Framework

EPIC-DOC-001 governs documentation quality and structure.

Candidate documentation is part of final release qualification where required.

---

# Candidate and Release Validation

`12-Release-Validation.md` defines how the candidate is finally qualified.

This document defines what the candidate is.

The relationship is:

```text id="o5l7y0"
Candidate Definition
      ↓
Candidate Identity
      ↓
Candidate Stability
      ↓
Release Validation
```

---

# Candidate and Governance

Release Governance defines:

* who may create candidates;
* who may approve candidate promotion;
* who may accept candidate risk;
* who may invalidate candidates;
* who may authorize stable publication.

---

# Candidate and Observability

Candidate lifecycle should be observable.

Possible events include:

```text id="s5l3wc"
candidate.created
candidate.validation.started
candidate.validation.failed
candidate.invalidated
candidate.rejected
candidate.approved
candidate.promoted
```

These event names are conceptual.

---

# Candidate and Auditability

A candidate record should eventually allow maintainers to answer:

```text id="4bvxxp"
Who created the candidate?

Which source did it use?

Which build produced its artifacts?

Which version did it target?

Which validation passed?

Which issues were found?

Why was it rejected or promoted?
```

---

# Candidate Status Model

A future candidate status model may include:

```text id="lrzz8v"
CREATED
VALIDATING
BLOCKED
REJECTED
VALIDATED
APPROVED
PROMOTED
WITHDRAWN
```

These states complement the broader Release Lifecycle.

---

# Candidate Validation Failure

When validation fails, the candidate should not silently return to development.

A clear outcome should be recorded.

Example:

```text id="vh20e4"
Candidate        4.8.0-rc.1
Validation       FAIL
Reason           compatibility regression
Status           REJECTED
Next Candidate   required
```

---

# Candidate Reuse

A previously rejected candidate SHOULD NOT later be silently reclassified as valid without renewed qualification.

If the reason for rejection was erroneous or external conditions changed, a documented re-evaluation may occur.

The evidence must remain explicit.

---

# Candidate Idempotency

Candidate creation tooling should avoid accidentally creating duplicate or conflicting candidate identities.

For example:

```text id="zc7eu3"
4.8.0-rc.2 already exists
```

should result in verification or blocking, not silent overwrite.

---

# Candidate Concurrency

Parallel release work may attempt to create candidate identities simultaneously.

Future tooling should prevent conflicts such as:

```text id="0fxvr3"
workflow A → 4.8.0-rc.2
workflow B → 4.8.0-rc.2
```

Candidate numbering may require coordination or reservation.

---

# Candidate Provenance Verification

Before final validation begins, the system should be able to establish:

```text id="wd2kqf"
candidate source verified
candidate build verified
candidate artifacts verified
candidate metadata verified
```

This ensures validation starts from a trusted candidate state.

---

# Candidate Checksums

Where release artifacts are files or packages, checksums SHOULD be used as candidate integrity evidence where practical.

Example:

```text id="8qj2bn"
artifact:
familyos-cli-4.8.0-rc.2.whl

sha256:
<digest>
```

The exact integrity mechanism is defined further in `11-Artifacts-and-Provenance.md`.

---

# Candidate Reproducibility

Where the Build Framework supports reproducibility, a candidate may be independently rebuilt and compared.

This can strengthen confidence that:

```text id="7c27yz"
candidate artifact
=
expected output from candidate source
```

Reproducibility is not a prerequisite for every current release profile, but the architecture supports it.

---

# Candidate Minimal Model

At minimum, a formal candidate should identify:

```text id="99k2mi"
candidate ID
target version
source revision
release scope
artifact set where applicable
validation profile
```

Without these elements, final validation may become ambiguous.

---

# Framework Candidate Example

A Release Framework candidate may conceptually be:

```text id="id20vb"
Candidate:
4.8.0-rc.1

Subject:
EPIC-REL-001 — Release Framework

Source:
specific Git commit

Scope:
docs/epics/EPIC-REL-001-release-framework/

Validation:
canonical structure
document completeness
control document alignment
cross-reference checks
repository checks

Target Stable:
4.8.0
```

---

# Plugin Candidate Example

A plugin candidate may be:

```text id="v9etub"
Candidate:
Finance Plugin 3.0.0-rc.2

Source:
plugin source revision

Artifacts:
finance plugin package

Validation:
unit tests
integration tests
plugin compliance
platform compatibility
artifact verification

Target:
Finance Plugin 3.0.0
```

---

# Platform Candidate Example

A platform candidate may aggregate multiple component states.

```text id="ceij7u"
Platform Candidate:
5.0.0-rc.1

Core:
5.0.0-rc.1

CLI:
5.0.0-rc.1

Plugins:
compatibility set

Documentation:
candidate documentation state

Specifications:
candidate specification state
```

Aggregation must remain explicit.

---

# Candidate Promotion Checklist

Before candidate promotion, the release process should verify:

```text id="c7l2o7"
candidate identity confirmed
source revision confirmed
artifact identity confirmed
validation complete
blocking findings zero
required exceptions approved
release notes aligned
version valid
approval granted
```

---

# Candidate Invariants

The following invariants apply.

## RCAND1 — Every formal release candidate has an explicit identity.

## RCAND2 — Every candidate maps to a controlled source state.

## RCAND3 — Candidate validation applies to the exact candidate.

## RCAND4 — Material candidate changes require renewed qualification.

## RCAND5 — Candidate identifiers are not reused for materially different contents.

## RCAND6 — Candidate evidence identifies the candidate it supports.

## RCAND7 — Rejected candidates must not be silently promoted.

## RCAND8 — Final stable release must trace back to a qualified candidate where candidate workflow is used.

## RCAND9 — Candidate artifacts should remain stable during final validation.

## RCAND10 — Candidate promotion should reuse validated artifacts where practical.

## RCAND11 — Candidate history must remain sufficiently traceable.

## RCAND12 — Candidate semantics must remain tool-independent.

---

# Candidate Anti-Patterns

## Moving Candidate

Validating a branch name whose underlying commit continues changing.

---

## Candidate-by-Filename

Assuming a package is the intended candidate solely because its filename contains the expected version.

---

## Reused RC Identifier

Replacing the contents of `rc.1` while keeping the same candidate identity.

---

## Validation Drift

Using validation results from one candidate to approve another.

---

## Rebuild-and-Publish

Validating candidate artifacts and then publishing newly rebuilt artifacts without equivalence verification.

---

## Candidate Without Source

Creating a candidate that cannot be traced to a specific source revision.

---

## Candidate Without Artifact Inventory

Publishing multiple release artifacts without identifying which ones belonged to the qualified candidate.

---

## Silent Rejection Recovery

Fixing defects after candidate failure without recording a new candidate or renewed validation.

---

# Minimum Candidate Process

At minimum, FamilyOS candidate qualification should follow:

```text id="9bgkea"
readiness passes
      ↓
select exact source revision
      ↓
identify candidate
      ↓
identify artifacts
      ↓
freeze material state
      ↓
validate candidate
      ↓
promote or reject
```

---

# Target Candidate Experience

At higher maturity, a maintainer should be able to inspect a candidate and receive:

```text id="dbwjps"
FamilyOS Release Candidate

Candidate            5.2.0-rc.3
Target Version       5.2.0
Type                 Platform
Source Revision      VERIFIED
Build                ci-4821
Artifacts            7 VERIFIED
Dependencies         LOCKED
Provenance           AVAILABLE
Documentation        READY
Validation Profile   platform-stable

Status               VALIDATING
```

After validation:

```text id="p52sjx"
Candidate            5.2.0-rc.3
Validation           PASS
Blocking Findings    0
Exceptions           0

Status               VALIDATED
```

---

# Candidate Maturity

FamilyOS candidate handling may mature through:

```text id="4lamkf"
Stage 1
Git commit + manual candidate record

Stage 2
standard rc versioning

Stage 3
candidate artifact inventory

Stage 4
candidate checksums

Stage 5
structured candidate manifest

Stage 6
automated evidence binding

Stage 7
candidate signing / attestations

Stage 8
policy-driven candidate promotion
```

---

# Relationship With Release Readiness

`09-Release-Readiness.md` determines whether a release may become a candidate.

This document defines the candidate created after that decision.

---

# Relationship With Artifacts and Provenance

`11-Artifacts-and-Provenance.md` defines the deeper identity, integrity, and provenance model for candidate artifacts.

---

# Relationship With Release Validation

`12-Release-Validation.md` defines how the exact candidate is qualified for approval.

---

# Relationship With Versioning

`06-Versioning-Strategy.md` defines candidate version syntax and stable target version semantics.

---

# Relationship With Tagging

`16-Tagging-and-Repository-State.md` defines final official release anchors and any candidate tag policies.

---

# Relationship With Publishing

`17-Publishing-and-Distribution.md` defines how a validated and approved candidate becomes published.

---

# Final Statement

The FamilyOS Release Candidate model establishes the exact engineering object on which final release confidence is built.

By binding source revision, version intent, build identity, artifact set, dependencies, configuration, documentation, provenance, and validation evidence into a controlled candidate identity, FamilyOS prevents release qualification from drifting across changing states.

A candidate is therefore not simply a temporary version label.

It is the stable release boundary that ensures the thing being validated is the thing intended to be approved and published.
