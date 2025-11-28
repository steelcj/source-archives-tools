# sat-build-config

```yaml
slug: sat-build-config
location: tools/builders/sat-build-config/docs/sat-build-config.md
```

## Description

`sat-build-config` assembles the final configuration for a SAT archive.
It loads default fragments from SAT core plugins, merges optional plugin fragments, applies archive-level overrides, and processes CLI flags. The result is a fully-expanded configuration file that `sat-init-archive` can use to create the archive on disk.

`sat-build-config` does **not** create directories or files inside the target archive.
It only creates the configuration that *describes* the archive.

## Purpose

The purpose of `sat-build-config` is to perform all of the “thinking” required to assemble a valid SAT configuration:

- discover plugins
- load their default fragments
- merge fragments in a well-defined order
- apply archive-level overrides
- apply CLI overrides
- expand templates
- validate the result

The output is a single YAML document representing everything `sat-init-archive` needs.

This separation allows:

- reproducible builds
- safe testing
- debugging configuration without touching the filesystem
- predictable behavior
- clean plugin composition

## Responsibilities

`sat-build-config`:

- loads all plugins (core first, then optional)
- reads `etc/defaults.yml` from each plugin
- extracts:
- `config_fragments`
- `language_fragments`
- `taxonomy_fragments`
- merges all fragments
- applies archive-level config overrides
- applies CLI overrides
- expands template fields
- validates the final configuration
- writes the complete `archive-config.yml` to stdout (or a file if requested)

## Non-Responsibilities

`sat-build-config` NEVER:

- creates an archive root directory
- installs plugins
- creates PARA roots
- writes `config/*.yml` inside an archive
- executes plugin entrypoints
- touches the filesystem outside of writing the assembled config

All of these belong to `sat-init-archive`.

## Plugin Loading

Plugins are loaded in deterministic order:

1. **SAT Core Plugins (required)**
 - `core.schema`
 - `core.archive-identity`

 These always load first and supply baseline defaults.

2. **Add-on Plugins (optional)**
 - metadata plugins
 - language plugins
 - taxonomy plugins

To add entries into the config file that is build a plugin must contain:

```bash
plugin.yml
etc/defaults.yml
```

`sat-build-config` only reads default fragments.
It does not run executable code.

## Plugin file requirements and soft failures

`sat-build-config` expects each plugin to contain at least:

```text
plugin.yml
etc/defaults.yml
```

These files serve different purposes:

- `plugin.yml`  
  Defines the plugin ID, version, description, and paths (including where to find defaults).

- `etc/defaults.yml`  
  Provides configuration fragments (such as `config_fragments`, `language_fragments`, and `taxonomy_fragments`) that `sat-build-config` merges into the final configuration.

If either file is missing, `sat-build-config` does **not** abort. Instead, it:

1. Emits a clear message describing what is missing.
2. Skips loading defaults from that plugin.
3. Continues processing other plugins.

This keeps the tool usable in partially configured environments and during incremental development.

### Behavior when plugin.yml is missing

If a plugin directory is discovered but `plugin.yml` is missing:

- `sat-build-config` logs a message such as:

  ```text
  [sat-build-config] Skipping plugin at tools/plugins/example/ (missing plugin.yml)
  ```

- No defaults are loaded from that path.
- The plugin is ignored for this run.

### Behavior when etc/defaults.yml is missing

If `plugin.yml` exists but `etc/defaults.yml` is missing:

- `sat-build-config` logs a message such as:

  ```text
  [sat-build-config] Plugin core.example has no etc/defaults.yml; no config fragments will be loaded.
  ```

- The plugin is still considered “present”, but it contributes no defaults.
- This is useful for plugins that are purely runtime-oriented (for example, plugins used only by `sat-init-archive`) or plugins that have not yet defined default fragments.

### Summary

- Missing plugin files result in **warnings**, not hard errors.
- `sat-build-config` continues assembling the configuration using whatever valid fragments are available.
- This behavior supports:
  - gradual plugin development
  - testing in incomplete environments
  - resilience when one plugin is misconfigured

## Merge Precedence

Fragments are merged in this order:

1. **SAT Core Defaults**
2. **Optional Plugin Defaults**
3. **Archive-Level Configuration File**
4. **CLI Overrides (highest precedence)**

Protected fields (such as `schema_version`) cannot be overridden by add-on plugins.

## Template Expansion

After merging, `sat-build-config` expands template expressions such as:

```yaml
archive_root: "../{{ archive_identity.id }}"
```

Rules:

- expansion happens **after merging**
- expansions can reference any resolved value
- the expansion is evaluated as Jinja-style simple substitution
- paths are normalized after expansion

This allows plugin defaults to refer to fields that may be overridden later.

## Validation

`sat-build-config` performs schema validation using rules from the `core.schema` plugin:

- required keys must exist
- protected keys must not be modified by unauthorized plugins
- field types must match the schema
- template expansions must resolve cleanly
- fragments must conform to expected shapes

If validation fails, `sat-build-config` provides a clear error and exits without producing output.

## CLI Interface

Minimal CLI interface:

```
sat-build-config [options]
```

### Options

```
--archive-id <id>Override archive identity
--archive-label <label>Override archive label
--archive-description <desc> Override archive description
--archive-root <path>Override archive root

--plugin <id>Enable a plugin (repeatable)
--plugin-dir <path>Additional plugin search path

--config <file>Archive-level config input
--output <file>Write assembled config to file instead of stdout

--debugPrint merge steps
--versionPrint tool version
--help Show help
```

## Output File

By default:

- output is written to **stdout**

Users can redirect:

```
sat-build-config > archive-config.yml
```

Or specify explicitly:

```
sat-build-config --output archive-config.yml
```

The output is always a single YAML document representing the final SAT configuration.

## Example

```
sat-build-config \
--archive-id universalcake.com \
--plugin metadata.dublin-core \
--plugin language.en-ca \
--output archive-config.yml
```

Produces (simplified):

```yaml
schema_version: "1.0.0"

archive_identity:
id: "universalcake.com"
label: "SAT Test Archive"
description: "A SAT archive initialized with default testing configuration."
archive_root: "../universalcake.com"

languages:
- bcp_47_tag: "en-CA"
slug: "en-ca"
canonical: true
default_for_archive: true

plugins:
enabled:
- core.schema
- core.archive-identity
- metadata.dublin-core
- language.en-ca
```

This file is now ready for:

```
sat-init-archive --config archive-config.yml
```