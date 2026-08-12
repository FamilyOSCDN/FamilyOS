# RFC-0003 — Plugin Discovery & Distribution

# 16 — CLI

This document defines the CLI interface for plugin management.

The CLI provides user-facing operations:

```bash
familyos plugin search
familyos plugin info <plugin>
familyos plugin install <plugin>
familyos plugin list
familyos plugin update
familyos plugin remove <plugin>
```

CLI responsibilities:

- receive user commands;
- validate input;
- invoke application services;
- display results.

The CLI must remain separated from plugin domain logic.
