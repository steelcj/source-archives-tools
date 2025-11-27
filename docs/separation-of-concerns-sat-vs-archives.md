---
Title: "Separation of Concerns: How SAT (Source-Archive-Tools) Relates to Created Archives"
Description: "A clear explanation of how the SAT repository functions as the canonical toolkit—and how created archives consume SAT tools, templates, and configuration. Includes guidance on directory boundaries, installation logic, and recommended archive-init behavior."
Author: "Christopher Steel"
Date: "2025-11-25"
Last_Modified_Date: "2025-11-25"
License: "CC BY-SA 4.0"
Version: "1.0.0"
Tags:
  - "source-archive-tools"
  - "sat"
  - "design"
  - "architecture"
  - "archives"
Keywords:
  - "Sovereign Archive Toolkit"
  - "SAT"
  - "archive-init"
  - "metadata"
  - "templates"
URL: "https://universalcake.com/tools/docs/use/separation-of-concerns-sat-vs-archives"
Path: "tools/docs/use/separation-of-concerns-sat-vs-archives.md"
Canonical: "https://universalcake.com/tools/docs/use/separation-of-concerns-sat-vs-archives"
Sitemap: "true"
DC_Title: "Separation of Concerns: How SAT (Source-Archive-Tools) Relates to Created Archives"
DC_Creator: "Christopher Steel"
DC_Subject: "Source-Archive-Tools architecture and archive separation model"
DC_Description: "A formal documentation defining how SAT serves as the canonical toolkit and how created archives inherit tools and templates from it."
DC_Language: "en"
DC_Version: "1.0.0"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
DC_RightsHolder: "Christopher Steel"
OG_Title: "Separation of Concerns: SAT vs Created Archives"
OG_Description: "Understanding how the Sovereign Archive Toolkit (SAT) relates to individual archives."
OG_URL: "https://universalcake.com/tools/docs/use/separation-of-concerns-sat-vs-archives"
Schema:
  "@type": "TechArticle"
  "about": "Source-Archive-Tools architecture"
  "contributor": "ChatGPT-5 (OpenAI)"
Video_Metadata: 
  "null"
---

# Separation of Concerns: How SAT (Source-Archive-Tools) Relates to Created Archives

This document clarifies the separation between your **SAT repository** (the canonical toolkit) and **individual created archives** (the consumers).  
It also lays out best practices for directory boundaries, templates, installed tools, and how `archive-init` should populate a new archive.

No numbering is used for headings.

---

## SAT Means the Source-Archive-Tools Repository Only

Throughout development, the abbreviation **SAT** refers *exclusively* to:

```
source-archive-tools/
```

This repo is:

- The **canonical source** of all tooling  
- The place where you keep:
  - templates  
  - plugins  
  - shared libraries  
  - developer documentation  
  - the runtime Bash tools (`sat-*`)
- The direction of truth for all archive generation

Created archives are **never** authoritative about SAT tools—only consumers.

---

## What Belongs in SAT (and Nowhere Else)

SAT should be structured like this:

```
source-archive-tools/
  tools/
    sat-refresh-path-metadata
    sat-fill-default-metadata
    sat-check-archive
    lib/
      __init__.py
      io_utils.py
      metadata_utils.py
    plugins/
      # reserved for future taxonomy/metadata plugins

  templates/
    config/
      project.yml.example
      languages.yml.example
      structure.yml.example
      metadata_defaults.yml.example
      tools_manifest.yml.example

  docs/
    dev/
    use/
```

SAT contains:

- **All tools**
- **All template files**
- **All plugin directories**
- **All library code**
- **All developer + maintainer documentation**

Created archives **pull from SAT**, not the other way around.

---

## What Belongs in a Created Archive

When `archive-init` generates a new archive, it should install:

### Tools (copied verbatim from SAT)

```
archive-root/
  tools/
    sat-refresh-path-metadata
    sat-fill-default-metadata
    sat-check-archive
```

**Only** the runtime scripts.  
No `tools/lib`.  
No `tools/plugins`.  
No `.example` files.

### Configuration (generated or copied from templates)

```
archive-root/
  config/
    project.yml            <- rendered from .example
    languages.yml          <- rendered from .example
    structure.yml          <- rendered from .example
    metadata_defaults.yml  <- copied from .example
    tools_manifest.yml     <- copied from .example
```

### Locale roots

```
archive-root/
  en-ca/
  fr-ca/
  ...
```

No additional SAT directories should appear inside the archive.

---

## Why Templates Must Stay in SAT

Files such as:

- `project.yml`
- `languages.yml`
- `structure.yml`
- `tools_manifest.yml`
- `metadata_defaults.yml`

are **archive-specific configuration**.  
They cannot be shipped as fixed files inside SAT.

Therefore SAT ships:

```
templates/config/*.example
```

and `archive-init` generates:

```
config/*.yml
```

based on user input.

The rule:

> Anything that depends on user input → template  
> Anything uniform across all archives → tool

---

## Why lib/ and plugins/ Stay Only in SAT

The directories:

```
tools/lib/
tools/plugins/
```

are part of SAT’s internal extensibility layer.  
They:

- store shared Python helpers  
- store future metadata/taxonomy plugins  
- evolve independently of any archive  
- should not be shipped into each archive unless needed  

Your current tools are Bash-only → no runtime need for these in archives yet.

Later, if Python tools require them, SAT will install *only the required plugins*.

---

## Updating Existing Archives

Your wellbeing archive serves as a prototype.  
Once SAT becomes canonical:

1. Move `tools/` and template files from the prototype into SAT  
2. Clean the archive so it only contains runtime versions  
3. Any further SAT updates can be selectively copied into existing archives manually or via a future helper tool

This ensures SAT is the direction of truth.

---

## The Result: Clean, Predictable Separation

### SAT is:
- Pure toolkit  
- Templates  
- Plugins  
- Libs  
- Docs  
- Canonical tool versions  

### Archives are:
- Individual instantiations  
- Minimal runtime toolsets  
- Archive-specific config  
- Content (Markdown)  

This separation ensures maintainability, upgradability, and clarity.

---

## License

This document, *Separation of Concerns: How SAT (Source-Archive-Tools) Relates to Created Archives*, by **Christopher Steel**, with AI assistance from **ChatGPT-5 (OpenAI)**, is licensed under the [Creative Commons Attribution-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/).

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)
