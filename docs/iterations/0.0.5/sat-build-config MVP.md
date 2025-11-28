## sat-build-config MVP

The MVP for `sat-build-config` focuses on a very small but fully usable subset:

- load the `core.schema` plugin (schema_version)
- load the `core.archive-identity` plugin (archive_identity)
- apply optional archive-level configuration
- apply optional CLI overrides
- expand simple templates
- output a minimal, valid configuration file

This MVP only produces:

```yaml
schema_version: "..."
archive_identity:
id: "..."
label: "..."
description: "..."
archive_root: "..."
```

Later iterations can add languages, metadata, taxonomy, and plugin lists.

### MVP Inputs

- **Required core plugins**
- `core.schema`
- `core.archive-identity`

- **Optional archive-level config file**
- `--config archive-config.in.yml`

- **Optional CLI overrides**
- `--archive-id`
- `--archive-label`
- `--archive-description`
- `--archive-root`

### MVP Output

A single YAML document written to stdout (or to `--output` if provided) with:

```yaml
schema_version: "<from core.schema>"
archive_identity:
id: "<from defaults, config, or CLI>"
label: "<from defaults, config, or CLI>"
description: "<from defaults, config, or CLI>"
archive_root: "<from defaults, config, or CLI, with templates expanded>"
```

### MVP CLI

```bash
sat-build-config [options]
```

Supported options (MVP):

```text
--config <file> Optional archive-level config
--archive-id <id> Override archive_identity.id
--archive-label <label> Override archive_identity.label
--archive-description <desc>Override archive_identity.description
--archive-root <path> Override archive_identity.archive_root
--output <file> Write output to file instead of stdout
--helpShow basic usage
```

### MVP Plugin Expectations

`sat-build-config` looks for the two core plugins in a known location, e.g.:

```text
tools/plugins/core/schema/
tools/plugins/core/archive-identity/
```

Each must contain:

```text
plugin.yml
etc/defaults.yml
```

If these files are missing, `sat-build-config` prints a warning and continues. For the MVP, you can treat missing core plugins as a hard error if you want, but the behavior for other plugins should remain “warn and skip”.

#### core.schema defaults (MVP)

```yaml
# tools/plugins/core/schema/etc/defaults.yml
version: "0.1.0"

plugin:
id: "core.schema"

defaults:
config_fragments:
schema_version: "1.0.0"
```

#### core.archive-identity defaults (MVP)

```yaml
# tools/plugins/core/archive-identity/etc/defaults.yml
version: "0.1.0"

plugin:
id: "core.archive-identity"

defaults:
config_fragments:
archive_identity:
id: "unnamed-archive"
label: "SAT Test Archive"
description: "A SAT archive initialized with default testing configuration."
archive_root: "../{{ archive_identity.id }}"
```

### MVP Merge Algorithm (Identity-only)

High-level steps:

1. **Initialize an empty config object**:
 ```yaml
 schema_version: null
 archive_identity: {}
 ```

2. **Load core.schema defaults**
 - Read `etc/defaults.yml`
 - Merge `config_fragments.schema_version` into `schema_version` if present

3. **Load core.archive-identity defaults**
 - Read `etc/defaults.yml`
 - Merge `config_fragments.archive_identity` into `archive_identity`

4. **Apply archive-level config (if `--config` is provided)**
 - Read YAML file
 - If it contains `archive_identity`, deep-merge it over the current `archive_identity`
 - If it contains `schema_version`, it may replace the default (for MVP you can allow this, or choose to protect it later)

5. **Apply CLI overrides**
 - If `--archive-id` is set, override `archive_identity.id`
 - If `--archive-label` is set, override `archive_identity.label`
 - If `--archive-description` is set, override `archive_identity.description`
 - If `--archive-root` is set, override `archive_identity.archive_root`

6. **Template expansion**
 - Look for `{{ archive_identity.id }}` inside `archive_identity.archive_root`
 - Replace it with the final `archive_identity.id`
 - Example:
 - id = `universalcake.com`
 - archive_root = `"../{{ archive_identity.id }}"`
 - result = `"../universalcake.com"`

7. **Minimal validation (MVP)**
 - Ensure `schema_version` is not null
 - Ensure `archive_identity.id` is not empty
 - Ensure `archive_identity.archive_root` is not empty
 - If any fail, print an error and exit with non-zero status

8. **Output final config**
 - If `--output FILE` is given, write YAML there
 - Otherwise, print YAML to stdout

### MVP Example

No config, no CLI overrides:

```bash
sat-build-config > archive-config.yml
```

Produces:

```yaml
schema_version: "1.0.0"
archive_identity:
id: "unnamed-archive"
label: "SAT Test Archive"
description: "A SAT archive initialized with default testing configuration."
archive_root: "../unnamed-archive"
```

With CLI overrides:

```bash
sat-build-config \
--archive-id universalcake.com \
--archive-label "Universal Cake Source Archive" \
--archive-description "Primary SAT archive for the Universal Cake ecosystem." \
> archive-config.yml
```

Produces:

```yaml
schema_version: "1.0.0"
archive_identity:
id: "universalcake.com"
label: "Universal Cake Source Archive"
description: "Primary SAT archive for the Universal Cake ecosystem."
archive_root: "../universalcake.com"
```

This MVP is enough to:

- prove your plugin model
- test core behavior
- give `sat-init-archive` something real to consume
- grow into the full config assembly pipeline later