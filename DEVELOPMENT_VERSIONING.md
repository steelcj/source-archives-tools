# SAT Development Versioning Policy

This document defines **how SAT developers must handle versioning during active development**, including how to save unfinished work, introduce experimental features, and decide when to bump versions.

This policy exists to prevent **version inflation**, **silent contract changes**, and **accidental user breakage**.

Versions in SAT describe **user-facing guarantees**, not internal progress.

## Assumptions

It is written as a **working contract for contributors**, not marketing copy.

This document assumes SAT is currently **`1.0.0`** and explicitly supports unfinished, experimental work **without corrupting version meaning**.

## Current Baseline

- SAT is currently at version **1.0.0**
- Version **1.0.0** represents a **stable, minimal, finished contract**
- All future work must preserve the integrity of this contract unless a version bump explicitly declares otherwise

---

## Core Rule

> **If a feature is not ready to be enabled by default, it must not affect the version number.**

Unfinished work must be **explicitly gated**, **isolated**, or **kept off release branches**.

---

## What Counts as “User-Facing”

A change is considered user-facing if it:

- Changes default behavior
- Changes archive interpretation
- Changes validation rules
- Changes outputs
- Changes error conditions
- Introduces new required configuration
- Alters directory expectations

If a change is user-facing, it **must** be reflected in versioning.

---

## How to Save Unfinished Work Safely

Developers are encouraged to commit incomplete work using **one of the approved containment mechanisms** below.

### 1. Feature Flags (Preferred)

Unfinished features must be gated behind **explicit, off-by-default feature flags**.

Example:

```yaml
experimental:
  enable_sat_tree_v2: false
  enable_plugin_registry: false
~~~

Rules:

- Feature flags must default to `false`
- Feature flags must be explicitly named as `experimental`
- No behavior may change unless the flag is enabled
- Flags must not be required for normal workflows
- Flags must be documented as unstable or undocumented

Using feature flags does **not** require a version bump.

------

### 2. Experimental Tool Namespace

Unfinished tools may be introduced using a clearly experimental name.

Examples:

```
sat-experimental-tree
sat-dev-index
```

Rules:

- Experimental tools must not be referenced in primary documentation
- Experimental tools may change or disappear without notice
- Experimental tools must not be installed or invoked by default
- Experimental tools may break compatibility at any time

Experimental tools do **not** affect version numbers.

------

### 3. Development Branches

Long-lived development branches are encouraged.

Suggested structure:

```
main        → stable, tagged releases only
dev         → integrated experimental work
feature/*   → isolated feature development
```

Rules:

- Only `main` may receive version tags
- `dev` may contain breaking or unfinished work
- Features must be stabilized before merging to `main`

------

### 4. Internal Schema Versions (Optional)

Developers may use internal-only schema or state versions.

Example:

```yaml
_internal_schema_version: "0.3"
```

Rules:

- Internal versions must not appear in user documentation
- Internal versions must not be required
- Internal versions must not be interpreted automatically
- Internal versions must not replace SAT or schema versions

------

## Version Bump Rules

### PATCH Releases (`1.0.Z`)

Allowed when:

- Fixing bugs
- Improving error handling
- Improving diagnostics or logging
- Refactoring without behavior change
- Documentation fixes

PATCH releases must not introduce new features or behavior.

------

### MINOR Releases (`1.Y.0`)

Allowed only when a feature is:

- Complete
- Documented
- Enabled by default
- Backwards compatible
- Safe to ignore by existing users

If a feature requires a feature flag, it is **not eligible** for a MINOR bump.

------

### MAJOR Releases (`X.0.0`)

Required when:

- Archive interpretation changes
- Config schema changes in a breaking way
- Defaults change meaningfully
- Validation rules become stricter in incompatible ways
- Migration may be required
- Existing archives may be rejected

MAJOR releases must be deliberate and rare.

------

## Forbidden Practices

The following are not allowed:

- Bumping versions to “save progress”
- Shipping unfinished behavior without gating
- Changing defaults silently
- Introducing undocumented required fields
- Using version numbers as internal bookmarks
- Treating `main` as a scratch branch

------

## Developer Checklist Before Merging to `main`

Before merging any change into `main`, ask:

1. Does this change default behavior?
2. Does this change archive interpretation?
3. Does this require new configuration?
4. Does this surprise users?
5. Does this break old assumptions?

If **any answer is yes**, the change must:

- be gated,
- delayed,
- or paired with an appropriate version bump.

------

## Relationship to VERSIONING.md

This document governs **developer behavior**.

The public-facing rules and guarantees are defined in:

```
VERSIONING.md
```

If these two documents conflict, **VERSIONING.md takes precedence**.

------

## Guiding Principle

> **SAT versions are promises to users.
> Development progress lives elsewhere.**

