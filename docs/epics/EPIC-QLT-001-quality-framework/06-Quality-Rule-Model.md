# Quality Framework

# 06 Quality Rule Model

## Overview

The FamilyOS Quality Rule Model defines how quality requirements are translated into explicit, evaluable, and governable rules.

A quality rule is the operational expression of a quality requirement.

It establishes:

* what must be verified;
* where the rule applies;
* how the rule is evaluated;
* what result is expected;
* what severity applies;
* whether failure is blocking;
* what evidence must be produced;
* how exceptions are handled;
* how the rule evolves over time.

The Quality Rule Model provides the bridge between quality intent and executable quality verification.

---

# Purpose

The purpose of the Quality Rule Model is to transform broad quality expectations into precise engineering constraints.

Without a formal rule model, quality requirements may remain:

* ambiguous;
* inconsistent;
* difficult to automate;
* difficult to govern;
* difficult to trace;
* difficult to audit.

The model therefore establishes a consistent path:

```text
Quality Principle
        ↓
Quality Policy
        ↓
Quality Requirement
        ↓
Quality Rule
        ↓
Quality Check
        ↓
Quality Evidence
```

A quality rule must be specific enough to support reliable evaluation.

---

# Rule Definition

A Quality Rule is a versioned engineering constraint associated with one or more quality requirements.

A rule defines a condition that can be evaluated against a specific target.

Conceptually:

```text
Rule
  =
Applicability
  +
Condition
  +
Evaluation Method
  +
Expected Result
  +
Severity
  +
Governance Metadata
```

A rule must be clear enough that two independent implementations can interpret its intent consistently.

---

# Rule Characteristics

A FamilyOS quality rule should be:

* explicit;
* uniquely identifiable;
* traceable;
* scoped;
* versioned;
* deterministic where practical;
* testable;
* explainable;
* governable;
* tool-independent.

The rule definition must describe the engineering expectation rather than embed unnecessary implementation details.

---

# Rule Identity

Each quality rule must have a stable identifier.

A conceptual naming pattern may be:

```text
QLT-RULE-<DOMAIN>-<NUMBER>
```

Examples:

```text
QLT-RULE-ARC-001
QLT-RULE-SEC-004
QLT-RULE-TST-012
QLT-RULE-DOC-003
```

The exact identifier scheme may evolve, but identifiers must remain:

* unique;
* stable;
* human-readable where practical;
* suitable for machine processing.

Identifiers must not be silently reused for different semantics.

---

# Rule Metadata

A quality rule should contain structured metadata.

A conceptual rule model may include:

```text
id
title
description
domain
requirement_id
rationale
scope
severity
blocking
execution_type
status
version
owner
introduced_at
deprecated_at
replacement_rule
tags
```

Additional implementation-specific metadata may be added later.

---

# Rule Title

The title should provide a concise description of the expected behavior.

Example:

```text
Public interfaces must satisfy type verification
```

Titles should describe the engineering requirement rather than the underlying tool.

Preferred:

```text
Python modules must satisfy static analysis requirements
```

Avoid:

```text
Ruff must pass
```

because the rule should remain conceptually independent from the tool.

---

# Rule Description

The rule description defines the condition being evaluated.

It should answer:

```text
What must be true?

Which target is affected?

Under which conditions does the rule apply?
```

A good rule description must minimize ambiguity.

---

# Rule Rationale

Every significant rule should explain why it exists.

The rationale may reference:

* architecture integrity;
* correctness;
* security;
* maintainability;
* reliability;
* compliance;
* developer experience;
* release confidence.

Example:

```text
Public interfaces must satisfy type verification because
type inconsistencies increase compatibility risk and reduce
static correctness guarantees across component boundaries.
```

Rationale improves:

* adoption;
* governance;
* review;
* exception decisions;
* long-term maintainability.

---

# Rule Domain

Every rule must belong to one primary Quality Domain.

Examples:

```text
Architecture
Security
Testing
Documentation
Compatibility
Maintainability
```

The primary domain determines the rule's main classification and governance ownership.

A rule may also reference related domains.

---

# Rule Requirement Traceability

Every rule should trace to at least one Quality Requirement.

Example:

```text
Requirement:
QLT-REQ-ARC-003

Rule:
QLT-RULE-ARC-007
```

The relationship is:

```text
Requirement
    ↓
Rule
```

A requirement may generate several rules.

A rule should not exist without a clear requirement unless it is explicitly classified as provisional or experimental.

---

# Rule Scope

Scope defines where a rule applies.

Possible scopes include:

```text
File
Module
Package
Capability
Plugin
Repository
Build
Release
Platform
```

Scope may also include target filters.

Example:

```text
scope:
  type: file
  language: python
```

or:

```text
scope:
  type: plugin
  classification: official
```

Scope must remain precise enough to avoid unintended enforcement.

---

# Rule Applicability

Applicability determines whether a rule is relevant to a particular target.

Applicability may depend on:

* target type;
* programming language;
* quality profile;
* component criticality;
* lifecycle stage;
* domain;
* repository configuration;
* release context.

Conceptually:

```text
Target
   ↓
Applicability Evaluation
   ├── Applicable
   └── Not Applicable
```

A non-applicable rule should produce a clear `NOT_APPLICABLE` state rather than silently disappearing.

---

# Rule Condition

The condition defines the actual quality expectation.

Examples:

```text
No dependency may violate the defined architecture direction.

All required tests must pass.

Critical security vulnerabilities must not remain unresolved.

Required documentation metadata must be present.

Public capability contracts must remain backward compatible.
```

Conditions should be written in implementation-neutral language whenever practical.

---

# Rule Evaluation Type

Rules may use several evaluation types.

Initial categories may include:

```text
AUTOMATED
MANUAL
HYBRID
ADVISORY
```

---

# Automated Rules

An automated rule can be evaluated deterministically by software.

Examples include:

* lint checks;
* type verification;
* dependency validation;
* test execution;
* metadata validation;
* architecture checks.

Automated rules should provide reproducible evidence.

---

# Manual Rules

A manual rule requires engineering judgment.

Examples include:

* architecture coherence review;
* domain modeling assessment;
* documentation usefulness;
* risk acceptance review.

Manual rules must still define:

* evaluation criteria;
* expected evidence;
* responsible reviewer;
* decision semantics.

Manual must not mean informal.

---

# Hybrid Rules

A hybrid rule combines automated evidence and human judgment.

Example:

```text
Automated Dependency Analysis
        +
Architecture Review
        ↓
Final Architecture Compliance Decision
```

Hybrid rules are appropriate when automation can detect signals but cannot determine the full engineering context.

---

# Advisory Rules

Advisory rules provide information without automatically blocking progress.

Examples may include:

* complexity warnings;
* performance degradation notices;
* style recommendations;
* maturity recommendations.

Advisory rules remain part of the quality system and should be traceable.

---

# Rule Severity

Every finding produced by a rule should map to a defined severity model.

The baseline FamilyOS model may include:

```text
INFO
LOW
MEDIUM
HIGH
CRITICAL
```

Severity describes engineering impact.

It must not be confused with whether a rule blocks a gate.

---

# Severity and Blocking Are Separate

A finding may be severe without automatically blocking every workflow.

Similarly, a lower-severity finding may be blocking in a specific profile.

Therefore:

```text
Severity
    ≠
Blocking Behavior
```

Blocking behavior is determined by:

* rule configuration;
* quality profile;
* gate policy;
* lifecycle stage;
* component criticality.

---

# Rule Blocking Behavior

Rules may define default blocking behavior.

Possible values include:

```text
NON_BLOCKING
CONDITIONALLY_BLOCKING
BLOCKING
```

The final behavior may be refined by the applicable quality profile.

Example:

```text
Security HIGH
    ↓
Non-blocking in Experimental Profile
Blocking in Release Profile
```

Such differences must be explicit.

---

# Rule Result Model

Rule evaluation should produce standardized result states.

Possible states include:

```text
PASS
FAIL
WARNING
ERROR
SKIPPED
NOT_APPLICABLE
```

These states must have stable semantics.

---

# PASS

`PASS` means the rule was successfully evaluated and its condition was satisfied.

---

# FAIL

`FAIL` means the rule was successfully evaluated and its condition was not satisfied.

A failure should normally produce one or more findings.

---

# WARNING

`WARNING` means the rule produced a concern that does not currently constitute a failure.

Warnings should remain visible and traceable.

---

# ERROR

`ERROR` means the rule could not be evaluated because the verification mechanism failed.

Examples:

* tool execution failure;
* invalid configuration;
* missing dependency;
* corrupted evidence.

An `ERROR` must not be interpreted as `PASS`.

---

# SKIPPED

`SKIPPED` means the rule was intentionally not executed.

The reason should be recorded.

Examples:

* explicitly disabled by profile;
* unavailable execution environment;
* approved execution exception.

---

# NOT_APPLICABLE

`NOT_APPLICABLE` means the rule does not apply to the evaluated target.

This is distinct from `SKIPPED`.

---

# Rule Evidence

Each rule evaluation should generate evidence.

Evidence should answer:

```text
Which rule was evaluated?

Against what target?

Which implementation performed the check?

Which rule version applied?

What result was produced?

What supporting information exists?
```

Evidence may include:

* command output;
* structured findings;
* metrics;
* reports;
* artifacts;
* reviewer decisions.

---

# Rule Findings

A failed or advisory rule may produce one or more Quality Findings.

Example:

```text
Rule:
No cross-plugin internal imports

Finding:
Plugin A imports internal package from Plugin B
```

One rule may generate multiple findings.

---

# Finding Normalization

Tool-specific output should be normalized to the FamilyOS finding model.

Example:

```text
External Tool Finding
        ↓
Adapter
        ↓
FamilyOS Quality Finding
```

Normalization should preserve sufficient original context while using a common semantic model.

---

# Rule Execution Provider

A rule may be implemented by one or more execution providers.

Example:

```text
QLT-RULE-TYP-001
        ↓
Type Verification Capability
        ↓
MyPy Adapter
```

The rule must not depend conceptually on the current provider.

A future provider should be replaceable without changing the rule semantics.

---

# Rule Configuration

Rules may expose configuration parameters.

Examples:

```text
threshold
timeout
severity
path_filter
exclusions
minimum_coverage
maximum_complexity
```

Configuration must be:

* explicit;
* validated;
* version-controlled where authoritative;
* traceable in evidence.

---

# Rule Defaults

Rules may define default configuration values.

Example:

```text
timeout = 120 seconds
severity = HIGH
blocking = true
```

Default values must represent safe baseline behavior.

Overrides must follow configuration governance.

---

# Rule Thresholds

Some rules depend on thresholds.

Examples include:

```text
Minimum Coverage
Maximum Complexity
Maximum Allowed Latency
Maximum Dependency Age
Maximum Allowed Findings
```

Thresholds must be contextual.

A threshold should define:

* unit;
* comparison operator;
* expected value;
* scope;
* profile applicability.

---

# Threshold Example

A conceptual rule could define:

```text
metric:
  name: test_coverage
operator: greater_or_equal
threshold: 85
unit: percent
```

The exact serialization format is an implementation concern.

The semantic model remains stable.

---

# Rule Profiles

Quality Profiles determine which rules apply to particular component classes.

Example:

```text
Base Profile
    ↓
QLT-RULE-COR-001
QLT-RULE-ARC-001
QLT-RULE-DOC-001

Official Plugin Profile
    ↓
Base Profile
+
QLT-RULE-CPL-010
QLT-RULE-CPL-011
```

Profiles should reuse rules rather than duplicate them.

---

# Rule Inheritance

Rules themselves should generally not inherit from each other.

Inheritance complexity should remain in:

* requirements;
* profiles;
* configuration.

This reduces hidden behavior.

A rule should remain a clear, directly evaluable unit.

---

# Rule Composition

A complex requirement may be represented by several rules.

Example:

```text
Requirement:
Official plugins must be structurally compliant.

        ↓

Rule 1:
Manifest must exist.

Rule 2:
Required capabilities must be declared.

Rule 3:
Plugin boundaries must be respected.

Rule 4:
Required documentation must exist.
```

This is preferable to one opaque monolithic rule.

---

# Atomic Rules

Rules should be as atomic as practical.

An atomic rule:

* evaluates one clear concern;
* generates focused findings;
* supports targeted remediation;
* simplifies ownership;
* improves traceability.

Avoid rules such as:

```text
Plugin must be completely valid.
```

because this combines unrelated concerns.

---

# Composite Checks

Atomic rules do not require one process invocation per rule.

A single check provider may evaluate several atomic rules efficiently.

Example:

```text
Architecture Check
      ↓
QLT-RULE-ARC-001
QLT-RULE-ARC-002
QLT-RULE-ARC-003
```

Execution efficiency and rule semantics remain separate concerns.

---

# Rule Ordering

Rules should generally be independent.

However, some evaluations may depend on prerequisite rules.

Example:

```text
Manifest Parsing Rule
      ↓
Capability Validation Rules
```

Dependencies must be explicit.

Hidden execution ordering should be avoided.

---

# Rule Dependencies

A rule may declare prerequisites.

Conceptually:

```text
rule:
  QLT-RULE-CPL-002

depends_on:
  QLT-RULE-CPL-001
```

If the prerequisite fails, the dependent rule may become:

```text
SKIPPED
```

or:

```text
ERROR
```

depending on semantics.

The behavior must be defined.

---

# Rule Conflict Prevention

Two rules should not impose contradictory requirements on the same target.

Rule governance must detect or prevent conflicts.

Potential conflict:

```text
Rule A:
Dependency X must be version 2.

Rule B:
Dependency X must be version 3.
```

Conflicts must be resolved at the framework level rather than left to tool behavior.

---

# Rule Precedence

If override mechanisms exist, precedence must be deterministic.

A possible model is:

```text
Framework Mandatory Rule
        ↓
Profile Rule Configuration
        ↓
Repository Configuration
        ↓
Approved Exception
```

Mandatory requirements must not be silently disabled by lower-precedence configuration.

---

# Mandatory Rules

Some rules may be classified as mandatory.

Mandatory rules cannot be disabled through ordinary local configuration.

Examples may include:

* critical security requirements;
* core architecture boundaries;
* release integrity rules;
* evidence integrity rules.

Bypass requires a governed exception if permitted at all.

---

# Optional Rules

Optional rules may be enabled by profiles or repositories.

Examples may include:

* experimental metrics;
* stricter maintainability checks;
* additional performance checks.

Optional rules must still use the same rule model.

---

# Experimental Rules

New rules may enter an experimental state.

Experimental rules allow FamilyOS to evaluate:

* false-positive rate;
* developer impact;
* runtime cost;
* usefulness;
* threshold suitability.

Experimental rules should normally be non-blocking.

---

# Rule Lifecycle

A quality rule should follow a controlled lifecycle.

A baseline lifecycle may be:

```text
DRAFT
  ↓
EXPERIMENTAL
  ↓
ACTIVE
  ↓
DEPRECATED
  ↓
RETIRED
```

Not every rule must pass through every state, but transitions must be controlled.

---

# DRAFT

A draft rule is under development.

It must not be treated as authoritative unless explicitly configured for testing.

---

# EXPERIMENTAL

An experimental rule may execute in real workflows but should normally not block engineering progress.

Its purpose is validation and calibration.

---

# ACTIVE

An active rule is part of the authoritative quality framework.

Its behavior and semantics are governed.

---

# DEPRECATED

A deprecated rule remains supported temporarily but should no longer be used for new quality profiles.

A replacement should be identified where applicable.

---

# RETIRED

A retired rule is no longer active.

Historical evidence must remain interpretable.

Its identifier must not be reused.

---

# Rule Versioning

Rules must be versioned when their semantics materially change.

Examples of material changes include:

* different applicability;
* different condition;
* different severity interpretation;
* different blocking semantics;
* changed threshold meaning.

Minor metadata or wording improvements may not require semantic version changes if behavior remains identical.

---

# Rule Semantic Stability

A rule identifier should represent a stable quality concept.

If the fundamental meaning changes, the framework should consider creating a new rule instead of silently redefining the existing one.

This protects historical evidence.

---

# Rule Deprecation

Deprecation should define:

* deprecation date;
* reason;
* replacement;
* migration guidance;
* final retirement target.

Deprecated rules should remain visible in governance reporting.

---

# Rule Ownership

Every active rule must have an owner.

Ownership includes responsibility for:

* semantic definition;
* lifecycle;
* configuration guidance;
* issue interpretation;
* exception policy;
* replacement decisions.

Ownership may belong to a framework, domain authority, or designated engineering role.

---

# Rule Review

Rules should undergo review before becoming authoritative.

Review should consider:

```text
Is the rule necessary?

Is the scope correct?

Is the condition clear?

Can it be evaluated reliably?

Is the severity appropriate?

Is blocking behavior justified?

What is the expected developer impact?

Can findings be remediated?
```

Rules that cannot provide useful remediation should be reconsidered.

---

# Rule Validation

The framework should validate rule definitions themselves.

Validation may verify:

* required metadata;
* unique identifiers;
* valid domain;
* valid requirement reference;
* supported status;
* valid severity;
* valid configuration schema;
* valid dependencies.

Invalid rules must not silently become active.

---

# Rule Testing

Rule implementations must be tested.

Testing should include:

* positive cases;
* negative cases;
* edge cases;
* applicability behavior;
* configuration behavior;
* error behavior;
* severity mapping;
* evidence generation.

A quality rule that is incorrectly implemented can produce false engineering decisions.

---

# Golden Rule Tests

Important rules may use golden test fixtures.

Example:

```text
Compliant Fixture
      ↓
Expected PASS

Non-Compliant Fixture
      ↓
Expected FAIL
```

Golden tests help preserve rule behavior across implementation changes.

---

# False Positives

A false positive occurs when a rule reports a violation where the target is actually acceptable.

False positives create:

* developer frustration;
* ignored warnings;
* bypass behavior;
* reduced trust.

The framework must monitor and minimize false-positive rates.

---

# False Negatives

A false negative occurs when a rule fails to detect a real violation.

False negatives create incorrect confidence.

Critical rules should prioritize reliable detection over cosmetic convenience.

---

# Rule Precision

Rules should balance:

```text
Detection Coverage
        ↕
Precision
```

The appropriate balance depends on risk.

Critical security rules may prefer broader detection.

Advisory maintainability rules may prefer higher precision to avoid noise.

---

# Rule Performance

Quality rules affect developer feedback time.

Rule implementations should therefore consider execution cost.

Performance characteristics may include:

* startup time;
* execution duration;
* memory usage;
* external dependency requirements.

Slow rules may be assigned to deeper execution profiles if immediate feedback is not required.

---

# Fast Rules

Fast rules are appropriate for local workflows.

Examples may include:

* formatting;
* linting;
* lightweight architecture checks;
* metadata validation.

Fast rules should normally execute early.

---

# Deep Rules

Deep rules may require more resources.

Examples include:

* full integration testing;
* security analysis;
* performance benchmarks;
* compatibility suites.

These may execute in CI or release workflows.

---

# Rule Execution Context

Every evaluation should record relevant context.

Possible context includes:

```text
repository_commit
branch
target
profile
environment
tool_version
rule_version
configuration_version
```

This improves reproducibility and auditability.

---

# Rule Determinism

Rules should be deterministic where possible.

Given equivalent:

```text
Target
Rule Version
Configuration
Environment
```

the result should be equivalent.

Nondeterministic rule implementations must document the reason.

---

# External Dependencies

Rules should minimize dependence on uncontrolled external services.

External dependency failures can make quality evaluation unreliable.

If external services are necessary, the rule should define:

* timeout behavior;
* retry behavior;
* failure semantics;
* evidence handling.

---

# Rule Error Semantics

Execution failure must never silently imply compliance.

Example:

```text
Scanner unavailable
```

must produce:

```text
ERROR
```

rather than:

```text
PASS
```

The applicable quality gate then decides how an error affects progression.

---

# Rule Remediation

Every actionable rule should provide remediation guidance.

Remediation may include:

* explanation;
* expected correction;
* documentation reference;
* example;
* automated fix capability.

A quality system should not merely report failure.

It should help engineers resolve it.

---

# Auto-Fix Support

Some rules may support automated remediation.

Examples include:

* formatting;
* import cleanup;
* metadata normalization.

Auto-fix capabilities must be:

* deterministic;
* safe;
* reviewable;
* optional when risk exists.

The rule itself remains separate from its remediation mechanism.

---

# Suppression

Local suppression of findings must be controlled.

Examples such as inline suppression markers may be permitted for specific rule classes.

Suppression must not become an invisible exception system.

A suppression should ideally record:

* rule ID;
* reason;
* scope.

---

# Suppression vs Exception

Suppression and exception are distinct.

```text
Suppression
    ↓
Local handling of an individual finding

Exception
    ↓
Governed deviation from a quality requirement
```

High-risk or blocking rules should typically require formal exceptions rather than casual suppression.

---

# Rule Exceptions

A rule may define whether exceptions are allowed.

Possible policies include:

```text
NOT_ALLOWED
APPROVAL_REQUIRED
TIME_BOUND
LOCAL_SUPPRESSION_ALLOWED
```

The policy should reflect the risk of the rule.

---

# Exception Application

An approved exception should reference:

* rule identifier;
* scope;
* target;
* reason;
* risk;
* expiration;
* owner;
* approver.

The rule still executes when practical.

The exception modifies the decision interpretation rather than erasing evidence.

---

# Rule Baselines

Rules may support baselining when introduced into existing repositories.

Example:

```text
Existing 120 Findings
        ↓
Baseline
        ↓
No New Findings Allowed
```

Baselines allow progressive adoption.

They must not permanently legitimize quality debt.

---

# Baseline Fingerprints

Individual findings may require stable fingerprints to distinguish:

```text
Existing Finding
```

from:

```text
New Finding
```

Fingerprinting may use:

* rule ID;
* path;
* symbol;
* location;
* normalized message.

Implementation must balance stability with accuracy.

---

# Rule Metrics

Rules may produce metrics in addition to pass/fail results.

Examples include:

```text
coverage = 92%
complexity = 14
latency = 180ms
vulnerability_count = 2
```

Metrics can support trends and threshold-based rules.

---

# Rule Trend Analysis

Historical rule results can reveal systemic changes.

Example:

```text
QLT-RULE-ARC-001

Month 1 → 0 findings
Month 2 → 2 findings
Month 3 → 8 findings
```

This trend may indicate architecture degradation even if individual findings remain non-blocking.

---

# Rule Aggregation

Rules may contribute to higher-level assessments.

Example:

```text
QLT-RULE-TST-001 PASS
QLT-RULE-TST-002 PASS
QLT-RULE-TST-003 WARNING
        ↓
Testing Domain Assessment
```

Aggregation logic belongs to the assessment layer, not the rule itself.

---

# Rule and Gate Separation

Rules determine compliance with specific expectations.

Gates determine whether engineering progression is permitted.

Therefore:

```text
Rule
    ↓
Evidence / Finding

Gate
    ↓
Decision
```

This separation allows the same rule to behave differently at different lifecycle stages.

---

# Example Rule Definition

A conceptual rule may be represented as:

```text
id: QLT-RULE-ARC-001
title: Cross-domain internal dependencies are forbidden
domain: Architecture
requirement: QLT-REQ-ARC-001
severity: HIGH
execution_type: AUTOMATED
status: ACTIVE
scope: Python packages
blocking: CONDITIONALLY_BLOCKING
```

Its condition may be:

```text
A domain package must not import internal implementation
symbols from another domain package outside approved public contracts.
```

---

# Example Rule Evaluation

```text
Target:
src/familyos_cli/plugins/builtin/finance

Rule:
QLT-RULE-ARC-001

Result:
FAIL

Finding:
Finance plugin imports internal repository implementation
from the Documents plugin.

Severity:
HIGH
```

The finding may then participate in a Merge Gate or Release Gate.

---

# Example Documentation Rule

```text
id: QLT-RULE-DOC-001
title: Required EPIC control documents must exist
domain: Documentation
severity: HIGH
execution_type: AUTOMATED
```

Applicable targets may require:

```text
EPIC.yaml
README.md
MANIFEST.md
CHANGELOG.md
VALIDATION.md
```

Missing artifacts generate individual findings.

---

# Example Testing Rule

```text
id: QLT-RULE-TST-001
title: Required tests must pass
domain: Testing
severity: CRITICAL
execution_type: AUTOMATED
```

Condition:

```text
All tests selected by the active quality profile must complete successfully.
```

Infrastructure execution failure produces `ERROR`, not `FAIL`.

---

# Example Security Rule

```text
id: QLT-RULE-SEC-001
title: Critical known vulnerabilities are forbidden
domain: Security
severity: CRITICAL
```

The rule may produce one finding per affected dependency.

Release profiles may classify this rule as blocking.

---

# Rule Catalog

The framework should maintain a rule catalog.

The catalog provides discoverability for:

* engineers;
* automation;
* governance;
* documentation;
* quality reports.

The catalog may expose:

```text
Rule ID
Title
Domain
Status
Severity
Owner
Version
Applicable Profiles
```

---

# Machine-Readable Rule Definitions

Rules should eventually support machine-readable representation.

A machine-readable format enables:

* automated discovery;
* validation;
* profile composition;
* reporting;
* governance tooling.

Possible implementation formats may include YAML or another structured representation.

The exact serialization format is not normative at this architectural stage.

---

# Human-Readable Rule Documentation

Every significant rule should also remain understandable to humans.

Human-readable documentation should explain:

* purpose;
* rationale;
* scope;
* severity;
* examples;
* remediation;
* exceptions.

Machine-readable configuration alone is insufficient for governance quality.

---

# Rule Registry

The Quality Registry may maintain all active and historical rules.

Conceptually:

```text
Quality Registry
      ↓
Rule Catalog
      ├── Active
      ├── Experimental
      ├── Deprecated
      └── Retired
```

The registry enables rule resolution by identifier and version.

---

# Rule Discovery

The Quality Execution Engine should discover applicable rules through:

```text
Target
  +
Quality Profile
  +
Lifecycle Stage
  +
Configuration
        ↓
Applicable Rules
```

Discovery should be deterministic.

---

# Rule Selection

Rule selection must distinguish:

```text
Applicable
Enabled
Mandatory
Optional
Suppressed
Excepted
```

These states must not be conflated.

---

# Mandatory Rule Preservation

Specialized profiles may strengthen rules.

They must not silently remove mandatory baseline rules.

Example:

```text
Base Profile
    ↓
Mandatory Security Rule

Official Plugin Profile
    ↓
Mandatory Security Rule remains active
```

Removal, when ever allowed, requires explicit governance.

---

# Rule Configuration Validation

Invalid rule configuration must fail clearly.

Example:

```text
minimum_coverage: "high"
```

when a numeric value is expected must produce a configuration error.

The quality engine must not silently substitute arbitrary defaults.

---

# Rule Integrity

Rule definitions are part of quality infrastructure.

Unauthorized modifications to critical rules can undermine the entire assurance model.

Authoritative rule definitions should therefore be:

* version-controlled;
* reviewed;
* traceable;
* protected by normal engineering controls.

---

# Rule Auditability

A quality decision should be reconstructable from rule history.

For a past evaluation, FamilyOS should eventually be able to determine:

```text
Which rule version applied?

Which configuration applied?

Which provider executed it?

What evidence was generated?

Which findings resulted?
```

This is essential for release traceability and governance.

---

# Rule Change Impact

Rule changes may affect large portions of the platform.

Before activating significant changes, impact should be evaluated.

Questions include:

```text
How many new findings will appear?

Will existing profiles fail?

Will CI duration increase?

Will release gates change behavior?

Are repositories prepared for the new requirement?
```

This supports controlled adoption.

---

# Rule Rollout

Significant rules may use progressive rollout.

Example:

```text
DRAFT
  ↓
EXPERIMENTAL
  ↓
WARNING ONLY
  ↓
BLOCK NEW VIOLATIONS
  ↓
FULL ENFORCEMENT
```

Progressive rollout reduces disruptive framework changes.

---

# Rule Migration

When one rule replaces another, migration guidance should define:

* changed semantics;
* profile updates;
* configuration updates;
* baseline implications;
* expected remediation.

Rule migration must not invalidate historical evidence unnecessarily.

---

# Rule Compatibility

Machine-readable rule contracts may eventually become dependencies for:

* CI;
* plugins;
* dashboards;
* compliance tools;
* release automation.

Changes to these contracts must consider compatibility.

---

# Rule Governance Events

The framework may emit events for rule lifecycle changes.

Examples:

```text
quality.rule.created
quality.rule.activated
quality.rule.updated
quality.rule.deprecated
quality.rule.retired
```

Such events may support auditing and automation.

---

# Rule Quality

Rules themselves have quality requirements.

A poor quality rule may be:

* ambiguous;
* noisy;
* slow;
* unreliable;
* difficult to remediate;
* impossible to reproduce.

The framework must therefore evaluate rule quality.

---

# Rule Quality Criteria

An active rule should ideally satisfy:

```text
Clear Intent
Precise Scope
Reliable Detection
Acceptable Performance
Actionable Findings
Stable Semantics
Documented Ownership
Traceable Requirement
```

Rules that consistently fail these criteria should be improved or retired.

---

# Rule Effectiveness

Rule effectiveness should be evaluated over time.

Possible indicators include:

* number of meaningful defects prevented;
* false-positive rate;
* suppression frequency;
* exception frequency;
* remediation time;
* execution cost.

A rule that generates persistent noise without meaningful value should be reconsidered.

---

# Rule Observability

The quality system should eventually expose operational information about rules.

Examples:

```text
Execution Count
Failure Rate
Average Duration
Error Rate
Finding Volume
Suppression Count
Exception Count
```

These metrics help maintain the quality infrastructure itself.

---

# AI-Assisted Rule Analysis

AI may assist with:

* rule documentation;
* finding explanation;
* remediation suggestions;
* pattern analysis;
* proposed rule discovery.

However, AI must not autonomously redefine authoritative rule semantics.

Any rule change must remain governed and reviewable.

---

# Rule Anti-Patterns

The Quality Rule Model rejects several patterns.

## Tool-Named Rules

Avoid:

```text
Ruff must pass
```

Prefer:

```text
Python source must satisfy configured static analysis requirements
```

## Monolithic Rules

Avoid:

```text
Repository must be high quality
```

Rules must address specific concerns.

## Hidden Rules

Mandatory quality behavior must not exist only inside CI scripts.

## Unowned Rules

Every active authoritative rule requires ownership.

## Permanent Suppressions

Suppression must not become invisible technical debt.

## Unversioned Semantic Changes

Rule behavior must not change materially without traceability.

## Silent Evaluation Errors

Execution failure must never imply compliance.

---

# Reference Rule Flow

The complete rule flow can be represented as:

```text
Quality Requirement
        ↓
Quality Rule
        ↓
Applicability
        ↓
Rule Configuration
        ↓
Execution Provider
        ↓
Rule Evaluation
        ↓
Evidence
        ↓
Finding / Metric
        ↓
Assessment
        ↓
Quality Gate
        ↓
Decision
```

This model preserves clear responsibility at every stage.

---

# Strategic Outcome

The Quality Rule Model transforms FamilyOS quality requirements from descriptive guidance into governed engineering constraints.

It enables FamilyOS to answer:

```text
Which rule applies?

Why does it exist?

What target does it evaluate?

How is it verified?

Which version was used?

What evidence was generated?

What happens when it fails?

Can an exception apply?
```

These questions are essential for scalable quality automation and governance.

---

# Final Rule Principle

A quality rule must make an engineering expectation executable without making it obscure.

Every authoritative rule must preserve a clear connection between:

```text
Intent
  ↓
Requirement
  ↓
Rule
  ↓
Verification
  ↓
Evidence
```

The FamilyOS Quality Rule Model therefore establishes the normative structure required to make quality requirements explicit, repeatable, traceable, automatable, explainable, and governable throughout the complete FamilyOS engineering lifecycle.

---

## Phase 2 Runtime Rule and Status Contract

This section reconciles the normative Quality Rule Model with the initial
machine-readable Quality domain implementation.

### Canonical Quality Severity

`QualitySeverity` SHALL expose exactly the following initial values:

```text
INFO
LOW
MEDIUM
HIGH
CRITICAL
```

Severity expresses the significance of a quality concern. It MUST NOT itself
decide gate behavior or progression policy.

### Canonical Quality Status

`QualityStatus` SHALL expose exactly the following initial values:

```text
PASS
WARNING
FAIL
ERROR
SKIPPED
UNKNOWN
```

The status semantics are:

- `PASS` — evaluation completed successfully and the evaluated condition was
  satisfied.
- `WARNING` — evaluation completed and identified a non-blocking concern.
- `FAIL` — evaluation completed successfully and identified a quality
  violation.
- `ERROR` — the evaluation mechanism could not produce a reliable conclusion.
- `SKIPPED` — evaluation was intentionally not executed.
- `UNKNOWN` — available information is insufficient to determine the quality
  state.

The following distinctions are normative:

- `ERROR` MUST NOT be collapsed into `FAIL`.
- `UNKNOWN` MUST NOT be interpreted as `PASS`.
- `SKIPPED` MUST remain distinct from `UNKNOWN`.
- `WARNING` is the canonical Quality status spelling.

Existing uses of `WARN` that describe an enforcement mode, lifecycle phase,
profile behavior, or another semantically distinct policy concept are not
renamed by this contract.

### Runtime Quality Identifiers

Runtime identifiers SHALL preserve the governed FamilyOS Quality namespaces
already established by the normative framework and SHALL remain compatible
with the canonical FamilyOS identifier specification.

The initial namespaces include:

```text
QLT-DOM-*
QLT-REQ-*
QLT-RULE-*
QLT-FIND-*
```

Phase 2 MUST NOT invent a competing identifier convention.

This contract authorizes only the core model vocabulary governed by the Core
Domain Models phase. It does not authorize Quality Evidence implementation,
tool adapters, assessment execution, profiles, CLI integration, CI integration,
or quality gates.
