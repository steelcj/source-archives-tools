---
Title: "Self-Contained Plugins and Cascading Wisdom: Foundations for a Portable Tool Ecosystem"
Description: "A conceptual and structural guide defining self-contained plugins using relative paths and a cascading wisdom configuration model for the Source-Archive-Tools ecosystem."
Author: "Christopher Steel"
Date: "2025-11-26"
Last_Modified_Date: "2025-11-26"
License: "CC BY-SA 4.0"
Version: "1.0.0"
Tags:
- "plugins"
- "architecture"
- "source-archive-tools"
- "cascading-wisdom"
- "design"
Keywords:
- "plugin-architecture"
- "relative-paths"
- "configuration"
- "tooling"
- "documentation"
URL: "https://universalcake.com/tools/plugins/docs/self-contained-plugins-and-cascading-wisdom"
Path: "tools/plugins/docs/self-contained-plugins-and-cascading-wisdom.md"
Canonical: "https://universalcake.com/tools/plugins/docs/self-contained-plugins-and-cascading-wisdom"
Sitemap: "true"
DC_Title: "Self-Contained Plugins and Cascading Wisdom: Foundations for a Portable Tool Ecosystem"
DC_Creator: "Christopher Steel"
DC_Subject: "Plugin Architecture and Configuration Hierarchies"
DC_Description: "Defines a standard model for self-contained plugins and multi-layer cascading configuration wisdom across tools."
DC_Language: "en"
DC_Version: "1.0.0"
DC_License: "CC BY-SA 4.0"
DC_RightsHolder: "Christopher Steel"
DC_Contributor: "ChatGPT-5 (OpenAI)"
OG_Title: "Self-Contained Plugins and Cascading Wisdom"
OG_Description: "A foundation for portable plugins, relative-path tooling, and layered configuration wisdom inside Source-Archive-Tools."
OG_URL: "https://universalcake.com/tools/plugins/docs/self-contained-plugins-and-cascading-wisdom"
OG_Image: ""
Schema:
"@context": "https://schema.org"
"@type": "TechArticle"
"contributor": "ChatGPT-5 (OpenAI)"
"about": "Portable plugin models using relative paths and cascading configuration wisdom."
Video_Metadata: ""
---

# Self-Contained Plugins and Cascading Wisdom

This document establishes the foundational architecture for a **self-contained plugin ecosystem** within the Source-Archive-Tools project.
It defines:

- what a plugin *is*
- how plugins structure themselves
- how they avoid global assumptions
- how they participate in a **cascading wisdom** model that produces stable, portable, future-proof tools

This is the reference design for every plugin in `tools/plugins/`.

## What Is a Self-Contained Plugin?

A **self-contained plugin** is a directory that includes everything it needs to run:

- executables
- templates
- sane defaults
- examples
- documentation
- metadata
- tests

Plugins use **relative paths only**, allowing them to be:

- moved
- copied
- nested
- archived
- transferred
- versioned
- reused

without rewriting anything.

A plugin does not assume where it “lives.”
It only assumes:

- **“I am here.”**
- **“Everything I need is under me.”**

This is the key to durability and portability.

## Standard Plugin Layout

Draft of a canonical, future-proof layout:

```
plugin-name/
plugin.yml
bin/
etc/
docs/
examples/
templates/
tests/
meta/
```

### ~~plugin.yml~~ Manifest?

The manifest is intentionally minimal:

- identifies the plugin (`id`, `name`, `version`)
- defines runnable entrypoints
- declares internal paths (always relative)
- contains plugin-level defaults

Example:

```yaml
id: "metadata.dublin-core"
name: "Dublin Core Metadata Plugin"
version: "0.1.0"

entrypoints:
apply:
run: "./bin/apply.sh"
args:
- "--config"
- "./etc/defaults.yml"

paths:
docs: "./docs"
examples: "./examples"
templates: "./templates"
metadata: "./meta"

defaults:
apply_mode: "append-if-missing"
author: "Christopher Steel"
license: "CC BY-SA 4.0"
```

Plugins are **self-documenting** when:

- all examples live under `examples/`
- all human docs live under `docs/`
- all defaults live under `etc/`
- templates are fully relative

The user (or an automated system) can discover everything using relative paths alone.

---

## Cascading Wisdom: A Multi-Layer Configuration Model

“Cascading Wisdom” means:

A plugin begins with its own intelligent defaults, and external contexts may override them—**but never mutate the plugin’s internal state**.

Configuration layers:

1. **Plugin defaults**
 - shipped in the plugin
 - stable, safe, sensible

2. **Project or Archive Overrides**
 Typically in a location such as:
  `archives/dev/universalcake.com/config/metadata.dublin-core.yml`

3. **Invocation-time Overrides**
 (CLI flags, environment variables, temporary settings)

Precedence rule:

```
final_config = CLI > project_overrides > plugin_defaults
```

This gives:

- stable reproducibility
- predictable behaviour
- flexibility
- interoperability
- long-term maintainability

---

## How Tools Discover Plugins

The Source-Archive-Tools “desktop” can discover plugins simply by scanning for `plugin.yml`.

Discovery behavior:

1. Walk the tree:
 `tools/plugins/**/plugin.yml`
2. Read identifiers, entrypoints, descriptions.
3. Build a manifest-of-manifests used by:
 - tool launchers
 - documentation generators
 - archive builders
 - dashboards / UIs

This means plugins do not need registration.
They only need to exist.

---

## Benefits of the Self-Contained + Cascading Wisdom Model

### Portability
A plugin can be moved anywhere without breaking.

### Predictable Behaviour
Defaults always exist and always work.

### Extensibility
Projects can override without replacing.

### Durability
Tools survive time, refactoring, migration, and reorganizing.

### Discoverability
The manifest exposes everything needed for automation or UX.

### Self-Documentation
Examples, docs, and templates travel with the plugin.

### Ecosystem-Scale Power
Plugins become “atoms”—the smallest reusable building blocks of Source-Archive-Tools.

---

## License

This document, *Self-Contained Plugins and Cascading Wisdom: Foundations for a Portable Tool Ecosystem*, by **Christopher Steel**, with AI assistance from **ChatGPT-5 (OpenAI)**, is licensed under the [Creative Commons Attribution-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/).

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)
