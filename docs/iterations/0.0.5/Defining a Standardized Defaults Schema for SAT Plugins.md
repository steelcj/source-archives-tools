# Defining a Standardized Defaults Schema for SAT Plugins

**Slug:** `standardized-plugin-defaults-schema`

This document outlines how SAT plugins will define and expose their default configuration values so that tooling such as `sat-init-archive` can automatically assemble, merge, and render archive configuration files. Standardizing the defaults schema ensures that all plugins behave predictably, can be composed safely, and integrate cleanly into archive initialization workflows.

## Purpose of a Standardized Defaults Schema

Every SAT plugin may contribute configuration fragments, metadata defaults, language definitions, structural behavior, or PARA-related settings. In order for tools to automatically initialize a new archive, plugin defaults must be:

- machine-readable  
- predictable in structure  
- namespaced to avoid collisions  
- mergeable with core SAT defaults  
- overridable by archive-level configuration  

A standardized schema solves these requirements by defining a stable contract for how plugin defaults are declared and consumed.

## Location of Defaults

Each SAT plugin must place its defaults file at:

```
etc/defaults.yml
```

inside the plugin’s directory.

For example:

```
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
defaults:
  config:
  languages:
  structure:
  para:
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