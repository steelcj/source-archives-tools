# SAT — Source Archive Tools

## Description

**SAT (Source Archive Tools)** is a modular, path-oriented toolchain for creating, validating, and maintaining **portable, self-describing content archives**.

SAT is intentionally **archive-first** and **location-agnostic**.
It operates on explicitly provided archive paths and makes no assumptions about workspace layout, hosting environment, or publication target.

SAT is a **set of tools and related documents**.

## Core Goals

SAT is designed to support:

- Portable, **sovereign** archives that can move between systems
- Human-readable, auditable structures
- Explicit metadata and schema validation
- Long-term maintainability over short-term convenience
- Separation of tooling concerns from content concerns
- Export of content in multiple formats:
  - Markdown file
  - PDF
  - web-page
  - website
  - Word document
  - ...


SAT favors clarity, explicitness, and durability over hidden automation magic.

## Development Workspace Convention

**SAT (Source Archive Tools)** operates on **archive paths** and does **not assume** any specific workspace layout.

The `archives/` directory described below exists **solely for development convenience**.  
SAT archives are designed to be **portable**, **self-contained**, and **location-agnostic**.

This document describes a **recommended development convention**, not a requirement enforced by SAT.

```bash
~/projects/sat/dev/
├── sat/ # Clone of source-archive-tools (renamed to "sat")
└── archives/# Contains one or more development archives (portable)
```

This convention allows developers to:

- Work on SAT tools and (testing) archives side-by-side
- Test multiple archives against a single SAT codebase
- Move, publish, or version archives independently of the original Source Archive Tools sat directory.

SAT itself does not assumes this structure.

* Location of archives should be configurable using config option(s)

## SAT Repository Contents

The SAT repository contains the following:

```bash
sat/
├── config/      # Tool and schema configuration
├── docs/        # Project documentation
├── meta/        # Tools structural metadata, not birthed archives
│   └── archive.manifest.yml   ← authoritative Tool Archive manifest
├── plugins/     # Extensible SAT plugins (metadata, language, taxonomy, etc.)
├── tools/       # CLI tools (sat-init, sat-tree, sat-build-config, etc.)
├── README.md    # Project overview and conventions
└── VERSION      # Toolchain version
```

Archives (aside from SAT documentation!) live elsewhere.

---

## Design Principles

SAT tools are designed to:

- Accept archive paths explicitly
- Make no assumptions about directory layouts
- Treat archives as first-class, portable artifacts
- Keep tooling content and birthed archive concerns separate
- Remain inspectable and understandable by humans as well as machines

The goal is not to hide complexity, but to **make structure explicit and reliable**.

---

## Licensing Model

SAT is licensed under the **GNU General Public License, version 3 or later (GPL-3.0-or-later)**.

This licensing choice follows the model used by **Ansible Core** and other foundational infrastructure tools.

Key points:

- SAT may be used, studied, modified, and redistributed freely
- Modifications to SAT itself must remain open under the same license
- SAT may be used in commercial, academic, and personal contexts
- **Content archives created and/or managed using SAT are not covered by this license**, unless you explicitly apply it

The GPL applies **only** to the SAT toolchain and its plugins and documentation, not to the data, content, or archives processed by it.

The full license text is included in the `LICENSE` file.

---

## Copyright

Copyright (C) 2025 Christopher Steel

SAT (Source Archive Tools) is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

SAT is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

---

## Initial Setup

### Development example

Clone the repository:

```bash
mkdir -p ~/projects/sat/dev/
cd ~/projects/sat/dev/
git clone git@github.com:steelcj/source-archives-tools.git sat
cd sat
chmod +x tools/.
```

From here you can:

- Develop SAT tools within `sat/`
- Create or clone archives under `archives/`
- Invoke SAT tools against any archive path explicitly

No archive is required to live inside the SAT repository.

### Initialize new archives

[sat-init-archive_README.md](./bin/sat-init-archive_README.md)





- Validate archive structure with `sat-tree`
- Explore plugins under `plugins/`
- Review detailed documentation under `docs/`

Each tool is documented individually.

---

## Project Status

SAT is under active development.
Interfaces, schemas, and tools may evolve, but backward compatibility and archive stability are treated as first-order concerns.

---

## Contributing

Contribution guidelines will be documented in `CONTRIBUTING.md`.

In the meantime:
- Prefer clarity over cleverness
- Treat schemas and metadata as contracts
- Keep tools composable and explicit
- Avoid assumptions about user workflows

---

## Philosophy

SAT exists to make **archives resilient**.

Tools should be replaceable.
Archives should endure.
