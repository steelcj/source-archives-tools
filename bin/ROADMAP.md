# ROADMAP.md

## Description

Sat tools work on three primary things:

* SAT tools
  * it has it's own documentation archive
* Archives
  * only SAT connected archives
* Content in archives

## SAT Tools

*(Tools for SAT itself)*

### Purpose

These tools define, validate, and reason about **SAT as a system**, independent of any specific archive or content.

They answer questions like:

- “Is this a valid SAT archive?”
- “Does this archive conform to the SAT schema?”
- “What version of SAT is this archive expecting?”

### Characteristics

- **Archive-agnostic**
- **Content-agnostic**
- Operate on **SAT concepts**, not user meaning
- Enforce *identity, structure, and invariants*

### Typical Inputs

- SAT config files
- SAT manifests
- Schema versions
- Tooling metadata

### Typical Outputs

- Validation results
- Expected structure
- Errors about incompatibility or misuse

### Examples

- `sat-init-archive`
- `sat-tree`
- `sat-validate`
- `sat-version`
- `sat-doctor`

### Hard Rule

> SAT core tools **never interpret content meaning** and **never modify content**.

They establish the *rules of the game*, not the gameplay.

## Archive Tools

*(Tools for archives as containers)*

### Purpose

These tools operate **within a specific archive**, managing its structure, organization, and metadata *as an archive*, not as authored content.

They answer questions like:

- “Is this archive internally consistent?”
- “How is this archive organized?”
- “What languages, PARA roots, or taxonomies exist here?”

### Characteristics

- **Archive-aware**
- **Content-light**
- Concerned with *organization, not meaning*
- May read archive-local configuration

### Typical Inputs

- Archive root
- Archive-local config
- Archive metadata sidecars
- Directory structure

### Typical Outputs

- Structural changes
- Metadata scaffolding
- Reports about archive health or completeness

### Examples

- `sat-archive-audit`
- `sat-archive-lint`
- `sat-archive-normalize`
- `sat-archive-migrate`
- `sat-archive-stats`

### Hard Rule

> Archive tools may **touch content files**, but only structurally or mechanically—never semantically.

They rearrange shelves; they do not rewrite books.

------

## Content Tools

*(Tools for content itself)*

### Purpose

These tools operate at the **content level**, assisting humans with authoring, transforming, validating, or enriching content.

They answer questions like:

- “Is this document well-described?”
- “Can this content be transformed for output?”
- “What metadata is missing or inconsistent?”

### Characteristics

- **Content-aware**
- Often **language- and domain-sensitive**
- Human-facing
- May be opinionated or configurable

### Typical Inputs

- Markdown files
- Media assets
- Sidecar metadata
- Front matter

### Typical Outputs

- Enriched content
- Generated metadata
- Reports, previews, exports

### Examples

- `sat-content-metadata`
- `sat-content-lint`
- `sat-content-export`
- `sat-content-translate`
- `sat-content-preview`

### Hard Rule

> Content tools must **never assume archive-wide authority** unless explicitly instructed.

They work on *what you point at*, not the whole system.

## Why This Division Matters (Critically)

This separation gives you:

- **Clear blast-radius control**
- **Predictable behavior**
- **Composable pipelines**
- **Permission-aware tooling**
- **Future plugin clarity**

It also maps cleanly onto your earlier principle:

> *“Nothing influences SAT behavior unless a tool is explicitly told to read it.”*

Each class knows **what it is allowed to read**, **what it is allowed to change**, and **what it must never infer**.

## Suggested Directory Reflection (Optional, but powerful)

If you choose to reflect this in layout later:

```
bin/
  sat/           # Core SAT tools
  archive/       # Archive-level tools
  content/       # Content-level tools
```

Or via naming convention alone:

- `sat-*`
- `sat-archive-*`
- `sat-content-*`

Both approaches reinforce the mental model without enforcing it prematurely.

## One-Sentence Summary (Worth Writing Down)

> **SAT tools define the rules, archive tools manage containers, and content tools help humans work with meaning.**

If you want, next we can:

- Formalize this as a **README contract**
- Define **cross-layer interaction rules**
- Or map existing tools into this taxonomy to spot gaps or misplacements