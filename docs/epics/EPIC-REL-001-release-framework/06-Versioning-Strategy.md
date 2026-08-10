# Release Framework

# 06 Versioning Strategy

## Overview

EPIC-REL-001 — Release Framework defines the versioning strategy used to identify and order official FamilyOS releases.

Versioning is a core part of release identity.

A version is not merely a label.

It communicates:

* release order;
* compatibility expectations;
* release maturity;
* change magnitude;
* release stability;
* historical position.

The FamilyOS versioning strategy must remain predictable, explicit, automation-friendly, and compatible with long-term ecosystem growth.

---

# Purpose

The Versioning Strategy establishes:

* canonical version semantics;
* release version structure;
* major, minor, and patch meaning;
* pre-release identifiers;
* release candidate identifiers;
* version increment rules;
* version uniqueness;
* tag relationships;
* platform versioning;
* component versioning;
* plugin versioning;
* compatibility implications;
* emergency and maintenance versioning;
* version validation requirements.

The strategy prevents arbitrary version selection and inconsistent release identities.

---

# Versioning Principle

Every official FamilyOS release MUST have an explicit version identity.

The version must:

* follow the applicable versioning rules;
* be unique within its release domain;
* correspond to a specific release state;
* remain stable after publication;
* support historical ordering.

The same version MUST NOT identify materially different official releases.

---

# Canonical Version Model

FamilyOS adopts a semantic version structure as its default release versioning model.

The canonical structure is:

```text
MAJOR.MINOR.PATCH
```

For example:

```text
4.8.0
```

The three components communicate different types of evolution.

---

# Major Version

The `MAJOR` component represents significant platform evolution.

A major version SHOULD increase when changes introduce substantial compatibility impact or architectural transition.

Examples may include:

* incompatible public API changes;
* incompatible plugin platform changes;
* major CLI contract changes;
* significant platform architecture transitions;
* removal of previously supported behavior;
* changes requiring explicit migration;
* major governance or release model transitions where version semantics require it.

Example:

```text
4.9.3
   ↓
5.0.0
```

A major increment resets:

```text
MINOR = 0
PATCH = 0
```

---

# Minor Version

The `MINOR` component represents backward-compatible feature or capability evolution within a major release line.

A minor version SHOULD increase for changes such as:

* new platform capabilities;
* new official plugin capabilities;
* new framework functionality;
* new compatible commands;
* compatible API additions;
* significant new documentation frameworks;
* compatible behavior extensions.

Example:

```text
4.8.2
   ↓
4.9.0
```

A minor increment resets:

```text
PATCH = 0
```

---

# Patch Version

The `PATCH` component represents backward-compatible corrections or limited maintenance evolution.

Patch versions SHOULD normally be used for:

* bug fixes;
* documentation corrections;
* security fixes without incompatible change;
* small quality improvements;
* limited internal refactoring;
* packaging corrections;
* release metadata corrections requiring a new official release;
* maintenance changes.

Example:

```text
4.8.0
   ↓
4.8.1
```

---

# Version Ordering

Versions follow numeric ordering.

For example:

```text
4.7.0
<
4.7.1
<
4.8.0
<
4.9.0
<
5.0.0
```

Version ordering must remain deterministic.

Automation MUST NOT rely on lexical string ordering where that could produce incorrect results.

---

# Pre-Release Versions

FamilyOS may use pre-release identifiers before stable publication.

Canonical syntax:

```text
MAJOR.MINOR.PATCH-PRERELEASE
```

Examples:

```text
4.8.0-alpha.1
4.8.0-beta.1
4.8.0-rc.1
```

Pre-release versions represent a release line that has not yet reached final stable status.

---

# Pre-Release Ordering

Within a target version, maturity normally progresses as:

```text
alpha
  ↓
beta
  ↓
rc
  ↓
stable
```

For example:

```text
4.8.0-alpha.1
4.8.0-alpha.2
4.8.0-beta.1
4.8.0-rc.1
4.8.0-rc.2
4.8.0
```

A stable version has higher release maturity than its associated pre-release versions.

---

# Alpha Releases

Alpha releases represent early pre-release states.

They MAY contain:

* incomplete functionality;
* unstable interfaces;
* known defects;
* experimental behavior;
* incomplete compatibility guarantees.

Alpha releases are not considered stable production releases.

Example:

```text
4.9.0-alpha.1
```

---

# Beta Releases

Beta releases represent more mature pre-release states.

They SHOULD normally have:

* substantially complete intended functionality;
* broader validation;
* fewer known blocking defects;
* stronger compatibility expectations than alpha releases.

Example:

```text
4.9.0-beta.1
```

---

# Release Candidates

Release candidate versions use:

```text
MAJOR.MINOR.PATCH-rc.N
```

Example:

```text
4.9.0-rc.1
```

A release candidate represents a specific candidate for final stable release.

If a material change is required after candidate validation, a new candidate number SHOULD be created.

Example:

```text
4.9.0-rc.1
    ↓
change required
    ↓
4.9.0-rc.2
```

---

# Stable Releases

A stable release omits the pre-release suffix.

Example:

```text
4.9.0
```

A stable release represents an officially qualified release intended for normal supported consumption according to the applicable release channel and policy.

---

# Release Candidate to Stable Promotion

The preferred model is:

```text
4.9.0-rc.2
      ↓
final validation
      ↓
4.9.0
```

Where practical, the stable release SHOULD promote the same validated artifact set.

The stable release MUST NOT silently introduce material changes that were absent from the final candidate.

If material changes occur, renewed candidate validation is required.

---

# Build Metadata

Where technically useful, version identifiers MAY include build metadata.

Example:

```text
4.9.0+build.145
```

Build metadata may identify:

* CI build;
* build environment;
* internal artifact generation;
* provenance context.

Build metadata MUST NOT redefine the official precedence semantics of the stable release version.

Official public release identity should remain as simple as practical.

---

# Version Domain

A version is meaningful within a defined release domain.

Possible FamilyOS version domains include:

```text
platform
CLI
plugin
framework
specification
schema
API
```

Not all domains require independent versioning.

Independent versioning should only be introduced where it provides clear engineering value.

---

# Platform Version

The FamilyOS platform version identifies an official integrated platform release.

Example:

```text
v4.8.0
```

A platform release may represent a coherent state across:

* core platform;
* CLI;
* official plugin compatibility;
* documentation;
* specifications;
* release metadata.

The platform version is the primary high-level release identity where applicable.

---

# Component Version

A component MAY have an independent version when its lifecycle requires independent release identity.

Examples may include:

* official plugin;
* SDK;
* standalone library;
* separately distributed CLI;
* independent integration adapter.

Component versioning MUST remain compatible with the platform release model.

---

# Avoiding Version Proliferation

FamilyOS SHOULD avoid creating independent versions merely because an asset can technically be versioned.

Independent versioning introduces complexity in:

* compatibility;
* dependency management;
* release planning;
* documentation;
* support;
* upgrade paths.

A component should receive an independent version only when it has a meaningful independent lifecycle.

---

# Plugin Versioning

Official plugins MAY use semantic versions independently from the platform.

Example:

```text
Platform: 4.8.0
Security Plugin: 3.2.0
Finance Plugin: 2.4.1
```

When plugin versions are independent, compatibility information MUST remain explicit.

For example:

```text
Finance Plugin 2.4.1
requires FamilyOS >= 4.7.0
```

The precise compatibility format may be defined by plugin metadata specifications.

---

# Framework Versioning

FamilyOS engineering frameworks may be released using platform milestone versions or independently tracked framework versions according to repository governance.

When framework releases are represented by repository tags such as:

```text
v4.7.0-build-framework
```

the numeric prefix remains the release version.

The suffix communicates the release subject.

---

# Versioned Tag Pattern

A canonical FamilyOS tag pattern may use:

```text
v<version>-<release-subject>
```

Examples:

```text
v4.7.0-build-framework
v4.8.0-release-framework
v4.9.0-security-plugin
```

The tag naming strategy is governed in detail by:

```text
16-Tagging-and-Repository-State.md
```

The versioning strategy governs the numeric version semantics.

---

# Version and Tag Separation

A version and a Git tag are related but distinct concepts.

For example:

```text
Version
4.8.0
```

may correspond to:

```text
Tag
v4.8.0-release-framework
```

The version expresses release semantics.

The tag anchors the release to repository state.

The framework MUST NOT treat the entire tag string as the version value when release subject metadata is appended.

---

# Version Uniqueness

An official version MUST be unique within its release domain.

Before publication, the release process should verify:

```text
version not already used
```

and, where relevant:

```text
tag not already present
```

Reusing an official version for different content is prohibited.

---

# Version Immutability

Once an official version is published, its meaning MUST remain stable.

A correction MUST normally result in a new version.

For example:

```text
4.8.0
problem discovered
    ↓
4.8.1
```

not:

```text
4.8.0
artifact silently replaced
```

---

# Version Intent

Version selection begins before final release publication.

The lifecycle may use:

```text
version intent
```

during planning and preparation.

Example:

```text
next intended version: 4.8.0
```

This is not yet an official release version until release identity is finalized.

---

# Tentative Version

A tentative version MAY change before release candidate creation.

For example:

```text
planned: 4.8.0
```

may become:

```text
4.9.0
```

if release scope changes materially.

Tentative versions must not be confused with published versions.

---

# Candidate Version

Candidate versions identify specific release candidates.

Example:

```text
4.8.0-rc.1
```

Candidate numbering SHOULD increase monotonically for the same target stable version.

---

# Final Version

The final release version becomes authoritative when the release reaches the release identity stage.

Conceptually:

```text
candidate
4.8.0-rc.2

        ↓ approval

final version
4.8.0
```

---

# Version Calculation

Version calculation may initially remain a governed manual process.

As FamilyOS release automation matures, version selection SHOULD become increasingly machine-verifiable.

Automation may validate:

* current version;
* requested next version;
* change classification;
* release type;
* existing tags;
* branch policy.

Automation MAY calculate a recommended next version.

Final authority remains defined by governance.

---

# Change Classification

Version decisions should consider the nature of changes.

A conceptual classification is:

```text
BREAKING
FEATURE
FIX
SECURITY
DOCUMENTATION
INTERNAL
```

Typical mapping:

```text
BREAKING
→ MAJOR

FEATURE
→ MINOR

FIX
→ PATCH
```

Security, documentation, and internal changes may map according to compatibility and release impact.

---

# Breaking Changes

A breaking change is one that invalidates a supported compatibility expectation.

Examples may include:

* removed public command;
* incompatible API change;
* incompatible persisted data format;
* plugin contract break;
* configuration contract break;
* removed supported behavior.

Breaking changes SHOULD normally require a major version increment.

---

# Compatible Features

New backward-compatible functionality SHOULD normally require a minor version increment.

Examples include:

* new command;
* new optional API;
* new plugin capability;
* new supported workflow;
* new framework capability.

---

# Compatible Fixes

Backward-compatible corrections SHOULD normally require a patch increment.

Examples include:

* bug correction;
* documentation correction;
* internal reliability fix;
* packaging fix;
* non-breaking security fix.

---

# Security Releases

Security releases follow normal version semantics unless security policy requires exceptional treatment.

A backward-compatible security correction may use:

```text
PATCH
```

An incompatible security correction may require:

```text
MINOR
```

or:

```text
MAJOR
```

depending on compatibility impact.

Security urgency does not eliminate versioning rules.

---

# Emergency Releases

Emergency releases SHOULD use the next valid version according to change impact.

An emergency release must not reuse an existing version simply because rapid publication is required.

Example:

```text
4.8.0
critical issue
    ↓
4.8.1
```

---

# Maintenance Releases

Maintenance releases normally use patch increments within an active release line.

Example:

```text
4.8.0
4.8.1
4.8.2
```

If FamilyOS later maintains multiple supported major or minor lines, each line must preserve independent monotonic ordering.

---

# Hotfix Versioning

A hotfix is operationally urgent but does not require a special incompatible version syntax.

A normal semantic patch is preferred.

Example:

```text
4.8.3
```

rather than inventing:

```text
4.8.2-hotfix-final2
```

except where a pre-release workflow specifically requires such metadata.

---

# Documentation-Only Releases

Documentation-only changes may still require a new official version if they are independently published as part of the repository release history.

The increment depends on release policy.

A patch increment is generally appropriate when the change does not alter software compatibility.

---

# Framework Release Versions

Major framework completion milestones may intentionally use minor or major platform sequence increments according to FamilyOS repository release strategy.

The Release Framework must not force every documentation framework change into a purely software-library interpretation if the repository governance defines milestone versioning across the engineering platform.

However, version increments must remain systematic and documented.

---

# Version Sequence Integrity

Version history MUST remain monotonic within a release domain.

The following is valid:

```text
4.7.0
4.8.0
4.9.0
```

The following should normally be rejected:

```text
4.9.0
4.8.5
```

for a single forward-moving canonical release line unless `4.8.x` is an explicitly maintained historical branch.

---

# Parallel Maintenance Lines

Future FamilyOS maturity may require parallel maintenance.

Example:

```text
5.2.0  current stable
4.9.7  supported maintenance line
```

In this case, version monotonicity applies within each supported line.

Release metadata must make branch lineage explicit.

---

# Branch and Version Relationship

The Versioning Strategy does not require one specific branch model.

Possible future models include:

```text
main
release/4.x
release/5.x
```

or a simpler trunk-based model.

Regardless of branch architecture, version identity must remain unambiguous.

Branch names do not replace versions.

---

# Version and Compatibility

Version changes SHOULD communicate compatibility expectations.

Consumers should be able to reason approximately that:

```text
PATCH
low compatibility risk

MINOR
compatible capability expansion

MAJOR
potential compatibility break
```

This is a contract expectation, not a guarantee that every change has identical operational risk.

---

# Version and Release Type

Release type and version are separate concepts.

For example:

```text
4.8.1
```

may be:

```text
maintenance release
security release
emergency release
```

The release type provides operational context.

The version provides identity and compatibility semantics.

---

# Version and Channel

Release channel is also separate from version.

For example:

```text
4.9.0-rc.1
channel: candidate
```

and:

```text
4.9.0
channel: stable
```

A channel must not replace version identity.

---

# Version and Build Identity

Build identity is distinct from release version.

Example:

```text
Release Version:
4.8.0

Build ID:
ci-2841
```

Multiple internal builds may occur before one release candidate is selected.

The Release Framework must preserve the exact build chosen for release.

---

# Version and Artifact Identity

Artifacts should encode or expose release version where appropriate.

Examples:

```text
familyos-4.8.0.tar.gz
familyos_cli-4.8.0-py3-none-any.whl
```

Filename inclusion is helpful but not sufficient as the sole identity mechanism.

Artifact metadata and provenance should also establish version relationship.

---

# Version and Release Notes

Release notes MUST reference the corresponding official release version.

Release documentation must not create ambiguity between:

```text
planned version
candidate version
final version
```

Final release notes should describe the final official version.

---

# Version and Changelog

The changelog should record versions consistently.

A release entry may use:

```text
## [4.8.0]
```

or another format defined by documentation standards.

The version referenced must match the actual release identity.

---

# Version Validation

Before official release identity is established, version validation should verify:

```text
syntax valid
version increment valid
version unique
tag name valid
tag unique
candidate relationship valid
release type compatible
```

Additional checks may be introduced as release automation matures.

---

# Invalid Version Examples

Examples that should normally be rejected include:

```text
4.8
```

when full semantic versioning is required.

```text
v4.8.0
```

when the field expects a version rather than a tag.

```text
4.08.0
```

if leading-zero rules prohibit it.

```text
4.8.0-final-final
```

when no governed pre-release identifier permits it.

---

# Version Parsing

Automation SHOULD use a structured version parser rather than ad hoc string splitting.

Version processing should distinguish:

```text
major
minor
patch
pre-release
build metadata
```

This reduces errors in ordering and validation.

---

# Version Source of Truth

FamilyOS should eventually define an authoritative source for the intended software version.

Possible implementations include:

* project metadata;
* release manifest;
* generated version file;
* package metadata.

The exact mechanism is not established by this document.

The architectural requirement is that conflicting version declarations be detected.

---

# Single Source of Version Truth

Where possible, the same canonical version value SHOULD drive:

```text
package version
release metadata
release notes
tag generation
artifact naming
```

Duplicated manually maintained versions create release risk.

---

# Derived Version Data

Some release information may be derived from the canonical version.

For example:

```text
version = 4.8.0

tag = v4.8.0-release-framework
artifact = familyos-4.8.0.tar.gz
release title = FamilyOS 4.8.0
```

Derived values SHOULD be generated where practical instead of independently entered.

---

# Version Governance

Version policy changes are governed Release Framework changes.

Examples include changing:

* semantic meaning;
* tag version formatting;
* pre-release identifiers;
* component version independence;
* compatibility interpretation.

Such changes must be documented and versioned.

---

# Version Authority

The authority to finalize an official version is defined by Release Governance.

Automation MAY verify or recommend a version.

Automation MUST NOT silently choose a version outside applicable policy.

---

# Version Reservation

At higher release maturity, FamilyOS MAY reserve a version during candidate preparation.

Version reservation can prevent parallel workflows from attempting to publish the same version.

A reservation is not equivalent to official publication.

---

# Concurrent Release Risk

Parallel release work may create conflicts such as:

```text
workflow A → intends 4.9.0
workflow B → intends 4.9.0
```

Future release orchestration should detect and prevent conflicting final publication.

---

# Version Provenance

Release evidence SHOULD record:

```text
previous version
selected version
candidate version
final version
version decision context
```

This improves historical reconstruction.

---

# Version Migration

If FamilyOS ever changes versioning strategies, migration must preserve historical version interpretation.

Existing releases MUST NOT be retroactively renumbered merely to fit a new strategy.

A migration should define a clear boundary.

Example:

```text
Versions <= 5.x
legacy policy

Versions >= 6.0.0
new policy
```

---

# Version Deprecation

Versions themselves are historical identifiers and should not be deleted.

A release version may become:

```text
deprecated
superseded
withdrawn
unsupported
```

but its identity remains valid.

---

# Version Support Status

Support status is independent from version identity.

Example:

```text
4.8.0
status: superseded

4.8.4
status: supported

5.0.0
status: stable
```

A future support policy may define maintenance windows.

---

# Version Aliases

Human-friendly aliases such as:

```text
latest
stable
current
```

MAY exist for distribution convenience.

They MUST resolve to explicit version identities.

Aliases are mutable references.

Official version identities are immutable historical anchors.

---

# Stable Alias

A `stable` alias may move from:

```text
4.8.0
```

to:

```text
4.9.0
```

after promotion.

This does not change either release identity.

---

# Latest Alias

The concept of `latest` must be used carefully.

It may mean:

* highest published version;
* newest stable version;
* newest release regardless of channel.

Any implementation MUST define which meaning applies.

---

# Version Invariants

The following invariants apply.

## VSN1 — Every official release has a version.

## VSN2 — Official versions are unique within their release domain.

## VSN3 — Published versions are immutable.

## VSN4 — Version ordering is deterministic.

## VSN5 — Version increments follow documented semantics.

## VSN6 — Candidate versions remain distinguishable from stable versions.

## VSN7 — Version identity remains distinct from Git tag identity.

## VSN8 — Component versioning must not create hidden compatibility ambiguity.

## VSN9 — Version reuse is prohibited.

## VSN10 — Corrective releases receive new versions.

## VSN11 — Version changes are traceable in release evidence.

## VSN12 — Version semantics are tool-independent.

---

# Versioning Anti-Patterns

## Arbitrary Increment

Choosing the next number without considering release semantics.

---

## Version Reuse

Publishing different content under an existing version.

---

## Tag-as-Version Confusion

Treating:

```text
v4.8.0-release-framework
```

as the semantic version instead of:

```text
4.8.0
```

---

## Candidate Mutation

Changing release contents while preserving the same candidate identifier without revalidation.

---

## Hidden Component Version

Publishing independently evolving components without explicit component version identity.

---

## Version Explosion

Introducing independent versions for every internal artifact without lifecycle justification.

---

## Filename Authority

Treating a filename as the authoritative version source.

---

## Mutable Stable Version

Replacing artifacts under an already published stable version.

---

## Unordered Labels

Using version names that cannot be reliably compared or ordered.

---

# Current FamilyOS Mapping

The current FamilyOS engineering milestone strategy already uses release tags similar to:

```text
v4.5.0-plugin-compliance-framework
v4.6.0-quality-framework
v4.7.0-build-framework
```

Under this strategy:

```text
4.5.0
4.6.0
4.7.0
```

are semantic release versions.

The suffix identifies the primary milestone or release subject.

The expected next framework milestone may therefore follow the sequence:

```text
v4.8.0-release-framework
```

provided release validation confirms that this version remains correct according to repository state at final publication.

---

# Future Automation Example

A future version check may conceptually produce:

```text
Current Release       4.7.0
Requested Release     4.8.0
Change Type           FEATURE / FRAMEWORK
Expected Increment    MINOR
Version Syntax        PASS
Version Ordering      PASS
Version Uniqueness    PASS
Tag Availability      PASS

VERSION VALID
```

This is an implementation target rather than a required current interface.

---

# Versioning Maturity

FamilyOS versioning may mature through the following stages.

```text
Stage 1
Documented manual version selection

Stage 2
Automated version syntax validation

Stage 3
Automated tag and uniqueness validation

Stage 4
Change classification support

Stage 5
Automated version recommendation

Stage 6
Structured component compatibility

Stage 7
Release orchestration with version reservation
```

---

# Relationship With Release Lifecycle

Version state evolves across the lifecycle.

```text
PLANNED
tentative version

PREPARED
version intent

CANDIDATE
pre-release / candidate version

VALIDATED
validated candidate version

APPROVED
approved final version intent

RELEASED
official immutable version
```

This model prevents tentative version planning from being confused with official publication.

---

# Relationship With Release Types and Channels

`07-Release-Types-and-Channels.md` defines whether a release is:

* development;
* preview;
* candidate;
* stable;
* maintenance;
* emergency;
* security.

This document defines how that release is versioned.

The two concerns must remain coordinated but distinct.

---

# Relationship With Release Candidates

`10-Release-Candidates.md` defines candidate stability and identity.

Candidate versioning defined here provides a standard mechanism such as:

```text
4.8.0-rc.1
4.8.0-rc.2
```

---

# Relationship With Tagging

`16-Tagging-and-Repository-State.md` defines how the release version becomes anchored to Git repository state.

The expected relationship is:

```text
Release Version
      ↓
Tag Name
      ↓
Git Commit
```

---

# Relationship With Changelog and Release Notes

`15-Changelog-and-Release-Notes.md` must use the final version identity consistently across all release communication.

---

# Minimum Versioning Requirements

At minimum, every FamilyOS official release process must verify:

```text
version exists
version syntax valid
version is unique
version is greater than applicable predecessor
tag does not conflict
release documentation uses same version
```

These checks can initially be manual.

They should become automated over time.

---

# Target Versioning State

The target FamilyOS versioning model is one in which version selection becomes predictable and verifiable.

A release workflow should eventually be able to determine:

```text
Current Version
Change Classification
Applicable Version Policy
Expected Next Version
Candidate Version
Final Version
Tag Name
```

without requiring maintainers to reconstruct prior version logic manually.

---

# Final Statement

The FamilyOS Versioning Strategy establishes versions as stable engineering identities rather than arbitrary labels.

It defines semantic version structure, major/minor/patch meaning, pre-release and release candidate semantics, component and platform version relationships, version immutability, and version governance.

By establishing predictable version semantics, FamilyOS gains a reliable foundation for tagging, compatibility, publication, release history, automation, and long-term ecosystem evolution.
