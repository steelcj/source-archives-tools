# SAT Archive Initialization Tool Design: `sat-init-archive` MVP

```yaml
slug: sat-init-archive-mvp-design
```

## Description

`sat-init-archive` is the second phase in creating a SAT archive.

Where `sat-build-config` **thinks** (assembling the configuration),
`sat-init-archive` **does** the work of creating the archive on disk.

The MVP version of `sat-init-archive` focuses on a small but complete workflow:

- take the assembled configuration from `sat-build-config`
- validate the core fields required to create an archive root
- create the archive directory structure
- write a minimal `config/archive.yml` file

No plugins are installed, no language roots are created, and no PARA structure is generated in the MVP. Those will come later.

---

## Purpose

The purpose of `sat-init-archive` is to:

- consume a fully-assembled SAT configuration file
- turn it into a concrete archive directory on disk
- ensure that the configuration and filesystem are consistent

This separation keeps configuration logic (`sat-build-config`) and filesystem logic (`sat-init-archive`) clearly decoupled.

---

## Responsibilities (MVP)

The MVP `sat-init-archive` performs the following steps:

1. **Read configuration**
   - Accept a configuration file (e.g., `archive-config.yml`) produced by `sat-build-config`.

2. **Validate required fields**
   
   - `schema_version`
   - `archive_identity.id`
   - `archive_identity.archive_root`
   
3. **Resolve archive root path**
   - Interpret `archive_identity.archive_root` as a path
   - Normalize to an absolute path (for clarity and logging)

4. **Create archive root directory**
   - Create the directory at `archive_root` if it does not exist
   - Refuse to proceed if the directory contains “unexpected” content (MVP policy can be simple: either create if not exists, or require empty)

5. **Create basic subdirectories**
   - `config/` under `archive_root`

6. **Write a minimal `config/archive.yml`**
   - Include at least:
     ```yaml
     schema_version: "<from config>"
     archive_identity:
     id: "<from config>"
     label: "<from config, if any>"
     description: "<from config, if any>"
     ```
   - Optionally include `archive_root` for convenience:
     ```yaml
     archive_root: "<resolved absolute path>"
     ```

7. **Report what was created**
   - Print a short summary:
     - archive root path
     - config file path
     - any warnings

This is enough to create a real SAT archive skeleton from the MVP config.

---

## Non-Responsibilities (MVP)

The MVP does **not**:

- create language roots (`en-ca/`, `fr-qc/`, etc.)
- create PARA directories (`projects/`, `areas/`, `resources/`, `archives/`)
- install or copy plugin code
- run plugin entrypoints
- generate `languages.yml` or `metadata.yml`

All of these will be introduced in later iterations, once we extend the configuration schema (languages, metadata, taxonomy, plugins, etc.).

---

## Inputs

### Configuration file

`sat-init-archive` expects a single configuration file produced by `sat-build-config`, for example:

```yaml
schema_version: "1.0.0"
archive_identity:
  id: "universalcake.com"
  label: "Universal Cake Source Archive"
  description: "Primary SAT archive for the Universal Cake ecosystem."
  archive_root: "../universalcake.com"
```

The exact file path is provided via `--config`, e.g.:

```bash
sat-init-archive --config config.yml
```

### Working directory

The tool does not depend on being called from any special directory.
It uses:

- the `archive_root` value from the config, resolved to an absolute path, as the authoritative location for the archive.

---

## Outputs

### Created directories

At a minimum, the MVP creates:

```text
<archive_root>/
config/
```

Where `<archive_root>` is the resolved value of `archive_identity.archive_root`.

### Created files

- `config/archive.yml`

Example content:

```yaml
schema_version: "1.0.0"
archive_identity:
id: "universalcake.com"
label: "Universal Cake Source Archive"
description: "Primary SAT archive for the Universal Cake ecosystem."
archive_root: "/home/initial/projects/archives/universalcake.com"
```

Later iterations may add:

- `config/languages.yml`
- `config/metadata.yml`
- additional config fragments

---

## CLI Interface (MVP)

Basic CLI:

```bash
sat-init-archive [options]
```

Supported options (MVP):

```text
--config <file> Path to the assembled SAT configuration file (required)
--force Allow initialization into an existing non-empty directory (optional)
--dry-run Show what would be created without writing to disk (optional)
--output-root <path>Override archive_identity.archive_root (optional, low priority)
```

Resolution precedence for the archive root:

1. `--output-root` (if provided)
2. `archive_identity.archive_root` from the config

---

## Initialization Algorithm (MVP)

High-level steps:

1. **Load configuration**
   ```python
   config = load_yaml(config_path)
   ```

2. **Validate required keys**
   - `schema_version` present and non-empty
   - `archive_identity.id` present and non-empty
   - `archive_identity.archive_root` present and non-empty (or overridden by `--output-root`)

3. **Resolve archive root**
   - `root = Path(output_root or config["archive_identity"]["archive_root"])`
   - `root = root.resolve()`

4. **Check directory state**
   - If `root` does not exist: create it
   - If `root` exists:
     - If `--force` is not set and directory is non-empty: abort with a clear message
     - If `--force` is set: continue, but warn

5. **Create required subdirectories**
   ```python
   (root / "config").mkdir(parents=True, exist_ok=True)
   ```

6. **Write `config/archive.yml`**
   - Construct a minimal dict:
     ```python
     out = {
     "schema_version": config.get("schema_version"),
     "archive_identity": {
     "id": config["archive_identity"].get("id"),
     "label": config["archive_identity"].get("label"),
     "description": config["archive_identity"].get("description"),
     "archive_root": str(root),
     },
     }
     ```
   - Write YAML to `root / "config" / "archive.yml"`

7. **Report success**
   - Print:
     ```text
     [sat-init-archive] Archive initialized at: /absolute/path/to/archive_root
     [sat-init-archive] Wrote config/archive.yml
     ```

---

## MVP Example Flow

### Build the config:

```bash
./sat-build-config \
--archive-id universalcake.com \
--archive-label "Universal Cake Source Archive" \
--archive-description "Primary SAT archive for the Universal Cake ecosystem." \
> archive-config.yml
```

### Confirm

```bash
cat archive-config.yml
```

output example:

```yaml
schema_version: 1.0.0
archive_identity:
  id: universalcake.com
  label: Universal Cake Source Archive
  description: Primary SAT archive for the Universal Cake ecosystem.
  archive_root: ../universalcake.com
```

### Initialize the archive:

```bash
./sat-init-archive --config archive-config.yml
```

Resulting filesystem:

```text
../universalcake.com/
config/
archive.yml
```

You now have a real SAT archive root on disk, with identity and schema version recorded, ready for future tooling to extend (language roots, PARA structure, metadata, plugins, etc.).