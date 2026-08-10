# FamilyOS Naming Conventions

## Purpose

This document defines the canonical naming conventions used across the FamilyOS platform.

It provides the reference naming rules for:

* architecture;
* documentation;
* domains;
* plugins;
* capabilities;
* contributions;
* source code;
* command-line interfaces;
* generated artifacts;
* tests;
* Git workflows;
* public identifiers.

This document complements the normative specifications:

* SPEC-0002 — Identifier;
* SPEC-0008 — Naming Conventions;
* SPEC-0009 — Plugin Manifest;
* SPEC-0010 — Plugin Capability Contract.

Identifier identity, uniqueness, ownership, permanence, compatibility, and migration rules are governed primarily by SPEC-0002.

This document defines the canonical naming representation used throughout FamilyOS.

---

# General Naming Principles

FamilyOS naming SHALL follow these principles:

* names MUST communicate architectural responsibility;
* established terminology MUST be reused consistently;
* public names MUST remain stable;
* implementation details MUST NOT define public identity;
* display names and identifiers MUST remain distinct;
* namespace ownership MUST remain explicit;
* versions MUST remain separate from canonical identifiers;
* ambiguous generic terminology SHOULD be avoided.

Naming is part of the FamilyOS platform contract.

A public name SHALL NOT be changed solely for stylistic consistency when doing so would break compatibility.

---

# Identifier Categories

FamilyOS distinguishes multiple identifier categories.

The category determines syntax and semantic responsibility.

---

## Governance Identifiers

Governance identifiers identify governed platform artifacts.

Format:

```text
<PREFIX>-<NUMBER>
```

Examples:

```text
SPEC-0002
ADR-0007
RFC-0010
```

Governance identifiers MUST:

* use an approved uppercase category prefix;
* remain unique within their category;
* remain stable after publication;
* never be reassigned.

The `<PREFIX>-<NUMBER>` representation applies to governance identifiers and MUST NOT be treated as the universal syntax for all FamilyOS identifiers.

---

## Ecosystem Identifiers

Ecosystem identifiers identify persistent resources participating in the FamilyOS extension ecosystem.

Canonical format:

```text
<namespace>.<resource>
```

Examples:

```text
familyos.security
familyos.education
acme.backup
vendor.documents.archive
```

Ecosystem identifiers MUST:

* use lowercase dot-separated segments;
* use an authorized namespace;
* remain stable;
* remain independent from versions;
* remain independent from implementation paths.

---

## Capability Identifiers

Capability identifiers identify stable functional contracts.

Canonical official plugin capability format:

```text
familyos.<plugin-name>.<capability>
```

Examples:

```text
familyos.health.record
familyos.finance.account
familyos.education.course
familyos.documents.archive
familyos.communication.messaging
```

Capability identifiers MUST represent abilities or contracts, not implementation class names.

---

# Case Conventions

## PascalCase

PascalCase MUST be used for:

* Python classes;
* type names;
* domain names in prose;
* bounded context names;
* command types;
* query types;
* event types;
* value object types.

Examples:

```text
Family
Person
Education
SecurityPlugin
PluginDescriptor
PluginActivated
CreatePerson
PluginId
```

---

## snake_case

Lowercase snake_case MUST be used for:

* Python modules;
* Python functions;
* Python methods;
* Python variables;
* Python import packages.

Examples:

```text
plugin_descriptor
plugin_registry
familyos_security_plugin
plugin_id
capability_id
activate_plugin
```

---

## kebab-case

Lowercase kebab-case MUST be used where applicable for:

* Python distribution names;
* CLI tokens;
* persisted generation resource names;
* generated artifact names.

Examples:

```text
familyos-security-plugin
domain-summary-documentation
default-domain
complete-documentation
```

---

## Dot-separated lowercase

Lowercase dot-separated names MUST be used for namespaced ecosystem and capability identifiers.

Examples:

```text
familyos.security
familyos.education
familyos.security.audit
familyos.education.course
```

---

# Domain-Driven Design Naming

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

Normalized domain identifiers MUST use lowercase forms.

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

A normalized domain identifier MUST NOT automatically be interpreted as a Plugin Identifier.

Example:

```text
education
```

represents the normalized Education domain context.

The official Education Plugin Identifier is:

```text
familyos.education
```

---

## Bounded Contexts

Bounded context names MUST use PascalCase and describe a coherent business language boundary.

Preferred:

```text
Identity
Documents
Communication
Education
```

Avoid:

```text
Database
Backend
Api
Infrastructure
```

A bounded context SHOULD be named after a business capability rather than a technical implementation layer.

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

Documentation describing aggregates SHOULD use the aggregate name.

Example:

```text
aggregates/Family.md
```

---

## Aggregate Roots

Aggregate root classes MUST use the business concept name without redundant suffixes.

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

The aggregate-root role SHOULD be expressed through architecture and documentation rather than duplicated in the type name.

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

The suffix `Entity` SHOULD NOT be used unless necessary to disambiguate a technical contract.

Avoid:

```python
PersonEntity
DocumentEntity
```

---

## Value Objects

Value object names MUST represent the value itself.

Examples:

```python
PersonId
FamilyId
PluginId
CapabilityId
EmailAddress
DateRange
PluginVersion
VersionConstraint
```

The suffix `ValueObject` MUST NOT be used.

---

## Identifier Value Objects

Identifier value objects SHOULD use:

```text
<Concept>Id
```

Examples:

```python
PersonId
FamilyId
PluginId
CapabilityId
```

The PascalCase spelling MUST use:

```text
Id
```

and SHOULD NOT use:

```text
ID
```

inside Python type names.

---

## Domain Services

Domain service names MUST describe the business operation.

The suffix `Service` SHOULD be used only when the behavior does not belong naturally to an entity or value object.

Examples:

```python
MembershipEligibilityService
DocumentClassificationService
```

---

## Domain Events

Domain event names MUST:

* use PascalCase;
* describe a completed fact;
* use past-tense wording where natural.

Examples:

```python
PersonCreated
MemberAdded
DocumentArchived
PluginActivated
```

Avoid:

```python
CreatePerson
AddMember
ArchiveDocument
```

when representing completed events.

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

A command name MUST NOT imply that the requested action has already completed.

---

## Queries

Query names MUST describe requested information.

Examples:

```python
GetPerson
ListFamilyMembers
FindDocuments
GetPluginStatus
```

---

# Plugin Naming

## Plugin Identity Model

FamilyOS distinguishes the following plugin representations:

```text
Display Name
Plugin Identifier
Distribution Name
Python Import Package
Implementation Class
Version
```

These representations MUST NOT be treated as interchangeable.

Example:

```text
Display Name:
FamilyOS Education Plugin

Plugin Identifier:
familyos.education

Distribution Name:
familyos-education-plugin

Python Import Package:
familyos_education_plugin

Implementation Class:
EducationPlugin

Version:
1.0.0
```

---

## Plugin Display Names

Plugin display names MUST use human-readable PascalCase words.

Official plugin display names SHOULD use the corresponding domain or function name followed by `Plugin`.

Examples:

```text
Security Plugin
Health Plugin
Finance Plugin
Education Plugin
Documents Plugin
Communication Plugin
Documentation Plugin
```

Product-facing names MAY include `FamilyOS`.

Examples:

```text
FamilyOS Security Plugin
FamilyOS Education Plugin
```

Display names MUST NOT serve as canonical runtime identity.

---

## Official Plugin Identifiers

Official Plugin Identifiers MUST use the `familyos` namespace.

Canonical format:

```text
familyos.<plugin-name>
```

Examples:

```text
familyos.security
familyos.health
familyos.finance
familyos.education
familyos.documents
familyos.communication
familyos.documentation
```

Official Plugin Identifiers MUST:

* use lowercase dot-separated syntax;
* remain stable;
* use an authorized FamilyOS plugin name;
* exclude version information.

---

## Third-Party Plugin Identifiers

Third-party plugins MUST use a namespace controlled by the plugin owner.

Examples:

```text
acme.backup
example.health.import
vendor.documents.archive
```

Third-party plugins MUST NOT use the `familyos` namespace without explicit authorization.

Third-party identifiers MAY refer to official FamilyOS domains but MUST NOT imply official ownership.

---

## Plugin Identifier Stability

Plugin Identifiers MUST remain stable across compatible versions.

The following changes MUST NOT automatically alter the Plugin Identifier:

* class renaming;
* internal refactoring;
* source relocation;
* package reorganization;
* display-name change;
* implementation architecture changes.

Changing a stable Plugin Identifier is an identity migration and requires compatibility governance.

---

## Legacy Plugin Identifiers

Existing identifiers predating the canonical namespace convention MAY temporarily remain in use.

Known legacy forms include:

```text
education
documents
communication
documentation
```

Canonical targets are:

```text
education
→ familyos.education

documents
→ familyos.documents

communication
→ familyos.communication

documentation
→ familyos.documentation
```

These mappings define canonical targets only.

They MUST NOT be interpreted as authorization for automatic migration.

Legacy identifiers SHALL be handled according to SPEC-0002 and SPEC-0009 compatibility rules.

---

## Plugin Package Names

Python distribution names MUST use lowercase kebab-case.

Recommended official form:

```text
familyos-<plugin-name>-plugin
```

Examples:

```text
familyos-security-plugin
familyos-health-plugin
familyos-finance-plugin
familyos-education-plugin
familyos-documents-plugin
familyos-communication-plugin
```

A distribution name MUST NOT be treated as the Plugin Identifier.

---

## Plugin Import Packages

Python import packages MUST use lowercase snake_case.

Examples:

```python
familyos_security_plugin
familyos_health_plugin
familyos_finance_plugin
familyos_education_plugin
```

Import package names MUST NOT define runtime plugin identity.

---

## Plugin Classes

The primary plugin implementation class MUST use the domain or function name followed by `Plugin`.

Examples:

```python
SecurityPlugin
HealthPlugin
FinancePlugin
EducationPlugin
DocumentsPlugin
CommunicationPlugin
DocumentationPlugin
```

Generic names SHOULD NOT be used.

Avoid:

```python
MainPlugin
GenericPlugin
FamilyOSPlugin
```

---

## Plugin Versions

Plugin versions MUST remain separate from Plugin Identifiers.

Canonical identity:

```text
familyos.security
```

Version:

```text
1.0.0
```

A combined display or resolution representation MAY use:

```text
familyos.security@1.0.0
```

The `@1.0.0` portion MUST NOT be part of the canonical Plugin Identifier.

---

# Capability Naming

## Capability Identifier Format

Official plugin capability identifiers MUST use:

```text
familyos.<plugin-name>.<capability>
```

Examples:

```text
familyos.health.profile
familyos.health.record

familyos.finance.account
familyos.finance.transaction
familyos.finance.asset
familyos.finance.liability
familyos.finance.budget

familyos.education.learner
familyos.education.course
familyos.education.record

familyos.documents.document
familyos.documents.archive

familyos.communication.messaging
familyos.communication.archive
```

---

## Capability Ownership

A plugin-owned capability SHOULD use the Plugin Identifier as its prefix.

Example:

```text
Plugin:
familyos.education

Capabilities:
familyos.education.learner
familyos.education.course
familyos.education.record
```

A capability MUST NOT use another plugin's namespace without authorization.

---

## Capability Semantics

The final capability segment MUST describe the functional ability represented by the contract.

Preferred:

```text
familyos.documents.archive
familyos.finance.account
familyos.communication.messaging
```

Avoid:

```text
familyos.documents.document_archive_capability
familyos.finance.finance_account_capability
```

Capability identifiers MUST remain independent from implementation class names.

---

## Capability Stability

Published Capability Identifiers MUST remain stable across compatible versions.

Breaking identity changes require:

* compatibility analysis;
* migration strategy;
* documentation;
* test updates;
* architectural approval.

A retired Capability Identifier MUST NOT be reassigned to an unrelated capability.

---

## Legacy Capability Forms

Older capability identifiers MAY exist in forms such as:

```text
security.validation
generation.template
documents.storage
```

New official capability contracts MUST use the canonical namespaced form.

Canonical target:

```text
familyos.<plugin-name>.<capability>
```

Existing public capability identifiers MUST NOT be rewritten automatically.

---

# Contribution Naming

## Contribution Types

Contribution type names MUST describe the contributed extension.

Types SHOULD end with `Contribution`.

Examples:

```python
GenerationContribution
DomainGenerationContribution
GenerationRecipeContribution
TemplateContribution
```

---

## Contribution Identifiers

Externally referenced contributions SHOULD use stable namespaced identifiers when appropriate.

Examples:

```text
familyos.generation.recipe
familyos.generation.template
familyos.domain.documentation
```

Contribution identity MUST follow SPEC-0002.

---

# Generation Framework Naming

## Artifacts

Artifact names MUST identify the generated deliverable.

Examples:

```text
domain-readme
aggregate-documentation
plugin-manifest
python-module
```

Artifact type names SHOULD end with `Artifact`.

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

Preset identifiers MUST use lowercase kebab-case unless another specification defines a category-specific identifier contract.

Examples:

```text
security
default-domain
complete-documentation
```

Preset types MUST end with `Preset` or `PresetDefinition` according to responsibility.

---

## Strategies

Generation strategy type names MUST describe interchangeable behavior.

Examples:

```python
DomainDocumentationStrategy
AggregateDocumentationStrategy
```

Persisted strategy names SHOULD use lowercase kebab-case.

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

# Python Naming

## Classes

Python classes MUST use PascalCase.

Examples:

```python
PluginDescriptor
PluginRegistry
CapabilityRegistry
GenerationPipeline
```

---

## Functions and Methods

Functions and methods MUST use lowercase snake_case.

Examples:

```python
register_plugin
resolve_dependencies
load_manifest
activate_plugin
```

---

## Variables

Variables MUST use lowercase snake_case.

Names SHOULD describe the semantic value stored.

Preferred:

```python
plugin_id
capability_id
plugin_registry
manifest_path
```

Avoid:

```python
name
value
data
```

when the value has a more precise architectural meaning.

For example, a method accepting a canonical Plugin Identifier SHOULD prefer:

```python
def get(plugin_id: str) -> PluginDescriptor | None:
    ...
```

instead of:

```python
def get(name: str) -> PluginDescriptor | None:
    ...
```

---

## Constants

Constants SHOULD use uppercase snake_case.

Examples:

```python
DEFAULT_PLUGIN_DIRECTORY
SUPPORTED_MANIFEST_VERSION
```

---

## Python Reserved Words

Python keywords MUST NOT be used as Python identifiers.

Python built-ins SHOULD NOT be shadowed when a clearer alternative exists.

Avoid:

```python
id
type
list
input
format
```

where a more precise value name can be used.

Preferred:

```python
plugin_id
artifact_type
result_list
output_format
```

Public contracts MAY retain an existing field such as:

```python
PluginDescriptor.id
```

when compatibility requirements outweigh stylistic preference.

---

# Command-Line Interface Naming

## Commands

CLI commands MUST use lowercase names.

Command groups MAY use nouns.

Examples:

```text
familyos plugin
familyos generation
familyos domain
```

Commands performing actions SHOULD use verbs.

Examples:

```text
create
resolve
validate
install
activate
```

---

## Options

Long options MUST use lowercase kebab-case and begin with two hyphens.

Examples:

```text
--plugin-id
--output-format
--include-diagnostics
--destination
```

Short options MAY be provided when unambiguous.

Examples:

```text
-v
-q
-h
```

A short option MUST NOT represent incompatible meanings within the same command context.

---

## Positional Arguments

Python representations of CLI positional arguments MUST use lowercase snake_case.

Examples:

```text
plugin_id
domain_name
artifact_type
```

---

## Boolean Options

Boolean options SHOULD describe the enabled behavior positively.

Preferred:

```text
--include-diagnostics
--overwrite
--strict
```

Avoid unnecessary double-negative forms.

---

# Documentation Naming

## Architecture Decision Records

ADR filenames MUST use:

```text
ADR-NNNN-Descriptive-Title.md
```

Example:

```text
ADR-0007-Official-Plugin-Architecture.md
```

The ADR identifier MUST remain stable even if the title changes.

---

## Requests for Comments

RFC filenames MUST use:

```text
RFC-NNNN-Descriptive-Title.md
```

Examples:

```text
RFC-0010-Official-Security-Plugin.md
RFC-0011-Official-Health-Plugin.md
```

Temporary drafting identifiers MAY exist only where the RFC governance process explicitly permits them.

---

## Specifications

Specification filenames MUST identify both their governance identifier and subject.

Format:

```text
SPEC-NNNN-Descriptive-Title.md
```

Examples:

```text
SPEC-0002-Identifier.md
SPEC-0008-Naming-Conventions.md
SPEC-0009-Plugin-Manifest.md
SPEC-0010-Plugin-Capability-Contract.md
```

---

## Reference Documents

Reference document names MUST describe one authoritative responsibility.

Examples:

```text
Language.md
Glossary.md
Acronyms.md
Naming-Conventions.md
Reserved-Words.md
Reference-Index.md
```

Another document MUST NOT silently duplicate the responsibility of an official reference document.

---

## Document Headings

The first heading MUST provide a clear human-readable title.

Headings MUST follow FamilyOS documentation language and formatting rules.

---

# Test Naming

## Test Directories

Test directories SHOULD mirror relevant source structure where practical.

Example:

```text
src/familyos_cli/plugins/runtime/plugin_runtime.py

tests/unit/plugins/runtime/test_plugin_runtime.py
```

---

## Test Files

Test files MUST use:

```text
test_<subject>.py
```

Examples:

```text
test_plugin_runtime.py
test_plugin_registry.py
test_capability_registry.py
```

---

## Test Functions

Test functions MUST use lowercase snake_case and SHOULD describe observable behavior.

Preferred:

```python
def test_runtime_activates_initialized_plugins() -> None:
    ...
```

Recommended structure:

```text
test_<subject>_<expected_behavior>
```

Context MAY be added:

```text
test_<subject>_<behavior>_when_<condition>
```

---

## Test Classes

Test classes MAY group closely related behavior.

They MUST:

* use PascalCase;
* begin with `Test`;
* avoid constructors.

Example:

```python
class TestPluginRuntimeActivation:
    ...
```

---

## Fixtures

Fixture names SHOULD describe the provided state or object.

Preferred:

```text
plugin_registry
active_runtime
valid_manifest
temporary_project
```

Avoid:

```text
setup
data
fixture
```

when a more precise name exists.

---

# Git Naming

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
release/4.7.0
```

Branch names SHOULD NOT contain:

* spaces;
* uppercase letters;
* personal names;
* unnecessary underscores.

---

## Commits

Commit subjects SHOULD:

* describe one coherent change;
* remain concise;
* use imperative wording;
* omit unnecessary trailing punctuation.

Examples:

```text
Add plugin capability registry
Document canonical plugin identifiers
Fix dependency cycle diagnostics
```

---

## Release Tags

Stable platform release tags MUST follow approved FamilyOS release governance.

Base format:

```text
vMAJOR.MINOR.PATCH
```

Examples:

```text
v4.6.0
v4.6.0-quality-framework
```

Qualified suffixes MAY be used where explicitly approved.

Published tags MUST remain immutable.

---

# Reserved Prefixes

The following prefixes are reserved for official FamilyOS use according to context:

```text
familyos
familyos_
familyos-
FamilyOS
ADR-
RFC-
SPEC-
```

The `familyos` ecosystem namespace MUST NOT be used by third-party plugins without authorization.

Rules governing reserved names are defined in:

```text
docs/04-reference/Reserved-Words.md
```

---

# Public Naming Compatibility

A public name includes any name or identifier exposed through:

* Plugin SDK;
* plugin manifests;
* CLI;
* specifications;
* runtime registries;
* generated artifacts;
* documented extension points;
* importable public Python APIs.

Public names MUST NOT be changed casually.

A compatibility-sensitive rename requires:

1. identification of affected consumers;
2. compatibility analysis;
3. migration strategy;
4. deprecation or aliasing where applicable;
5. documentation updates;
6. test updates;
7. release-note entry;
8. architectural approval.

---

# Legacy Naming

Existing names that predate current conventions SHOULD be classified as:

* compliant;
* legacy-compatible;
* deprecated;
* scheduled for migration;
* explicitly exempted.

Stable public names MUST NOT be renamed automatically.

Compatibility requirements take precedence over stylistic consistency.

Legacy acceptance MUST NOT establish a new canonical naming convention.

---

# Naming Review Checklist

Before approving a public name or identifier representation, reviewers MUST verify that:

* official English terminology is used;
* the name communicates one responsibility;
* the correct casing convention is used;
* the correct separator convention is used;
* identifier category is understood;
* namespace ownership is valid;
* display names and identifiers remain distinct;
* package names and identifiers remain distinct;
* versions remain separate from canonical identifiers;
* established architectural suffixes are used correctly;
* no undocumented synonym is introduced;
* reserved terms are respected;
* prohibited generic terminology is avoided;
* public compatibility impact is understood;
* the name remains suitable for long-term use.

For Plugin Identifiers, reviewers MUST additionally verify:

* lowercase dot-separated representation;
* authorized namespace;
* stable plugin-name segment;
* no embedded version;
* compliance with SPEC-0002 and SPEC-0009.

For Capability Identifiers, reviewers MUST additionally verify:

* lowercase dot-separated representation;
* authorized namespace;
* expected plugin prefix;
* functional final segment;
* compliance with SPEC-0002 and SPEC-0010.

---

# Compliance

A component complies with these conventions when:

* its names follow the convention for their artifact type;
* public identifiers use the correct category representation;
* namespace ownership is respected;
* terminology remains consistent;
* versions are separated from identity;
* display names remain separate from identifiers;
* public compatibility rules are respected;
* reserved and prohibited naming rules are respected.

New public FamilyOS resources MUST use canonical naming.

Existing stable names require compatibility analysis before migration.

---

# Maintenance

This document evolves together with FamilyOS platform contracts.

New naming conventions MAY be introduced when:

* a new identifier category is established;
* a new platform-wide artifact type is introduced;
* ecosystem ownership rules require clarification;
* a recurring ambiguity needs canonical resolution.

Local implementation preferences MUST NOT be elevated into platform-wide naming rules unless they apply consistently across FamilyOS.

Changes affecting public naming contracts require documentation review and architectural approval.

---

# Summary

FamilyOS naming conventions establish a consistent language across architecture, documentation, source code, plugins, capabilities, generated artifacts, tests, and delivery workflows.

FamilyOS distinguishes governance identifiers from ecosystem and capability identifiers.

Governance identities use forms such as:

```text
SPEC-0002
ADR-0007
RFC-0010
```

Official Plugin Identifiers use:

```text
familyos.<plugin-name>
```

Official plugin Capability Identifiers use:

```text
familyos.<plugin-name>.<capability>
```

Examples:

```text
familyos.education
familyos.education.course

familyos.documents
familyos.documents.archive

familyos.communication
familyos.communication.messaging
```

Names are part of the platform contract.

Every official name and identifier representation must communicate intent, preserve ownership, remain stable, and support the long-term evolution of the FamilyOS ecosystem.
