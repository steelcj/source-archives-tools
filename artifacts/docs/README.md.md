# README.md

## source-archive-tools: Tools Layout

This directory contains the **extensible tooling layer** for source-archive-based projects.

The layout is designed to be:

- **Plugin-based**: metadata, taxonomy, generators, importers, exporters.
- **Spec-aware**: each plugin separates upstream standards from local config.
- **Archive-agnostic**: tools operate on archives described by YAML config, not any specific static site generator.

## Top-Level Structure

- `core/`  
  Shared utilities and base classes. Example: `plugin_base.py` defining the `Plugin` interface.

- `cli/`  
  Thin command-line entrypoints (e.g., `sat-apply-taxonomy`). These read archive config, discover plugins, and call them.

- `plugins/`  
  Families of plugins such as `metadata/`, `taxonomy/`, `generators/`, `importers/`, `exporters/`.

## Plugin Layout Pattern

Each plugin follows the same structure:

```text
tools/plugins/<family>/<name>/
  standard/   # Upstream or conceptual definitions/specs
  config/     # How source-archive-tools uses those definitions
  plugin.py   # Executable adapter logic
  plugin.yml  # Plugin manifest (id, kind, entry point, dirs)