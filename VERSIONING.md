# SAT Versioning Policy

This document defines **when and how SAT versions are bumped**, and what each version change means for users, archives, and tools.

SAT versioning exists to protect **archive integrity, behavioral guarantees, and user trust**.  
Versions describe **contracts**, not development speed.

SAT follows **Semantic Versioning (MAJOR.MINOR.PATCH)** with **stricter rules** than typical software projects.

---

## Version Format

SAT versions use the following format:
```

MAJOR.MINOR.PATCH

```
Example:
```

1.2.0

```
Each component has a strict and non-negotiable meaning.

---

## PATCH Releases — `x.y.Z`

**Bug fixes only. No behavioral change.**

### When to bump PATCH

Bump PATCH when changes include only:

- Bug fixes
- Error message corrections
- Logging or diagnostic improvements
- Documentation fixes that do not change meaning
- Performance optimizations that do not change outputs
- Crash fixes or incorrect failure handling

### What PATCH must not do

A PATCH release must **never**:

- Change directory structures
- Change configuration schemas
- Change defaults
- Change validation rules
- Change tool behavior
- Introduce new features

### Guiding rule

> If a user reruns the same command and only notices that “it works better,” the change is PATCH.

---

## MINOR Releases — `x.Y.0`

**New capability, same guarantees.**

### When to bump MINOR

Bump MINOR when adding functionality that does **not** affect existing behavior, such as:

- New SAT tools (`sat-*`)
- New optional configuration fields
- New plugin types
- New command-line flags
- New opt-in validation rules
- New output formats
- Extended behavior that preserves existing outputs unless explicitly enabled

### Required guarantees

A MINOR release must ensure:

- Existing archives continue to work
- Existing configurations continue to validate
- Existing directory structures remain valid
- Existing commands produce the same outputs by default

### Guiding rule

> If users can safely ignore the change, it is MINOR.

---

## MAJOR Releases — `X.0.0`

**Contract break. Archive meaning changes.**

MAJOR releases are **rare and deliberate**. They signal a change in how SAT interprets or enforces meaning.

### When to bump MAJOR

A MAJOR version bump is required if **any** of the following occur:

- Archive identity rules change
- Configuration schema changes in a breaking way
- Directory structure expectations change
- Language or PARA assumptions change
- SAT refuses archives that were previously valid
- Tool behavior changes meaningfully
- Defaults change in a way that alters results
- Safety or validation guarantees are tightened in a breaking way
- Implicit behavior is introduced where none existed before

### Examples of MAJOR changes

- Changing how `archive_identity` is defined or validated
- Changing how language roots are inferred
- Changing how PARA roots are generated
- Making previously optional fields mandatory
- Changing how tools discover or trust configuration files
- Changing archive interpretation logic

### Guiding rule

> If an archive might require migration, the change is MAJOR.

---

## Identity Locking (Critical Invariant)

SAT enforces **identity locking** as a core safety guarantee.

> Once an archive declares a SAT version, SAT must not reinterpret it silently.

### Practical implications

- `sat-init-archive` **writes** the SAT version
- SAT tools **read but never rewrite** the archive’s declared version
- If SAT detects a version mismatch, it must stop with a clear error

Example:
```

Error: SAT identity already exists but version mismatch detected

```
This behavior is **intentional and required**.

---

## Where Versions Live

SAT versions appear in three distinct and authoritative places:

### 1. SAT Tool Version (runtime)

- Embedded in the SAT executable or scripts
- Printed via `--version`
- Governs runtime behavior

### 2. Archive Declared Version

Stored in the archive, typically at:
```

meta/sat.manifest.yml

```
This answers:

> “What SAT rules was this archive created under?”

### 3. Schema Version (optional but recommended)

Example:
```

schema_version: "1.0.0"

```
This answers:

> “What structural rules apply to this configuration or archive?”

These versions are **related but not interchangeable**.

---

## Migration Policy

SAT follows a strict migration policy:

- **PATCH releases** must never require migration
- **MINOR releases** must never require migration
- **MAJOR releases** may require migration and must be explicit

For MAJOR releases, SAT must:

- Detect older archive versions
- Either:
  - refuse to operate with a clear error message, or
  - provide an explicit migration command

SAT must **never auto-migrate** archives.

---

## Version Bump Decision Checklist

Before releasing a version, ask:

1. Does this change how SAT interprets existing archives?
   - Yes → MAJOR
2. Does this add new functionality without affecting old behavior?
   - Yes → MINOR
3. Does this only fix something broken?
   - Yes → PATCH
4. Could this surprise users?
   - Yes → likely MAJOR
5. Could this silently corrupt meaning?
   - If yes, do not release without a MAJOR bump and migration plan

---

## Release Philosophy

SAT favors:

- Stability over speed
- Explicitness over convenience
- Guarantees over growth metrics

Expected cadence:

- PATCH: as needed
- MINOR: when a coherent capability is complete
- MAJOR: only when the mental model or contract changes

SAT should feel **boring, predictable, and trustworthy**.

---

## Guiding Principle

> **SAT versions describe guarantees, not progress.**