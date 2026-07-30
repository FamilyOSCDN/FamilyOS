# RFC-000Z — Plugin Discovery & Distribution

# 13 — Dependency Resolution

This document defines plugin dependency management.

Plugins may depend on:

- other plugins;
- specific versions;
- compatible FamilyOS SDK versions.

The resolver must support:

- dependency declaration;
- version constraints;
- conflict detection;
- deterministic resolution.

The result of resolution is a dependency graph ready for installation.
