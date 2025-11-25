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
```

Examples:

- `tools/plugins/metadata/dublin-core/`
- `tools/plugins/taxonomy/para/`
- `tools/plugins/generators/radial-wheel/`

### `standard/`

Holds upstream or conceptual “truth”:

- Dublin Core 1.1 fields and documentation
- PARA description and rationale
- Radial wheel layout schemas

### `config/`

Holds archive-tool-specific configuration:

- Field mappings from archive metadata into Dublin Core
- How PARA buckets map to directories under locale roots
- Default layout parameters for radial wheels

### plugin.py

Implements the `Plugin` interface defined in `core/plugin_base.py`. A plugin typically:

1. Reads archive configuration (e.g., `config/structure.yml`, `config/metadata/*.yml`).
2. Uses `standard/` definitions and `config/` mappings.
3. Applies transformations or creates directories under the archive root.

### plugin.yml

```yaml
id: "metadata.dublin-core"
version: "0.1.0"
kind: "metadata"
entry_point: "tools.plugins.metadata.dublin-core.plugin"
standard_dir: "standard"
config_dir: "config"
```

The loader can scan `tools/plugins/**/plugin.yml`, build a registry by `id`, and let archives opt in via their own config files.

## Relationship to Archives

Archives live elsewhere (e.g., `examples/`, `archives/`, or external paths). Each archive:

- Defines its language roots and taxonomy in `config/structure.yml`.
- May define extra metadata configuration in `config/metadata/*.yml`.
- Can choose which plugins to use.

The CLI tools in `tools/cli/` orchestrate everything:

- They read the archive’s `config/` files.
- They discover matching plugins in `tools/plugins/`.
- They call the appropriate `Plugin.apply()` methods with an execution context.