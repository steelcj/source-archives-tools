# SAT Command-Line Tools

This directory contains the **primary command-line tools** for working with
**Source Archive Tools (SAT)** projects.

These tools operate on **SAT Content Archives**, using the SAT Tool Archive
as the source of structure, schema, and defaults.

Each tool is designed to do **one clear job**, to be safe to run from any working
directory, and to operate explicitly on SAT-defined structures.

---

## sat-init-archive

**Purpose:**
Initialize a new **SAT Content Archive** using an existing SAT Tool Archive as the source of truth.

**When to use it:**

- When creating a new SAT Content Archive
- When bootstrapping a project that will be managed with SAT
- Before running other SAT tools against that archive

**What it does:**

- Reads the SAT Tool Archive identity and version
- Creates the minimal required archive directory structure
- Writes:
  - `config/archive.yml`
  - `meta/archive.manifest.yml`

This is typically the **first SAT command** used with a new archive.

---

## sat-plugin-discovery

**Purpose:**
Discover SAT plugins and resolve the configuration they collectively declare.

**When to use it:**

- After initializing an archive
- After adding, updating, or modifying SAT plugins
- When regenerating `config/archive.yml` deterministically

**What it does:**

- Discovers available SAT plugins under `plugins/`
- Loads plugin-declared configuration defaults
- Resolves and deep-merges those defaults
- Writes a single consolidated configuration file:
  - `config/archive.yml`

This tool only writes the configuration file it is instructed to generate.
It does not modify archive content or directory structure.

---

## sat-tree

**Purpose:**
Validate that the **filesystem structure** of a SAT Content Archive matches
what is declared in its configuration.

**When to use it:**

- To audit an archive’s directory structure
- After changing configuration that affects paths or taxonomy
- Before running downstream tooling
- As a safety check in automation or CI

**What it does:**

- Computes the expected directory tree from `config/archive.yml`
- Reports missing directories
- Optionally creates missing directories when explicitly requested

`sat-tree` is conservative by design:
it never removes directories and never modifies the filesystem unless asked.

---

## Typical Workflow

A common SAT workflow looks like:

```bash
sat-init-archive ...
sat-plugin-discovery
sat-tree --dry-run
sat-tree --create-missing
```

```bash
./bin/sat-tree --dry-run
usage: sat-tree [-h] --config CONFIG [--create-missing] [--dry-run]
sat-tree: error: the following arguments are required: --config
```

```bash
./bin/sat-tree --dry-run --config config/archive.yml 
[sat-tree] ERROR: archive_identity.archive_root is missing in config
```

```bash
./bin/sat-tree --dry-run --config archives/example-content-archive/config/archive.yml
```

