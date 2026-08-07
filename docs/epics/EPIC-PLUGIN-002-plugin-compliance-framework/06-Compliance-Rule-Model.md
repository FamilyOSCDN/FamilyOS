# Plugin Compliance Framework

# 06 Compliance Rule Model

## Introduction

The Compliance Rule Model defines how FamilyOS represents individual plugin compliance requirements.

A compliance rule is the smallest governed unit of plugin conformance.

Rules translate architectural, engineering, security, testing, quality, documentation, compatibility, lifecycle, and governance requirements into structured and evaluable statements.

The rule model must ensure that every requirement can be:

* identified;
* understood;
* versioned;
* evaluated;
* traced;
* reported;
* governed;
* remediated.

---

# Rule Definition

A compliance rule represents one explicit requirement that applies to one or more plugin contexts.

Conceptually:

```text
ComplianceRule
├── id
├── domain
├── title
├── description
├── requirement
├── rationale
├── severity
├── applicability
├── validation
├── evidence
├── remediation
├── lifecycle
├── ownership
└── versioning
```

The exact physical schema may evolve, but these semantic elements form the core model.

---

# Rule Identity

Every rule must have a stable identifier.

A rule identifier must:

* be unique;
* remain immutable after publication;
* be machine-readable;
* communicate domain ownership where practical;
* support historical traceability.

A conceptual naming pattern is:

```text
PLUGIN-<DOMAIN>-<NUMBER>
```

Examples:

```text
PLUGIN-META-001
PLUGIN-ARCH-004
PLUGIN-SEC-012
PLUGIN-TEST-003
PLUGIN-DOC-006
```

The final grammar must be standardized before implementation.

---

# Rule Identity Stability

A published rule identifier must never silently acquire a materially different meaning.

If the underlying requirement changes substantially, the framework should:

* create a new rule;
* deprecate the previous rule;
* define the replacement relationship.

For example:

```text
PLUGIN-ARCH-004
       │
       ▼
Deprecated
       │
       ▼
Replaced By
       │
       ▼
PLUGIN-ARCH-011
```

This preserves historical compliance records.

---

# Rule Domain

Every rule belongs to one primary compliance domain.

The domain determines:

* ownership;
* reporting location;
* governance responsibility;
* identifier namespace;
* default review path.

A rule may consume evidence related to multiple domains, but it must retain one primary domain.

---

# Rule Title

The rule title provides a concise human-readable description of the requirement.

A title should:

* describe the requirement clearly;
* avoid implementation-specific wording;
* remain understandable in reports;
* remain stable across validator changes.

Example:

```text
Plugin identifiers must use the reserved plugin namespace format.
```

---

# Rule Description

The description explains the requirement in greater detail.

It may include:

* context;
* affected platform contracts;
* expected plugin behavior;
* validation boundaries;
* known limitations.

The description should explain what the rule means without requiring developers to inspect validator source code.

---

# Rule Requirement

The requirement is the normative statement that determines compliance.

Requirements should use precise language.

Examples:

```text
A plugin MUST declare a unique plugin identifier.
```

```text
An official plugin MUST provide documentation for every public capability.
```

```text
A plugin MUST NOT import unsupported runtime-internal modules.
```

Requirements should avoid ambiguous wording when the rule is intended for deterministic validation.

---

# Normative Language

Compliance rules should use standardized normative terminology.

The preferred vocabulary includes:

```text
MUST
MUST NOT
SHOULD
SHOULD NOT
MAY
```

Rules based on `MUST` or `MUST NOT` typically represent enforceable requirements.

Rules based on `SHOULD` or `SHOULD NOT` may produce advisory findings depending on policy.

The exact semantic mapping must be defined by compliance governance.

---

# Rule Rationale

Every rule should explain why the requirement exists.

Rationale improves:

* developer understanding;
* remediation quality;
* review decisions;
* rule governance;
* long-term maintainability.

A rule should not appear arbitrary.

The rationale should connect the requirement to a platform objective such as:

* security;
* compatibility;
* maintainability;
* architectural integrity;
* ecosystem consistency;
* lifecycle reliability.

---

# Rule Severity

Every enforceable rule has a severity.

A conceptual severity model is:

```text
INFO
WARNING
ERROR
CRITICAL
```

Severity expresses the consequence of violation.

It is distinct from validation status.

For example:

```text
Rule Status: FAIL
Severity: WARNING
```

and:

```text
Rule Status: FAIL
Severity: CRITICAL
```

represent different compliance impact.

---

# Severity Semantics

Severity semantics must be globally consistent.

Conceptually:

## INFO

Provides informative compliance feedback.

INFO findings generally do not block compliance.

## WARNING

Represents a concern that should be corrected but may not block lower compliance profiles.

## ERROR

Represents a compliance violation that normally prevents compliant status.

## CRITICAL

Represents a severe violation involving platform safety, security, architecture, or mandatory governance.

CRITICAL findings should normally block release and certification.

The exact enforcement behavior belongs to policy and profile definitions.

---

# Rule Applicability

Not every rule applies to every plugin.

Applicability determines whether a rule belongs to the active evaluation context.

Applicability may depend on:

* plugin classification;
* plugin type;
* declared capabilities;
* contribution types;
* platform version;
* plugin version;
* lifecycle stage;
* compliance profile;
* certification target.

Conceptually:

```text
Rule
  │
  ▼
Applicability Evaluation
  │
  ├── Applicable ─────► Evaluate
  │
  └── Not Applicable ─► Record N/A
```

Applicability must be explicit and deterministic where practical.

---

# Applicability Conditions

Applicability conditions should use structured predicates rather than arbitrary validator logic.

Conceptually:

```text
classification == official
```

```text
capability == communication.send
```

```text
platform_version >= 4.0
```

```text
contribution_type == policy
```

The implementation language may differ, but applicability must remain inspectable and governed.

---

# Rule Profiles

Rules are activated through compliance profiles.

A rule may belong to multiple profiles.

For example:

```text
PLUGIN-META-001
├── development
├── built-in
├── official
└── third-party
```

Another rule may apply only to:

```text
PLUGIN-GOV-008
└── official
```

Profiles compose existing rules rather than redefining them.

---

# Mandatory Rules

A rule may be classified as mandatory.

Mandatory rules represent requirements that cannot be omitted by ordinary profile configuration.

Typical candidates include:

* critical identity rules;
* mandatory manifest requirements;
* critical security requirements;
* prohibited internal dependencies;
* core runtime safety constraints.

Mandatory status must be governed explicitly.

---

# Validation Binding

Every automated rule must define how it is evaluated.

A rule may reference:

* a validator;
* a validator family;
* an evidence query;
* a policy evaluator;
* a runtime contract check.

Conceptually:

```text
ComplianceRule
      │
      ▼
ValidationBinding
      │
      ▼
Validator
```

The rule defines the requirement.

The validator implements the evaluation mechanism.

---

# Validator Independence

Rule meaning must not depend on one validator implementation.

A validator may be replaced without changing the rule identity if:

* the requirement remains unchanged;
* evaluation semantics remain equivalent;
* evidence remains compatible.

This allows compliance tooling to improve while preserving policy stability.

---

# Manual Validation Rules

Some rules may require human review.

Such rules must be explicitly marked.

Conceptually:

```text
validation_mode = automated
```

or:

```text
validation_mode = manual
```

or:

```text
validation_mode = hybrid
```

Manual rules must not silently return automated success.

The result must show that human evidence or approval is required.

---

# Hybrid Validation

Some compliance requirements may combine machine evaluation and human judgment.

For example:

```text
Documentation File Exists
        │
        ▼
Automated Validation
        │
        ▼
Documentation Quality Review
        │
        ▼
Human Validation
```

Hybrid rules should preserve both evidence sources separately.

---

# Evidence Requirements

A rule should define which evidence is required to make a decision.

Evidence requirements may specify:

* evidence type;
* producer;
* freshness;
* trust level;
* scope;
* minimum quantity;
* version compatibility.

Conceptually:

```text
Rule
 │
 ▼
Required Evidence
 │
 ├── manifest metadata
 ├── static analysis
 └── test results
```

A rule cannot pass if required evidence is unavailable unless policy explicitly allows an alternate validation path.

---

# Evidence Optionality

Evidence may be:

```text
REQUIRED
OPTIONAL
ALTERNATIVE
SUPPORTING
```

For example:

```text
Static Analysis Evidence
        OR
Architecture Test Evidence
```

may be allowed when both provide equivalent assurance.

Alternative evidence paths must be governed explicitly.

---

# Evidence Freshness

Rules may require evidence produced within a defined validation context.

Evidence freshness should consider:

* plugin version;
* source revision;
* platform version;
* framework version;
* execution timestamp;
* dependency state.

Evidence from a previous plugin version must not silently satisfy a current rule unless compatibility is demonstrated.

---

# Rule Evaluation Status

A canonical rule evaluation should support explicit outcome states.

A conceptual model is:

```text
PASS
FAIL
WARNING
NOT_APPLICABLE
NOT_EVALUATED
ERROR
```

The final vocabulary must be standardized globally.

These statuses are separate from severity.

---

# PASS

PASS means that the available evidence demonstrates that the requirement is satisfied.

A pass must be traceable to evidence.

---

# FAIL

FAIL means that validation demonstrates that the requirement is violated.

A failed rule should normally produce a compliance finding.

---

# WARNING

WARNING may represent partial or advisory non-conformance when the framework chooses to model this directly as a status.

Alternatively, warning behavior may be represented through:

```text
status = FAIL
severity = WARNING
```

The framework should select one canonical semantic model and avoid ambiguity.

---

# NOT_APPLICABLE

NOT_APPLICABLE means that the rule is valid but does not apply to the current plugin context.

The applicability decision must remain visible.

---

# NOT_EVALUATED

NOT_EVALUATED means the rule applies but was not evaluated.

Possible reasons include:

* missing evidence;
* disabled optional validator;
* unsupported environment;
* deferred manual review.

NOT_EVALUATED must never be interpreted as PASS.

---

# ERROR

ERROR means that the validation mechanism failed to produce a valid compliance decision.

Examples include:

* validator crash;
* corrupted evidence;
* unsupported rule implementation;
* internal compliance engine error.

ERROR represents framework execution failure, not necessarily plugin non-compliance.

---

# Finding Generation

Rules define when findings should be generated.

Typical mapping:

```text
PASS
  └── no finding

FAIL
  └── finding

NOT_APPLICABLE
  └── no finding

NOT_EVALUATED
  └── incomplete finding or evaluation notice

ERROR
  └── validation error finding
```

The exact mapping may vary according to framework semantics.

---

# Rule Remediation

Every rule that can fail should provide remediation guidance.

Remediation should describe how a developer can move from failure to compliance.

A remediation section may include:

* corrective action;
* expected structure;
* supported API;
* replacement dependency;
* documentation reference;
* migration guidance.

Good remediation reduces compliance friction.

---

# Remediation Quality

Remediation guidance should avoid vague instructions such as:

```text
Fix the plugin.
```

Preferred guidance is specific:

```text
Replace imports from familyos.runtime.internal with the public capability API exposed by familyos.sdk.runtime.
```

The framework should treat remediation clarity as part of rule quality.

---

# Rule Ownership

Every published rule should have an explicit governance owner.

Ownership may be associated with:

* architecture governance;
* security governance;
* testing framework;
* quality framework;
* documentation governance;
* plugin platform governance.

Ownership determines who is responsible for reviewing rule evolution.

---

# Rule Source Authority

Rules should identify the authoritative requirement source.

Examples include:

```text
Engineering Constitution
Plugin Architecture
Testing Framework
Quality Framework
Security Architecture
Documentation Framework
ADR
RFC
Specification
```

This provides traceability between compliance enforcement and platform governance.

---

# Rule References

A compliance rule may include references to supporting documents.

Conceptually:

```text
references:
  - ADR-0007
  - EPIC-TST-001
  - Security-Architecture.md
```

References explain where the requirement originates and where developers can learn more.

---

# Rule Lifecycle

Rules themselves have lifecycle states.

A conceptual lifecycle is:

```text
DRAFT
  │
  ▼
ACTIVE
  │
  ▼
DEPRECATED
  │
  ▼
RETIRED
```

Additional states should only be introduced when governance requires them.

---

# Draft Rules

DRAFT rules may be used for experimentation or review.

They must not silently affect stable compliance profiles unless explicitly enabled.

---

# Active Rules

ACTIVE rules participate in normal compliance evaluation.

Their semantics must be considered stable according to framework versioning policy.

---

# Deprecated Rules

DEPRECATED rules remain valid for compatibility or historical reasons but are scheduled for replacement or removal.

A deprecated rule should identify:

* deprecation reason;
* deprecation version;
* replacement rule when available;
* expected removal window.

---

# Retired Rules

RETIRED rules no longer participate in active validation.

Historical compliance records must still retain their meaning.

Rule metadata should remain available for audit and report interpretation.

---

# Rule Versioning

Rule evolution must be version-aware.

Possible changes include:

* description clarification;
* remediation update;
* severity change;
* applicability change;
* requirement change;
* validator replacement;
* evidence requirement change.

Not all changes have equal compatibility impact.

---

# Non-Breaking Rule Changes

Examples may include:

* spelling corrections;
* clearer remediation guidance;
* additional references;
* equivalent validator optimization.

These changes may preserve the existing rule identity.

---

# Breaking Rule Changes

Examples include:

* materially stronger requirement;
* expanded applicability;
* stricter evidence requirement;
* changed compliance meaning.

Breaking changes may require:

* a new rule identity;
* a framework major version;
* explicit migration policy.

The governance model must define the correct strategy.

---

# Rule Deprecation

Deprecation must be explicit and observable.

A rule should never simply disappear from the active catalog without traceability.

Conceptually:

```text
ACTIVE
  │
  ▼
DEPRECATED
  │
  ├── replacement available
  │
  ▼
RETIRED
```

Compliance reports should remain able to interpret previous results.

---

# Rule Replacement

A replacement relation should be machine-readable where possible.

Example:

```text
replaced_by = PLUGIN-ARCH-011
```

This allows tooling to provide migration guidance automatically.

---

# Exception Eligibility

Not every rule should permit exceptions.

Rules may define an exception policy such as:

```text
NONE
GOVERNED
TEMPORARY
PROFILE_SPECIFIC
```

Security-critical rules may define:

```text
exception_policy = NONE
```

or require elevated governance authority.

---

# Suppression Eligibility

Rules may define whether individual findings may be suppressed.

Suppression and exception are distinct.

A suppression modifies how a known finding is handled or displayed.

An exception modifies how the requirement affects compliance policy.

The rule model must keep these semantics separate.

---

# Rule Dependencies

Some rules may depend on prerequisite rules.

For example:

```text
PLUGIN-CAP-010
      │
      depends on
      ▼
PLUGIN-META-004
```

A capability implementation rule may only be meaningful after the capability declaration itself is valid.

Dependencies should be explicit rather than encoded implicitly inside validators.

---

# Rule Dependency Semantics

When a prerequisite fails, the dependent rule may become:

```text
NOT_EVALUATED
```

rather than producing misleading duplicate failures.

This improves report clarity and avoids cascading noise.

---

# Rule Ordering

The rule catalog should not rely on arbitrary execution order.

Where ordering is required, it must be represented through explicit dependencies.

Validation planning can then construct a deterministic evaluation graph.

---

# Rule Evaluation Graph

Conceptually:

```text
PLUGIN-META-001
      │
      ▼
PLUGIN-META-004
      │
      ├──────────► PLUGIN-CAP-001
      │
      └──────────► PLUGIN-CONTRIB-001
                       │
                       ▼
                 PLUGIN-ARCH-010
```

This allows the engine to skip or defer rules whose prerequisites are unresolved.

---

# Rule Families

Related rules may belong to a common family.

Examples:

```text
Plugin Identifier Rules
Capability Declaration Rules
Dependency Boundary Rules
Documentation Completeness Rules
```

Families improve documentation and navigation but do not replace individual stable rule identities.

---

# Rule Tags

Rules may carry governed tags for discovery and automation.

Examples:

```text
security-critical
release-blocking
architecture
official-plugin
third-party
certification
```

Tags must not silently replace formal domain, severity, or applicability semantics.

---

# Rule Metadata Example

A conceptual rule representation might look like:

```text
id: PLUGIN-ARCH-001
domain: architecture
title: Plugins must use public platform APIs
requirement: Plugins MUST NOT import unsupported FamilyOS internal modules.
severity: ERROR
validation_mode: automated
validator: architecture.import-boundary
profiles:
  - built-in
  - official
  - third-party
mandatory: true
exception_policy: governed
lifecycle: active
```

This example is illustrative.

The detailed schema will be defined separately.

---

# Rule Validation Example

Conceptually:

```text
Rule
  PLUGIN-ARCH-001
        │
        ▼
Import Graph Evidence
        │
        ▼
Architecture Validator
        │
   ┌────┴────┐
   ▼         ▼
 PASS       FAIL
              │
              ▼
       Compliance Finding
```

This demonstrates the separation between rule definition, evidence, validator, and finding.

---

# Rule Quality Requirements

A compliance rule is itself a governed engineering artifact.

Every production rule should satisfy quality requirements including:

* unambiguous requirement;
* stable identity;
* clear domain;
* defined severity;
* explicit applicability;
* defined validation strategy;
* defined evidence requirements;
* actionable remediation;
* test coverage;
* ownership;
* version traceability.

A poorly defined rule weakens the entire compliance system.

---

# Rule Test Requirements

Automated rules should have dedicated tests.

At minimum:

```text
Passing Case
Failing Case
Not Applicable Case
Error Case
Boundary Cases
```

Where applicable, tests should also cover:

* dependency behavior;
* profile applicability;
* evidence freshness;
* exception handling.

---

# Rule Documentation

The rule catalog should be documentable automatically.

Because rule metadata is structured, FamilyOS should eventually be capable of generating:

* rule reference documentation;
* domain indexes;
* profile requirement lists;
* remediation guides;
* deprecation notices.

This reduces divergence between implementation and documentation.

---

# Rule Discovery

Developers should be able to inspect active rules.

Future tooling may support concepts such as:

```text
familyos plugin compliance rules
```

or:

```text
familyos plugin compliance explain PLUGIN-ARCH-001
```

Rule discovery is a core developer-experience requirement.

---

# Rule Governance Flow

A conceptual rule lifecycle process is:

```text
Requirement Identified
        │
        ▼
Rule Proposal
        │
        ▼
Domain Review
        │
        ▼
Compliance Review
        │
        ▼
Implementation
        │
        ▼
Rule Tests
        │
        ▼
Activation
        │
        ▼
Monitoring
        │
        ▼
Evolution / Deprecation
```

Rules must not enter stable profiles without review and validation.

---

# Rule Catalog Invariants

The Compliance Rule Model establishes the following invariants:

1. Every rule has one stable identifier.
2. Every rule has one primary domain.
3. Every enforceable rule has defined severity.
4. Applicability is explicit.
5. Validation strategy is defined.
6. Required evidence is identified.
7. Failed rules provide remediation guidance.
8. Rule meaning does not depend on presentation tooling.
9. Rule lifecycle is governed.
10. Deprecated rules remain historically traceable.
11. Rule dependencies are explicit.
12. Unknown evaluation never becomes implicit PASS.
13. Automated rules are themselves tested.
14. Rules reference authoritative platform requirements.
15. Plugins cannot redefine compliance rules governing themselves.

---

# Rule Model Summary

The FamilyOS compliance rule model can be summarized as:

```text
Platform Requirement
        │
        ▼
Compliance Rule
        │
        ├── Identity
        ├── Domain
        ├── Severity
        ├── Applicability
        ├── Validation
        ├── Evidence
        ├── Remediation
        ├── Governance
        └── Lifecycle
                │
                ▼
          Rule Evaluation
                │
                ▼
          Rule Outcome
                │
                ▼
             Finding
```

This model provides the smallest reusable building block of the Plugin Compliance Framework.

---

# Final Rule Principle

The governing principle of the Compliance Rule Model is:

> A compliance requirement is enforceable only when its meaning, applicability, evidence, evaluation, and consequences are explicit.

FamilyOS compliance rules must therefore remain stable, traceable, testable, understandable, and governed throughout their entire lifecycle.
