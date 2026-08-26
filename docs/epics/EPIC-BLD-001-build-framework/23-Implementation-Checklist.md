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

* [x] Define repository-root detection.
* [x] Avoid developer-specific absolute paths.
* [x] Define canonical source paths.
* [x] Define canonical build configuration location.
* [x] Define canonical artifact output location.
* [x] Define canonical temporary/staging location if required.
* [x] Define generated-content ownership.
* [x] Separate generated content from authoritative source.
* [x] Prevent build artifacts from being written into source directories.
* [x] Ensure output directories can be safely cleaned.
* [x] Review `.gitignore` for derived build state.
* [x] Add structural validation where high-value.

Implementation evidence: `RepositoryLayout` derives canonical repository
structure exclusively from the configured project root. It identifies the
authoritative source, test, documentation, script, automation, specification,
template, project-configuration, and dependency-lock locations, while
separately identifying derived build-output locations.

`GitSourceStateProvider` accepts source-state authority only when the supplied
project root resolves to the exact Git repository root. Nested paths inside an
ancestor repository are rejected as repository authority. Repository paths are
derived from the project root rather than developer-specific absolute paths.

The canonical package output remains `dist/`. The CLI exposes `Path("dist")` as
a repository-relative interface default, while `RepositoryLayout` resolves the
canonical repository location as `<project-root>/dist`. Structural tests prove
that relative and absolute representations resolve to the same output
authority. Explicit safe output directories outside authoritative repository
content remain supported.

`RepositoryLayoutValidator` rejects the repository root itself, authoritative
repository directories and their descendants, and authoritative root files as
package-output destinations. `RunPackageBuildUseCase` performs this structural
validation before Build Context resolution and before `PackageBuilderPort`
execution, so unsafe destinations fail without package transformation.

Generated dependency ownership is explicit:
`pyproject.toml` is the dependency declaration authority,
`scripts/compile_dependencies.py` generates `requirements.txt`, and the
embedded dependency-input SHA-256 contract detects stale generated dependency
state. Generated dependency state therefore remains controlled without being
confused with its authoritative declaration.

Temporary wheel functional validation uses an operating-system-managed
`TemporaryDirectory` and explicitly rejects a temporary root that resolves
inside the repository checkout. No persistent repository-local staging
directory is required by the current canonical package-build pipeline.

Root `dist/`, root `build/`, generated `*.egg-info/`, and known tool caches are
classified as derived state and ignored by Git. The documented safe local
cleanup procedure removes only explicitly identified derived state and warns
against generalizing cleanup to authoritative or tracked repository content.

Focused repository-layout and validator tests cover canonical path derivation,
immutability, absence of developer-specific absolute paths, safe relative and
external outputs, repository-root rejection, authoritative directory and file
protection, and relative-output resolution. Package-build integration tests
prove the same structural boundary prevents builder execution for unsafe
destinations.

---

# Level 9 — Build Toolchain

## Objective

Make required build tooling explicit and verifiable.

### Checklist

* [x] Confirm canonical Python runtime requirement.
* [x] Define supported runtime versions.
* [x] Define canonical runtime for release-candidate builds if required.
* [x] Identify package build frontend.
* [x] Identify package build backend.
* [x] Identify Ruff version strategy.
* [x] Identify MyPy version strategy.
* [x] Identify Pytest version strategy.
* [x] Identify any required generators.
* [x] Document tool acquisition.
* [x] Validate critical tool availability.
* [x] Validate unsupported tool versions.
* [x] Ensure local and CI use compatible tooling.
* [x] Eliminate canonical dependence on undocumented global tools.
* [x] Add toolchain inspection capability if useful.
* [x] Add tests for toolchain validation logic.

Implementation evidence: the canonical package compatibility contract remains
`project.requires-python = ">=3.13"`, while the controlled development, CI, and
dependency-generation runtime is Python 3.13.x. The canonical minor runtime is
derived from repository configuration and validated as compatible with the
package-level Python requirement.

The package build frontend is PyPA `build`, invoked through the current Python
interpreter as `python -m build`. The backend is `setuptools.build_meta`, with
build-system requirements declared in `pyproject.toml`. The generated
dependency state pins the exact resolved versions used by the controlled
development and CI environment.

Ruff, MyPy, and Pytest compatibility requirements are declared in the
development dependency extra and their exact controlled versions are captured
by `requirements.txt`. Canonical validation executes those tools through the
same Python interpreter with `python -m ruff`, `python -m mypy`, and
`python -m pytest`, avoiding undocumented dependence on globally installed
executables.

`pip-tools` is the canonical dependency generator. Its requirement is declared
in `pyproject.toml`, its executing version is validated by the dependency
generation workflow, and dependency compilation is restricted to the
repository-controlled Python 3.13 minor runtime.

`ToolchainStateProvider` observes the installed critical package-build
toolchain in deterministic order. `ToolchainPolicyProvider` resolves the
repository-owned compatibility policy from `pyproject.toml`.
`ToolchainValidator` compares the observed runtime and tool versions with that
policy using PEP 440 version semantics and produces deterministic validation
findings.

Unsupported runtimes, unavailable required tool distributions, malformed
versions, malformed compatibility requirements, and incompatible tool
versions fail before package transformation. The exact validated
`ToolchainState` and runtime version are reused when resolving `BuildContext`;
toolchain state is captured once rather than observed independently before and
during context resolution.

The canonical local bootstrap installs the exactly pinned `requirements.txt`
state and then installs FamilyOS without dependency resolution. The canonical
GitHub Actions workflow uses Python 3.13 and the same locked bootstrap before
invoking the repository-owned validation command, keeping local and CI tooling
compatible.

Build Context and CLI rendering expose the effective runtime version and
critical toolchain distribution versions for inspection and evidence.
Toolchain policy, policy resolution, state observation, compatibility
validation, fail-fast integration, single-capture reuse, and runtime reuse are
covered by focused automated tests.

---

# Level 10 — Environment Management

## Objective

Ensure builds can be reconstructed from supported environment requirements.

### Checklist

* [x] Document supported development environment.
* [x] Document supported CI environment.
* [x] Validate Python runtime before build.
* [x] Detect active virtual environment where useful.
* [x] Define environment setup instructions.
* [x] Ensure a fresh virtual environment can reproduce the build.
* [x] Remove reliance on undeclared globally installed packages.
* [x] Identify required system tools.
* [x] Identify relevant filesystem requirements.
* [x] Identify relevant network requirements.
* [x] Define temporary-directory behavior.
* [x] Define cache locations.
* [x] Ensure caches remain optional.
* [x] Protect sensitive environment variables.
* [x] Minimize environment variable influence on artifact semantics.
* [x] Add environment-validation tests.

Implementation evidence: canonical environment observation now captures the
operating system, operating-system release, machine architecture, virtual-
environment state, temporary-directory location, and filesystem encoding as
non-sensitive Build Context state. Structural invariants are enforced by
`EnvironmentState`, while `EnvironmentValidator` verifies operational
temporary-storage availability before package transformation.

`RunPackageBuildUseCase` captures environment state once, validates it
fail-fast before invoking the package builder, and reuses the exact validated
observation when resolving `BuildContext`. Invalid environment state therefore
cannot silently proceed into canonical package construction. Focused tests
cover state invariants, provider observation, validation results, fail-fast
execution, and single-capture Build Context reuse.

The CLI exposes the effective non-sensitive environment state for inspection:
runtime version, operating system, operating-system release, machine
architecture, virtual-environment activity, temporary directory, filesystem
encoding, and critical toolchain versions.

Canonical package construction now passes an explicit sanitized environment to
`python -m build`. Python contamination variables including `PYTHONHOME`,
`PYTHONPATH`, `PYTHONSTARTUP`, `PYTHONUSERBASE`, `VIRTUAL_ENV`, and
`__PYVENV_LAUNCHER__` are removed, `PYTHONNOUSERSITE=1` is enforced, and
publication-only Twine/uv credentials are excluded. Ordinary environment state
needed for supported networking, proxy, certificate, and host behavior remains
available rather than adopting an unnecessarily restrictive platform-specific
allowlist.

The supported development and CI bootstrap uses Python 3.13, the generated and
exactly pinned `requirements.txt` dependency state, and FamilyOS installation
without additional dependency resolution. Git is the explicit external system
tool used for source-state observation; package, validation, and dependency
tooling executes through the controlled Python environment.

Filesystem, temporary-storage, network, cache, and environment-variable
requirements are defined by the Build Environment Management contract. Package
outputs and tool caches are derived state. Caches are optional performance
state and must not affect correctness. Network access may be required for
dependency acquisition and isolated package-build environments; successful
build execution does not claim offline capability.

Final fresh-environment acceptance was executed from one external Python 3.13
virtual environment with `include-system-site-packages = false`, user site
disabled, no repository `.venv`, no inherited `PYTHONPATH`, and no undeclared
manual package installation. The environment was bootstrapped exclusively from
the canonical repository dependency state and then executed the complete
sequence:

```text
Fresh Environment
      ↓
Canonical Bootstrap
      ↓
Canonical CI Validation
      ↓
Canonical CI Package Build
      ↓
Structural Validation
      ↓
Functional Validation
      ↓
Valid Canonical Artifacts
Canonical CI Validation passed dependency freshness, dependency consistency,
Ruff, MyPy, Pytest, and builtin plugin compliance. The subsequent CI-profile
package build succeeded and produced exactly one wheel and one source
distribution with no unexpected direct outputs. Python package structural
validation and wheel functional validation both reported `VALID`, and all
required Build Evidence checks passed.

The acceptance run began without package-cache dependence, used no global
packages or repository-local virtual environment, and left the live repository
unchanged. The deterministic `git status --short` digest was identical before
and after the audit and `git diff --check` remained clean.

---

# Clean Environment Acceptance

FamilyOS demonstrates:

```text
Fresh Environment
      ↓
Documented Setup
      ↓
Declared Dependencies
      ↓
Canonical Build
      ↓
Valid Artifact
# Level 11 — Dependency Management

## Objective

Make dependency state sufficiently explicit and reproducible.

### Checklist

* [x] Inventory runtime dependencies.
* [x] Inventory build dependencies.
* [x] Inventory development dependencies.
* [x] Inventory validation dependencies.
* [x] Remove undeclared build dependencies.
* [x] Confirm canonical dependency declaration source.
* [x] Define version-constraint strategy.
* [x] Evaluate dependency lock strategy.
* [x] Ensure CI installs from canonical definitions.
* [x] Validate dependency-resolution failures clearly.
* [x] Validate runtime compatibility.
* [x] Review unused dependencies.
* [x] Review duplicated dependency functionality.
* [x] Define dependency update workflow.
* [x] Define security review integration.
* [x] Capture dependency state in release-candidate evidence when appropriate.
* [x] Add dependency-resolution tests where practical.

Initial implementation evidence: commit `113148e` established and validated the
Python 3.13 development/CI dependency version-resolution baseline. Subsequent
canonical bootstrap, CI, build-isolation, hygiene, and fresh-environment work
completed the Level 11 dependency-management controls described below without
claiming completion of unrelated Build Framework levels.

Incremental isolated-backend evidence: canonical pypa/build execution now
receives the absolute committed `requirements.txt` path as dependency
constraints for both its isolated sdist environment and its separate isolated
wheel-from-sdist environment. Constraints restrict versions only for packages
the backend requests; they do not install the complete lock or reject an
otherwise resolvable dependency merely because it is absent. Build isolation
and network/cache dependence remain. This isolated-backend constraint mechanism
complements rather than replaces full environment installation from the
canonical lock. It does not establish the broader critical toolchain version
identity required by Level 40.

Undeclared-build-dependency closure: canonical package construction does not
depend on an undeclared Python distribution. The `build` frontend,
`setuptools` backend, `wheel` artifact support, `packaging` standards support,
and `pip-tools` dependency-state compiler are all represented in canonical
dependency declarations and the controlled resolution. Git remains an
explicitly documented external system prerequisite for source-state
observation and is not a Python dependency. Fresh-environment acceptance used
the repository-owned bootstrap without global packages, the repository-local
virtual environment, system site packages, or `PYTHONPATH` contamination.

Canonical CI dependency installation is:

```text
python -m pip install -r requirements.txt
python -m pip install --no-deps --no-build-isolation -e .
familyos validation ci --output ci-validation.json
familyos build --profile ci --output-dir dist --evidence-output build-evidence.json
```

`requirements.txt` is generated from the direct dependency authority in
`pyproject.toml`. CI does not introduce an independent dependency-installation
path that bypasses these controlled definitions. Isolated backend resolution
uses declared build-system requirements under the canonical lock constraints.
Dependency freshness plus dependency consistency are mandatory canonical CI
validation gates before package construction.

The unused-dependency review found an identified role for every remaining
direct dependency. `packaging` supports standards-aware requirement and version
handling; `typer` owns the CLI surface; `jinja2` owns template rendering;
`pyyaml` owns YAML loading; and `pydantic` owns configuration models and
validation. The development and build declarations assign `build` to package
frontend execution, `pytest` to tests, `ruff` to linting, `mypy` to static
typing, `types-PyYAML` to YAML type information, and `pip-tools` to
dependency-lock compilation; `setuptools` and `wheel` supply the declared
build backend and artifact support. Commit `53cc47f` (`chore(deps): remove
redundant direct rich dependency`) removed FamilyOS's redundant direct Rich
declaration. Rich remains in the controlled resolution only as a transitive
dependency of Typer and is not a FamilyOS-owned direct contract.

The duplicate-functionality review found no materially interchangeable direct
dependency pair. `build`, `setuptools`, and `wheel` perform complementary
frontend, backend, and artifact roles. Ruff linting and MyPy static typing are
distinct validation responsibilities, while `pip-tools` is the canonical
dependency-resolution and lock compiler. No duplicate direct CLI, YAML,
templating, validation/model, or packaging framework was identified.

Dependency-security review integration is now defined explicitly in
`10-Dependency-Management.md`. The contract identifies the complete controlled
direct and transitive dependency resolution through canonical declaration and
lock digests, defines dependency-change and release-candidate trigger points,
and establishes `PASS`, `FAIL`, `SKIPPED`, and `ERROR` outcome semantics.

Security Architecture remains authoritative for vulnerability policy, finding
interpretation, severity, exceptions, and risk acceptance. The Build Framework
owns dependency facts and evidence binding, while the Release Framework may
consume mature Security-owned conclusions for candidate qualification. CI
integration is deferred until a stable local Security-owned implementation
exists. This documentation contract does not select or implement a scanner,
query advisory intelligence, add a CI gate, or establish release-candidate
security blocking behavior. This contract itself does not capture dependency
state; the separate Level 11.4 implementation is described below.

The subsequent Level 11.4 evidence slice closes that separate gap. Every
`BuildEvidence` instance now carries the dependency state already captured in
its canonical `BuildContext`. JSON evidence exposes stable `pyproject.toml` and
`requirements.txt` identities with their existing SHA-256 digests, excludes
absolute checkout paths, and reports the validation profile corresponding to
the selected build profile, including `release-candidate`. This does not make
evidence-output selection mandatory based on profile policy.

---

# Dependency Reproducibility Milestone

Level 11 demonstrates the implemented flow:

```text id="3dpqmu"
Canonical Dependency Declaration
            +
Controlled Resolution State
            ↓
Reconstructable Dependency Environment
```

Fresh-environment acceptance and canonical CI validation establish this
capability for the supported Python 3.13 development and CI workflow. It does
not claim offline resolution, artifact equivalence, vulnerability scanning, or
release authority.

---

# Level 12 — Build Configuration

## Objective

Provide explicit and deterministic configuration behavior.

### Checklist

* [x] Inventory existing build configuration sources.
* [x] Identify canonical project configuration.
* [x] Define configuration precedence.
* [x] Define framework defaults where needed.
* [x] Define profile configuration.
* [x] Define explicit invocation overrides.
* [x] Minimize environment-variable overrides.
* [x] Validate final effective configuration.
* [x] Reject unknown critical settings.
* [x] Reject conflicting configuration.
* [x] Prevent arbitrary validation bypass.
* [x] Separate secrets from build configuration.
* [x] Make non-sensitive effective configuration inspectable.
* [x] Document configuration sources and precedence.
* [x] Add configuration-resolution tests.

---

# Configuration Resolution Acceptance

Equivalent configuration sources should resolve to equivalent effective configuration.

```text id="9oyyro"
Same Configuration Inputs
         ↓
Same Effective Configuration
```

Level 12.1 establishes the implementation-specific configuration contract in
`11-Build-Configuration.md`. The current model is a combined authority:
`pyproject.toml` owns project/package declarations and applicable tool
configuration; generated `requirements.txt` owns controlled dependency
resolution; typed registries own supported profile and target contracts; the
CLI owns the four supported invocation settings; bootstrap owns adapter wiring;
and Build Context providers contribute observed execution state rather than
user overrides. FamilyOS does not use a monolithic build-configuration file or
a generic environment-variable override namespace.

The documented precedence contract records the `development`,
`familyos-cli-package`, `dist`, disabled-functional-validation, and absent-
evidence defaults; explicit profile, output, functional-validation, and
evidence-output invocation behavior and repository-root resolution for both
package and evidence output.
It also records the duplicated but aligned `dist` representations in the CLI
and `RepositoryLayout`.

The profile contract distinguishes definition from enforcement. All four
profiles declare supported targets, validation scope, evidence requirements,
environment requirements, and artifact expectations. Current execution
enforces profile existence and target compatibility and captures the selected
profile. Typed `evidence_required` policy is enforced; descriptive validation,
environment, and artifact strings are deliberately not interpreted as runtime
rules.

The environment contract records that canonical build semantics have no
generic `FAMILYOS_*` environment override mechanism. Package construction
removes inherited Python contamination variables and common Twine/UV
publication credentials, forces `PYTHONNOUSERSITE=1`, and retains ordinary
networking, proxy, certificate, and tool-compatibility variables. Git,
temporary-directory, validation-subprocess, and permitted external-tool
environment influence remains explicit rather than being claimed as fully
isolated. Secrets remain outside typed Build Context and effective
configuration models and outside ordinary package-build responsibility.

Level 12.2 adds a focused immutable effective-configuration validation result
and a deterministic application-layer validator. After the one canonical
`BuildContext` is resolved, the validator checks its profile against the
resolved canonical profile definition, confirms target support, validates the
typed functional-validation value, and consumes the existing successful
repository-layout decision without duplicating path rules. This gate runs
before package construction; failure preserves the same Build ID, source
state, and resolved context and prevents builder execution. Focused tests also
prove that semantically equivalent default and explicit development/profile,
target, functional-validation, and `dist` inputs resolve equivalently. The
broader precedence/conflict matrix remains open.

Level 12.3 makes the remaining concrete typed conflicts executable without a
generic policy engine. Evidence output is now a repository-root-resolved,
first-class `BuildContext` destination. The final validator rejects a missing
destination for `ci` and `release-candidate`, consumes the repository-layout
decision that protects canonical source/dependency authorities and the package
output tree, and prevents builder/artifact execution on conflict. The CLI
writes only to the resolved context destination, eliminating process-working-
directory precedence.

Required input, repository-layout, toolchain, environment, effective-
configuration, artifact discovery, structural validation, and artifact
identity/integrity/manifest stages expose no supported disable configuration.
Build-input validation now defaults on for direct application use; optional
functional validation remains explicit and captured. CLI and direct-use-case
tests cover required-evidence rejection, safe evidence requests, path
conflicts, failure ordering, and repository-root path equivalence. This does
not turn descriptive profile strings into executable rules or claim that
separate CI/release qualification is performed inside package construction.

For acceptance, equivalent deterministic configuration inputs mean equivalent
canonical repository declarations, typed registry policy, explicit supported
invocation values, defaults, and fixed wiring. The expected result is the same
resolved profile, target, package/evidence output, and effective options.
Source, dependency, toolchain, runtime, platform, and temporary-directory
observations may differ, so equivalent configuration does not imply identical
complete `BuildContext` objects.

Level 12.4 adds an immutable `EffectiveBuildConfigurationView` derived from the
resolved Build Context and canonical profile definition. It exposes profile,
target, resolved local package/evidence destinations, functional-validation
selection, evidence-required/requested policy, and target support without
becoming another authority. The CLI renders the local path-bearing view, while
portable Build Evidence JSON records only profile, target, functional-
validation, evidence-required, evidence-requested, and target-supported state.
The evidence model rejects profile disagreement and never serializes checkout-
specific output or evidence paths in this section.

A dedicated configuration-resolution matrix proves canonical interface
defaults, explicit overrides, equivalent relative/absolute/normalized paths,
all four profile evidence policies, supported-target inspection, typed unknown-
value rejection, required-evidence and protected-path conflicts, process-CWD
independence, repeated determinism, immutable inspection state, and a closed
non-sensitive projection surface. It separately varies Build ID, source,
dependency, toolchain, runtime, platform, and temporary-directory observations
and proves they do not change equivalent effective configuration.

All Level 12 checklist items are now implemented. No generic configuration
abstraction, policy engine, configuration file, or environment-variable
override mechanism was introduced by Level 12.1 through Level 12.4.

---

# Level 13 — Build Execution

## Objective

Implement predictable and observable transformation from validated context to candidate artifacts.

### Checklist

* [x] Define build execution stages.
* [x] Define workspace initialization.
* [x] Define staging behavior.
* [x] Define generation stages where needed.
* [x] Define package assembly.
* [x] Define packaging execution.
* [x] Define output collection.
* [x] Define execution finalization.
* [x] Propagate mandatory stage failures.
* [x] Prevent ignored subprocess failures.
* [x] Ensure execution does not unexpectedly mutate authoritative source.
* [x] Define partial-output handling.
* [x] Define failure cleanup.
* [x] Define cancellation semantics if required.
* [x] Define retry policy for transient failures only.
* [x] Add execution-stage logging.
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

## Level 13.2 — Current Execution Contract Reconciliation

Status: DOCUMENTATION RECONCILED.

The current implementation has subsequently matured beyond the first packaging
slice described above.

The canonical application orchestration now validates build inputs, repository
layout, toolchain, environment, and effective configuration before packaging;
resolves immutable Build Context; executes the canonical package builder;
performs Artifact Discovery and package validation; establishes Artifact
Identity, Artifact Integrity, and Artifact Manifest; and optionally performs
wheel functional validation.

This reconciliation records that existing execution contract without assigning
new runtime behavior.

The implemented flow is sequential and fail-fast for mandatory dependent
operations, but that orchestration structure is not treated as a canonical
execution-stage observability model.

No stage-event type, structured stage history, stage timestamps, stage
durations, retry history, cancellation state, or execution trace is currently
part of the package-build result contract.

The existing unchecked Level 13 items therefore remain open unless their
specific behavior is already independently implemented and evidenced.

In particular, Define build execution stages and Add execution-stage logging
remain open for the subsequent Canonical Execution Observability slice rather
than being closed by documentation inference.

No production code, test behavior, artifact semantics, validation semantics,
Build Evidence semantics, release behavior, or publication behavior changes in
Level 13.2.

## Level 13.3 — Canonical Execution Observability

Status: IMPLEMENTED AND VALIDATED.

The canonical package-build result now carries immutable ordered execution
observations.

The implemented model defines thirteen canonical execution stages covering
validated inputs through optional wheel functional validation.

Each reached stage records its canonical identifier, terminal `SUCCEEDED` or
`FAILED` status, elapsed monotonic duration, and an optional diagnostic.

Successful execution without requested functional validation records twelve
ordered observations. Requested functional validation adds
`FUNCTIONALLY_VALIDATE_WHEEL` as the thirteenth and final stage when reached.

Mandatory failures remain fail-fast. The failing stage is recorded as `FAILED`,
and later dependent stages are not reported as executed.

The CLI renders the application-owned execution observations in canonical
order, including stage identifier, terminal status, duration, and diagnostic
when available.

This closes the Level 13 checklist items:

* Define build execution stages.
* Add execution-stage logging.

Workspace initialization, staging, generation-stage definition, execution
finalization, partial-output handling, cleanup, cancellation, and retry policy
remain open and are not implied by this observability slice.

Level 13.3 does not introduce Build Evidence, artifact trust, release,
publication, retry, cancellation, or general-purpose distributed tracing
semantics.

## Level 13.4 — Canonical Build Workspace Initialization

Status: IMPLEMENTED AND VALIDATED.

The canonical package-build orchestration now initializes an isolated,
Build-ID-scoped filesystem workspace after successful environment validation
and before Build Context resolution.

The workspace root is derived from the validated environment temporary
directory:

```text
<temporary-directory>/
└── familyos-build/
    └── <build-id>/
        ├── staging/
        └── intermediate/
```

The immutable `BuildWorkspace` model represents the canonical workspace layout.

`BuildWorkspaceInitializer` creates the workspace from the canonical Build ID
and the already-captured validated environment temporary directory.

Workspace initialization is represented by the canonical
`INITIALIZE_WORKSPACE` execution stage.

Initialization failure is fail-fast. An operating-system failure records
`INITIALIZE_WORKSPACE` as `FAILED`, preserves its diagnostic, and prevents
Build Context resolution, effective-configuration validation, packaging,
Artifact Discovery, and later dependent operations.

The canonical Python package builder continues to consume authoritative
`project_root` directly and continues to write package candidates to the
canonical output directory. Level 13.4 does not copy authoritative source into
the workspace and does not change PyPA or setuptools package-assembly behavior.

This closes the Level 13 checklist item:

* Define workspace initialization.

The following concerns remain open:

* Define staging behavior.
* Define generation stages where needed.
* Define package assembly.
* Define execution finalization.
* Define partial-output handling.
* Define failure cleanup.
* Define cancellation semantics if required.
* Define retry policy for transient failures only.

The existence of the `staging` directory does not by itself define staging behavior.

Level 13.4 does not introduce Build Evidence, artifact trust, release,
publication, retry, cancellation, cleanup, or distributed tracing semantics.

---

## Level 13.5 — Canonical Build Input Staging

Status: IMPLEMENTED AND VALIDATED.

The canonical package-build orchestration now stages authoritative package
inputs after successful effective-configuration validation and before package
execution.

`BuildInputStager` materializes the canonical package-build input set beneath
the Build-ID-scoped workspace:

```text
<workspace-root>/
├── staging/
│   └── project/
└── intermediate/
```

The immutable `StagedBuildInputs` model represents the staged project root.

The canonical staging contract materializes the root packaging inputs and the
`src/familyos_cli` package tree required by the FamilyOS CLI package build,
while excluding unrelated repository state and Python cache state.

Staging is represented explicitly by the canonical `STAGE_BUILD_INPUTS`
execution stage.

The current canonical execution vocabulary therefore contains fifteen stages
through optional wheel functional validation.

Successful execution without requested functional validation records fourteen
ordered observations. Requested functional validation adds
`FUNCTIONALLY_VALIDATE_WHEEL` as the fifteenth and final stage when reached.

Staging failure is fail-fast. A failed `STAGE_BUILD_INPUTS` observation retains
its diagnostic and prevents package execution, Artifact Discovery, artifact
validation, identity establishment, integrity establishment, manifest
construction, and functional validation.

Staging does not mutate authoritative project source.

The canonical Python package builder intentionally continues to consume
authoritative `project_root` directly. Level 13.5 therefore defines staging
behavior without claiming implementation of package assembly from staged
inputs.

This closes the Level 13 checklist item:

* Define staging behavior.

The following concerns remain open:

* Define generation stages where needed.
* Define package assembly.
* Define execution finalization.
* Define partial-output handling.
* Define failure cleanup.
* Define cancellation semantics if required.
* Define retry policy for transient failures only.

Level 13.5 does not introduce Build Evidence, artifact trust, release,
publication, cleanup, cancellation, retry, or distributed tracing semantics.

---

## Level 13.6 — Canonical Generation Requirement Resolution

Status: DEFINED AND VALIDATED.

The current canonical FamilyOS CLI package build does not require a dedicated
generation stage before package assembly.

The package-build input set is already materialized before execution. The
generated dependency lock `requirements.txt` participates as a controlled build
input, and its freshness against `pyproject.toml` is validated by canonical
build-input validation before staging.

The repository contains a broader FamilyOS generation subsystem for project,
domain, documentation, and other generation workflows. That subsystem is not
coupled to the current canonical package-build orchestration and is therefore
not inserted into the package-build stage sequence merely to satisfy the
framework vocabulary.

No new `GENERATE` execution stage is introduced for the current package target.

Generation remains target-dependent. A future build target that requires
generated source, schemas, manifests, metadata, documentation, resources, or
other derived package inputs must introduce explicit generation semantics,
including generator identity, source inputs, destination, ordering, freshness,
validation, and failure propagation.

This closes the Level 13 checklist item:

* Define generation stages where needed.

The following concerns remain open:

* Define package assembly.
* Define execution finalization.
* Define partial-output handling.
* Define failure cleanup.
* Define cancellation semantics if required.
* Define retry policy for transient failures only.

Level 13.6 introduces no production-code behavior and does not change the
current fifteen-stage execution vocabulary.

It does not introduce Build Evidence, artifact trust, release, publication,
cleanup, cancellation, retry, or distributed tracing semantics.

---

## Level 13.7 — Canonical Package Assembly

Status: IMPLEMENTED AND VALIDATED.

The canonical FamilyOS CLI package build now consumes the isolated project snapshot produced by `BuildInputStager`.

After successful `STAGE_BUILD_INPUTS`, package execution passes `StagedBuildInputs.project_root` to the canonical Python package builder rather than authoritative `project_root`.

The canonical assembly flow is:

```text
Authoritative Project
        ↓
BuildInputStager
        ↓
<workspace-root>/staging/project
        ↓
PythonPackageBuilder
        ↓
Canonical Output Directory
```

The output-directory contract is unchanged. Candidate wheel and source-distribution artifacts remain outside the temporary workspace in the resolved canonical output directory.

Application validation confirms staged project-root consumption and preservation of the canonical output directory.

Real PyPA validation from the staged snapshot succeeds and produces exactly one wheel and one source distribution without mutating tracked authoritative project source.

This closes the Level 13 checklist item:

* Define package assembly.

The following concerns remain open:

* Define execution finalization.
* Define partial-output handling.
* Define failure cleanup.
* Define cancellation semantics if required.
* Define retry policy for transient failures only.

Level 13.7 does not introduce Build Evidence, artifact trust, release, publication, cleanup, cancellation, retry, or distributed tracing semantics.

---

## Level 13.8 — Canonical Execution Finalization

Status: IMPLEMENTED AND VALIDATED.

Canonical package-build execution now terminates through one centralized
finalization boundary.

`BuildExecutionStage` contains sixteen canonical stages, with
`FINALIZE_EXECUTION` as the terminal stage.

All fourteen current terminal return paths in
`RunPackageBuildUseCase.execute()` are routed through `_finalize_result()`.

The terminal execution flow is:

    Last Reached Business Stage
            ↓
    FINALIZE_EXECUTION
            ↓
    CanonicalPackageBuildResult

Finalization is independent from the underlying build outcome.

A failed business stage remains failed and retains its diagnostic, while
`FINALIZE_EXECUTION` records successful establishment of the terminal result.

Successful execution without requested functional validation records fifteen
ordered observations.

Successful execution with functional validation records sixteen ordered
observations, with `FUNCTIONALLY_VALIDATE_WHEEL` immediately preceding
`FINALIZE_EXECUTION`.

Application validation confirms terminal finalization for successful,
functionally validated, and failed package execution paths.

Workspace-initialization and build-input-staging failures remain fail-fast,
with their failed observations preserved immediately before finalization.

All current terminal returns use the centralized finalization boundary.

This closes the Level 13 checklist item:

* Define execution finalization.

The following concerns remain open:

* Define partial-output handling.
* Define failure cleanup.
* Define cancellation semantics if required.
* Define retry policy for transient failures only.

Finalization does not perform cleanup and does not delete the Build-ID-scoped
workspace, staging state, intermediate state, or partial candidate outputs.

Level 13.8 does not introduce Build Evidence, artifact trust, release,
publication, cancellation, retry, or distributed tracing semantics.

---

## Level 13.9 — Canonical Partial-Output Handling

Status: IMPLEMENTED AND VALIDATED.

Canonical Python package execution now preserves process-level outputs created
or modified before unsuccessful package termination.

`PythonPackageBuilder` compares direct output-directory state before and after
execution for `SUCCEEDED`, `FAILED`, and `ERROR` outcomes.

Created or modified files are returned through `PackageBuildResult.outputs`.

On failed or errored package execution, these files remain partial
process-level outputs only.

Artifact Discovery is not executed after unsuccessful package execution.
Partial outputs are therefore not promoted to canonical candidate artifacts.

The application-level contract preserves:

    PackageBuildResult.outputs
            ↓
    CanonicalPackageBuildResult.execution.outputs

while:

    discovery = None
    candidates = ()

Application and integration validation confirm:

* new outputs produced before a non-zero frontend result are preserved;
* outputs produced before a frontend execution error are preserved;
* unchanged pre-existing output files are excluded;
* real failed package execution preserves its generated source distribution;
* failed package execution does not invoke Artifact Discovery;
* partial outputs are not promoted to candidate artifacts;
* terminal execution still ends through `FINALIZE_EXECUTION`.

This closes the Level 13 checklist item:

* Define partial-output handling.

The following concerns remain open:

* Define failure cleanup.
* Define cancellation semantics if required.
* Define retry policy for transient failures only.

Level 13.9 does not remove partial outputs and introduces no failure-cleanup
policy.

It does not introduce Build Evidence, artifact trust, release, publication,
cancellation, retry, or distributed tracing semantics.

---

## Level 13.10 — Canonical Failure Cleanup

Status: IMPLEMENTED AND VALIDATED.

Canonical package-build execution now removes Build-ID-scoped internal
workspace state after terminal non-successful execution.

`BuildWorkspaceCleaner` removes the complete canonical workspace rooted at:

    <temporary-root>/familyos-build/<build-id>/

Cleanup is invoked only after successful workspace initialization and only when
the terminal `CanonicalPackageBuildResult` is non-successful.

All current post-workspace terminal paths pass the active `BuildWorkspace` to
the centralized `_finalize_result()` boundary.

The cleanup policy preserves:

* the original build status;
* the original failure diagnostic;
* execution observations;
* `PackageBuildResult.outputs`;
* the canonical package output directory.

Process-level partial outputs therefore remain governed by Level 13.9 and are
not deleted by failure cleanup.

Successful builds preserve their workspace.

Failures that occur before workspace initialization do not invoke cleanup.

Application validation covers:

* failed package execution cleanup;
* errored package execution cleanup;
* successful workspace retention;
* partial-output preservation;
* effective-configuration failure cleanup;
* staging failure cleanup;
* artifact-validation failure cleanup;
* functional-validation failure cleanup.

Dedicated workspace-cleaner validation confirms complete workspace removal and
idempotence when the workspace is already absent.

This closes the Level 13 checklist item:

* Define failure cleanup.

The following concerns remain open:

* Define cancellation semantics if required.
* Define retry policy for transient failures only.

Level 13.10 does not introduce Build Evidence, artifact trust, release,
publication, cancellation, retry, or distributed tracing semantics.

---

## Level 13.11 — Canonical Cancellation Semantics

Status: DEFINED AND DEFERRED BY DESIGN.

The current canonical package-build implementation is synchronous and does not
expose a runtime cancellation boundary.

The current slice therefore does not introduce:

* a cancellation token or cancellation request API;
* asynchronous package-build execution;
* managed child-process termination;
* explicit `SIGINT` or `SIGTERM` orchestration;
* a runtime `CANCELLED` value in `PackageBuildStatus`.

`CANCELLED` remains a reserved lifecycle state.

The canonical runtime deliberately does not synthesize a `CANCELLED` build
result when it cannot reliably observe and control cancellation.

Host-level interruption semantics therefore remain outside the current
canonical package-build result model.

Future runtime cancellation support must provide an explicit execution boundary
capable of:

* observing cancellation requests;
* controlling the active child process;
* preserving diagnostics;
* preserving partial-output semantics;
* applying deterministic workspace cleanup;
* producing a non-successful deterministic terminal result.

This closes the Level 13 checklist item:

* Define cancellation semantics if required.

The following concern remains open:

* Define retry policy for transient failures only.

Level 13.11 introduces no runtime production-code change.

---

## Level 13.12 — Canonical Retry Policy

Status: DEFINED AND DEFERRED BY DESIGN.

The current canonical package-build runtime performs no automatic retries.

Automatic retry is permitted only when a future execution boundary can
explicitly and reliably classify a failure as transient.

The current runtime has no canonical failure-classification model capable of
making that distinction.

Therefore:

* deterministic failures are not retried;
* unknown or unclassified failures are not retried;
* `PackageBuildStatus.ERROR` does not imply retryability;
* `PackageBuildStatus.FAILED` does not imply retryability;
* the current package-build execution performs exactly one packaging attempt.

Potential future retry support must introduce explicit transient-failure
classification before automatic retry is allowed.

A future retry mechanism must also provide:

* a finite deterministic attempt limit;
* observable attempt counts;
* preserved diagnostics from failed attempts;
* preserved partial-output semantics;
* consistent workspace cleanup;
* deterministic terminal-result semantics.

This closes the Level 13 checklist item:

* Define retry policy for transient failures only.

No Level 13 Build Execution checklist items remain open.

Level 13.12 introduces no production runtime-code change.

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

* [x] Identify tests required before build.
* [x] Identify tests required after artifact creation.
* [x] Integrate existing Pytest suite.
* [x] Keep test configuration canonical.
* [x] Preserve unit-test ownership under Testing Framework.
* [x] Preserve integration-test ownership under Testing Framework.
* [x] Add package installation tests where required.
* [x] Add packaged CLI smoke tests where useful.
* [x] Ensure failed mandatory tests fail Build Validation.
* [x] Preserve test reports as evidence where needed.

### Implementation evidence

Testing execution and Testing Evidence remain owned by EPIC-TST-001.
The Build Framework consumes canonical testing authority rather than
introducing a second test-execution path.

For release-candidate builds, the CLI consumes the canonical `pytest`
gate from supplied CI Validation Evidence. A successful gate must carry
canonical Testing Evidence, and that evidence must be fresh for the
current project source state before the release-candidate package build
is allowed to proceed. Missing, stale, or indeterminate testing
authority blocks the release-candidate build.

Build Validation projects the consumed canonical `pytest` gate into the
required `release-readiness-testing` check. Failed or errored mandatory
testing authority therefore fails Build Validation without transferring
test execution ownership into the Build Framework.

Tests required after artifact creation reuse the canonical package
validation authority established by Level 16, including clean package
installation, import smoke validation, and installed CLI smoke
validation. Level 20 does not duplicate those post-artifact checks.

Pytest configuration remains canonical under the Testing Framework.
Unit-test and integration-test ownership likewise remain with
EPIC-TST-001. Build consumes their canonical validation result and
preserves the associated Testing Evidence through the validation and
build evidence boundaries where required.

No independent Pytest execution authority is introduced into the Build
application layer.

---

# Level 21 — Quality Framework Integration

## Objective

Expose Build Evidence to EPIC-QLT-001.

### Checklist

* [x] Identify build-specific quality signals.
* [x] Expose validation results.
* [x] Expose artifact validation status.
* [x] Expose reproducibility evidence when available.
* [x] Define build quality-gate inputs.
* [x] Avoid defining independent competing quality policy.
* [x] Document ownership boundaries.
* [x] Integrate quality-gate failure with CI where applicable.

### Implementation evidence

The Build Framework exposes build-specific quality signals through canonical
Build Validation and Build Evidence rather than defining an independent
Quality Framework.

Canonical Build Evidence records the source state, dependency state, critical
toolchain state, environment state, effective configuration, aggregate Build
Validation result, artifact manifest, and artifact integrity records. Its
deterministic JSON representation exposes these authorities for downstream
quality evaluation and automation.

Build Validation exposes individual validation checks with explicit check
identity, domain, requirement, status, and diagnostic information. Artifact
validation state is represented through the artifact and functional-artifact
validation domains and through the structural validation status recorded in
artifact-manifest entries.

Reproducibility-related evidence is exposed when currently available through
captured source, dependency, toolchain, environment, configuration, artifact
identity, manifest, and digest authorities. Level 21 does not claim
byte-for-byte reproducibility and does not introduce a synthetic
reproducibility decision. Stronger reproducibility assessment remains governed
by the dedicated reproducibility maturity levels.

Build quality-gate inputs are therefore the canonical Build Validation result
and the structured evidence authorities supporting it. Existing canonical
validation gates such as Ruff, MyPy, Pytest, dependency validation, build
validation, and artifact validation remain owned by their respective
frameworks and validation authorities. Build consumes or projects those
results where required instead of redefining their quality policy.

EPIC-QLT-001 remains responsible for cross-cutting quality rules, evidence
interpretation, quality-gate policy, and quality decisions. EPIC-BLD-001
remains responsible for producing reproducible build artifacts, enforcing
build-specific validation, and exposing trustworthy Build Evidence. Testing,
Quality, Compliance, Release, and other framework authorities retain their
existing ownership boundaries.

CI executes the canonical mandatory validation gates and fails when required
validation fails. The canonical package build, Build Evidence collection,
artifact transfer verification, artifact validation, and release-handoff
preparation therefore remain downstream of successful authoritative
validation rather than establishing a competing quality decision path.

No independent Quality Framework, quality-rule engine, or competing
cross-framework quality policy is introduced into the Build application
layer.

---

# Level 22 — Plugin Compliance Integration

## Objective

Integrate EPIC-PLUGIN-002 compliance authority without duplicating
plugin-compliance ownership inside the Build Framework.

### Checklist

* [x] Consume canonical builtin-plugin compliance authority.
* [x] Preserve EPIC-PLUGIN-002 ownership of compliance rules.
* [x] Require the canonical `official` compliance profile.
* [x] Reject successful compliance gates without plugin results.
* [x] Fail Build Validation when mandatory plugin compliance fails.
* [x] Preserve plugin-compliance authority across CI Validation Evidence.
* [x] Preserve plugin-compliance results in Build Validation and Build Evidence.
* [x] Avoid introducing a separate plugin build target without architectural need.

### Implementation evidence

Plugin compliance execution, rules, profiles, validators, findings, and
compliance decisions remain owned by EPIC-PLUGIN-002. The Build Framework
does not import or execute the compliance engine directly.

Release-candidate builds consume the canonical
`builtin-plugin-compliance` gate from supplied CI Validation Evidence.
The gate must use the canonical `official` profile. A successful gate
must also contain plugin evaluation results; an empty successful result
is rejected as insufficient compliance authority.

Build Validation projects the consumed compliance gate into the required
`official-plugin-compliance` check under the canonical `COMPLIANCE`
validation domain. Failed or errored compliance authority therefore
blocks release-candidate Build Validation without transferring
compliance execution ownership into the Build Framework.

Canonical CI Validation JSON preserves `profile_id`, plugin summaries,
plugin status, diagnostics, and rule outcomes across the renderer/loader
boundary. This allows release-candidate builds to consume the same
compliance authority produced by CI rather than reconstructing or
re-executing it.

The resulting `official-plugin-compliance` validation check is preserved
alongside `release-readiness-testing` and the other canonical Build
Validation authorities in Build Evidence.

The canonical Build target remains `FAMILYOS_CLI_PACKAGE`. Builtin
plugins are packaged and validated as components of that package, so
Level 22 does not introduce an artificial plugin-specific build target.

Repository-wide validation for this level completed with Ruff passing,
MyPy passing on 1338 source files, 1742 Pytest tests passing, and 114
targeted Level 22 contracts passing. Architectural guards confirmed zero
direct compliance-engine imports and zero compliance execution authority
inside the Build application layer.

---

# Level 23 — Documentation Build Integration

## Objective

Support documentation as controlled build input and output where appropriate.

### Checklist

* [x] Identify generated documentation activities.
* [x] Identify authoritative documentation sources.
* [x] Define generators.
* [x] Define documentation artifact outputs.
* [x] Validate generated documentation.
* [x] Detect stale generated documentation where useful.
* [x] Keep Documentation Framework ownership boundaries.
* [x] Avoid undocumented local documentation tooling.

### Implementation Status

Level 23 is complete as a documentation/build authority reconciliation level.

Repository inspection confirms that no canonical generated-documentation
activity currently participates in the FamilyOS package-build path. The
Documentation Framework describes future and optional automation capabilities,
including documentation indexes, API references, plugin catalogs, architecture
maps, validation, and CI integration, but no canonical documentation generator
or executable documentation-generation authority is currently implemented.

Authoritative repository documentation remains under the governance of
EPIC-DOC-001 and the authoritative semantics of the framework or domain that
owns the documented subject. EPIC-DOC-001 remains authoritative for
documentation architecture, standards, lifecycle, validation semantics, and
documentation governance. EPIC-BLD-001 remains authoritative for build
engineering.

No canonical documentation generator is selected by Level 23. Build does not
introduce MkDocs, Sphinx, pdoc, markdownlint, or another implicit local
documentation tool merely to satisfy this level. Future documentation
generation may participate in controlled build execution only when an
authoritative generator and its dependencies have been explicitly established.

No documentation artifact is currently emitted by the canonical package-build
path. `DOCUMENTATION_BUNDLE` remains an architectural artifact category
described by the Build Framework rather than evidence of an implemented
documentation generator or current package-build output.

Generated-documentation validation is therefore not currently applicable.
When generated documentation becomes an executable build output, its
documentation-specific validity must remain governed by Documentation
Framework contracts rather than being independently redefined by the Build
application layer.

Generated-output staleness detection is likewise not currently applicable
because there is no canonical generated documentation output to compare with
authoritative sources. General documentation staleness, reference integrity,
metadata validity, structural compliance, and lifecycle maintenance remain
Documentation Framework concerns. Future build integration may consume such
authoritative results without acquiring their semantic ownership.

The resulting Level 23 boundary is:

    Documentation Framework
        -> owns documentation semantics, standards, lifecycle, and validation

    Authoritative Documentation Contracts
        -> may be consumed by future controlled integration

    Build Framework
        -> owns build orchestration and artifact handling

    Generated Documentation Build Output
        -> exists only when an authoritative generator exists

Level 23 intentionally introduces no new Build application-layer service,
generator, validator, artifact producer, or documentation-specific build
target. This preserves the existing framework ownership boundary and avoids
creating an artificial executable capability for a documentation-generation
path that the repository does not currently implement.

---

# Level 24 — Build Evidence

## Objective

Create evidence sufficient to explain important builds.

### Initial Evidence Checklist

* [x] Build ID.
* [x] source revision.
* [x] target.
* [x] profile.
* [x] runtime version.
* [x] critical tool versions.
* [x] effective configuration summary.
* [x] validation result.
* [x] artifact manifest.
* [x] artifact digests.

The initial Build Evidence baseline is complete.

Canonical Build Evidence preserves the build target through the effective
configuration authority and preserves the captured runtime version directly
from Build Context without recalculating runtime state. Critical toolchain
versions are represented by `ToolchainState`, while the effective configuration
projection records the resolved build profile, target, functional-validation
policy, evidence policy, and target-support decision.

The canonical JSON evidence renderer projects these established authorities
without recalculating them. Toolchain and environment state are serialized from
their captured application-layer models, and checkout-local absolute paths are
excluded from portable dependency-state and effective-configuration identity
where they are not part of canonical evidence identity.

These capabilities complete the initial evidence checklist. The canonical
Build Evidence JSON now exposes the captured runtime version alongside source,
dependency, toolchain, environment, effective-configuration, validation,
manifest, and integrity evidence.

This completion does not introduce dependency-graph fingerprinting, synthetic
environment fingerprints, stage-result aggregation, reproducibility decisions,
provenance, signing, publication, promotion, or deployment semantics.

### Mature Evidence Checklist

* [ ] dependency graph identity.
* [ ] environment identity.
* [x] stage results.
* [ ] reproducibility status.
* [ ] provenance data.

### Mature Evidence Status

Stage-result evidence is now implemented by preserving the canonical ordered
`BuildExecutionObservation` sequence already produced by package-build
orchestration. `BuildEvidenceFactory` reuses those observations directly
without recalculating stage outcomes or timing, and canonical Build Evidence
JSON exposes each reached stage with its stage identifier, terminal status,
elapsed monotonic duration, and optional diagnostic.

Stage duration is execution evidence rather than Build Context identity.
Preserving it does not imply that equivalent builds must have equal timings.

The remaining mature evidence capabilities intentionally remain open:

* Dependency graph identity remains deferred. The current `DependencyState`
  provides declaration and lock-file identities and SHA-256 digests, but the
  Build Framework has not yet established a canonical resolved dependency-graph
  fingerprint. Plugin dependency-graph models belong to plugin ecosystem
  resolution and are not Build dependency-graph identity.
* Environment identity remains deferred beyond the currently captured
  `EnvironmentState`. FamilyOS already records relevant non-sensitive
  environment properties, but canonical environment fingerprinting remains a
  future maturity capability.
* Reproducibility status remains deferred to the dedicated reproducibility
  maturity work. Current evidence must not synthesize a reproducibility verdict
  before canonical comparison and fingerprint semantics exist.
* Provenance data remains deferred to later supply-chain maturity. Level 24 does
  not introduce provenance attestations, signing, SLSA semantics, publication,
  promotion, or deployment authority.

Level 24 therefore establishes the complete initial Build Evidence baseline and
the currently available mature execution-stage evidence while preserving the
explicit maturity boundaries for dependency-graph identity, environment
fingerprinting, reproducibility assessment, and provenance.

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

* [x] Define Build Result representation.
* [x] Include Build ID.
* [x] Include target.
* [x] Include profile.
* [x] Include execution status.
* [x] Include validation status.
* [x] Include artifact set.
* [x] Include evidence reference.
* [x] Include failure diagnostics.
* [x] Ensure failed builds still return useful structured information.
* [x] Add serialization if machine-readable automation requires it.

Implementation evidence: `CanonicalBuildResult` aggregates the established package
build, optional Build Validation result, and optional Build Evidence reference
without recalculating those authorities. It projects the canonical Build ID,
target, profile, package execution status, validation status, artifact manifest,
and final diagnostic. `CanonicalBuildResultFinalizer` assembles that result for
all public `familyos build` exit paths: failed builds, successful builds with
Build Evidence, and successful builds without Build Evidence. Failed builds
therefore retain structured package diagnostics while leaving unavailable
validation and evidence authorities explicitly absent. No separate
`CanonicalBuildResult` serialization is currently required: machine-readable
Build Evidence is already emitted through the canonical Build Evidence JSON
contract, avoiding a redundant second result authority.

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
* [x] Separate build credentials from release credentials.
* [x] Prevent release credentials in pull-request builds.
* [x] Limit secret scope.
* [x] Prevent secrets from reaching untrusted execution contexts.
* [x] Review third-party CI actions or integrations.
* [x] Pin critical external automation dependencies where governance requires it.
* [x] Document CI security assumptions.

Implementation evidence: the canonical GitHub Actions workflow explicitly uses
repository permission `contents: read` and does not request write-capable
repository, package, deployment, security-event, or OIDC token permissions.

Ordinary canonical validation and package-build execution require no release,
publication, signing, promotion, deployment, registry, or production
credentials. The workflow contains no `${{ secrets.* }}` references and does
not pass repository secrets into canonical build commands or action inputs.
Build credentials and release credentials are therefore separated by absence:
the Build workflow owns no release credential authority.

The workflow supports ordinary `pull_request` execution but does not use
`pull_request_target`. Pull-request builds consequently execute the same
non-privileged validation and package-build path without release credentials.
Any future privileged Release workflow must remain separately governed by the
Release Framework and must not extend those credentials into ordinary Build or
pull-request execution.

External GitHub Actions used by canonical CI are reviewed and pinned to
immutable commit SHAs. The executable CI security contract is protected by
`tests/unit/interfaces/cli/test_ci_security_policy.py`, which rejects privileged
token permissions, repository-secret references, `pull_request_target`,
release/publication operations, and unpinned external actions.

Level 28 — CI Permissions is complete.

---

# Level 29 — CI Caching

## Objective

Improve performance without changing semantics.

### Checklist

* [x] Identify safe dependency caches.
* [x] Define cache key inputs.
* [x] Include runtime state in cache identity where required.
* [x] Include dependency state in cache identity.
* [x] Ensure cache miss still produces correct build.
* [x] Ensure corrupted cache can be discarded.
* [x] Validate cache-free builds periodically.
* [x] Avoid cache dependence for authoritative state.

Implementation evidence: canonical CI uses only the pip dependency cache exposed
by the pinned Python setup action. The cache is scoped by the explicit Python
runtime and by `requirements.txt` through `cache-dependency-path`, preserving
runtime and canonical dependency state in cache identity.

Dependency installation remains authoritative on every ordinary CI execution:
`python -m pip install -r requirements.txt` still executes after cache
restoration, and FamilyOS installation remains explicitly independent of a
cached virtual environment through `--no-deps --no-build-isolation -e .`.

Authoritative Build outputs and evidence are not used as dependency-cache
inputs. Package candidates, Build Evidence, validation evidence, local virtual
environments, and build-output directories therefore remain outside the
canonical dependency-cache authority.

A dedicated `cache-free-validation` job restores no dependency cache and
installs locked dependencies with `--no-cache-dir`. It executes canonical CI
validation and the canonical CI-profile package build from cache-free dependency
state.

The cache-free path runs periodically through the scheduled CI trigger and can
also be invoked explicitly through `workflow_dispatch`. This provides a
controlled recovery path for suspected or corrupted cache state without making
cache clearing, cache retry, or cached state authoritative to Build semantics.

The executable contract is protected by
`tests/unit/interfaces/cli/test_ci_caching_policy.py`, covering safe cache
selection, dependency/runtime cache identity, cache-miss correctness,
authoritative-state separation, periodic cache-free validation, and explicit
manual cache-free recovery.

Level 29 — CI Caching is complete at 8/8.

---

# Level 30 — Artifact Transfer Across CI Jobs

## Objective

Preserve exact artifact identity across automation stages.

### Checklist

* [x] Build artifact once.
* [x] Calculate digest.
* [x] Upload same artifact.
* [x] Download artifact in validation or release preparation stage.
* [x] Recalculate digest.
* [x] Compare digest.
* [x] Reject changed artifact.
* [x] Avoid rebuilding between build and validation jobs.

### Implementation Evidence

* The canonical `validate` job performs the package build once and
  uploads the resulting `dist/` candidates without rebuilding them.
* Canonical Build Evidence records SHA-256 artifact integrity metadata
  for the produced package candidates.
* `familyos-package-candidates` transfers the exact candidate bytes
  from the canonical build job to the downstream
  `artifact-validation` job.
* `familyos-build-evidence` transfers the corresponding canonical
  Build Evidence separately from the candidate bytes.
* The downstream artifact-validation stage recalculates SHA-256
  digests from the downloaded candidate bytes and compares them with
  the canonical integrity records.
* Missing, unexpected, or digest-mismatched artifacts cause downstream
  integrity validation to fail.
* The downstream artifact-validation job contains no package build
  operation and therefore validates transferred artifacts rather than
  silently rebuilding them.
* Structural and behavioral CI contracts cover producer/consumer
  identity, evidence separation, action pinning, no-rebuild semantics,
  successful identical-byte verification, and rejection of mutated,
  missing, or unexpected artifacts.

Level 30 — Artifact Transfer Across CI Jobs is complete at 8/8.

---

# Level 31 — Build-Once-Promote

## Objective

Prepare strong Build/Release integration.

### Checklist

* [x] Identify trusted artifact after Build Validation.
* [x] Preserve trusted artifact bytes.
* [x] Preserve digest.
* [x] Preserve Build ID.
* [x] Preserve validation evidence.
* [x] Provide explicit Release Handoff.
* [x] Ensure Release workflow consumes existing artifact.
* [x] Prevent downstream silent rebuild.
* [x] Verify artifact integrity before promotion.

### Implementation Evidence

* `CanonicalBuildResult.release_handoff_eligible` identifies Build
  results whose execution, Build Validation, Build ID, artifact manifest,
  and evidence authorities are coherent and suitable for Release handoff.
* `ReleaseHandoff` explicitly preserves the canonical Build ID,
  artifact manifest, validation result, and Build Evidence reference
  without recalculation or substitution.
* Artifact paths and digest records are projected directly from the
  canonical artifact manifest, preserving the identity and integrity
  authorities established during Build.
* `ReleaseHandoffConsumer` consumes the exact handoff object without
  rebuilding artifacts, recalculating digests, or replacing Build
  authorities.
* Canonical CI performs the package build once in the producer job.
* `artifact-validation` downloads those exact package candidates and
  canonical Build Evidence, recalculates SHA-256 from the transferred
  bytes, and rejects missing, unexpected, or changed artifacts.
* The downstream `release-handoff` job depends on successful artifact
  validation and downloads the same validated package candidates and
  Build Evidence without rebuilding them.
* Build remains responsible only for preparing the Release handoff;
  publication, approval, promotion, and deployment authority remain
  outside the Build Framework.

Level 31 — Build-Once-Promote is complete at 9/9.

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

* [x] Require identifiable source revision.
* [x] Require appropriate clean working-tree state.
* [x] Require canonical runtime.
* [x] Require controlled dependency resolution.
* [x] Require validated toolchain.
* [x] Require controlled environment.
* [x] Require complete source validation.
* [x] Require complete test suite applicable to release readiness.
* [x] Require artifact validation.
* [x] Require integrity digests.
* [x] Require Build Evidence.
* [x] Produce explicit release handoff.
* [x] Do not publish automatically from Build Framework.

---

# Level 33 — Observability

## Objective

Make build execution understandable.

### Checklist

* [x] Log Build ID.
* [x] Log target.
* [x] Log profile.
* [x] Log stage progression.
* [x] Log important stage duration.
* [x] Report artifacts.
* [x] Report validation failures.
* [x] Avoid secret logging.
* [x] Define debug diagnostics.
* [x] Define machine-readable output if needed.
* [x] Distinguish warning from error.
* [x] Ensure CI failure points remain visible.

### Implementation Status

Level 33 observability is complete for the current Build Framework scope.

Canonical build output exposes the Build ID, target, profile, ordered execution
stage progression, elapsed stage durations, produced artifacts, and validation
diagnostics. The same established build authorities are projected into
machine-readable Build Evidence JSON without recalculating build state.

Build Validation distinguishes blocking failures from non-blocking warnings
through explicit requirement classification. Failed `REQUIRED` checks are
reported as failures, while failed `OPTIONAL` checks remain observable as
warnings without invalidating the aggregate decision solely for that reason.

Debug diagnostics are governed by the existing Build execution and
configuration contracts, including diagnostic verbosity and developer
diagnostics. Level 33 does not require inventing a new CLI debug mode where no
additional diagnostic capability is currently required.

Build observability must not expose credentials, secrets, or other protected
information. Generic logging, telemetry security, filtering, and redaction
policy remain owned by EPIC-OBS-001; the Build Framework supplies
build-specific observable facts without creating a competing observability
infrastructure.

Canonical CI preserves failure visibility while retaining validation evidence.
The canonical validation step may continue temporarily so that its evidence can
be uploaded, but the subsequent preservation step explicitly restores the
failed workflow result. Downstream artifact validation and release handoff
remain dependency-gated and therefore do not hide an upstream Build failure.

Level 33 introduces no new logging backend, telemetry transport, secret
redaction engine, metrics framework, tracing framework, publication authority,
or deployment authority.

---

# Level 34 — Build Metrics

## Objective

Introduce metrics only where they support decisions.

### Potential Metrics

* [ ] total build duration;
* [x] stage duration;
* [ ] build success rate;
* [ ] failure category;
* [ ] artifact validation failure rate;
* [ ] dependency resolution failure rate;
* [ ] environment validation failure rate;
* [ ] cache hit rate;
* [ ] retry rate;
* [ ] reproducibility result.

Metrics should not become requirements merely because they can be measured.

### Current Metrics Status

Stage duration is already established as canonical Build execution evidence.
Each completed `BuildExecutionStage` produces an immutable
`BuildExecutionObservation` containing its terminal status and elapsed monotonic
duration. These observations are preserved by `CanonicalPackageBuildResult`,
propagated into Build Evidence, and exposed through the established Build
rendering paths.

This existing execution evidence satisfies the current Build-owned requirement
for stage-duration measurement without introducing a second timing authority or
a parallel metrics subsystem.

The remaining potential metrics intentionally remain open:

* Total build duration has no canonical measurement boundary yet. It must not be
  synthesized by summing stage durations because future orchestration may
  include parallel, overlapping, or otherwise non-additive execution.
* Build success rate requires aggregation across multiple build executions and
  therefore is not a property of one canonical build result.
* Failure category remains owned by the dedicated Level 35 failure
  classification work.
* Artifact-validation, dependency-resolution, and environment-validation
  failure rates require aggregation semantics that are not yet established.
* Cache hit rate remains deferred until canonical cache behavior and measurement
  semantics exist.
* Retry rate remains deferred until canonical retry behavior exists.
* Reproducibility result remains deferred until canonical reproducibility
  comparison semantics exist.

EPIC-BLD-001 remains authoritative for Build execution semantics. This level
does not introduce a Build-specific metrics backend, external telemetry
dependency, historical aggregation store, or duplicate observability
abstraction.

---

# Level 35 — Failure Classification

## Objective

Improve diagnostics through consistent failure categories.

### Checklist

* [x] Define input failure category.
* [x] Define configuration failure category.
* [x] Define dependency failure category.
* [x] Define toolchain failure category.
* [x] Define environment failure category.
* [x] Define execution failure category.
* [x] Define artifact failure category.
* [x] Define validation failure category.
* [x] Define integrity failure category.
* [x] Ensure diagnostics include corrective information.
* [x] Add failure-path tests.

### Implementation Status

Level 35 failure classification is complete for the current Build Framework
scope.

`BuildFailureCategory` establishes nine stable machine-readable categories:
input, configuration, dependency, toolchain, environment, execution, artifact,
validation, and integrity.

Classification is a projection over already established Build authorities. It
does not parse free-form diagnostic text. Failed required Build Validation
checks are classified from their `BuildValidationDomain`. When no more specific
failed validation authority exists, failed `BuildExecutionObservation` stages
provide the classification. A failed package result without a classified stage
falls back to the execution category.

Validation-domain and execution-stage mappings are exhaustive. Tests compare
the mapping sets with the complete enums so that introducing a new domain or
execution stage requires an explicit failure-classification decision.

Specialized validation domains preserve the Level 35 vocabulary without
creating undocumented categories. Source failures project to input; metadata
and functional-artifact failures project to artifact; testing, compliance, and
evidence failures project to the general validation category.

`CanonicalBuildResult` exposes the terminal `failure_category` while preserving
the existing diagnostic authority. Build Evidence remains factual evidence and
does not duplicate this derived result projection.

Each failure category also has stable corrective information. The correction is
derived from the structured category rather than inferred from diagnostic text.
On failed CLI builds, the canonical final result is now consumed and renders
both `Failure Category` and `Corrective Action` in addition to the original
failure diagnostic.

This level does not introduce a separate diagnostic subsystem, diagnostic-text
parser, failure-history store, telemetry backend, or additional Build Evidence
authority.

Failure-path tests cover successful absence, validation-domain classification,
execution-stage classification, precedence of required validation failures,
execution fallback, corrective-information projection, and CLI rendering.

---

# Level 36 — Build Security

## Objective

Integrate secure build principles from the beginning.

### Checklist

* [x] Minimize build-process privileges.
* [x] Keep production credentials out of normal builds.
* [x] Keep release publication credentials out of normal builds.
* [x] Protect registry credentials.
* [x] Avoid secret logging.
* [x] Detect accidental secret inclusion in artifacts where practical.
* [x] Review build dependencies for supply-chain risk.
* [x] Review generators for trust risk.
* [x] Review network access.
* [x] Avoid unrestricted external execution.
* [x] Control subprocess arguments.
* [x] Avoid unsafe shell command construction.
* [x] Document build security assumptions.

### Current Build Security Boundary

The canonical Build path operates without production or release-publication
credentials. Publication remains outside ordinary package construction, and
the package-build environment explicitly excludes publication-only Twine and
uv credential variables.

Canonical Build Context, environment state, and effective-configuration
projections intentionally expose only non-sensitive state. Existing tests
protect that closed projection surface, while Build Validation documentation
requires diagnostics not to expose secrets discovered in configuration or
environment state.

The canonical package builder executes the declared PyPA build frontend through
the current Python interpreter using explicitly constructed subprocess
arguments. Build execution does not require shell command construction or
arbitrary user-provided executable selection. Critical package-build tooling is
declared, version-controlled through the canonical dependency state, observed,
and validated before package transformation.

Artifact validation establishes a closed expected package-content boundary for
the canonical wheel and source distribution. Unexpected package content is
rejected. This provides the currently practical Build-owned protection against
accidental inclusion of repository-local or otherwise unintended content.
Build does not introduce a general-purpose secret-scanning subsystem at this
maturity.

Dependency supply-chain responsibilities are deliberately split by authority.
Build owns canonical dependency declarations, controlled resolution state,
dependency freshness, dependency identity, and evidence binding. Security
Architecture remains authoritative for vulnerability policy, severity,
exceptions, finding interpretation, and risk acceptance. Level 36 therefore
does not introduce a duplicate vulnerability scanner or Build-specific
security-policy authority.

Generator trust is controlled according to actual target requirements. The
current canonical FamilyOS CLI package target has no dedicated GENERATE stage.
Its generated dependency lock is materialized before execution, has an explicit
repository-owned generator, and is freshness-validated before packaging.
Future targets requiring generated source, schemas, manifests, metadata,
documentation, resources, or other derived inputs must define generator
identity, source inputs, destination, ordering, freshness, validation, and
failure propagation before those outputs may enter canonical execution.

Network access is explicit rather than assumed absent. Dependency acquisition
and isolated package-build environments may require supported network access.
The Build Framework does not claim offline execution. Network behavior remains
limited to the requirements of the declared build and dependency tooling; the
canonical Build orchestration does not provide an unrestricted external-command
execution facility.

Build-process privilege remains proportional to Build responsibility. Ordinary
build execution does not own deployment, production access, artifact
publication, release promotion, or credential authority. Stronger release,
security, signing, provenance, or trusted-builder controls remain the
responsibility of their owning frameworks or future maturity levels.

Level 36 therefore closes through existing implementation, validation, and
documented authority boundaries. No Build-specific secret backend,
vulnerability scanner, credential store, security-policy engine, or parallel
security subsystem is introduced merely to satisfy the checklist.

Level 36 — Build Security is complete at 13/13.

---

# Level 37 — Build Governance Implementation

## Objective

Make `16-Build-Governance.md` operational.

### Checklist

* [x] Define Build Framework ownership.
* [x] Define build implementation ownership.
* [x] Define toolchain ownership.
* [x] Define CI ownership.
* [x] Define artifact ownership.
* [x] Define routine-change review path.
* [x] Define significant-change review path.
* [x] Define ADR threshold.
* [x] Define RFC threshold.
* [x] Define exception process.
* [x] Define technical-debt tracking.
* [x] Define build-security escalation.
* [x] Define artifact-contract change review.
* [x] Define validation-weakening review.
* [x] Document governance process.

### Implementation Status

Level 37 operationalizes the governance architecture already defined by
`16-Build-Governance.md` without introducing a runtime governance subsystem.

The current ownership contract distinguishes Build Framework architecture,
canonical Build implementation and maintenance, critical toolchain ownership,
provider-specific CI automation, artifact construction and trust semantics, and
downstream Release ownership. CI remains subordinate to canonical Build
semantics and must not become an independent Build authority.

Build changes follow an explicit four-class review model. Routine Class 1
changes use normal code or documentation review with appropriate validation.
Significant Class 2 changes require explicit technical review. Class 3 changes
that establish or modify significant Build architecture require an ADR. Class 4
changes that affect broader platform strategy or multiple architectural areas
require an RFC, with EPIC evolution when framework responsibilities, structure,
or long-term requirements change.

Exceptions to normative Build requirements must be recorded with their reason,
scope, authority, accepted risk, compensating controls where applicable, and
remediation, review, or expiry conditions. Repeated or structural exceptions
must be treated as technical debt or as proposals to change the governing
architecture.

Build technical debt must remain visible through repository-owned tracking and
be prioritized according to impact and risk. Security-sensitive changes
involving credentials, trust boundaries, dependency sources, network authority,
signing, privileged execution, or comparable concerns require Security
Architecture review.

Artifact-contract changes require compatibility review against downstream
consumers. Breaking changes require rationale, migration impact, documentation,
and appropriate version or release handling. Removal, bypass, disabling, or
weakening of mandatory Build validation requires explicit technical
justification and review and must not be performed merely to make execution
pass.

The operational governance path is:

```text
Proposed Change
      ↓
Assess Scope And Risk
      ↓
Classify Change
      ↓
Select Required Review
      ↓
Record ADR / RFC / Exception / Debt When Required
      ↓
Implement
      ↓
Validate
      ↓
Synchronize Documentation
      ↓
Adopt
```

Governance evidence remains repository-visible through ADRs, RFCs, review and
exception records, validation evidence, revision history, changelog entries,
manifest updates, and synchronized EPIC lifecycle metadata as applicable.

Level 37 — Build Governance Implementation is complete at 15/15.

---
# Level 38 — Documentation Synchronization

## Objective

Ensure implementation and documentation remain aligned.

### Checklist

* [x] Update Build Framework when architecture changes.
* [x] Update developer build instructions.
* [x] Update CLI reference when build interface changes.
* [x] Update CI documentation.
* [x] Update toolchain documentation.
* [x] Update environment setup.
* [x] Update dependency workflow.
* [x] Update artifact documentation.
* [x] Update release handoff documentation.
* [x] Update ADRs/RFCs when applicable.
* [x] Prevent permanent implementation/documentation drift.

### Implementation Status

Level 38 reconciles the Build Framework documentation with the implemented
state established through the preceding Build Framework levels.

Architecture and governance changes remain synchronized through the canonical
Build Framework documentation set, including Build Architecture, Build
Governance, Build Automation and CI, Artifact Management, Build Validation,
Release, and the progressive Implementation Checklist.

Developer build instructions document the supported Python 3.13 environment,
virtual-environment bootstrap, canonical dependency installation, dependency
freshness workflow, local validation, canonical package build, and evidence
generation paths.

The documented CLI surface tracks the implemented Build command semantics,
including canonical Build ID, Build Profile, Build Target, functional
validation, output-directory behavior, and Build Evidence output.

CI documentation remains aligned with canonical local Build semantics and
documents provider-specific automation as an integration layer rather than an
independent Build authority. Current documentation covers canonical CI
validation, package construction, Build Evidence collection, artifact transfer,
integrity verification, cache policy, and release-handoff consumption without
downstream rebuilding.

Toolchain, environment, and dependency documentation describe the implemented
runtime, governed package-build tooling, environment expectations, exactly
resolved dependency state, generated requirements workflow, freshness checks,
and canonical dependency evidence.

Artifact documentation reflects implemented Artifact Discovery, Artifact
Identity, Artifact Integrity, Artifact Manifest, Build Evidence association,
validation semantics, lifecycle boundaries, and transfer verification.

Release-handoff documentation reflects the build-once handoff model in which
validated package candidates and Build Evidence are transferred downstream
without rebuilding and without granting Build publication, promotion, or
deployment authority.

ADR and RFC synchronization follows the operational Build Governance contract.
Class 3 architectural changes require an ADR; Class 4 strategic or
cross-platform changes require an RFC, with EPIC evolution where framework
responsibilities or long-term requirements change.

Permanent documentation drift is explicitly prohibited by Build Governance and
Build Automation documentation. The Level 38 audit itself detected and repaired
an unclosed historical Markdown fence in `VALIDATION.md`, restoring structural
validity without changing the recorded validation evidence.

Documentation synchronization remains an ongoing governance responsibility.
Future implementation changes must update the applicable authoritative
documentation before drift becomes permanent.

Level 38 — Documentation Synchronization is complete at 11/11.

---
# Level 39 — Build Technical Debt

## Objective

Identify and reduce legacy build behavior.

### Checklist

* [x] Inventory legacy build scripts.
* [x] Inventory duplicate build commands.
* [x] Inventory CI-specific build logic.
* [x] Inventory duplicated configuration.
* [x] Inventory obsolete environment assumptions.
* [x] Inventory unowned tools.
* [x] Inventory permanently skipped validations.
* [x] Inventory manual release preparation steps.
* [x] Prioritize debt by impact and risk.
* [x] Remove obsolete paths after migration.
* [x] Document accepted temporary debt.

### Current Technical-Debt State

The Level 39 repository audit found no active legacy Build script, duplicate
canonical Build command, independent CI-only Build semantic path, unowned
critical Build tool, permanently skipped mandatory Build validation, or
Build-owned manual release-preparation path.

The repository contains `install-epics.sh` for documentation installation and
`scripts/doctor.sh` for developer diagnostics. Neither implements or replaces
the canonical Build path.

Canonical package construction remains exposed through `familyos build`.
The infrastructure-owned Python package builder invokes the declared PyPA
frontend internally; that adapter is part of the canonical implementation and
does not constitute a second user-facing Build authority.

CI remains a thin automation adapter around canonical validation and Build
semantics. Its temporary `continue-on-error` on canonical CI validation exists
only so validation evidence can be uploaded. The subsequent
`Preserve canonical validation result` step explicitly exits non-zero whenever
the canonical validation outcome is not successful.

Canonical Build configuration remains centered on repository-owned
`pyproject.toml` and generated `requirements.txt` dependency state. No
conflicting active package-manager or Build configuration authority was found.

The canonical documentation baseline reports zero duplicate numbered documents
and zero legacy files. No active legacy Build-named path was found by the
repository audit.

### Accepted Temporary Debt

One known maintenance debt remains accepted:

* pinned GitHub Actions used by Canonical CI have historically emitted a
  Node.js runtime deprecation warning and may require action-version upgrades.

This debt is maintenance-level rather than correctness-critical. Canonical CI
continues to pass, Build semantics are unaffected, and no weakened permission,
validation, artifact-integrity, or release boundary results from the warning.

The remediation path is to upgrade the affected official GitHub Actions through
normal CI maintenance and revalidate the existing workflow contracts. It must
not be addressed by weakening validation, changing Build semantics, or granting
additional permissions.

Capabilities intentionally scheduled for Levels 40 through 49, including
broader reproducibility, provenance, SBOM evaluation, signing evaluation,
controlled builders, registries, remote execution, and performance maturity,
are planned maturity work and are not classified as current technical debt.

Level 39 — Build Technical Debt is complete at 11/11.

---
# Level 40 — Reproducibility Baseline

## Objective

Move from repeatable procedure toward reconstructable Build Context.

### Checklist

* [x] Establish canonical source identity.
* [x] Establish deterministic configuration resolution.
* [x] Establish controlled dependency state.
* [x] Establish critical toolchain version identity.
* [x] Establish reconstructable environment setup.
* [x] Remove time-dependent artifact content where unnecessary.
* [x] Remove random artifact content where unnecessary.
* [x] Normalize input ordering where relevant.
* [x] Reduce uncontrolled network dependency.
* [x] Compare repeated builds.
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

### Current Reproducibility Baseline

Canonical Python package construction now normalizes `SOURCE_DATE_EPOCH` to
`315532800` at the package-builder execution boundary.

Repeated canonical validation-profile builds from equivalent controlled inputs
produced equivalent logical artifacts.

The Python wheel was byte-for-byte identical across both executions, including
identical size, identical SHA-256, identical member contents, and identical
archive-member timestamps.

The source distribution remained logically equivalent but not byte-for-byte
identical. Its logical file contents were unchanged, while backend-generated
archive metadata retained temporal variability.

This baseline therefore removes unnecessary wall-clock influence at the
FamilyOS package-builder boundary and records the remaining source-distribution
archive metadata variability as a known limitation.

Level 40 currently stands at 11/11.

---

# Level 41 — Build Context Fingerprint

## Objective

Provide stronger context identity for reproducibility and caching.

### Checklist

* [x] Define canonical fingerprint inputs.
* [x] Include source identity.
* [x] Include relevant configuration.
* [x] Include dependency-state identity.
* [x] Include critical toolchain state.
* [x] Include relevant environment state.
* [x] Define canonical serialization.
* [x] Calculate fingerprint.
* [x] Associate fingerprint with Build Evidence.
* [x] Use fingerprint for comparison where useful.

This is a maturity capability and may remain deferred initially.

### Current Build Context Fingerprint

Canonical Build Context fingerprinting is implemented as a deterministic
semantic projection of the resolved Build Context.

The canonical fingerprint includes:

* source revision and dirty state;
* Python runtime version;
* dependency declaration identity and SHA-256;
* dependency lock identity and SHA-256;
* critical toolchain distributions and versions;
* operating system;
* operating-system release;
* machine architecture;
* filesystem encoding;
* Build profile;
* Build target;
* functional-validation configuration.

Execution-specific or volatile values are intentionally excluded, including:

* Build ID;
* package output path;
* Build Evidence output path;
* temporary directory;
* virtual-environment activation state.

Critical toolchain entries are sorted by distribution before serialization.

The canonical projection includes schema identity
`familyos.build-context-fingerprint.v1` and is serialized using deterministic
JSON ordering and separators before UTF-8 encoding and SHA-256 calculation.

The resulting immutable `BuildContextFingerprint` requires lowercase
64-character SHA-256 hexadecimal identity.

`BuildEvidenceFactory` calculates the fingerprint from the already-resolved
Build Context without recapturing canonical authorities. Build Evidence carries
the fingerprint as a required authority and deterministic Build Evidence JSON
exposes both algorithm and digest.

`BuildContextFingerprint.matches()` provides explicit semantic comparison for
reproducibility and future cache-oriented uses.

Equivalent canonical semantic contexts therefore produce matching
fingerprints, while relevant context changes produce different fingerprints.

Level 41 — Build Context Fingerprint is complete at 10/10.

---

# Level 42 — Reproducibility Testing

## Objective

Test whether equivalent contexts produce equivalent artifacts.

### Checklist

* [x] Execute equivalent build twice.
* [x] Compare artifact count.
* [x] Compare artifact type.
* [x] Compare metadata.
* [x] Compare file contents.
* [x] Compare digests where bit-for-bit reproducibility is expected.
* [x] Categorize expected variability.
* [x] Investigate unexplained variability.
* [x] Add periodic CI reproducibility checks if justified.

### Current Baseline

Canonical repeated-build validation now establishes artifact reproducibility
semantics for equivalent Build Contexts.

The validated package pair contains one Python wheel and one source
distribution in each execution.

The Python wheel is bit-for-bit equivalent across equivalent builds:

* artifact count and type are stable;
* raw size is equal;
* raw SHA-256 digest is equal;
* semantic member content is equal;
* observed archive metadata is equal.

The source distribution is logically equivalent across equivalent builds:

* artifact count and type are stable;
* semantic member content is equal;
* raw size and raw SHA-256 digest may differ;
* observed archive metadata variability is limited to timestamps;
* timestamp-only source-distribution variability is classified as expected.

Archive metadata observation, semantic content snapshots, explicit variability
policy, and aggregate reproducibility comparison now provide deterministic
application-level authorities for this classification.

Periodic reproducibility CI was evaluated but is not introduced at this
maturity level. Existing Build CI already contains periodic cache-free
validation, while artifact reproducibility automation remains a distinct
future capability. A scheduled reproducibility gate should be introduced only
after a canonical reproducibility runner owns repeated-build orchestration,
comparison, diagnostics, and CI result semantics.

The absence of a periodic reproducibility job therefore represents an explicit
Level 42 maturity decision rather than an unassessed checklist item.

---

# Level 43 — Supply Chain Evidence

## Objective

Progressively strengthen artifact provenance.

### Checklist

* [x] Record dependency-source information.
* [x] Record toolchain identity.
* [x] Record environment identity.
* [ ] Record builder identity where appropriate.
* [x] Record artifact digests.
* [x] Define provenance representation.
* [x] Evaluate industry-standard provenance formats.
* [x] Avoid creating a proprietary format without clear need.

### Dependency Source Evidence Boundary

At the current Supply Chain Evidence maturity level, dependency-source
information is limited to dependency input authorities that the canonical
Build Framework can establish without inference.

Canonical Build Evidence records the repository-controlled dependency
declaration and lock inputs through `DependencyState`, including their
canonical paths and cryptographic digests. Build Provenance preserves that
established dependency state without recapturing or reinterpreting it.

This establishes traceability to the dependency inputs that governed the
build. It does not establish the network origin from which individual
distributions were resolved or downloaded.

The current framework does not observe or authenticate a package registry,
mirror, index URL, upstream repository, download URL, or equivalent
distribution-origin authority. Absence of explicit source metadata must not
be interpreted as evidence that a dependency originated from PyPI or any
other registry.

Per-distribution source provenance, governed registry identity, upstream
origin, dependency artifact integrity, and stronger dependency provenance
remain future supply-chain maturity concerns and may require changes to the
dependency resolution or lock strategy before they can become canonical
evidence.

No `DependencySourceState`, inferred registry identity, package-origin claim,
or network-resolution provenance is introduced by Level 43.

### Builder Identity Boundary

Builder identity is intentionally deferred at the current Supply Chain
Evidence maturity level.

The canonical Build Framework currently records the observed execution
environment and critical toolchain state, but those authorities do not
constitute an authenticated builder identity. CI runner metadata,
provider-specific infrastructure identifiers, controlled-worker identity,
cryptographic builder assertions, and provenance attestations are therefore
not inferred from the current environment model.

Introducing a canonical builder identity before FamilyOS defines a controlled
builder boundary would create an identity or trust claim that the current
architecture cannot establish.

Builder identity will be reconsidered with Level 46 — Controlled Builder
Evaluation, where stronger isolation, environment identity, dedicated or
ephemeral workers, portability, security properties, and the corresponding
trust boundary can be evaluated together.

This deferral does not weaken the current artifact-trust contract. Build trust
remains based on the applicable controlled inputs, canonical execution
semantics, validation results, artifact integrity, Build Evidence, and
governance requirements.

No `BuilderIdentity`, provider-specific runner identity, signing assertion,
attestation, or SLSA provenance statement is introduced by Level 43.

---

# Level 44 — SBOM Evaluation

## Objective

Evaluate whether Software Bill of Materials generation provides operational value.

### Checklist

* [x] Identify SBOM use cases.
* [x] Identify target artifacts.
* [x] Identify required dependency depth.
* [x] Evaluate SPDX.
* [x] Evaluate CycloneDX.
* [x] Evaluate integration with Security Architecture.
* [x] Evaluate release evidence integration.
* [x] Decide through architecture governance before adoption.

### Current Evaluation

SBOM generation has clear potential operational value for FamilyOS.

Primary identified use cases are:

* runtime dependency inventory;
* dependency and vulnerability analysis;
* software supply-chain transparency;
* release composition evidence;
* historical release investigation;
* future compliance and security-policy enforcement.

The current canonical package artifacts are:

* Python wheel;
* source distribution.

For executable package composition, the relevant dependency depth is the
artifact runtime dependency closure: the FamilyOS package component, its
direct runtime dependencies, and applicable transitive runtime dependencies.

Build, development, validation, and toolchain dependencies remain separate
Build Evidence / provenance concerns unless a future SBOM profile explicitly
defines a broader build-environment composition scope.

SPDX and CycloneDX were both evaluated as viable industry-standard SBOM
representations.

Neither format is adopted as a canonical FamilyOS authority. A future SBOM
must remain a projection from established FamilyOS dependency authorities
rather than becoming the source of truth for dependency identity or
resolution.

Security Architecture integration is justified because dependency inventory
and transitive dependency visibility can support vulnerability analysis,
dependency-risk evaluation, and release eligibility decisions.

Release Evidence integration is also justified. A future SBOM may become
durable supply-chain evidence associated with applicable release artifacts,
while remaining complementary to Build Provenance, Artifact Integrity,
release manifests, and release validation.

### Architecture Governance Decision

SBOM implementation is intentionally deferred at the current Build Framework
maturity level.

The current `DependencyState` establishes the identity and SHA-256 digests of
the canonical dependency declaration and lock inputs, but FamilyOS has not yet
established a canonical resolved dependency-graph identity suitable for
authoritative SBOM generation.

Generating an SBOM before that authority exists would risk treating a derived
or partially reconstructed dependency inventory as canonical build evidence.

No SBOM generator, SPDX model, CycloneDX model, dependency-inventory authority,
package URL authority, new third-party dependency, or CI SBOM pipeline is
introduced by Level 44.

Future SBOM adoption would cross Build, Security, and Release Evidence
boundaries and therefore requires architecture governance before
implementation. Under the current Build Governance classification, such a
cross-cutting supply-chain architecture decision requires an RFC or equivalent
stronger governance record.

The future governance decision must establish at least:

* canonical dependency-graph authority;
* artifact/SBOM binding semantics;
* supported dependency scope;
* standard and version selection;
* component identity requirements;
* integrity and package-origin semantics;
* Security Architecture consumption;
* Release Evidence retention and validation;
* CI generation and verification policy.

Level 44 therefore completes the SBOM evaluation without adopting SBOM
generation.

SBOM generation remains a future maturity capability unless separately
mandated through architecture governance and an applicable build or release
profile.

---

# Level 45 — Artifact Signing Evaluation

## Objective

Evaluate cryptographic artifact signing when Release Framework maturity requires it.

### Checklist

* [x] Define signing objective.
* [x] Define signing authority.
* [x] Define Build versus Release ownership.
* [x] Define key-management requirements.
* [x] Define signature format.
* [x] Define verification process.
* [x] Define CI permission boundary.
* [x] Define release integration.
* [x] Define rotation and revocation behavior.
* [x] Record an ADR or RFC before adoption.

Signing should generally represent release authority rather than ordinary build execution.


### Artifact Signing Architecture Decision

Level 45 evaluates artifact signing as a future supply-chain trust control.
The evaluation is complete, but artifact-signing adoption is intentionally
deferred by architecture governance.

The current Build Framework establishes artifact identity, artifact integrity,
Build Evidence, and Build Provenance. SHA-256 artifact digests establish
content integrity, but they do not establish signer authenticity, release
authority, or an authenticated builder identity. Build Provenance similarly
records canonical build relationships without constituting a signed
attestation.

Artifact signing would introduce a new trust boundary. A meaningful signing
architecture must define the signing objective, trusted signing identity or
authority, key or identity lifecycle, signature representation, verification
policy, CI permission boundary, release integration, rotation, revocation, and
failure semantics before adoption.

Build remains responsible for artifact construction, identity, integrity,
metadata, validation, and Build Evidence. Release remains responsible for
downstream promotion and release policy. A future signing architecture must
preserve that ownership boundary and align with the Security Framework's
cryptographic and trust requirements.

No signing mechanism is selected by Level 45. Sigstore, Cosign, GPG/PGP,
key-based signing, keyless signing, certificates, OIDC identities,
transparency logs, and equivalent mechanisms remain candidates for future
governed evaluation rather than current implementation choices.

No `ArtifactSignature`, signing service, signer abstraction, signing key,
verification key, certificate identity, CI signing secret, OIDC `id-token`
permission, signature serializer, or signature-verification runtime is
introduced by this level.

Any future adoption that establishes or modifies a significant Build
architecture decision requires architecture governance. Because an artifact
signing and trust model is expected to cross Build, Release, Security, and CI
boundaries, adoption may require an RFC under the Build governance
classification. An ADR may be appropriate for a narrower architectural
decision where repository governance permits it.

Level 46 — Controlled Builder Evaluation remains relevant to future trust and
builder-identity decisions, but Level 45 does not equate release signing
authority with builder identity. Controlled-builder evaluation may inform a
future signing or attestation architecture without prematurely coupling the
two concepts.

Therefore Level 45 closes as an evaluation milestone:

* artifact-signing use cases and trust requirements are evaluated;
* Build, Release, Security, and CI ownership boundaries are identified;
* implementation and dependency introduction remain intentionally absent;
* adoption is deferred until the required trust architecture is approved
  through architecture governance.

**Artifact Signing Adoption: Deferred by Governance.**

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

* [x] Identify current environment reproducibility limitation.
* [x] Determine whether isolation solves the actual problem.
* [x] Evaluate maintenance cost.
* [x] Evaluate local developer impact.
* [x] Evaluate CI portability.
* [x] Evaluate security benefits.
* [x] Record architecture decision before introduction.


### Controlled Builder Architecture Decision

Level 46 evaluates whether FamilyOS currently requires a stronger controlled
builder boundary. The evaluation is complete, but adoption is intentionally
deferred until a demonstrated engineering, security, release-trust, or
distribution-scale need justifies the additional architecture.

The current reproducibility limitation is explicit. FamilyOS controls and
records canonical source, dependency declarations and lock state, runtime
policy, critical toolchain state, Build configuration, Build Context,
environment observations, artifact identity, artifact integrity, Build
Evidence, and reproducibility comparison. It does not fully control the host
operating-system image, provider runner-image lifecycle, preinstalled system
packages, underlying host infrastructure, or an authenticated builder
identity.

Stronger isolation can reduce that uncontrolled state. Containerized builds,
immutable build images, dedicated or isolated runners, and remote build workers
could improve environment definition, reproducibility, CI portability,
security isolation, or high-trust release assurance.

Those benefits do not establish a current adoption requirement. Existing
ephemeral CI runners already prevent reliance on previous local build state,
while virtual environments, explicit dependency installation, canonical
toolchain policy, environment-state capture, cache-free validation, and
reproducibility testing provide controls appropriate to the current maturity
level.

A stronger builder also carries material costs. Containerization introduces
image maintenance, image complexity, security patching, and local developer
overhead. Dedicated runners require lifecycle, cleanup, isolation, patching,
and operational ownership. Immutable images require controlled image
production and update governance. Remote build workers introduce distributed
infrastructure and must integrate with the existing canonical Build Context
and Build Evidence architecture rather than creating parallel Build semantics.

The canonical environment model must remain provider-independent. Provider
specific runner mechanisms belong at the CI integration boundary. A future
controlled builder must preserve practical local development and must not make
container or remote infrastructure the hidden source of canonical Build
semantics.

Security benefits are real: stronger isolation can reduce interaction with
host state and limit the impact of compromised tooling or dependencies.
However, isolation strength remains proportional to risk. The Build roadmap
places trusted builders in the future high-trust supply-chain maturity path,
where stronger isolation and environment identity may be justified by platform
risk or distribution scale.

Builder identity therefore remains deferred. `ubuntu-latest`, runner metadata,
provider infrastructure identifiers, `EnvironmentState`, or other observed
execution properties are not promoted into an authenticated
`BuilderIdentity`. A future builder-identity model requires a controlled trust
boundary capable of supporting that claim.

No containerized canonical build, immutable build image, dedicated or
self-hosted build runner, remote build worker, authenticated `BuilderIdentity`,
or provider-specific builder identity is introduced by Level 46.

Future adoption must pass architecture governance before introduction.
Introducing containerized builds, dedicated workers, or a significant change
to the Build environment model is an architectural change and requires the
governance path appropriate to its scope. A cross-platform remote execution or
broader trusted-builder strategy may require RFC-level governance.

Level 46 therefore closes as an evaluation milestone.

**Controlled Builder Adoption: Deferred Until Demonstrated Need.**

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

* [x] release-candidate build profile exists;
* [x] release handoff contract exists;
* [x] artifacts are not rebuilt unnecessarily downstream;
* [x] integrity is verified across handoff;
* [x] EPIC-REL-001 consumes Build Evidence;
* [x] release credentials remain outside ordinary Build execution.

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
