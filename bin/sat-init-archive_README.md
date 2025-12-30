# sat-init-archive_README.md

## Description

`sat-init-archive` initializes a new **SAT Content Archive** using an existing **SAT Tool Archive** as its source of truth.

The script:

- Locates the SAT Tool Archive root based on its own location under `tools/bin/`
- Reads `tool_archive_id` and `tool_archive_version` from the Tool Archive manifest
- Creates a new Content Archive directory
- Writes the minimal required files:
  - `config/archive.yml`
  - `meta/archive.manifest.yml`

The tool is designed to be:

- Cross-platform (Linux, macOS, Windows)
- Safe to run from any working directory
- Free of external dependencies
- Explicit about structure and intent

This script represents the **first step** in creating a SAT-compliant Content Archive.

## Usage example

### Usage in Development

#### sat-init-archive

If new install ensure sat-init-archive.py is executable

```bash
chmod +x ./bin/sat-init-archive.py
```

 Run the tool

```bash
./bin/sat-init-archive.py \
  --archive-root ./archives/example-content-archive \
  --id "example-content-archive" \
  --label "Example Content Archive" \
  --description "An example SAT content archive created for testing."
```

Expected oputput

```bash
  --archive-root ./archives/example-content-archive \
  --id "example-content-archive" \
  --label "Example Content Archive" \
  --description "An example SAT content archive created for testing."
Initialized Content Archive at: /home/initial/projects/sat/dev/sat/archives/example-content-archive
  sat_version: 1.0.0
```



#### Troubleshooting

##### Invalid layout

```bash
Error: invalid SAT tools layout detected at /home/initial/projects/sat/dev/sat
```

This error indicates that **one or more required SAT directories were not found** relative to the tool being executed.

Typical causes include:

- Running the tool from outside the SAT repository
- Copying `tools/` without `config/` or `plugins/`
- Executing a tool via `$PATH` without an installed SAT runtime
- Renaming or restructuring internal SAT directories

##### Tool Archive manifest not found

```bash
Error: Tool Archive manifest not found at /home/initial/projects/sat/dev/meta/archive.manifest.yml. Is sat-init-archive being run from a valid Tool Archive?
```



```bash
sat-init-archive \
  --archive-root ~/archives/example-content-archive \
  --id "example-content-archive" \
  --label "Example Content Archive" \
  --description "An example SAT content archive created for testing."