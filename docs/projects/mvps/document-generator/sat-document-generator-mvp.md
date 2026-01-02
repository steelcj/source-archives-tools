---
Title: "SAT Document Generator MVP"
Description: "A standalone, data-driven generator for injecting SAT-compliant front matter into Markdown documents based on file path and context."
Author: "Christopher Steel"
Date: "2026-01-01"
License: "CC BY-SA 4.0"
Path: "projects/mvps/document-generator/sat-document-generator-mvp.md"
Canonical: "https://universalcake.com/projects/mvps/document-generator"
Sitemap: "true"
DC_Subject: "Document Generation, Metadata Automation, SAT Tools"
DC_Description: "Generates SAT-compliant front matter for Markdown documents using filename, path, and config — no hardcoded values, fully data-driven."
Domain: "projects"
Category: "mvps"
Locale: "en-ch"
---

# SAT Document Generator MVP

> **Generate SAT-compliant front matter for Markdown documents — based on file path, filename, and config — not hardcoded values.**

This is a **standalone MVP**, not a plugin — designed to inject consistent, data-driven metadata into documents in a SAT-compliant way.

## Purpose

- Inject front matter into `.md` files
- Derive metadata from filename and path
- Follow SAT conventions for structure, fields, and localization
- Human-in-the-loop — explicit, opt-in, no background execution

## Features

- Title from filename -> `Draft Users Manual Pipeline SKetch` -> `Draft Users Manual Pipeline Sketch`
- Description from title -> `"Initial draft of {{ title }}."`
- Path from relative path -> `docs/en-ch/projects/information-architecture/Draft Users Manual Pipeline SKetch.md`
- Date from now -> `2026-01-01`
- Canonical from config -> `https://universalcake.com/...`
- Locale, domain, category from path -> `en-ch`, `projects`, `information-architecture`
- No hardcoded values
- Fully data-driven
- No YAML parsing errors — no `---` in model
- Uses Jinja2 templates for structure — not logic

---

## Quick Start

```bash
bin/sat-generate-document.py archives/euria-generated/docs/en-ch/projects/information-architecture/Draft\ Users\ Manual\ Pipeline\ SKetch.md
```

```yaml
---
Title: "Draft Users Manual Pipeline Sketch"
Description: "Initial draft of Draft Users Manual Pipeline Sketch."
Author: "Christopher Steel"
Date: "2026-01-01"
License: "CC BY-SA 4.0"
Path: "docs/en-ch/projects/information-architecture/Draft Users Manual Pipeline SKetch.md"
Sitemap: "true"
DC_Subject: "Documentation, Process Design"
DC_Description: "Draft sketch of Draft Users Manual Pipeline Sketch under SAT standards."
Domain: "projects"
Category: "information-architecture"
Locale: "en-ch"
---
```

## Architecture

### 1. Context Extraction

Extract from file path:

    locale -> from docs/en-ch/...
    domain -> from docs/en-ch/projects/...
    category -> from docs/en-ch/projects/information-architecture/...
    basename -> from Draft Users Manual Pipeline SKetch.md
    relative_path -> from archives/euria-generated/ -> docs/en-ch/...

### 2. Model Computation

Compute in Python — not Jinja2:

```python
title = basename.replace('-', ' ').replace('_', ' ').title()
description = f"Initial draft of {title}."
dc_description = f"Draft sketch of {title} under SAT standards."
date = datetime.now().strftime("%Y-%m-%d")
path = relative_path
...
```

### 3.  Template Rendering

Use sat-document-template.yml.j2:

```yaml
---
Title: "{{ title }}"
Description: "{{ description }}"
Author: "{{ author }}"
Date: "{{ date }}"
License: "{{ license }}"
Path: "{{ path }}"
{% if canonical %}Canonical: "{{ canonical }}"{% endif %}
Sitemap: "{{ sitemap }}"
DC_Subject: "{{ dc_subject }}"
DC_Description: "{{ dc_description }}"
Domain: "{{ domain }}"
Category: "{{ category }}"
Locale: "{{ locale }}"
---
```

### 4. Output Injection

    If front matter exists -> skip
    If not -> inject at top

## File Structure

```bash
docs/projects/mvps/document-generator/
├── README.md
├── sat-generate-document.py
├── templates/
│   └── sat-document-template.yml.j2
├── models/
│   └── document-context.yml.j2
└── config.yml
```

### Configuration (config.yml)

DO THIS LATER IF DOING THIS
```yaml
base_url: "https://universalcake.com"
```

Optional — if missing, uses fallback.

### Template (sat-document-template.yml.j2)

```yaml
---
Title: "{{ title }}"
Description: "{{ description }}"
Author: "{{ author }}"
Date: "{{ date }}"
License: "{{ license }}"
Path: "{{ path }}"
{% if canonical %}Canonical: "{{ canonical }}"{% endif %}
Sitemap: "{{ sitemap }}"
DC_Subject: "{{ dc_subject }}"
DC_Description: "{{ dc_description }}"
Domain: "{{ domain }}"
Category: "{{ category }}"
Locale: "{{ locale }}"
---
```

### Model (document-context.yml.j2)

```yaml
title: "{{ basename | title | replace('-', ' ') | replace('_', ' ') }}"
description: "Initial draft of {{ title }}."
dc_description: "Draft sketch of {{ title }} under SAT standards."
date: "{{ now }}"
path: "{{ relative_path }}"
domain: "{{ domain }}"
category: "{{ category }}"
locale: "{{ locale }}"
dc_subject: "Documentation, Process Design"
author: "Christopher Steel"
license: "CC BY-SA 4.0"
sitemap: "true"
# canonical: "{{ base_url }}/{{ path }}"  ← commented out, as desired
```

## Validation

No YAML parsing errors — because:

    Model has no ---
    Template has --- — but it’s not parsed — it’s written to file
    All logic in Python — no Jinja2 computation in model

## SAT Compliance

    Human in the loop — explicit, opt-in
    No background execution
    Interpreter neutral — doesn’t change what the document means
    Plugins never replace intent — front matter is derived, not defined
    Definition is source of truth — front matter is computed from it

## License

This document, SAT Document Generator MVP, by Christopher Steel, with AI assistance from Euria (Infomaniak), is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License.

CC License

Euria is an ethical, Swiss-hosted AI assistant developed by Infomaniak. No data is stored. Powered by renewable energy.
