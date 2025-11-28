# Creating the `core.schema` Plugin

```yaml
slug: creating-the-core-schema-plugin
```

## Overview

The `core.schema` plugin is the foundational SAT plugin responsible for defining the archive configuration schema version and enforcing minimal structural guarantees for all SAT archives.

It is intentionally simple in the MVP: it provides only a schema version and the structural contract that all SAT configuration documents must contain a `schema_version` field. Later iterations may add validation rules, required sections, field types, and compatibility rules.

The presence of this plugin ensures that:

- Every SAT archive configuration file has a known schema version
- Tools (`sat-build-config`, `sat-init-archive`, validators, future tooling) have a stable compatibility point
- Plugins can evolve safely while maintaining backward and forward compatibility

---

## Plugin Location

The plugin lives here:

```bash
tools/plugins/core/schema/
```

Create directory structure

```bash
mkdir -p plugins/core/schema/{docs,etc}
```

Confirmation:

```bash
tree plugins/core/schema/
```

output example:

```bash
plugins/core/schema/
├── docs
└── etc

3 directories, 0 files
```



## Purpose of the core.schema Plugin

This plugin provides:

- A **single authoritative scalar**: `schema_version`
- A **baseline minimal contract** for SAT configuration
- A predictable input for tools that need to ensure they are working with compatible configuration formats

The plugin does **not** validate the entire config or enforce a full schema.
It is not a JSON Schema or formal validator.
Its MVP purpose is to define:

```
schema_version: "1.0.0"
```

All tools merge this value as early as possible and treat it as a protected field.

---

## plugin.yml

`plugin.yml` identifies the plugin and declares its version.

```bash
nano plugins/core/schema/plugin.yml
```

content:

```yaml
# plugins/core/schema/plugin.yml
id: "core.schema"
name: "SAT Core Schema Plugin"
version: "0.1.0"

paths:
defaults: "./etc/defaults.yml"
```

Notes:

- The plugin ID **must** match what tools expect when loading the core plugin.
- `paths.defaults` is optional in the MVP, but recommended for long-term consistency.

---

## defaults.yml

This file contains configuration fragments contributed by the plugin.

```bash
nano plugins/core/schema/etc/defaults.yml
```


For the MVP, only the schema version is included.

```yaml
# tools/plugins/core/schema/etc/defaults.yml
version: "0.1.0"

plugin:
  id: "core.schema"

defaults:
  config_fragments:
    schema_version: "1.0.0"
```

Confirmation:

```bash
tree plugins/core/schema/
```

output:

```bash
plugins/core/schema/
├── docs
├── etc
│   └── defaults.yml
└── plugin.yml

3 directories, 2 files
```

```bash
docs/ # optional but recommended
```

### Rationale

- The schema version is stored inside `defaults.config_fragments`, so `sat-build-config` can merge it into the final configuration.
- The plugin’s `version` (0.1.0) is distinct from `schema_version` (“1.0.0”).
  - The former is the plugin file version.
  - The latter is the SAT archive config schema version.

---

## Responsibilities in the SAT Ecosystem

The `core.schema` plugin:

- Defines `schema_version`
- Provides the foundation for configuration compatibility
- Ensures the assembled config file is not missing the most fundamental structural field
- Gives SAT tooling a consistent versioning anchor point

It does **not**:

- Validate user-defined fields
- Validate plugin-specific fields
- Interpret or modify PARA trees
- Handle language configuration
- Manage archive identity

All of these belong to other plugins.

---

## How Tools Use This Plugin

### sat-build-config

`sat-build-config` loads `core.schema` first:

1. Finds the plugin directory
2. Reads `plugin.yml`
3. Reads `etc/defaults.yml`
4. Merges `config_fragments.schema_version` into the output config
5. Rejects the build if the plugin is missing

Because schema versioning is the strongest possible dependency, `core.schema` is considered **required**.

### sat-init-archive

`sat-init-archive` uses the resolved `schema_version` to:

- ensure it supports the configuration format
- choose implementation paths if multiple schema formats exist
- enforce minimal backward compatibility rules

(These behaviors will be defined in a future document.)

---

## Testing the Plugin

A minimal test sequence:

```bash
tools/sat-build-config
```

Produces:

```yaml
schema_version: "1.0.0"
archive_identity:
id: "unnamed-archive"
label: "SAT Test Archive"
description: "A SAT archive initialized with default testing configuration."
archive_root: "../unnamed-archive"
```

This confirms:

- Plugin loaded
- Defaults applied
- No merge conflicts
- Schema version visible at top-level

---

## Summary

The `core.schema` plugin represents the foundation of all SAT archives.
It is small, deterministic, and stable.
Its responsibilities will grow over time as SAT expands, but its minimal MVP behavior is deliberately limited to one essential purpose:

> Provide a schema version that all tools can depend on.