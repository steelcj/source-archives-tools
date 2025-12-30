---
Title: "Licensing Boundaries in SAT: Code, Documentation, and Outputs"
Description: "Explains why SAT code and documentation may share values but require different licenses, and how licensing boundaries are intentionally preserved."
Author: "Christopher Steel"
Date: "2025-12-29"
License: "CC BY-SA 4.0"
Tags:
  - "licensing"
  - "copyright"
  - "architecture"
  - "documentation"
Path: "docs/resources/licensing/licensing-code-and-documents.md"
Canonical: "resources/licensing/licensing-code-and-documents"
Slug: "licensing-boundaries-code-docs-outputs"
---

# Licensing Boundaries in SAT: Code, Documentation, and Outputs

This document explains how **Source Archive Tools (SAT)** applies licensing across different kinds of artifacts, and why those licenses are intentionally **aligned in values but separated in scope**.

The goal is to preserve freedom, clarity, and long-term sustainability without creating unnecessary legal or practical friction.

---

## Core Principle

> **Licenses should match the nature of the artifact, not ideology alone.**

SAT is designed around openness and user agency, but different artifacts require different legal tools to express those values correctly.

---

## Code and Documentation Are Separate Works

Although SAT code and SAT documentation are closely related, they are **distinct copyrightable works**.

This means:
- They can be licensed differently
- They should be licensed differently
- Doing so is standard, not exceptional

Conflating the two often leads to confusion, especially for reuse, teaching, and redistribution.

---

## SAT Code

SAT source code is licensed under the **GNU General Public License (GPL)**.

This is intentional.

The GPL is well-suited for:
- Executable software
- Source code modification
- Strong copyleft guarantees
- Preventing proprietary enclosure of tooling

It ensures that improvements to SAT itself remain free and auditable.

---

## SAT Documentation

SAT documentation is licensed under **Creative Commons Attribution–ShareAlike 4.0 (CC BY-SA 4.0)**.

This choice reflects the nature of documentation as:
- Human-readable
- Educational
- Explanatory
- Often reused outside the original codebase

CC BY-SA:
- Preserves attribution
- Enforces share-alike principles similar to GPL
- Avoids ambiguity around concepts like “linking”
- Works cleanly with static sites, wikis, and teaching materials

Structurally and ethically, this mirrors the spirit of GPL without imposing software-oriented constraints on text.

---

## Structural Alignment Without Legal Coupling

Although the licenses differ, SAT code and documentation are intentionally aligned in practice:

- Transparency is expected everywhere
- Forkability is encouraged
- Hidden constraints are avoided
- Provenance and authorship are explicit

The difference is **legal precision**, not philosophical divergence.

---

## Generated Outputs

SAT-generated archives and outputs are treated as a **third, independent layer**.

Key rule:
- **SAT does not impose a license on generated outputs unless explicitly configured to do so.**

This preserves:
- User agency
- Project-specific licensing needs
- Compatibility with institutional, academic, or private archives

Licensing of outputs must be declared intentionally, not inherited implicitly.

---

## Summary Model

SAT operates with three clear licensing layers:

- **Code**  
  GPL — strong copyleft for executable tooling

- **Documentation**  
  CC BY-SA 4.0 — share-alike for knowledge and explanation

- **Outputs**  
  Explicitly defined by the archive or project

This separation is a feature, not a compromise.

---

## Why This Matters

Clear licensing boundaries:
- Reduce ambiguity for contributors
- Prevent accidental license violations
- Enable reuse without fear
- Support SAT’s long-term credibility and adoption

Most importantly, they respect the autonomy of both developers and archive owners.

---

## License

This document, *Licensing Boundaries in SAT: Code, Documentation, and Outputs*, by **Christopher Steel**, with AI assistance from **ChatGPT-4 (OpenAI)**, is licensed under the [Creative Commons Attribution-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/).

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)