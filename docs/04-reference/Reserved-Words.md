# FamilyOS reserved words

**Version:** 1.0
**Status:** Stable
**Last Updated:** August 2026

---

# Purpose

This document defines the words, identifiers, namespaces, prefixes, and naming patterns reserved by the FamilyOS platform.

Its purpose is to:

- protect official platform terminology
- prevent naming conflicts
- distinguish official components from third-party extensions
- preserve the stability of public contracts
- avoid ambiguous or misleading identifiers

This document is normative.

---

# Scope

These rules apply to:

- repositories
- source code
- Python packages
- Python modules
- public APIs
- command-line interfaces
- plugin identifiers
- plugin manifests
- capabilities
- contributions
- generation recipes
- generation presets
- generated artifacts
- specifications
- documentation
- Architecture Decision Records
- Requests for Comments
- release tags
- third-party extensions

Naming format rules are defined in:

`docs/04-reference/Naming-Conventions.md`

Terminology definitions are maintained in:

`docs/04-reference/Glossary.md`

---

# Normative language

The keywords **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** express normative requirements.

Their interpretation follows:

`docs/04-reference/Language.md`

---

# Reservation categories

FamilyOS distinguishes the following reservation categories:

| Category | Meaning |
|---|---|
| Platform-reserved | Exclusively controlled by the FamilyOS platform |
| Official-component-reserved | Reserved for components maintained by the FamilyOS project |
| Contract-reserved | Assigned a stable meaning in a public platform contract |
| Contextually restricted | Permitted only when used with a precise documented responsibility |
| Language-reserved | Reserved by an implementation language or data format |
| Future-reserved | Protected for anticipated platform evolution |

A reserved word MAY belong to more than one category.

---

# Platform identity

The following names are reserved for the official platform:

```text
FamilyOS
familyos
FAMILYOS
```

```

These names MUST NOT be used by third-party projects in a way that implies:

- official ownership
- official maintenance
- official certification
- platform endorsement
- inclusion in the FamilyOS distribution

Third-party projects MAY reference FamilyOS descriptively.

Examples of acceptable descriptive usage include:

```text
Plugin for FamilyOS
Compatible with FamilyOS
FamilyOS integration
```

Examples of prohibited identity claims include:

```text
Official FamilyOS Security
FamilyOS Core Extension
FamilyOS Certified Plugin
FamilyOS Platform Plugin
```

unless the component has received the corresponding official status.

---

# Reserved namespaces

## General namespace

The following namespace is reserved:

```text
familyos
```

It is reserved in:

- Python packages
- Python modules
- plugin identifiers
- capability identifiers
- contribution identifiers
- configuration keys
- environment variables
- command names
- generated artifact identifiers
- service identifiers

Third-party components MUST NOT create new identifiers directly under the `familyos` namespace.

---

## Python namespaces

The following Python namespace forms are reserved:

```text
familyos
familyos_cli
familyos_core
familyos_sdk
familyos_platform
familyos_plugins
familyos_official
```

Official repositories MAY define approved packages beneath these namespaces.

Third-party plugins MUST use their own package namespace.

Preferred third-party forms include:

```text
acme_familyos_plugin
example_familyos_security
vendor_familyos_integration
```

A third-party package MUST NOT use a name that can reasonably be mistaken for an official FamilyOS package.

---

## Plugin identifier namespace

Official plugin identifiers use:

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

The complete `familyos.*` plugin identifier namespace is reserved for official plugins.

Third-party plugins MUST use a namespace controlled by their author or organization.

Examples:

```text
acme.backup
example.calendar
org.example.documents
```

Third-party identifiers MUST NOT use:

```text
familyos.*
official.*
core.*
platform.*
```

unless explicitly authorized by the corresponding namespace owner.

---

## Capability namespace

Official capability identifiers use the `familyos` namespace.

Examples:

```text
familyos.security.audit
familyos.security.encryption
familyos.documents.classification
familyos.generation.recipes
familyos.runtime.lifecycle
```

Third-party capabilities MUST use a third-party-controlled namespace.

A capability identifier MUST NOT be designed to appear more authoritative than its actual ownership.

---

## Contribution namespace

Official contribution identifiers beginning with the following prefix are reserved:

```text
familyos.
```

Examples:

```text
familyos.generation.recipe
familyos.generation.template
familyos.domain.documentation
familyos.security.policy
```

Third-party contribution identifiers MUST use their own namespace.

---

# Reserved prefixes

The following prefixes are reserved for official FamilyOS artifacts:

```text
FamilyOS
familyos
familyos_
familyos-
familyos.
FAMILYOS_
ADR-
RFC-
```

Their lowercase, uppercase, snake_case, kebab-case, and dot-separated equivalents are protected when they could imply official ownership.

---

## Repository prefixes

The following repository name prefixes are reserved:

```text
familyos-
familyos_
```

Official examples include:

```text
familyos-cli
familyos-security-plugin
familyos-plugin-template
familyos-documentation
```

Third-party repositories SHOULD place their own organization or project name before the FamilyOS reference.

Preferred:

```text
acme-familyos-backup-plugin
example-familyos-integration
```

Avoid:

```text
familyos-backup-plugin
familyos-example-extension
```

---

## Environment variable prefixes

Official FamilyOS environment variables MUST use:

```text
FAMILYOS_
```

Examples:

```text
FAMILYOS_HOME
FAMILYOS_CONFIG
FAMILYOS_PLUGIN_PATH
FAMILYOS_LOG_LEVEL
```

Third-party plugins MUST use their own environment variable prefix.

Example:

```text
ACME_FAMILYOS_BACKUP_PATH
```

A third-party plugin MUST NOT introduce a new `FAMILYOS_*` variable without architectural approval.

---

## Command prefixes

The command name:

```text
familyos
```

is reserved for the official FamilyOS command-line interface.

Third-party executables MUST NOT use the same command name.

Acceptable third-party command names include:

```text
acme-familyos
familyos-acme-tool
example-familyos-plugin
```

Such commands MUST NOT misrepresent themselves as part of the official CLI.

# Reserved documentation identifiers

## Architecture Decision Records

The prefix:

```text
ADR-
```

is reserved for Architecture Decision Records governed by the FamilyOS ADR process.

An official ADR identifier MUST:

- contain four digits
- be unique
- remain stable
- never be reassigned
- refer to one architectural decision

Examples:

```text
ADR-0001
ADR-0007
ADR-0009
```

Draft documents MUST NOT reuse an identifier assigned to another decision.

Third-party plugin repositories MAY maintain their own ADRs, but they MUST NOT imply that those ADRs are platform-level FamilyOS decisions.

---

## Requests for Comments

The prefix:

```text
RFC-
```

is reserved for proposals governed by the FamilyOS RFC process.

An official RFC identifier MUST:

- contain four digits
- be unique
- remain stable
- never be reassigned
- refer to one governed proposal

Examples:

```text
RFC-0010
RFC-0011
RFC-0012
```

Temporary letter-based identifiers MAY exist during early drafting but MUST NOT be treated as permanent platform identifiers.

---

## Reference document names

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

Within `docs/04-reference/`, another document MUST NOT assume one of these responsibilities under a different name.

---

# Reserved platform component names

The following names identify established platform components and are contract-reserved:

```text
Application Layer
Artifact
Capability
Capability Provider
Capability Registry
Command
Command Context
Contribution
Contribution Provider
Contribution Registry
Dependency Graph
Diagnostic Pipeline
Domain
Domain Context
Domain Generation Framework
Domain Generation Pipeline
Domain Model
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

These terms MUST retain the meanings defined by the FamilyOS reference and architecture documentation.

A component MUST NOT reuse one of these names for an incompatible responsibility.

---

# Reserved architectural suffixes

The following suffixes have established meanings:

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

However, it is reserved for components that fulfill the corresponding architectural responsibility defined in:

`docs/04-reference/Naming-Conventions.md`

Examples of prohibited misuse include:

```text
PluginResolver
```

for a component that installs plugins, or:

```text
CapabilityRegistry
```

for a component that merely formats capability output.

---

# Reserved lifecycle terms

The following runtime lifecycle terms are reserved:

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

- an explicit contract
- transition rules
- compatibility analysis
- architectural approval

The following lifecycle operation names are also reserved for their established meanings:

```text
load
initialize
activate
stop
```

A lifecycle component MUST NOT use these verbs interchangeably.

---

# Reserved dependency-resolution terms

The following terms have separate, stable responsibilities:

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

They MUST NOT be treated as synonyms.

Their responsibilities are:

| Term | Reserved responsibility |
|---|---|
| discover | Locate available plugin packages or manifests |
| select | Choose candidates from an available set |
| resolve | Determine a valid outcome from dependencies and constraints |
| order | Produce a dependency-safe processing sequence |
| verify | Confirm integrity, compatibility, authenticity, or trust |
| install | Make a plugin package available to the platform |
| load | Read and instantiate a plugin component |
| activate | Make a loaded plugin operational |

A single component MAY coordinate several operations through a pipeline, but its name MUST NOT hide the distinction between them.

---

# Reserved generation terms

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

- a `Template` is not a `Recipe`
- a `Recipe` is not a `Preset`
- a `Preset` is not a `Strategy`
- a `Plan` is not a `Result`
- a `Definition` is not an instantiated `Artifact`
- a `Context` is not an unrestricted dependency container

---

# Reserved domain terms

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

These terms MUST NOT be used only as stylistic suffixes.

Examples of prohibited misuse include:

```text
PersonEntity
```

when `Person` is the accepted entity name, or:

```text
FamilyAggregateRoot
```

when `Family` is the accepted aggregate root name.

---

# Reserved official domain names

The following names are reserved for official FamilyOS domains and official plugins:

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

The corresponding normalized identifiers are also reserved:

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

A third-party plugin MAY integrate with one of these domains, but MUST NOT claim to be the official implementation of that domain.

Examples:

Preferred:

```text
acme.security.backup
example.health.import
vendor.documents.archive
```

Prohibited without official authorization:

```text
familyos.security
familyos.health
familyos.documents
```

---

# Reserved official plugin names

The following display names are reserved:

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
```

The reservation covers names that differ only by:

- capitalization
- punctuation
- spacing
- singular or plural form
- common package-name normalization

---

# Contextually restricted words

The following words are not absolutely forbidden, but their use is restricted:

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

`Base` MAY identify an established reusable abstraction when no more precise contract name is available.

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

## Core

`Core` is reserved for foundational platform responsibilities.

It MUST NOT be used merely to indicate importance.

Acceptable:

```text
familyos-core
```

when referring to the official platform core.

Avoid:

```text
SecurityCoreHelper
PluginCoreManager
```

---

## Default

`Default` MAY identify the canonical built-in implementation of an abstraction.

Acceptable:

```text
DefaultRecipeRegistry
DefaultGenerationStrategyRegistry
```

A default implementation MUST have a documented abstraction or selection contract.

---

## Engine

`Engine` MAY identify a component that executes a complete technical processing mechanism.

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

## Handler

`Handler` MAY be used for a component responsible for one clearly identified event, command, protocol operation, or error category.

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

when a more precise term exists.

---

## Legacy

`Legacy` MAY identify a compatibility component for a documented previous contract.

Acceptable:

```text
LegacyManifestAdapter
```

A component MUST NOT be named `Legacy` solely because it is old.

---

## Manager

`Manager` MUST NOT be used when a precise architectural role exists.

Prefer:

```text
PluginRegistry
PluginLifecycleManager
PluginInstaller
RuntimeLifecycleManager
```

The word MAY be retained when the component genuinely coordinates a lifecycle with multiple transitions and no narrower established term communicates that responsibility.

---

## Official

`Official` is reserved for components governed and maintained by the FamilyOS project.

Third-party components MUST NOT use `Official` in names, descriptions, package metadata, or identifiers in a way that implies endorsement.

---

## Platform

`Platform` is reserved for the complete FamilyOS platform or an explicitly defined platform-level contract.

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
---

## Temporary

`Temporary` MAY describe genuinely short-lived runtime resources.

Acceptable:

```text
TemporaryDirectory
temporary_path
```

It MUST NOT appear in the name of a committed production component.

---

## Utility and helper

`Utility`, `Utilities`, `Helper`, and `Helpers` SHOULD NOT be used for production architectural components.

Their use commonly hides an undefined responsibility.

Prefer a name that identifies the actual operation.

Examples:

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

An exception MAY be acceptable when the component represents a well-defined compatibility layer or wraps an external library whose terminology cannot reasonably be changed.

Even in such cases, the architectural responsibility MUST remain explicit.

---

# Prohibited identifiers

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

These names MAY appear in isolated documentation examples when clearly marked as placeholders, but MUST NOT appear in production contracts or committed implementation components.

Official reference documents MUST NOT contain unresolved placeholder identifiers.
---

# Version words

The following words MUST NOT be used to represent version history in production file or component names:

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

Version history MUST be managed through:

- version control
- release tags
- package versions
- migration documents
- explicit deprecation metadata

A version suffix MAY be used when it is part of an approved public contract.

Examples:

```text
Plugin SDK v2
ManifestVersion2
ApiV2Adapter
```

Such use requires a defined compatibility boundary.

---

# Language-reserved words

Implementation languages and data formats define their own reserved words.

FamilyOS identifiers MUST comply with those restrictions.

---

## Python reserved words

Python keywords MUST NOT be used as Python identifiers.

The authoritative keyword list is the list provided by the Python version supported by the platform.

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

Soft keywords defined by Python MUST also be considered in contexts where they have reserved meaning.

FamilyOS MUST NOT duplicate the complete Python language specification in this document.

---

## Python built-in names

Python built-in names SHOULD NOT be shadowed.

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

---

## CLI reserved options

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

A command MUST NOT assign an incompatible meaning to one of these options.

Where `-v` is used for `--version`, it MUST NOT simultaneously mean `--verbose` within the same command context.

---

## Configuration keys

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

Their use in official schemas MUST follow an approved specification.

Third-party configuration SHOULD be placed under a vendor-controlled namespace.

Example:

```yaml
plugins:
  acme.backup:
    destination: /archive
```


---

# Future-reserved namespaces

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

Reservation does not mean that the corresponding component currently exists.

Future-reserved namespaces MUST NOT be used by third-party extensions.

Their eventual activation requires an approved platform contract.

---

# Ownership and authorization

A reserved identifier MAY be assigned only through an approved FamilyOS governance process.

Authorization MAY be granted through:

- an approved Architecture Decision Record
- an approved Request for Comments
- an approved specification
- an official plugin designation
- an explicit platform governance decision

Informal usage, existing code, or repository availability does not automatically grant ownership of a reserved identifier.

---

# Conflict handling

When a proposed identifier conflicts with this document:

1. the conflict MUST be identified during review
2. the proposed identifier MUST be changed unless an exception is approved
3. public compatibility impact MUST be evaluated
4. related documentation MUST be updated
5. the final decision MUST be traceable

A naming conflict MUST NOT be resolved by silently redefining the reserved term.

---

# Existing conflicts

Existing identifiers that predate this specification SHOULD be classified as:

- compliant
- contextually acceptable
- deprecated
- scheduled for migration
- explicitly exempted

A stable public identifier MUST NOT be renamed automatically.

Compatibility and migration requirements take precedence over stylistic consistency.

---

---

# Exceptions

An exception to a reserved-word rule requires:

- a concrete technical or architectural justification
- confirmation that no clearer alternative exists
- compatibility analysis
- documentation of the intended meaning
- architectural approval

Exceptions MUST remain narrow.

An exception for one component does not establish a general naming convention.

---

# Review checklist

Before approving an identifier, reviewers MUST verify that:

- it does not use an official namespace without authorization
- it does not imply official status incorrectly
- it does not conflict with an official domain or plugin name
- it does not redefine a contract-reserved term
- it uses architectural suffixes correctly
- it does not shadow a Python keyword
- it avoids shadowing Python built-ins
- it does not use filename-based version history
- it does not introduce a prohibited generic name
- it respects third-party namespace ownership
- it remains stable enough for its intended visibility

---

# Compliance

An identifier complies with this specification when:

- its namespace is authorized
- its terms retain their official meanings
- its prefixes and suffixes match its responsibility
- it does not imply unauthorized ownership or endorsement
- it does not conflict with language-level restrictions
- it does not use prohibited naming patterns
- it follows the official naming conventions

Non-compliant identifiers MUST be corrected before becoming stable public contracts.

Existing public identifiers require compatibility analysis before modification.

---

# Maintenance

This document is maintained as part of the FamilyOS platform reference.

New reserved words SHOULD be introduced only when required to:

- protect a public contract
- establish an official namespace
- prevent ecosystem ambiguity
- support a new governed platform capability

Every addition MUST define:

- the reserved identifier
- its category
- its intended meaning
- its ownership
- its permitted uses
- its prohibited uses

Reserved identifiers MUST NOT be added solely to prevent legitimate third-party innovation.

---

# Summary

FamilyOS reserved words protect the identity, terminology, namespaces, contracts, and extension boundaries of the platform.

Official identifiers are controlled resources.

They must remain unambiguous, stable, and correctly owned so that official components, third-party plugins, generated artifacts, documentation, and public APIs can coexist without naming conflicts or false claims of platform authority.
