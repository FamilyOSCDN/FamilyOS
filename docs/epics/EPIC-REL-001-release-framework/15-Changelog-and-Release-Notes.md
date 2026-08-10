# Release Framework

# 15 Changelog and Release Notes

## Overview

EPIC-REL-001 — Release Framework defines the rules governing changelogs and release notes across the FamilyOS ecosystem.

Changelogs and release notes are both release communication artifacts, but they serve different purposes.

The changelog provides a structured historical record of changes across versions.

Release notes provide release-specific communication describing what changed, why the release matters, what consumers should know, and whether migration or compatibility considerations apply.

The two artifacts may share source information.

They MUST NOT be treated as interchangeable.

---

# Purpose

The purpose of this document is to establish:

* changelog responsibilities;
* release note responsibilities;
* required content;
* version alignment;
* change classification;
* historical traceability;
* automation expectations;
* compatibility communication;
* migration communication;
* known issue disclosure;
* security communication;
* release-specific documentation validation;
* relationship with the Documentation Framework.

The objective is to ensure that FamilyOS releases are understandable both at the time of publication and years later.

---

# Core Principle

The central principle is:

> Release communication must describe the release that actually exists.

Documentation must not describe:

* an abandoned plan;
* an earlier candidate;
* an incomplete feature set;
* a different version;
* a different artifact state.

The release communication set must remain aligned with the final validated candidate and official release identity.

---

# Changelog Definition

A changelog is a structured historical record describing significant changes across FamilyOS versions.

Its primary purpose is historical traceability.

A changelog should allow maintainers and consumers to answer:

```text
What changed in version X?

When was it released?

What type of change occurred?

Which previous release preceded it?
```

The changelog is cumulative.

---

# Release Notes Definition

Release notes are a release-specific communication artifact.

Their purpose is to explain the significance and practical implications of one release.

Release notes should answer questions such as:

```text
Why does this release exist?

What are the important changes?

Are there breaking changes?

Is migration required?

Are there known limitations?

What compatibility considerations apply?

Are there security implications?
```

Release notes are not merely a copy of the changelog.

---

# Changelog vs Release Notes

The distinction is:

```text
CHANGELOG
historical record
version-oriented
structured
cumulative

RELEASE NOTES
release communication
audience-oriented
contextual
release-specific
```

Both should derive from the same factual release state.

---

# Documentation Ownership

The Documentation Framework governs:

* documentation standards;
* Markdown conventions;
* publication quality;
* metadata;
* traceability;
* documentation lifecycle.

The Release Framework governs:

* when release communication is required;
* which release identity it describes;
* which changes belong to the release;
* when documentation becomes release-ready.

These responsibilities must remain separate.

---

# Changelog Structure

A FamilyOS changelog SHOULD use a consistent version-oriented structure.

A conceptual model is:

```text
# Changelog

## [Unreleased]

### Added
### Changed
### Fixed
### Deprecated
### Removed
### Security

## [5.2.0]

### Added
...
```

The exact formatting remains governed by documentation standards.

---

# Unreleased Section

An `Unreleased` section MAY be used to accumulate changes intended for future releases.

Its purpose is to separate:

```text
changes already released
```

from:

```text
changes planned for the next release
```

Before publication, the relevant entries should be moved or transformed into the final version section.

---

# Change Categories

FamilyOS SHOULD use stable change categories.

Canonical categories include:

```text
Added
Changed
Fixed
Deprecated
Removed
Security
```

Additional categories MAY be introduced where they provide meaningful release information.

---

# Added

`Added` records new functionality or capability.

Examples include:

* new command;
* new plugin capability;
* new API;
* new framework section;
* new release feature.

---

# Changed

`Changed` records modifications to existing behavior or structure.

Examples include:

* workflow changes;
* architecture changes;
* compatibility changes;
* revised default behavior.

Changes with compatibility impact must be called out explicitly.

---

# Fixed

`Fixed` records corrections.

Examples include:

* bug fixes;
* broken documentation references;
* build correction;
* release workflow correction.

---

# Deprecated

`Deprecated` records functionality that remains available but is scheduled for future removal or replacement.

Deprecation entries should identify:

* deprecated behavior;
* replacement where applicable;
* expected removal policy if known.

---

# Removed

`Removed` records functionality or behavior no longer available.

Removal may imply compatibility impact and therefore must align with versioning policy.

---

# Security

`Security` records security-related changes suitable for public disclosure.

Sensitive information must be handled according to security release policy.

The changelog must not disclose confidential vulnerability information prematurely.

---

# Changelog Version Identity

Every released changelog section MUST use the correct official release version.

For example:

```text
## [5.2.0]
```

must correspond to the actual release version.

The changelog must not contain:

```text
## [5.2.0]
```

if the final release was published as:

```text
5.3.0
```

---

# Version Consistency

Version identity must remain consistent across:

```text
release version
Git tag
changelog
release notes
artifact metadata
release manifest
```

Any conflict must be resolved before release completion.

---

# Changelog Release Date

Released changelog entries SHOULD include a release date where appropriate.

Example:

```text
## [5.2.0] - 2026-08-10
```

Dates should represent the actual release publication date according to applicable documentation conventions.

---

# Historical Immutability

Published changelog history SHOULD remain stable.

Historical corrections may be made when factual errors are discovered.

Such corrections should not rewrite release meaning silently.

The preferred approach is to preserve historical traceability.

---

# Changelog Correction

A factual changelog correction MAY be made without changing the original release identity when the correction affects documentation only.

However, the correction should not falsely imply that software behavior changed retroactively.

---

# Changelog Completeness

A release changelog entry should represent all significant changes relevant to consumers and maintainers.

It does not need to list every internal commit.

The purpose is meaningful change history, not raw commit duplication.

---

# Commit Log Is Not Changelog

The following is insufficient as a release changelog:

```text
commit abc
commit def
commit ghi
```

Commit messages are engineering history.

A changelog is curated release history.

---

# Pull Requests Are Not Changelog

Similarly, a list of pull requests does not automatically constitute a useful changelog.

Automation may use pull request metadata as input.

The resulting changelog should still present meaningful release categories.

---

# Release Notes Structure

Release notes SHOULD normally include the following areas where applicable:

```text
Release identity
Summary
Highlights
Changes
Compatibility
Migration
Known issues
Security
Upgrade guidance
Recovery considerations
```

Not every release requires every section.

---

# Release Identity

Release notes must clearly identify the release.

Example:

```text
FamilyOS 5.2.0
```

or:

```text
EPIC-REL-001 — Release Framework
Version 4.8.0
```

The identity must match official release metadata.

---

# Release Summary

The summary should explain why the release exists.

Example concepts include:

* introduces a new framework;
* adds platform capability;
* fixes stability issues;
* publishes security remediation;
* updates documentation architecture.

The summary should remain concise and accurate.

---

# Highlights

Release highlights may identify the most significant changes.

Highlights should be selective.

They should not simply duplicate every changelog item.

---

# Change Details

Release notes may expand on important changelog items where consumers need more context.

For example:

```text
Changelog:
Added plugin compatibility validation.

Release Notes:
Plugin compatibility is now verified before stable publication,
reducing the risk of incompatible plugin-platform combinations.
```

---

# Compatibility Section

Release notes MUST include compatibility information when the release changes supported relationships.

Relevant areas may include:

```text
platform ↔ plugin
CLI ↔ API
schema ↔ data
configuration ↔ runtime
```

Compatibility must not be left implicit when materially affected.

---

# Breaking Changes

Breaking changes must be clearly visible.

They should not be buried among minor fixes.

Release notes should identify:

* what changed;
* who is affected;
* why it changed;
* required migration;
* replacement path where applicable.

---

# Migration Section

A migration section is required when consumers must take action to move from a previous supported version.

Migration information may include:

* configuration changes;
* schema changes;
* command changes;
* API changes;
* plugin changes;
* data migration.

Migration steps should reflect validated behavior.

---

# Upgrade Guidance

Upgrade guidance may describe:

```text
supported source versions
required sequence
pre-upgrade steps
post-upgrade checks
```

For simple releases, this may be minimal.

---

# Known Issues

Known non-blocking issues SHOULD be disclosed where they are relevant to consumers.

A known issue entry should ideally include:

* affected functionality;
* impact;
* workaround where available;
* expected future resolution.

Known issues must not be hidden simply because they were accepted for release.

---

# Security Notes

Security-related release communication must balance:

* transparency;
* consumer actionability;
* responsible disclosure.

Security release notes may include:

* affected versions;
* fixed version;
* risk summary;
* required action;
* mitigation.

Sensitive technical detail may be published separately according to security policy.

---

# Security Advisory Relationship

A security advisory is distinct from general release notes.

Release notes may reference the existence of a security fix.

A dedicated advisory may provide detailed security information.

The Security Framework or security governance defines disclosure depth.

---

# Rollback Information

Where rollback is supported and operationally relevant, release notes MAY include rollback considerations.

Example:

```text
Rollback supported to 5.1.x
```

or:

```text
Rollback not supported after schema migration.
Forward recovery required.
```

This information must align with validated recovery behavior.

---

# Release Notes for Framework Releases

A FamilyOS framework release should normally describe:

* framework purpose;
* canonical architecture;
* major normative areas;
* relationship with previous frameworks;
* version;
* tag;
* validation status.

For example, EPIC-REL-001 release notes should explain that the Release Framework establishes formal release engineering architecture across FamilyOS.

---

# Release Notes for Plugin Releases

Plugin release notes may include:

* plugin version;
* platform compatibility;
* capabilities added;
* compliance status;
* configuration changes;
* known issues;
* migration requirements.

---

# Release Notes for Platform Releases

Platform release notes may need broader structure.

Possible areas include:

```text
platform changes
CLI changes
plugin compatibility
API changes
schema changes
security changes
migration
known issues
```

Platform notes should provide an integrated view.

---

# Release Notes for Documentation Releases

Documentation release notes may be lighter.

They should identify:

* documentation scope;
* major corrections;
* new specifications or frameworks;
* version impact.

---

# Release Notes for Maintenance Releases

Maintenance notes should focus on:

* defects corrected;
* reliability improvements;
* security fixes;
* compatibility impact;
* known remaining issues.

---

# Release Notes for Emergency Releases

Emergency release notes may initially be concise due to urgency.

However, minimum information should include:

```text
release identity
reason for emergency
affected behavior
consumer action
known risk
```

Documentation may be expanded after immediate stabilization if governance permits.

---

# Candidate Release Notes

Release candidate notes may exist before stable publication.

They should clearly identify candidate status.

Example:

```text
FamilyOS 5.2.0-rc.2
Release Candidate
```

They must not be represented as stable release notes.

---

# Stable Release Notes

Stable release notes should be generated or finalized from the Final Candidate.

Any material difference between candidate and stable release must be reflected before publication.

---

# Release Note Freeze

Release note content becomes increasingly stable as the candidate approaches approval.

Material content changes may be required when:

* candidate changes;
* known issues change;
* compatibility changes;
* version changes.

Editorial improvements may continue later if factual meaning remains unchanged.

---

# Changelog Freeze

The release's changelog entry should be considered final once the stable scope is finalized.

Changes after final validation should trigger review of changelog consistency.

---

# Release Communication Gate

Before stable publication, the release process should verify:

```text
changelog ready
release notes ready
version aligned
compatibility documented
migration documented where required
known issues documented
security communication ready where required
```

Missing mandatory release communication may block publication.

---

# Documentation Readiness Relationship

`09-Release-Readiness.md` evaluates whether release communication is sufficiently prepared to create a candidate.

This document defines the communication content and semantics.

---

# Final Validation Relationship

`12-Release-Validation.md` confirms that changelog and release notes describe the actual Final Candidate.

---

# Changelog Source Data

FamilyOS MAY progressively use structured change data.

Potential sources include:

* pull request labels;
* change fragments;
* issue metadata;
* conventional commit metadata;
* release plan entries.

No specific mechanism is mandated by this document.

---

# Change Fragments

A future FamilyOS workflow may use change fragments created during development.

Conceptually:

```text
changes/
├── 123.added.md
├── 124.fixed.md
└── 130.security.md
```

At release time, automation could consolidate these into changelog entries.

This is an optional future capability.

---

# Structured Change Record

Another possible model is:

```text
change:
  type: added
  component: release
  description: Introduce release candidate validation.
```

Machine-readable change data can improve automation while preserving human-readable output.

---

# Automation Principle

Automation may assist changelog and release note generation.

It must not publish inaccurate generated text without appropriate review.

The governing principle is:

> Automate collection and formatting; preserve factual review.

---

# Automatic Version Insertion

The release workflow SHOULD automate version insertion where practical.

This reduces mismatch between:

```text
5.2.0
```

and accidental:

```text
5.1.0
```

in release documents.

---

# Automatic Date Insertion

Release date insertion may also be automated at publication time.

This ensures the date represents actual release timing rather than planning assumptions.

---

# Automatic Comparison Links

Where the hosting platform supports it, changelog entries may include links comparing versions.

For example:

```text
previous tag → current tag
```

This supplements curated change information.

It does not replace it.

---

# Release Note Generation

Automation may generate a draft such as:

```text
Release 5.2.0

Added
- feature A

Fixed
- defect B
```

Human review may then add:

* significance;
* migration context;
* compatibility;
* known issues.

---

# AI-Assisted Release Notes

Future FamilyOS tooling MAY use AI assistance for drafting release notes.

AI-generated content must be verified against authoritative release data.

It must not invent changes, compatibility guarantees, or security information.

The release evidence remains authoritative.

---

# Release Notes and Artifact Set

Release notes should correspond to the actual published artifact set.

If a package expected in the notes was removed from the Final Candidate, the notes must be updated.

---

# Release Notes and Versioned Components

Platform releases may contain independently versioned components.

Release notes should expose meaningful version relationships.

Example:

```text
FamilyOS Platform 5.2.0

Security Plugin 4.1.0
Finance Plugin 3.2.0
Documents Plugin 3.0.1
```

where relevant.

---

# Release Notes and Channels

Pre-release channels must be clearly identified.

For example:

```text
5.2.0-rc.1
Channel: Candidate
```

Stable notes should not contain ambiguous preview language unless the release itself is preview.

---

# Release Notes and Support Status

Release communication may identify:

* stable;
* maintenance;
* deprecated;
* unsupported;
* withdrawn.

Support status must remain separate from version identity.

---

# Withdrawn Release Communication

If a release is withdrawn, its release notes should remain historically discoverable where appropriate.

They should be updated or annotated to indicate:

```text
WITHDRAWN
```

and provide:

* reason;
* replacement version;
* consumer action.

The original release history must not be erased.

---

# Superseded Release Communication

A superseded release may remain available.

Release metadata may indicate:

```text
Superseded by 5.2.1
```

This helps consumers understand the recommended upgrade path.

---

# Rolled-Back Release Communication

If a release is rolled back operationally, its history must remain intact.

Release notes may record:

* rollback status;
* affected deployment;
* corrected release;
* recommended version.

---

# Release Documentation Integrity

Release communication itself is part of release integrity.

Incorrect release notes can cause:

* invalid migrations;
* incompatible upgrades;
* security exposure;
* operational confusion.

Documentation validation is therefore a release control, not merely editorial polish.

---

# Documentation Validation

Validation should check:

```text
release version consistency
candidate consistency
changelog completeness
release note existence
breaking change visibility
migration information
known issue accuracy
security communication where applicable
```

---

# Release Notes Approval

High-risk release notes MAY require specialized review.

Examples include:

* security release;
* major platform release;
* breaking changes;
* public API changes.

Governance defines required reviewers.

---

# Release Communication Ownership

The Release Owner is responsible for ensuring that release communication is complete.

Domain owners may contribute technical content.

Documentation specialists may ensure structure and quality.

Security owners may control sensitive disclosure.

---

# Audience Model

Release notes may serve multiple audiences:

```text
maintainers
developers
plugin authors
administrators
users
security stakeholders
```

One release note document may serve several audiences, or specialized documents may be produced.

---

# Consumer-Oriented Content

Release notes should prioritize practical information.

Consumers generally need to know:

* what changed;
* whether they are affected;
* whether upgrade is safe;
* what action is required.

Internal implementation detail should be included only where useful.

---

# Maintainer-Oriented Content

Maintainer notes may additionally include:

* architectural implications;
* deprecations;
* internal migration;
* compatibility constraints;
* follow-up work.

---

# Machine-Readable Release Notes Metadata

Future FamilyOS releases may expose structured metadata alongside human-readable release notes.

Conceptual example:

```text
release:
  version: 5.2.0
  type: platform
  channel: stable

changes:
  breaking: false
  security: true

compatibility:
  minimum_plugin_api: 3
```

This does not replace human-readable communication.

---

# Release Communication Evidence

Final release evidence should identify:

```text
changelog version
release notes version
documentation validation result
publication location
```

This supports historical reconstruction.

---

# Changelog Retention

The changelog should be a durable repository artifact.

It should survive:

* CI/CD changes;
* release hosting changes;
* contributor turnover.

The changelog is part of long-term project history.

---

# Release Notes Retention

Release notes should also remain accessible for historical official releases.

Consumers and maintainers may need them years later for:

* migration;
* debugging;
* compatibility;
* incident investigation.

---

# Release Note Publication Targets

Release notes may be published through:

* Git repository release page;
* documentation site;
* package registry metadata;
* generated release documentation.

At least one authoritative representation should remain accessible.

---

# Changelog and Release Notes Consistency

The two artifacts must not contradict one another.

Example invalid state:

```text
Changelog:
Feature X added

Release Notes:
Feature X postponed
```

The release communication set must be reconciled before completion.

---

# Release Notes and Commit State

Release notes should normally be included in or traceable to the release source state where applicable.

This prevents release communication from becoming detached from the released repository history.

---

# Comparison With Previous Release

Release notes SHOULD identify the meaningful delta from the previous release.

This may include:

* added features;
* corrected defects;
* compatibility changes;
* migration requirements.

The previous release must be correctly identified.

---

# Initial Release Notes

For a first release with no predecessor, release notes should clearly describe the initial capability rather than forcing artificial change comparisons.

---

# Major Release Notes

Major releases should provide stronger communication.

They SHOULD prominently include:

* breaking changes;
* migration guidance;
* removed functionality;
* compatibility changes;
* support policy changes;
* deprecations.

---

# Minor Release Notes

Minor releases should emphasize:

* new capabilities;
* compatible enhancements;
* notable improvements;
* any migration concerns.

---

# Patch Release Notes

Patch releases should focus on:

* fixes;
* security corrections;
* reliability improvements;
* known remaining limitations.

---

# Release Communication Checklist

Before publication, the following questions should be answerable:

```text
Does the changelog contain the release?

Does the version match everywhere?

Do release notes describe the Final Candidate?

Are breaking changes visible?

Is migration documented where required?

Are known issues disclosed?

Is compatibility clear?

Is security communication complete?

Are recovery implications documented where needed?
```

---

# Framework Release Changelog Example

A FamilyOS framework milestone may use:

```text
## [4.8.0]

### Added

- Release Framework.
- Release lifecycle model.
- Release candidate architecture.
- Release validation architecture.
- Release governance and compliance model.
```

The exact content must reflect the final framework scope.

---

# Framework Release Notes Example Structure

Conceptually:

```text
# FamilyOS 4.8.0 — Release Framework

## Summary

Establishes the official FamilyOS Release Framework.

## Highlights

- Release lifecycle
- Versioning strategy
- Release candidates
- Provenance
- Validation
- Automation
- Governance
- Recovery

## Compatibility

Documentation and engineering framework release.

## Migration

No runtime migration required.
```

This example is illustrative, not the final EPIC-REL-001 release note.

---

# Release Note Generation Pipeline

A future automation flow may be:

```text
structured changes
      ↓
changelog generation
      ↓
candidate release notes
      ↓
human / policy review
      ↓
final candidate
      ↓
version finalization
      ↓
release note finalization
      ↓
publication
```

---

# Release Communication Failure

Missing or inaccurate required release communication must block release progression where applicable.

Examples include:

* wrong release version;
* missing breaking change notice;
* missing required security notice;
* migration steps inconsistent with candidate;
* changelog omits a significant released change.

---

# Documentation-Only Correction

A purely editorial correction after release may not require a new software version if governance permits documentation to evolve independently.

However, if the corrected documentation itself is published as a new official release artifact, an appropriate release identity may be required.

---

# Release Communication and Immutability

Release communication may require factual correction after publication.

The correction must not silently redefine the released software.

Where possible, history should show the correction.

---

# Changelog Anti-Patterns

## Raw Commit Dump

Copying Git history directly into the changelog.

---

## Missing Version

Recording changes without clear release identity.

---

## Retroactive Feature Addition

Editing an old changelog entry to claim functionality that was not actually present in that release.

---

## Unreleased Drift

Allowing unreleased entries to remain indefinitely without clear release mapping.

---

# Release Note Anti-Patterns

## Changelog Copy

Publishing the changelog entry verbatim as release notes without practical context.

---

## Candidate Drift

Publishing release notes prepared for an earlier candidate.

---

## Hidden Breaking Changes

Mentioning incompatible behavior only deep inside technical details.

---

## Migration by Assumption

Telling consumers to upgrade without validating the migration path.

---

## Security Overexposure

Publishing sensitive vulnerability detail before coordinated disclosure.

---

## Marketing Without Engineering Facts

Producing release notes that emphasize promotion while omitting compatibility, migration, or known limitations.

---

# Changelog Invariants

The following invariants apply.

## CL1 — Every significant official release has a traceable changelog record where the project uses a changelog.

## CL2 — Released changelog entries use the correct official version.

## CL3 — Changelog history reflects actual released changes.

## CL4 — Breaking and security-relevant changes are classified appropriately.

## CL5 — Historical release meaning must not be silently rewritten.

## CL6 — Changelog structure remains consistent enough for human and automated use.

---

# Release Notes Invariants

## RN1 — Required release notes identify the exact official release.

## RN2 — Release notes describe the Final Candidate.

## RN3 — Breaking changes are clearly communicated.

## RN4 — Migration is documented when consumer action is required.

## RN5 — Known material limitations are disclosed where appropriate.

## RN6 — Compatibility information is explicit when relevant.

## RN7 — Security communication follows disclosure governance.

## RN8 — Release notes remain historically accessible where required.

## RN9 — Release notes and changelog must not contradict each other.

## RN10 — Release communication is part of release readiness and validation.

---

# Minimum Changelog Requirements

At minimum, a FamilyOS changelog entry should identify:

```text
version
significant changes
change categories
release date where required
```

---

# Minimum Release Notes Requirements

At minimum, significant release notes should identify:

```text
release version
release purpose
important changes
compatibility impact
migration requirements where applicable
known material issues
```

---

# Target Release Communication Experience

At higher maturity, a FamilyOS release workflow should be able to report:

```text
Release Communication

Version               6.0.0
Changelog             READY
Release Notes         READY
Breaking Changes      DOCUMENTED
Migration             VERIFIED
Compatibility         DOCUMENTED
Known Issues          DOCUMENTED
Security Notes        READY
Version Consistency   PASS

COMMUNICATION READY
```

This result should be based on structured release evidence.

---

# Relationship With Versioning

`06-Versioning-Strategy.md` defines official version semantics.

Changelog and release notes must consistently use that version.

---

# Relationship With Release Planning

`08-Release-Planning.md` determines which release documentation is required.

---

# Relationship With Release Readiness

`09-Release-Readiness.md` verifies that required communication is sufficiently prepared before candidate creation.

---

# Relationship With Release Candidates

`10-Release-Candidates.md` establishes the exact candidate the release communication must describe.

---

# Relationship With Release Validation

`12-Release-Validation.md` verifies that release communication is consistent with the Final Candidate.

---

# Relationship With Release Automation

`13-Release-Automation.md` may automate collection, version insertion, changelog generation, and release note drafting.

---

# Relationship With Documentation Framework

EPIC-DOC-001 remains authoritative for documentation standards, formatting, quality, metadata, and lifecycle.

EPIC-REL-001 defines the release-specific obligations applied to changelogs and release notes.

---

# Relationship With Publishing

`17-Publishing-and-Distribution.md` defines how release notes and release communication become officially published.

---

# Relationship With Release Security

`19-Release-Security.md` defines security-related disclosure and integrity requirements.

---

# Final Statement

The FamilyOS Changelog and Release Notes model establishes release communication as a first-class part of release engineering.

The changelog preserves structured historical change information.

Release notes explain the significance and practical impact of a specific release.

By keeping these responsibilities distinct while binding both to the same validated release identity, FamilyOS gains release documentation that supports traceability, compatibility, migration, security communication, operational clarity, and long-term platform history.

A release should never force maintainers or consumers to guess what changed, whether they are affected, or which actions they must take.
