# Release Framework

# 08 Release Planning

## Overview

EPIC-REL-001 — Release Framework defines Release Planning as the structured activity that converts release intent into a concrete, reviewable, and executable release plan.

Release Planning occurs before formal readiness evaluation.

Its purpose is to determine:

* what will be released;
* why the release exists;
* which components are involved;
* which release type applies;
* which target channel applies;
* which version is intended;
* which dependencies exist;
* which validation is required;
* which documentation must be prepared;
* which risks must be considered;
* which approvals may be required;
* which publication targets are expected;
* which recovery strategy is appropriate.

A release that is not adequately planned may still technically be publishable, but it is not sufficiently governed.

---

# Purpose

The purpose of Release Planning is to establish a controlled release scope before candidate qualification begins.

Release Planning must reduce uncertainty around:

```text
scope
version
dependencies
compatibility
validation
risk
documentation
authority
publication
recovery
```

The output of planning should provide enough information for Release Preparation and Release Readiness to proceed without relying on undocumented assumptions.

---

# Planning Principle

The central planning principle is:

> A release should be understood before it is qualified.

Planning must not be confused with approval.

A planned release may still:

* change;
* be blocked;
* be postponed;
* be cancelled;
* require a different version;
* require additional validation;
* require additional scope.

Planning provides structure, not guaranteed publication.

---

# Planning Lifecycle Position

Release Planning primarily operates during:

```text
PLANNED
   ↓
PREPARED
```

It may begin before the formal `PLANNED` state and may continue until readiness evaluation begins.

The relationship is:

```text
Release Intent
      ↓
Release Planning
      ↓
Defined Scope
      ↓
Prepared Release
      ↓
Release Readiness
```

---

# Release Intent

Every planned release should begin with a clear release intent.

Release intent answers:

> Why does this release exist?

Typical release intents include:

* new capability delivery;
* framework completion;
* maintenance;
* defect correction;
* security correction;
* plugin publication;
* compatibility update;
* documentation update;
* emergency correction;
* platform milestone.

A release without clear intent risks accumulating unrelated changes and becoming difficult to validate.

---

# Release Scope

Release scope identifies exactly what is intended to change.

Scope may include:

* components;
* packages;
* plugins;
* frameworks;
* documentation;
* configuration;
* schemas;
* specifications;
* generated assets.

The scope should be specific enough to determine applicable release requirements.

---

# Scope Example

A framework release scope may be:

```text
Release:
EPIC-REL-001 — Release Framework

Scope:
docs/epics/EPIC-REL-001-release-framework/

Includes:
00-EPIC.md
01-Context.md
...
31-Implementation-Checklist.md
control documents
```

This scope is materially different from a full FamilyOS platform release.

---

# Scope Boundaries

A release plan should identify both:

```text
IN SCOPE
```

and:

```text
OUT OF SCOPE
```

This prevents unrelated work from entering the candidate unintentionally.

For example:

```text
IN SCOPE
Release Framework documentation

OUT OF SCOPE
CLI implementation
Release orchestration implementation
CI/CD implementation
artifact signing implementation
```

---

# Scope Stability

Release scope may evolve during planning.

Once readiness evaluation begins, scope changes should become increasingly controlled.

A material scope expansion should normally cause renewed preparation.

Example:

```text
Prepared:
documentation-only release

change:
runtime code added

result:
release scope and profile must be reassessed
```

---

# Release Type Selection

Planning must identify the applicable release type.

Examples include:

```text
framework
plugin
platform
maintenance
security
documentation
emergency
```

Release type influences:

* required evidence;
* validation depth;
* governance;
* publication targets;
* recovery planning.

---

# Target Channel Selection

Where channels are applicable, planning should identify the intended channel.

Examples:

```text
development
preview
candidate
stable
maintenance
```

The intended channel influences qualification requirements.

A release targeting `stable` should normally require stronger readiness than one targeting `development`.

---

# Release Profile Selection

Planning should select or determine the applicable release profile.

A release profile may define:

* mandatory checks;
* required evidence;
* approvals;
* documentation;
* publication targets;
* post-release verification;
* recovery expectations.

Example:

```text
Profile:
framework-release
```

may require different checks from:

```text
Profile:
plugin-release
```

---

# Version Intent

Release Planning should establish an intended version.

For example:

```text
Current:
4.7.0

Intended:
4.8.0
```

The version remains provisional until final release qualification.

Version intent provides a basis for:

* documentation;
* candidate naming;
* tag planning;
* changelog preparation;
* compatibility assessment.

---

# Version Decision Inputs

Version intent should consider:

* previous release;
* change scope;
* compatibility impact;
* release type;
* repository sequence;
* applicable versioning policy.

A version must not be selected simply because it appears numerically convenient.

---

# Version Reassessment

If release scope changes materially, version intent must be reassessed.

For example:

```text
planned:
patch release

scope change:
breaking API modification

result:
major version decision required
```

Version changes during planning are acceptable.

Uncontrolled version changes after candidate validation are not.

---

# Release Dependency Planning

A release may depend on other components or releases.

Dependencies may include:

* minimum platform version;
* plugin compatibility;
* specification version;
* schema version;
* build tooling;
* external package;
* infrastructure dependency;
* documentation dependency.

Release Planning should identify dependencies early enough for readiness evaluation.

---

# Dependency Categories

Dependencies may be classified as:

```text
build dependency
runtime dependency
release dependency
compatibility dependency
publication dependency
operational dependency
```

These categories may require different release controls.

---

# Release Dependency Example

A plugin release may require:

```text
Plugin:
Finance 3.0.0

Requires:
FamilyOS >= 5.0.0

Compliance Framework:
compatible

Plugin API:
v2
```

This dependency context must be known before stable publication.

---

# Dependency Risk

Mutable or externally controlled dependencies introduce release risk.

Planning should identify dependencies that may change between:

```text
planning
build
candidate creation
publication
```

Where possible, release inputs should be locked or recorded.

---

# Compatibility Planning

Release Planning must identify compatibility concerns relevant to the scope.

Compatibility may include:

```text
platform ↔ plugin
plugin ↔ plugin
CLI ↔ API
schema ↔ data
configuration ↔ runtime
specification ↔ implementation
```

If compatibility is affected, the release plan should identify required validation and communication.

---

# Breaking Change Planning

Known breaking changes must be explicitly identified during planning.

They may require:

* major version increment;
* migration documentation;
* compatibility notes;
* additional validation;
* stronger approval;
* extended support planning.

Breaking changes must not be discovered only during final publication.

---

# Validation Planning

Planning should identify which validation applies.

Possible validation domains include:

```text
build
unit tests
integration tests
system tests
quality
security
compliance
documentation
compatibility
installation
upgrade
rollback
```

The release plan does not execute all validation.

It defines what must eventually be satisfied.

---

# Validation Scope

Validation should be proportional to release scope and risk.

Example:

```text
Documentation Release
→ structure validation
→ Markdown validation
→ reference validation
→ documentation governance
```

versus:

```text
Platform Release
→ build
→ tests
→ integration
→ quality
→ security
→ compliance
→ compatibility
→ installation
→ migration
```

---

# Evidence Planning

Planning should identify the evidence expected before approval.

Examples include:

* test reports;
* build results;
* quality reports;
* compliance reports;
* artifact checksums;
* documentation validation;
* repository state verification;
* approval records.

Evidence requirements should not be invented after release execution has already begun.

---

# Documentation Planning

Release documentation must be planned as part of the release.

Depending on release type, required documentation may include:

* changelog;
* release notes;
* migration guide;
* upgrade instructions;
* compatibility notes;
* known issues;
* security advisory;
* rollback guidance;
* framework validation documents.

Documentation readiness is part of release readiness.

---

# Changelog Planning

The release plan should determine:

* which changes belong to the release;
* which changelog section receives them;
* whether change categories are complete;
* whether previous unreleased entries must be consolidated.

The changelog should reflect the actual release scope.

---

# Release Notes Planning

Release notes should begin before final publication.

They may remain provisional during planning.

Final release notes must reflect the actual validated candidate.

Planning should identify whether release notes must include:

* major features;
* fixes;
* breaking changes;
* migration information;
* compatibility;
* known limitations;
* security information.

---

# Publication Planning

The release plan should identify expected publication targets.

Possible targets include:

```text
Git repository tag
Git hosting release
package registry
plugin registry
documentation hosting
artifact registry
container registry
```

Not every release requires every target.

---

# Publication Target Ownership

Each publication target should have defined ownership.

For example:

```text
Git tag
→ repository release authority

Package registry
→ package publication authority

Documentation hosting
→ documentation publication authority
```

A release plan should expose missing ownership before publication begins.

---

# Publication Ordering

Where multiple targets exist, planning should define expected ordering.

Example:

```text
validate candidate
      ↓
create release tag
      ↓
publish repository release
      ↓
publish artifacts
      ↓
verify artifacts
      ↓
promote stable channel
```

Publication order should minimize unsafe partial states.

---

# Distribution Planning

Where publication and distribution are separate, planning should identify:

* target audience;
* target channel;
* rollout scope;
* promotion criteria;
* timing constraints;
* post-promotion verification.

Future platform releases may use staged distribution.

---

# Release Timing

Release Planning may identify intended release timing.

Timing may include:

* milestone;
* release window;
* coordination date;
* maintenance window;
* security disclosure time;
* dependency availability.

Timing must not weaken validation requirements.

---

# Release Freeze

Some releases may require a release freeze.

A freeze limits changes after a defined point.

Possible freeze stages include:

```text
scope freeze
feature freeze
candidate freeze
documentation freeze
```

Freeze policies should be proportional to release complexity.

---

# Candidate Planning

Release Planning should determine how candidate identity will be created.

For example:

```text
target:
4.8.0

candidate sequence:
4.8.0-rc.1
4.8.0-rc.2
...
```

Candidate strategy should be known before final qualification begins.

---

# Artifact Planning

The expected artifact set should be defined.

For example:

```text
Release Artifact Set
├── source archive
├── Python package
├── plugin package
├── release manifest
└── documentation archive
```

Planning should identify which artifacts are authoritative.

---

# Artifact Reuse Strategy

The release plan should determine whether candidate artifacts will be promoted unchanged to stable.

The preferred strategy is:

```text
build once
validate
promote
```

Where rebuilding is necessary, the plan must identify renewed validation requirements.

---

# Provenance Planning

Planning should identify required provenance depth.

At minimum:

```text
source revision
build identity
artifact identity
```

More mature releases may require:

* checksums;
* dependency manifests;
* SBOM;
* signatures;
* attestations.

---

# Security Planning

Release security considerations must be identified during planning.

Examples include:

* sensitive release credentials;
* restricted vulnerability information;
* tag protection;
* publication permissions;
* artifact integrity;
* supply-chain risks;
* dependency integrity.

Security must not be introduced only at final publication.

---

# Credential Planning

If release publication requires credentials, planning should determine:

* which credentials are needed;
* who or what uses them;
* required scope;
* storage mechanism;
* environment;
* expiration where applicable.

Credentials should follow least-privilege principles.

---

# Governance Planning

Planning must identify governance requirements.

Questions include:

```text
Who owns the release?

Who validates readiness?

Who approves?

Who may publish?

Who may accept risk?

Who may approve exceptions?
```

These roles may overlap for small release profiles.

Their responsibilities must still remain explicit.

---

# Release Owner

Every significant release SHOULD have a release owner.

The Release Owner coordinates the release process.

Responsibilities may include:

* maintaining scope;
* coordinating validation;
* tracking blockers;
* ensuring documentation readiness;
* coordinating approval;
* confirming final completion.

Release ownership does not necessarily grant publication authority.

---

# Technical Owners

Components involved in a release may have technical owners responsible for validating domain-specific concerns.

Examples include:

* plugin owner;
* security owner;
* documentation owner;
* platform owner.

Planning should identify required ownership early.

---

# Approval Planning

Planning should determine which approvals may be required.

Examples:

```text
maintainer approval
security approval
platform approval
risk approval
emergency approval
```

Approval requirements should not be discovered only after a candidate is ready to publish.

---

# Exception Planning

Known required exceptions should be identified as early as possible.

An exception may involve:

* skipped non-critical check;
* temporary compatibility limitation;
* missing optional automation;
* emergency process variation.

Planning must not assume an exception will automatically be approved.

---

# Risk Planning

Release Planning must identify known risks.

Risk areas may include:

```text
technical
compatibility
security
operational
publication
dependency
migration
recovery
governance
```

Risks should be evaluated before readiness.

---

# Risk Record

A release risk record may include:

```text
risk
likelihood
impact
mitigation
owner
status
```

The exact representation may evolve.

---

# High-Risk Release Indicators

Indicators may include:

* breaking changes;
* major version transition;
* data migration;
* critical security change;
* new publication infrastructure;
* dependency replacement;
* large plugin compatibility impact;
* irreversible operational change.

High-risk releases should receive stronger planning and validation.

---

# Recovery Planning

Recovery must be considered before publication.

Planning should answer:

```text
Can this release be rolled back?

If yes, to what version?

What state must be restored?

If rollback is unsafe, what is the forward-recovery strategy?

How is a defective release withdrawn?

How are consumers informed?
```

---

# Rollback Feasibility

Rollback feasibility should be explicitly classified.

Example:

```text
rollback:
supported
```

or:

```text
rollback:
not safe

recovery:
forward fix required
```

This prevents false assumptions during incidents.

---

# Post-Release Planning

A release may require post-release actions.

Examples include:

* publication verification;
* smoke tests;
* monitoring;
* compatibility validation;
* support communication;
* issue tracking;
* stability observation.

These activities must be included before release completion is declared.

---

# Release Communication Planning

Significant releases may require communication to:

* maintainers;
* plugin developers;
* users;
* administrators;
* security stakeholders.

Planning should identify the appropriate audience and communication artifacts.

---

# Planning for Known Issues

Known non-blocking issues should be identified before publication.

The release plan should determine:

* whether the issue is acceptable;
* whether approval is required;
* whether it must appear in release notes;
* whether it affects support;
* whether follow-up work is required.

Known issues must not remain hidden simply because they do not block publication.

---

# Planning for Deprecation

If a release deprecates functionality, planning should include:

* deprecation scope;
* replacement;
* migration guidance;
* expected removal timeline;
* compatibility implications.

Deprecation is part of release communication and lifecycle management.

---

# Planning for Removal

Removing previously supported behavior requires stronger planning.

The plan should consider:

* version impact;
* migration;
* consumers;
* plugin compatibility;
* documentation;
* support implications.

Removal should normally be treated as compatibility-impacting.

---

# Release Planning Record

A future machine-readable release plan may contain:

```text
release:
  subject: Release Framework
  type: framework
  target_version: 4.8.0
  channel: stable

scope:
  - docs/epics/EPIC-REL-001-release-framework

validation:
  documentation: required
  repository: required

publication:
  git_tag: required

risk:
  level: low
```

The format is illustrative rather than normative.

---

# Minimum Planning Record

At minimum, a release plan should identify:

```text
subject
scope
release type
version intent
target channel if applicable
required validation
publication targets
known risks
recovery strategy
```

---

# Planning Checklist

Before progressing from `PLANNED` toward `PREPARED`, the following questions should be answerable.

```text
What is being released?

Why is it being released?

Which files or components are in scope?

Which release type applies?

Which version is intended?

Which channel is targeted?

Which dependencies matter?

Which validation is required?

Which documentation is required?

Who owns the release?

Who may approve it?

Where will it be published?

What are the major risks?

How will recovery work?
```

---

# Entry Criteria for Planning

Release Planning may begin when:

* a release intent exists;
* a meaningful change set exists or is expected;
* a milestone exists;
* maintenance or emergency need exists.

A fully completed implementation is not required to begin planning.

---

# Exit Criteria for Planning

Planning is sufficiently complete when the release can transition toward `PREPARED`.

At minimum:

* scope is understood;
* release type is selected;
* version intent exists;
* dependencies are known;
* expected validation is known;
* documentation expectations are known;
* publication targets are known;
* major risk is identified;
* recovery has been considered.

---

# Planning Reassessment

Planning must be revisited when material assumptions change.

Triggers include:

```text
scope change
version change
release type change
new breaking change
dependency change
security finding
publication target change
risk increase
```

A release plan is a controlled artifact, not a static assumption.

---

# Planning and Change Control

Once a release reaches advanced qualification stages, changes to the release plan become increasingly sensitive.

Conceptually:

```text
PLANNED
high flexibility

PREPARED
moderate flexibility

CANDIDATE
limited flexibility

VALIDATED
very limited flexibility

APPROVED
changes normally invalidate approval
```

This creates progressive release stabilization.

---

# Planning and Release Freeze

A release freeze represents a point where certain changes are no longer accepted without explicit requalification.

For example:

```text
candidate created
      ↓
scope frozen
      ↓
only release-blocking fixes accepted
```

Any accepted fix produces renewed candidate validation.

---

# Planning and Automation

Release Planning should remain human-readable even when automation is introduced.

Automation MAY assist by:

* detecting changed components;
* recommending release type;
* calculating version candidates;
* identifying dependencies;
* generating planning templates;
* identifying required policies.

Automation should not hide release intent.

---

# Planning and CI/CD

CI/CD may consume release planning metadata to determine:

* required jobs;
* target environments;
* release profile;
* validation matrix;
* publication targets.

CI/CD should implement the plan rather than become the only place where the plan exists.

---

# Planning and Governance

Release Governance defines who may approve or modify protected aspects of the plan.

Examples include:

* major version changes;
* emergency classification;
* security release classification;
* risk acceptance;
* exception use;
* target stable channel.

---

# Planning and Compliance

Compliance evaluation may eventually verify that required planning fields exist.

Examples:

```text
release scope defined         PASS
release type defined          PASS
version intent defined        PASS
recovery strategy defined     PASS
publication targets defined   PASS
```

Planning completeness may itself become a release gate.

---

# Planning Invariants

The following invariants apply.

## RP1 — Every significant release has explicit intent.

## RP2 — Release scope is known before formal qualification.

## RP3 — Release type is identified.

## RP4 — Version intent exists before candidate finalization.

## RP5 — Required validation is identified before readiness evaluation.

## RP6 — Applicable dependencies are known.

## RP7 — Major compatibility impact is identified.

## RP8 — Required documentation is planned.

## RP9 — Publication targets are known before publication.

## RP10 — Significant release risks are identified.

## RP11 — Recovery is considered before release.

## RP12 — Material scope change triggers planning reassessment.

---

# Planning Anti-Patterns

## Release by Momentum

Publishing simply because development work appears finished.

---

## Undefined Scope

Allowing unrelated changes to enter the release candidate without review.

---

## Version Last-Minute Guessing

Choosing the version immediately before tagging.

---

## Validation Discovery

Discovering required tests only after the release candidate is created.

---

## Publication Discovery

Determining publication targets during release execution.

---

## No Recovery Plan

Assuming a defective release can always be reverted later.

---

## Documentation After Release

Treating release notes and migration guidance as optional post-release work.

---

## Hidden Dependencies

Depending on components whose versions or state are not recorded.

---

## Unowned Release

Beginning release execution without clear responsibility.

---

# Current FamilyOS Framework Planning Mapping

The current Release Framework work itself can be mapped to Release Planning.

```text
Subject:
EPIC-REL-001 — Release Framework

Type:
framework

Scope:
docs/epics/EPIC-REL-001-release-framework/

Target:
stable framework milestone

Previous milestone:
v4.7.0-build-framework

Version intent:
4.8.0

Potential tag:
v4.8.0-release-framework
```

The final version and tag remain subject to final repository validation.

---

# Current Scope Model

For EPIC-REL-001, the canonical numbered scope is:

```text
00-EPIC.md
01-Context.md
02-Vision.md
03-Release-Principles.md
04-Release-Architecture.md
05-Release-Lifecycle.md
06-Versioning-Strategy.md
07-Release-Types-and-Channels.md
08-Release-Planning.md
09-Release-Readiness.md
10-Release-Candidates.md
11-Artifacts-and-Provenance.md
12-Release-Validation.md
13-Release-Automation.md
14-CI-CD-Integration.md
15-Changelog-and-Release-Notes.md
16-Tagging-and-Repository-State.md
17-Publishing-and-Distribution.md
18-Rollback-and-Recovery.md
19-Release-Security.md
20-Release-Observability.md
21-Release-Governance.md
22-Release-Compliance.md
23-Release-Metrics.md
24-Release-Risk-Management.md
25-Framework-Lifecycle.md
26-Roadmap.md
27-References.md
28-Validation.md
29-Summary.md
30-Release.md
31-Implementation-Checklist.md
```

Control documents complete the release framework package.

---

# Target Planning Experience

At higher maturity, a FamilyOS maintainer should be able to initiate planning and receive a structured view such as:

```text
Release Plan

Subject               Release Framework
Type                  Framework
Current Version       4.7.0
Target Version        4.8.0
Target Channel        Stable
Scope                 Defined
Dependencies          Known
Validation Profile    Framework Release
Documentation         Required
Publication           Git Tag + Repository
Risk                  Assessed
Recovery              Defined

PLAN READY
```

This reduces reliance on individual memory.

---

# Relationship With Release Readiness

Release Planning defines what must be true.

Release Readiness determines whether it is true.

The relationship is:

```text
Planning
"What do we require?"

      ↓

Readiness
"Have we satisfied it?"
```

The next document, `09-Release-Readiness.md`, defines this evaluation model.

---

# Relationship With Release Candidates

Planning determines the intended candidate strategy.

Candidate creation freezes the exact object that will be validated.

---

# Relationship With Release Risk Management

Planning identifies risk.

`24-Release-Risk-Management.md` defines how risk is classified, evaluated, mitigated, accepted, and monitored.

---

# Relationship With Governance

Planning identifies required authority.

`21-Release-Governance.md` defines who possesses that authority and how decisions are recorded.

---

# Relationship With Publishing

Planning defines intended publication.

`17-Publishing-and-Distribution.md` governs how that publication is executed and verified.

---

# Final Statement

The FamilyOS Release Planning model ensures that releases begin as deliberate engineering activities rather than terminal procedures.

By defining release intent, scope, type, version, dependencies, compatibility, validation, documentation, governance, publication, risk, and recovery before qualification begins, FamilyOS creates the conditions required for predictable and auditable release execution.

Release Planning establishes what the release is supposed to become.

Release Readiness then determines whether the engineering state is sufficient to proceed.
