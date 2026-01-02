# SAT — Source Archive Tools

## Description

**SAT (Source Archive Tools)** is a modular, path-oriented toolchain for creating, validating, and maintaining **portable, self-describing source archives**.

SAT is **archive-first** and **location-agnostic** by design.
It operates on explicitly provided archive paths and makes no assumptions about workspace layout, hosting environment, or publication target.

SAT is a **set of tools and related documentation**.
It does not own, manage, or centralize content by default.

## Core Goals

SAT is designed to support:

- Portable, **sovereign** archives that can move between systems
- Human-readable, auditable directory structures
- Explicit metadata and schema validation
- Long-term maintainability over short-term convenience
- Clear separation between tooling concerns and content concerns
- Export of content to multiple formats (e.g. Markdown, PDF, web, Word)

SAT favors clarity, explicitness, and durability over hidden automation.

## How SAT Relates to Archives

SAT supports two explicit modes of operation.

### Detached (Independent) Archives (Default)

Archives are self-rooted and self-describing.
Archive identity is defined entirely by files within the archive itself.

In this mode:
- SAT does not retain archive identity, attachment, or location beyond the current invocation, except for optional operational logs.
- archive roots are resolved relative to the archive
- no host, user, or environment details are recorded

Archives remain portable, private, and free of attachment to SAT.

### Attached SAT-Managed Archives (Explicit)

In some cases, SAT may explicitly manage or coordinate archives.

In this mode:
- archives are deliberately attached to SAT
- SAT tracks archives using SAT-side metadata (for example in `satellites/`)
- SAT may retain host- or time-specific operational information

This mode is opt-in and SAT-side only:
- archives never reference SAT
- archive identity remains internal and unchanged
- detaching an archive does not invalidate it

---

## Development Workspace Convention (Optional)

SAT operates on **explicit archive paths** and does not require a particular workspace layout.

For development convenience, the following structure is recommended but not required:

```bash
~/projects/sat/dev/
├── sat/        # Clone of source-archive-tools (renamed to "sat")
└── archives/   # One or more development archives (portable)
```

This convention allows developers to work on SAT tools and test multiple archives side-by-side.
SAT itself does not assume or enforce this structure.

---

## Repository Contents

The SAT repository contains tooling and documentation only:

```bash
sat/
├── config/      # Tool and schema configuration
├── docs/        # SAT documentation archive
├── meta/        # Tool structural metadata
│   └── archive.manifest.yml
├── plugins/     # SAT plugins (metadata, language, taxonomy, etc.)
├── tools/       # CLI tools (sat-init, sat-tree, sat-build-config, etc.)
├── README.md
└── VERSION
```

Content archives live elsewhere.

---

## Licensing

SAT is licensed under the **GNU General Public License, version 3 or later (GPL-3.0-or-later)**.

The GPL applies to:
- SAT tools
- SAT plugins
- SAT documentation

It does **not** apply to:
- content archives created, validated, or managed using SAT
- archive contents, unless explicitly licensed as such

See `LICENSE` for full details.

---

## Initial Setup (Development)

Clone the repository:

```bash
mkdir -p ~/projects/sat/dev/
cd ~/projects/sat/dev/
git clone git@github.com:steelcj/source-archives-tools.git sat
cd sat
chmod +x tools/*
```

From here you can:
- develop SAT tools within `sat/`
- create or clone archives anywhere
- invoke SAT tools against any archive path explicitly

Each tool is documented individually.

---

## Project Status

SAT is under active development.
Interfaces and schemas may evolve, but **archive stability and backward compatibility are treated as first-order concerns**.

---

## Philosophy

SAT exists to make **archives resilient**.

Tools should be replaceable.  
Archives should endure.
