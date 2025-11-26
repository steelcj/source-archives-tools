---
Title: "Planning the Maintainer Runtime: Tools, Manifests, and Core Behaviors for Sovereign Source Archives"
Description: "A structured plan for implementing the maintainer-focused runtime inside each archive, including the tools directory layout, init-script extensions, and the functional design of sat-refresh-path-metadata."
Author: "Christopher Steel"
Date: "2025-11-25"
Last_Modified_Date: "2025-11-25"
License: "CC BY-SA 4.0"
Version: "1.0.1"
Tags:
- "source-archives"
- "maintainers"
- "tool-capsules"
- "metadata"
- "architecture"
Keywords:
- "tools"
- "manifest"
- "metadata-refresh"
- "taxonomy"
- "archive-maintenance"
URL: "https://universalcake.com/tools/docs/archive-life-cycle/planning-the-maintainer-runtime-tools-manifests-core-behaviors"
Path: "tools/docs/archive-life-cycle/planning-the-maintainer-runtime-tools-manifests-core-behaviors.md"
Canonical: "https://universalcake.com/tools/docs/archive-life-cycle/planning-the-maintainer-runtime-tools-manifests-core-behaviors"
Sitemap: "true"
DC_Title: "Planning the Maintainer Runtime: Tools, Manifests, and Core Behaviors for Sovereign Source Archives"
DC_Creator: "Christopher Steel"
DC_Subject: "Design and planning for embedded maintainer tools within independent source archives"
DC_Description: "A detailed specification of the tools directory structure, manifest behavior, and metadata regeneration workflow required to support long-term archive autonomy."
DC_Language: "en"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
OG_Title: "Planning the Maintainer Runtime for Sovereign Source Archives"
OG_Description: "A practical guide to embedding maintainer tools, defining manifests, and shaping metadata repair workflows inside autonomous archives."
OG_URL: "https://universalcake.com/tools/docs/archive-life-cycle/planning-the-maintainer-runtime-tools-manifests-core-behaviors"
Schema:
"@context": "https://schema.org"
"@type": "TechArticle"
"name": "Planning the Maintainer Runtime for Sovereign Source Archives"
"description": "A detailed exploration of the minimum runtime environment needed inside sovereign archives, including embedded tools and metadata repair mechanisms."
"author": "Christopher Steel"
"contributor": "ChatGPT-5.1 (OpenAI)"
Video_Metadata: {}
---

# Planning the Maintainer Runtime: Tools, Manifests, and Core Behaviors for Sovereign Source Archives

This document formalizes the next steps in adopting the **maintainer-focused Sovereign Archive Toolkit (sat)** model for sovereign source archives. It describes the structure of the embedded `tools/` directory, the manifest that governs updates, the split between usage and development documentation, and the core functionality maintainers will depend on for long-term operation.

# The Maintainer Runtime Inside Each Archive

Each archive contains two major layers:

1. Content and configuration
   Markdown, images, taxonomy definitions, metadata schemas, and structure rules.

2. Maintainer runtime (`tools/` directory)
   A small embedded toolkit containing only the commands and plugins needed for day-to-day maintenance and integrity checks.

This runtime is designed for simplicity, autonomy, and permanence. It must remain usable indefinitely without dependence on any external repository or platform.

# Documentation Layout: Usage vs Development

In the main tools repository, documentation is split by audience:

- `tools/docs/usage/`
  Stable, maintainer-facing documentation. These documents describe how to operate archives using sat commands, how to reorganize content safely, and how to upgrade the embedded tools.

- `tools/docs/develop/`
  Developer-facing documents. Design drafts, architecture notes, experiments, roadmaps, and other evolving materials live here. This directory is not copied into archives.

When a new archive is created, the initializer copies the contents of `tools/docs/usage/` into the archive as:

```
<archive-root>/
tools/
docs/
usage/
maintainers-guide.md
metadata-refresh.md
taxonomy-application.md
upgrading-tools.md
troubleshooting.md
```

This ensures each archive carries its own stable, offline, maintainer documentation, while development materials remain in the tools repository.

# The Archive’s Tools Directory Structure

Every new archive will include the following internal structure:

```
<archive-root>/
tools/
docs/
usage/
maintainers-guide.md
metadata-refresh.md
taxonomy-application.md
upgrading-tools.md
troubleshooting.md

sat-refresh-path-metadata
sat-apply-taxonomy
sat-check-archive

plugins/
taxonomy/
para/
plugin.py
config/
metadata/
dublin-core/
plugin.py
config/
apa7-cap/
plugin.py
config/

lib/
__init__.py
io_utils.py
metadata_utils.py
```

Key characteristics:

- Includes only the plugins used by this archive.
- Provides a small standard library (`lib/`) used internally by runtime scripts.
- Contains no build or development tooling; it is purely a **maintenance runtime**.
- Ships with usage documentation under `tools/docs/usage/`, derived from the main `tools/docs/usage/` in the tools repository.

# Extending the Init Script

The archive initializer must now:

- Create the full `tools/` skeleton shown above.
- Copy `tools/docs/usage/` from the tools repository into `<archive-root>/tools/docs/usage/`.
- Install stub or initial runnable commands:
  - `sat-refresh-path-metadata`
  - `sat-apply-taxonomy`
  - `sat-check-archive`
- Populate `tools/plugins/` with only the plugins required by the new archive’s configuration.
- Generate `config/tools.yml` containing:
  - The origin repository of the tools
  - The exact commit or tag used at archive creation
  - The list of plugin IDs
  - The runtime version expected by the archive

This ensures every archive is born with a complete, minimal, fully operational runtime and matching usage documentation.

# Functional Specification: sat-refresh-path-metadata

This command is central to archive maintainers, enabling safe reorganization of the archive without breaking metadata.

## Purpose

To scan the archive’s content structure and regenerate all path-derived metadata:

- `Path`
- `URL`
- `Canonical`
- Any field computed from directory hierarchy or relative position

## Behavior

1. Read archive configuration from:
   - `config/structure.yml`
   - Optionally `config/metadata/*.yml` for field naming and rules

2. Walk all content directories under language roots.

3. For each Markdown file:
   - Compute the correct path from filesystem position.
   - Load YAML front matter.
   - Update only location-derived metadata.
   - Preserve all other metadata fields.

4. Support safe and transparent operation via:
   - `--dry-run` to show changes only
   - `--verbose` to show detailed comparisons
   - Optional `--backup` mode for writing backups before changes

## Typical Workflow

Maintainers reorganize content using ordinary file operations:

```
mv areas/well-being/en/old/* areas/well-being/en/new/
```

Then:

```
./tools/sat-refresh-path-metadata --dry-run
./tools/sat-refresh-path-metadata
```

The archive self-repairs its metadata in place.

# The Role of config/tools.yml (Manifest)

The manifest formalizes the provenance and versioning of the embedded maintainer tools.

It includes:

- The upstream source-archive-tools repository URL
- The exact commit or tag the tools were derived from
- The list of plugins included in this archive’s runtime
- Runtime metadata, such as the tools directory path and version expectations

This file is rarely needed during routine maintenance but becomes essential for:

- Updating the archive to newer tools
- Reconstructing tool provenance
- Debugging and cross-archive consistency

# Summary

This iteration establishes a clear structure for the embedded maintainer runtime, defines the behavior of the most core maintenance tool, and integrates the manifest and documentation layout into the lifecycle of archive creation and maintenance. Together, these pieces ensure that:

- Archives remain sovereign and self-sufficient.
- Maintainers have predictable, built-in tools and usage documentation.
- Metadata and structure can always be repaired or updated.
- Upgrades are possible but controlled and explicit.

# License

This document, *Planning the Maintainer Runtime: Tools, Manifests, and Core Behaviors for Sovereign Source Archives*, by **Christopher Steel**, with AI assistance from **ChatGPT-5.1 (OpenAI)**, is licensed under the [Creative Commons Attribution-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/).

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)
