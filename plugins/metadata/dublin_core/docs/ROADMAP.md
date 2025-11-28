---
Title: "Dublin Core Plugin Roadmap"
Description: "A progress roadmap for the Dublin Core metadata plugin, including completed tasks and next planned enhancements."
Author: "Christopher Steel"
Date: "2025-11-27"
Last_Modified_Date: "2025-11-27"
License: "CC BY-SA 4.0"
Version: "0.0.1"
Tags:
  - "metadata"
  - "dublin-core"
  - "plugin"
  - "roadmap"
Keywords:
  - "dublin-core"
  - "metadata"
  - "roadmap"
  - "plugin-development"
URL: "https://github.com/steelcj/source-archives-tools/blob/dev/tools/plugins/metadata/dublin_core/docs/ROADMAP.md"
Path: "tools/plugins/metadata/dublin_core/docs/ROADMAP.md"
Canonical: "https://github.com/steelcj/source-archives-tools/blob/dev/tools/plugins/metadata/dublin_core/docs/ROADMAP.md"
OG_URL: "https://github.com/steelcj/source-archives-tools/blob/dev/tools/plugins/metadata/dublin_core/docs/ROADMAP.md"
Sitemap: "false"
DC_Title: "Dublin Core Plugin Roadmap"
DC_Creator: "Christopher Steel"
DC_Subject: "Development roadmap for the Dublin Core metadata plugin"
DC_Description: "Completed steps and future development direction for the Dublin Core metadata plugin in source-archive-tools iteration 0.0.4."
DC_Language: "en"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
DC_Contributor: "ChatGPT-5 (OpenAI)"
DC_RightsHolder: "Christopher Steel"
OG_Title: "Dublin Core Plugin Roadmap"
OG_Description: "A clear roadmap showing completed, active, and upcoming work for the Dublin Core metadata plugin."
OG_URL: "https://github.com/steelcj/source-archives-tools/blob/main/plugins/metadata/dublin_core/docs/ROADMAP.md"
OG_Image: ""
Schema:
  "@context": "https://schema.org"
  "@type": "TechArticle"
  "headline": "Dublin Core Plugin Roadmap"
  "author": "Christopher Steel"
  "inLanguage": "en"
  "license": "https://creativecommons.org/licenses/by-sa/4.0/"
  "contributor": "ChatGPT-5 (OpenAI)"
Video_Metadata: ""
---

# Dublin Core Plugin Roadmap

This document tracks progress on the **Dublin Core metadata plugin** implemented as part of the **0.0.4 plugin-based architecture** for `source-archive-tools`.  
It includes completed milestones, work in progress, and clear next steps.

# Completed

- Established plugin directory structure:
  - `plugins/metadata/dublin_core/`

- Implemented:
  - `plugin.yml` (manifest)
  - `plugin.py` (metadata transformation logic)
  - `config/defaults.yml` (baseline configuration)

- Added example configuration profiles:
  - `minimal.yml`
  - `defaults.yml`
  - `custom.yml`
  - `complete.yml`

- Added plugin documentation:
  - `docs/examples-overview.md`

- Implemented plugin loader support for hyphen/underscore normalization.

- Implemented plugin self-tests:
  - `self_test.py`
  - CLI wrapper:  
    ```bash
    ./cli/sat-test-plugin metadata.dublin-core
    ```

- Verified end-to-end functionality:
  ```
  [OK] minimal.yml
  [OK] defaults.yml
  [OK] custom.yml
  [OK] complete.yml
  ```

# In Progress

- Refining internal plugin documentation to define:
  - structure of example profiles
  - purpose and expectations of self-tests
  - how plugin metadata fields interact with defaults

- Reviewing plugin architecture conventions to ensure portability across future plugins:
  - example placement
  - naming patterns
  - manifest consistency guidelines

# Next Steps

## Improve Dublin Core Plugin Behavior

- Add clearer messages for missing required fields  
- Add support for dry-run metadata application (output only)  
- Add richer validation rules beyond mere presence  
- Add optional strict mode for enforcing complete compliance  

## Enhance Plugin Loader

- Validate manifest structure (required keys, entrypoints, paths)  
- Improve error messages for missing or malformed plugin content  
- Add plugin metadata inspection commands for debugging  

## Expand Example Usage

- Add Markdown-based examples under:
  ```
  plugins/metadata/dublin_core/examples/docs/
  ```
- Provide before/after examples to show transformation  

## Integrate With Higher-Level Test Runner

- Add a global CLI:
  ```
  sat-test-all
  ```
  which runs all plugin-level self-tests and summarizes results  

## Prepare for Next Plugin

Recommended next plugins (in order):

1. APA7 metadata plugin  
2. CAP (Citation Anchor Pair) plugin  
3. Schema.org metadata (JSON-LD) plugin  

Each will follow the same structure pioneered by the Dublin Core plugin.

# Optional Future Enhancements

- Add schema validation for metadata example files  
- Add dependency graph or capability declaration to manifest  
- Add plugin discovery UI:
  ```
  sat list-plugins --type metadata
  ```

## License

This document, *Dublin Core Plugin Roadmap*, by **Christopher Steel**, with AI assistance from **ChatGPT-5 (OpenAI)**, is licensed under the Creative Commons Attribution-ShareAlike 4.0 License.

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)
