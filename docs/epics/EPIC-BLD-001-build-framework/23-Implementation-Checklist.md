# Build Framework

# 23 Implementation Checklist

## Overview

EPIC-BLD-001 — Build Framework defines the architecture, principles, lifecycle, governance, validation model, artifact model, automation model, and roadmap required to establish build engineering as an official FamilyOS platform capability.

This document translates the normative Build Framework into an actionable implementation checklist.

Its purpose is not to replace architecture.

Its purpose is to provide a controlled bridge between:

```text id="y9m5fa"
Build Framework
      ↓
Engineering Tasks
      ↓
Implementation
      ↓
Validation
```

The checklist should be used to plan, implement, review, and verify Build Framework capabilities progressively.

The central principle is:

> Implementation must realize the Build Framework without weakening its architectural boundaries or introducing unnecessary complexity.

---

# Purpose

The implementation checklist defines practical work required to realize EPIC-BLD-001.

It covers:

* framework structure;
* repository preparation;
* build entry points;
* build context;
* build profiles;
* dependency management;
* environment management;
* toolchain management;
* configuration;
* execution;
* artifacts;
* validation;
* evidence;
* automation;
* CI;
* security;
* governance;
* release integration;
* documentation;
* future maturity.

Not every future capability is immediately mandatory.

The checklist distinguishes foundational implementation from progressive maturity work.

---

# Checklist Status Model

Each implementation item may use the following status model:

```text id="rl2xop"
[ ] Not Started
[-] In Progress
[x] Complete
[!] Blocked
[~] Deferred
```

Where used in repository planning, status should reflect actual implementation state.

---

# Implementation Priority Model

Checklist items are grouped into three implementation levels.

```text id="cnfc12"
FOUNDATION
    ↓
Required To Establish Canonical Build Capability

MATURITY
    ↓
Strengthens Reliability, Traceability, And Automation

FUTURE
    ↓
Advanced Capability Introduced When Justified
```

---

# Level 1 — Framework Baseline

## Objective

Finalize EPIC-BLD-001 as the normative architecture before significant build implementation proceeds.

### Checklist

* [ ] Confirm all 24 numbered Build Framework chapters exist.
* [ ] Confirm all seven control documents exist.
* [ ] Remove temporary migration files.
* [ ] Remove duplicate numbered documents.
* [ ] Remove obsolete inherited canonical filenames.
* [ ] Confirm all normative files contain complete content.
* [ ] Validate final document structure against `20-Validation.md`.
* [ ] Synchronize `MANIFEST.md`.
* [ ] Synchronize `README.md`.
* [ ] Synchronize `EPIC.yaml`.
* [ ] Update `CHANGELOG.md`.
* [ ] Update `Revision-History.md`.
* [ ] Record final framework validation in `VALIDATION.md`.
* [ ] Review `EPIC-BLD-001.md` against `00-EPIC.md`.
* [ ] Commit the validated Build Framework baseline.
* [ ] Create the appropriate repository tag after checking actual tag history.

---

# Level 2 — Canonical Build Entry Point

## Objective

Establish one canonical build interface for FamilyOS.

The implementation should eliminate dependence on undocumented command sequences.

### Checklist

* [x] Identify the current canonical Python package build mechanism.
* [x] Define one official FamilyOS build entry point.
* [ ] Ensure the entry point works from the documented repository context.
* [x] Ensure the build entry point is callable locally.
* [ ] Ensure the same build entry point can be invoked by CI.
* [x] Document supported build arguments.
* [x] Define default build behavior.
* [ ] Define explicit profile selection.
* [ ] Define explicit build target selection if multiple targets exist.
* [x] Define canonical build exit-code behavior.
* [x] Ensure required-stage failure produces non-zero process status.
* [x] Prevent the canonical build command from publishing releases.
* [x] Add usage documentation.
* [x] Add tests for build-interface behavior where practical.

Implementation evidence: `familyos build` delegates through the CLI context,
application container, package-build use case, packaging port, and
subprocess-backed Python frontend adapter. The adapter invokes
`sys.executable -m build --outdir <output-dir>` without shell interpretation.
Focused tests cover command registration, delegation, explicit output,
success/failure exits, normalized execution failures, and the absence of a
publication command. An isolated integration test copies the actual packaging
inputs into a temporary project and proves that the production adapter builds
one wheel and one source distribution without changing tracked checkout files.
GitHub Actions does not invoke `familyos build` yet.

---

# Canonical Build Interface Acceptance

The canonical interface should eventually support a model conceptually similar to:

```text id="m4jk05"
Build Request
      ↓
Resolve Context
      ↓
Validate Preconditions
      ↓
Execute Build
      ↓
Return Build Result
```

Implementation syntax may differ.

---

# Level 3 — Build Target Model

## Objective

Make build scope explicit.

### Checklist

* [x] Identify current build target or targets.
* [x] Define the FamilyOS CLI package as an explicit build target.
* [ ] Define official plugin build targets if independent packaging is required.
* [ ] Define documentation build targets where appropriate.
* [x] Define expected inputs for every target.
* [x] Define expected artifact types for every target.
* [x] Define target-specific validation requirements.
* [x] Prevent targets from consuming unrelated repository state.
* [x] Document target ownership.
* [x] Add target validation tests where practical.

Implementation evidence: the canonical Build Framework currently supports one
explicit build target, `familyos-cli-package`. The immutable
`BuildTargetDefinition` records its owning framework responsibility, canonical
dependency and package-source inputs, expected Python wheel and source
distribution artifact classes, and structural-validation requirement.

`RunPackageBuildUseCase` resolves the target definition before Build Context
resolution and package execution. The production package builder executes from
the explicit repository project root, while existing integration coverage proves
the real package build can run from isolated copied packaging inputs without
modifying tracked checkout files.

The target-level expected artifact classes are intentionally kept separate from
the richer package-discovery rules. A dedicated consistency test guarantees that
the canonical target contract remains aligned with the discoverer's exact wheel
and source-distribution expectations.

Official plugin and documentation targets remain intentionally undefined until
independent packaging requirements make those targets necessary.

---

# Level 4 — Build Profiles

## Objective

Introduce explicit profiles representing build purpose.

### Initial Recommended Profiles

```text id="et3svt"
development
validation
ci
release-candidate
```

Additional profiles should only be introduced when necessary.

### Checklist

* [x] Define `development` profile purpose.
* [x] Define `validation` profile purpose.
* [x] Define `ci` profile purpose.
* [x] Define `release-candidate` profile purpose.
* [x] Define profile-specific validation.
* [x] Define profile-specific evidence requirements.
* [x] Define profile-specific environment restrictions.
* [x] Define artifact expectations per profile.
* [x] Ensure profile selection is explicit.
* [x] Avoid environment-based implicit profile switching.
* [x] Validate unsupported target/profile combinations.
* [x] Document profile behavior.

Implementation evidence: immutable `BuildProfileDefinition` contracts now
define purpose, supported targets, validation scope, evidence requirements,
environment requirements, and artifact expectations for `development`,
`validation`, `ci`, and `release-candidate`.

`validate_profile_target()` provides the canonical compatibility authority for
profile/target combinations and is invoked by `RunPackageBuildUseCase` before
Build Context resolution or package execution.

The public `familyos build` command exposes explicit `--profile` selection with
`development` as the documented default. Typer rejects unsupported profile
values before execution. No environment variable or evidence-output option
implicitly changes the selected Build Profile.

The canonical GitHub Actions package-build step explicitly invokes
`familyos build --profile ci`, so CI package execution records `ci` in the
resolved Build Context rather than relying on the development default.

Unit and end-to-end coverage verifies profile definitions, explicit CLI
propagation, default-profile behavior, invalid-profile rejection, CI-profile
real package execution, and pre-execution profile/target compatibility
enforcement.

---

# Level 5 — Build Context

## Objective

Create a stable effective Build Context for execution and evidence.

### Checklist

* [x] Define the minimum Build Context model.
* [x] Capture source revision when Git is available.
* [x] Capture relevant working-tree state.
* [x] Capture selected build profile.
* [x] Capture selected build target.
* [x] Capture effective configuration.
* [x] Capture dependency state at appropriate maturity.
* [x] Capture runtime version.
* [x] Capture critical toolchain versions.
* [x] Capture relevant environment properties.
* [x] Capture applicable policy state where required.
* [x] Resolve context before significant execution.
* [x] Prevent uncontrolled context mutation during execution.
* [x] Make non-sensitive context inspectable.
* [x] Add tests for context resolution.

---

# Minimum Build Context

An initial implementation may use:

```text id="b4uxje"
BuildContext
│
├── Source Revision
├── Working Tree State
├── Target
├── Profile
├── Runtime Version
├── Effective Configuration
└── Output Location
```

Additional fields may be introduced progressively.

Implementation evidence: the application-owned immutable `BuildContext` now
captures `SourceState`, canonical `DependencyState`, immutable
`EnvironmentState`, explicit `BuildProfile`, explicit `BuildTarget`, runtime
version, non-sensitive effective configuration, and resolved artifact output
location. `DependencyState` identifies the canonical `pyproject.toml`
declaration and `requirements.txt` lock by resolved path and SHA-256 digest.

The immutable `ToolchainState` captures the installed versions of the critical
`build`, `pip-tools`, `setuptools`, and `wheel` distributions in deterministic
order. These cover the canonical package-build frontend, dependency-state
compiler, build backend, and wheel packaging support. Python runtime identity
remains explicit in its dedicated Build Context field.

`EnvironmentStateProvider` captures the canonical non-sensitive execution
environment properties currently required by the Build Framework: operating
system identity, operating-system release, and machine architecture. The
captured `EnvironmentState` is immutable and becomes part of the resolved
Build Context before package execution.

At the current Build Framework maturity, applicable build-policy requirements
are represented by the explicitly selected canonical `BuildProfileDefinition`.
Profile definitions establish supported targets, validation scope, evidence
requirements, environment requirements, and artifact expectations.
`validate_profile_target()` rejects unsupported profile/target combinations
before Build Context resolution and package execution.

No independent mutable or duplicated `PolicyState` is introduced at this
maturity. Policy authorities owned by the Quality, Security, Plugin Compliance,
Release, or repository-governance frameworks remain external authorities until
their requirements become concrete inputs that must be independently resolved
for a build. In particular, the Build Framework does not redefine plugin
compliance rules or Release Framework promotion policy.

`BuildContextResolver` resolves source, dependency, critical toolchain,
environment, profile, target, runtime, effective configuration, and output
location before canonical package execution. `RunPackageBuildUseCase`
preserves the resolved context in `CanonicalPackageBuildResult` on both
successful and failed execution paths.

`BuildContext`, `BuildEffectiveConfiguration`, `SourceState`,
`DependencyState`, `ToolchainState`, and `EnvironmentState` are immutable,
preventing uncontrolled mutation of resolved canonical context during
execution.

The canonical CLI renders the non-sensitive resolved profile, target, runtime,
operating system, operating-system release, machine architecture, critical
toolchain versions, output directory, and functional-validation configuration
for inspection.

Focused model, provider, resolver, package-build, execution-order, CLI, and
real-build tests cover context resolution, source and dependency state,
critical toolchain capture, environment capture, explicit profile and target
selection, runtime capture, policy-bearing profile resolution, immutability,
pre-execution ordering, failed execution preservation, and non-sensitive
rendering.

Level 5 is complete at the current Build Framework maturity. Future policy
integration may extend the Build Context when an independently resolved
Quality, Security, Plugin Compliance, Release, or governance policy becomes a
concrete canonical build input.

---

# Level 6 — Build Identity

## Objective

Associate significant build execution with stable identity.

### Checklist

* [x] Define Build ID semantics.
* [x] Generate a Build ID for CI and release-candidate builds.
* [x] Determine whether local development builds require Build IDs.
* [x] Associate Build ID with Build Context.
* [x] Associate Build ID with artifacts.
* [x] Associate Build ID with validation results.
* [x] Associate Build ID with Build Evidence.
* [x] Include Build ID in diagnostics.
* [x] Avoid using CI provider run ID as the only logical Build ID unless explicitly adopted.
* [x] Document Build ID format.
* [x] Add tests for Build ID generation and propagation.

Implementation evidence: `BuildId` is the canonical immutable UUID-backed
identity for one build execution and is generated exactly once by
`RunPackageBuildUseCase` before Build Context resolution or package execution.

The generated Build ID is now part of the immutable `BuildContext`, making the
resolved source, dependency, toolchain, environment, profile, target, runtime,
configuration, and output location explicitly associated with the same
execution identity carried by `CanonicalPackageBuildResult`.

Successful structurally validated artifacts receive immutable
`ArtifactIdentity` metadata containing the canonical Build ID. The
`ArtifactManifest` preserves the same Build ID and rejects inconsistent
artifact associations.

Canonical build-validation results preserve the Build ID used for the build,
and `BuildEvidence` requires Build ID consistency across validation, manifest,
and artifact-integrity records. Evidence construction rejects mismatched Build
IDs rather than silently combining records from different executions.

The canonical CLI renders the Build ID for diagnostics. Build identity remains
provider-neutral and does not depend on a CI-provider run identifier. Local
development, validation, CI, and release-candidate executions use the same
logical Build ID semantics.

Focused Build ID, Build Context, package-build, Artifact Identity, manifest,
validation, evidence, and CLI tests verify generation, immutability,
pre-execution creation, successful and failed execution preservation, context
association, artifact propagation, validation propagation, evidence
consistency, and mismatch rejection.

Level 6 is complete at the current Build Framework maturity.

---

# Level 7 — Build Input Validation

## Objective

Validate build-relevant source state before transformation.

### Checklist

* [x] Validate required source directories.
* [x] Validate required project configuration.
* [x] Validate package metadata.
* [x] Validate required dependency definitions.
* [x] Validate build-profile existence.
* [x] Validate target existence.
* [x] Validate required generated inputs where applicable.
* [x] Detect stale generated inputs where practical.
* [x] Reject malformed build metadata.
* [x] Fail early on missing mandatory input.
* [x] Produce actionable failure diagnostics.
* [x] Add automated tests for invalid input cases.

Implementation evidence: the canonical `familyos-cli-package` target declares
its mandatory inputs through `BuildTargetDefinition`. `BuildInputValidator`
enforces those requirements before Build Context resolution and before
`PackageBuilderPort.build()` may execute.

The canonical target requires `pyproject.toml`, generated `requirements.txt`,
and package source governed by the project configuration. Missing mandatory
inputs fail deterministically with actionable diagnostics and prevent package
transformation.

`BuildInputValidator` parses `pyproject.toml` before execution and validates
the minimum canonical package metadata required at this maturity: a valid
`[project]` table with non-empty `name`, `version`, and `requires-python`
fields. Malformed TOML, absent project metadata, and invalid required fields
are rejected before build execution.

Generated dependency state is treated as a canonical build input.
`requirements.txt` carries the SHA-256 digest of normalized dependency-relevant
inputs from `pyproject.toml`. The application-owned
`dependency_input_freshness` contract computes that digest deterministically
and compares it with the digest embedded in the generated lock.

A missing dependency digest or a digest that no longer matches canonical
dependency declarations is rejected as stale before Build Context resolution
and package execution. The existing canonical dependency-lock verification
continues to perform the stronger seeded-resolution drift check independently,
without duplicating that expensive operation in every package build.

The application freshness digest has been verified byte-for-byte against the
historical dependency-generation digest for the canonical repository state.
The committed `requirements.txt` is currently synchronized with
`pyproject.toml`.

Build profile and target existence are validated by the canonical profile and
target registries before input validation. Production `familyos build` receives
`BuildInputValidator` through `ApplicationContainer`, making these checks part
of the real package-build path rather than test-only behavior.

Focused tests cover mandatory-input presence, valid and malformed package
metadata, generated-lock digest presence, fresh and stale generated dependency
state, deterministic digest calculation, diagnostic propagation, and fail-fast
package-build behavior. Integration coverage proves that stale generated input
prevents `PackageBuilderPort.build()` from being called.

Validation evidence for this Level includes:

* package-build integration: 19 passed;
* input-validation and freshness coverage: 21 passed;
* dependency-lock regression coverage: 18 passed;
* Build Application suite: 267 passed;
* full repository suite: 1575 passed;
* Ruff: passed;
* MyPy: passed for 664 source files;
* canonical dependency freshness: `requirements.txt` synchronized with
  `pyproject.toml`;
* `git diff --check`: passed.

Level 7 is complete at the current Build Framework maturity.

---

# Level 8 — Repository Structure Validation

## Objective

Ensure project structure supports deterministic build discovery.

### Checklist

* [ ] Define repository-root detection.
* [ ] Avoid developer-specific absolute paths.
* [ ] Define canonical source paths.
* [ ] Define canonical build configuration location.
* [ ] Define canonical artifact output location.
* [ ] Define canonical temporary/staging location if required.
* [ ] Define generated-content ownership.
* [ ] Separate generated content from authoritative source.
* [ ] Prevent build artifacts from being written into source directories.
* [ ] Ensure output directories can be safely cleaned.
* [ ] Review `.gitignore` for derived build state.
* [ ] Add structural validation where high-value.

---

# Level 9 — Build Toolchain

## Objective

Make required build tooling explicit and verifiable.

### Checklist

* [ ] Confirm canonical Python runtime requirement.
* [ ] Define supported runtime versions.
* [ ] Define canonical runtime for release-candidate builds if required.
* [ ] Identify package build frontend.
* [ ] Identify package build backend.
* [ ] Identify Ruff version strategy.
* [ ] Identify MyPy version strategy.
* [ ] Identify Pytest version strategy.
* [ ] Identify any required generators.
* [ ] Document tool acquisition.
* [ ] Validate critical tool availability.
* [ ] Validate unsupported tool versions.
* [ ] Ensure local and CI use compatible tooling.
* [ ] Eliminate canonical dependence on undocumented global tools.
* [ ] Add toolchain inspection capability if useful.
* [ ] Add tests for toolchain validation logic.

---

# Level 10 — Environment Management

## Objective

Ensure builds can be reconstructed from supported environment requirements.

### Checklist

* [ ] Document supported development environment.
* [ ] Document supported CI environment.
* [ ] Validate Python runtime before build.
* [ ] Detect active virtual environment where useful.
* [ ] Define environment setup instructions.
* [ ] Ensure a fresh virtual environment can reproduce the build.
* [ ] Remove reliance on undeclared globally installed packages.
* [ ] Identify required system tools.
* [ ] Identify relevant filesystem requirements.
* [ ] Identify relevant network requirements.
* [ ] Define temporary-directory behavior.
* [ ] Define cache locations.
* [ ] Ensure caches remain optional.
* [ ] Protect sensitive environment variables.
* [ ] Minimize environment variable influence on artifact semantics.
* [ ] Add environment-validation tests.

---

# Clean Environment Acceptance

FamilyOS should eventually demonstrate:

```text id="uf48td"
Fresh Environment
      ↓
Documented Setup
      ↓
Declared Dependencies
      ↓
Canonical Build
      ↓
Valid Artifact
```

---

# Level 11 — Dependency Management

## Objective

Make dependency state sufficiently explicit and reproducible.

### Checklist

* [x] Inventory runtime dependencies.
* [x] Inventory build dependencies.
* [x] Inventory development dependencies.
* [x] Inventory validation dependencies.
* [ ] Remove undeclared build dependencies.
* [x] Confirm canonical dependency declaration source.
* [x] Define version-constraint strategy.
* [x] Evaluate dependency lock strategy.
* [ ] Ensure CI installs from canonical definitions.
* [x] Validate dependency-resolution failures clearly.
* [x] Validate runtime compatibility.
* [ ] Review unused dependencies.
* [ ] Review duplicated dependency functionality.
* [x] Define dependency update workflow.
* [ ] Define security review integration.
* [ ] Capture dependency state in release-candidate evidence when appropriate.
* [x] Add dependency-resolution tests where practical.

Implementation evidence: commit `113148e` establishes and validates the Python 3.13 development/CI dependency version-resolution baseline. This does not complete CI integration or the broader Build Framework implementation.

Incremental isolated-backend evidence: canonical pypa/build execution now
receives the absolute committed `requirements.txt` path as dependency
constraints for both its isolated sdist environment and its separate isolated
wheel-from-sdist environment. Constraints restrict versions only for packages
the backend requests; they do not install the complete lock or reject an
otherwise resolvable dependency merely because it is absent. Build isolation
and network/cache dependence remain. This evidence does not close `Ensure CI
installs from canonical definitions`, and it does not establish the broader
critical toolchain version identity required by Level 40.

---

# Dependency Reproducibility Milestone

A stronger implementation should support:

```text id="3dpqmu"
Canonical Dependency Declaration
            +
Controlled Resolution State
            ↓
Reconstructable Dependency Environment
```

---

# Level 12 — Build Configuration

## Objective

Provide explicit and deterministic configuration behavior.

### Checklist

* [ ] Inventory existing build configuration sources.
* [ ] Identify canonical project configuration.
* [ ] Define configuration precedence.
* [ ] Define framework defaults where needed.
* [ ] Define profile configuration.
* [ ] Define explicit invocation overrides.
* [ ] Minimize environment-variable overrides.
* [ ] Validate final effective configuration.
* [ ] Reject unknown critical settings.
* [ ] Reject conflicting configuration.
* [ ] Prevent arbitrary validation bypass.
* [ ] Separate secrets from build configuration.
* [ ] Make non-sensitive effective configuration inspectable.
* [ ] Document configuration sources and precedence.
* [ ] Add configuration-resolution tests.

---

# Configuration Resolution Acceptance

Equivalent configuration sources should resolve to equivalent effective configuration.

```text id="9oyyro"
Same Configuration Inputs
         ↓
Same Effective Configuration
```

---

# Level 13 — Build Execution

## Objective

Implement predictable and observable transformation from validated context to candidate artifacts.

### Checklist

* [ ] Define build execution stages.
* [ ] Define workspace initialization.
* [ ] Define staging behavior.
* [ ] Define generation stages where needed.
* [ ] Define package assembly.
* [x] Define packaging execution.
* [x] Define output collection.
* [ ] Define execution finalization.
* [x] Propagate mandatory stage failures.
* [x] Prevent ignored subprocess failures.
* [x] Ensure execution does not unexpectedly mutate authoritative source.
* [ ] Define partial-output handling.
* [ ] Define failure cleanup.
* [ ] Define cancellation semantics if required.
* [ ] Define retry policy for transient failures only.
* [ ] Add execution-stage logging.
* [x] Add execution-stage tests.

Implementation evidence: the first canonical package-build slice implements
one controlled packaging invocation and returns only sorted wheel and
source-distribution paths as process-level outputs. Non-zero frontend results
and launch errors cannot become successful build results. This does not assign
artifact identity, validation, integrity, trust, or Build Evidence semantics.
Packaging repository hygiene commit `a85b5a7` removes six generated egg-info
files from Git authority and configures `*.egg-info/`, root `dist/`, and root
`build/` as ignored generated state. Post-commit empirical verification ran an
editable installation, dependency freshness, a real checkout `familyos build`,
and `familyos validation ci`; tracked Git status was clean after every workflow.
This directly closes the source-mutation item without assigning Artifact
Discovery, validation, identity, integrity, trust, or Build Evidence semantics.

---

# Build Execution Acceptance

Execution should produce:

```text id="tozcx7"
Validated Build Context
        ↓
Controlled Execution
        ↓
Candidate Artifact Set
```

not trusted artifacts directly.

---

# Level 14 — Artifact Discovery

## Objective

Explicitly identify the output of each build.

### Checklist

* [x] Define expected artifact classes.
* [x] Define expected artifact count.
* [x] Define canonical output locations.
* [x] Collect artifacts explicitly after execution.
* [x] Detect missing required artifacts.
* [x] Detect unexpected artifacts where useful.
* [x] Distinguish temporary output.
* [x] Distinguish intermediate output.
* [x] Distinguish candidate artifacts.
* [x] Associate candidate artifacts with Build ID.
* [x] Add artifact-discovery tests.

Implementation evidence: the application-owned package discovery use case
compares raw files created or replaced by the current packaging execution with
an explicit contract requiring exactly one `.whl` and one `.tar.gz` file. The
resolved `--output-dir`, defaulting to `<project-root>/dist`, is canonical for
that invocation. Missing, duplicate, out-of-location, and unexpected current
outputs fail discovery and therefore fail `familyos build`.

`ArtifactOutputClassification` now defines three distinct lifecycle roles:
`TEMPORARY`, `INTERMEDIATE`, and `CANDIDATE`. This classification remains
independent from `ArtifactClass`, which identifies artifact/package type such
as Python wheel or source distribution.

The current canonical Python package adapter exposes only final direct
package-build outputs to artifact discovery. Therefore the wheel and source
distribution discovered under the exact package contract are classified
exclusively as `CANDIDATE`; temporary and intermediate roles remain explicitly
representable without being falsely inferred from outputs the builder does not
expose.

Focused tests prove all three lifecycle classifications are distinct, that
temporary and intermediate outputs can be represented explicitly, and that
canonical package discovery emits only candidate outputs.

Candidate artifacts are associated with the canonical Build ID through
explicit Artifact Identity metadata after successful structural validation;
discovery itself remains identity-neutral.

Level 14 — Artifact Discovery is complete.

---

# Level 15 — Artifact Identity

## Objective

Make artifacts independently identifiable.

### Checklist

* [x] Define artifact logical name.
* [x] Define artifact type.
* [x] Capture version context.
* [x] Associate source revision.
* [x] Associate Build ID.
* [x] Record artifact path or storage reference.
* [x] Record artifact size.
* [x] Introduce cryptographic digest.
* [x] Define artifact metadata representation.
* [x] Ensure artifact metadata does not conflict with package metadata.
* [x] Add artifact-identity tests.

---

# Level 16 — Python Package Validation

## Objective

Validate current FamilyOS Python artifacts directly.

### Checklist

* [x] Build wheel artifact.
* [x] Build source distribution where required.
* [x] Validate artifact filename.
* [x] Validate archive structure.
* [x] Validate package metadata.
* [x] Validate Python runtime requirement metadata.
* [x] Validate dependency metadata.
* [x] Validate expected package modules.
* [x] Validate required non-code resources.
* [x] Detect unintended file inclusion.
* [x] Detect missing required package content.
* [x] Install wheel in a clean environment.
* [x] Perform basic import smoke test.
* [x] Perform CLI smoke test where appropriate.
* [x] Validate source distribution can build or install correctly if required.

Implementation evidence: the canonical `familyos build` application flow now
passes the exact successful Artifact Discovery candidates to an application-owned
Python package structural validator. The validator inspects and decompresses
archive members through bounded streams without filesystem extraction. It
validates wheel and source-distribution filename coherence, ZIP/gzip-tar
readability and corruption, safe archive member paths, one
appropriate wheel `.dist-info` directory, required `METADATA`, `WHEEL`, and
`RECORD` structure, one source-distribution root, required `PKG-INFO`, archived
`pyproject.toml`, Python source presence, and package name/version consistency
with the authoritative repository `pyproject.toml`. Focused tests cover valid,
corrupt, malformed, incoherent, missing-metadata, traversal-like, composition,
integration, and CLI outcomes.

Content-and-metadata inventory evidence: the same application validator parses
`Requires-Python` and every `Requires-Dist` field with the standards-compliant
`packaging` library and compares their normalized values with the authoritative
`pyproject.toml` project metadata. Its deterministic Python-module inventory
comes from the configured setuptools package discovery and regular package
source. Non-code resource intent comes independently from regular source files
matching the exact `tool.setuptools.package-data` policy; source existence alone
does not make a resource intended package content. Wheel and source-distribution
package content must contain every expected module/resource and no unintended
package content. The source distribution also rejects unrelated root content
while allowing its defined project and backend-generated metadata files. The
real canonical build proves that both formats contain the declared `py.typed`,
builtin plugin manifests, and templates.

Wheel functional-validation evidence: `familyos build --functional-validation`
preserves the established execution/discovery/static-validation sequence and
passes its exact already-valid wheel candidate to an infrastructure adapter
through an application port. The adapter creates a fresh temporary venv without
system site packages, installs only the wheel's runtime dependency closure under
the committed `requirements.txt` constraints, imports `familyos_cli.main` with
the venv Python in isolated mode, proves its resolved path belongs to the venv
and not repository `src/`, and invokes the installed `familyos --help` entry
point from an external working directory. Stage-specific failures are
deterministic `INVALID` results and fail the aggregate opt-in build. A real
FamilyOS wheel passes; a structurally valid wheel with a broken console entry
point is rejected as the integration negative control.

Source-distribution rebuildability evidence: production infrastructure invokes
the explicitly declared pypa/build frontend with no distribution flags. Its
documented default first emits the source distribution, extracts that exact
archive into temporary state, and builds the wheel from it in a separate
isolated backend environment. A load-bearing integration negative control proves
that a direct wheel can build from checkout while canonical execution fails when
`MANIFEST.in` omits a source file required by a test-only construction guard;
checkout source is therefore not silently substituted for the generated source
distribution. The real canonical build produces exactly one source distribution
and its derived wheel, both of which pass static validation, and the existing
opt-in functional path installs and smokes that derived wheel.

Level 16 is complete. Its source-distribution closure means rebuildability, not
byte-for-byte reproducibility. Static `VALID` and opt-in wheel functional
`VALID` retain their narrow implemented meanings; none establishes Artifact
Identity, Artifact Integrity, trust, provenance, Build Evidence, or release
readiness.

---

# Level 17 — Artifact Integrity

## Objective

Protect artifact identity through cryptographic integrity.

### Checklist

* [x] Select approved digest algorithm.
* [x] Calculate digest from final candidate bytes.
* [x] Record digest in Build Evidence.
* [x] Verify digest after artifact transfer between automation stages.
* [x] Recalculate digest after any intentional artifact mutation.
* [x] Prevent validation state from surviving byte modification.
* [x] Add integrity-verification tests.

Implementation evidence: canonical package-build execution now calculates
explicit SHA-256 integrity metadata from the final bytes of each structurally
validated candidate artifact. Immutable `ArtifactIntegrity` records associate
the corresponding Artifact Identity with the selected digest algorithm and
hexadecimal digest. Integrity calculation occurs after successful structural
validation and Artifact Identity construction; Artifact Discovery remains
integrity-neutral.

`ArtifactIntegrityService` calculates SHA-256 directly from the artifact file
stream and can verify current bytes against a recorded digest.
`BuildArtifactIntegritiesUseCase` deterministically constructs integrity
records for the validated canonical artifact set. The aggregate canonical
package-build result exposes those records on both successful static-only and
functional-validation paths.

Focused tests cover digest calculation, deterministic SHA-256 representation,
successful verification, byte-modification detection, and construction of
integrity records from Artifact Identity metadata. A real canonical functional
build produced and verified integrity records for both the Python wheel and
source distribution. An independent SHA-256 calculation matched the recorded
digest, while a same-size one-byte mutation of a copied wheel invalidated the
recorded integrity digest.

Level 17 remains partial. Build Evidence recording is implemented, and
artifact integrity verification after transfer between automation stages has
now been demonstrated against remotely produced CI artifacts.

Downloaded wheel and source-distribution bytes were recomputed locally and
compared against the SHA-256 digests recorded in canonical Build Evidence.
The transferred artifacts matched their recorded digests. A same-size one-byte
mutation of a transferred wheel produced a different digest and was rejected
against the recorded Build Evidence integrity value.

Intentional artifact mutation is now represented by the application-owned
`MutateArtifactUseCase`. The mutation transition preserves logical build
context while refreshing material Artifact Identity metadata from the mutated
bytes and recalculating canonical SHA-256 Artifact Integrity immediately after
the mutation.

Previously recorded integrity does not survive byte modification: focused
tests prove that both same-size and size-changing mutations invalidate the old
digest while the freshly calculated integrity verifies the new bytes.

Validation state is deliberately not carried through the mutation transition.
`MutatedArtifact` contains only refreshed Artifact Identity and Artifact
Integrity. It exposes no structural-validation, functional-validation,
validated, or trusted state. Mutated bytes therefore require fresh validation
before downstream validated-artifact semantics can be re-established.

Focused lifecycle tests cover digest recalculation from new bytes, material
identity refresh, invalidation of previous integrity, and exclusion of
previous validation state.

Level 17 — Artifact Integrity is complete.

---

# Level 18 — Artifact Manifest

## Objective

Provide a structured record of generated artifact sets.

### Checklist

* [x] Define artifact manifest structure.
* [x] Include Build ID.
* [x] Include artifact names.
* [x] Include artifact types.
* [x] Include artifact sizes.
* [x] Include artifact digests.
* [x] Include validation state.
* [x] Include artifact references or paths.
* [x] Validate manifest completeness.
* [x] Associate manifest with Build Evidence.
* [x] Add manifest-generation tests.

Implementation evidence: canonical package-build execution now constructs an
immutable `ArtifactManifest` after Artifact Identity and Artifact Integrity
have been established for the structurally validated artifact set. The manifest
records the canonical Build ID and deterministic artifact entries containing
logical name, artifact type, version, size, path, digest algorithm, digest, and
structural validation state.

`BuildArtifactManifestUseCase` consumes established Artifact Integrity and
structural-validation results without recalculating artifact identity or
cryptographic digest data. Manifest completeness validation rejects duplicate
artifact paths, mismatched artifact sets, Build ID inconsistencies, and
artifact-type inconsistencies between integrity metadata and structural
validation.

A real canonical functional build produced exactly two manifest entries: one
for the Python wheel and one for the source distribution. Each entry matched
the corresponding Artifact Identity and Artifact Integrity metadata, carried
SHA-256 integrity data, reported structural validation state `valid`, and
referenced an existing artifact whose filesystem size matched the manifest
entry.

Focused manifest-generation tests cover complete manifest construction,
deterministic ordering, missing integrity, unmatched artifact sets, Build ID
mismatch, duplicate integrity paths, artifact-type mismatch, preservation of
established digest and size metadata, and exclusion of Build Evidence, trust,
provenance, signing, publication, and release semantics.

Artifact Manifest association with Build Evidence is implemented.
`BuildEvidenceFactory` requires the canonical package build to contain an
`ArtifactManifest` and passes that manifest into the immutable `BuildEvidence`
aggregate. `BuildEvidence` requires the manifest Build ID to match its own
Build ID and requires every Artifact Integrity record to be represented by an
equivalent manifest entry.

Focused Build Evidence and manifest tests cover manifest presence, Build ID
consistency, manifest/integrity coherence, and preservation of the established
manifest authority without recalculation.

No standalone serialized manifest artifact, provenance, signing, publication,
promotion, release authority, or deployment semantics are introduced.

Level 18 — Artifact Manifest is complete.

---

# Level 19 — Build Validation Orchestration

## Objective

Implement layered validation aligned with `15-Build-Validation.md`.

### Checklist

* [x] Implement input validation.
* [x] Implement configuration validation.
* [x] Implement dependency validation.
* [x] Implement toolchain validation.
* [x] Implement environment validation.
* [x] Implement execution validation.
* [x] Implement artifact validation.
* [x] Implement metadata validation.
* [x] Implement integrity validation.
* [x] Integrate functional artifact validation.
* [x] Integrate evidence validation.
* [x] Define mandatory versus optional checks.
* [x] Define overall validation decision.
* [x] Produce validation diagnostics.
* [x] Add validation test suite.

---

# Validation Decision Acceptance

The implementation should provide a clear result such as:

```text id="nudnsa"
PASSED
```

or:

```text id="xh2vi4"
FAILED
```

for each mandatory validation profile.

---


Implementation evidence: Build Validation now provides an explicit immutable
validation model covering the canonical input, configuration, dependency,
toolchain, environment, execution, artifact, metadata, integrity, functional
artifact, and evidence domains. Checks are explicitly classified as required,
optional, or informational and carry deterministic passed, failed, or skipped
status with optional diagnostics.

`BuildValidationCheckFactory` currently maps established canonical package-build
results into execution, artifact discovery, artifact structural validation,
artifact metadata, artifact integrity, and functional-artifact checks.
Execution, artifact, metadata, and integrity checks are mandatory. Functional
artifact validation is classified according to the caller-provided requirement.

`BuildValidationOrchestrator` produces the aggregate Build Validation decision.
A failed or skipped required check blocks validation. Optional failures are
reported as warnings without failing the aggregate decision, while
informational failures remain non-blocking. The resulting
`BuildValidationResult` preserves the Build ID, validation profile, ordered
checks, diagnostics, failures, and warnings.

Focused tests cover canonical check ordering and domain mapping, missing
artifact discovery, missing manifest metadata, optional and required skipped
functional validation, required failures, optional and informational failures,
required skipped checks, successful mandatory checks, Build ID and profile
preservation, and the current empty-check-set behavior. A real canonical
functional package build was mapped to six Build Validation checks and produced
a successful aggregate decision with every performed check passing.

Dependency Validation integration now consumes the existing canonical
`dependency-freshness` and `dependency-consistency` gate results without
re-executing their underlying checks. `BuildValidationCheckFactory` maps both
gates into required `DEPENDENCY` checks while preserving diagnostics.
Canonical gate `PASSED` maps to Build Validation `PASSED`; both gate `FAILED`
and gate `ERROR` map to blocking Build Validation `FAILED`.

Focused tests cover successful dependency mapping, freshness failure,
consistency failure, diagnostic preservation, canonical gate execution error,
rejection of unrelated validation gates, and aggregate Build Validation
failure behavior. A real canonical CI validation run produced passing
`dependency-freshness` and `dependency-consistency` gates, which mapped to two
required passing Build Validation dependency checks.

Toolchain Validation now consumes explicit observations of the
canonical build toolchain. Build Validation currently requires a compatible
Python runtime and availability of the Python `build` module used by canonical
package construction. These observations map to required `TOOLCHAIN` checks.

Focused tests cover successful toolchain mapping, unsupported Python,
unavailable build tooling, diagnostic preservation, and aggregate validation
failure behavior. A real probe confirmed Python 3.13.7, `build` 1.5.0, and a
successful aggregate Build Validation decision for both required toolchain
checks.

Environment Validation now maps explicit observations of the
canonical build environment into required checks. The current environment
contract verifies that the project root is available and that the configured
build-output environment exists, is a directory, and is writable.

Focused tests cover successful environment mapping, unavailable project root,
unavailable output environment, diagnostic preservation, and aggregate
validation failure behavior. A real canonical environment probe confirmed the
repository project root and a writable temporary build-output directory,
including a write/read/delete filesystem probe, and produced two required
passing `ENVIRONMENT` checks with an aggregate Build Validation `PASSED`
decision.

Input Validation now maps explicit canonical package-build request
observations into required checks. The current input contract covers the
requested output-path input and the functional-validation option without
duplicating environment, filesystem, or build-execution validation.

Focused tests cover successful input mapping, invalid output-path input,
invalid functional-validation input, diagnostic preservation, and aggregate
validation failure behavior. A real probe confirmed the canonical `dist`
output input and both boolean functional-validation modes, producing two
required passing `INPUT` checks with an aggregate Build Validation `PASSED`
decision.

Configuration Validation now maps explicit observations of the
canonical build configuration into required checks. The current configuration
contract verifies the authoritative package/build configuration from
`pyproject.toml` and the canonical dependency-constraint configuration from
`requirements.txt` without duplicating dependency freshness or consistency
execution.

Focused tests cover successful configuration mapping, invalid package
configuration, invalid dependency configuration, diagnostic preservation, and
aggregate validation failure behavior. A real canonical configuration probe
confirmed project metadata, Python requirement, build backend, and the
dependency-constraint file, producing two required passing `CONFIGURATION`
checks with an aggregate Build Validation `PASSED` decision.

Evidence Validation now consumes concrete canonical `BuildEvidence`.
`BuildValidationCheckFactory.from_evidence_validation()` produces one required
`EVIDENCE` check. Missing Build Evidence fails validation, Build Evidence for a
different Build ID fails validation, and coherent Build Evidence associated
with the current validation Build ID passes.

Focused tests cover coherent Build Evidence, missing evidence, mismatched Build
IDs, and aggregate validation failure behavior. A real canonical package build
was validated, converted into `BuildEvidence`, mapped to a required passing
`EVIDENCE` check, and combined with the existing package-build checks to produce
a final aggregate Build Validation `PASSED` decision.

Level 19 is now functionally complete across input, configuration, dependency,
toolchain, environment, execution, artifact, metadata, integrity, functional
artifact, and Build Evidence validation.

No release decision, publication, promotion, signing, provenance, or deployment
semantics are introduced.

---

# Level 20 — Testing Framework Integration

## Objective

Integrate EPIC-TST-001 without duplicating testing ownership.

### Checklist

* [ ] Identify tests required before build.
* [ ] Identify tests required after artifact creation.
* [ ] Integrate existing Pytest suite.
* [ ] Keep test configuration canonical.
* [ ] Preserve unit-test ownership under Testing Framework.
* [ ] Preserve integration-test ownership under Testing Framework.
* [ ] Add package installation tests where required.
* [ ] Add packaged CLI smoke tests where useful.
* [ ] Ensure failed mandatory tests fail Build Validation.
* [ ] Preserve test reports as evidence where needed.

---

# Level 21 — Quality Framework Integration

## Objective

Expose Build Evidence to EPIC-QLT-001.

### Checklist

* [ ] Identify build-specific quality signals.
* [ ] Expose validation results.
* [ ] Expose artifact validation status.
* [ ] Expose reproducibility evidence when available.
* [ ] Define build quality-gate inputs.
* [ ] Avoid defining independent competing quality policy.
* [ ] Document ownership boundaries.
* [ ] Integrate quality-gate failure with CI where applicable.

---

# Level 22 — Plugin Compliance Integration

## Objective

Ensure official plugin builds can consume EPIC-PLUGIN-002 compliance results.

### Checklist

* [ ] Identify plugin build targets.
* [ ] Validate plugin metadata before packaging.
* [ ] Invoke required compliance checks.
* [ ] Capture compliance result.
* [ ] Block trusted plugin artifact creation on blocking compliance findings.
* [ ] Preserve compliance evidence.
* [ ] Ensure Build Framework does not redefine compliance rules.
* [ ] Add representative official-plugin build tests.

---

# Level 23 — Documentation Build Integration

## Objective

Support documentation as controlled build input and output where appropriate.

### Checklist

* [ ] Identify generated documentation activities.
* [ ] Identify authoritative documentation sources.
* [ ] Define generators.
* [ ] Define documentation artifact outputs.
* [ ] Validate generated documentation.
* [ ] Detect stale generated documentation where useful.
* [ ] Keep Documentation Framework ownership boundaries.
* [ ] Avoid undocumented local documentation tooling.

---

# Level 24 — Build Evidence

## Objective

Create evidence sufficient to explain important builds.

### Initial Evidence Checklist

* [x] Build ID.
* [x] source revision.
* [ ] target.
* [x] profile.
* [ ] runtime version.
* [ ] critical tool versions.
* [ ] effective configuration summary.
* [x] validation result.
* [x] artifact manifest.
* [x] artifact digests.

### Mature Evidence Checklist

* [ ] dependency graph identity.
* [ ] environment identity.
* [ ] stage results.
* [ ] reproducibility status.
* [ ] provenance data.

---

# Build Evidence Bundle

A mature conceptual structure may be:

```text id="8gh8cz"
BuildEvidence
│
├── BuildIdentity
├── Source
├── Configuration
├── Dependencies
├── Toolchain
├── Environment
├── Validation
├── ArtifactManifest
└── Integrity
```

---

# Level 25 — Build Result

## Objective

Provide one coherent final result for automation and diagnostics.

### Checklist

* [ ] Define Build Result representation.
* [ ] Include Build ID.
* [ ] Include target.
* [ ] Include profile.
* [ ] Include execution status.
* [ ] Include validation status.
* [ ] Include artifact set.
* [ ] Include evidence reference.
* [ ] Include failure diagnostics.
* [ ] Ensure failed builds still return useful structured information.
* [ ] Add serialization if machine-readable automation requires it.

---

# Level 26 — Local Developer Workflow

## Objective

Keep canonical build behavior practical for developers.

### Checklist

* [x] Document local environment setup.
* [x] Document dependency installation.
* [x] Document canonical build command.
* [x] Document canonical validation command.
* [x] Document artifact location.
* [x] Document cleanup.
* [x] Document common failures.
* [x] Ensure local validation approximates CI semantics.
* [x] Ensure developers can reproduce common CI failures locally.
* [x] Avoid mandatory CI-only build steps.

Implementation evidence: the root `README.md` documents the supported Python
3.13 virtual environment, controlled `requirements.txt` bootstrap, read-only
dependency freshness check, intentional dependency regeneration, canonical
`familyos validation ci` command, deterministic JSON evidence, local/CI
semantic alignment, and remediation for common bootstrap and validation
failures. The provider-neutral command is the same entry point invoked by
`.github/workflows/ci.yml`. The `Canonical CI Validation` workflow's package
build step invokes the identical `familyos build --output-dir dist` command a
developer runs locally, with no CI-only build flag, script, or logic; the
candidate output location (`dist/`, defaulting from the Level 14 discovery
contract) is now explicit in both places.

Local developer cleanup is now explicitly documented in the repository root
`README.md`. The procedure identifies the implemented derived state that may be
removed safely: `.venv`, root `dist/`, root `build/`, generated `*.egg-info/`,
and Pytest, Ruff, and MyPy cache directories.

The cleanup contract preserves authoritative source, configuration, dependency
definitions, tracked generated derivatives, and other repository authority.
All documented cleanup targets are reconstructable from committed repository
inputs and are already classified as ignored derived state where applicable.

Artifact failure-cleanup semantics and broader lifecycle cleanup remain owned
by their respective implementation levels and are not prerequisites for the
local developer cleanup procedure.

Level 26 — Local Developer Workflow is complete.

---

# Developer Experience Acceptance

A contributor should be able to answer:

```text id="0cv6wr"
How do I set up the environment?

How do I validate the project?

How do I build?

Where is the artifact?

Why did the build fail?
```

without relying on tribal knowledge.

---

# Level 27 — CI Foundation

## Objective

Use CI as an independent executor of canonical build semantics.

### Checklist

* [x] Check out known source revision.
* [x] Provision explicit runtime.
* [x] Install canonical dependency state.
* [x] Validate toolchain.
* [x] Run Ruff.
* [x] Run MyPy.
* [x] Run Pytest.
* [x] Run canonical build command.
* [x] Collect explicit candidate artifacts.
* [x] Run artifact validation.
* [x] Generate artifact integrity data.
* [x] Collect Build Evidence.
* [x] Upload CI artifacts where useful.
* [x] Ensure mandatory failure produces failed workflow.
* [x] Document how to reproduce CI locally.

Implementation evidence: commit `504bd19` introduced the provider-neutral Canonical CI Validation Baseline and its thin GitHub Actions adapter. Commit `c2ed8de` corrected the missing Health documentation template found by the first real execution. GitHub Actions run `31749853569` then completed successfully under Python 3.13, uploaded `ci-validation.json`, and recorded all six mandatory gates as `PASSED`.

Package-build integration evidence: commit `63693e6` was executed by the
`Canonical CI Validation` workflow in push run `31792439104`. The completed
run and `validate` job both succeeded, retained `familyos-ci-validation`, and
uploaded `familyos-package-candidates`. The downloaded candidate artifact
contained exactly `familyos_cli-0.1.0-py3-none-any.whl` and
`familyos_cli-0.1.0.tar.gz` (one wheel and one source distribution). This
empirically satisfies canonical build execution and explicit candidate
collection in CI.

Structural artifact-validation evidence: commit `c49c655` was executed by the
`Canonical CI Validation` workflow in push run `31801029251`. The completed
run and `validate` job both succeeded. At that commit, the canonical
`familyos build --output-dir dist` invocation includes Python Package
Structural Validation after successful Artifact Discovery, so this success
empirically proves remote execution of the mandatory structural-validation
path, not only build and discovery. `familyos-ci-validation` remained
available and `familyos-package-candidates` was uploaded, again containing
exactly `familyos_cli-0.1.0-py3-none-any.whl` and
`familyos_cli-0.1.0.tar.gz` (one wheel and one source distribution). This
closes `Run artifact validation` above.

At the time of that structural-validation run, this evidence did not yet
establish artifact integrity or Build Evidence and did not complete the
remaining functional Level 16 checks (clean-environment installation,
import/CLI smoke, or source-distribution build/install validation).

Subsequent CI Build Evidence integration in commit `794907e` closed the
artifact-integrity and Build Evidence gaps. GitHub Actions run `32574446181`
successfully uploaded `familyos-build-evidence`; the downloaded evidence
matched the executed source revision, contained a passing `ci` Build Validation
result, two artifact manifest entries, and two matching SHA-256 integrity
records. The observed working-tree state was preserved as `dirty: true`.

---

# CI Foundation Flow

```text id="3arvku"
Checkout
   ↓
Setup
   ↓
Ruff
   ↓
MyPy
   ↓
Pytest
   ↓
Build
   ↓
Artifact Validation
   ↓
Evidence
```

Parallelization may be introduced after correctness is established.

---

# Level 28 — CI Permissions

## Objective

Apply least privilege to automation.

### Checklist

* [x] Review default workflow permissions.
* [x] Use read-only repository permissions where sufficient.
* [ ] Separate build credentials from release credentials.
* [ ] Prevent release credentials in pull-request builds.
* [ ] Limit secret scope.
* [ ] Prevent secrets from reaching untrusted execution contexts.
* [x] Review third-party CI actions or integrations.
* [x] Pin critical external automation dependencies where governance requires it.
* [ ] Document CI security assumptions.

---

# Level 29 — CI Caching

## Objective

Improve performance without changing semantics.

### Checklist

* [ ] Identify safe dependency caches.
* [ ] Define cache key inputs.
* [ ] Include runtime state in cache identity where required.
* [ ] Include dependency state in cache identity.
* [ ] Ensure cache miss still produces correct build.
* [ ] Ensure corrupted cache can be discarded.
* [ ] Validate cache-free builds periodically.
* [ ] Avoid cache dependence for authoritative state.

---

# Level 30 — Artifact Transfer Across CI Jobs

## Objective

Preserve exact artifact identity across automation stages.

### Checklist

* [ ] Build artifact once.
* [ ] Calculate digest.
* [ ] Upload same artifact.
* [ ] Download artifact in validation or release preparation stage.
* [ ] Recalculate digest.
* [ ] Compare digest.
* [ ] Reject changed artifact.
* [ ] Avoid rebuilding between build and validation jobs.

---

# Level 31 — Build-Once-Promote

## Objective

Prepare strong Build/Release integration.

### Checklist

* [ ] Identify trusted artifact after Build Validation.
* [ ] Preserve trusted artifact bytes.
* [ ] Preserve digest.
* [ ] Preserve Build ID.
* [ ] Preserve validation evidence.
* [ ] Provide explicit Release Handoff.
* [ ] Ensure Release workflow consumes existing artifact.
* [ ] Prevent downstream silent rebuild.
* [ ] Verify artifact integrity before promotion.

---

# Release Handoff Acceptance

The Build Framework should provide conceptually:

```text id="36ofcd"
ReleaseHandoff
│
├── Build ID
├── Artifact Set
├── Artifact Manifest
├── Digests
├── Validation Result
└── Evidence
```

---

# Level 32 — Release Candidate Profile

## Objective

Implement the strongest Build Framework profile required before EPIC-REL-001 evaluation.

### Checklist

* [ ] Require identifiable source revision.
* [ ] Require appropriate clean working-tree state.
* [ ] Require canonical runtime.
* [ ] Require controlled dependency resolution.
* [ ] Require validated toolchain.
* [ ] Require controlled environment.
* [ ] Require complete source validation.
* [ ] Require complete test suite applicable to release readiness.
* [ ] Require artifact validation.
* [ ] Require integrity digests.
* [ ] Require Build Evidence.
* [ ] Produce explicit release handoff.
* [ ] Do not publish automatically from Build Framework.

---

# Level 33 — Observability

## Objective

Make build execution understandable.

### Checklist

* [ ] Log Build ID.
* [ ] Log target.
* [ ] Log profile.
* [ ] Log stage progression.
* [ ] Log important stage duration.
* [ ] Report artifacts.
* [ ] Report validation failures.
* [ ] Avoid secret logging.
* [ ] Define debug diagnostics.
* [ ] Define machine-readable output if needed.
* [ ] Distinguish warning from error.
* [ ] Ensure CI failure points remain visible.

---

# Level 34 — Build Metrics

## Objective

Introduce metrics only where they support decisions.

### Potential Metrics

* [ ] total build duration;
* [ ] stage duration;
* [ ] build success rate;
* [ ] failure category;
* [ ] artifact validation failure rate;
* [ ] dependency resolution failure rate;
* [ ] environment validation failure rate;
* [ ] cache hit rate;
* [ ] retry rate;
* [ ] reproducibility result.

Metrics should not become requirements merely because they can be measured.

---

# Level 35 — Failure Classification

## Objective

Improve diagnostics through consistent failure categories.

### Checklist

* [ ] Define input failure category.
* [ ] Define configuration failure category.
* [ ] Define dependency failure category.
* [ ] Define toolchain failure category.
* [ ] Define environment failure category.
* [ ] Define execution failure category.
* [ ] Define artifact failure category.
* [ ] Define validation failure category.
* [ ] Define integrity failure category.
* [ ] Ensure diagnostics include corrective information.
* [ ] Add failure-path tests.

---

# Level 36 — Build Security

## Objective

Integrate secure build principles from the beginning.

### Checklist

* [ ] Minimize build-process privileges.
* [ ] Keep production credentials out of normal builds.
* [ ] Keep release publication credentials out of normal builds.
* [ ] Protect registry credentials.
* [ ] Avoid secret logging.
* [ ] Detect accidental secret inclusion in artifacts where practical.
* [ ] Review build dependencies for supply-chain risk.
* [ ] Review generators for trust risk.
* [ ] Review network access.
* [ ] Avoid unrestricted external execution.
* [ ] Control subprocess arguments.
* [ ] Avoid unsafe shell command construction.
* [ ] Document build security assumptions.

---

# Level 37 — Build Governance Implementation

## Objective

Make `16-Build-Governance.md` operational.

### Checklist

* [ ] Define Build Framework ownership.
* [ ] Define build implementation ownership.
* [ ] Define toolchain ownership.
* [ ] Define CI ownership.
* [ ] Define artifact ownership.
* [ ] Define routine-change review path.
* [ ] Define significant-change review path.
* [ ] Define ADR threshold.
* [ ] Define RFC threshold.
* [ ] Define exception process.
* [ ] Define technical-debt tracking.
* [ ] Define build-security escalation.
* [ ] Define artifact-contract change review.
* [ ] Define validation-weakening review.
* [ ] Document governance process.

---

# Level 38 — Documentation Synchronization

## Objective

Ensure implementation and documentation remain aligned.

### Checklist

* [ ] Update Build Framework when architecture changes.
* [ ] Update developer build instructions.
* [ ] Update CLI reference when build interface changes.
* [ ] Update CI documentation.
* [ ] Update toolchain documentation.
* [ ] Update environment setup.
* [ ] Update dependency workflow.
* [ ] Update artifact documentation.
* [ ] Update release handoff documentation.
* [ ] Update ADRs/RFCs when applicable.
* [ ] Prevent permanent implementation/documentation drift.

---

# Level 39 — Build Technical Debt

## Objective

Identify and reduce legacy build behavior.

### Checklist

* [ ] Inventory legacy build scripts.
* [ ] Inventory duplicate build commands.
* [ ] Inventory CI-specific build logic.
* [ ] Inventory duplicated configuration.
* [ ] Inventory obsolete environment assumptions.
* [ ] Inventory unowned tools.
* [ ] Inventory permanently skipped validations.
* [ ] Inventory manual release preparation steps.
* [ ] Prioritize debt by impact and risk.
* [ ] Remove obsolete paths after migration.
* [ ] Document accepted temporary debt.

---

# Level 40 — Reproducibility Baseline

## Objective

Move from repeatable procedure toward reconstructable Build Context.

### Checklist

* [ ] Establish canonical source identity.
* [ ] Establish deterministic configuration resolution.
* [x] Establish controlled dependency state.
* [ ] Establish critical toolchain version identity.
* [x] Establish reconstructable environment setup.
* [ ] Remove time-dependent artifact content where unnecessary.
* [ ] Remove random artifact content where unnecessary.
* [ ] Normalize input ordering where relevant.
* [ ] Reduce uncontrolled network dependency.
* [ ] Compare repeated builds.
* [x] Document known reproducibility limitations.

---

# Reproducibility Acceptance

The initial target is:

```text id="sd5w0j"
Equivalent Controlled Inputs
            ↓
Equivalent Logical Artifact
```

Bit-for-bit identity may be a later objective.

---

# Level 41 — Build Context Fingerprint

## Objective

Provide stronger context identity for reproducibility and caching.

### Checklist

* [ ] Define canonical fingerprint inputs.
* [ ] Include source identity.
* [ ] Include relevant configuration.
* [ ] Include dependency-state identity.
* [ ] Include critical toolchain state.
* [ ] Include relevant environment state.
* [ ] Define canonical serialization.
* [ ] Calculate fingerprint.
* [ ] Associate fingerprint with Build Evidence.
* [ ] Use fingerprint for comparison where useful.

This is a maturity capability and may remain deferred initially.

---

# Level 42 — Reproducibility Testing

## Objective

Test whether equivalent contexts produce equivalent artifacts.

### Checklist

* [ ] Execute equivalent build twice.
* [ ] Compare artifact count.
* [ ] Compare artifact type.
* [ ] Compare metadata.
* [ ] Compare file contents.
* [ ] Compare digests where bit-for-bit reproducibility is expected.
* [ ] Categorize expected variability.
* [ ] Investigate unexplained variability.
* [ ] Add periodic CI reproducibility checks if justified.

---

# Level 43 — Supply Chain Evidence

## Objective

Progressively strengthen artifact provenance.

### Checklist

* [ ] Record dependency-source information.
* [ ] Record toolchain identity.
* [ ] Record environment identity.
* [ ] Record builder identity where appropriate.
* [ ] Record artifact digests.
* [ ] Define provenance representation.
* [ ] Evaluate industry-standard provenance formats.
* [ ] Avoid creating a proprietary format without clear need.

This remains a future maturity capability.

---

# Level 44 — SBOM Evaluation

## Objective

Evaluate whether Software Bill of Materials generation provides operational value.

### Checklist

* [ ] Identify SBOM use cases.
* [ ] Identify target artifacts.
* [ ] Identify required dependency depth.
* [ ] Evaluate SPDX.
* [ ] Evaluate CycloneDX.
* [ ] Evaluate integration with Security Architecture.
* [ ] Evaluate release evidence integration.
* [ ] Decide through architecture governance before adoption.

SBOM generation is not an immediate mandatory EPIC-BLD-001 implementation requirement.

---

# Level 45 — Artifact Signing Evaluation

## Objective

Evaluate cryptographic artifact signing when Release Framework maturity requires it.

### Checklist

* [ ] Define signing objective.
* [ ] Define signing authority.
* [ ] Define Build versus Release ownership.
* [ ] Define key-management requirements.
* [ ] Define signature format.
* [ ] Define verification process.
* [ ] Define CI permission boundary.
* [ ] Define release integration.
* [ ] Define rotation and revocation behavior.
* [ ] Record an ADR or RFC before adoption.

Signing should generally represent release authority rather than ordinary build execution.

---

# Level 46 — Controlled Builder Evaluation

## Objective

Evaluate stronger build isolation only when justified.

### Potential Options

```text id="63ikde"
Containerized Build
Ephemeral Dedicated Runner
Immutable Build Image
Remote Build Worker
```

### Checklist

* [ ] Identify current environment reproducibility limitation.
* [ ] Determine whether isolation solves the actual problem.
* [ ] Evaluate maintenance cost.
* [ ] Evaluate local developer impact.
* [ ] Evaluate CI portability.
* [ ] Evaluate security benefits.
* [ ] Record architecture decision before introduction.

---

# Level 47 — Artifact Registry Evaluation

## Objective

Introduce dedicated artifact infrastructure only when required by scale or release workflows.

### Checklist

* [ ] Identify current artifact storage limitation.
* [ ] Define registry use cases.
* [ ] Define artifact retention policy.
* [ ] Define permissions.
* [ ] Define artifact immutability requirements.
* [ ] Define Build/Release ownership.
* [ ] Define integrity verification.
* [ ] Evaluate existing registry capabilities before custom infrastructure.
* [ ] Record architectural decision.

---

# Level 48 — Remote Build Execution Evaluation

## Objective

Avoid premature distributed build complexity.

### Checklist

* [ ] Measure current build performance.
* [ ] Identify scalability limitation.
* [ ] Determine whether local/CI optimization is sufficient.
* [ ] Evaluate remote execution benefits.
* [ ] Evaluate cache correctness requirements.
* [ ] Evaluate infrastructure complexity.
* [ ] Evaluate security boundaries.
* [ ] Require RFC-level review before adoption.

Remote execution should remain deferred until a demonstrated need exists.

---

# Level 49 — Performance Optimization

## Objective

Improve build speed without weakening correctness.

### Checklist

* [ ] Establish baseline duration.
* [ ] Identify slow stages.
* [ ] Measure dependency-installation cost.
* [ ] Measure testing cost.
* [ ] Measure packaging cost.
* [ ] Evaluate caching.
* [ ] Evaluate parallel validation.
* [ ] Evaluate incremental execution.
* [ ] Revalidate semantics after optimization.
* [ ] Re-measure performance.
* [ ] Document optimization assumptions.

---

# Performance Priority

Optimization must preserve:

```text id="ss6sx8"
Correctness
    ↓
Reliability
    ↓
Reproducibility
    ↓
Validation
    ↓
Performance
```

---

# Level 50 — Final Build Framework Implementation Validation

## Objective

Determine whether the Build Framework has been materially realized in FamilyOS engineering.

### Checklist

* [ ] Canonical build interface exists.
* [ ] Build profiles exist.
* [ ] Build Context is explicit.
* [ ] Build environment is reconstructable.
* [ ] dependencies are canonical.
* [ ] configuration precedence is explicit.
* [ ] build execution is observable.
* [ ] candidate artifacts are explicit.
* [ ] artifact validation is automated.
* [ ] artifact integrity exists.
* [ ] Build Evidence exists.
* [ ] CI invokes canonical build behavior.
* [ ] local and CI semantics align.
* [ ] security boundaries are enforced.
* [ ] Build Governance is operational.
* [ ] Release Handoff exists.
* [ ] implementation documentation is current.
* [ ] implementation tests pass.
* [ ] no critical Build Framework implementation finding remains.

---

# Minimum Viable Build Framework Implementation

The initial implementation does not need every advanced capability.

A minimum viable Build Framework implementation SHOULD provide:

```text id="tv5otu"
Canonical Build Command
      +
Supported Environment
      +
Declared Dependencies
      +
Explicit Configuration
      +
Canonical Execution
      +
Known Artifact Output
      +
Artifact Validation
      +
CI Integration
```

This provides a strong foundation for later maturity.

---

# Recommended First Implementation Milestone

The first practical milestone should likely establish:

1. one canonical package build command;
2. fresh-environment build success;
3. Ruff validation;
4. MyPy validation;
5. Pytest validation;
6. wheel and source-distribution generation;
7. artifact presence validation;
8. clean artifact installation;
9. CLI/import smoke validation;
10. CI execution of the same workflow.

This creates immediate engineering value without unnecessary infrastructure.

---

# Recommended Second Implementation Milestone

The next milestone should establish:

1. Build ID;
2. artifact manifest;
3. artifact checksums;
4. structured validation result;
5. stronger dependency reproducibility;
6. release-candidate profile;
7. Build Evidence;
8. explicit Release Handoff.

---

# Recommended Third Implementation Milestone

A later milestone may introduce:

1. Build Context fingerprinting;
2. reproducibility comparison;
3. stronger environment definitions;
4. build-once-promote integration;
5. provenance preparation.

---

# Deferred By Default

The following should remain deferred unless a demonstrated requirement appears:

```text id="f606ox"
Distributed Build System
Remote Execution
Custom Build Language
Custom Artifact Registry
Mandatory Containerization
Artifact Signing Infrastructure
Custom Provenance Service
Mandatory SBOM Pipeline
Dedicated Build Cluster
```

---

# Implementation Review Questions

Before implementing a new Build Framework capability, ask:

```text id="jk73tr"
Which Build Framework requirement does this implement?

Which uncertainty does it reduce?

Is there already a simpler mechanism?

Does it preserve canonical local and CI behavior?

Does it alter artifact semantics?

Does it affect release handoff?

Does it introduce security risk?

Does it require architecture governance?

How will it be validated?
```

---

# Implementation Anti-Patterns

The implementation must avoid:

* creating CI-only canonical logic;
* duplicating build commands;
* creating separate local and release builders without reason;
* treating source tests as complete artifact validation;
* introducing hidden environment dependencies;
* adding undeclared build tools;
* modifying trusted artifacts after validation;
* publishing directly from ordinary build jobs;
* creating complex infrastructure before demonstrated need;
* claiming Build Framework implementation completion without evidence.

---

# Implementation Evidence

Implementation progress should be supported by evidence.

Examples include:

```text id="c4lyy3"
git diff
git status
pytest
ruff
mypy
build output
artifact inspection
clean installation test
CI results
artifact digest
```

Framework implementation should remain measurable.

---

# Definition Of Done — Framework Documentation

The EPIC documentation is complete when:

* [ ] all normative documents are complete;
* [ ] final structure is validated;
* [ ] legacy migration state is removed;
* [ ] control documents are synchronized;
* [ ] framework validation passes;
* [ ] framework baseline is committed;
* [ ] framework baseline is tagged according to repository conventions.

---

# Definition Of Done — Initial Implementation

The first Build Framework implementation is complete when:

* [ ] one canonical build path exists;
* [ ] a clean supported environment can execute it;
* [x] dependencies are reconstructed from canonical definitions;
* [ ] required source validation succeeds;
* [ ] required tests succeed;
* [ ] artifacts are generated predictably;
* [ ] artifacts are directly validated;
* [ ] local and CI execution use equivalent semantics;
* [ ] failures are actionable;
* [ ] implementation documentation is current.

---

# Definition Of Done — Trusted Artifact Capability

Trusted artifact capability is complete when:

* [ ] artifact identity is explicit;
* [ ] artifact validation is mandatory;
* [ ] artifact integrity is recorded;
* [ ] Build ID associates artifacts with execution;
* [ ] Build Evidence is available;
* [ ] trusted artifacts are immutable in practice;
* [ ] downstream handoff references the exact validated bytes.

---

# Definition Of Done — Release Integration

Build/Release integration is complete when:

* [ ] release-candidate build profile exists;
* [ ] release handoff contract exists;
* [ ] artifacts are not rebuilt unnecessarily downstream;
* [ ] integrity is verified across handoff;
* [ ] EPIC-REL-001 consumes Build Evidence;
* [ ] release credentials remain outside ordinary Build execution.

---

# Definition Of Done — Reproducibility

Strong reproducibility capability is complete when:

* [ ] source state is precisely identifiable;
* [ ] configuration resolution is deterministic;
* [ ] dependency state is reconstructable;
* [ ] critical toolchain state is controlled;
* [ ] build environment is reconstructable;
* [ ] repeated builds can be compared;
* [ ] meaningful differences are explainable.

Bit-for-bit reproducibility may remain a separate higher maturity target.

---

# Framework Implementation Order

The recommended order is:

```text id="73kx1f"
Framework Baseline
      ↓
Canonical Build Interface
      ↓
Environment
      ↓
Dependencies
      ↓
Configuration
      ↓
Execution
      ↓
Artifact Management
      ↓
Validation
      ↓
CI Automation
      ↓
Build Identity
      ↓
Evidence
      ↓
Release Handoff
      ↓
Reproducibility
      ↓
Supply Chain Maturity
```

This ordering minimizes architectural rework.

---

# Implementation Governance

Implementation must remain subordinate to EPIC-BLD-001.

When implementation reveals that a normative framework requirement is impractical or incomplete, the correct process is:

```text id="2d2s6l"
Implementation Finding
        ↓
Architecture Review
        ↓
Framework Correction If Needed
        ↓
Implementation Update
```

The implementation should not silently diverge from the framework.

---

# Implementation Success Criteria

The implementation checklist is successfully fulfilled when FamilyOS can demonstrate:

1. canonical build execution;
2. reconstructable environment;
3. governed dependencies;
4. deterministic configuration;
5. observable execution;
6. explicit artifacts;
7. artifact-level validation;
8. Build Evidence;
9. local/CI alignment;
10. Build/Release separation;
11. controlled governance;
12. progressive reproducibility;
13. security-aware automation;
14. clear developer workflows;
15. a platform capable of future supply-chain assurance without architectural replacement.

---

# Final Checklist Summary

The complete implementation progression is:

```text id="bczlwm"
Architecture
    ↓
Canonical Interface
    ↓
Controlled Context
    ↓
Controlled Execution
    ↓
Explicit Artifacts
    ↓
Artifact Validation
    ↓
Automation
    ↓
Evidence
    ↓
Release Handoff
    ↓
Reproducibility
    ↓
Supply Chain Assurance
```

---

# Final Principle

The EPIC-BLD-001 Implementation Checklist is founded on the following rule:

> Implementation should introduce the minimum mechanism necessary to realize each Build Framework responsibility while preserving a clear path toward stronger trust.

FamilyOS does not need the largest possible build platform.

It needs a build capability that can evolve deliberately.

The first objective is simple and reliable canonical artifact production.

The next objective is validation and automation.

The next is traceability and evidence.

The next is reproducibility and strong release handoff.

Only then should more advanced supply-chain mechanisms be considered.

This checklist therefore transforms EPIC-BLD-001 from a normative architecture into a controlled implementation path for the FamilyOS Engineering Platform.
