---
Title: "Preparing the Source-Archive-Tools Repository for a New Iteration"
Description: "A clear, repeatable sequence of Git commands and checks to ensure the source-archive-tools repository is in a good state before starting a new iteration."
Author: "Christopher Steel"
Date: "2025-11-27"
Last_Modified_Date: "2025-11-27"
License: "CC BY-SA 4.0"
Version: "1.0.0"
Tags:
  - "source-archive-tools"
  - "git-workflow"
  - "mvp-iterations"
  - "versioning"
  - "repository-hygiene"
Keywords:
  - "git"
  - "version-control"
  - "iteration"
  - "repository-preparation"
  - "workflow"
URL: "https://universalcake.com/areas/tools/development/mvp/preparing-repository-for-new-iteration"
Path: "areas/tools/development/mvp/preparing-repository-for-new-iteration.md"
Canonical: "https://universalcake.com/areas/tools/development/mvp/preparing-repository-for-new-iteration"
Sitemap: "true"
DC_Title: "Preparing the Source-Archive-Tools Repository for a New Iteration"
DC_Creator: "Christopher Steel"
DC_Subject: "Practical Git workflow for preparing the source-archive-tools repository before starting a new iteration"
DC_Description: "Step-by-step commands and explanations for ensuring the source-archive-tools repository is clean, versioned, and ready for a new development iteration."
DC_Language: "en"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
DC_Contributor: "ChatGPT-5 (OpenAI)"
DC_RightsHolder: "Christopher Steel"
OG_Title: "Preparing the Source-Archive-Tools Repository for a New Iteration"
OG_Description: "A concrete Git-based checklist for getting the source-archive-tools repository into a known-good state before starting a new iteration."
OG_URL: "https://universalcake.com/areas/tools/development/mvp/preparing-repository-for-new-iteration"
OG_Image: ""
Schema:
  "@context": "https://schema.org"
  "@type": "TechArticle"
  "headline": "Preparing the Source-Archive-Tools Repository for a New Iteration"
  "author": "Christopher Steel"
  "inLanguage": "en"
  "license": "https://creativecommons.org/licenses/by-sa/4.0/"
  "contributor": "ChatGPT-5 (OpenAI)"
Video_Metadata: ""
---

# Preparing the Source-Archive-Tools Repository for a New Iteration

This document defines a small, repeatable sequence of Git commands and checks to ensure the `source-archive-tools` repository is in a good state before starting a new iteration. The focus is on **what you actually type** and **what each command is for**, so the process is clear and easy to follow.

You can use this checklist before any new iteration, regardless of the version number.

## Confirm you are in the correct repository

### Show the current directory

```bash
pwd
```

Use this to confirm that you are in the expected `source-archive-tools` project root.

If it is not the correct path, navigate to the right repository before continuing.

## Inspect the current repository status

### Check the working tree

```bash
git status
```

Use this to see:

- which branch you are on
- whether your branch is up to date with its remote tracking branch
- whether there are uncommitted changes
- whether there are untracked files

If `git status` already shows:

```text
nothing to commit, working tree clean
```

your working tree is clean and you can skip directly to checking the `VERSION` file.

## Review what has changed

If `git status` shows modified, deleted, or untracked files, it is useful to see a summary of what changed before preparing the new iteration.

### Show a summary of differences

```bash
git diff --stat
```

This displays the number of insertions and deletions per file, helping you verify that all changes are expected and belong to the state you want to consider “final” for the current iteration.

If the output includes changes you do not want to keep, revert or adjust them before proceeding.

## Add any outstanding changes to the repository

Once you are satisfied that the differences are intentional and reflect the desired final state of the current iteration, stage everything.

### Stage all changes, including deletions

```bash
git add -A
```

This updates the Git index so it exactly matches the working tree:

- stages all new files  
- stages all modifications  
- stages all deletions  
- ensures nothing in the working tree is left unstaged  

```bash
       -A, --all, --no-ignore-removal
           Update the index not only where the working tree has a file matching <pathspec> but also where the index already
           has an entry. This adds, modifies, and removes index entries to match the working tree.
```

## Confirm what is staged

### Re-check repository status

```bash
git status
```

You should now see your changes listed under “Changes to be committed”. Review the list to confirm that everything staged is expected and nothing important is missing.

If something is staged by mistake, you can unstage it with:

```bash
git restore --staged <file>
```

and adjust as needed.

## Commit the final state of the current iteration

When you are satisfied with what is staged, create a commit that clearly describes the final state of the current iteration.

### Commit the staged changes

```bash
git commit -m "Describe the final state of the previous iteration"
```

Use a message that describes what you just finalized (for example, “Restructure docs before starting next MVP iteration” or similar).

After this commit, the working tree should be clean again.

### Confirm the working tree is clean

```bash
git status
```

You should now see:

```text
nothing to commit, working tree clean
```

This indicates the repository is in a stable, committed state.

## Ensure the VERSION file matches the repository state

The `VERSION` file should reflect the version of the state you are about to tag as “complete” before starting the next iteration.

### Inspect the VERSION file

```bash
cat VERSION
```

If the file exists and contains the correct current version (for example, `0.0.3`), no change is needed.

If the file is missing or incorrect, fix it now.

### Create or update the VERSION file

```bash
echo "<current-version>" > VERSION
git add VERSION
git commit -m "Set VERSION to <current-version> for completed iteration"
```

Replace `<current-version>` with the version you consider “finished” (for example, `0.0.3`). At this point, the repository history and the `VERSION` file should agree about the current version.

## Tag the completed iteration

Once the current iteration is committed and the `VERSION` file is correct, tag the repository so you can always return to this exact state later.

### Create a version tag

```bash
git tag v<current-version>
```

For example:

```bash
git tag v0.0.3
```

### Push tags to the remote

```bash
git push --tags
```

This makes the tag available to anyone else working with the repository and to any tooling that uses tags for releases or comparisons.

## Final readiness check

Before starting a new iteration, run a final check so you know the repository is in a known-good state.

### Confirm clean state and tags

```bash
git status
```

Output example:

```bash
On branch dev
Your branch is ahead of 'origin/dev' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```

### Publish the current state to the remote

If your branch is ahead then:

```bash
git push
```

This sends your latest local commit(s) to `origin/dev` so that:

- the remote branch matches your local branch  
- the final state of the previous iteration is stored on the server  
- anyone else (or any automation) sees the same baseline you are about to iterate from

### git tag --list

```bash
git tag --list
```

output example:

```bash
v0.0.1
v0.0.3
```



You should see:

- a clean working tree
- a tag that matches the `VERSION` file for the completed iteration

At this point:

- the previous iteration is fully committed and tagged  
- the `VERSION` file reflects the completed state  
- there are no uncommitted changes  

The repository is now prepared for a new iteration. The next steps (not covered in this document) typically include:

- creating a new branch for the upcoming iteration  
- bumping the `VERSION` file to the next version number  
- beginning work on the new features or structural changes  

# License

This document, *Preparing the Source-Archive-Tools Repository for a New Iteration*, by **Christopher Steel**, with AI assistance from **ChatGPT-5 (OpenAI)**, is licensed under the Creative Commons Attribution-ShareAlike 4.0 License.

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)