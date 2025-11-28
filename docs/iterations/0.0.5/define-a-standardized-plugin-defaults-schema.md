# Defining a Standardized Defaults Schema for SAT Plugins

```yaml
title_slug: define-a-standardized-plugin-defaults-schema
location: docs/interations/0.0.5/define-a-standardized-plugin-defaults-schema.md
```

## Description

This document outlines how SAT plugins will define and expose their default configuration values so that tooling such as `sat-init-archive` can automatically assemble, merge, and render the archive skeleton.

files. Standardizing the defaults schema ensures that all plugins behave predictably, can be composed safely, and integrate cleanly into archive initialization workflows.

## Purpose of a Standardized Defaults Schema

Every SAT plugin may contribute configuration fragments, metadata defaults, language definitions, structural behavior, or taxonomy, such as PARA, related settings. In order for tools to automatically initialize a new archive, plugin defaults must be:

- machine-readable
- predictable in structure
- namespaced to avoid collisions
- mergeable with core SAT defaults
- overridable by archive-level configuration

A standardized schema solves these requirements by defining a stable contract for how plugin defaults are declared and consumed.

## Location of Defaults

Each SAT plugin must place its defaults file at:

```bash
etc/defaults.yml
```

inside the plugin’s directory.

For example:

```bash
tools/plugins/metadata/dublin-core/
plugin.yml
etc/defaults.yml
bin/
docs/
templates/
```

## Required Top-Level Keys

Each plugin’s `etc/defaults.yml` must include the following top-level keys:

```yaml
version: "0.1.0"
plugin:
  id: "metadata.dublin-core"
defaults:
  config_fragments: {}
  language_fragments: []
  taxonomy_fragments: {}
```

These keys are **plugin-scoped**. They do not directly mirror the final archive configuration (which will include top-level `config`, `languages`, `structure`, and `taxonomy` sections). Instead, they provide **fragments** that tools like `sat-init-archive` can consume and merge when building an archive skeleton.

Later, a separate document will define the schema for the **assembled defaults** used by `sat-init-archive`, where high-level keys such as `config`, `languages`, `structure`, and `taxonomy` will live. Those are *built from* plugin defaults, not defined inside the plugin itself.

### `version`

Indicates the version of this defaults schema for the plugin.

Example:

```yaml
version: "0.1.0"
```

### `plugin`

The `plugin` block identifies the plugin that these defaults belong to.

Example:

```yaml
plugin:
  id: "metadata.dublin-core"
```

This should match the `id` in `plugin.yml`.

### `defaults.config_fragments`

`config_fragments` contains configuration contributions that will eventually be merged into the archive’s generated `config/*` files (for example, `metadata.yml`). These fragments are namespaced under the plugin so they can be composed without collisions.

Example for a metadata plugin:

```yaml
defaults:
  config_fragments:
    metadata:
      defaults:
        Author: "Unknown"
        License: "CC BY-SA 4.0"
```

### `defaults.language_fragments`

`language_fragments` contains language- or locale-related contributions that a **language plugin** or similar plugin wants to expose. These fragments are not the final `languages:` array for the archive; instead, they are candidates that can be merged into the assembled defaults.

Example:

```yaml
defaults:
  language_fragments:
    - bcp_47_tag: "en-CA"
      slug: "en-ca"
      name: "English (Canada)"
      canonical: false
      default_for_archive: false
```

A dedicated language or locale plugin can provide these fragments. `sat-init-archive` (or another higher-level tool) decides which fragments are selected and promoted into the archive’s top-level `languages:` block.

### `defaults.taxonomy_fragments`

`taxonomy_fragments` contains contributions from taxonomy-oriented plugins (for example, PARA) about how they expect the archive to be structured, expressed in a plugin-scoped way. These fragments do not directly define archive-level `structure` or `taxonomy`; they provide inputs that later tools can interpret.

Example for a PARA taxonomy plugin:

```yaml
defaults:
  taxonomy_fragments:
    para:
      roots:
        - "projects"
        - "areas"
        - "resources"
        - "archives"
      vocabulary:
        project_root: "para_project_root"
        area_root: "para_area_root"
        resource_root: "para_resource_root"
        archive_root: "para_archive_root"
```

Again, the archive-level `structure` (for example, how PARA is actually laid out under each language root) is **calculated** by tools such as `sat-init-archive` using these fragments plus archive-level configuration. It is *not* defined directly inside the plugin defaults file.

### Summary of the layering

- **Plugin defaults (`etc/defaults.yml`)**  
  - Plugin-scoped  
  - Provide: `config_fragments`, `language_fragments`, `taxonomy_fragments`  
  - Never define global `config`, `languages`, `structure`, or `taxonomy` directly  

- **Assembled archive defaults (built by tools)**  
  - Tool-scoped (e.g., for `sat-init-archive`)  
  - Combine core SAT defaults + plugin fragments + archive overrides  
  - Produce:  
    - top-level `config` (e.g., `config/metadata.yml`)  
    - top-level `languages`  
    - computed `structure`  
    - selected `taxonomy` behavior  

This separation ensures plugins stay modular and composable, while archive-level structure and configuration are calculated by dedicated tooling rather than being baked into each plugin.


# OLD
## Required Top-Level Keys

Each plugin’s `etc/defaults.yml` must include the following top-level keys:

```yaml
version: "0.1.0"
defaults:
config:
languages: # < This is a plugin
structure: # < This must be calculated
taxonomy: # < This is a plugin
```

Each section is optional, but the keys must exist to ensure predictable merging.

### `version`

Indicates the version of this defaults schema for the plugin.
Example:

```yaml
version: "0.1.0"
```

### `defaults.config`

Configuration fragments that contribute to generated archive config files, such as:

- metadata defaults
- Dublin Core fields
- Open Graph fields
- Schema.org metadata

Example:

```yaml
defaults:
config:
metadata:
Author: "Unknown"
License: "CC BY-SA 4.0"
```

### `defaults.languages`

Language or locale fragments that the plugin adds or modifies.

Example:

```yaml
defaults:
languages:
- bcp_47_tag: "en-CA"
slug: "en-ca"
canonical: false
```

### `defaults.structure`

Structural expectations for how the archive should be laid out.

Example:

```yaml
defaults:
structure:
docs_root: "docs"
para_enabled: true
```

### `defaults.para`

PARA-related behavior or directory expectations.
This is especially useful for taxonomies or structural plugins.

Example:

```yaml
defaults:
para:
roots:
- "projects"
- "areas"
- "resources"
- "archives"
```

## Namespacing Rules

Plugin defaults **must not** inject top-level keys that conflict with core SAT configuration.
To avoid naming collisions:

- All plugin-provided config blocks must appear under `defaults.config.*`
- Plugins must not write directly to:
- `archive:`
- `structure.docs_root:` (except via `defaults.structure`)
- `languages:` (except via `defaults.languages`)
- PARA taxonomy contributions must only appear under `defaults.para.*`

This approach ensures plugins remain modular and safe to combine.

## How Tools Will Consume Plugin Defaults

Tools such as `sat-init-archive` will:

1. Load each plugin’s `etc/defaults.yml`
2. Validate that required keys exist
3. Merge defaults in the following order:
 - SAT core defaults (lowest precedence)
 - plugin defaults
 - archive-level config overrides
 - CLI flags (highest precedence)
4. Generate:
 - `config/archive.yml`
 - `config/languages.yml`
 - `config/metadata.yml`
5. Create directory structures based on combined defaults
6. Inject plugin behaviors or config fragments as appropriate

## Example Minimal `etc/defaults.yml`

```yaml
version: "0.1.0"

defaults:
config:
metadata:
Author: "Unknown"
License: "CC BY-SA 4.0"

languages: []

structure:
para_enabled: true

para:
roots:
- "projects"
- "areas"
- "resources"
- "archives"
```

## Summary

A standardized defaults schema provides a predictable, machine-composable contract for all SAT plugins. By defining consistent placement, namespacing, and merge rules, plugins can be combined without conflict and can automatically populate new SAT archives through tooling like `sat-init-archive`.

This standard becomes the foundation for fully automating archive creation while preserving the flexibility and modularity of the SAT plugin ecosystem.