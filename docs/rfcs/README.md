# FamilyOS RFCs

## Purpose

Request for Comments (RFC) documents describe significant architectural,
functional, or process changes before implementation.

The objective is to ensure that important decisions are discussed,
reviewed, documented, and understood before code is written.

FamilyOS follows an **Architecture First** approach.
RFCs ensure that important decisions are validated before implementation.

---

## When is an RFC Required?

An RFC is required when a change:

- introduces a new architectural component;
- modifies the public API;
- changes a generation workflow;
- affects multiple architectural layers;
- introduces a breaking change;
- significantly changes developer experience.

Minor bug fixes, documentation updates and refactorings that do not affect
the architecture do not require an RFC.

---

## Workflow

Every major change follows this lifecycle:

1. Draft
2. Review
3. Accepted
4. Implemented
5. Released

An RFC may also be:

- Rejected
- Superseded

---

## RFC Principles

- Architecture before implementation.
- Document decisions before writing code.
- Keep RFCs concise and actionable.
- One RFC should describe one architectural decision.
- Update RFC status as the project evolves.

---

## RFC Structure

Each RFC should contain at least:

- Summary
- Motivation
- Goals
- Non Goals
- Proposed Design
- Alternatives Considered
- Acceptance Criteria
- Future Work

The official layout is defined in `RFC-template.md`.

---

## RFC Naming

RFC documents follow this naming convention:


RFC numbers are unique and are never reused.

---

## Design Philosophy

RFCs are part of FamilyOS engineering culture.

They exist to improve communication, preserve architectural decisions,
and reduce unnecessary redesign.

Think.
Design.
Build.
Validate.
Document.
Repeat.

