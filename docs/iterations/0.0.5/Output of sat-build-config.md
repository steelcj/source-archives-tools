## Output of sat-build-config

The output of `sat-build-config` is a single, fully-assembled configuration document. This file contains everything required by `sat-init-archive` to create a working SAT archive on disk.

At minimum, the output includes:

- the schema version  
- archive identity  
- the archive root path  

If additional plugins are present, it may also include:

- language definitions  
- metadata defaults  
- taxonomy information (e.g., PARA)  
- a list of enabled plugins  

The output is a single YAML document. For example:

```yaml
schema_version: "1.0.0"
archive_identity:
  id: "unnamed-archive"
  label: "SAT Test Archive"
  description: "A SAT archive initialized with default testing configuration."
  archive_root: "../unnamed-archive"
```

When archive-level overrides or CLI flags are supplied, they replace the defaults.

`sat-build-config` guarantees that the final configuration file is complete enough to be passed directly to `sat-init-archive`.

## How merging works

`sat-build-config` assembles configuration fragments in a predictable order:

1. **SAT Core Plugin Defaults**  
   These plugins always load first and provide safe baseline values.

2. **Add-on Plugin Defaults (Optional)**  
   These contribute non-essential fragments such as metadata, languages, or taxonomy information.

3. **Archive-level Configuration (Optional)**  
   A user-supplied configuration file that adds or overrides values.

4. **CLI Overrides (Optional)**  
   Flags passed to `sat-build-config` take precedence over all other sources.

All fragments are deep-merged according to the schema. Arrays are concatenated or replaced depending on the field type. Config blocks that should not be overridden (such as `schema_version`) are protected by validation.

## Template expansion

Before output, `sat-build-config` expands template expressions such as:

```yaml
archive_root: "../{{ archive_identity.id }}"
```

Templates are expanded **after** merging and **before** validation.  
This ensures:

- plugin defaults may reference fields set later (e.g., `archive_identity.id`)
- archive-level overrides and CLI flags are reflected in expanded values
- path-related fields resolve cleanly before `sat-init-archive` runs

After expansion, paths are normalized to ensure a predictable final format.

## Validation

The final assembled configuration is validated against the schema defined by the `core.schema` plugin. Validation ensures that:

- required fields are present  
- protected fields have not been overridden by unauthorized plugins  
- fragments conform to the expected shape  
- template expansion produced valid values  

If validation fails, `sat-build-config` reports the issue and exits without producing output.