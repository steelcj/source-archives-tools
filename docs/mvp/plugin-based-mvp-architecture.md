---
Title: "Plugin-Based MVP Architecture for Source-Archive-Tools"
Description: "A complete, end-to-end guide defining the plugin-first MVP architecture for source-archive-tools, including directory structure, version reset, archival of legacy generator components, and a formal plugin contract for immediate implementation."
Author: "Christopher Steel"
Date: "2025-11-27"
Last_Modified_Date: "2025-11-27"
License: "CC BY-SA 4.0"
Version: "0.3.0"
Tags:
  - "source-archive-tools"
  - "plugins"
  - "architecture"
  - "mvp"
  - "versioning"
Keywords:
  - "source-archive"
  - "plugin-system"
  - "metadata"
  - "architecture"
  - "mvp"
URL: "https://universalcake.com/areas/tools/development/plugin-mvp/plugin-based-mvp-architecture"
Path: "areas/tools/development/plugin-mvp/plugin-based-mvp-architecture.md"
Canonical: "https://universalcake.com/areas/tools/development/plugin-mvp/plugin-based-mvp-architecture"
Sitemap: "true"
DC_Title: "Plugin-Based MVP Architecture for Source-Archive-Tools"
DC_Creator: "Christopher Steel"
DC_Subject: "Software architecture for plugin-driven document processing"
DC_Description: "A detailed specification defining the first plugin-driven MVP for source-archive-tools, including version reset, archival strategy, and future extensibility."
DC_Language: "en"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
OG_Title: "Plugin-Based MVP Architecture for Source-Archive-Tools"
OG_Description: "A complete, plugin-first architecture for source-archive-tools version 0.3.0."
OG_URL: "https://universalcake.com/areas/tools/development/plugin-mvp/plugin-based-mvp-architecture"
Schema:
  "@context": "https://schema.org"
  "@type": "TechArticle"
  "headline": "Plugin-Based MVP Architecture for Source-Archive-Tools"
  "author": "Christopher Steel"
  "inLanguage": "en"
  "license": "https://creativecommons.org/licenses/by-sa/4.0/"
  "contributor": "ChatGPT-5 (OpenAI)"
Video_Metadata: ""
---

# Plugin-Based MVP Architecture for Source-Archive-Tools

This document defines the complete A–Z plan for transitioning `source-archive-tools` into a **plugin-first architecture**, restarting the version line at **0.3.0**, and archiving all pre-MVP generator code into the `artifacts/` directory. It provides a clean slate and a future-aligned design that reflects how features will be added going forward.

This specification is intended to be implemented directly. Each section is actionable and describes precisely how to structure, operate, and extend the MVP.

## Purpose of This MVP

This MVP establishes:

- A minimal, functional plugin execution pipeline.
- A formal plugin directory structure.
- Three core plugins:
  - Dublin Core metadata injector.
  - APA7 reference-section enforcer.
  - CAP (Citation Anchor Pair) navigation injector.
- A clean separation between standards, configuration, and executable logic.
- A repeatable foundation for future tools, validators, generators, and format translators.
- A version reset that acknowledges a major architectural shift.

This is the first stable, pluggable foundation intended for long-term use.

# Version Reset and Archive Strategy

## Why Version 0.3.0?

The plugin-first model represents a foundational architectural shift. The existing generator code, experimental directories, and prototypes should not remain co-located with the new design.

Resetting to **0.3.0** establishes:

- A clear break from experimental prototypes.
- A new semantic versioning line.
- The beginning of stable, incremental growth.

## Moving Legacy Generator Code to `artifacts/`

All existing generator scripts, earlier radial-geometry prototypes, earlier metadata generators, and any transitional code should be placed in:

```
artifacts/
  generators/
  prototypes/
  research/
  legacy/
```

This ensures the primary `tools/` tree is reserved exclusively for:

- The plugin system
- The SAT runner
- Required configuration

This archival step removes ambiguity and provides clarity for future contributors.

# Clean-Slate Directory Structure for the Tools System

The new directory structure is:

```
tools/
  sat                      # core entrypoint (bash or python)
  config.yml               # global tool configuration (optional in MVP)
  plugins/
    dublin-core/
      standard/
      config/
      plugin.py
    apa7/
      standard/
      config/
      plugin.py
    cap/
      standard/
      config/
      plugin.py
artifacts/
  generators/
  research/
  legacy/
```

This structure ensures:

- All operative components live under `tools/`.
- All plugins are namespaced and discoverable.
- All prior work is preserved—but definitively out of the active execution path.

# Formal Plugin Contract (MVP)

Each plugin must implement a single script:

```
plugin.py
```

It must accept the following call signature:

```
python plugin.py apply --file path/to/file.md --config path/to/config.yml
```

### Required behaviors

- Operate **in place** on the target file.
- Exit with `0` on success.
- Perform transformations that are:
  - deterministic  
  - idempotent  
  - order-independent wherever possible  
  (but MVP sequencing is fixed)

### MVP Plugin Ordering

For the MVP, ordering is:

1. Dublin Core
2. APA7
3. CAP

This ordering is fixed inside `tools/sat` and can later be replaced by a declarative plugin-order registry.

# Core MVP Plugins

## Dublin Core Plugin (MVP)

Purpose:

- Ensure YAML metadata exists.
- Insert minimally required Dublin Core fields.
- Provide sane defaults when values are missing.
- Never remove user-provided metadata.

Directory:

```
tools/plugins/dublin-core/
  standard/       # DC 1.1 text, notes, specifications
  config/         # default.yml, extended-project.yml, etc.
  plugin.py
```

## APA7 Plugin (MVP)

Purpose:

- Ensure a reference section exists.
- Prepare scaffolding for later validation.
- Do not enforce formatting aggressively in MVP.
- Maintain compatibility with CAP plugin.

Directory:

```
tools/plugins/apa7/
  standard/
  config/
  plugin.py
```

## CAP Plugin (MVP)

Purpose:

- Add in-text citation anchors.
- Add reference-section anchors.
- Add bidirectional navigation (`[Return to citation]`).
- Prepare for multilanguage anchor strategies in the future.

Directory:

```
tools/plugins/cap/
  standard/
  config/
  plugin.py
```

# SAT Runner (tools/sat)

The SAT runner is the executable that orchestrates plugin execution.

### Responsibilities

- Accept a subcommand (`apply` in MVP).
- Accept a file path.
- Run each plugin in correct order.
- Pass plugin config path.
- Stop on errors.

### MVP Implementation (Simplified)

Pseudocode:

```
PLUGINS = ["dublin-core", "apa7", "cap"]

for plugin in PLUGINS:
    run tools/plugins/<plugin>/plugin.py apply \
        --file <target> \
        --config tools/plugins/<plugin>/config/default.yml
```

Future versions may introduce:

- Plugin discovery.
- Configurable ordering.
- Feature-gated plugin activation.
- Multistage processing (validate, normalize, enrich, export).

# A–Z Implementation Plan (MVP)

## A. Create version 0.3.0 branch or tag  
This marks the beginning of the plugin-first architecture.

## B. Move all non-MVP code into `artifacts/`  
Ensure `tools/` is clean.

## C. Create directory structure exactly as defined  
This guarantees forward compatibility.

## D. Implement empty plugin skeletons  
Establish the contract even before implementing logic.

## E. Write the MVP versions of each plugin  
Small, simple, predictable.

## F. Implement `tools/sat`  
Minimal shell or Python runner.

## G. Test using two or three sample Markdown files  
Verify idempotency.

## H. Document behavior and expected outputs  
Prepare for publication and future automation.

## I. Tag the release `v0.3.0`  
This becomes the first stable version of the plugin architecture.

## Z. Begin adding new plugins  
Examples:

- schema.org
- commonmark
- internal-defaults
- translation-sync
- figure extraction
- mermaid validation

This incremental path aligns directly with your long-term vision.

# Future Directions

This MVP provides the backbone for:

- pluggable transformations  
- consistent document preparation  
- multi-standard compliance  
- metadata expansion  
- language-aware transformations  
- cross-site generation  
- automated style enforcement  

The architecture now supports controlled growth without ever repeating the generator sprawl of earlier iterations.

# License

This document, *Plugin-Based MVP Architecture for Source-Archive-Tools*, by **Christopher Steel**, with AI assistance from **ChatGPT-5 (OpenAI)**, is licensed under the Creative Commons Attribution-ShareAlike 4.0 License.

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)
