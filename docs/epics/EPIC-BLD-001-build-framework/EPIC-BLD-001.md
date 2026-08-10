id: EPIC-BLD-001
title: Build Framework
type: engineering-framework
domain: engineering-platform

status: completed

summary: >
Establish the official FamilyOS Build Framework for transforming controlled
engineering state into validated, traceable, reproducible, and trustworthy
software artifacts through explicit build inputs, governed toolchains,
controlled environments, deterministic configuration, canonical execution,
artifact validation, build evidence, automation, and release handoff.

purpose:

* define canonical build principles
* establish Build Architecture
* define the Build Lifecycle
* control build inputs
* govern project structure expectations
* define Build Toolchain requirements
* define Build Environment Management
* govern dependency management
* define deterministic Build Configuration
* define Build Execution
* define Artifact Management
* define Build Validation
* define Build Governance
* define Build Automation and CI integration
* establish Build Evidence
* support reproducibility
* establish trusted artifact handoff to the Release Framework
* prepare FamilyOS for future software supply-chain assurance

scope:
includes:
- build principles
- build architecture
- build lifecycle
- build input requirements
- build project structure
- build toolchain
- build environments
- dependency management
- build configuration
- build philosophy
- build execution
- artifact management
- artifact identity
- artifact integrity
- build validation
- build evidence
- build automation
- continuous integration
- build governance
- reproducibility
- release handoff
- future supply-chain maturity

excludes:
- software release authorization
- release version selection
- software publication
- deployment
- runtime orchestration
- testing methodology ownership
- quality policy ownership
- documentation governance ownership
- plugin compliance policy ownership
- security architecture ownership

canonical_directory: docs/epics/EPIC-BLD-001-build-framework

structure:
numbered_documents: 24
control_documents: 7
canonical_files: 31

numbered_documents:

* 00-EPIC.md
* 01-Context.md
* 02-Vision.md
* 03-Build-Principles.md
* 04-Build-Architecture.md
* 05-Build-Lifecycle.md
* 06-Build-Input-Requirements.md
* 07-Build-Inputs-and-Project-Structure.md
* 08-Build-Toolchain.md
* 09-Build-Environment-Management.md
* 10-Dependency-Management.md
* 11-Build-Configuration.md
* 12-Build-Philosophy.md
* 13-Build-Execution.md
* 14-Artifact-Management.md
* 15-Build-Validation.md
* 16-Build-Governance.md
* 17-Build-Automation-and-CI.md
* 18-Roadmap.md
* 19-References.md
* 20-Validation.md
* 21-Summary.md
* 22-Release.md
* 23-Implementation-Checklist.md

control_documents:

* EPIC-BLD-001.md
* EPIC.yaml
* README.md
* MANIFEST.md
* CHANGELOG.md
* VALIDATION.md
* Revision-History.md

framework_relationships:
upstream:
- id: EPIC-ENG-001
title: Engineering Foundation

```
- id: EPIC-TST-001
  title: Testing Framework

- id: EPIC-QLT-001
  title: Quality Framework

- id: EPIC-DOC-001
  title: Documentation Framework

- id: EPIC-PLUGIN-002
  title: Plugin Compliance Framework
```

downstream:
- id: EPIC-REL-001
title: Release Framework

architectural_relationships:

* Engineering Foundation provides general engineering principles and governance.
* Testing Framework provides test semantics and test evidence.
* Quality Framework governs quality assessment and quality gates.
* Documentation Framework governs documentation architecture and standards.
* Plugin Compliance Framework governs plugin-specific compliance rules.
* Build Framework produces trusted artifacts and Build Evidence.
* Release Framework evaluates, promotes, publishes, and distributes trusted artifacts.

build_model:
stages:
- build_inputs
- build_context_resolution
- environment_preparation
- dependency_resolution
- toolchain_validation
- pre_build_validation
- build_execution
- candidate_artifact_collection
- artifact_validation
- build_evidence_generation
- trusted_artifact_finalization
- release_handoff

build_context:
includes:
- source_state
- effective_configuration
- dependency_state
- toolchain_state
- environment_state
- build_profile
- applicable_policies

build_profiles:
initial:
- development
- validation
- ci
- release-candidate

artifact_model:
states:
- raw_output
- candidate_artifact
- validated_artifact
- trusted_artifact

trust_model:
principles:
- build_success_is_not_artifact_trust
- artifact_trust_is_not_release_authorization
- artifacts_must_be_validated_before_trust
- trusted_artifacts_must_have_traceable_origin
- artifact_integrity_must_correspond_to_final_bytes
- downstream_release_should_prefer_promotion_of_validated_bytes

automation:
principles:
- ci_executes_canonical_build_semantics
- ci_does_not_define_build_architecture
- local_and_ci_build_semantics_should_align
- caches_are_optional_optimizations
- build_permissions_follow_least_privilege
- release_credentials_remain_separate_from_ordinary_build_jobs

governance:
change_classes:
- routine
- significant
- architectural
- strategic

mechanisms:
- code-review
- documentation-review
- technical-review
- ADR
- RFC
- EPIC-revision
- quality-review
- security-review

decisions:

* ADR-0007
* ADR-0008
* ADR-0009
* ADR-0010
* ADR-0011
* ADR-0013

related_rfcs:

* RFC-0010
* RFC-0011
* RFC-0012
* RFC-0013
* RFC-0014
* RFC-0015

deliverables:

* Build Framework definition
* Build Context model
* Build Principles
* Build Architecture
* Build Lifecycle
* Build Input Requirements
* Build project structure model
* Build Toolchain model
* Build Environment Management model
* Dependency Management model
* Build Configuration model
* Build Philosophy
* Build Execution model
* Artifact Management model
* Build Validation model
* Build Governance model
* Build Automation and CI model
* Build Roadmap
* Build reference model
* framework validation model
* framework summary
* framework release model
* implementation checklist
* framework control documentation

acceptance_criteria:

* all 24 numbered documents exist
* all 7 control documents exist
* canonical file count is 31
* no duplicate numbered chapters remain
* no legacy migration files remain
* no temporary framework files remain
* no canonical document is empty
* canonical structure matches MANIFEST.md
* Build Architecture is coherent
* Build Lifecycle is coherent
* Build Context terminology is consistent
* artifact terminology is consistent
* Build Validation is complete
* Build Governance is complete
* Build Automation remains subordinate to canonical Build Architecture
* Build and Release responsibilities remain separated
* cross-framework relationships are coherent
* 20-Validation.md has been applied
* VALIDATION.md records the final validation result
* control documents describe the same framework state
* no unresolved critical or major framework finding remains

framework_completion:
architecture: complete
documentation: complete
structural_normalization: complete
implementation: planned
final_validation: pending
release_tag: pending

roadmap:
phases:
- build-foundation
- build-standardization
- build-validation
- build-automation
- artifact-trust
- reproducibility-and-traceability
- release-integration
- supply-chain-assurance

implementation_direction:

* canonical build interface
* environment standardization
* dependency standardization
* configuration standardization
* canonical execution
* artifact management
* artifact validation
* CI integration
* Build ID
* Build Evidence
* release handoff
* reproducibility
* supply-chain assurance

release_handoff:
provides:
- trusted artifact set
- Build ID
- artifact manifest
- artifact digests
- validation result
- Build Evidence

consumed_by:
- EPIC-REL-001

final_principle: >
FamilyOS does not trust software because a build command succeeded.
FamilyOS trusts an artifact when the process that produced it is controlled,
the artifact itself has been validated, and sufficient evidence exists to
understand its origin.
