---
Title: "Data-Driven Archive Behavior — Plugin Types and Integration Points"
Description: "Developer-facing overview of plugin types used in the Data-Driven Archive Behavior MVP, including where plugins attach in the interpretation flow and concrete examples of their responsibilities."
Author: "Christopher Steel"
Date: "2025-12-30"
Last_Modified_Date: "2025-12-30"
License: "CC BY-SA 4.0"
Tags:
  - "source-archive-tools"
  - "sat"
  - "mvp"
  - "data-driven"
  - "plugins"
URL: "https://universalcake.com/docs/projects/mvps/data-driven/plugins/data-driven-archive-behavior-plugin-types"
Path: "docs/projects/mvps/data-driven/plugins/data-driven-archive-behavior-plugin-types.md"
Canonical: "https://universalcake.com/docs/projects/mvps/data-driven/plugins/data-driven-archive-behavior-plugin-types"
Sitemap: "true"
Keywords:
  - "sat plugins"
  - "data-driven behavior"
  - "archive interpretation"
  - "plugin architecture"
  - "declarative archives"
  DC_Title: "Data-Driven Archive Behavior — Plugin Types and Integration Points"
  DC_Creator: "Christopher Steel"
  DC_Subject: "Plugin roles and extension points in a data-driven archive interpretation model"
  DC_Description: "Defines plugin categories, responsibilities, and integration points within the Data-Driven Archive Behavior MVP for SAT."
  DC_Language: "en"
  DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
  Robots: "index, follow"
  OG_Title: "Data-Driven Archive Behavior — Plugin Types and Integration Points"
  OG_Description: "Developer overview of plugin types and where they attach in the Data-Driven Archive Behavior MVP."
  OG_URL: "https://universalcake.com/docs/projects/mvps/data-driven/plugins/data-driven-archive-behavior-plugin-types"
  Schema:
    "@type": "TechArticle"
    "name": "Data-Driven Archive Behavior — Plugin Types and Integration Points"
    "author": "Christopher Steel"
    "license": "https://creativecommons.org/licenses/by-sa/4.0/"
---

# Plugin Types and Integration Points

This document describes the **types of plugins** that may be used with the *Data-Driven Archive Behavior* MVP, the **roles they play**, and **where they attach** in the overall process.

This is a **developer-oriented overview**, not a specification.  
The intent is to clarify *where extension is possible* without constraining implementation prematurely.


## Core Process (Context)

The MVP establishes a simple, explicit flow:

1. An archive definition is read as data  
2. The definition is interpreted once  
3. A human-readable understanding of intended structure is produced  

Plugins attach **around this flow**, not inside the definition itself.


## Plugin Categories

Plugins are best understood by **what stage they attach to**, not by what technology they use.


## Definition Plugins

### Role

Definition plugins operate on the **archive definition file itself**.

They exist to help humans author, review, and reason about definitions.

### Examples

- Validate allowed fields and shapes
- Enforce naming conventions (e.g., language codes)
- Check required keys beyond the MVP minimum
- Enforce formatting or structural norms
- Gate definitions by supported schema versions

### Characteristics

- Input: raw archive definition data
- Output: pass / fail with explanation
- No filesystem access
- No interpretation logic
- No mutation

## Interpretation Augmentation Plugins

### Role

These plugins extend or enrich the **interpreted meaning** of a definition without changing the definition itself.

They add *derived structure* or annotations.

### Examples

- Expanding shorthand definitions into full structural sets
- Adding default or conventional subpaths
- Annotating interpreted paths with labels or metadata
- Injecting computed expectations (e.g., index files)

### Characteristics

- Input: parsed definition
- Output: augmented interpretation
- No filesystem mutation
- No enforcement

## Projection Plugins

### Role

Projection plugins take an **interpreted structure** and project it into another form.

They do not change reality; they *represent* intent in a different medium.

### Examples

- Render a directory tree preview
- Generate Markdown documentation
- Export JSON or YAML for other tools
- Visualize structure graphically

### Characteristics

- Input: interpreted structure
- Output: representation
- Read-only with respect to the archive

## Execution / Mutation Plugins

### Role

Execution plugins are responsible for **changing the world** based on interpreted intent.

They are always explicit and opt-in.

### Examples

- Create missing directories
- Initialize placeholder files
- Scaffold empty archive structures

### Characteristics

- Input: interpreted structure
- Output: filesystem changes + report
- Never implicit
- Never automatic

## Reporting and Visualization Plugins

### Role

These plugins improve **human understanding** of definitions, interpretations, or execution outcomes.

### Examples

- Pretty console output
- Diff-style summaries
- Tree views
- HTML or static visualizations

### Characteristics

- No effect on meaning or behavior
- Purely presentational

## Policy and Governance Plugins (Optional)

### Role

These plugins encode **organizational or social constraints**, not technical ones.

### Examples

- Enforcing required languages
- Restricting allowed domains
- Approval workflows

### Characteristics

- Context-specific
- Never hard-coded into the engine
- Always explicit

## Plugin Integration Flow

The following diagram shows **where each plugin type attaches** relative to the core MVP process.

```mermaid
flowchart LR
    A[Archive Definition File] --> B[Definition Plugins]

    B --> C[Core Interpreter]

    C --> D[Interpretation Augmentation Plugins]

    D --> E[Interpreted Structure]

    E --> F[Projection Plugins]
    E --> G[Execution / Mutation Plugins]
    E --> H[Reporting / Visualization Plugins]
```

## Key Design Insight

The interpreter remains **neutral and minimal**.

Plugins:
- constrain inputs
- enrich interpretation
- project meaning
- or apply changes

They do **not** redefine what an archive definition *means*.

## Summary

The Data-Driven Archive Behavior model supports extension by:

- clearly separating stages of responsibility
- allowing plugins to attach at specific points
- keeping the core engine small and trustworthy

This structure enables growth **without sacrificing clarity or control**.
## License

This document, *Data-Driven Archive Behavior — Plugin Types and Integration Points*, by **Christopher Steel**, with AI assistance from **ChatGPT-5.2 (OpenAI)**, is licensed under the [Creative Commons Attribution-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/).

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)