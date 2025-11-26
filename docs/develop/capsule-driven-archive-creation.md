---
Title: "Capsule-Driven Archive Creation: Simplifying SAT Installation Logic with Plugin Manifests"
Description: "A structured explanation of how Source-Archive-Tools (SAT) can use capsule-style plugins to simplify archive creation, reduce hardcoding, and enable declarative installation of tools, metadata, and taxonomy components."
Author: "Christopher Steel"
Date: "2025-11-25"
Last_Modified_Date: "2025-11-25"
License: "CC BY-SA 4.0"
Version: "1.0.0"
Tags:
  - "sat"
  - "source-archive-tools"
  - "plugins"
  - "capsules"
  - "archive-init"
Keywords:
  - "Sovereign Archive Toolkit"
  - "capsule plugins"
  - "plugin.yml"
  - "archive creation"
  - "metadata capsules"
URL: "https://universalcake.com/tools/docs/use/capsule-driven-archive-creation"
Path: "tools/docs/use/capsule-driven-archive-creation.md"
Canonical: "https://universalcake.com/tools/docs/use/capsule-driven-archive-creation"
Sitemap: "true"
DC_Title: "Capsule-Driven Archive Creation: Simplifying SAT Installation Logic with Plugin Manifests"
DC_Creator: "Christopher Steel"
DC_Subject: "Capsule-style plugin architecture for Source-Archive-Tools"
DC_Description: "A detailed guide describing how SAT can use declarative capsules to simplify archive initialization and modular installation of tools, templates, and metadata engines."
DC_Language: "en"
DC_Version: "1.0.0"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
DC_RightsHolder: "Christopher Steel"
OG_Title: "Capsule-Driven Archive Creation"
OG_Description: "How SAT plugins can simplify archive creation using declarative manifest-based capsules."
OG_URL: "https://universalcake.com/tools/docs/use/capsule-driven-archive-creation"
Schema:
  "@type": "TechArticle"
  "about": "Source-Archive-Tools plugins and capsule architecture"
  "contributor": "ChatGPT-5 (OpenAI)"
Video_Metadata: 
  "null"
---

# Capsule-Driven Archive Creation: Simplifying SAT Installation Logic with Plugin Manifests

This document explains how the **Source-Archive-Tools (SAT)** repository can use **capsule-style plugins** to dramatically simplify archive creation.  
Capsules enable declarative installation of tools, metadata engines, taxonomy definitions, and configuration templates—without requiring `archive-init` to know anything about the details.

## What Is a Capsule?

A **capsule** is a self-contained plugin directory under the SAT `plugins/` hierarchy.

A capsule:

- Contains files to install into new archives  
- Provides a small manifest (`plugin.yml`) describing:
  - Its identity
  - What kind of plugin it is
  - Where its files should be copied inside an archive  
- May include canonical definitions (`standard/`), SAT-specific config (`config/`), runtime code (`plugin.py`), or templates.

A capsule describes its own installation process.  
The `archive-init` tool simply reads the manifest and copies accordingly.

---

## Example: The Dublin Core Metadata Capsule

The following structure is an example of a metadata capsule:

```
plugins/
  metadata/
    dublin-core/
      standard/
      config/
      plugin.py
      plugin.yml
```

The corresponding `plugin.yml` might be:

```yaml
plugin_id: "metadata.dublin-core"
kind: "metadata-capsule"

description: "Dublin Core 1.1 metadata interpretation and defaults for SAT archives."

install:
  - src: "standard/"
    dest: "config/metadata/dublin-core/standard/"

  - src: "config/"
    dest: "config/metadata/dublin-core/config/"

  - src: "plugin.py"
    dest: "tools/plugins/metadata/dublin-core/plugin.py"
```

This removes all “tool-specific copy logic” from `archive-init`.

---

## Capsule Example: Core Runtime Tools

Bash-based tools can also be packaged as a capsule:

```
plugins/
  tools/
    core-runtime/
      plugin.yml
      tools/
        sat-refresh-path-metadata
        sat-fill-default-metadata
        sat-check-archive
      templates/
        metadata_defaults.yml.example
        tools_manifest.yml.example
```

A `plugin.yml` for this capsule might be:

```yaml
plugin_id: "tools.core-runtime"
kind: "tools-capsule"

description: "Core SAT runtime tools for metadata path derivation and defaults."

install:
  - src: "tools/sat-refresh-path-metadata"
    dest: "tools/sat-refresh-path-metadata"

  - src: "tools/sat-fill-default-metadata"
    dest: "tools/sat-fill-default-metadata"

  - src: "tools/sat-check-archive"
    dest: "tools/sat-check-archive"

  - src: "templates/metadata_defaults.yml.example"
    dest: "config/metadata_defaults.yml"

  - src: "templates/tools_manifest.yml.example"
    dest: "config/tools_manifest.yml"
```

This defines exactly how to install core SAT tools into new archives.

---

## How Archive Creation Changes with Capsules

Without capsules, `archive-init` contains hard-coded logic:

- Copy tool A  
- Copy tool B  
- Copy config C  
- Copy template D  
- Don’t forget E  

This becomes brittle and error-prone.

With capsules:

> `archive-init` only needs to know which capsules are activated.

Example:

```bash
archive-init \
  --root-dir ~/archives/wellbeing-mvp \
  --canonical en-CA \
  --taxonomy para \
  --capsules tools.core-runtime,metadata.dublin-core
```

Then `archive-init`:

1. Scans SAT `plugins/` for the listed capsule IDs  
2. Loads each capsule’s `plugin.yml`  
3. For each `install` entry:
   - Copies `SAT/plugins/.../<src>`  
   - Into `<archive-root>/<dest>`  

No special knowledge built into the initializer.

---

## Benefits of Capsule-Driven Design

### Configuration stays in SAT’s templates  
Archives only get rendered versions, avoiding duplication.

### Tools are installed cleanly  
Capsules describe their own file layout and install paths.

### New capabilities become drop-in  
To add a taxonomy or metadata engine:

```
plugins/taxonomy/para/
plugins/metadata/apa7-cap/
```

with `plugin.yml` in each directory.

No changes needed in `archive-init`.

### Clean separation of concerns  
- SAT is the toolkit  
- Archives are consumers  
- Capsules are modular building blocks  

### Future upgrades become simple  
Eventually an archive can use its `tools_manifest.yml` to:

- re-install missing capsules  
- update capsule contents  
- migrate to new SAT versions  

---

## A Capsule-First SAT Ecosystem

Your long-term vision naturally leads here:

- SAT becomes a library of capsules  
- “Capsules” become the unit of modularity and installation  
- Archive creation becomes declarative  
- Archive maintenance tools read capsule manifests  
- Plugins become first-class SAT components  

You already defined the early structure perfectly with the Dublin Core metadata plugin:

```
standard/
config/
plugin.py
plugin.yml
```

This is now the consistent pattern across:

- metadata engines  
- taxonomy engines  
- tool bundles  
- defaults  
- override logic  
- accessibility support  
- path metadata tooling  

Everything can be expressed as a capsule.

---

## License

This document, *Capsule-Driven Archive Creation: Simplifying SAT Installation Logic with Plugin Manifests*, by **Christopher Steel**, with AI assistance from **ChatGPT-5 (OpenAI)**, is licensed under the [Creative Commons Attribution-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/).

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)