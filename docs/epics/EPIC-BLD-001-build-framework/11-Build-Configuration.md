# Build Framework

# 11 Build Configuration

## Overview

EPIC-BLD-001 — Build Framework defines how FamilyOS build configuration is declared, resolved, validated, versioned, applied, observed, and governed.

Build configuration controls how controlled engineering inputs are transformed into artifacts.

Configuration may influence:

* build targets;
* build profiles;
* dependency selection;
* generation behavior;
* packaging behavior;
* validation stages;
* artifact output;
* environment assumptions;
* automation behavior;
* evidence requirements.

Because configuration can materially change build behavior, it is part of the effective build context.

The central principle is:

> Build configuration must be explicit enough that FamilyOS can explain why a build behaved the way it did.

---

# Purpose

The purpose of the Build Configuration model is to prevent critical build behavior from being distributed across hidden defaults, environment variables, CI-specific overrides, local scripts, and undocumented conventions.

The framework defines how configuration should remain:

* explicit;
* discoverable;
* version-controlled where practical;
* validated;
* deterministic;
* layered;
* traceable;
* profile-aware;
* automation-compatible;
* secure;
* governable.

---

# Build Configuration Definition

Build configuration is any controlled state that influences how a build executes.

Conceptually:

```text
Build Configuration
        ↓
Resolved Build Behavior
        ↓
Build Execution
        ↓
Artifact Outcome
```

Configuration is therefore not merely operational metadata.

It is part of the transformation contract.

---

# Configuration Categories

FamilyOS build configuration may be classified into several categories.

```text
Build Configuration
│
├── Project Configuration
├── Build Configuration
├── Tool Configuration
├── Profile Configuration
├── Environment Configuration
├── Artifact Configuration
├── Validation Configuration
├── Automation Configuration
└── Policy Configuration
```

The categories may share physical configuration files.

Their conceptual responsibilities should remain clear.

---

# Project Configuration

Project configuration defines general project-level metadata and engineering settings.

Examples may include:

* project identity;
* package metadata;
* supported runtime;
* dependency declarations;
* packaging configuration;
* tool settings.

For Python-based FamilyOS components, this may be represented through `pyproject.toml`.

---

# Build-Specific Configuration

Build-specific configuration controls the build lifecycle itself.

Examples include:

* build target;
* build profile;
* generation settings;
* output location;
* artifact selection;
* validation level;
* evidence level.

The exact representation may evolve.

---

# Tool Configuration

Tool configuration defines how individual build or validation tools behave.

Examples include configuration for:

* build backend;
* package builder;
* Ruff;
* MyPy;
* Pytest;
* documentation generators;
* compliance validators.

Tool configuration is part of effective toolchain behavior.

---

# Profile Configuration

Build profiles group related configuration for a specific execution purpose.

Possible profiles include:

```text
development
validation
ci
documentation
plugin
release-candidate
```

Each profile may specialize the canonical build configuration.

---

# Environment Configuration

Environment configuration adapts canonical behavior to execution context.

Examples may include:

* environment-specific paths;
* CI identifiers;
* controlled external endpoints;
* infrastructure settings.

Environment configuration must not silently redefine core build semantics.

---

# Artifact Configuration

Artifact configuration defines what the build produces.

It may include:

* artifact type;
* package metadata;
* artifact name;
* output directory;
* included resources;
* generated manifests;
* metadata requirements.

---

# Validation Configuration

Validation configuration defines which checks apply before an artifact becomes trusted.

Examples include:

* static validation requirements;
* test requirements;
* package validation;
* plugin compliance checks;
* documentation validation.

Validation configuration should remain aligned with Testing and Quality frameworks.

---

# Automation Configuration

Automation configuration defines how build execution integrates with CI or other automated systems.

Automation configuration may specify:

* trigger context;
* execution adapter;
* environment setup;
* artifact collection;
* evidence retention.

It must not become an independent source of canonical build semantics.

---

# Policy Configuration

Policy configuration controls governance rules affecting build validity.

Examples may include:

* quality gates;
* security rules;
* dependency restrictions;
* plugin compliance requirements;
* release-candidate requirements.

Policy configuration must remain traceable to the framework that owns the policy.

---

# Configuration Principle 1 — Configuration Must Be Explicit

Significant build configuration SHOULD be explicitly represented.

The framework rejects:

```text
Hidden Default
      ↓
Undocumented Behavior
```

The preferred model is:

```text
Declared Configuration
        ↓
Resolved Behavior
```

---

# Configuration Principle 2 — Configuration Must Be Discoverable

An engineer should be able to determine where build behavior is configured.

Configuration should not require searching through:

* personal shell files;
* hidden CI variables;
* random scripts;
* undocumented environment state.

---

# Configuration Principle 3 — Configuration Should Be Version Controlled

Configuration that affects canonical build behavior SHOULD be version controlled where practical.

This includes:

* package configuration;
* dependency declarations;
* build profiles;
* tool configuration;
* validation rules;
* generation settings.

Version control provides:

* history;
* reviewability;
* traceability;
* rollback.

---

# Configuration Principle 4 — Configuration Must Be Validated

Configuration must not be accepted solely because it is syntactically readable.

Validation should include:

```text
Syntax
  ↓
Structure
  ↓
Semantics
  ↓
Compatibility
  ↓
Policy
```

Invalid configuration must prevent trusted build execution.

---

# Configuration Principle 5 — Precedence Must Be Defined

If multiple configuration layers can define the same setting, precedence must be explicit.

A conceptual model may be:

```text
Framework Defaults
        ↓
Repository Configuration
        ↓
Profile Configuration
        ↓
Explicit Invocation Override
```

Environment overrides should be used only when appropriate.

---

# Configuration Principle 6 — Effective Configuration Must Be Understandable

The build should be able to determine the final resolved configuration before execution.

The conceptual relationship is:

```text
Multiple Configuration Sources
           ↓
Resolution
           ↓
Effective Build Configuration
```

The effective state should be inspectable where practical.

---

# Configuration Principle 7 — Configuration Must Not Hide Architecture

Configuration should parameterize architecture.

It should not replace architecture.

The anti-pattern is a large configuration system that implicitly defines:

* build lifecycle;
* trust model;
* release rules;
* artifact semantics;

without corresponding architectural documentation.

---

# Configuration Principle 8 — Configuration Must Remain Minimal

Configuration should only exist where it controls meaningful behavior.

Unnecessary options increase:

* complexity;
* testing requirements;
* failure surface;
* documentation burden.

The preferred rule is:

```text
No Meaningful Variability
        ↓
No Configuration Option
```

---

# Configuration Principle 9 — Defaults Must Be Safe

Defaults should represent safe and predictable behavior.

A default must not:

* disable required validation;
* enable insecure behavior;
* publish artifacts;
* expose secrets;
* change release state.

Risk-sensitive behavior should require explicit selection.

---

# Configuration Principle 10 — Build Profiles Must Be Explicit

A build profile should not be inferred from vague environment conditions.

The target is:

```text
Explicit Profile Selection
        ↓
Known Configuration Set
```

This improves reproducibility.

---

# Configuration Source Model

The canonical configuration source model may be represented as:

```text
Configuration Sources
│
├── Framework Defaults
├── Repository Configuration
├── Component Configuration
├── Profile Configuration
├── Invocation Parameters
└── Controlled Environment Inputs
```

The implementation may use fewer layers.

---

# Current Implemented Configuration Contract

The current FamilyOS package build does not use a single monolithic build-
configuration file. Its configuration authority is intentionally divided
between repository declarations, typed Build Framework policy, supported
invocation parameters, fixed application wiring, and observed execution state.

The implemented flow is:

```text
Canonical Repository Authorities
            +
Typed Framework Policy And Defaults
            +
Explicit Supported Invocation Overrides
            +
Observed Execution State
            ↓
BuildContextResolver
            ↓
BuildContext
            +
BuildEffectiveConfiguration
```

This is a combined authority, not a precedence chain in which every source may
override every other source. Each source owns a bounded category of state.

## Canonical Configuration Authorities

| Authority | Current responsibility | Not its responsibility |
|---|---|---|
| `pyproject.toml` | Project and package metadata, Python compatibility, direct dependency declarations, build backend requirements, setuptools package discovery and package-data configuration, and the applicable Ruff, MyPy, and Pytest tool configuration | Runtime invocation values such as profile, output directory, functional validation, or evidence output |
| `requirements.txt` | Generated, controlled Python 3.13 development/CI dependency resolution and dependency-constraint state | Independently hand-authored project declarations or arbitrary build configuration |
| `BuildProfile` registry | Supported profile contracts for `development`, `validation`, `ci`, and `release-candidate` | Project metadata, dependency resolution, or unrestricted user-defined profiles |
| `BuildTarget` registry | Supported target contract for `familyos-cli-package`, including required inputs and expected artifact classes | Arbitrary target discovery or user-defined target configuration |
| `familyos build` invocation | The supported per-invocation profile, output directory, functional-validation request, and evidence-output request | Replacement of canonical repository metadata, dependency state, profile definitions, or target definitions |
| Application bootstrap/container | Repository-root derivation and wiring of the package builder, artifact discoverer and validators, functional validator, source-state provider, and build-input validator | Arbitrary user configuration |
| Build Context providers | Observation of source, dependency, installed toolchain, runtime, platform, virtual-environment, filesystem-encoding, and temporary-directory state | User-provided semantic overrides |
| `PythonPackageBuilder` | Fixed canonical package-construction command and subprocess boundary | A selectable build frontend, backend, distribution sequence, or publication mechanism |
| `.github/workflows/ci.yml` | Explicit CI provisioning and invocation of canonical validation and package-build entry points | An independent source of FamilyOS package-build semantics |

`pyproject.toml` is therefore the canonical project declaration authority, but
it is not the complete runtime invocation authority. `requirements.txt` is
generated from canonical dependency inputs through
`scripts/compile_dependencies.py`; it records controlled resolution rather than
competing with `pyproject.toml` as a hand-edited source.

The typed profile and target registries are code-owned Build Framework policy.
They provide a closed set of supported values. The current implementation does
not load another YAML, TOML, environment, or dictionary-based Build Framework
configuration namespace.

## Invocation Configuration

The public package-build command currently supports exactly these invocation
settings:

| Setting | CLI form | Meaning |
|---|---|---|
| Profile | `--profile` | Select one canonical `BuildProfile` |
| Package output | `--output-dir` | Select the directory receiving package candidates |
| Functional validation | `--functional-validation` | Request installation/import/CLI validation of the discovered wheel after structural validation |
| Evidence output | `--evidence-output` | Request JSON Build Evidence after a successful build |

Typer rejects an unsupported profile value before application execution.
Target selection is available to the typed application use-case API but is not
currently exposed as a public CLI option.

Invocation configuration does not mutate `pyproject.toml`,
`requirements.txt`, or the typed registries. Evidence-output selection does not
implicitly select a profile, and profile selection is not inferred from an
environment variable or CI-provider context.

## Current Configuration Precedence

The current model applies precedence only where more than one supported source
can supply the same setting.

| Setting | Source or default | Explicit override | Final resolved authority | Current conflict or rejection behavior |
|---|---|---|---|---|
| Repository/project root | Application bootstrap derives the repository root from the installed application location | No public CLI override; constructors accept an explicit root for composition and tests | `RunPackageBuildUseCase` and `BuildContextResolver` | Git source authority is accepted only when this path is the exact Git repository root |
| Target | `BuildTarget.FAMILYOS_CLI_PACKAGE` | Typed application API only | `BuildTarget` plus `BuildTargetDefinition` | Unknown targets fail registry lookup; unsupported profile/target combinations fail before context resolution |
| Profile | `BuildProfile.DEVELOPMENT` | `--profile` or typed application API | `BuildProfile` captured in `BuildContext` | Unknown CLI values are rejected; supported-target compatibility is validated |
| Output directory | CLI default `Path("dist")` | `--output-dir` or required application argument | Repository-root-resolved `BuildContext.output_dir` for the canonical public command | Relative values resolve from the repository root; repository root, authoritative directories, and authoritative root files are rejected |
| Functional validation | Disabled | `--functional-validation` or typed boolean application argument | `BuildEffectiveConfiguration.functional_validation` | The boolean controls whether functional wheel validation executes; it is not currently reconciled with profile policy |
| Evidence output | Absent | `--evidence-output` or typed application argument | Repository-root-resolved `BuildContext.evidence_output` | Relative values resolve from the repository root; authoritative repository content, package-output overlap, and directory destinations are rejected; `ci` and `release-candidate` reject an absent destination |
| Runtime and critical toolchain | Runtime requirement and tool requirements derived from `pyproject.toml`; versions observed from the active interpreter environment | No public override; providers may be injected internally | Validated runtime version and `ToolchainState` captured in `BuildContext` | Missing, malformed, incompatible, or undeclared critical tool policy prevents package execution |
| Dependency state | Fixed `pyproject.toml` declaration and generated `requirements.txt` lock | None | `DependencyState` captured in `BuildContext` | Missing inputs or stale generated dependency state prevent canonical execution |
| Environment state | Current runtime/platform observations | No public override; provider injection is internal | `EnvironmentState` captured in `BuildContext` | The current environment validator requires an available temporary directory; broader profile environment requirements are not yet enforced |

An explicit supported invocation value takes precedence over its interface
default. Repository authorities and typed registry definitions are not
overridden by invocation values. Observed execution state is captured after
the request has been selected; it is evidence about the execution context, not
a higher-precedence source of semantic configuration.

Package-output and evidence-output paths now share one deterministic relative-
path authority: `BuildContextResolver` resolves both against the canonical
repository root. Process working directory therefore does not change either
effective destination. Evidence output remains a file destination owned by
the CLI renderer rather than a `BuildEffectiveConfiguration` field; its
resolved path is a first-class `BuildContext` field so the application gate
can enforce profile and repository-layout policy before package construction.
Equivalent relative, absolute, and normalized path forms therefore project to
the same effective configuration.

## Current Framework Defaults

The current defaults proven by the public interface and application use case
are:

```text
profile                 development
target                  familyos-cli-package
package output          dist
functional validation   disabled
evidence output          absent
```

The development-profile and disabled-functional-validation defaults appear at
adjacent CLI/helper/application boundaries and currently agree. The package
output default is also represented twice: the CLI exposes `Path("dist")`, while
`RepositoryLayout.default_output_dir` represents `<project-root>/dist`.
Resolution currently makes those representations equivalent, but their
duplication is an implementation limitation rather than a new precedence
layer.

The target default is owned by the application use case because no public
target option exists. Evidence is written only when an explicit evidence path
is supplied. Selecting `ci` or `release-candidate` does not invent a default
path; the absent default instead conflicts with those profiles' typed
`evidence_required=True` policy and is rejected before package construction.

## Bootstrap And Fixed Infrastructure Policy

The application bootstrap wires the current repository-owned build adapters.
This dependency injection supports architectural separation and testing; it is
not an unrestricted user configuration surface.

For the canonical Python package target, fixed infrastructure policy includes:

* the active `sys.executable` as the canonical Python executable;
* `python -m build` as the package frontend;
* the absolute repository `requirements.txt` path supplied through
  `--dependency-constraints-txt`;
* `--outdir` set to the resolved package-output directory;
* repository root as subprocess working directory;
* no wheel-only or sdist-only flag, preserving pypa/build's wheel-from-sdist
  behavior;
* discovery of exactly one wheel and one source distribution with rejection of
  unexpected direct outputs;
* mandatory structural package validation for the current target;
* no publishing or upload operation.

These are fixed implementation semantics, not invocation overrides.

## Configuration Versus Observed State

`BuildContextResolver` combines selected configuration with state observed for
one execution. The distinction is:

```text
Selected Configuration
├── profile
├── target
├── output directory
├── evidence-output destination
└── functional-validation request

Observed State
├── source revision and working-tree state
├── dependency declaration and lock digests
├── installed critical toolchain versions
├── runtime version
├── operating system and architecture
├── virtual-environment state
├── filesystem encoding
└── temporary-directory state
```

Observed state may determine whether execution is permitted, but it is not
equivalent to a user-provided configuration override. Provider injection at an
internal composition or test boundary does not create a public configuration
source.

## Current Profile Contract And Enforcement

All four profile definitions are immutable and declare purpose, supported
targets, validation scope, whether evidence is required, environment
requirements, and artifact expectations.

| Profile | Defined policy | Currently enforced by selecting the profile |
|---|---|---|
| `development` | Everyday local engineering, essential dependency and basic build/artifact checks, no required evidence, practical local isolation | Profile existence, support for `familyos-cli-package`, and capture of the selected profile in Build Context and optional evidence |
| `validation` | Ruff, MyPy, Pytest, packaging and structural checks under a controlled validation environment, no required evidence | Profile existence, target compatibility, and profile capture; selecting it on `familyos build` does not itself execute Ruff, MyPy, or Pytest |
| `ci` | Canonical environment, static validation, tests, build, artifact validation, and required standard evidence | Profile existence, target compatibility, profile capture, required explicit evidence destination, and correct evidence-profile identity; the repository CI workflow separately performs canonical validation and supplies the evidence destination |
| `release-candidate` | Source, configuration, dependency, toolchain, environment, execution, artifact, integrity, evidence, and release-readiness controls with required stronger evidence | Profile existence, target compatibility, profile capture, required explicit evidence destination, and correct evidence-profile identity; clean-workspace, complete validation, and release-readiness remain outside the current typed execution policy |

`profile` identity and `supported_targets` are executable typed policy already
consumed before Build Context resolution and revalidated by the final gate.
`evidence_required` is executable typed policy: the final gate rejects a
resolved `ci` or `release-candidate` context without an explicit evidence
destination. `purpose`, `validation_scope`, `environment_requirements`, and
`artifact_expectations` remain descriptive policy only. Their strings are
validated as documentation-bearing contract data and are not parsed into
runtime rules.

Likewise, `BuildTargetDefinition.required_inputs` participates in build-input
validation. Other target policy is currently implemented through the single
canonical package pipeline rather than selected dynamically from every target
definition field.

## Environment-Variable Boundary

The current canonical package-build path has no generic `FAMILYOS_*`
environment-variable mechanism for overriding profile, target, output,
validation, evidence, dependency, or toolchain semantics.

Before package construction, `PythonPackageBuilder` copies the parent
environment and removes:

```text
PYTHONHOME
PYTHONPATH
PYTHONSTARTUP
PYTHONUSERBASE
VIRTUAL_ENV
__PYVENV_LAUNCHER__
TWINE_USERNAME
TWINE_PASSWORD
UV_PUBLISH_USERNAME
UV_PUBLISH_PASSWORD
UV_PUBLISH_TOKEN
```

It then sets:

```text
PYTHONNOUSERSITE=1
```

The first group prevents inherited Python interpreter and virtual-environment
state from silently changing isolated package construction. The Twine and UV
publication variables are removed because package construction has no
publication responsibility.

The environment is not an allowlist. Ordinary variables, including networking,
proxy, certificate, locale, and external-tool compatibility state, may still
propagate. This permits legitimate dependency retrieval but means that
external-tool influence is not completely eliminated.

Additional current environment influence includes:

* Git source-state subprocesses inherit the ambient environment, so Git-specific
  variables can affect Git behavior;
* operating-system temporary-directory selection influences the observed
  temporary directory and functional-validation workspace;
* canonical validation subprocesses inherit the environment in which the
  FamilyOS command executes.

These are environment and tool-execution boundaries, not supported FamilyOS
semantic override keys. They remain subject to later control where their
influence proves material.

## Secret Separation Contract

Secrets are not Build Configuration.

`BuildContext` and `BuildEffectiveConfiguration` are typed, non-sensitive
models. They must not become arbitrary containers for credentials, tokens,
private keys, or publication authority. Current Build Evidence does not
serialize arbitrary environment variables.

Package construction requires no publication credential. Common Twine and UV
publication variables are removed from the canonical package-build subprocess.
Publication credentials belong to downstream Release Framework publication
concerns and must remain separate from ordinary package-build semantic
configuration.

This is not a claim that every possible ambient secret name is identified or
that the subprocess environment is a complete allowlist. It defines the
configuration ownership boundary and records the current verified sanitation.

## Unknown Critical Settings

The current Build Framework configuration surface is closed and typed:

* Typer rejects unknown CLI options and unsupported profile values;
* profile and target selection use enums and fixed registries;
* there is no generic Build Framework configuration dictionary, `**kwargs`
  extension surface, or user-defined build-configuration namespace;
* `pyproject.toml` tool namespaces remain governed by their owning tools.

Unknown critical Build Framework settings therefore cannot silently enter the
currently supported configuration model. If a future extensible configuration
schema is introduced, it must add explicit unknown-key handling rather than
weakening this closed surface.

## Final Effective-Configuration Validation

Canonical package-build execution now validates the final resolved
configuration after `BuildContextResolver` returns and before the package
builder runs. `EffectiveConfigurationValidator` receives the exact
`BuildContext` later used by execution, the canonical resolved
`BuildProfileDefinition`, and the already-established package-output and
evidence-output repository-layout validation results. It does not resolve
another context, recapture observed state, or duplicate repository path rules.

The current final gate deterministically verifies that the resolved profile
matches its canonical definition, the resolved target is supported by that
profile, the effective functional-validation setting remains a boolean, and
the established output-layout decision succeeded. It also enforces the typed
required-evidence policy and the established evidence-path safety decision. A
failure prevents package transformation while preserving the resolved Build
ID, source state, and Build Context in the pre-execution result.

Evidence destinations are resolved in Build Context but evidence serialization
remains at the CLI boundary. The final gate does not interpret descriptive
profile strings or invent clean-workspace, release-readiness, or severity
policy.

## Conflict And Validation-Bypass Policy

The current typed configuration surface rejects the material conflicts it can
represent:

* an unsupported profile/target pair;
* a profile requiring evidence with no explicit evidence destination;
* package output that conflicts with the repository root, authoritative
  directories, or authoritative build-control files;
* evidence output that replaces authoritative build-control files, overlaps
  authoritative directories or the package-output tree, targets the repository
  root, or names an existing directory;
* malformed non-boolean functional-validation state at the typed application
  boundary.

Repeated CLI spelling does not introduce two surviving authorities: Typer
resolves the closed option surface to one typed value before application
execution. An explicitly selected evidence file may replace an earlier file at
that same evidence destination; that is the requested output operation, not a
conflict with canonical source or package artifacts.

Mandatory package-build integrity stages are not selectable configuration.
Build-input, repository-layout, toolchain, environment, final effective-
configuration, artifact discovery, structural package validation, artifact
identity/integrity, and manifest construction have no supported disable
switch. `BuildInputValidator` is now instantiated by default even for direct
application composition, so passing no validator no longer bypasses required
input and dependency-freshness validation. Adapter injection remains a
composition/test seam rather than a public build setting.

Functional wheel validation remains intentionally optional and its selected
boolean remains visible in `BuildEffectiveConfiguration`. Canonical CI
validation is a separate repository-owned automation command executed before
the CI package build; free-form profile `validation_scope` text is not treated
as an in-process policy parser. Downstream release qualification likewise
remains outside this package-build configuration gate.

## Effective Configuration Inspectability

`EffectiveBuildConfigurationView` is the immutable inspection projection of
one already-resolved `BuildContext` and its canonical
`BuildProfileDefinition`. It is derived state, not another configuration
authority or resolver. The projection exposes exactly:

* selected profile and target;
* resolved package-output directory;
* functional-validation selection;
* resolved optional evidence destination and whether evidence was requested;
* the profile's typed `evidence_required` policy;
* whether the selected target is supported by that profile.

Successful and pre-execution-failure CLI rendering uses this projection. It
reports the resolved local package and evidence paths plus explicit
`Evidence Required`, `Evidence Requested`, and `Profile Supports Target`
decisions. These local paths are appropriate for operator inspection but are
not portable evidence identities.

Every `BuildEvidence` instance also carries the derived projection. Its JSON
renderer emits a compact `effective_configuration` object containing profile,
target, functional-validation, evidence-required, evidence-requested, and
target-supported values. Package-output and evidence-output paths are omitted
from JSON so equivalent builds in different checkout roots remain portable.
The evidence model rejects a projected build profile that disagrees with the
typed validation profile.

Source state, dependency digests, installed toolchain versions, runtime and
platform details, and temporary-directory state remain observations rather
than effective configuration. The CLI may render those observations beside
configuration, and Build Evidence may record them through their own evidence
authorities, but the inspection projection does not mix them into
configuration. It contains no environment-variable map, credentials, tokens,
or publication secrets.

## Current Implementation Limits

The completed Level 12 contract retains these deliberate limits:

* `BuildEffectiveConfiguration` currently contains only the functional-
  validation boolean; the derived inspection view combines it with existing
  first-class `BuildContext` and profile-policy fields without duplicating
  their authority;
* descriptive profile `validation_scope`, `environment_requirements`, and
  `artifact_expectations` are not executable runtime policy;
* Git and other permitted external-tool environment influence is not completely
  controlled;
* aligned defaults are duplicated at some adjacent code boundaries, including
  the `dist` output representation.

These limits do not create an additional configuration source or leave the
Level 12 effective-resolution contract ambiguous. Broader profile semantics,
external-tool control, and default-authority consolidation require their own
typed policy decisions rather than interpretation by the configuration view.

## Current Configuration Resolution Acceptance Contract

Under the current architecture, "same configuration inputs" means:

* the same canonical repository declarations relevant to the selected target;
* the same typed profile and target registry definitions;
* the same explicitly selected profile and target;
* the same explicit package-output, evidence-output, and functional-validation
  inputs after documented path resolution;
* the same applicable framework defaults and fixed bootstrap wiring.

For inputs currently represented by `BuildContextResolver`, the acceptance
target is:

```text
Equivalent Deterministic Configuration Inputs
                    ↓
Same Resolved Profile, Target, Output, And Effective Options
```

Source revision, working-tree state, dependency digests, installed tool
versions, runtime patch version, platform state, and temporary-directory state
are observations. Equivalent configuration does not require two builds to have
identical observations or identical complete `BuildContext` objects.

Evidence-output selection is resolved into `BuildContext.evidence_output`.
Equivalent relative and absolute destinations resolve identically, and a
change in process working directory does not alter the repository-relative
destination. The destination is intentionally not duplicated in
`BuildEffectiveConfiguration`; its requested state and typed requirement are
serialized without its machine-specific path.

The dedicated configuration-resolution matrix proves public defaults,
explicit overrides, normalized relative/absolute equivalence, all four
profile evidence policies, supported-target inspection, missing-evidence and
repository-path conflicts, working-directory independence, repeated
determinism, and rejection of unknown enum values. It also constructs contexts
with different Build IDs, source revisions, dependency digests, toolchain
versions, runtime versions, operating systems, and temporary directories and
proves that their equivalent deterministic inputs produce equal
`EffectiveBuildConfigurationView` values rather than equal complete contexts.

---

# Framework Defaults

Framework defaults define baseline behavior.

Defaults should be:

* stable;
* conservative;
* documented;
* overridable only where justified.

Defaults should not carry hidden platform-specific assumptions.

---

# Repository Configuration

Repository configuration is authoritative for project-wide build behavior.

This is the preferred location for:

* package metadata;
* dependency definitions;
* general build settings;
* tool configuration.

---

# Component Configuration

Individual components or plugins may require specialized configuration.

Component configuration should extend canonical rules rather than contradict them.

---

# Profile Configuration

Profile configuration specializes build behavior for a specific purpose.

For example:

```text
development
```

may prioritize feedback speed, while:

```text
release-candidate
```

may require stronger validation and evidence.

---

# Invocation Parameters

Explicit invocation parameters may temporarily override configuration.

Examples include:

* selected target;
* selected profile;
* output path;
* diagnostic verbosity.

Invocation parameters should not provide unrestricted access to bypass trust controls.

---

# Environment-Based Configuration

Environment values may provide context when configuration cannot reasonably be stored in the repository.

Examples include:

* CI build identifier;
* temporary workspace;
* external service endpoint;
* secret reference.

Environment configuration must remain constrained.

---

# Configuration Resolution

Configuration resolution combines all applicable sources into one effective state.

The canonical model is:

```text
Load Defaults
    ↓
Load Repository State
    ↓
Load Component State
    ↓
Apply Profile
    ↓
Apply Explicit Overrides
    ↓
Resolve Environment Context
    ↓
Validate
    ↓
Effective Configuration
```

---

# Configuration Resolution Determinism

Equivalent configuration sources should resolve to equivalent effective configuration.

Resolution order must not depend on:

* filesystem enumeration;
* shell ordering;
* undefined dictionary behavior;
* provider-specific CI semantics.

---

# Configuration Conflict

A conflict occurs when two configuration sources define incompatible values.

The framework should either:

* apply documented precedence;
* reject ambiguous state.

It should never choose silently through incidental implementation behavior.

---

# Effective Configuration

The effective configuration is the final build configuration used by execution.

Conceptually:

```text
EffectiveBuildConfiguration
│
├── Target
├── Profile
├── Dependency Settings
├── Tool Settings
├── Environment Settings
├── Artifact Settings
├── Validation Settings
└── Evidence Settings
```

The exact model may remain distributed across existing tooling initially.

---

# Configuration Identity

For trusted builds, FamilyOS may eventually associate configuration with an identifier or fingerprint.

A future configuration fingerprint could support:

* reproducibility;
* cache correctness;
* provenance;
* artifact comparison.

This is a maturity capability rather than an immediate universal requirement.

---

# Build Profiles

Profiles provide controlled specialization of the canonical build model.

A profile must have a documented purpose.

---

# Development Profile

The development profile may prioritize:

* fast execution;
* local iteration;
* lighter evidence;
* developer diagnostics.

It must not redefine canonical build semantics.

---

# Validation Profile

The validation profile may enable:

* static analysis;
* type checks;
* tests;
* structural validation;
* artifact checks.

Its purpose is engineering verification.

---

# CI Profile

The CI profile may require:

* known repository revision;
* fresh environment;
* standard validations;
* standard evidence;
* artifact collection.

---

# Documentation Profile

The documentation profile may enable:

* documentation generation;
* index creation;
* reference validation;
* documentation artifact production.

---

# Plugin Profile

The plugin profile may enable:

* plugin metadata validation;
* plugin compliance;
* plugin packaging;
* plugin artifact generation.

---

# Release Candidate Profile

The release-candidate profile should apply stronger controls.

Possible settings include:

* clean source requirement;
* locked dependencies;
* canonical toolchain;
* full validation;
* artifact integrity;
* strong evidence.

---

# Profile Inheritance

Profile inheritance should be used cautiously.

A deeply nested configuration hierarchy can become difficult to reason about.

The preferred model is shallow and explicit.

For example:

```text
Base
├── Development
├── CI
└── Release Candidate
```

is easier to understand than complex multi-level inheritance.

---

# Configuration Schema

As configuration complexity grows, FamilyOS may introduce explicit schemas.

Schemas can validate:

* required fields;
* allowed values;
* types;
* structural relationships.

A schema should be introduced only when it reduces real ambiguity.

---

# Configuration Validation

Configuration validation should occur before execution.

The validation flow may include:

```text
Parse
  ↓
Schema Check
  ↓
Semantic Check
  ↓
Compatibility Check
  ↓
Policy Check
```

---

# Syntax Validation

Syntax validation ensures the configuration can be parsed.

Examples include:

* TOML;
* YAML;
* JSON;
* structured Python configuration.

---

# Structural Validation

Structural validation ensures required configuration fields or sections exist.

---

# Semantic Validation

Semantic validation ensures values make sense.

For example:

```text
profile = "unknown-profile"
```

may parse correctly but be semantically invalid.

---

# Compatibility Validation

Compatibility validation checks interactions such as:

```text
Build Target
    +
Build Profile
    ↓
Supported?
```

or:

```text
Runtime
    +
Toolchain Configuration
    ↓
Compatible?
```

---

# Policy Validation

Policy validation confirms configuration does not bypass required platform controls.

For example:

* disabling mandatory release validation;
* using prohibited dependencies;
* omitting required plugin checks.

---

# Configuration Error Handling

Configuration failures should be explicit.

A useful failure should identify:

* configuration source;
* affected key;
* invalid value;
* reason;
* expected form.

---

# Configuration Failure Categories

Possible conceptual categories include:

```text
CONFIG_NOT_FOUND
CONFIG_SYNTAX_ERROR
CONFIG_SCHEMA_ERROR
CONFIG_SEMANTIC_ERROR
CONFIG_CONFLICT
CONFIG_UNSUPPORTED_VALUE
CONFIG_POLICY_VIOLATION
```

Formal machine-readable implementation may come later.

---

# Configuration And Reproducibility

Configuration is one of the principal contributors to reproducibility.

The relationship is:

```text
Known Configuration
       ↓
Known Build Semantics
       ↓
Reduced Variability
```

---

# Configuration And Determinism

Hidden defaults and environment-driven behavior reduce determinism.

Explicit resolution improves it.

---

# Configuration And Traceability

Trusted build evidence should eventually be able to identify the configuration state used.

This may include:

* profile;
* configuration revision;
* selected values;
* configuration fingerprint.

Sensitive values must be excluded.

---

# Configuration And Build Evidence

A build evidence bundle may conceptually include:

```text
Build Evidence
│
└── Configuration
    ├── Profile
    ├── Source References
    ├── Effective Options
    └── Fingerprint
```

The amount of detail depends on build profile.

---

# Configuration And Toolchain

Tool configuration is inseparable from tool behavior.

Therefore:

```text
Tool
  +
Tool Configuration
  ↓
Effective Toolchain Behavior
```

A tool version alone is insufficient evidence if behavior is heavily configuration-dependent.

---

# Configuration And Dependencies

Dependency selection may be configuration-dependent.

Examples include:

* optional dependency groups;
* plugin extras;
* build features.

Such relationships must remain explicit.

---

# Configuration And Environment

The framework should separate configuration from environment wherever practical.

The undesirable pattern is:

```text
Environment Variable
      ↓
Unknown Build Semantics
```

The preferred pattern is:

```text
Controlled Configuration
       +
Environment Context
       ↓
Explicit Resolution
```

---

# Configuration And Artifacts

Configuration may affect:

* artifact type;
* artifact naming;
* resource inclusion;
* metadata;
* generation;
* target platform.

Such configuration should be captured as part of artifact traceability where relevant.

---

# Configuration And Testing

Testing configuration remains governed primarily by the Testing Framework.

The Build Framework defines when testing configuration participates in build readiness.

---

# Configuration And Quality

Quality configuration may define:

* thresholds;
* required checks;
* gate behavior.

The Build Framework must consume these requirements without duplicating Quality Framework governance.

---

# Configuration And Plugins

Plugins may require configuration for:

* metadata;
* packaging;
* capabilities;
* compliance;
* optional features.

Plugin configuration must remain compatible with platform build rules.

---

# Configuration And Release

Release-candidate configuration may become part of the release handoff evidence.

The Release Framework may reject builds with unsupported configuration states.

---

# Configuration Secrets

Secrets require special treatment.

A secret must not be stored as ordinary build configuration.

Instead, configuration should reference a secret source where required.

For example:

```text
registry_credential = <secret reference>
```

rather than embedding the actual secret.

---

# Secret Configuration Rules

Secrets MUST:

* remain outside version control;
* avoid logs;
* avoid normal configuration dumps;
* avoid artifact embedding;
* be exposed only to required stages.

---

# Configuration Observability

Build diagnostics should make non-sensitive effective configuration understandable.

A future diagnostic command might expose:

```text
Target: ...
Profile: ...
Artifact Type: ...
Validation Mode: ...
Dependency Mode: ...
```

without revealing secrets.

---

# Configuration Inspection

Inspectability improves:

* debugging;
* reproducibility;
* governance;
* support.

The system should eventually allow engineers to answer:

```text
What configuration did this build actually use?
```

---

# Configuration Diff

Future tooling may support comparison between build configurations.

This may be useful when investigating why two builds differ.

For example:

```text
Build A Configuration
        ↓
      Diff
        ↑
Build B Configuration
```

This is a future diagnostic capability.

---

# Configuration Drift

Configuration drift occurs when:

* local configuration differs from canonical configuration;
* CI duplicates outdated settings;
* documentation describes obsolete values;
* environment overrides silently diverge.

Drift must be reduced.

---

# CI Configuration Drift

CI configuration is a frequent source of divergence.

The preferred model is:

```text
CI
 ↓
Invoke Canonical Build Configuration
```

not:

```text
CI
 ↓
Recreate Build Configuration Independently
```

---

# Local Configuration Drift

Local developer overrides should not become required for canonical build success.

If a local override becomes universally required, it should be promoted to canonical configuration.

---

# Configuration Duplication

The same semantic setting should not be independently duplicated across:

* project config;
* CI;
* scripts;
* documentation;
* environment variables.

Duplication creates synchronization debt.

---

# Configuration Normalization

Where multiple syntax forms exist, the build system may normalize them into an internal representation.

Conceptually:

```text
External Configuration
        ↓
Normalization
        ↓
Canonical Internal Configuration
```

This simplifies validation.

---

# Configuration Immutability During Build

Once effective configuration is resolved, it should remain stable during execution.

The preferred model is:

```text
Resolve
  ↓
Validate
  ↓
Freeze Effective State
  ↓
Execute
```

Dynamic mutation during a build makes traceability difficult.

---

# Configuration Caching

Configuration resolution may eventually be cached.

Cache reuse must depend on stable configuration identity.

Caching must not cause stale configuration to be applied.

---

# Configuration Change Management

Configuration changes should follow controlled engineering practice.

A typical change flow is:

```text
Requirement
   ↓
Configuration Change
   ↓
Validation
   ↓
Build
   ↓
Artifact Comparison
   ↓
Documentation
   ↓
Adoption
```

---

# Low-Risk Configuration Changes

Examples may include:

* diagnostic verbosity;
* non-semantic logging options.

These may require normal review only.

---

# High-Risk Configuration Changes

Examples include:

* dependency behavior;
* artifact inclusion;
* validation bypass;
* release profile behavior;
* security-sensitive settings.

These may require stronger governance.

---

# Configuration Deprecation

Obsolete configuration should be removed rather than maintained indefinitely.

A deprecation process may include:

* mark deprecated;
* document replacement;
* warn;
* remove after migration.

---

# Unknown Configuration

Unknown configuration keys should normally fail or warn explicitly.

Silently ignoring misspelled critical settings can produce dangerous assumptions.

---

# Backward Compatibility

Build configuration changes may affect:

* developers;
* CI;
* plugins;
* release workflows.

Breaking configuration changes must be deliberate and documented.

---

# Configuration Migration

When configuration structure changes, migration should be explicit.

A migration may include:

* old-to-new mapping;
* transition period;
* validation of deprecated keys;
* documentation updates.

---

# Configuration Ownership

Configuration ownership should reflect responsibility.

Conceptually:

```text
Project Metadata
      → Engineering Ownership

Build Profiles
      → Build Framework Ownership

Quality Gates
      → Quality Governance

Plugin Rules
      → Plugin Governance

Release Settings
      → Release Governance
```

The Build Framework should not absorb ownership of every configuration domain.

---

# Configuration Governance

Significant configuration model changes may require architectural review.

Examples include:

* introducing a new configuration hierarchy;
* changing precedence;
* introducing dynamic remote configuration;
* changing release-candidate semantics;
* introducing policy-driven configuration.

---

# Configuration Technical Debt

Configuration debt includes:

* obsolete keys;
* duplicate settings;
* undocumented defaults;
* conflicting files;
* excessive environment variables;
* abandoned profiles;
* CI-specific configuration forks.

This debt should be reduced continuously.

---

# Configuration Minimalism

A new configuration option should only be introduced when real variability is required.

The question should be:

```text
Does the system genuinely need multiple valid behaviors?
```

If not, a single canonical behavior is preferable.

---

# Configuration Anti-Pattern — Hidden Defaults

Critical build behavior must not depend on undocumented default values.

---

# Configuration Anti-Pattern — Environment Variable Explosion

Dozens of loosely defined environment variables make builds difficult to reproduce.

Structured configuration should be preferred.

---

# Configuration Anti-Pattern — CI Override Architecture

CI must not override enough settings that it becomes a separate build system.

---

# Configuration Anti-Pattern — Configuration As Code Without Boundaries

Arbitrary executable configuration can hide side effects and undermine determinism.

Declarative configuration should be preferred where practical.

---

# Configuration Anti-Pattern — Secrets In Repository

Credentials and private keys must never be committed as normal build configuration.

---

# Configuration Anti-Pattern — Profile Ambiguity

The build should not infer profiles from vague context such as:

```text
if running somewhere in CI:
    maybe release mode
```

Profile selection must be explicit.

---

# Configuration Anti-Pattern — Silent Unknown Keys

Typos must not silently disable or change critical behavior.

---

# Configuration Maturity Model

FamilyOS build configuration maturity may progress through:

```text
Level 1
Documented Configuration

    ↓

Level 2
Centralized Configuration

    ↓

Level 3
Validated Configuration

    ↓

Level 4
Profile-Based Configuration

    ↓

Level 5
Inspectable Effective Configuration

    ↓

Level 6
Configuration Fingerprinting

    ↓

Level 7
Policy-Aware Configuration
```

Each stage should solve demonstrated needs.

---

# Configuration Success Criteria

The Build Configuration model is successful when FamilyOS can answer:

1. where canonical build configuration is defined;
2. which configuration sources exist;
3. which source has precedence;
4. which profile is active;
5. how configuration is validated;
6. what effective configuration a build used;
7. which values affect artifact output;
8. which configuration is safe to override;
9. how secrets remain separated;
10. how CI consumes canonical configuration;
11. how configuration changes are governed;
12. how obsolete settings are removed;
13. how configuration contributes to reproducibility;
14. how build configuration participates in evidence.

---

# Configuration Invariants

The following invariants should remain true.

## Invariant 1

Critical build configuration must be explicit.

## Invariant 2

Configuration precedence must be deterministic.

## Invariant 3

Invalid configuration must prevent trusted artifact creation.

## Invariant 4

Secrets must not be stored as ordinary configuration.

## Invariant 5

CI must not maintain independent canonical build semantics.

## Invariant 6

Effective configuration must remain stable during a build.

## Invariant 7

Profiles must have documented purpose.

## Invariant 8

Unknown critical configuration must not silently pass.

## Invariant 9

Configuration changes must remain reviewable.

## Invariant 10

Trusted build configuration state must remain explainable.

---

# Configuration Model Summary

The canonical FamilyOS Build Configuration flow is:

```text
Define
  ↓
Store
  ↓
Select Profile
  ↓
Resolve
  ↓
Validate
  ↓
Freeze Effective State
  ↓
Execute Build
  ↓
Record Relevant Evidence
  ↓
Maintain
```

This transforms configuration from an implicit collection of settings into a governed part of the FamilyOS build system.

---

# Final Principle

The FamilyOS Build Configuration model is founded on the following rule:

> A build cannot be reproducible if its behavior depends on configuration that FamilyOS cannot locate, resolve, validate, or explain.

Configuration must therefore remain an explicit engineering input.

It should control variability without creating ambiguity.

It should support different build purposes without fragmenting architecture.

And it should make the effective behavior of every trusted FamilyOS build understandable.
