# FamilyOS Reserved Words

## Purpose

This document defines the reserved words, identifiers, namespaces, prefixes, suffixes, domain names, plugin names, lifecycle terms, architectural terms, and naming restrictions used throughout the FamilyOS platform.

Reserved terms protect:

* architectural meaning;
* platform identity;
* ecosystem ownership;
* official plugin identity;
* namespace boundaries;
* public contracts;
* compatibility;
* documentation consistency;
* implementation clarity.

This document complements:

* SPEC-0002 — Identifier;
* SPEC-0008 — Naming Conventions;
* SPEC-0009 — Plugin Manifest;
* SPEC-0010 — Plugin Capability Contract;
* `docs/04-reference/Naming-Conventions.md`.

This document defines ownership and reservation.

It does not independently redefine identifier categories or naming syntax established by the normative specifications.

---

# Scope

This document applies to:

* documentation;
* architecture;
* specifications;
* plugins;
* capabilities;
* contributions;
* manifests;
* source code;
* CLI interfaces;
* generated artifacts;
* configuration;
* packages;
* public extension points;
* third-party ecosystem integrations.

A reserved term MAY be used only according to the responsibility and ownership defined by FamilyOS governance.

---

# Reservation Principles

FamilyOS reservations follow these principles:

1. a reserved term has a defined architectural or ownership meaning;
2. reservation SHALL protect interoperability rather than stylistic preference;
3. public identity SHALL remain stable;
4. third-party extensions SHALL retain their own namespace ownership;
5. FamilyOS ownership SHALL NOT be implied without authorization;
6. compatibility requirements take precedence over cosmetic consistency;
7. legacy public identifiers SHALL NOT be renamed automatically;
8. a reservation SHALL NOT silently redefine an existing contract.

---

# Identifier Categories

FamilyOS distinguishes several identifier categories.

The identifier category determines how reservation rules apply.

---

## Governance Identifiers

Governance identifiers use forms such as:

```text
SPEC-0002
ADR-0007
RFC-0010
```

Their category prefixes are reserved.

---

## Ecosystem Identifiers

Ecosystem identifiers use authorized namespaces.

Examples:

```text
familyos.security
familyos.education
acme.backup
vendor.documents.archive
```

The first segment identifies ownership.

---

## Capability Identifiers

Capability identifiers represent functional contracts.

Examples:

```text
familyos.health.record
familyos.finance.account
familyos.education.course
```

Capability namespace ownership SHALL follow SPEC-0002 and SPEC-0010.

---

# Reserved FamilyOS Identity

The following representations are reserved for the FamilyOS platform identity:

```text
FamilyOS
familyos
FAMILYOS
```

These names MUST NOT be used by third-party projects in a way that implies:

* ownership by FamilyOS;
* official FamilyOS status;
* certification by FamilyOS;
* endorsement by FamilyOS;
* platform authority.

The restrictions apply according to naming context.

Examples include:

```text
familyos.*
familyos_*
familyos-*
FamilyOS *
```

when those forms imply official ownership.

---

# Reserved Governance Prefixes

The following governance prefixes are reserved:

```text
SPEC-
ADR-
RFC-
```

They identify governed FamilyOS artifacts.

A third-party component MUST NOT use these prefixes to imply participation in the official FamilyOS governance process.

---

## SPEC-

```text
SPEC-
```

is reserved for approved or governed FamilyOS specifications.

An official specification identifier MUST:

* use the approved numeric format;
* remain unique;
* remain stable;
* never be reassigned;
* refer to exactly one governed specification.

Examples:

```text
SPEC-0002
SPEC-0008
SPEC-0009
SPEC-0010
```

---

## ADR-

```text
ADR-
```

is reserved for Architecture Decision Records governed by FamilyOS architecture governance.

An official ADR identifier MUST:

* use the approved numeric format;
* remain unique;
* remain stable;
* never be reassigned;
* identify exactly one architectural decision record.

Examples:

```text
ADR-0007
ADR-0010
ADR-0011
```

---

## RFC-

```text
RFC-
```

is reserved for proposals governed by the FamilyOS RFC process.

An official RFC identifier MUST:

* contain four digits;
* be unique;
* remain stable;
* never be reassigned;
* refer to one governed proposal.

Examples:

```text
RFC-0010
RFC-0011
RFC-0012
```

Temporary letter-based identifiers MAY exist during early drafting when permitted by RFC governance but MUST NOT be treated as permanent platform identifiers.

---

# Reserved Reference Document Names

The following file names are reserved for their official responsibilities:

```text
README.md
Language.md
Glossary.md
Acronyms.md
Naming-Conventions.md
Reserved-Words.md
Reference-Index.md
```

Within `docs/04-reference/`, another document MUST NOT assume one of these authoritative responsibilities under an unrelated or competing name.

---

# Reserved Platform Component Names

The following names identify established platform concepts and are contract-reserved:

```text
Application Layer
Artifact
Capability
Capability Identifier
Capability Provider
Capability Registry
Command
Command Context
Contribution
Contribution Identifier
Contribution Provider
Contribution Registry
Dependency Graph
Diagnostic Pipeline
Domain
Domain Context
Domain Generation Framework
Domain Generation Pipeline
Domain Model
Ecosystem Identifier
Entity
Event
Generation Artifact
Generation Context
Generation Framework
Generation Pipeline
Generation Recipe
Generation Request
Generation Result
Generation Strategy
Governance Identifier
Plugin
Plugin Capability
Plugin Contribution
Plugin Dependency
Plugin Discovery
Plugin Ecosystem
Plugin Identifier
Plugin Installer
Plugin Loader
Plugin Manifest
Plugin Metadata
Plugin Package
Plugin Registry
Plugin Repository
Plugin Resolver
Plugin Runtime
Plugin SDK
Plugin Verifier
Preset
Recipe
Repository
Resolution Diagnostic
Resolution Plan
Runtime Context
Runtime State
Specification
Template
Use Case
Value Object
```

These terms MUST retain the meanings established by FamilyOS architecture, specifications, and reference documentation.

A component MUST NOT reuse one of these names for an incompatible responsibility.

---

# Reserved Architectural Suffixes

The following suffixes have established architectural meanings:

```text
Adapter
Artifact
Builder
Context
Contribution
Definition
Descriptor
Error
Factory
Formatter
Loader
Mapper
Metadata
Pipeline
Plan
Policy
Provider
Registry
Repository
Request
Resolver
Result
Selector
Service
Specification
Strategy
Template
UseCase
Validator
Verifier
```

A suffix is not globally prohibited.

However, it is reserved for components fulfilling the corresponding architectural responsibility defined by FamilyOS naming and architecture contracts.

Examples of misuse include:

```text
PluginResolver
```

for a component responsible only for installation, or:

```text
CapabilityRegistry
```

for a component that only formats capability output.

Suffixes SHALL communicate responsibility rather than perceived importance.

---

# Reserved Plugin Architecture Terms

The following plugin terms have stable architectural meanings:

```text
Plugin
Plugin Identifier
Plugin Manifest
Plugin Metadata
Plugin Package
Plugin SDK
Plugin Ecosystem
Plugin Discovery
Plugin Repository
Plugin Resolver
Plugin Installer
Plugin Loader
Plugin Registry
Plugin Runtime
Plugin Capability
Plugin Contribution
Plugin Dependency
Plugin Verifier
```

These terms MUST NOT be treated as interchangeable.

In particular:

* a Plugin Manifest describes a plugin package;
* a Plugin Identifier identifies the plugin;
* a Plugin Package contains distributable or loadable resources;
* a Plugin Loader loads plugin descriptors or implementations;
* a Plugin Registry stores identifiable plugin registrations;
* a Plugin Resolver resolves dependency and compatibility constraints;
* a Plugin Installer makes a plugin package available;
* a Plugin Runtime controls execution lifecycle;
* a Plugin Capability exposes functional contracts.

---

# Reserved Lifecycle Terms

The following runtime lifecycle states are reserved:

```text
LOADED
INITIALIZED
ACTIVE
STOPPING
STOPPED
```

These names represent official runtime states.

They MUST NOT be redefined with incompatible semantics.

Additional lifecycle states require:

* an explicit contract;
* transition rules;
* compatibility analysis;
* architectural approval.

The following lifecycle operation names are also reserved:

```text
load
initialize
activate
stop
```

These verbs MUST NOT be treated as synonyms.

---

# Reserved Dependency-Resolution Terms

The following terms represent separate, stable responsibilities:

```text
discover
select
resolve
order
verify
install
load
activate
```

Their responsibilities are:

| Term     | Reserved responsibility                                               |
| -------- | --------------------------------------------------------------------- |
| discover | Locate available plugin packages, manifests, or repository records    |
| select   | Choose candidate resources from an available set                      |
| resolve  | Determine a valid result from dependencies, versions, and constraints |
| order    | Produce a dependency-safe processing sequence                         |
| verify   | Confirm integrity, compatibility, authenticity, trust, or conformance |
| install  | Make a plugin package available to the platform                       |
| load     | Read, resolve, or instantiate the plugin implementation               |
| activate | Make a loaded and initialized plugin operational                      |

A pipeline MAY coordinate multiple operations, but naming MUST preserve these conceptual distinctions.

---

# Reserved Generation Terms

The following terms have stable meanings in the Generation Framework:

```text
artifact
context
definition
engine
pipeline
plan
preset
recipe
request
result
strategy
template
```

These terms MUST NOT be used interchangeably.

In particular:

* a `Template` is not a `Recipe`;
* a `Recipe` is not a `Preset`;
* a `Preset` is not a `Strategy`;
* a `Plan` is not a `Result`;
* a `Definition` is not an instantiated `Artifact`;
* a `Context` is not an unrestricted dependency container.

---

# Reserved Domain Terms

The following Domain-Driven Design terms retain their established meanings:

```text
Aggregate
Aggregate Root
Bounded Context
Command
Domain
Domain Event
Domain Model
Domain Service
Entity
Repository
Specification
Value Object
```

These terms MUST NOT be used merely as decorative suffixes.

Examples of discouraged or prohibited misuse include:

```text
PersonEntity
```

when `Person` is already the accepted entity name, and:

```text
FamilyAggregateRoot
```

when `Family` is already the accepted aggregate-root type name.

---

# Reserved Official Domain Names

The following names are reserved for official FamilyOS domains:

```text
Identity
Person
Family
Security
Health
Finance
Education
Home
Tasks
Documents
Communication
Integration
Notification
AI
```

The corresponding normalized domain names are also reserved:

```text
identity
person
family
security
health
finance
education
home
tasks
documents
communication
integration
notification
ai
```

These normalized names represent official domain ownership.

They MUST NOT automatically be interpreted as canonical Plugin Identifiers.

For example:

```text
education
```

is the normalized Education domain name.

The canonical official Education Plugin Identifier is:

```text
familyos.education
```

---

# Reserved Official Plugin Identifiers

The following canonical Plugin Identifiers are reserved for official FamilyOS ownership:

```text
familyos.identity
familyos.person
familyos.family
familyos.security
familyos.health
familyos.finance
familyos.education
familyos.home
familyos.tasks
familyos.documents
familyos.communication
familyos.integration
familyos.notification
familyos.ai
familyos.documentation
```

Reservation indicates ownership protection.

It does not necessarily assert that every listed plugin currently exists or is implemented.

Third-party extensions MUST NOT claim these identifiers.

---

# Reserved Official Plugin Display Names

The following display names are reserved for official FamilyOS plugins:

```text
Identity Plugin
Person Plugin
Family Plugin
Security Plugin
Health Plugin
Finance Plugin
Education Plugin
Home Plugin
Tasks Plugin
Documents Plugin
Communication Plugin
Integration Plugin
Notification Plugin
AI Plugin
Documentation Plugin
```

Product-facing forms prefixed by `FamilyOS` are also reserved where they imply official status.

Examples:

```text
FamilyOS Security Plugin
FamilyOS Education Plugin
FamilyOS Documents Plugin
```

Reservation covers confusingly equivalent representations differing only by:

* capitalization;
* punctuation;
* spacing;
* common package normalization;
* superficial singular/plural changes.

---

# Documents and Documentation

The following concepts are distinct:

```text
Documents
Documentation
```

The canonical official Plugin Identifiers are:

```text
Documents Plugin
→ familyos.documents
```

and:

```text
Documentation Plugin
→ familyos.documentation
```

These identifiers MUST NOT be treated as aliases or synonyms.

The namespace:

```text
familyos.documents
```

belongs to the Documents Plugin context.

The namespace:

```text
familyos.documentation
```

belongs to the Documentation Plugin context.

---

# Reserved Official Capability Namespace Patterns

Capabilities exposed by official FamilyOS plugins SHALL use official namespace ownership according to SPEC-0010.

Canonical pattern:

```text
familyos.<plugin-name>.<capability>
```

Existing canonical examples include:

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

Third-party extensions MUST NOT expose capabilities under these namespaces without authorization.

---

# Reserved Platform Capability Namespaces

The following platform-owned namespace examples are reserved where governed by corresponding FamilyOS contracts:

```text
familyos.security.audit
familyos.security.encryption
familyos.security.policy
familyos.documents.classification
familyos.generation.recipes
familyos.generation.recipe
familyos.generation.template
familyos.domain.documentation
familyos.runtime.lifecycle
```

Reservation of an identifier does not by itself guarantee that the corresponding runtime capability currently exists.

It protects ownership and future compatibility.

---

# Official and Third-Party Namespace Ownership

A third-party plugin MAY integrate with an official FamilyOS domain.

Preferred examples:

```text
acme.security.backup
example.health.import
vendor.documents.archive
```

Third-party identifiers MUST NOT falsely claim official FamilyOS ownership.

Without explicit authorization, third parties MUST NOT use forms such as:

```text
familyos.security
familyos.health
familyos.documents
familyos.education
```

or any derived capability namespace such as:

```text
familyos.security.backup
familyos.education.import
```

---

# Legacy Official Plugin Identifiers

The following current or historical short identifiers MAY exist as legacy-compatible identifiers:

```text
education
documents
communication
documentation
```

Their canonical targets are:

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

These mappings define canonical ownership and migration targets.

They MUST NOT be interpreted as authorization for automatic migration.

A legacy identifier MAY remain temporarily supported when compatibility requirements justify it.

Legacy support SHALL NOT redefine the canonical identifier convention.

---

# Legacy Identifier Protection

A legacy public identifier that remains in active use is still protected from reassignment.

For example, while:

```text
education
```

remains accepted as the historical identifier of the official Education Plugin, another plugin MUST NOT claim `education` as an unrelated plugin identity.

Legacy identifiers SHALL remain traceable throughout migration and deprecation.

---

# Future-Reserved Namespaces

The following namespaces are reserved for potential platform evolution:

```text
familyos.api
familyos.core
familyos.domain
familyos.events
familyos.identity
familyos.marketplace
familyos.plugins
familyos.runtime
familyos.sdk
familyos.specifications
```

Reservation does not mean that a corresponding implementation currently exists.

Future-reserved namespaces MUST NOT be used by third-party extensions.

Activation of a future-reserved namespace requires an approved FamilyOS contract.

---

# Reserved Package Identity Forms

The following ownership forms are reserved for official FamilyOS packages according to context:

```text
familyos-
familyos_
```

Examples:

```text
familyos-security-plugin
familyos_health_plugin
```

Third-party packages MUST NOT use these forms in a manner that implies official FamilyOS ownership.

A package name does not automatically define the canonical Plugin Identifier.

---

# Reserved Configuration Roots

The following configuration key roots are reserved:

```text
familyos
platform
runtime
plugins
generation
domains
security
```

Their use in official schemas MUST follow an approved platform contract.

Third-party configuration SHOULD use vendor-controlled namespaces where appropriate.

Example:

```yaml
plugins:
  acme.backup:
    destination: /archive
```

---

# Reserved CLI Options

The following options are reserved for conventional CLI behavior:

```text
--help
-h
--version
-v
--verbose
--quiet
-q
```

A command MUST NOT assign incompatible meaning to a reserved conventional option.

Where `-v` means `--version`, it MUST NOT simultaneously mean `--verbose` in the same command context.

---

# Contextually Restricted Words

The following terms are not absolutely prohibited but require precise justification:

```text
Base
Common
Core
Data
Default
Engine
Generic
Global
Handler
Helper
Legacy
Manager
Misc
New
Object
Official
Platform
Processor
Shared
Standard
System
Temporary
Utility
```

A restricted word MAY be used only when it communicates a precise and reviewable responsibility.

---

## Base

`Base` MAY identify an established reusable abstraction when no more precise contract name exists.

Acceptable:

```text
BaseCommand
```

Avoid:

```text
BaseService
BaseObject
BaseManager
```

---

## Common

`Common` SHOULD NOT be used as a container for unrelated reusable functionality.

A shared contract SHOULD instead receive a precise architectural name.

---

## Core

`Core` is reserved for foundational platform responsibilities.

It MUST NOT be used merely to indicate importance.

Acceptable:

```text
familyos-core
```

when referring to the governed FamilyOS core package or platform concept.

Avoid:

```text
SecurityCoreHelper
PluginCoreManager
```

without a specific architectural contract.

---

## Data

`Data` SHOULD NOT be used where the actual semantic concept is known.

Prefer:

```text
PluginMetadata
GenerationRequest
DocumentRecord
```

over:

```text
PluginData
GenerationData
GenericData
```

---

## Default

`Default` MAY identify a canonical built-in implementation of a documented abstraction.

Acceptable:

```text
DefaultRecipeRegistry
DefaultGenerationStrategyRegistry
```

A default implementation MUST correspond to a defined abstraction or selection contract.

---

## Engine

`Engine` MAY identify a component executing a complete technical processing mechanism.

Acceptable:

```text
GenerationEngine
```

Avoid:

```text
PluginEngine
SecurityEngine
```

unless the complete execution responsibility is explicitly defined.

---

## Generic

`Generic` SHOULD NOT be used as a substitute for an undefined abstraction.

A production component named `Generic*` requires explicit justification.

---

## Global

`Global` MAY be used only when the scope is genuinely platform-global and explicitly governed.

It MUST NOT be used merely to indicate shared access.

---

## Handler

`Handler` MAY identify a component responsible for one clearly defined event, command, protocol operation, or error category.

Acceptable:

```text
ErrorHandler
```

Avoid:

```text
PluginHandler
DataHandler
RequestHandler
```

when a more precise architectural term exists.

---

## Legacy

`Legacy` MAY identify a compatibility component for a documented previous contract.

Acceptable:

```text
LegacyManifestAdapter
LegacyPluginIdentifierAlias
```

A component MUST NOT be named `Legacy` solely because it is old.

---

## Manager

`Manager` SHOULD NOT be used when a precise architectural role exists.

Prefer:

```text
PluginRegistry
PluginInstaller
PluginResolver
RuntimeLifecycleManager
```

`Manager` MAY remain where a component genuinely coordinates multiple lifecycle responsibilities and no narrower established term is accurate.

---

## Official

`Official` is reserved for components governed and maintained by the FamilyOS project.

Third-party components MUST NOT use `Official` in:

* names;
* descriptions;
* identifiers;
* package metadata;

when doing so could imply FamilyOS endorsement or ownership.

---

## Platform

`Platform` is reserved for the complete FamilyOS platform or an explicitly governed platform-level contract.

A plugin MUST NOT include `Platform` in its name merely to appear foundational.

---

## Processor

`Processor` SHOULD NOT be used when a more precise operation exists.

Prefer:

```text
Resolver
Validator
Renderer
Formatter
Mapper
Pipeline
```

---

## Shared

`Shared` MAY identify a deliberately governed shared contract.

It MUST NOT become a container for unrelated reusable code.

Avoid:

```text
shared/utils.py
shared/helpers.py
```

---

## Standard

`Standard` MAY be used only when a governed standard or canonical behavior is clearly defined.

It MUST NOT be used merely to imply superiority or default status.

---

## System

`System` SHOULD be used only for system-level responsibilities.

A local component SHOULD NOT use `System` simply to imply importance.

---

## Temporary

`Temporary` MAY describe genuinely short-lived runtime resources.

Acceptable:

```text
TemporaryDirectory
temporary_path
```

It MUST NOT normally appear in committed production component identity.

---

## Utility and Helper

`Utility`, `Utilities`, `Helper`, and `Helpers` SHOULD NOT be used for production architectural components.

Their use commonly hides an undefined responsibility.

Preferred:

```text
PluginResolver
SpecificationLoader
GenerationPipeline
TemplateRenderer
CapabilityRegistry
PluginVerifier
```

Avoid:

```text
Utility
Utilities
Helper
Helpers
PluginHelper
GeneralUtility
MiscUtilities
CommonHelper
```

An exception MAY exist for a precisely documented compatibility layer or unavoidable external-library terminology.

---

# Prohibited Production Identifiers

The following identifiers MUST NOT be used as production component names:

```text
Thing
Stuff
Miscellaneous
Unknown
Whatever
Example
ExampleClass
TestClass
MyClass
MyObject
Foo
Bar
Baz
Tmp
Temp2
Final2
NewVersion
OldVersion
Copy
BackupCopy
Untitled
```

These terms MAY appear in isolated examples when clearly identified as placeholders.

Official reference documents MUST NOT contain unresolved placeholder identifiers.

---

# Version Words

The following terms MUST NOT be used to represent ordinary version history in production file or component names:

```text
old
new
latest
final
final2
v2
copy
backup
deprecated-copy
```

Version history MUST instead be represented through:

* version control;
* release tags;
* package versions;
* explicit migration documents;
* compatibility metadata;
* deprecation metadata.

An approved public compatibility boundary MAY contain a version designation.

Examples:

```text
Plugin SDK v2
ManifestVersion2
ApiV2Adapter
```

Such use requires an explicit compatibility contract.

Canonical Plugin and Capability Identifiers MUST NOT embed versions.

---

# Language-Reserved Words

Implementation languages and data formats define their own reserved words.

FamilyOS implementation identifiers MUST comply with those restrictions.

---

## Python Reserved Words

Python keywords MUST NOT be used as Python identifiers.

The authoritative keyword list is defined by the supported Python runtime.

Common examples include:

```text
False
None
True
and
as
assert
async
await
break
class
continue
def
del
elif
else
except
finally
for
from
global
if
import
in
is
lambda
nonlocal
not
or
pass
raise
return
try
while
with
yield
```

Soft keywords MUST also be respected where Python assigns them special meaning.

---

## Python Built-In Names

Python built-in names SHOULD NOT be shadowed when a precise alternative exists.

Examples include:

```text
bool
bytes
dict
filter
format
id
input
int
list
map
max
min
object
open
property
range
set
str
sum
super
tuple
type
zip
```

Preferred alternatives include:

```text
plugin_id
items_by_name
output_format
artifact_type
result_list
```

An existing public contract such as:

```text
PluginDescriptor.id
```

MAY remain when compatibility requirements outweigh local naming preference.

---

# Namespace Ownership

A namespace represents controlled ecosystem identity.

A namespaced identifier MUST NOT be used without ownership or authorization.

The namespace:

```text
familyos
```

belongs to the FamilyOS project.

Third-party publishers SHOULD use namespaces they control.

Examples:

```text
acme
example
vendor
```

resulting in identifiers such as:

```text
acme.backup
example.health.import
vendor.documents.archive
```

---

# Ownership and Authorization

A reserved identifier MAY be assigned only through an approved FamilyOS governance process.

Authorization MAY be granted through:

* an approved Architecture Decision Record;
* an approved Request for Comments;
* an approved specification;
* an official plugin designation;
* an explicit platform governance decision.

Informal usage, repository availability, historical experimentation, or implementation existence does not automatically establish ownership.

---

# Canonical Identity and Aliases

FamilyOS distinguishes:

```text
Canonical Identifier
Alias
Legacy Identifier
Display Name
Package Name
```

These concepts MUST NOT be conflated.

An alias MAY provide compatibility lookup for a canonical identity.

An alias MUST NOT create an independent identity.

For example:

```text
Legacy:
education

Canonical:
familyos.education
```

MAY eventually coexist during an approved migration.

The canonical identity remains:

```text
familyos.education
```

---

# Identifier Reassignment

A reserved, deprecated, retired, or legacy public identifier MUST NOT be reassigned to an unrelated entity.

This requirement protects:

* historical traceability;
* dependency resolution;
* persisted configuration;
* generated artifacts;
* ecosystem compatibility.

---

# Conflict Handling

When a proposed identifier conflicts with this document:

1. the conflict MUST be identified during review;
2. the proposed identifier MUST be changed unless an exception is approved;
3. namespace ownership MUST be evaluated;
4. public compatibility impact MUST be evaluated;
5. related documentation MUST be updated;
6. the final decision MUST remain traceable.

A naming conflict MUST NOT be resolved by silently redefining a reserved term.

---

# Existing Conflicts

Existing identifiers predating current conventions SHOULD be classified as:

* compliant;
* legacy-compatible;
* contextually acceptable;
* deprecated;
* scheduled for migration;
* explicitly exempted.

A stable public identifier MUST NOT be renamed automatically.

Compatibility and migration requirements take precedence over stylistic consistency.

Known legacy Plugin Identifiers currently include:

```text
education
documents
communication
documentation
```

Their existence SHALL NOT establish the canonical convention for new official plugins.

---

# Exceptions

An exception to a reserved-word or namespace rule requires:

* a concrete technical or architectural justification;
* confirmation that no clearer alternative exists;
* ownership analysis;
* compatibility analysis;
* documentation of intended meaning;
* architectural approval.

Exceptions MUST remain narrow.

An exception for one component MUST NOT establish an ecosystem-wide convention.

---

# Review Checklist

Before approving a public identifier or reserved name, reviewers MUST verify that:

* its identifier category is understood;
* it does not use an official namespace without authorization;
* it does not falsely imply official FamilyOS status;
* it does not conflict with an official domain;
* it does not conflict with an official Plugin Identifier;
* it does not conflict with an official Capability Identifier;
* it does not redefine a contract-reserved term;
* it uses architectural suffixes correctly;
* it does not use prohibited generic terminology;
* it does not contain version information where prohibited;
* it respects third-party namespace ownership;
* it does not shadow a language keyword;
* it avoids unnecessary built-in shadowing;
* it is stable enough for its intended public scope;
* compatibility impact has been considered.

For official Plugin Identifiers, reviewers MUST additionally verify:

```text
familyos.<plugin-name>
```

For official plugin Capability Identifiers, reviewers MUST additionally verify:

```text
familyos.<plugin-name>.<capability>
```

---

# Compliance

An identifier or name complies with this reference when:

* its ownership is authorized;
* its identifier category is valid;
* its namespace is valid;
* its terms retain official meanings;
* its prefixes and suffixes match responsibility;
* it does not falsely imply ownership or endorsement;
* it respects language-level restrictions;
* it avoids prohibited naming patterns;
* it follows SPEC-0002 and SPEC-0008;
* plugin identity follows SPEC-0009 where applicable;
* capability identity follows SPEC-0010 where applicable.

New non-compliant identifiers MUST be corrected before becoming stable public contracts.

Existing public identifiers require compatibility analysis before modification.

---

# Migration Governance

Identifier migration SHALL be treated as compatibility-sensitive when the identifier is exposed through:

* plugin manifests;
* Plugin SDK contracts;
* registries;
* dependency declarations;
* CLI interfaces;
* configuration;
* generated artifacts;
* public APIs;
* documentation;
* persisted state.

Migration SHALL consider:

1. affected consumers;
2. dependencies;
3. lookup behavior;
4. aliasing;
5. deprecation;
6. tests;
7. generated artifacts;
8. documentation;
9. release notes;
10. retirement strategy.

Canonical naming alone does not authorize migration.

---

# Maintenance

This document is maintained as part of the FamilyOS platform reference.

New reserved terms SHOULD be introduced only when required to:

* protect a public contract;
* establish official namespace ownership;
* protect canonical plugin identity;
* protect capability ownership;
* prevent ecosystem ambiguity;
* establish architectural terminology;
* support future governed platform evolution.

Every new reservation SHOULD define:

* the reserved term or identifier;
* its category;
* intended meaning;
* ownership;
* permitted uses;
* prohibited uses;
* compatibility implications.

Reserved identifiers MUST NOT be introduced solely to prevent legitimate third-party innovation.

---

# Summary

FamilyOS reserved words protect platform identity, architectural terminology, namespace ownership, plugin identity, capability identity, and extension boundaries.

Governance identifiers remain distinct from ecosystem identifiers.

Examples of governance identity include:

```text
SPEC-0002
ADR-0007
RFC-0010
```

Official Plugin Identifiers use:

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

Official plugin Capability Identifiers use:

```text
familyos.<plugin-name>.<capability>
```

Examples:

```text
familyos.health.record
familyos.education.course
familyos.documents.archive
familyos.communication.messaging
```

Third-party resources MUST use namespaces they are authorized to control.

Legacy public identifiers MAY remain temporarily compatible but MUST NOT redefine canonical FamilyOS identity.

Official identifiers are controlled resources.

They must remain unambiguous, stable, correctly owned, non-reassignable, and compatibility-aware so that official components, third-party plugins, generated artifacts, documentation, and public APIs can coexist without naming conflicts or false claims of platform authority.
