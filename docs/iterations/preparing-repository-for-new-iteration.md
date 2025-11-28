---
Title: "Preparing the Repository for a New Iteration (source-archive-tools)"
Description: "A complete, unified guide for preparing the source-archive-tools repository before beginning any new iteration, including standard workflow steps, clean-slate resets, tagging, and version declaration."
Author: "Christopher Steel"
Date: "2025-11-27"
Last_Modified_Date: "2025-11-27"
License: "CC BY-SA 4.0"
Version: "1.1.0"
Tags:
  - "source-archive-tools"
  - "git-workflow"
  - "iteration-management"
  - "versioning"
  - "repository-preparation"
Keywords:
  - "iteration"
  - "git"
  - "version-control"
  - "workflow"
  - "repository-hygiene"
URL: "https://github.com/steelcj/source-archives-tools/blob/main/tools/docs/iterations/preparing-repository-for-new-iteration.md"
Path: "tools/docs/iterations/preparing-repository-for-new-iteration.md"
Canonical: "https://github.com/steelcj/source-archives-tools/blob/main/tools/docs/iterations/preparing-repository-for-new-iteration.md"
Sitemap: "false"
DC_Title: "Preparing the Repository for a New Iteration (source-archive-tools)"
DC_Creator: "Christopher Steel"
DC_Subject: "Unified workflow for preparing the source-archive-tools repository before starting a new iteration"
DC_Description: "This document provides a complete workflow for preparing the source-archive-tools repository for a new iteration, including clean states, commits, tagging, clean-slate resets, and version declarations."
DC_Language: "en"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
DC_Contributor: "ChatGPT-5 (OpenAI)"
DC_RightsHolder: "Christopher Steel"
OG_Title: "Preparing the Repository for a New Iteration (source-archive-tools)"
OG_Description: "A unified workflow for preparing the source-archive-tools repository before beginning a new iteration."
OG_URL: "https://github.com/steelcj/source-archives-tools/blob/main/tools/docs/iterations/preparing-repository-for-new-iteration.md"
OG_Image: ""
Schema:
  "@context": "https://schema.org"
  "@type": "TechArticle"
  "headline": "Preparing the Repository for a New Iteration (source-archive-tools)"
  "author": "Christopher Steel"
  "inLanguage": "en"
  "license": "https://creativecommons.org/licenses/by-sa/4.0/"
  "contributor": "ChatGPT-5 (OpenAI)"
Video_Metadata: ""
---

# Preparing the Source-Archive-Tools Repository for a New Iteration

This unified document provides a complete workflow for preparing the `source-archive-tools` repository before beginning a new iteration. It includes:

- the **standard iteration-preparation workflow** used between normal versions  
- the **clean-slate reset workflow** used when starting a new architecture (e.g., 0.0.4)  

This guide is now the authoritative reference for all future iteration boundaries.

# Standard Pre-Iteration Preparation

This workflow applies to **every new iteration**, unless you are deliberately performing a clean-slate reset.

## Confirm you are in the correct repository

```bash
pwd
```

Verify that this is the correct working copy of `source-archive-tools`.

## Check the current repository status

```bash
git status
```

This shows:

- the current branch  
- whether your branch is ahead/behind  
- staged or unstaged changes  
- untracked files  

If the output shows:

```text
nothing to commit, working tree clean
```

you may skip ahead to verifying the `VERSION` file.

## Review what has changed

If changes are present, inspect a concise summary:

```bash
git diff --stat
```

This helps confirm that all changes are understood and expected.

## Stage all outstanding changes

```bash
git add -A
```

This ensures:

- new files are staged  
- modified files are staged  
- **deleted files are also staged** (unlike `git add .`)  
- the index matches the working tree exactly  

## Confirm what is staged

```bash
git status
```

Review everything under “Changes to be committed”.

If anything was staged accidentally:

```bash
git restore --staged <file>
```

## Commit the final state of the previous iteration

```bash
git commit -m "Describe the final state of the previous iteration"
```

Use a clear message, such as:

```text
"Finalize iteration 0.0.3 prior to clean-slate reset"
```

## Push the final state to the remote

```bash
git push
```

This synchronizes the remote with the final state of the iteration.

# Verify and Tag the Completed Iteration

## Inspect the VERSION file

```bash
cat VERSION
```

Ensure it reflects the completed version (example: `0.0.3`).

If missing or incorrect:

```bash
echo "0.0.3" > VERSION
git add VERSION
git commit -m "Set VERSION to 0.0.3 for completed iteration"
git push
```

## Create a version tag

```bash
git tag v0.0.3
git push --tags
```

This marks the exact commit where the iteration ended.

This concludes the **standard preparation workflow**.

# Clean-Slate Reset Workflow (Full Structure Reset)

Use this workflow **only when replacing or rebuilding the entire architecture**.  
This was used to begin **version 0.0.4**.

## Create a clean-slate by archiving all existing files

```bash
mkdir artifacts
mv * artifacts/.
ls -al
git status
git add .
git commit -m 'moved entire project to artifacts dir'
git push
git status
```

## Interpretation

- `artifacts/` now contains the entire previous architecture.  
- The root directory is now empty (except for `.git` and hidden files).  
- This root will become the home of the **new 0.0.4 architecture**.

## Result

The repository root is now:

- empty  
- clean  
- ready for new design  

This state marks the beginning of the next major version.

# Declare the New Version (0.0.4)

After the clean-slate reset, explicitly define the new version.

## Set the new version

```bash
echo "0.0.4" > VERSION
git add VERSION
git commit -m "Set VERSION to 0.0.4 for new clean-slate iteration"
git push
```

The project is now officially at **0.0.4**, and the clean-slate state is the anchor commit for this version.

# What Happens Next

After completing the steps in this guide, the repository is ready for:

- designing the **new 0.0.4 directory layout**  
- initializing **tools/** and **plugins/**  
- defining the new **iteration plan**  
- implementing the new architecture  

These tasks begin immediately after the clean-slate + version declaration steps.

## License

This document, *Preparing the Source-Archive-Tools Repository for a New Iteration*, by **Christopher Steel**, with AI assistance from **ChatGPT-5 (OpenAI)**, is licensed under the Creative Commons Attribution-ShareAlike 4.0 License.

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)
