# FamilyOS CLI Roadmap

> **Status:** In Progress
> **Version:** 0.1.0
> **Last Updated:** July 2026

---

# Vision

FamilyOS CLI is the official command-line interface used to generate, manage and evolve FamilyOS projects.

The CLI must remain:

* Modular
* Testable
* Specification-driven
* Template-driven
* Domain-Driven Design compliant

---

# Current Architecture

```
familyos-cli
│
├── src/
│   └── familyos_cli/
│       ├── application/
│       ├── domain/
│       ├── infrastructure/
│       ├── interfaces/
│       └── shared/
│
├── templates/
├── specifications/
├── tests/
├── scripts/
└── docs/
```

---

# Completed Milestones

## Foundation

* [x] Python project initialized
* [x] Typer CLI configured
* [x] Ruff configured
* [x] Pytest configured
* [x] Package installation working

## CLI

* [x] `familyos version`
* [x] `familyos init`

## Infrastructure

* [x] ProjectGenerator
* [x] FileSystemService
* [x] TemplateRenderer
* [x] SpecificationLoader

## Templates

* [x] README template

## Specifications

* [x] project.yaml

---

# Current Sprint

## Domain Layer

* [ ] ProjectFile
* [ ] ProjectSpecification
* [ ] SpecificationLoader → ProjectSpecification

---

# Next Milestones

## Generation Engine

* [ ] Read project specification
* [ ] Create directories
* [ ] Generate files
* [ ] Render templates
* [ ] Copy static resources

---

## Testing

* [ ] Unit tests
* [ ] Integration tests
* [ ] Template tests
* [ ] CLI tests

---

## CLI

* [ ] familyos doctor
* [ ] familyos generate
* [ ] familyos validate
* [ ] familyos create
* [ ] familyos domain
* [ ] familyos core

---

## Quality

* [ ] 100% Ruff compliant
* [ ] Complete type hints
* [ ] Logging
* [ ] Error handling

---

# Technical Debt

* Review ProjectSpecification implementation
* Complete ProjectFile model
* Add domain validation
* Improve generator robustness

---

# Definition of Done

A feature is complete only if:

* Ruff passes
* Tests pass
* Documentation updated
* ROADMAP updated
* CLI validated
* Demo project generated successfully

---

# Daily Development Workflow

```
./scripts/doctor.sh

↓

Read ROADMAP.md

↓

Implement next feature

↓

ruff check .

↓

pytest

↓

Update ROADMAP.md

↓

Commit
```

---

# Long-Term Goal

Build a professional, specification-driven generation engine capable of generating complete FamilyOS applications from reusable specifications and templates.
