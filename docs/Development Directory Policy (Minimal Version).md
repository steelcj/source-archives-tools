# Development Directory Policy (Minimal Version)

All active source archive work must be placed under:

```
~/projets/archives/dev/
```

The development environment contains three elements:

1. `archive-x/` – Individual archives under development.
2. `tools/` – Shared tooling used to create, validate, and manage archives.
3. `configs/` – Optional shared configuration, templates, or rules that apply to all development archives.

This layout keeps development self-contained, easy to navigate, and clearly separate from any future stable or production environments. Archives placed in `dev/` are expected to change, break, or be reorganized without guarantees of stability.