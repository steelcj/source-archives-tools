---
Title: ""
Description: "Defines a Git ignore pattern for excluding all SAT archives by default while explicitly including a designated testing archive."
Author: "Christopher Steel"
License: "CC BY-SA 4.0"
---

# Selective Inclusion of Archives in Git Repositories

## Purpose

This document defines a **safe and explicit Git strategy** for SAT repositories where:

- Multiple archives may exist under a common `archives/` directory
- Most archives are **local, private, or environment-specific**
- A single archive (e.g. `testing`) is intentionally tracked and shared

The goal is to prevent accidental inclusion of authoritative or private archives while preserving a reproducible testing archive.

---

## Design Principle

SAT follows a strict principle of **explicit authority**:

> Archives are ignored by default and only included when intentionally opted in.

Git behavior must reinforce this rule.

---

## Required `.gitignore` Rules

To ignore **all archives** under `archives/` *except* the `testing` archive, use the following rules **in this order**:

```gitignore
# Ignore all archives by default
archives/*

# Allow the testing archive directory
!archives/testing/

# Allow all contents inside the testing archive
!archives/testing/**
```

---

## Why This Works

Git applies ignore rules **top to bottom**.

1. `archives/*`  
   Ignores every immediate child directory of `archives/`

2. `!archives/testing/`  
   Re-includes the `testing` directory itself

3. `!archives/testing/**`  
   Re-includes all files and subdirectories within `testing`

Git cannot track files inside an ignored directory unless the directory itself is explicitly un-ignored.  
Both negation rules are required.

---

## Optional: Keep the `archives/` Directory Present

If you want the `archives/` directory to exist in the repository even when empty, add:

```gitignore
!archives/.gitkeep
```

Then commit an empty file at:

```
archives/.gitkeep
```

This is optional and purely structural.

---

## SAT-Specific Recommendation

For clarity and long-term maintainability, include intent-revealing comments:

```gitignore
# --------------------------------------------------
# SAT archives
# Track only the testing archive; others are local
# --------------------------------------------------
archives/*
!archives/testing/
!archives/testing/**
```

This helps future contributors understand *why* archives are excluded.

---

## What This Prevents

- Accidental publication of private archives
- Silent coupling between environments
- Repository bloat
- Ambiguous source-of-truth boundaries

---

## One-Sentence Rule

> Ignore entire archive trees by default; explicitly opt in the archives meant to be shared.

This rule aligns Git behavior with SAT’s architectural boundaries.

---

## License

This document is licensed under the  
**Creative Commons Attribution-ShareAlike 4.0 International License (CC BY-SA 4.0)**.