---
Title: "Version Management Strategy for the Source-Archive-Tools Ecosystem"
Description: "A self-contained guide explaining how to check, bump, and maintain version numbers for the source-archive-tools project using both a VERSION file and Git tags."
Author: "Christopher Steel"
Date: "2025-11-25"
Last_Modified_Date: "2025-11-25"
License: "CC BY-SA 4.0"
Version: "1.0.0"
Tags:
  - "versioning"
  - "source-archive-tools"
  - "sovereign-archives"
  - "development"
  - "tooling"
Keywords:
  - "Git"
  - "semantic-versioning"
  - "manifest"
  - "version-file"
  - "archive-tools"
URL: "https://universalcake.com/tools/docs/develop/version-management-strategy"
Path: "tools/docs/develop/version-management-strategy.md"
Canonical: "https://universalcake.com/tools/docs/develop/version-management-strategy"
Sitemap: "true"
DC_Title: "Version Management Strategy for the Source-Archive-Tools Ecosystem"
DC_Creator: "Christopher Steel"
DC_Subject: "Versioning practices for source-archive-tools"
DC_Description: "A guide to inspecting and bumping versions in the source-archive-tools ecosystem using a VERSION file and Git tags."
DC_Language: "en"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
OG_Title: "Version Management Strategy for Source-Archive-Tools"
OG_Description: "How to consistently check, bump, and manage versions in the source-archive-tools ecosystem."
OG_URL: "https://universalcake.com/tools/docs/develop/version-management-strategy"
Schema:
  "@context": "https://schema.org"
  "@type": "TechArticle"
  "name": "Version Management Strategy for the Source-Archive-Tools Ecosystem"
  "description": "A clear workflow for using a VERSION file and Git tags to manage versions of source-archive-tools."
  "author": "Christopher Steel"
  "contributor": "ChatGPT-5.1 (OpenAI)"
Video_Metadata: {}
---

# Version Management Strategy for the Source-Archive-Tools Ecosystem

This document describes the recommended method for managing versions of the **source-archive-tools** project. It ensures that:

- Each release has a **canonical version number**,  
- Archives can record the exact tools version they were created with,  
- Developers can reliably bump versions without hidden state.

The approach uses two synchronized mechanisms:

- A **`VERSION` file** stored at the root of the tools repository  
- A **Git tag** with the same value (e.g., `v0.2.0`)

Together, these provide traceability, reproducibility, and long-term stability for the Sovereign Archive Toolkit (sat).

# Where the Version Lives

Every source-archive-tools checkout should contain:

```
source-archive-tools/
  VERSION
```

The `VERSION` file contains a single line, such as:

```
0.1.0
```

This file is:

- Human-readable  
- Script-friendly  
- Always available even without Git  
- Used directly when generating `tools_manifest.yml` inside new archives

# Checking the Current Version

To inspect the current version, use both the file and the Git tag system.

## Check the file value

```bash
cat VERSION
```

## Check the latest Git tag (if tags exist)

```bash
git describe --tags --abbrev=0
```

If no tags exist yet, Git will return an error—that simply means you haven’t tagged anything yet.

# Bumping the Version

When preparing a new tools release, follow this workflow.

## Step 1: Edit the VERSION file

Open and modify:

```
VERSION
```

Set it to the next semantic version, for example:

```
0.2.0
```

## Step 2: Commit the change

```bash
git add VERSION
git add .
git commit -m "Bump source-archive-tools version to 0.2.0"
```

## Step 3: Tag the release

```bash
git tag v0.2.0
```

## Step 4: Push repository and tags

```bash
git push
git push --tags
```

At this point:

- `VERSION` contains the authoritative version number.
- A Git tag marks the corresponding commit.
- Archives can embed this version inside their `config/tools_manifest.yml`.

# Using the Version in New Archives

When initializing a new archive, the init script should read the `VERSION` file:

```bash
TOOLS_VERSION=$(cat VERSION)
```

And write it into:

```
config/tools_manifest.yml
```

As:

```yaml
runtime:
  tools_version: "0.2.0"
```

This ensures every archive is **born** with a permanent record of the exact tools version used during creation.

# Why Use Both a VERSION File and Git Tags?

Using both patterns provides several benefits:

- The `VERSION` file is visible offline, in packaged tarballs, or when browsing archives.
- Git tags enable:
  - Easy reproduction of specific tool versions
  - Clean upgrade paths
  - Automated release tooling
- The version always stays in sync across:
  - Human-readable file  
  - Git-native repository metadata  
  - Archive manifests  

This is especially important for long-lived archives and sovereign maintenance workflows.

# Summary

The recommended version management flow is:

1. Maintain a plain `VERSION` file in the repository root.  
2. Create a matching Git tag for every version bump.  
3. Store the version inside each archive’s `tools_manifest.yml`.  
4. Use the combination of file + tag to ensure reproducibility and stable upgrades.

This method is simple, durable, scripting-friendly, and aligned with the long-term vision of source archives as sovereign, self-maintaining knowledge vessels.

# License

This document, *Version Management Strategy for the Source-Archive-Tools Ecosystem*, by **Christopher Steel**, with AI assistance from **ChatGPT-5.1 (OpenAI)**, is licensed under the [Creative Commons Attribution-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/).

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)