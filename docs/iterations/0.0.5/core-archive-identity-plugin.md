# core.archive-identity Plugin

```yaml
slug: core-archive-identity-plugin
location: tools/plugins/core/archive-identity/
```

## Description

Provides the default `archive_identity` block used by `sat-build-config`.  
This plugin ensures that every archive has a valid identity even when no archive-level configuration is supplied. It also provides a default `archive_root` path that can be used for testing or rapid prototyping.

This plugin is required and is always loaded before all other plugins.

## Purpose

The `core.archive-identity` plugin supplies baseline values for:

- `archive_identity.id`
- `archive_identity.label`
- `archive_identity.description`
- `archive_identity.archive_root`

These values are intended to be safe defaults suitable for testing.  
They are replaced when archive-level configuration or CLI overrides are supplied.

## Directory structure

```bash
mkdir -p plugins/core/archive-identity/{docs,etc}
```

confirm:

```bash
tree plugins/core/archive-identity/
```

## plugin.yml

```bash
nano plugins/core/archive-identity/plugin.yml
```

Content:

```yaml
id: "core.archive-identity"
name: "SAT Core Archive Identity Plugin"
version: "0.1.0"

description: "Provides default archive_identity configuration for SAT archives, including a testing-friendly archive_root."

paths:
  defaults: "./etc/defaults.yml"
  docs: "./docs"
```

This plugin does not define any executable entrypoints. It contributes only configuration fragments used during the `sat-build-config` phase.

## etc/defaults.yml

```bash
nano plugins/core/archive-identity/etc/defaults.yml
```

Content:

```yaml
version: "0.1.0"

plugin:
  id: "core.archive-identity"

defaults:
  config_fragments:
    archive_identity:
      id: "unnamed-archive"
      label: "SAT Test Archive"
      description: "A SAT archive initialized with default testing configuration."

      # Default archive root path.
      # Template expansion is performed by sat-build-config.
      archive_root: "../{{ archive_identity.id }}"
```

### confirm

```bash
tree plugins/core/archive-identity/
```

Output example:

```bash
tools/plugins/core/archive-identity/
  plugin.yml
  etc/
    defaults.yml
  docs/
    README.md    # optional reference documentation
```

### Notes

- `archive_root` uses a relative default so new test archives can be created without requiring a specific directory structure.
- `{{ archive_identity.id }}` is expanded by `sat-build-config` after all overrides are applied.
- Only this plugin (plus archive-level config and CLI) may set or modify `archive_identity.*`.
- If another plugin attempts to contribute to `archive_identity`, validation should fail.

## How it is used

`sat-build-config` loads this plugin before all others. Its fragments become the baseline identity for the archive. Archive-specific configuration, if present, overrides these defaults.

Example:

```bash
sat-build-config --archive-id universalcake.com
```

The resulting `archive_identity` section becomes:

```yaml
archive_identity:
  id: "universalcake.com"
  label: "SAT Test Archive"
  description: "A SAT archive initialized with default testing configuration."
  archive_root: "../universalcake.com"
```

Archive-level configuration may provide more meaningful labels or descriptions.