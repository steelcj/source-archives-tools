---
Title: "Creating a Pilot Archive for Testing sat-refresh-path-metadata"
Description: "A practical guide for setting up a minimal well-being archive containing PARA-structured content to support MVP development and testing of sat-refresh-path-metadata."
Author: "Christopher Steel"
Date: "2025-11-25"
Last_Modified_Date: "2025-11-25"
License: "CC BY-SA 4.0"
Version: "1.0.0"
Tags:
  - "source-archives"
  - "sat-tools"
  - "well-being"
  - "para"
  - "metadata"
Keywords:
  - "archive-initialization"
  - "path-metadata"
  - "content-structure"
  - "paradigm"
  - "testing"
URL: "https://universalcake.com/tools/docs/develop/creating-a-pilot-archive-for-testing-sat-refresh"
Path: "tools/docs/develop/creating-a-pilot-archive-for-testing-sat-refresh.md"
Canonical: "https://universalcake.com/tools/docs/develop/creating-a-pilot-archive-for-testing-sat-refresh"
Sitemap: "true"
DC_Title: "Creating a Pilot Archive for Testing sat-refresh-path-metadata"
DC_Creator: "Christopher Steel"
DC_Subject: "Pilot archive setup for testing sat-refresh-path-metadata"
DC_Description: "A step-by-step guide for constructing a minimal PARA-based well-being archive to support development and validation of path-metadata regeneration tools."
DC_Language: "en"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
OG_Title: "Creating a Pilot Archive for Testing sat-refresh-path-metadata"
OG_Description: "Build a structured PARA well-being archive to provide real content for sat-refresh-path-metadata testing."
OG_URL: "https://universalcake.com/tools/docs/develop/creating-a-pilot-archive-for-testing-sat-refresh"
Schema:
    "@context": "https://schema.org"
    "@type": "TechArticle"
    "name": "Creating a Pilot Archive for Testing sat-refresh-path-metadata"
    "description": "A practical document describing how to assemble a small well-being archive to support tool development and testing."
    "author": "Christopher Steel"
    "contributor": "ChatGPT-5.1 (OpenAI)"
Video_Metadata: {}
---

# Creating a Pilot Archive for Testing sat-refresh-path-metadata

Before implementing or refining `sat-refresh-path-metadata`, we need real content for safety, correctness, and meaningful development.  
This guide describes how to build a **small PARA-structured well-being archive** to serve as an MVP testbed.

The goal is not to reconstruct the entire well-being site, but to create **just enough content** so that `sat-refresh-path-metadata` can walk realistic directories, discover Markdown files, and compute path-based metadata.

# Step 1: Initialize a New Pilot Archive

Use your existing archive initialization script to create an MVP well-being archive:

```bash
./init-archive.sh \
  --root-dir ~/archives/wellbeing-mvp \
  --canonical en-CA \
  --taxonomy para \
  --apply
```

This produces:

```
~/archives/wellbeing-mvp/
  config/
  en-ca/
  taxonomy/
  tools/
```

The canonical language directory (`en-ca`) will be the home of our minimal content structure.

# Step 2: Create a Minimal PARA Content Structure

Inside the canonical language root, create the simplest possible PARA directory layout:

```bash
cd ~/archives/wellbeing-mvp/en-ca
ls -al w	
```

This gives you:

```
en-ca/
  areas/
    well-being/
      projects/
      resources/
  resources/
    research/
    practices/
```

This structure provides varied nesting depth for testing metadata path derivation.

# Step 3: Add Four Minimal Markdown Files

These files contain placeholder YAML metadata where `Path`, `URL`, and `Canonical` are deliberately incorrect (`"TODO"`).  
This gives the `sat-refresh-path-metadata` tool something concrete to detect and propose replacements for.

## Project-level document

```bash
cat > areas/well-being/projects/wellbeing-overview.md <<'EOF'
---
Title: "Well-Being Overview"
Path: "TODO"
URL: "TODO"
Canonical: "TODO"
---

# Well-Being Overview

This is a pilot document describing the overall approach to well-being in this archive.
EOF
```

## Resource-level document (well-being dimensions)

```bash
cat > areas/well-being/resources/wellbeing-dimensions.md <<'EOF'
---
Title: "Dimensions of Well-Being"
Path: "TODO"
URL: "TODO"
Canonical: "TODO"
---

# Dimensions of Well-Being

This is a placeholder for content on dimensions or models of well-being.
EOF
```

## Research resource (ACEs)

```bash
cat > resources/research/aces-and-health.md <<'EOF'
---
Title: "ACEs and Health"
Path: "TODO"
URL: "TODO"
Canonical: "TODO"
---

# ACEs and Health

Placeholder for content linking Adverse Childhood Experiences and long-term health outcomes.
EOF
```

## Practices resource (grounding exercises)

```bash
cat > resources/practices/basic-grounding.md <<'EOF'
---
Title: "Basic Grounding Practices"
Path: "TODO"
URL: "TODO"
Canonical: "TODO"
---

# Basic Grounding Practices

Placeholder for simple grounding practices and exercises.
EOF
```

# Step 4: Why This Pilot Archive Matters

With this minimal archive in place, `sat-refresh-path-metadata` can now:

- Walk directories with realistic PARA layout  
- Detect Markdown files with YAML metadata  
- Compute path-based metadata (`Path`, `URL`, `Canonical`)  
- Display “old → new” corrections in plan mode  
- Confirm your rules produce stable, predictable results  
- Eventually perform safe write-back updates

This pilot archive is small enough to experiment freely, but rich enough to meaningfully test path derivation, taxonomy placement, and future metadata rules.

# Step 5: Next Step — Implementing v0.1 sat-refresh-path-metadata

Now that the archive contains realistic content, the next development action is:

- Implementing a **read-only plan mode** (`--dry-run`) for:
  - Reading YAML front matter
  - Computing correct derived paths
  - Printing differences, without touching the file system

Once the plan mode feels correct and predictable, write-back functionality can be added.

# License

This document, *Creating a Pilot Archive for Testing sat-refresh-path-metadata*, by **Christopher Steel**, with AI assistance from **ChatGPT-5.1 (OpenAI)**, is licensed under the [Creative Commons Attribution-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/).

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)