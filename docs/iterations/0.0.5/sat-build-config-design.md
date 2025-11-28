# sat-build-config Design

```yaml
slug: sat-build-config-design
```

## Description

Assembles the archive configuration.

## How it works

`sat-build-config` is the first phase in creating a new SAT archive. It assembles all configuration fragments from SAT core plugins, optional plugins, archive-level overrides, and CLI flags into a single fully-expanded configuration file. This configuration becomes the canonical input for the second-phase tool, `sat-init-archive`.

`sat-build-config` **does not create directories**, does not write PARA structures, and does not install plugins. It only produces a complete configuration that describes what the archive *should be*.

## What it does

`sat-build-config` provides a clean, reproducible way to generate a configuration for a SAT archive.

It assembles configuration fragments from plugins in a defined order of preference, beginning with plugin defaults (which are especially helpful for testing).

Its output is a single configuration document that, at a minimum:

- **schema plugin**
- establishes and records a known schema version

- **core/archive-identity**
- defines the archive identity
- defines the archive’s root path

If available, it also merges:

- language fragments
- metadata fragments
- taxonomy fragments (e.g., PARA)

It does this by:

- discovering which plugins were loaded
- assembling their fragments
- merging those fragments into a final, usable configuration document

This output is then used directly by `sat-init-archive`.

The core idea is:

> **Separate “thinking” from “doing.”**
> `sat-build-config` thinks.
> `sat-init-archive` does.

## Inputs to sat-build-config

`sat-build-config` merges four input layers.

### SAT Core Plugins (Required)

- `core.schema`
- `core.archive-identity`

These plugins provide safe, testing-friendly defaults so that `sat-build-config` can always produce a usable configuration—even with no archive-level overrides.

### Add-on Plugins (Optional)

- metadata plugins
- language plugins
- taxonomy plugins (e.g., PARA)

### Summary

Each plugin contributes **fragments**, not full configuration blocks.
`sat-build-config` is responsible for assembling these fragments into a single final configuration.
