# Documentation Language

**Version:** 1.0
**Status:** Stable
**Last Updated:** August 2026

---

# Purpose

This document defines the official language rules used throughout the FamilyOS platform documentation.

Its objective is to ensure that every document is written consistently, remains understandable over time, and can be maintained by contributors regardless of their native language.

This document is normative.

---

# Scope

These rules apply to all official documentation, including:

- Foundation
- Product
- Architecture
- Engineering
- Reference
- Specifications
- Business
- Knowledge
- ADRs
- RFCs
- Plugin documentation
- Generated documentation

Unless explicitly stated otherwise, every document in the repository shall follow this specification.

---

# Official Language

The official language of FamilyOS documentation is **English**.

English is used for:

- architecture
- specifications
- RFCs
- ADRs
- code comments
- public APIs
- user documentation
- plugin documentation
- generated documentation

Internal discussions may occur in any language, but official documentation shall be written in English.

---

# English Variant

FamilyOS uses international technical English.

The objective is clarity rather than regional preference.

Documentation should avoid unnecessary regional spelling differences and prioritize terminology that is widely understood by the international software engineering community.

Consistency is more important than dialect.

---

# Writing Principles

Documentation shall be:

- clear
- concise
- precise
- factual
- implementation-independent whenever possible
- technically accurate

Writers should prefer simple sentences over complex constructions.

---

# Tone

Documentation uses a professional and neutral tone.

Avoid:

- marketing language
- emotional language
- subjective opinions
- humor
- unnecessary adjectives
- ambiguous expressions

Documentation describes facts rather than opinions.

---

# Voice

Active voice should be preferred.

Example:

> The Plugin Manager loads plugins.

Instead of:

> Plugins are loaded by the Plugin Manager.

Passive voice may be used when the actor is intentionally omitted.

---

# Terminology

The same concept shall always use the same term.

Do not introduce synonyms for established concepts.

Terminology defined in the Glossary is authoritative.

---

# Normative Keywords

The following keywords are interpreted according to RFC 2119.

- MUST
- MUST NOT
- SHALL
- SHALL NOT
- SHOULD
- SHOULD NOT
- MAY

These keywords shall be written in uppercase when used normatively.

---

# Headings

Use sentence-style headings.

Example:

```text
# Plugin lifecycle

## Runtime states

### Activation sequence
```
Avoid headings written entirely in uppercase.

---

# Lists

Bulleted lists should be used for unordered information.

Numbered lists should be used only when sequence is important.

Keep list items concise.

---

# Tables

Use tables when comparing structured information.

Avoid tables containing long paragraphs.

Each column should represent a single type of information.

---

# Code Formatting

All code shall use fenced code blocks.

Example:

```python
print("FamilyOS")
```

Specify the language whenever possible.

---

# File Names

Documentation file names shall follow the official naming conventions defined in:

`Naming-Conventions.md`

---

# Cross References

When referencing another document, use its repository-relative path.

Example:

`docs/02-architecture/README.md`

Avoid duplicated explanations when a reference already exists.

---

# Abbreviations

Do not introduce abbreviations unless they are defined in:

`Acronyms.md`

The first occurrence of an abbreviation should be expanded unless it is universally recognized.

---

# Definitions

New technical concepts shall be defined in:

`Glossary.md`

Documentation should reference those definitions instead of redefining them.

---

# Examples

Examples should:

- illustrate concepts
- remain minimal
- be technically correct
- avoid unnecessary complexity

Examples are informative and do not replace specifications.

---

# Consistency Rules

Documentation should maintain consistency in:

- terminology
- formatting
- capitalization
- punctuation
- document structure
- naming

Consistency takes precedence over stylistic preference.

---

# Capitalization

Use official capitalization for platform concepts.

Examples:

- FamilyOS
- Plugin Runtime
- Domain Generation Framework
- Plugin SDK
- Generation Pipeline

Avoid inconsistent capitalization of the same concept.

---

# Markdown

Documentation shall use standard Markdown.

Avoid platform-specific extensions unless officially adopted by the project.

Markdown should remain readable in plain text.

---

# Unicode

UTF-8 encoding shall be used for every documentation file.

Unicode characters may be used when they improve readability.

Avoid decorative symbols.

---

# Versioning

Reference documents evolve with platform releases.

Changes affecting terminology or language rules require architectural review before approval.

---

# Compliance

A document complies with this specification if it:

- is written in English
- follows the official terminology
- respects the naming conventions
- uses consistent formatting
- follows the normative language rules
- remains implementation-independent where appropriate

---

# Summary

Language consistency is essential for maintaining a long-lived software platform.

These rules establish a common writing standard that improves readability, reduces ambiguity, and ensures that all FamilyOS documentation communicates architectural intent with precision and consistency.
