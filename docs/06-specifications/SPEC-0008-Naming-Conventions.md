# SPEC-0008 — Naming Conventions

**Identifier:** SPEC-0008
**Title:** Naming Conventions
**Version:** 2.0.0
**Status:** Draft
**Owner:** FamilyOS Project
**Layer:** Specifications

---

# Abstract

This specification defines the normative naming conventions used throughout the FamilyOS platform.

It establishes consistent naming rules for:

* directories;
* files;
* documents;
* specifications;
* Architecture Decision Records;
* Requests for Comments;
* domains;
* plugins;
* capabilities;
* contributions;
* source code artifacts;
* command-line interfaces;
* generated resources;
* persistent platform resources.

Naming conventions define how FamilyOS concepts are represented consistently across documentation, source code, manifests, packages, runtime contracts, and ecosystem resources.

Identifier identity, uniqueness, permanence, namespace ownership, and identifier categories are governed by SPEC-0002 — Identifier.

This specification defines the naming representation associated with those identifiers and MUST NOT redefine identifier semantics independently from SPEC-0002.

---

# 1. Purpose

The purpose of this specification is to establish a uniform naming model across the FamilyOS platform.

Consistent naming enables:

* predictable resource identification;
* improved readability;
* automated validation;
* interoperability;
* architectural consistency;
* ecosystem namespace clarity;
* long-term stability;
* consistent generated artifacts;
* consistent developer experience.

Names are part of the FamilyOS platform contract.

Naming conventions SHALL therefore be treated as architectural rules rather than local implementation preferences.

---

# 2. Scope

This specification applies to persistent and public FamilyOS names, including but not limited to:

* directories;
* files;
* documentation;
* specifications;
* ADRs;
* RFCs;
* domains;
* plugins;
* capabilities;
* contributions;
* Python modules;
* Python packages;
* Python types;
* CLI commands;
* CLI options;
* templates;
* recipes;
* presets;
* generated artifacts;
* manifests;
* public extension points.

This specification defines naming syntax and representation.

It does not independently define:

* identifier uniqueness;
* identifier permanence;
* namespace ownership;
* identifier lifecycle;
* version semantics;
* metadata semantics.

Those responsibilities are governed by their respective specifications.

---

# 3. Normative References

This specification depends on:

* SPEC-0002 — Identifier;
* SPEC-0003 — Metadata;
* SPEC-0004 — Versioning;
* SPEC-0005 — Document Format;
* SPEC-0006 — Directory Layout;
* SPEC-0007 — File Format.

Plugin-related naming additionally relates to:

* SPEC-0009 — Plugin Manifest;
* SPEC-0010 — Plugin Capability Contract;
* ADR-0007 — Official Plugin Architecture.

Reference terminology is governed by:

* `docs/04-reference/Naming-Conventions.md`;
* `docs/04-reference/Reserved-Words.md`;
* `docs/04-reference/Glossary.md`;
* `docs/04-reference/Acronyms.md`.

Where this specification and a reference document conflict, the conflict SHALL be resolved through the FamilyOS documentation governance process.

---

# 4. Terms and Definitions

## Name

A human-readable or machine-readable designation assigned to a resource according to its naming context.

---

## Canonical Name

The authoritative name assigned to a concept within a defined naming context.

---

## Display Name

A human-readable name intended primarily for presentation.

Example:

```text
FamilyOS Security Plugin
```

---

## Identifier Representation

The textual representation of an identifier governed by SPEC-0002.

Example:

```text
familyos.security
```

This specification MAY define casing, separators, and segment naming for an identifier category but SHALL NOT redefine the identity semantics established by SPEC-0002.

---

## Namespace

The leading ownership segment of a namespaced ecosystem identifier.

Example:

```text
familyos
```

in:

```text
familyos.security
```

Namespace ownership is governed by SPEC-0002 and FamilyOS reserved-word rules.

---

## Resource Name

The name assigned to a persistent FamilyOS resource.

---

## Filename

The complete name of a file, including its extension.

---

## Directory Name

The name assigned to a directory.

---

## Package Name

A name used to identify a distributable or importable software package.

Package names SHALL NOT automatically be interpreted as canonical runtime identifiers.

---

# 5. Normative Language

The keywords MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY and OPTIONAL are interpreted as defined by the FamilyOS Specification Writing Guide.

---

# 6. General Naming Principles

## SPEC-0008-R1 — English Naming

Public FamilyOS names SHALL use English terminology unless an external standard requires another language.

---

## SPEC-0008-R2 — Semantic Precision

A name SHALL communicate the responsibility or concept it represents.

Names SHALL NOT intentionally obscure architectural responsibility.

Generic terms such as:

```text
Helper
Utility
Manager
Data
Object
Thing
Stuff
Misc
```

SHOULD NOT be used when a more precise architectural term exists.

Reserved and contextually restricted terms SHALL comply with:

```text
docs/04-reference/Reserved-Words.md
```

---

## SPEC-0008-R3 — Stable Public Names

Public names SHOULD remain stable.

A public name includes names exposed through:

* specifications;
* plugin manifests;
* Plugin SDK contracts;
* public Python APIs;
* CLI interfaces;
* generated artifacts;
* documented extension points;
* runtime registries.

Changing a public name SHALL require compatibility analysis when the change affects consumers.

---

## SPEC-0008-R4 — Consistent Terminology

The same architectural concept SHALL use the same canonical terminology across FamilyOS.

A new synonym SHALL NOT be introduced when an established term already exists.

---

## SPEC-0008-R5 — Identifier Separation

A display name, package name, module name, class name, directory name, and canonical identifier SHALL be treated as separate representations.

A component MUST NOT assume that changing one representation automatically changes another.

---

# 7. Case and Separator Conventions

## SPEC-0008-R6 — PascalCase

PascalCase SHALL be used for:

* Python class names;
* type names;
* domain names in prose where applicable;
* bounded context names;
* value object types;
* event types;
* command types;
* query types.

Examples:

```text
SecurityPlugin
PluginDescriptor
Family
Education
PluginActivated
CreatePerson
```

---

## SPEC-0008-R7 — snake_case

Lowercase snake_case SHALL be used for:

* Python module names;
* Python function names;
* Python method names;
* Python variable names;
* Python import package names.

Examples:

```text
plugin_descriptor
plugin_registry
familyos_security_plugin
activate_plugin
plugin_id
```

---

## SPEC-0008-R8 — kebab-case

Lowercase kebab-case SHALL be used where required for:

* Python distribution names;
* CLI commands where multiple words form one command token;
* selected persisted resource names;
* generated artifact identifiers where specified.

Examples:

```text
familyos-security-plugin
default-domain
domain-summary-documentation
```

---

## SPEC-0008-R9 — Dot-Separated Names

Lowercase dot-separated names SHALL be used for namespaced ecosystem identifiers and capability identifiers governed by SPEC-0002.

Examples:

```text
familyos.security
familyos.education
familyos.security.audit
familyos.education.course
```

Dot-separated identifier representations SHALL NOT contain whitespace.

---

# 8. Domain Naming

## SPEC-0008-R10 — Domain Display Names

Domain names SHALL use singular PascalCase in prose and type-oriented contexts.

Examples:

```text
Identity
Person
Family
Security
Health
Finance
Education
Documents
Communication
```

---

## SPEC-0008-R11 — Normalized Domain Names

Normalized domain names SHALL use lowercase naming.

Examples:

```text
identity
person
family
security
health
finance
education
documents
communication
```

A normalized domain name SHALL NOT automatically be interpreted as a Plugin Identifier.

Example:

```text
education
```

may represent the normalized Education domain, while:

```text
familyos.education
```

represents the official Education Plugin Identifier.

---

## SPEC-0008-R12 — Domain Types

The suffix `Domain` SHOULD be used only when referring to a technical domain abstraction or component.

Examples:

```text
DomainSpecification
SecurityDomainPlugin
```

The suffix SHALL NOT be added merely for stylistic consistency.

---

# 9. Plugin Naming

## SPEC-0008-R13 — Plugin Display Names

Official plugin display names SHALL use the corresponding plugin or domain concept followed by `Plugin`.

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

A product-facing display name MAY include `FamilyOS` when appropriate.

Examples:

```text
FamilyOS Security Plugin
FamilyOS Education Plugin
```

The display name SHALL remain distinct from the Plugin Identifier.

---

## SPEC-0008-R14 — Official Plugin Identifiers

Official Plugin Identifiers SHALL use the canonical ecosystem identifier representation defined by SPEC-0002:

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

Plugin Identifier segments SHALL use lowercase characters.

Plugin Identifiers SHALL NOT contain version information.

---

## SPEC-0008-R15 — Third-Party Plugin Identifiers

Third-party plugins SHALL use an authorized namespace they control.

Examples:

```text
acme.backup
example.health.import
vendor.documents.archive
```

Third-party plugins MUST NOT use the `familyos` namespace without explicit authorization.

---

## SPEC-0008-R16 — Plugin Distribution Names

Python distribution names for official plugins SHALL use lowercase kebab-case.

Recommended form:

```text
familyos-<plugin-name>-plugin
```

Examples:

```text
familyos-security-plugin
familyos-health-plugin
familyos-finance-plugin
familyos-education-plugin
```

Distribution names SHALL NOT be treated as Plugin Identifiers.

---

## SPEC-0008-R17 — Plugin Import Packages

Python import package names SHALL use lowercase snake_case.

Examples:

```text
familyos_security_plugin
familyos_health_plugin
familyos_finance_plugin
familyos_education_plugin
```

Import package names SHALL NOT define plugin identity.

---

## SPEC-0008-R18 — Plugin Classes

The primary plugin implementation class SHALL use PascalCase and SHOULD end with `Plugin`.

Examples:

```text
SecurityPlugin
HealthPlugin
EducationPlugin
DocumentsPlugin
CommunicationPlugin
DocumentationPlugin
```

Generic names such as:

```text
MainPlugin
FamilyOSPlugin
GenericPlugin
```

SHOULD NOT be used.

---

## SPEC-0008-R19 — Plugin Version Representation

Plugin versions SHALL remain separate from Plugin Identifiers.

Canonical:

```text
familyos.security
```

Version:

```text
1.0.0
```

Combined representational form MAY be used:

```text
familyos.security@1.0.0
```

The `@<version>` portion SHALL NOT become part of the canonical Plugin Identifier.

---

# 10. Capability Naming

## SPEC-0008-R20 — Capability Identifier Representation

Official plugin capability identifiers SHALL use lowercase dot-separated hierarchical names.

Canonical form:

```text
familyos.<plugin-name>.<capability>
```

Examples:

```text
familyos.security.audit
familyos.health.profile
familyos.health.record
familyos.finance.account
familyos.finance.transaction
familyos.education.learner
familyos.education.course
familyos.education.record
familyos.documents.document
familyos.documents.archive
familyos.communication.messaging
familyos.communication.archive
```

---

## SPEC-0008-R21 — Capability Semantic Naming

The final capability segment SHALL describe the ability or contract exposed by the capability.

Capability names SHALL NOT encode implementation class names unnecessarily.

Preferred:

```text
familyos.documents.archive
```

Avoid:

```text
familyos.documents.document_archive_capability
```

---

## SPEC-0008-R22 — Capability Namespace Consistency

A capability owned by a plugin SHOULD use the canonical Plugin Identifier as its identifier prefix.

Example:

```text
Plugin:
familyos.education

Capabilities:
familyos.education.learner
familyos.education.course
familyos.education.record
```

Exceptions require an explicitly governed platform-level capability contract.

---

# 11. Contribution Naming

## SPEC-0008-R23 — Contribution Types

Contribution type names SHALL describe the platform extension being contributed and SHOULD end with `Contribution`.

Examples:

```text
GenerationContribution
DomainGenerationContribution
GenerationRecipeContribution
TemplateContribution
```

---

## SPEC-0008-R24 — Contribution Identifiers

Externally referenced contribution identifiers SHALL use stable lowercase dot-separated names when governed as ecosystem identifiers.

Examples:

```text
familyos.generation.recipe
familyos.generation.template
familyos.domain.documentation
```

Contribution identity SHALL comply with SPEC-0002.

---

# 12. Python Naming

## SPEC-0008-R25 — Python Classes

Python classes SHALL use PascalCase.

Examples:

```text
PluginDescriptor
PluginRegistry
CapabilityRegistry
GenerationPipeline
```

---

## SPEC-0008-R26 — Python Functions and Methods

Python functions and methods SHALL use lowercase snake_case.

Examples:

```text
register_plugin
resolve_dependencies
load_manifest
activate_plugin
```

---

## SPEC-0008-R27 — Python Variables

Python variables SHALL use lowercase snake_case.

Examples:

```text
plugin_id
plugin_registry
capability_id
manifest_path
```

Names SHOULD describe the semantic value they contain.

For example, a variable containing a Plugin Identifier SHOULD prefer:

```text
plugin_id
```

over:

```text
name
```

---

## SPEC-0008-R28 — Identifier Value Objects

Identifier value object types SHOULD use the concept name followed by `Id`.

Examples:

```text
PersonId
FamilyId
PluginId
CapabilityId
```

The spelling `Id` SHALL be used in PascalCase Python identifiers.

`ID` SHOULD NOT be used inside PascalCase Python identifiers.

---

# 13. Command-Line Interface Naming

## SPEC-0008-R29 — CLI Commands

CLI command tokens SHALL use lowercase names.

Multi-word command tokens SHALL use lowercase kebab-case where applicable.

Examples:

```text
familyos init
familyos plugin resolve
familyos generation presets
```

Action commands SHOULD use verbs.

Examples:

```text
create
resolve
validate
install
activate
```

Nouns MAY identify command groups.

Examples:

```text
plugin
generation
domain
```

---

## SPEC-0008-R30 — CLI Options

Long CLI options SHALL:

* begin with `--`;
* use lowercase kebab-case.

Examples:

```text
--output-format
--include-diagnostics
--plugin-id
```

Short options MAY be used when unambiguous.

---

## SPEC-0008-R31 — CLI Arguments

Internal Python representations of positional CLI arguments SHALL use lowercase snake_case.

Examples:

```text
plugin_id
domain_name
artifact_type
```

---

# 14. Documentation Naming

## SPEC-0008-R32 — Architecture Decision Records

Architecture Decision Record files SHALL use:

```text
ADR-NNNN-Title-In-Pascal-Kebab-Case.md
```

Example:

```text
ADR-0007-Official-Plugin-Architecture.md
```

The identifier portion SHALL comply with SPEC-0002.

---

## SPEC-0008-R33 — Requests for Comments

Request for Comments files SHALL use:

```text
RFC-NNNN-Title-In-Pascal-Kebab-Case.md
```

Example:

```text
RFC-0010-Official-Security-Plugin.md
```

Temporary drafting identifiers MAY be used only when permitted by the RFC governance process.

---

## SPEC-0008-R34 — Specifications

Specification filenames SHOULD use:

```text
SPEC-NNNN-Descriptive-Title.md
```

Examples:

```text
SPEC-0002-Identifier.md
SPEC-0008-Naming-Conventions.md
SPEC-0009-Plugin-Manifest.md
```

The specification identifier SHALL remain independent from title changes.

---

## SPEC-0008-R35 — Reference Documents

Reference documents SHALL use stable descriptive names representing one authoritative responsibility.

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

# 15. Generation Framework Naming

## SPEC-0008-R36 — Artifact Names

Artifact names SHALL identify the generated deliverable.

Examples:

```text
domain-readme
aggregate-documentation
plugin-manifest
python-module
```

---

## SPEC-0008-R37 — Recipe Names

Recipe names SHOULD describe the complete generation outcome.

Examples:

```text
domain-summary-documentation
aggregate-documentation
domain-model-documentation
```

---

## SPEC-0008-R38 — Preset Names

Preset names SHALL use lowercase kebab-case when persisted or exposed through the CLI.

Examples:

```text
security
default-domain
complete-documentation
```

---

## SPEC-0008-R39 — Strategy Names

Python strategy types SHOULD use PascalCase and end with `Strategy`.

Examples:

```text
DomainDocumentationStrategy
AggregateDocumentationStrategy
```

Persisted strategy names SHOULD use lowercase kebab-case.

---

## SPEC-0008-R40 — Template Names

Template filenames SHALL identify their generated target and format.

Examples:

```text
domain-readme.md.j2
plugin-class.py.j2
plugin-manifest.yaml.j2
```

---

# 16. Test Naming

## SPEC-0008-R41 — Test Files

Python test files SHALL use:

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

## SPEC-0008-R42 — Test Functions

Test functions SHALL use lowercase snake_case.

They SHOULD describe observable behavior.

Recommended semantic form:

```text
test_<subject>_<expected_behavior>
```

Context MAY be added:

```text
test_<subject>_<behavior>_when_<condition>
```

---

## SPEC-0008-R43 — Test Classes

Test classes MAY group closely related behavior.

They SHALL use PascalCase and begin with `Test`.

Example:

```text
TestPluginRuntimeActivation
```

---

## SPEC-0008-R44 — Fixtures

Fixture names SHOULD describe the provided object or state.

Preferred:

```text
plugin_registry
active_runtime
valid_manifest
temporary_project
```

Avoid generic names such as:

```text
data
setup
fixture
```

---

# 17. Git Naming

## SPEC-0008-R45 — Branches

Branches SHALL use lowercase kebab-case after an approved category prefix.

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
```

---

## SPEC-0008-R46 — Commit Subjects

Commit subjects SHOULD:

* describe one coherent change;
* remain concise;
* use imperative wording;
* avoid unnecessary punctuation.

Examples:

```text
Add plugin capability registry
Document official plugin identifiers
Fix dependency cycle diagnostics
```

---

## SPEC-0008-R47 — Release Tags

Stable platform release tags SHALL follow the release and versioning conventions defined by FamilyOS release governance.

Canonical stable form:

```text
vMAJOR.MINOR.PATCH
```

Qualified release tags MAY use approved suffixes.

Examples:

```text
v4.0.0
v4.6.0-quality-framework
```

---

# 18. Reserved Names and Prefixes

## SPEC-0008-R48 — Reserved Prefixes

Reserved FamilyOS prefixes include:

```text
familyos
familyos_
familyos-
FamilyOS
ADR-
RFC-
SPEC-
```

Their permitted use depends on naming context.

Third-party resources MUST NOT use reserved FamilyOS ownership representations in a manner that implies official status.

---

## SPEC-0008-R49 — Reserved Domain and Plugin Names

Official domain and plugin names SHALL comply with:

```text
docs/04-reference/Reserved-Words.md
```

Reserved official domain names include:

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

Authorization rules SHALL apply to corresponding normalized and namespaced representations.

---

# 19. Public Naming Compatibility

## SPEC-0008-R50 — Public Rename

A stable public name SHALL NOT be changed casually.

A compatibility-sensitive rename SHALL require:

1. identification of affected consumers;
2. compatibility analysis;
3. migration strategy;
4. deprecation period where appropriate;
5. documentation updates;
6. test updates;
7. release-note entry;
8. architectural approval.

---

## SPEC-0008-R51 — Legacy Names

Existing names that predate this specification SHALL NOT be renamed automatically.

They SHOULD be classified as:

* compliant;
* legacy-compatible;
* deprecated;
* scheduled for migration;
* explicitly exempted.

Naming consistency SHALL NOT override compatibility requirements.

---

# 20. Validation

## SPEC-0008-R52 — Naming Validation

Public and persistent names SHOULD be validated at appropriate contract boundaries.

Validation MAY include:

* casing;
* separators;
* reserved words;
* namespace representation;
* suffix semantics;
* prohibited generic terms;
* identifier representation.

---

## SPEC-0008-R53 — Plugin Naming Validation

Plugin manifests SHOULD validate:

* Plugin Identifier representation;
* display-name representation;
* version separation;
* namespace representation.

Identifier identity and ownership validation SHALL comply with SPEC-0002.

---

## SPEC-0008-R54 — Capability Naming Validation

Capability registration SHOULD validate:

* lowercase representation;
* hierarchical dot-separated syntax;
* plugin-prefix consistency;
* capability semantic naming.

Identity and ownership validation SHALL comply with SPEC-0002.

---

# 21. Security Considerations

Names and identifier representations SHALL NOT disclose:

* credentials;
* authentication secrets;
* private cryptographic material;
* confidential personal information.

Names SHALL NOT falsely imply:

* official FamilyOS ownership;
* certification;
* endorsement;
* platform authority.

Third-party naming SHALL preserve namespace ownership boundaries.

---

# 22. Compatibility

New public FamilyOS resources MUST comply with this specification.

Existing resources SHOULD be aligned through normal maintenance when doing so does not violate compatibility guarantees.

Breaking changes to public naming rules SHALL require:

* compatibility analysis;
* migration planning;
* specification versioning;
* release documentation.

A naming-rule change SHALL NOT silently rename stable public identifiers.

---

# 23. Conformance

A component conforms to this specification when:

* its names follow the convention for their naming context;
* established FamilyOS terminology is used;
* casing and separators are correct;
* public identifiers use the representation defined by SPEC-0002;
* namespace representations respect ownership;
* package, class, display, and identifier names remain semantically distinct;
* prohibited or reserved naming patterns are respected;
* public compatibility requirements are preserved.

---

# 24. Naming Review Checklist

Before approving a public name, reviewers SHOULD verify that:

* the name uses official English terminology;
* the name communicates one clear responsibility;
* the correct casing convention is used;
* the correct separator convention is used;
* established architectural suffixes are used correctly;
* no existing concept is duplicated;
* no undocumented synonym is introduced;
* reserved words and prefixes are respected;
* namespace ownership is valid;
* display names and identifiers remain distinct;
* versions are not embedded into canonical identifiers;
* the name is suitable for long-term public use;
* compatibility impact has been evaluated.

---

# Annex A — Informative Examples

## A.1 Governance Identifier and Document

```text
Identifier:
SPEC-0008

Filename:
SPEC-0008-Naming-Conventions.md
```

---

## A.2 Official Plugin

```text
Display Name:
FamilyOS Education Plugin

Plugin Identifier:
familyos.education

Distribution:
familyos-education-plugin

Python import package:
familyos_education_plugin

Implementation class:
EducationPlugin
```

---

## A.3 Documents Plugin

```text
Display Name:
FamilyOS Documents Plugin

Normalized domain:
documents

Plugin Identifier:
familyos.documents

Capability:
familyos.documents.archive
```

---

## A.4 Documentation Plugin

```text
Display Name:
Documentation Plugin

Normalized plugin name:
documentation

Plugin Identifier:
familyos.documentation
```

The Documentation Plugin and Documents Plugin are distinct components.

---

## A.5 Capability

```text
Plugin:
familyos.education

Capability:
familyos.education.course
```

---

## A.6 Third-Party Plugin

```text
Display Name:
Acme Backup Plugin

Plugin Identifier:
acme.backup
```

---

## A.7 Architecture Decision Record

```text
Identifier:
ADR-0007

Filename:
ADR-0007-Official-Plugin-Architecture.md
```

---

## A.8 Request for Comments

```text
Identifier:
RFC-0010

Filename:
RFC-0010-Official-Security-Plugin.md
```

---

# 25. Normative References

* SPEC-0002 — Identifier;
* SPEC-0003 — Metadata;
* SPEC-0004 — Versioning;
* SPEC-0005 — Document Format;
* SPEC-0006 — Directory Layout;
* SPEC-0007 — File Format;
* SPEC-0009 — Plugin Manifest;
* SPEC-0010 — Plugin Capability Contract;
* ADR-0007 — Official Plugin Architecture;
* `docs/04-reference/Naming-Conventions.md`;
* `docs/04-reference/Reserved-Words.md`;
* FamilyOS Specification Writing Guide.

---

# 26. Revision History

| Version | Status   | Description                                                                                                                                                                                                                                                        |
| ------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1.0.0   | Approved | Initial publication of the Naming Conventions specification.                                                                                                                                                                                                       |
| 2.0.0   | Draft    | Aligns naming conventions with the categorized identifier model introduced by SPEC-0002 v2, formalizes official plugin and capability naming, separates display names, package names and identifiers, and establishes compatibility rules for legacy public names. |
