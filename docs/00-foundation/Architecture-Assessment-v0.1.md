# FamilyOS Architecture Assessment v0.1

## Status

- Version: 0.1
- Status: Draft
- Audience: Architects, Contributors, Maintainers

---

# Purpose

This document summarizes the current architecture of FamilyOS.

It is the result of an architectural review performed before introducing
new RFCs and major refactorings.

Its objectives are:

- establish a shared understanding of the current architecture;
- identify architectural strengths;
- identify convergence opportunities;
- provide the foundation for future RFCs.

This document is descriptive.

It does not define implementation work.

---

# Architecture Overview

FamilyOS is organized as a layered architecture.

```text
CLI
    ↓
Application
    ↓
Domain
    ↓
Infrastructur
