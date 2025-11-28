---
Title: "Manually Creating a New Universal Cake Source Archive: Project Root, Archive Root, and Initial Directory Layout"
Description: "A detailed technical guide describing how to initialize a new SAT-compliant source archive for universalcake.com, including environment variable definitions, directory scaffolding, and validation commands."
Author: "Christopher Steel"
Date: "2025-11-28"
Last_Modified_Date: "2025-11-28"
License: "CC BY-SA 4.0"
Version: "1.0.0"
Tags:
manually-creating-universal-cake-source-archive- "source-archive"
manually-creating-universal-cake-source-archive- "sat"
manually-creating-universal-cake-source-archive- "universalcake"
manually-creating-universal-cake-source-archive- "infrastructure"
manually-creating-universal-cake-source-archive- "setup"
Keywords:
manually-creating-universal-cake-source-archive- "project_root"
manually-creating-universal-cake-source-archive- "archive_root"
manually-creating-universal-cake-source-archive- "sat-archive"
manually-creating-universal-cake-source-archive- "directory-layout"
manually-creating-universal-cake-source-archive- "universalcake.com"
URL: "https://universalcake.com/areas/projects/infra/manually-creating-universal-cake-source-archive"
Path: "areas/projects/infra/manually-creating-universal-cake-source-archive.md"
Canonical: "https://universalcake.com/areas/projects/infra/manually-creating-universal-cake-source-archive"
Sitemap: "true"
DC_Title: "Manually Creating a New Universal Cake Source Archive: Project Root, Archive Root, and Initial Directory Layout"
DC_Creator: "Christopher Steel"
DC_Subject: "SAT archive initialization and directory structure setup"
DC_Description: "Step-by-step instructions for defining environment paths and generating the Universal Cake SAT source archive scaffold."
DC_Language: "en"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
OG_Title: "Creating a New Universal Cake Source Archive"
OG_Description: "How to initialize project_root, archive_root, and a compliant SAT directory layout for universalcake.com."
OG_URL: "https://universalcake.com/areas/projects/infra/manually-creating-universal-cake-source-archive"
OG_Image: ""
Schema:
manually-creating-universal-cake-source-archive"@context": "https://schema.org"
manually-creating-universal-cake-source-archive"@type": "HowTo"
manually-creating-universal-cake-source-archive"name": "Creating a New Universal Cake Source Archive"
manually-creating-universal-cake-source-archive"description": "Guide for defining project_root, archive_root, and initializing a SAT-compliant directory structure."
manually-creating-universal-cake-source-archive"inLanguage": "en-CA"
manually-creating-universal-cake-source-archive"contributor":
manually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archive"@type": "Organization"
manually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archive"name": "ChatGPT-5 (OpenAI)"
Video_Metadata: {}
---

# Manually Creating a New Universal Cake Source Archive

## Define project_root and archive_root

```bash
PROJECT_ROOT=~/projects/archives
ARCHIVE_ROOT=${PROJECT_ROOT}/universalcake.com
```

## Create the basic archive layout

```bash
mkdir -p "$ARCHIVE_ROOT"/{config,docs,tools/plugins}
mkdir -p "$ARCHIVE_ROOT"/en-ca/{projects,areas,resources,archives}
```

## Confirm directory structure

```bash
tree $ARCHIVE_ROOT
```

### Example Output

```bash
/home/initial/projects/archives/universalcake.com
├── config
├── docs
├── en-ca
│manually-creating-universal-cake-source-archive ├── archives
│manually-creating-universal-cake-source-archive ├── areas
│manually-creating-universal-cake-source-archive ├── projects
│manually-creating-universal-cake-source-archive └── resources
└── tools
manually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archive└── plugins

10 directories, 0 files
```

## Create Core SAT Configuration Files

A SAT-compliant source archive requires a small set of configuration files that define the archive’s identity, available languages, and metadata defaults. These files live under the `config/` directory inside the archive root and allow tools, generators, and plugins to operate consistently across the entire project.

Create the following three files inside:

```bash
$ARCHIVE_ROOT/config/
```

### archive.yml

```bash
nano $ARCHIVE_ROOT/config/archive.yml
```



This file defines the identity of the archive, the canonical language, and the plugins or structural rules that apply across the project.

```yaml
version: "0.1.0"

archive:
manually-creating-universal-cake-source-archiveid: "universalcake.com"
manually-creating-universal-cake-source-archivelabel: "Universal Cake Source Archive"
manually-creating-universal-cake-source-archivecanonical_language: "en-ca"
manually-creating-universal-cake-source-archivedescription: "Primary SAT archive for the Universal Cake website."

structure:
manually-creating-universal-cake-source-archivepara_enabled: true
manually-creating-universal-cake-source-archivedocs_root: "docs"
manually-creating-universal-cake-source-archivelanguage_roots:
manually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archive- "en-ca"

plugins:
manually-creating-universal-cake-source-archiveenabled:
manually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archive- "metadata.dublin-core"
manually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archive- "language"
manually-creating-universal-cake-source-archivesearch_paths:
manually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archive- "tools/plugins"
```


Confirmation:

```bash
cat $ARCHIVE_ROOT/config/metadata.yml
```

### languages.yml

```bash
nano $ARCHIVE_ROOT/config/languages.yml
```

The languages file defines the language and locale roots available in the archive. For the initial version of the archive, only the canonical `en-ca` root is required.

```yaml
version: "0.1.0"

languages:
manually-creating-universal-cake-source-archive- bcp_47_tag: "en-CA"
manually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archiveslug: "en-ca"
manually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archivename: "English (Canada)"
manually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archivecanonical: true
manually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archivedefault_for_archive: true
```

Confirmation:

```bash
cat $ARCHIVE_ROOT/config/languages.yml
```

Additional language definitions may be added later as the project expands.

### metadata.yml

```bash
nano $ARCHIVE_ROOT/config/metadata.yml
```

This file provides default metadata values for all documents created in the archive. Required fields are explicitly marked, and auto-populated placeholders allow tools to insert appropriate values at creation time.

```yaml
version: "0.1.0"

defaults:
manually-creating-universal-cake-source-archiveTitle: "__REQUIRED_TITLE__"
manually-creating-universal-cake-source-archiveDescription: "__REQUIRED_DESCRIPTION__"
manually-creating-universal-cake-source-archiveAuthor: "Christopher Steel"
manually-creating-universal-cake-source-archiveLicense: "CC BY-SA 4.0"

manually-creating-universal-cake-source-archiveDate: "__AUTO_TODAY__"
manually-creating-universal-cake-source-archiveLast_Modified_Date: "__AUTO_TODAY__"

manually-creating-universal-cake-source-archiveTags: []
manually-creating-universal-cake-source-archiveKeywords: []

manually-creating-universal-cake-source-archiveURL: "__AUTO_FROM_PATH__"
manually-creating-universal-cake-source-archivePath: "__AUTO_FROM_FILENAME__"
manually-creating-universal-cake-source-archiveCanonical: "__AUTO_FROM_URL__"
manually-creating-universal-cake-source-archiveSitemap: "true"

manually-creating-universal-cake-source-archiveDC_Title: "__REQUIRED_TITLE__"
manually-creating-universal-cake-source-archiveDC_Creator: "Christopher Steel"
manually-creating-universal-cake-source-archiveDC_Subject: "__REQUIRED_SUBJECT__"
manually-creating-universal-cake-source-archiveDC_Description: "__REQUIRED_DESCRIPTION__"
manually-creating-universal-cake-source-archiveDC_Language: "en"
manually-creating-universal-cake-source-archiveDC_License: "https://creativecommons.org/licenses/by-sa/4.0/"

manually-creating-universal-cake-source-archiveOG_Title: "__REQUIRED_TITLE__"
manually-creating-universal-cake-source-archiveOG_Description: "__REQUIRED_DESCRIPTION__"
manually-creating-universal-cake-source-archiveOG_URL: "__AUTO_FROM_URL__"
manually-creating-universal-cake-source-archiveOG_Image: ""

manually-creating-universal-cake-source-archiveSchema:
manually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archive"@context": "https://schema.org"
manually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archive"@type": "Article"
manually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archive"inLanguage": "en-CA"
manually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archive"author":
manually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archive"@type": "Person"
manually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archive"name": "Christopher Steel"
manually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archive"contributor":
manually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archive"@type": "Organization"
manually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archivemanually-creating-universal-cake-source-archive"name": "ChatGPT-5 (OpenAI)"

manually-creating-universal-cake-source-archiveVideo_Metadata: {}

required_keys:
manually-creating-universal-cake-source-archive- "Title"
manually-creating-universal-cake-source-archive- "Description"
manually-creating-universal-cake-source-archive- "DC_Subject"
manually-creating-universal-cake-source-archive- "DC_Description"
```

Confirmation:

```bash
cat $ARCHIVE_ROOT/config/metadata.yml
```



With these three files in place, the archive has enough information for SAT tools and plugins to reason about structure, metadata, and language. This completes the foundational setup required before adding initial documents to the system.

## Initialize the Canonical Language Root

SAT archives use a language-rooted directory model. Each language or locale is represented by its own top-level subtree. For this archive, the canonical and only language is `en-ca`.

Create the canonical language root:

```bash
mkdir -p "$ARCHIVE_ROOT"/en-ca/{projects,areas,resources,archives}
```

Resulting structure:

```text
en-ca/
manually-creating-universal-cake-source-archiveprojects/
manually-creating-universal-cake-source-archiveareas/
manually-creating-universal-cake-source-archiveresources/
manually-creating-universal-cake-source-archivearchives/
```

The canonical language is also declared in `config/languages.yml` using:

```yaml
slug: "en-ca"
canonical: true
```

This ensures that SAT tools recognize `en-ca` as the default location for new documents and future PARA structures.

## Understanding the PARA Taxonomy

The Universal Cake source archive uses the PARA taxonomy to organize documents within each language root. To avoid ambiguity with global SAT terms (such as `ARCHIVE_ROOT`), each PARA directory is expressed using a taxonomy-prefixed SAT vocabulary term:

- `para_project_root`
- `para_area_root`
- `para_resource_root`
- `para_archive_root`

These prefixed terms clearly identify each directory as part of the PARA taxonomy rather than part of the global archive structure. The following sections describe the purpose of each PARA root and the criteria for deciding where a document belongs.

### para_project_root

Mapped to:

```text
en-ca/projects/
```

The `para_project_root` contains project directories. A project is a time-bounded effort with a specific outcome or deliverable. A project ends when its objective is achieved.

A document belongs under `para_project_root` if it:

- supports an effort with a defined outcomemanually-creating-universal-cake-source-archive
- contributes to a deliverable or milestonemanually-creating-universal-cake-source-archive
- has a clear completion statemanually-creating-universal-cake-source-archive
- tracks work that ends when the goal is metmanually-creating-universal-cake-source-archive

Examples:manually-creating-universal-cake-source-archive
- Creating the initial Universal Cake websitemanually-creating-universal-cake-source-archive
- Building the metadata plugin MVPmanually-creating-universal-cake-source-archive
- Designing the taxonomy pluginmanually-creating-universal-cake-source-archive

### para_area_root

Mapped to:

```text
en-ca/areas/
```

The `para_area_root` contains ongoing domains of responsibility that require continuous maintenance. Areas have no defined endpoint; they represent active stewardship.

A document belongs under `para_area_root` if it:

- describes ongoing or recurring workmanually-creating-universal-cake-source-archive
- maintains a standard, practice, or responsibilitymanually-creating-universal-cake-source-archive
- persists beyond individual projectsmanually-creating-universal-cake-source-archive
- documents operational or long-term functionsmanually-creating-universal-cake-source-archive

Examples:manually-creating-universal-cake-source-archive
- Accessibility and inclusive design practicesmanually-creating-universal-cake-source-archive
- Archive maintenance proceduresmanually-creating-universal-cake-source-archive
- Style guidelines and content governancemanually-creating-universal-cake-source-archive

### para_resource_root

Mapped to:

```text
en-ca/resources/
```

The `para_resource_root` contains reusable knowledge, reference materials, and documents that support both projects and areas. These documents are evergreen and not tied to a single initiative.

A document belongs under `para_resource_root` if it:

- explains or teaches somethingmanually-creating-universal-cake-source-archive
- is intended for reuse across the archivemanually-creating-universal-cake-source-archive
- serves as documentation, research, or guidancemanually-creating-universal-cake-source-archive
- is not specific to one project or areamanually-creating-universal-cake-source-archive

Examples:manually-creating-universal-cake-source-archive
- SAT Structure Vocabularymanually-creating-universal-cake-source-archive
- Writing guidelinesmanually-creating-universal-cake-source-archive
- Technical design notesmanually-creating-universal-cake-source-archive
- Research summariesmanually-creating-universal-cake-source-archive

### para_archive_root

Mapped to:

```text
en-ca/archives/
```

The `para_archive_root` contains completed, inactive, or historical documents preserved for reference. Items move here when they are no longer actively maintained.

A document belongs under `para_archive_root` if it:

- comes from a completed or retired projectmanually-creating-universal-cake-source-archive
- represents an older standard or deprecated approachmanually-creating-universal-cake-source-archive
- is no longer updated but still valuable historicallymanually-creating-universal-cake-source-archive
- provides provenance, insight, or context for past decisionsmanually-creating-universal-cake-source-archive

Examples:manually-creating-universal-cake-source-archive
- Completed project deliverablesmanually-creating-universal-cake-source-archive
- Superseded versions of policiesmanually-creating-universal-cake-source-archive
- Legacy documentationmanually-creating-universal-cake-source-archive

Understanding the PARA taxonomy ensures that every document is placed intentionally, supports the archive’s long-term clarity, and allows SAT tools and plugins to reason about structure in a predictable and consistent way.

## Next steps

Create the First Document


## License

This document, *Manually Creating a New Universal Cake Source Archive: Project Root, Archive Root, and Initial Directory Layout*, by **Christopher Steel**, with AI assistance from **ChatGPT-5 (OpenAI)**, is licensed under the [Creative Commons Attribution-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/).

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)
