# Release Framework

# 03 Release Principles

## Overview

EPIC-REL-001 — Release Framework defines a set of release engineering principles that govern how FamilyOS prepares, qualifies, approves, versions, tags, publishes, distributes, observes, and recovers releases.

These principles are intentionally independent from specific automation tools, repository providers, package registries, CI/CD systems, or deployment technologies.

They define the behavioral foundation of the FamilyOS release model.

Any release implementation, workflow, policy, automation, or future release orchestration capability must remain consistent with these principles.

---

# Purpose

The purpose of the Release Principles is to establish durable engineering rules that prevent release behavior from becoming dependent on:

* individual maintainer habits;
* terminal command history;
* undocumented scripts;
* provider-specific assumptions;
* manual memory;
* ad hoc version decisions;
* accidental repository state;
* implicit approval;
* partial publication without recovery;
* opaque automation.

The principles provide a stable reference against which release architecture and implementation decisions can be evaluated.

---

# Principle Model

The FamilyOS Release Framework distinguishes between:

```text
principle
requirement
policy
mechanism
implementation
```

A principle defines a durable engineering truth.

A requirement translates a principle into a specific obligation.

A policy determines how the obligation is governed in a particular context.

A mechanism provides the technical capability required to implement the policy.

An implementation selects concrete tools and technologies.

The intended relationship is:

```text
Release Principle
      ↓
Normative Requirement
      ↓
Release Policy
      ↓
Release Mechanism
      ↓
Technical Implementation
```

Tools may change.

The principles must remain stable unless the Release Framework itself is intentionally revised.

---

# P1 — A Build Is Not a Release

A successful build MUST NOT automatically be interpreted as an official release.

A build establishes that artifacts were produced.

A release establishes that artifacts were qualified and transitioned into an official release state.

The distinction is:

```text
BUILD
  ↓
artifact exists

RELEASE
  ↓
artifact is officially qualified and published
```

A release may require evidence not provided by the build process, including:

* release readiness;
* validation;
* approval;
* version assignment;
* documentation readiness;
* tagging;
* publication verification;
* release governance.

Release automation MUST preserve this distinction.

---

# P2 — Every Official Release Must Have an Explicit Identity

Every official FamilyOS release MUST have an unambiguous release identity.

A release identity must allow humans and systems to determine exactly which release is being referenced.

The release identity may include:

* version;
* release type;
* release channel;
* component identity;
* candidate identifier;
* repository tag.

The same official release identity MUST NOT intentionally refer to materially different release contents.

---

# P3 — Every Release Must Be Traceable to Source

An official release MUST be traceable to the controlled source state from which it originated.

At minimum, this normally requires an identifiable source revision.

For Git-based FamilyOS components, this typically means a commit identity.

The traceability chain should support:

```text
Release
   ↓
Release Version
   ↓
Release Tag
   ↓
Source Revision
```

Where appropriate, traceability should extend further to:

```text
Source Revision
   ↓
Build
   ↓
Artifacts
   ↓
Validation
   ↓
Release
```

A release whose source cannot be reasonably identified MUST NOT be considered fully trustworthy.

---

# P4 — Release Validation Must Apply to the Actual Candidate

Validation evidence MUST correspond to the actual release candidate intended for publication.

A candidate that changes materially after validation MUST be considered changed.

The existing evidence must then be reassessed.

Depending on the type of change, the candidate may require:

* a new candidate identity;
* partial revalidation;
* full revalidation;
* renewed approval.

The framework MUST prevent the following invalid assumption:

```text
validated object A
        =
published object B
```

unless A and B are demonstrably equivalent under the applicable release rules.

---

# P5 — Release Readiness Must Be Evidence-Based

Release readiness MUST be based on explicit evidence.

A release MUST NOT be considered ready solely because:

* development appears complete;
* a maintainer believes it is ready;
* tests passed at some unrelated earlier state;
* an artifact exists;
* a tag can be created.

Applicable evidence may include:

```text
build evidence
test evidence
quality evidence
compliance evidence
security evidence
documentation evidence
artifact evidence
repository evidence
risk evidence
```

The required evidence depends on release type and risk.

---

# P6 — Release Promotion Must Be Explicit

Movement between release states MUST be deliberate.

The release model must avoid implicit transitions.

For example, the existence of a tag should not automatically mean that all prior release qualification stages were satisfied unless the release architecture explicitly guarantees that relationship.

A canonical progression may be:

```text
prepared
   ↓
candidate
   ↓
validated
   ↓
approved
   ↓
released
   ↓
published
```

State transitions must have defined entry criteria where relevant.

---

# P7 — Published Release Artifacts Must Be Immutable

An artifact officially published under a release identity SHOULD be treated as immutable.

The preferred correction model is:

```text
published release
      ↓
problem discovered
      ↓
withdraw / supersede if necessary
      ↓
new corrected release
```

Silent replacement under the same identity creates ambiguity and damages release trust.

If a distribution system technically permits artifact replacement, FamilyOS release policy SHOULD prohibit such replacement for official immutable release identities except under exceptional governed conditions.

---

# P8 — Version Meaning Must Be Stable

Versions MUST follow consistent semantics.

The meaning of a version increment must not change arbitrarily between releases.

For example, if semantic versioning is adopted for a release domain, major, minor, and patch increments must have defined interpretation.

The framework MUST prevent version identifiers from becoming merely chronological labels with no stable meaning unless the applicable versioning strategy intentionally defines them that way.

---

# P9 — Release Tags Must Be Stable Anchors

Official release tags MUST identify a specific repository state.

Once an official release has been published, its tag SHOULD NOT be moved.

A tag associated with an official release must not be casually deleted and recreated against another commit.

The intended relationship is:

```text
Release Version
      ↕
Release Tag
      ↕
Source Revision
```

This relationship is fundamental to historical release reconstruction.

---

# P10 — Repository State Must Be Verified Before Release

The repository state relevant to a release MUST be verified before final release operations.

Applicable checks may include:

* expected branch;
* expected HEAD;
* clean working tree;
* expected upstream state;
* commit availability on the authoritative remote;
* tag uniqueness;
* version consistency.

Not every release type requires identical repository rules.

However, repository assumptions MUST NOT remain implicit.

---

# P11 — Release Automation Must Be Deterministic Where Practical

Repeatable release operations SHOULD produce consistent behavior when given equivalent controlled inputs.

Automation SHOULD minimize dependence on:

* local machine state;
* hidden environment variables;
* undocumented operator actions;
* uncontrolled timestamps;
* transient mutable dependencies;
* workstation-specific configuration.

Where nondeterminism cannot be eliminated, it SHOULD be observable and documented.

---

# P12 — Release Automation Must Fail Safely

Release automation MUST treat failure as a first-class state.

A failed workflow MUST NOT incorrectly report release success.

Automation should preserve enough state to determine:

* which steps completed;
* which steps failed;
* which external systems were modified;
* whether publication partially occurred;
* what recovery is required.

The system must avoid ambiguous states such as:

```text
some release operations completed
+
unknown final release state
```

---

# P13 — Automation Must Not Override Governance

Automation executes release policy.

Automation does not define release authority.

A pipeline MUST NOT bypass:

* mandatory approvals;
* required release gates;
* security boundaries;
* exception policies;
* risk acceptance requirements.

The fact that a task can be automated does not imply that it should execute without authorization.

---

# P14 — Manual Steps Must Be Governed

Manual release operations MAY remain part of the release process.

When they exist, they should be:

* documented;
* ordered;
* reviewable;
* repeatable;
* observable;
* associated with explicit authority.

Manual work is not inherently non-compliant.

Undocumented manual dependency is the problem.

---

# P15 — Release Authority Must Be Explicit

The framework MUST define who or what has authority to perform sensitive release actions.

These actions may include:

* approving release readiness;
* approving release risk;
* assigning final version;
* creating official tags;
* publishing artifacts;
* promoting channels;
* withdrawing releases;
* authorizing emergency releases;
* accepting exceptions.

Authority must be governed rather than assumed.

---

# P16 — Least Privilege Applies to Release Systems

Release automation and maintainers SHOULD receive only the permissions necessary for their responsibilities.

A system capable only of validating release readiness should not automatically require publication authority.

Where possible, sensitive release capabilities should be separated.

Conceptually:

```text
validate permission
approve permission
tag permission
publish permission
withdraw permission
```

may represent separate responsibilities.

---

# P17 — Release Credentials Must Be Protected

Release credentials MUST NOT be embedded directly in:

* source code;
* committed scripts;
* documentation;
* release notes;
* repository configuration intended for public distribution.

Credentials should use appropriate secure storage and access mechanisms.

Release credentials should be:

* scoped;
* protected;
* rotatable;
* auditable where practical.

---

# P18 — Release Security Is End-to-End

Security MUST be considered across the complete release path.

Security does not begin only when artifacts are uploaded.

The protected chain includes:

```text
source
  ↓
build
  ↓
candidate
  ↓
validation
  ↓
tag
  ↓
publication
  ↓
distribution
```

Weak integrity guarantees at any stage may compromise the final release.

---

# P19 — Release Evidence Must Be Durable

Critical release evidence SHOULD survive beyond an individual CI job or terminal session.

Examples include:

* release identity;
* source revision;
* candidate identity;
* artifact inventory;
* validation status;
* approvals;
* release tag;
* publication status;
* release notes;
* exceptions.

The precise storage mechanism may evolve.

The evidence must remain available for the period required by FamilyOS governance.

---

# P20 — Historical Releases Must Be Reconstructable

FamilyOS SHOULD preserve enough release information to reconstruct significant historical releases.

A maintainer should be able to determine, where applicable:

```text
what was released
which version it had
which commit produced it
which artifacts belonged to it
which tag represented it
what validation passed
what changed
when it was published
whether it was superseded
```

Historical reconstruction supports:

* maintenance;
* debugging;
* security investigation;
* compliance;
* compatibility analysis;
* recovery.

---

# P21 — Release Documentation Is Part of Release Readiness

Required release documentation MUST be prepared before a release is considered complete.

Depending on the release type, documentation may include:

* changelog;
* release notes;
* migration information;
* compatibility information;
* known limitations;
* security information;
* recovery guidance.

Documentation SHOULD describe the actual final candidate.

It must not describe only an earlier planned release state.

---

# P22 — Changelog and Release Notes Serve Different Purposes

The Release Framework MUST distinguish between changelog information and release notes.

A changelog is primarily a structured historical record.

Release notes are primarily release-specific communication.

The two may share source data.

They must not be treated as interchangeable concepts.

---

# P23 — Release Risk Must Influence Release Controls

Release controls SHOULD be proportional to release risk.

A low-risk documentation correction should not necessarily require the same process as a major security-sensitive platform release.

Risk-based variation may affect:

* validation depth;
* approval level;
* release evidence;
* rollout strategy;
* rollback expectations;
* observation period.

Core release invariants must still remain satisfied.

---

# P24 — Exceptions Must Be Explicit

A mandatory release rule MAY only be bypassed through an explicitly governed exception when the applicable policy permits it.

An exception should record:

* requirement being bypassed;
* justification;
* risk;
* approving authority;
* compensating controls;
* scope;
* expiration where relevant.

Silent exceptions are prohibited.

---

# P25 — Emergency Releases Must Remain Controlled

Emergency releases MAY use an accelerated lifecycle.

They MUST NOT become uncontrolled releases.

Minimum controls should continue to include:

* identity;
* source traceability;
* authorization;
* appropriate validation;
* versioning;
* documentation;
* publication verification;
* recovery planning.

Emergency release processes should be defined before emergencies occur.

---

# P26 — Publication Must Be Verifiable

A release workflow MUST distinguish between attempted publication and verified publication.

For example:

```text
upload command succeeded
```

does not automatically prove:

```text
release is correctly and fully available
```

Post-publication verification SHOULD confirm relevant release state.

---

# P27 — Partial Publication Must Be Detectable

When release publication spans multiple systems, partial failure must be expected.

The framework SHOULD make it possible to identify states such as:

```text
tag created
artifact published
release metadata missing
```

or:

```text
artifact published
distribution failed
```

Partial publication MUST NOT be silently reported as full success.

---

# P28 — Recovery Is Part of Release Design

Rollback and recovery MUST NOT be designed only after release failures occur.

Every significant release class SHOULD define an appropriate recovery strategy.

Possible strategies include:

* rollback;
* withdrawal;
* supersession;
* channel demotion;
* republishing;
* corrective release;
* forward recovery.

The appropriate strategy depends on release characteristics.

---

# P29 — Rollback Must Not Be Assumed Safe

The existence of an older version does not automatically make rollback safe.

Rollback feasibility may depend on:

* schema compatibility;
* persistent data;
* external side effects;
* protocol compatibility;
* configuration changes;
* dependency transitions.

Release planning should explicitly determine whether rollback is valid.

---

# P30 — Forward Recovery Is a First-Class Strategy

When rollback is unsafe or impossible, the framework MUST support forward recovery.

A corrective release with a new identity may be safer than attempting to restore a previous state.

Forward recovery must remain governed and traceable.

---

# P31 — Release State Must Be Observable

The release system SHOULD expose clear information about current release state.

Operators and automation should be able to distinguish:

```text
planned
prepared
candidate
validated
approved
published
failed
withdrawn
superseded
```

The exact canonical state model is defined elsewhere in the framework.

The principle is that release state must not depend on interpretation of unrelated system side effects.

---

# P32 — Release Failures Must Be Diagnosable

A failed release operation SHOULD provide sufficient diagnostic information to determine:

* failed stage;
* candidate involved;
* source state;
* artifacts involved;
* external operations already completed;
* applicable error;
* recommended recovery entry point.

Failure messages that only indicate generic failure without state information are insufficient for mature release engineering.

---

# P33 — Release Metrics Must Support Improvement

FamilyOS MAY measure release performance and reliability.

Metrics should support engineering improvement.

They MUST NOT encourage unsafe behavior merely to improve numerical targets.

For example, maximizing release frequency must not incentivize bypassing validation.

Relevant metrics may include:

* release success rate;
* release lead time;
* candidate rejection rate;
* rollback rate;
* publication failure rate;
* recovery time;
* evidence completeness;
* automation coverage.

---

# P34 — Release Profiles Must Extend Common Semantics

Different release types may use different release profiles.

Possible profiles include:

* framework release;
* documentation release;
* plugin release;
* platform release;
* security release;
* emergency release.

Profiles MAY add requirements.

They MUST NOT redefine fundamental release concepts inconsistently.

---

# P35 — Platform and Component Releases Must Remain Distinguishable

FamilyOS may contain both platform-level and component-level releases.

A component release MUST NOT automatically imply a full platform release.

Similarly, a platform release may aggregate multiple component states.

The relationship between them must remain explicit.

---

# P36 — Compatibility Must Be Considered Before Release

Where compatibility matters, release readiness MUST evaluate it.

Compatibility considerations may include:

```text
platform ↔ plugin
plugin ↔ dependency
API ↔ consumer
schema ↔ data
specification ↔ implementation
```

A release known to introduce compatibility changes must communicate those changes clearly.

---

# P37 — Release Channels Must Have Clear Semantics

If FamilyOS uses release channels, every channel MUST have a defined purpose.

A channel should communicate expectations such as:

* stability;
* intended audience;
* support level;
* promotion status.

Channels must not create ambiguity around the meaning of versions.

---

# P38 — Promotion Must Not Rebuild Without Explicit Reason

Where practical, a release candidate should be promoted using the same validated artifacts.

The preferred model is:

```text
build once
validate
promote same artifacts
```

rather than:

```text
build
validate
rebuild different artifacts
publish
```

If rebuilding is required, the new artifacts must receive appropriate validation and provenance treatment.

---

# P39 — Release Artifacts Must Be Identifiable

Release artifacts SHOULD have sufficient metadata to determine:

* what they are;
* which release they belong to;
* which version they represent;
* where they originated;
* whether they are the intended artifacts.

Artifact identity must remain distinct from simple filename coincidence.

---

# P40 — Provenance Should Strengthen Over Time

FamilyOS SHOULD progressively improve release provenance.

Possible maturity stages include:

```text
source revision
    ↓
build metadata
    ↓
checksums
    ↓
dependency metadata
    ↓
SBOM
    ↓
signatures
    ↓
attestations
```

The Release Framework should permit stronger provenance mechanisms without breaking earlier release semantics.

---

# P41 — Tooling Must Implement the Framework

Release tooling exists to implement release rules.

Tool behavior SHOULD be derived from the documented framework.

The framework MUST NOT become merely documentation describing whatever a script currently happens to do.

This principle protects architectural authority.

---

# P42 — Release Semantics Must Be Tool-Independent

FamilyOS release concepts MUST NOT depend fundamentally on a specific vendor.

Concepts such as:

* release;
* candidate;
* version;
* approval;
* publication;
* withdrawal;
* release evidence;

must remain meaningful independently of GitHub, GitLab, CI/CD providers, registries, or hosting systems.

---

# P43 — Policy Should Become Machine-Evaluable Where Practical

Objective release rules SHOULD become automatable where practical.

Examples include:

```text
working_tree_clean == true
tests_passed == true
version_valid == true
tag_unique == true
required_docs_present == true
```

Machine evaluation should reduce repetitive manual verification.

Human-readable policy must remain authoritative and understandable.

---

# P44 — Human Judgment Must Remain Visible

When release decisions depend on judgment, that judgment SHOULD be explicit.

Examples include:

* risk acceptance;
* known defect acceptance;
* emergency authorization;
* compatibility exception;
* release timing decision.

Automation should not silently convert judgment into hidden defaults.

---

# P45 — Release Workflows Must Be Idempotent Where Possible

Where technically practical, retrying a release operation should not produce unintended duplicate or contradictory state.

For example, tooling should safely detect whether:

* a tag already exists;
* an artifact was already uploaded;
* a release object already exists;
* metadata was already recorded.

Idempotency reduces recovery risk after interrupted workflows.

---

# P46 — External Side Effects Must Be Deliberate

Release operations that modify external systems SHOULD occur only after applicable local and candidate validation has passed.

Examples of external side effects include:

* pushing tags;
* publishing artifacts;
* creating registry versions;
* updating stable channels;
* distributing packages.

The framework should perform low-risk validation before high-impact side effects whenever possible.

---

# P47 — Release Completion Must Be Explicit

A release is not complete merely because its primary artifact was published.

Completion criteria should consider applicable finalization steps, including:

* publication verification;
* release notes publication;
* evidence recording;
* distribution verification;
* final repository state;
* post-release checks.

The framework must provide a clear definition of release completion.

---

# P48 — Release History Must Not Be Rewritten Casually

Published historical release records SHOULD remain stable.

Corrections to historical metadata should preserve an audit trail where appropriate.

The framework should favor:

```text
supersede
correct
annotate
```

over:

```text
erase
silently rewrite
```

This principle protects long-term trust.

---

# P49 — Framework Rules Must Be Internally Consistent

The Release Framework itself must avoid contradictory requirements.

When documents overlap, responsibility must be clear.

For example:

* version rules belong primarily to Versioning Strategy;
* candidate rules belong primarily to Release Candidates;
* state transitions belong primarily to Release Lifecycle;
* release authority belongs primarily to Release Governance.

Cross-references may summarize those rules but must not redefine them inconsistently.

---

# P50 — The Release Framework Must Govern Its Own Release

EPIC-REL-001 must eventually apply its own principles to its completion and publication.

The framework should therefore close through a controlled process including:

```text
documentation completion
      ↓
validation
      ↓
repository verification
      ↓
commit
      ↓
version assignment
      ↓
annotated release tag
      ↓
publication
      ↓
final verification
```

This establishes the Release Framework through the release discipline it defines.

---

# Principle Categories

The principles can be grouped into the following domains.

## Identity and Traceability

```text
P2
P3
P8
P9
P20
P39
P48
```

---

## Validation and Readiness

```text
P1
P4
P5
P6
P21
P36
P38
P47
```

---

## Governance

```text
P13
P14
P15
P23
P24
P25
P44
```

---

## Automation

```text
P11
P12
P26
P27
P41
P43
P45
P46
```

---

## Security and Integrity

```text
P7
P16
P17
P18
P40
```

---

## Recovery and Operations

```text
P28
P29
P30
P31
P32
```

---

## Ecosystem Evolution

```text
P34
P35
P37
P42
P49
P50
```

---

# Principle Evaluation Model

Release architecture decisions should be evaluated against these principles.

A proposed release mechanism should answer questions such as:

```text
Does it preserve release identity?

Does it preserve source traceability?

Does validation apply to the exact candidate?

Does it create external side effects safely?

Can partial failure be detected?

Can the workflow be recovered?

Does it respect governance?

Can the resulting release be reconstructed later?
```

If a mechanism repeatedly conflicts with the principles, the mechanism should be redesigned rather than weakening the framework without explicit architectural justification.

---

# Principle Precedence

Release principles define the general release engineering direction.

More specific documents in EPIC-REL-001 provide detailed rules.

Where a detailed requirement appears inconsistent with these principles, the inconsistency must be resolved explicitly through framework governance.

Implementation behavior MUST NOT silently override normative framework rules.

---

# Minimum Release Principle Set

Regardless of release type or profile, every official FamilyOS release must preserve the following minimum properties:

```text
IDENTITY
TRACEABILITY
VALIDATION
VERSION
CONTROLLED STATE
INTEGRITY
DOCUMENTATION
GOVERNANCE
OBSERVABILITY
RECOVERY
```

A release process that cannot provide these fundamental properties should be considered immature or incomplete.

---

# Anti-Patterns

The following practices conflict with the Release Principles.

## Tag-and-Hope

```text
work completed
git tag
git push
done
```

without explicit readiness and validation.

---

## Rebuild-after-Validation

Validating one artifact set and publishing a materially different rebuilt set without renewed qualification.

---

## Mutable Release Identity

Replacing published artifacts while keeping the same official version identity.

---

## Hidden Release Authority

Allowing an automation token or maintainer account to publish releases without explicit governance simply because the permission exists.

---

## Terminal-Memory Release

Depending on the operator remembering the correct sequence of commands.

---

## Partial-Success Blindness

Treating a multi-system release as successful when only some publication steps completed.

---

## Pipeline-as-Policy

Allowing CI/CD configuration to become the only definition of release behavior.

---

## Version Guessing

Selecting a release version manually without defined version semantics.

---

## Evidence-by-Assumption

Assuming validation exists because the project normally runs tests.

---

## Rollback Assumption

Declaring a release recoverable without evaluating whether reversal is actually safe.

---

# Expected Engineering Effect

Applying these principles should progressively transform FamilyOS releases from operator-driven procedures into governed engineering workflows.

The transition is:

```text
Individual Knowledge
        ↓
Documented Process
        ↓
Standardized Rules
        ↓
Automated Validation
        ↓
Structured Evidence
        ↓
Controlled Publication
        ↓
Policy-Driven Release Engineering
```

The Release Framework should mature without losing transparency.

---

# Principle Compliance

A FamilyOS release implementation is aligned with EPIC-REL-001 when it:

* preserves explicit release identity;
* maintains source and artifact traceability;
* validates the actual candidate;
* uses evidence-based readiness;
* applies controlled state transitions;
* protects published release immutability;
* follows defined version semantics;
* uses stable release anchors;
* verifies repository assumptions;
* handles automation failures safely;
* respects governance;
* protects release credentials;
* preserves release evidence;
* supports diagnosis and recovery;
* remains compatible with future framework evolution.

Partial implementation is acceptable during framework maturity progression.

Violations of core invariants must remain visible as implementation gaps rather than being silently normalized.

---

# Final Statement

The FamilyOS Release Principles establish the permanent behavioral foundation of release engineering.

They ensure that release maturity is not measured only by the amount of automation introduced.

A mature release system is one in which identity, traceability, validation, governance, integrity, publication, observability, and recovery remain coherent across the complete release lifecycle.

These principles provide the architectural constraints required for all subsequent EPIC-REL-001 documents and future FamilyOS release tooling.
