# FamilyOS naming conventions

**Version:** 1.0
**Status:** Stable
**Last Updated:** August 2026

---

# Purpose

This document defines the official naming conventions used throughout the FamilyOS platform.

Its purpose is to ensure that names communicate architectural intent, remain consistent across components, and can be understood without inspecting implementation details.

This document is normative.

---

# Scope

These conventions apply to:

* repositories
* directories
* files
* Markdown documents
* Python packages and modules
* Python types and members
* Domain-Driven Design components
* application services
* infrastructure components
* generation components
* plugins
* capabilities
* contributions
* command-line interfaces
* specifications
* Architecture Decision Records
* Requests for Comments
* tests
* Git branches
* release tags

Rules for words that cannot be used as identifiers are defined separately in:

`docs/04-reference/Reserved-Words.md`

---

# Normative language

The keywords **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** express normative requirements.

Their interpretation follows the conventions established in:

`docs/04-reference/Language.md`

---

# General principles

## Clarity

Names MUST communicate purpose and responsibility.

A reader SHOULD understand the role of a component from its name without reading its implementation.

Preferred:

```text
PluginResolutionPipeline
```

Avoid:

```text
PluginProcessor
```

The preferred name communicates the specific operation being performed.

---

## Precision

Names MUST describe what a component is or does.

Generic terms such as `manager`, `helper`, `utility`, `processor`, or `handler` MUST NOT be used when a more precise architectural term exists.

A generic term MAY be used only when it accurately represents an established platform responsibility.

---

## Consistency

The same architectural concept MUST use the same term throughout the platform.

A concept MUST NOT be renamed locally for stylistic preference.

For example, a component that resolves dependencies MUST consistently use the term `Resolver` rather than alternating between `Resolver`, `Selector`, `Finder`, and `Processor`.

---

## Stability

Public names SHOULD remain stable across compatible platform releases.

Renaming a public identifier requires:

* documented justification
* compatibility analysis
* migration guidance
* architectural review

---

## Single responsibility

A name SHOULD represent one responsibility.

Names combining unrelated responsibilities indicate that the component may require decomposition.

Avoid:

```text
PluginLoaderValidatorInstaller
```

Prefer separate components:

```text
PluginLoader
PluginVerifier
PluginInstaller
```

---

## Vocabulary

Names MUST use terminology defined in:

`docs/04-reference/Glossary.md`

A new platform-wide term MUST be added to the glossary before becoming part of the public vocabulary.

---

## Language

All official identifiers MUST use English.

Names MUST NOT mix languages.

Abbreviations MUST comply with:

`docs/04-reference/Acronyms.md`

---

## Abbreviations

Unnecessary abbreviations MUST be avoided.

Preferred:

```text
configuration
dependency
specification
repository
```

Avoid:

```text
config
dep
spec
repo
```

Established technical acronyms MAY be used when they improve clarity.

Examples:

```text
CLI
API
SDK
JSON
UUID
```

Acronyms inside Python class names MUST follow normal PascalCase composition.

Preferred:

```text
PluginApiClient
JsonSpecificationLoader
UuidGenerator
```

Avoid:

```text
PluginAPIClient
JSONSpecificationLoader
UUIDGenerator
```

---

# Repository naming

The official repository name is:

```text
FamilyOS
```

Repository names belonging to the FamilyOS ecosystem SHOULD use lowercase kebab-case.

Examples:

```text
familyos
familyos-cli
familyos-security-plugin
familyos-plugin-template
familyos-documentation
```

Repository names MUST NOT contain spaces or underscores.

---

# Directory naming

## General directories

Directories MUST use lowercase kebab-case unless the language ecosystem requires another convention.

Examples:

```text
docs/04-reference
docs/00-foundation
plugin-templates
generated-artifacts
```

---

## Python package directories

Python package directories MUST use lowercase snake_case.

Examples:

```text
familyos_cli
dependency_graph
generation_framework
plugin_runtime
```

Hyphens MUST NOT be used in Python package directory names.

---

## Documentation directories

Top-level documentation directories MAY use a numeric ordering prefix followed by a lowercase kebab-case name.

Format:

```text
NN-name
```

Examples:

```text
00-foundation
01-product
02-architecture
03-engineering
04-reference
05-knowledge
06-specifications
07-business
```

The numeric prefix defines navigation order. It MUST NOT express document versioning.

---

## Domain directories

Domain directories MUST use the canonical lowercase domain name.

Examples:

```text
person
family
security
health
finance
education
documents
communication
```

A domain directory MUST NOT include suffixes such as `domain`, `module`, or `context` unless required to distinguish a technical package from the domain itself.

---

# File naming

## General files

File names MUST be descriptive and stable.

Temporary suffixes such as the following MUST NOT appear in committed production files:

```text
new
old
final
final2
copy
backup
temp
draft-latest
```

Version control provides file history and MUST be used instead of filename-based revisions.

---

## Markdown files

Markdown document names MUST use PascalCase words separated by hyphens.

Examples:

```text
Architecture-Principles.md
Engineering-Principles.md
Naming-Conventions.md
Reserved-Words.md
Reference-Index.md
Business-Rules.md
Domain-Model.md
```

The following conventional file names are permitted:

```text
README.md
CHANGELOG.md
CONTRIBUTING.md
SECURITY.md
LICENSE.md
```

Markdown file names MUST use the `.md` extension.

Spaces and underscores MUST NOT be used in official Markdown file names.

---

## README files

A directory overview MUST be named:

```text
README.md
```

Alternative names such as the following MUST NOT be used for the same responsibility:

```text
Overview.md
Index.md
Home.md
About.md
```

A separate index MAY exist only when it provides a distinct reference or navigation responsibility.

---

## Configuration files

Configuration file names SHOULD follow the convention of the corresponding tool.

Examples:

```text
pyproject.toml
pytest.ini
mypy.ini
ruff.toml
```

Project-defined YAML files MUST use lowercase kebab-case.

Examples:

```text
security-domain.yaml
plugin-manifest.yaml
generation-recipe.yaml
```

---

## Template files

Template file names MUST identify the artifact they generate.

Examples:

```text
domain-readme.md.j2
aggregate-documentation.md.j2
plugin-manifest.yaml.j2
python-module.py.j2
```

Template names MUST NOT use generic names such as:

```text
template.j2
default.j2
file.j2
```

---

# Python naming

FamilyOS Python code MUST follow PEP 8 unless this document defines a stricter platform rule.

---

## Packages

Python packages MUST use lowercase snake_case.

Examples:

```python
familyos_cli
plugin_runtime
dependency_graph
```

Package names SHOULD be nouns representing coherent architectural areas.

---

## Modules

Python modules MUST use lowercase snake_case.

The module name SHOULD match its primary public type.

Examples:

```text
plugin_runtime.py
resolution_plan.py
domain_generation_pipeline.py
capability_registry.py
```

A module containing `PluginRuntime` SHOULD be named:

```text
plugin_runtime.py
```

Generic module names such as the following SHOULD be avoided:

```text
common.py
helpers.py
utils.py
misc.py
base.py
core.py
```

A generic module MAY exist only when its responsibility is explicit and architecturally justified.

---

## Classes

Classes MUST use PascalCase.

Examples:

```python
PluginRuntime
ResolutionPlan
DomainGenerationPipeline
CapabilityRegistry
```

Class names MUST be nouns or noun phrases.

A class name SHOULD identify its architectural role through an approved suffix when applicable.

---

## Abstract classes

Abstract class names MUST describe the contract they represent.

The `Abstract` prefix SHOULD NOT be used unless needed to distinguish the abstraction from a canonical concrete type.

Preferred:

```python
PluginRepository
TemplateRenderer
GenerationStrategy
```

Avoid:

```python
AbstractPluginRepository
BaseTemplateRenderer
IGenerationStrategy
```

---

## Protocols

Protocol names MUST use PascalCase and SHOULD describe the behavior they require.

Examples:

```python
CapabilityProvider
ContributionProvider
DiagnosticFormatter
```

The suffix `Protocol` SHOULD NOT be added unless required to prevent ambiguity.

Avoid Hungarian-style prefixes such as:

```python
IPlugin
IRepository
IProvider
```

---

## Dataclasses

Dataclasses MUST follow normal class naming rules.

Their names MUST represent values, records, requests, results, definitions, plans, or contexts.

Examples:

```python
GenerationRequest
GenerationResult
PluginMetadata
ResolutionPlan
DomainContext
```

The suffix `Data` SHOULD NOT be used unless the class specifically represents an external data-transfer structure.

---

## Enumerations

Enumeration classes MUST use PascalCase.

Their names SHOULD be singular.

Examples:

```python
RuntimeState
DiagnosticSeverity
VersionOperator
PluginState
```

Enumeration members MUST use uppercase snake_case.

Examples:

```python
LOADED
INITIALIZED
ACTIVE
STOPPING
STOPPED
```

---

## Exceptions

Exception classes MUST end with `Error`.

Examples:

```python
PluginNotFoundError
InvalidRuntimeTransitionError
SpecificationValidationError
DependencyResolutionError
```

Exception names MUST describe the failure condition.

Avoid:

```python
PluginException
RuntimeProblem
ValidationIssue
```

---

## Functions

Functions MUST use lowercase snake_case.

Function names SHOULD begin with a verb.

Examples:

```python
create_plugin()
resolve_dependencies()
validate_specification()
render_template()
```

Functions that return boolean values SHOULD use a predicate form.

Examples:

```python
is_compatible()
has_capability()
can_activate()
```

---

## Methods

Methods MUST use lowercase snake_case.

Method names MUST describe an operation performed by the owning type.

Common operation names SHOULD be used consistently:

```python
create()
load()
save()
find()
get()
list()
register()
resolve()
validate()
render()
execute()
activate()
deactivate()
```

The verb `get` SHOULD be used when the requested value is expected to exist.

The verb `find` SHOULD be used when absence is an expected result.

---

## Private members

Private implementation members MUST begin with a single underscore.

Examples:

```python
_runtime
_registry
_load_manifest()
```

Double-leading underscores SHOULD NOT be used except when Python name mangling is explicitly required.

---

## Variables

Variables MUST use lowercase snake_case.

Names MUST describe the represented value.

Preferred:

```python
resolved_packages
generation_context
plugin_identifier
```

Avoid:

```python
data
value
item
obj
thing
tmp
```

Short names MAY be used for narrow mathematical or iteration contexts when their meaning is obvious.

---

## Constants

Constants MUST use uppercase snake_case.

Examples:

```python
DEFAULT_PLUGIN_DIRECTORY
SUPPORTED_MANIFEST_VERSION
MAX_RESOLUTION_DEPTH
```

Constants MUST NOT be used for values that vary during runtime.

---

## Type aliases

Type aliases MUST use PascalCase.

Examples:

```python
PluginIdentifier
ArtifactPath
CapabilityMap
```

A type alias name MUST communicate domain meaning rather than merely repeat its underlying type.

---

## Type variables

Type variables MUST use concise PascalCase names.

Examples:

```python
T
TResult
TPlugin
TContribution
```

A descriptive type variable SHOULD be preferred in public generic contracts.

---

## Boolean names

Boolean variables and properties SHOULD use one of the following prefixes:

```text
is_
has_
can_
should_
supports_
requires_
```

Examples:

```python
is_active
has_errors
can_resolve
supports_generation
requires_restart
```

Negative boolean names SHOULD be avoided.

Avoid:

```python
is_not_active
not_valid
disable_validation
```

---

## Collections

Collection names SHOULD use plural nouns.

Examples:

```python
plugins
artifacts
diagnostics
dependencies
```

Mappings SHOULD use names that describe their key-to-value relationship.

Examples:

```python
plugins_by_identifier
capabilities_by_id
templates_by_name
```

---

# Architectural role suffixes

Approved suffixes communicate established architectural responsibilities.

A suffix MUST NOT be added when the component does not fulfill the corresponding responsibility.

---

## Service

The suffix `Service` identifies a stateless application or domain operation that does not naturally belong to an entity or value object.

Examples:

```python
SpecificationService
RecipeCatalogService
DiagnosticPresentationService
```

`Service` MUST NOT be used as a default suffix for arbitrary classes.

---

## Use case

Application use cases MUST end with `UseCase`.

Examples:

```python
CreateProjectUseCase
CreateDomainUseCase
GetDomainSpecificationUseCase
```

A use case name MUST begin with an action.

---

## Repository

The suffix `Repository` identifies an abstraction that provides access to stored domain or platform objects.

Examples:

```python
PluginRepository
DomainSpecificationRepository
```

Infrastructure implementations SHOULD identify their storage mechanism when multiple implementations exist.

Examples:

```python
FileSystemPluginRepository
InMemoryPluginRepository
```

---

## Factory

The suffix `Factory` identifies a component responsible for constructing fully initialized objects.

Examples:

```python
RuntimeFactory
ApplicationFactory
GenerationRequestFactory
```

A factory MUST NOT be used merely to wrap a constructor without adding construction policy or dependency assembly.

---

## Builder

The suffix `Builder` identifies incremental construction of a complex object.

Examples:

```python
DependencyGraphBuilder
ResolutionDiagnosticBuilder
```

Builders SHOULD expose explicit construction steps and produce a final result.

---

## Registry

The suffix `Registry` identifies a controlled collection indexed by stable identifiers.

Examples:

```python
PluginRegistry
CapabilityRegistry
ContributionRegistry
GenerationRecipeRegistry
```

A registry SHOULD define registration, lookup, uniqueness, and lifecycle rules.

---

## Resolver

The suffix `Resolver` identifies a component that determines a result from constraints, dependencies, identifiers, or context.

Examples:

```python
PluginResolver
PresetRecipeResolver
DependencyGraphResolver
```

Resolvers MUST NOT perform installation, activation, or rendering unless those operations are part of the documented resolution contract.

---

## Selector

The suffix `Selector` identifies a component that chooses one or more candidates from an existing set.

Examples:

```python
PluginPackageSelector
PluginVersionSelector
```

Selection MUST remain distinct from dependency resolution.

---

## Provider

The suffix `Provider` identifies a component that supplies values, capabilities, contributions, or implementations to another component.

Examples:

```python
CapabilityProvider
PluginContributionProvider
```

Providers SHOULD NOT own orchestration responsibilities.

---

## Loader

The suffix `Loader` identifies a component that reads and converts an external representation into a platform object.

Examples:

```python
DomainSpecificationLoader
PluginManifestLoader
```

Loading MUST remain distinct from validation and activation unless explicitly defined otherwise.

---

## Renderer

The suffix `Renderer` identifies a component that transforms structured information into a presentation format.

Examples:

```python
TemplateRenderer
DiagnosticCliRenderer
```

---

## Formatter

The suffix `Formatter` identifies a component that converts information into a defined textual or serialized representation.

Examples:

```python
TextExplanationFormatter
JsonExplanationFormatter
```

---

## Validator

The suffix `Validator` identifies a component that verifies compliance with explicit rules.

Examples:

```python
SpecificationValidator
PluginManifestValidator
```

A validator SHOULD return structured validation information or raise a specific validation error.

---

## Verifier

The suffix `Verifier` identifies integrity, authenticity, compatibility, or trust verification.

Examples:

```python
PluginVerifier
SignatureVerifier
```

Verification MUST remain distinct from structural validation.

---

## Adapter

The suffix `Adapter` identifies a component that translates one contract or representation into another.

Examples:

```python
DomainGenerationAdapter
ConflictDiagnosticAdapter
```

Adapters MUST NOT contain unrelated orchestration logic.

---

## Mapper

The suffix `Mapper` identifies deterministic conversion between two models.

Examples:

```python
GenerationSpecificationMapper
DomainGenerationPlanMapper
```

A mapper SHOULD NOT perform persistence, network access, or lifecycle management.

---

## Pipeline

The suffix `Pipeline` identifies an ordered orchestration of multiple processing stages.

Examples:

```python
GenerationPipeline
DomainGenerationPipeline
PluginResolutionPipeline
DiagnosticPipeline
```

A pipeline MUST expose a clear input, processing sequence, and output.

---

## Strategy

The suffix `Strategy` identifies an interchangeable implementation of an algorithm or generation behavior.

Examples:

```python
GenerationStrategy
DomainDocumentationStrategy
```

---

## Policy

The suffix `Policy` identifies an explicit decision rule.

Examples:

```python
ArtifactNamingPolicy
GenerationOverwritePolicy
```

Policies SHOULD be deterministic and independent from infrastructure concerns.

---

## Context

The suffix `Context` identifies immutable or controlled information passed through an operation or runtime boundary.

Examples:

```python
RuntimeContext
GenerationContext
DomainContext
CommandContext
```

A context MUST NOT become an unrestricted container for unrelated dependencies.

---

## Request and result

Input models SHOULD end with `Request` when they represent an operation request.

Output models SHOULD end with `Result` when they represent an operation outcome.

Examples:

```python
GenerationRequest
GenerationResult
DependencyResolutionResult
```

---

## Plan

The suffix `Plan` identifies a computed description of work that has not yet been executed.

Examples:

```python
ResolutionPlan
DomainGenerationPlan
InstallationPlan
```

---

## Definition

The suffix `Definition` identifies declarative configuration or metadata defining a platform concept.

Examples:

```python
ArtifactDefinition
PresetDefinition
CapabilityDefinition
```

---

## Descriptor

The suffix `Descriptor` identifies structured descriptive metadata about another component.

Examples:

```python
DomainDescriptor
PluginDescriptor
ArtifactDescriptor
```

---

## Metadata

The suffix `Metadata` identifies descriptive information that does not itself define behavior.

Examples:

```python
PluginMetadata
ProjectMetadata
```

---

# Domain-Driven Design naming

## Domains

Domain names MUST use singular PascalCase in prose and type names.

Examples:

```text
Person
Family
Security
Health
Finance
Education
Documents
Communication
```

Directory and package forms MUST use lowercase snake_case or lowercase directory conventions as applicable.

Examples:

```text
security
security_domain
```

The suffix `Domain` SHOULD be used only when referring to the domain as a technical model or component.

Examples:

```python
DomainSpecification
SecurityDomainPlugin
```

---

## Bounded contexts

Bounded context names MUST use PascalCase and describe a coherent business language boundary.

A bounded context name SHOULD NOT be based on a technical layer.

Preferred:

```text
Identity
Documents
Communication
```

Avoid:

```text
Database
Backend
Api
```

---

## Aggregates

Aggregate names MUST use singular PascalCase.

Examples:

```text
Family
Person
Household
Document
```

Documentation files describing aggregates SHOULD use the aggregate name.

Example:

```text
aggregates/Family.md
```

---

## Aggregate roots

Aggregate root classes MUST use the business concept name without an `AggregateRoot` suffix.

Preferred:

```python
Family
Person
```

Avoid:

```python
FamilyAggregateRoot
PersonAggregate
```

The architectural role MUST be documented rather than encoded redundantly in the class name.

---

## Entities

Entity names MUST use singular business nouns.

Examples:

```python
Person
Membership
Document
Account
```

The suffix `Entity` SHOULD NOT be used.

Avoid:

```python
PersonEntity
DocumentEntity
```

---

## Value objects

Value object names MUST represent the value itself.

Examples:

```python
PersonId
EmailAddress
DateRange
PluginVersion
VersionConstraint
```

The suffix `ValueObject` MUST NOT be used.

---

## Domain services

Domain service names MUST describe the business operation and end with `Service` only when the operation does not belong naturally to an entity or value object.

Examples:

```python
MembershipEligibilityService
DocumentClassificationService
```

---

## Domain events

Domain event names MUST:

* use PascalCase
* describe a completed fact
* use past-tense wording where natural

Examples:

```python
PersonCreated
MemberAdded
DocumentArchived
PluginActivated
```

Avoid command-style event names:

```python
CreatePerson
AddMember
ArchiveDocument
```

---

## Commands

Command names MUST describe requested actions.

Examples:

```python
CreatePerson
AddFamilyMember
ArchiveDocument
ActivatePlugin
```

A command name MUST NOT imply that the action has already succeeded.

---

## Queries

Query names MUST describe the requested information.

Examples:

```python
GetPerson
ListFamilyMembers
FindDocuments
GetPluginStatus
```

---

## Identifiers

Identifier value objects SHOULD use the concept name followed by `Id`.

Examples:

```python
PersonId
FamilyId
PluginId
CapabilityId
```

The spelling `Id` MUST be used in PascalCase names.

Uppercase `ID` MUST NOT be used inside Python identifiers.

---

## Specifications

Business rule specifications MUST use a descriptive predicate or rule name followed by `Specification` when implemented as specification objects.

Examples:

```python
CompatiblePluginSpecification
ValidMembershipSpecification
```

Document specifications SHOULD use descriptive kebab-case file names.

Examples:

```text
security-domain.yaml
plugin-manifest.yaml
```

---

# Generation framework naming

## Artifacts

Artifact names MUST identify the generated deliverable.

Examples:

```text
domain-readme
aggregate-documentation
plugin-manifest
python-module
```

Artifact type names SHOULD end with `Artifact` when represented as Python types.

Examples:

```python
GenerationArtifact
DocumentationArtifact
```

---

## Recipes

Recipe names MUST describe the complete generation outcome.

Examples:

```text
domain-summary-documentation
aggregate-documentation
domain-model-documentation
```

Python recipe types SHOULD end with `Recipe`.

Examples:

```python
DomainSummaryDocumentationRecipe
AggregateDocumentationRecipe
```

---

## Presets

Preset identifiers MUST use lowercase kebab-case.

Examples:

```text
security
default-domain
complete-documentation
```

Preset type names MUST end with `Preset` or `PresetDefinition` according to responsibility.

---

## Strategies

Generation strategy names MUST describe the interchangeable generation behavior.

Examples:

```python
DomainDocumentationStrategy
AggregateDocumentationStrategy
```

Strategy identifiers MUST use lowercase kebab-case when persisted or exposed through the CLI.

---

## Templates

Template names MUST identify their generated target and format.

Examples:

```text
domain-readme.md.j2
plugin-class.py.j2
plugin-manifest.yaml.j2
```

---

# Plugin naming

## Plugin display names

Plugin display names MUST use PascalCase words in prose.

Examples:

```text
Security Plugin
Health Plugin
Finance Plugin
```

Official plugin names MUST use the corresponding domain name followed by `Plugin`.

---

## Plugin package names

Python distribution names MUST use lowercase kebab-case.

Examples:

```text
familyos-security-plugin
familyos-health-plugin
familyos-finance-plugin
```

Python import packages MUST use lowercase snake_case.

Examples:

```python
familyos_security_plugin
familyos_health_plugin
familyos_finance_plugin
```

---

## Plugin classes

The primary plugin class MUST use the domain or function name followed by `Plugin`.

Examples:

```python
SecurityPlugin
HealthPlugin
DocumentationPlugin
```

Generic names such as `MainPlugin` or `FamilyOSPlugin` MUST NOT be used.

---

## Plugin identifiers

Plugin identifiers MUST use lowercase dot-separated names.

Official plugin identifiers MUST use the `familyos` namespace.

Format:

```text
familyos.<plugin-name>
```

Examples:

```text
familyos.security
familyos.health
familyos.finance
familyos.documentation
```

Plugin identifiers MUST be stable and MUST NOT include a version.

---

## Plugin versions

Plugin versions MUST be represented separately from plugin identifiers.

A combined package identifier MAY use the following display format:

```text
familyos.security@1.0.0
```

The `@` notation is representational and MUST NOT be part of the canonical plugin identifier.

---

## Capabilities

Capability identifiers MUST use lowercase dot-separated names.

Format:

```text
<namespace>.<area>.<capability>
```

Examples:

```text
familyos.security.audit
familyos.security.encryption
familyos.documents.classification
familyos.generation.recipes
```

Capability identifiers MUST represent abilities, not implementation classes.

---

## Contributions

Contribution type names MUST describe the contributed platform extension and end with `Contribution`.

Examples:

```python
GenerationContribution
DomainGenerationContribution
GenerationRecipeContribution
TemplateContribution
```

Contribution identifiers MUST use stable lowercase dot-separated names when externally referenced.

---

## Plugin hooks

Hook names MUST describe lifecycle events or extension operations.

Examples:

```python
on_load
on_initialize
on_activate
on_stop
```

Hooks MUST NOT use ambiguous names such as:

```python
run
process
handle
execute_hook
```

---

# Command-line interface naming

## Commands

CLI commands MUST use lowercase kebab-case.

Examples:

```text
familyos init
familyos create domain
familyos plugin resolve
familyos generation presets
```

Command names SHOULD begin with a verb when they perform an action.

Examples:

```text
create
resolve
validate
install
activate
```

Noun commands MAY be used as command groups.

Examples:

```text
plugin
generation
domain
```

---

## Options

Long option names MUST use lowercase kebab-case and begin with two hyphens.

Examples:

```text
--specification
--destination
--output-format
--include-diagnostics
```

Short options MAY be provided when they are unambiguous and commonly used.

Examples:

```text
-v
-q
-h
```

A short option MUST NOT have different meanings across closely related commands.

---

## Positional arguments

Positional argument names MUST use lowercase snake_case in Python and lowercase descriptive names in help output.

Examples:

```text
domain_name
plugin_identifier
artifact_type
```

---

## Boolean options

Boolean options SHOULD express the enabled behavior positively.

Preferred:

```text
--include-diagnostics
--overwrite
--strict
```

Avoid:

```text
--no-skip-diagnostics
--disable-protection
```

A negative option MAY exist when disabling a default behavior is the clearest user-facing contract.

---

# Documentation naming

## Architecture Decision Records

Architecture Decision Record files MUST use the following format:

```text
ADR-NNNN-Title-In-Pascal-Kebab-Case.md
```

Examples:

```text
ADR-0001-Family-Aggregate-Root.md
ADR-0007-Plugin-Architecture.md
ADR-0008-Official-Plugin-Structure.md
```

The numeric identifier MUST:

* contain four digits
* remain unique
* never be reused
* remain stable after publication

---

## Requests for Comments

Request for Comments files MUST use the following format:

```text
RFC-NNNN-Title-In-Pascal-Kebab-Case.md
```

Examples:

```text
RFC-0010-Official-Security-Plugin.md
RFC-0011-Official-Health-Plugin.md
```

Temporary letter-based identifiers MAY be used only during early drafting and MUST be replaced by permanent numeric identifiers before approval.

---

## Specifications

Specification document names MUST identify the subject being specified.

Examples:

```text
Plugin-Manifest-Specification.md
Domain-Specification.md
Security-Domain-Specification.md
```

The suffix `Specification` SHOULD be used for documents that define normative contracts.

---

## Reference documents

Reference document names MUST describe the single authoritative subject they define.

Examples:

```text
Language.md
Glossary.md
Acronyms.md
Naming-Conventions.md
Reserved-Words.md
Reference-Index.md
```

---

## Document headings

The first heading MUST use a human-readable document title.

Example:

```markdown
# FamilyOS naming conventions
```

Headings MUST follow the language rules defined in:

`docs/04-reference/Language.md`

---

# Test naming

## Test directories

Test directories SHOULD mirror the source package structure.

Example:

```text
src/familyos_cli/plugins/runtime/plugin_runtime.py
tests/unit/plugins/runtime/test_plugin_runtime.py
```

---

## Test files

Test files MUST use the following format:

```text
test_<subject>.py
```

Examples:

```text
test_plugin_runtime.py
test_capability_registry.py
test_domain_generation_pipeline.py
```

---

## Test functions

Test function names MUST use lowercase snake_case and describe observable behavior.

Preferred:

```python
def test_runtime_activates_initialized_plugins() -> None:
    ...
```

Avoid:

```python
def test_runtime() -> None:
    ...
```

Test names SHOULD follow this semantic structure:

```text
test_<subject>_<expected_behavior>
```

Context MAY be included when necessary:

```text
test_<subject>_<behavior>_when_<condition>
```

Example:

```python
def test_resolver_reports_conflict_when_constraints_are_incompatible() -> None:
    ...
```

---

## Test classes

Test classes MAY be used to group closely related behavior.

They MUST use PascalCase and begin with `Test`.

Example:

```python
class TestPluginRuntimeActivation:
    ...
```

Test classes MUST NOT define constructors.

---

## Fixtures

Fixture names MUST describe the provided object or state.

Examples:

```python
plugin_registry
active_runtime
valid_manifest
temporary_project
```

Generic names such as `setup`, `data`, or `fixture` SHOULD be avoided.

---

# Git naming

## Branches

Branches MUST use lowercase kebab-case with an approved category prefix.

Approved prefixes include:

```text
feature/
fix/
refactor/
docs/
test/
release/
hotfix/
```

Examples:

```text
feature/security-plugin
docs/reference-naming-conventions
fix/plugin-resolution-cycle
refactor/runtime-lifecycle
release/1.1.0
```

Branch names MUST NOT contain spaces, underscores, uppercase letters, or personal names.

Long-lived architecture work MAY use a descriptive feature branch.

---

## Commits

Commit subjects SHOULD use the imperative mood.

Examples:

```text
Add plugin capability registry
Document official naming conventions
Fix dependency cycle diagnostics
Refactor runtime lifecycle transitions
```

Commit subjects SHOULD:

* begin with an uppercase letter
* omit a trailing period
* describe one coherent change
* remain concise

---

## Release tags

Stable platform release tags MUST follow Semantic Versioning.

Format:

```text
vMAJOR.MINOR.PATCH
```

Examples:

```text
v1.0.0
v1.1.0
v1.1.1
```

Qualified release tags MAY add an approved suffix.

Examples:

```text
v1.0.0-platform
v1.1.0-rc.1
v2.0.0-beta.1
```

A release tag MUST be immutable after publication.

---

# Reserved prefixes

The following prefixes are reserved for official FamilyOS use:

```text
familyos
familyos_
familyos-
FamilyOS
ADR-
RFC-
```

Third-party plugins MUST NOT present themselves as official FamilyOS components.

Rules governing reserved identifiers are defined in:

`docs/04-reference/Reserved-Words.md`

---

# Prohibited naming patterns

The following naming patterns MUST NOT be used in production components unless explicitly justified:

```text
Manager
Helper
Helpers
Utility
Utilities
Common
Misc
Miscellaneous
Stuff
Thing
Object
Data
Base
Generic
Default
New
Old
Final
Temp
Temporary
Legacy
```

Some of these terms MAY be valid when they express an established and precise responsibility.

Examples of acceptable contextual use include:

```python
DefaultRecipeRegistry
BaseCommand
LegacyManifestAdapter
TemporaryDirectory
```

Their use MUST be intentional and reviewable.

---

# Public naming compatibility

A public name includes any identifier exposed through:

* the Plugin SDK
* the CLI
* specifications
* plugin manifests
* generated artifacts
* documented extension points
* importable public Python APIs

Public names MUST NOT be changed casually.

A public rename requires:

1. identification of affected consumers
2. compatibility strategy
3. deprecation period when applicable
4. migration documentation
5. release-note entry
6. architectural approval

---

# Naming review checklist

Before approving a new name, reviewers MUST verify that:

* the name uses official English terminology
* the name communicates one responsibility
* the name follows the required casing convention
* the name uses an established architectural suffix correctly
* the name does not duplicate an existing concept
* the name does not introduce an undocumented synonym
* the name does not conflict with a reserved word
* the name is suitable for long-term public use
* the name remains meaningful outside its immediate implementation
* the name complies with the Glossary and Acronyms documents

---

# Compliance

A component complies with this specification when:

* its name follows the convention for its artifact type
* its terminology is defined by the official reference documents
* its architectural suffix accurately represents its responsibility
* its public identifiers are stable and unambiguous
* it does not use prohibited or reserved naming patterns
* it does not introduce duplicate terminology

Non-compliant names MUST be corrected before the component becomes part of a stable public contract.

Existing names that predate this specification SHOULD be reviewed progressively.

Changes to stable public names require compatibility analysis.

---

# Maintenance

This document evolves together with the FamilyOS platform contracts.

A new naming convention MAY be added when a new platform-wide component category is introduced.

Local implementation preferences MUST NOT be added unless they apply consistently across the platform.

Changes require documentation review and architectural approval.

---

# Summary

FamilyOS naming conventions establish a consistent language across documentation, architecture, source code, plugins, generation artifacts, tests, and delivery workflows.

Names are part of the platform contract.

Every official name must communicate intent, reflect architectural responsibility, use established terminology, and remain stable enough to support the long-term evolution of the FamilyOS ecosystem.
