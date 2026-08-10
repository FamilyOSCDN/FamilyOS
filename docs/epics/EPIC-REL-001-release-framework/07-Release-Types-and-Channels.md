# Release Framework

# 07 Release Types and Channels

## Overview

EPIC-REL-001 — Release Framework defines a classification model for FamilyOS releases.

Not all releases have the same purpose, stability expectations, validation depth, audience, or operational risk.

The Release Types and Channels model provides a consistent way to distinguish:

* why a release exists;
* how mature it is;
* who should consume it;
* what level of validation is expected;
* how it may be promoted;
* how it should be documented;
* how it should be governed.

Release type and release channel are related but distinct concepts.

A release type describes the purpose and operational intent of a release.

A release channel describes the availability or stability path through which the release is exposed to consumers.

---

# Purpose

The Release Types and Channels model establishes:

* canonical release types;
* canonical release channels;
* type semantics;
* channel semantics;
* stability expectations;
* promotion rules;
* release profile implications;
* validation expectations;
* governance expectations;
* documentation expectations;
* compatibility expectations;
* emergency and security release treatment.

The model prevents release classifications from becoming informal or inconsistent across the FamilyOS ecosystem.

---

# Release Type vs Release Channel

Release type and release channel MUST NOT be treated as interchangeable.

For example:

```text id="ba4p3d"
Release Type:
security

Release Channel:
stable
```

or:

```text id="pl859e"
Release Type:
feature

Release Channel:
preview
```

The type explains the reason or category of the release.

The channel explains how the release is exposed and what stability expectation applies.

---

# Canonical Release Type Model

FamilyOS recognizes the following high-level release types:

```text id="i4l0qq"
development
preview
feature
maintenance
security
emergency
framework
plugin
platform
documentation
```

Some releases may belong to more than one descriptive category.

For governance and automation, one primary release type SHOULD be selected where practical.

Secondary attributes MAY provide additional context.

---

# Development Release

## Definition

A Development Release is intended for engineering validation, internal testing, or early integration.

Development releases may contain:

* incomplete functionality;
* experimental behavior;
* unstable interfaces;
* temporary instrumentation;
* incomplete documentation;
* unresolved known defects.

Development releases MUST NOT be represented as stable releases.

---

# Development Release Expectations

Typical expectations include:

```text id="mji96i"
stability                low
consumer scope           internal / engineering
validation depth         limited
compatibility guarantee  minimal
publication authority    restricted
support expectation      none or limited
```

Development releases may be frequent and highly automated.

---

# Development Release Versioning

Development releases may use pre-release identifiers or internal build metadata.

Examples:

```text id="n1u73o"
4.9.0-dev.1
4.9.0-alpha.1
4.9.0+build.241
```

The exact syntax must remain compatible with the Versioning Strategy.

---

# Preview Release

## Definition

A Preview Release is intended to expose upcoming FamilyOS functionality before stable release.

Preview releases may be used for:

* early consumer feedback;
* compatibility testing;
* integration testing;
* operational evaluation;
* ecosystem validation.

Preview releases provide stronger expectations than development releases but remain non-stable.

---

# Preview Release Expectations

A Preview Release SHOULD generally have:

* coherent release scope;
* identified version intent;
* basic release documentation;
* passing required core tests;
* known limitations documented;
* sufficient stability for controlled evaluation.

Preview releases SHOULD clearly communicate that compatibility may still change.

---

# Feature Release

## Definition

A Feature Release introduces meaningful backward-compatible functionality.

Feature releases normally correspond to a semantic minor version increment.

Example:

```text id="g8pj8n"
4.8.0
   ↓
4.9.0
```

Feature releases may include:

* new capabilities;
* new commands;
* new plugin features;
* new compatible APIs;
* new framework functionality;
* significant compatible platform expansion.

---

# Feature Release Expectations

A stable Feature Release should normally satisfy the complete applicable release lifecycle.

This includes:

* readiness;
* candidate validation;
* approval;
* versioning;
* tagging;
* publication;
* verification;
* documentation.

---

# Maintenance Release

## Definition

A Maintenance Release corrects or improves an existing supported release line without intentionally introducing major compatibility changes.

Maintenance releases commonly include:

* bug fixes;
* reliability corrections;
* small internal improvements;
* documentation corrections;
* packaging fixes;
* minor non-breaking maintenance.

They normally use a patch version increment.

Example:

```text id="c92cjr"
4.9.0
   ↓
4.9.1
```

---

# Maintenance Release Expectations

Maintenance releases may use a reduced release profile when risk is lower.

However, they must still preserve:

* identity;
* traceability;
* validation;
* version integrity;
* documentation;
* publication verification.

---

# Security Release

## Definition

A Security Release addresses one or more security concerns.

Security releases may be:

* planned;
* coordinated;
* confidential before publication;
* accelerated;
* backward-compatible;
* compatibility-impacting.

Security release type does not determine semantic version increment by itself.

The version increment depends on actual compatibility impact.

---

# Security Release Characteristics

Security releases may require:

* restricted preparation;
* limited information disclosure;
* stronger approval controls;
* coordinated publication;
* security-specific validation;
* advisory preparation;
* precise artifact provenance;
* post-publication monitoring.

---

# Security Release Disclosure

Security-sensitive information SHOULD remain appropriately restricted until the intended disclosure point.

The Release Framework must support release coordination without requiring premature public documentation.

---

# Emergency Release

## Definition

An Emergency Release is an accelerated release performed to address severe operational, security, integrity, or platform-impacting conditions.

Examples include:

* critical regression;
* severe production defect;
* high-impact security vulnerability;
* broken package release;
* invalid release artifact;
* release pipeline defect affecting consumers.

---

# Emergency Release Principle

The governing rule is:

> Emergency means accelerated, not uncontrolled.

Emergency releases MUST preserve minimum release invariants.

These include:

```text id="pdj3di"
identity
source traceability
appropriate validation
authorization
versioning
publication verification
recovery
```

---

# Emergency Release Process

An emergency profile may compress normal lifecycle stages.

For example:

```text id="qs21ot"
incident
  ↓
prepare correction
  ↓
focused readiness
  ↓
candidate
  ↓
minimum required validation
  ↓
emergency approval
  ↓
release
  ↓
publish
  ↓
verify
```

---

# Framework Release

## Definition

A Framework Release publishes a major FamilyOS engineering framework or framework revision.

Examples include:

```text id="bvgoqe"
Build Framework
Quality Framework
Release Framework
Testing Framework
Documentation Framework
Plugin Compliance Framework
```

Framework releases primarily publish architectural and governance documentation.

---

# Framework Release Characteristics

Framework releases typically require:

* complete canonical document structure;
* normative consistency;
* control document alignment;
* documentation validation;
* repository validation;
* clean Git state;
* commit;
* version assignment;
* annotated tag;
* remote publication;
* final repository verification.

---

# Current Framework Release Model

A FamilyOS framework release may currently follow:

```text id="o9ow3c"
framework documentation complete
        ↓
validation
        ↓
repository clean
        ↓
commit
        ↓
annotated version tag
        ↓
push branch
        ↓
push tag
        ↓
verify remote state
```

This is a valid release profile under EPIC-REL-001.

---

# Plugin Release

## Definition

A Plugin Release publishes an official FamilyOS plugin or plugin revision.

A plugin release may require:

* plugin tests;
* plugin compliance validation;
* capability validation;
* metadata validation;
* platform compatibility verification;
* plugin documentation;
* plugin versioning;
* plugin artifact publication.

---

# Plugin Release Identity

A plugin release may use independent component versioning.

Example:

```text id="22r4iu"
Finance Plugin 2.5.0
```

with compatibility metadata such as:

```text id="eobfi9"
requires FamilyOS >= 4.9.0
```

The precise compatibility contract may be governed by plugin specifications.

---

# Platform Release

## Definition

A Platform Release represents an integrated FamilyOS platform state.

A Platform Release may coordinate:

* core platform;
* CLI;
* official plugin compatibility;
* schemas;
* specifications;
* documentation;
* release metadata.

Platform releases typically carry the strongest ecosystem-wide release significance.

---

# Platform Release Expectations

Platform releases SHOULD normally use the complete stable release profile.

They may require:

* broader integration testing;
* compatibility verification;
* full release notes;
* migration guidance;
* security assessment;
* complete provenance;
* stronger governance approval.

---

# Documentation Release

## Definition

A Documentation Release publishes documentation changes as an official versioned release.

Documentation releases may include:

* framework updates;
* reference updates;
* specifications;
* architecture documentation;
* user documentation;
* migration guidance.

A documentation release may use a lightweight profile when no executable artifacts are involved.

---

# Documentation Release Requirements

Documentation-only status does not eliminate release discipline.

A Documentation Release still requires:

* explicit version identity where officially released;
* source traceability;
* validation;
* documentation quality checks;
* repository state verification;
* publication verification.

---

# Composite Release Types

A release may have overlapping characteristics.

For example:

```text id="wlr67x"
Platform Release
+
Security Release
```

or:

```text id="61u8ac"
Plugin Release
+
Emergency Release
```

In such cases, the strictest applicable requirements SHOULD normally apply.

---

# Primary Release Type

For automation and governance, every release SHOULD identify one primary type.

Example:

```text id="zwhtmk"
primary_type: plugin
security_sensitive: true
emergency: false
```

This reduces ambiguity while allowing additional release attributes.

---

# Release Type Attributes

Future machine-readable release metadata may represent type as attributes instead of one rigid enumeration.

Conceptually:

```text id="cd5dsn"
release:
  domain: plugin
  purpose: maintenance
  security: false
  emergency: false
```

The architecture permits either approach.

---

# Release Channels

A Release Channel represents a controlled availability or stability classification.

The canonical FamilyOS channel model is:

```text id="9ohdui"
development
preview
candidate
stable
maintenance
```

Additional specialized channels MAY be introduced through governance if needed.

---

# Development Channel

The Development Channel exposes highly current engineering builds or releases.

It is intended primarily for:

* maintainers;
* integration testing;
* automated validation;
* development environments.

The Development Channel provides minimal stability expectations.

---

# Development Channel Properties

Typical properties include:

```text id="2h1d20"
stability        low
change frequency high
support          limited
compatibility    not guaranteed
audience         engineering
```

Consumers MUST NOT assume long-term compatibility.

---

# Preview Channel

The Preview Channel exposes functionality before final candidate qualification.

It is intended for:

* evaluation;
* early integration;
* feedback;
* controlled testing.

Preview releases SHOULD be coherent enough for external or broader internal evaluation.

---

# Candidate Channel

The Candidate Channel exposes release candidates that are close to stable qualification.

Candidate releases should have:

* frozen or tightly controlled scope;
* candidate identity;
* strong validation;
* known issues documented;
* final compatibility expectations.

Example:

```text id="0g2ocs"
4.9.0-rc.1
```

---

# Stable Channel

The Stable Channel represents the default officially supported release path.

A stable release should satisfy all mandatory requirements for its release profile.

Consumers may reasonably expect:

* documented behavior;
* explicit version identity;
* required validation;
* stable release artifacts;
* release documentation;
* supported compatibility semantics.

---

# Maintenance Channel

The Maintenance Channel may expose supported releases from an older release line.

Example:

```text id="0o65ko"
stable:
5.1.0

maintenance:
4.9.7
```

This supports parallel maintenance without confusing older supported releases with the current stable line.

---

# Channel vs Version

Channels MUST NOT replace version identity.

For example:

```text id="gsyh2s"
stable
```

is not a release identity.

It is a mutable reference to an explicit version such as:

```text id="3yho2c"
5.1.0
```

---

# Channel Aliases

Channel implementations may use aliases such as:

```text id="phqf30"
dev
preview
rc
stable
maintenance
```

Aliases are mutable distribution references.

Official versions remain immutable historical identities.

---

# Channel Promotion

Promotion moves a validated release or artifact set to a higher-stability channel.

The preferred model is:

```text id="iqqp3x"
development
    ↓
preview
    ↓
candidate
    ↓
stable
```

Promotion SHOULD use the same validated artifacts where practical.

---

# Promotion Principle

The governing principle is:

> Promote validated artifacts; do not casually rebuild them.

A channel promotion SHOULD NOT introduce materially different artifacts without renewed validation.

---

# Promotion Gate

A channel promotion may require:

* applicable validation;
* compatibility confirmation;
* release approval;
* artifact identity verification;
* release notes readiness;
* security approval;
* risk acceptance.

Example:

```text id="yhpiag"
Candidate Channel
        ↓
Promotion Gate
        ↓
Stable Channel
```

---

# Promotion Evidence

A promotion should record:

```text id="5uy0j9"
source channel
target channel
release version
artifact identity
validation state
approval state
timestamp
```

---

# Channel Demotion

A release MAY be removed from a higher-stability channel when problems are discovered.

For example:

```text id="7v8g8b"
stable
   ↓
critical defect
   ↓
withdraw stable reference
```

This must not erase the underlying release history.

---

# Channel Rollback

Channel aliases may be redirected to a previous valid release as part of recovery.

Example:

```text id="qgjd4k"
stable → 5.1.0
```

may be changed to:

```text id="jrqv8y"
stable → 5.0.4
```

if rollback policy permits it.

Both explicit versions remain part of release history.

---

# Release Type and Channel Compatibility

Not every release type belongs in every channel.

Typical compatibility may be:

```text id="m45np4"
Development Release
→ development

Preview Release
→ preview

Release Candidate
→ candidate

Feature Release
→ stable

Maintenance Release
→ stable or maintenance

Security Release
→ stable or maintenance

Emergency Release
→ stable or maintenance after qualification
```

Actual policy may refine these mappings.

---

# Invalid Type and Channel Combinations

Examples that should normally be rejected include:

```text id="s5971c"
development release
published as stable
without stable qualification
```

or:

```text id="ny8ylh"
unvalidated preview
promoted directly to stable
```

The release system should validate type-channel compatibility.

---

# Release Maturity

Release channels communicate maturity.

Conceptually:

```text id="ma1t9s"
experimental
    ↓
evaluated
    ↓
candidate
    ↓
qualified
```

Mapped to channels:

```text id="ii84q6"
development
    ↓
preview
    ↓
candidate
    ↓
stable
```

---

# Release Type and Risk

Release type contributes to risk assessment.

Examples:

```text id="9o8hh5"
documentation patch
→ typically low risk

plugin feature release
→ medium risk

platform major release
→ high risk

security emergency release
→ high urgency, potentially high risk
```

Risk remains an independent release dimension.

---

# Release Type and Validation

Different release types may require different validation profiles.

Example:

```text id="j84h1g"
Documentation Release
├── Markdown validation
├── link validation
├── structure validation
└── governance validation
```

while:

```text id="v14x8o"
Platform Release
├── build validation
├── unit tests
├── integration tests
├── system tests
├── compatibility tests
├── quality gates
├── security validation
├── compliance
└── documentation validation
```

---

# Release Type and Governance

Governance intensity may vary by type.

For example:

```text id="2ns84g"
low-risk documentation patch
→ maintainer approval

major platform release
→ stronger release approval

security emergency release
→ emergency authority
```

The exact authority model is defined in Release Governance.

---

# Release Type and Documentation

Every release type must define applicable communication requirements.

Possible outputs include:

```text id="16uytx"
changelog entry
release notes
migration guidance
security advisory
known issues
compatibility information
```

Not every type requires every document.

---

# Release Type and Recovery

Recovery expectations differ by release type.

Examples:

```text id="9a35bm"
documentation release
→ revert or corrective documentation release

plugin release
→ plugin rollback or corrective plugin release

platform release
→ platform rollback or forward recovery

security release
→ generally avoid re-exposing vulnerable prior state
```

Recovery must remain type-aware.

---

# Stable Release Requirements

A release entering the Stable Channel MUST normally satisfy:

```text id="0e5acv"
official version
validated candidate
required approvals
required release documentation
artifact identity
repository traceability
publication verification
applicable security checks
applicable compliance checks
```

Stable qualification must remain stronger than lower-maturity channels.

---

# Preview Release Requirements

A Preview Release SHOULD normally satisfy:

```text id="w7gn30"
explicit version
known source state
successful core build
required baseline tests
known limitations
basic release notes
```

Stricter requirements may apply depending on audience.

---

# Candidate Release Requirements

A Candidate Release SHOULD normally satisfy:

```text id="84tn5e"
candidate version
frozen release scope
exact artifact set
candidate provenance
release validation
near-final documentation
known issue assessment
```

---

# Development Release Requirements

Development releases may use reduced controls.

However, they SHOULD remain identifiable enough to support debugging and provenance.

A development artifact should ideally identify:

* source revision;
* build identity;
* development version.

---

# Channel Mutability

Channels are mutable references.

Official versions are immutable identities.

This distinction is fundamental.

Example:

```text id="r1953a"
stable
```

may move from:

```text id="jkjkg6"
4.9.0
```

to:

```text id="wl2qi4"
4.10.0
```

without changing either release.

---

# Stable Channel Update

A new stable release normally causes:

```text id="6xqrp0"
stable → previous version
```

to become:

```text id="3jltc8"
stable → new version
```

The previous release may become superseded.

---

# Maintenance Channel Update

A maintenance channel may independently progress:

```text id="tth0c8"
maintenance/4.x
4.9.6
   ↓
4.9.7
```

while:

```text id="akyr4e"
stable
5.1.0
```

remains unchanged.

---

# Channel Naming

Channel names SHOULD be simple, stable, and descriptive.

Preferred concepts include:

```text id="oizb7k"
development
preview
candidate
stable
maintenance
```

Avoid informal names such as:

```text id="ezg1vo"
almost-stable
final2
latest-good
production-maybe
```

---

# Latest Alias

A generic `latest` alias MAY exist.

If used, its semantics MUST be explicit.

For example:

```text id="quh84n"
latest == highest stable version
```

is preferable to ambiguous behavior.

---

# Current Alias

A `current` alias MAY identify the currently recommended release.

It must resolve to an explicit immutable release version.

---

# Security Channel

FamilyOS SHOULD NOT automatically require a separate permanent security channel.

Security releases are generally release types published into stable or maintenance channels.

A specialized security channel may be introduced only if a real distribution need emerges.

---

# Emergency Channel

An emergency release SHOULD NOT require a permanent emergency channel.

Emergency describes release process and urgency, not necessarily consumer stability classification.

Once qualified, an emergency patch may enter the stable channel normally.

---

# Release Profiles

Release types should map to reusable release profiles.

Potential profiles include:

```text id="hh87ny"
development-release
preview-release
framework-release
documentation-release
plugin-release
platform-release
maintenance-release
security-release
emergency-release
```

A profile may define:

* required gates;
* required evidence;
* allowed channels;
* approval requirements;
* publication targets;
* recovery strategy.

---

# Profile Inheritance

Specialized release profiles SHOULD reuse common requirements.

For example:

```text id="ocd5a4"
stable-release
    ↓
plugin-release
    ↓
security-plugin-release
```

Each specialization may add controls.

It should not redefine core release semantics.

---

# Profile Composition

Where practical, release characteristics may compose rather than create endless unique profiles.

Example:

```text id="mx2uy4"
domain = plugin
purpose = maintenance
security = true
emergency = false
channel = stable
```

This provides flexibility without profile explosion.

---

# Channel Configuration

Future FamilyOS release tooling may represent channel configuration in machine-readable form.

Illustrative example:

```text id="cs6nd5"
channels:
  development:
    stability: experimental

  preview:
    stability: pre-release

  candidate:
    stability: candidate

  stable:
    stability: supported
```

This example is conceptual.

---

# Promotion Policy

A future promotion policy may express requirements such as:

```text id="mepm9o"
candidate → stable

requires:
  validation = pass
  security = pass
  compliance = pass
  approval = granted
```

Machine-readable policy should reflect documented framework rules.

---

# Type Policy Example

A future plugin release profile may conceptually define:

```text id="e2tjnw"
release_type: plugin

requires:
  plugin_tests: pass
  plugin_compliance: pass
  platform_compatibility: pass
  documentation: pass
```

Again, the syntax is illustrative.

---

# Release Type Detection

Automation MAY infer a likely release type from changed components.

For example:

```text id="gnymnn"
only docs/ changed
→ documentation candidate
```

or:

```text id="q6zwzx"
plugin source changed
→ plugin candidate
```

Inference MUST NOT silently override explicit release intent when ambiguity exists.

---

# Channel Promotion Without Rebuild

The preferred promotion flow is:

```text id="tc601i"
Build Artifact A
      ↓
Preview
      ↓
Validate Artifact A
      ↓
Candidate
      ↓
Final Validate Artifact A
      ↓
Stable
```

not:

```text id="wh7c9q"
Build Artifact A
      ↓
Validate
      ↓
Build Artifact B
      ↓
Stable
```

unless Artifact B is separately qualified.

---

# Channel Provenance

Release evidence should record channel history where relevant.

Example:

```text id="6kj1kb"
4.9.0-rc.1
candidate

4.9.0
stable
```

or:

```text id="pfolak"
5.1.0
stable
withdrawn

5.0.4
stable
restored
```

---

# Channel Observability

Consumers and operators should be able to determine:

```text id="808mx5"
which version is development
which version is preview
which version is candidate
which version is stable
which maintenance versions are supported
```

Channel state should not require interpretation of unrelated repository activity.

---

# Release Type Observability

Release history should identify release purpose.

For example:

```text id="5lzts2"
4.8.0
type: framework

4.9.0
type: feature

4.9.1
type: security maintenance
```

This improves historical understanding.

---

# Release Channel Governance

Governance must define who may:

* publish into development;
* promote into preview;
* promote into candidate;
* promote into stable;
* update maintenance channels;
* demote or withdraw stable releases.

Higher-stability channels SHOULD generally require stronger authority.

---

# Channel Protection

Stable channel mutation is a sensitive release operation.

Where supported, stable channel updates should be protected through:

* authorization;
* validation;
* auditability;
* version checks;
* publication verification.

---

# Channel Recovery

If a stable release is defective, recovery may involve:

```text id="j0bip3"
stable → defective release
        ↓
detect problem
        ↓
withdraw / demote
        ↓
stable → previous valid release
```

or:

```text id="dvn54v"
stable → defective release
        ↓
corrective release
        ↓
stable → corrected version
```

---

# Channel History

Mutable channel aliases should have recoverable history where practical.

This supports determining:

* when stable changed;
* which version previously occupied the channel;
* why it changed;
* whether a rollback occurred.

---

# Release Type Invariants

The following invariants apply.

## RT1 — Every official release has a clearly defined release purpose.

## RT2 — Release type does not replace version identity.

## RT3 — Emergency status does not bypass core release invariants.

## RT4 — Security release type does not automatically determine semantic version increment.

## RT5 — Specialized release types must preserve common release semantics.

## RT6 — Platform and component releases remain distinguishable.

## RT7 — Stable releases require stronger qualification than development releases.

---

# Release Channel Invariants

## RC1 — Every channel has explicit semantics.

## RC2 — Channels are mutable references, not immutable release identities.

## RC3 — Stable channel promotion requires applicable release qualification.

## RC4 — Promotion should reuse validated artifacts where practical.

## RC5 — Channel demotion must preserve release history.

## RC6 — Channel aliases must resolve to explicit versions.

## RC7 — Channel state must be observable.

---

# Anti-Patterns

## Stable by Naming

Calling an artifact `stable` without performing stable release qualification.

---

## Channel Equals Version

Using:

```text id="vvy3bl"
latest
```

as the only release identity.

---

## Emergency Bypass

Publishing unvalidated artifacts because the release is urgent.

---

## Security Version Guessing

Automatically incrementing patch solely because a release fixes a security issue.

---

## Profile Explosion

Creating a unique release process for every component without reusing common architecture.

---

## Rebuild Promotion

Rebuilding artifacts during channel promotion without renewed qualification.

---

## Hidden Channel Mutation

Changing stable or maintenance aliases without recording the transition.

---

## Undefined Preview

Publishing unstable artifacts publicly without defining their support and compatibility expectations.

---

# Minimum Release Classification

At minimum, every official FamilyOS release should identify:

```text id="2vvfu1"
release version
release type
release stability
release channel where applicable
```

For example:

```text id="dqv6w9"
Version: 4.9.0
Type: Framework
Stability: Stable
Channel: Stable
```

---

# Current FamilyOS Framework Mapping

The current FamilyOS framework completion workflow maps naturally to:

```text id="wk9jwp"
Release Type:
framework

Release Stability:
stable

Release Channel:
stable

Version:
repository milestone version
```

For example, a future completed Release Framework milestone may be represented conceptually as:

```text id="a683ko"
Version: 4.8.0
Type: Framework
Channel: Stable
Tag: v4.8.0-release-framework
```

subject to final release validation and repository state.

---

# Target Release Classification State

At higher maturity, FamilyOS should be able to describe a release using structured information such as:

```text id="mlavfd"
Release
├── version: 5.2.0
├── domain: platform
├── purpose: feature
├── stability: stable
├── channel: stable
├── security: false
└── emergency: false
```

This enables consistent policy evaluation.

---

# Relationship With Versioning

`06-Versioning-Strategy.md` defines the immutable release version.

This document defines release classification and channel exposure.

The relationship is:

```text id="7x4ae3"
Version
+
Release Type
+
Channel
=
Complete Release Classification
```

---

# Relationship With Release Lifecycle

Release types may select different lifecycle profiles.

Channels correspond primarily to publication and distribution state.

For example:

```text id="2ow37b"
CANDIDATE lifecycle state
        ↓
candidate channel
```

and:

```text id="rx9h7b"
COMPLETED stable release
        ↓
stable channel
```

Lifecycle state and channel must not be treated as identical concepts.

---

# Relationship With Release Planning

Release Planning determines:

* intended release type;
* intended target channel;
* expected risk;
* required profile.

These decisions influence all subsequent release gates.

---

# Relationship With Release Readiness

Release Readiness evaluates the requirements associated with the selected release type and target channel.

A stable platform release therefore requires a different readiness set from an internal development release.

---

# Relationship With Release Governance

Release Governance defines the authority required to create, promote, demote, withdraw, or supersede releases across channels.

---

# Final Statement

The FamilyOS Release Types and Channels model establishes a consistent classification system for release purpose, maturity, stability, and distribution.

It allows FamilyOS to distinguish development, preview, feature, maintenance, security, emergency, framework, plugin, platform, and documentation releases while preserving one common release architecture.

By separating immutable release identity from mutable release channels, FamilyOS gains a release model that supports stable publication, pre-release evaluation, parallel maintenance, emergency response, component evolution, and future progressive delivery without sacrificing traceability or governance.
