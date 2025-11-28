---
Title: "Using a Test Archive for Dublin Core Plugin Integration Testing"
Description: "A plugin-local guide for creating and using an external test archive to run integration tests for the Dublin Core metadata plugin."
Author: "Christopher Steel"
Date: "2025-11-27"
Last_Modified_Date: "2025-11-27"
License: "CC BY-SA 4.0"
Version: "0.0.2"
Tags:
  - "testing"
  - "integration-testing"
  - "dublin-core"
  - "metadata-plugin"
  - "source-archive-tools"
Keywords:
  - "plugin-testing"
  - "integration-tests"
  - "test-archive"
  - "metadata"
  - "dublin-core"
URL: "https://github.com/steelcj/source-archive-tools/blob/dev/plugins/metadata/dublin_core/docs/testing/using-test-archive-for-plugin-integration.md"
Path: "plugins/metadata/dublin_core/docs/testing/using-test-archive-for-plugin-integration.md"
Canonical: "https://github.com/steelcj/source-archive-tools/blob/dev/plugins/metadata/dublin_core/docs/testing/using-test-archive-for-plugin-integration.md"
Sitemap: "false"
DC_Title: "Using a Test Archive for Dublin Core Plugin Integration Testing"
DC_Creator: "Christopher Steel"
DC_Subject: "A guide for creating and using an external test archive to perform integration testing on the Dublin Core plugin"
DC_Description: "Instructions for preparing a structured test archive outside the repository and using it for full integration testing of the Dublin Core metadata plugin, including test file organization and commands."
DC_Language: "en"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
DC_Contributor: "ChatGPT-5 (OpenAI)"
DC_RightsHolder: "Christopher Steel"
OG_Title: "Using a Test Archive for Dublin Core Plugin Integration Testing"
OG_Description: "A practical guide for creating and using an external test archive to integration-test the Dublin Core metadata plugin."
OG_URL: "https://github.com/steelcj/source-archive-tools/blob/dev/plugins/metadata/dublin_core/docs/testing/using-test-archive-for-plugin-integration.md"
OG_Image: ""
Schema:
  "@context": "https://schema.org"
  "@type": "TechArticle"
  "headline": "Using a Test Archive for Dublin Core Plugin Integration Testing"
  "author": "Christopher Steel"
  "inLanguage": "en"
  "license": "https://creativecommons.org/licenses/by-sa/4.0/"
  "contributor": "ChatGPT-5 (OpenAI)"
Video_Metadata: ""
---

# Using a Test Archive for Dublin Core Plugin Integration Testing

This document explains how to use an **external test archive** to perform integration testing for the Dublin Core metadata plugin. It complements the plugin’s internal examples and unit tests by providing a realistic environment that mirrors how metadata plugins are used with real archives.

The test archive lives *outside* the repository to keep the tools clean and to reflect real-world usage.

## Creating the Test Archive

From the root of the `source-archive-tools` repository:

```bash
mkdir -p ../test-archive/{docs/en,docs/fr,areas,projects,resources}
```

Confirm:

```bash
tree ../test-archive/
```

This produces the following structure:

```
../test-archive/
├── areas
├── docs
│   ├── en
│   └── fr
├── projects
└── resources
```

This mirrors a minimal PARA-style archive layout.

## Organizing Plugin Markdown Test Documents

Our DC metadata plugin includes examples

```bash
tree plugins/metadata/dublin_core/examples/
plugins/metadata/dublin_core/examples/
├── complete.yml
├── custom.yml
├── defaults.yml
└── minimal.yml
```

We can mirror this structure with something like the following:

```bash
mkdir -p plugins/metadata/dublin_core/tests/md/{minimal,defaults,custom,complete}
```

Confirm our changes:

```bash
tree plugins/metadata/dublin_core/tests/md/
```

output example:

```bash
plugins/metadata/dublin_core/tests/md/
├── complete
├── custom
├── defaults
└── minimal
```
#### Minimal metadata test

```bash
cat > plugins/metadata/dublin_core/tests/md/minimal/dc-minimal-metadata.md << 'EOF'
# Dublin Core Minimal Metadata Test

This document is used to verify how the Dublin Core metadata plugin behaves when no metadata front-matter is present.

It allows the plugin to demonstrate:

- Automatic insertion of required Dublin Core fields
- Proper application of defaults from config/defaults.yml
- Stable and predictable generation of YAML front-matter
- Preservation of the original Markdown body content
EOF
```

Confirm:

```bash
cat plugins/metadata/dublin_core/tests/md/minimal/dc-minimal-metadata.md
```

#### Defaults profile test

```bash
cat > plugins/metadata/dublin_core/tests/md/defaults/dc-defaults-metadata.md << 'EOF'
# Dublin Core Defaults Metadata Test

This document is used to verify that the Dublin Core plugin correctly applies the default configuration profile.

It should produce:

- All required Dublin Core fields
- The expected default Creator
- The expected default Language
- The expected License, Contributor, and RightsHolder values
EOF
```

Confirm:

```bash
cat plugins/metadata/dublin_core/tests/md/defaults/dc-defaults-metadata.md
```

#### Custom profile test

```bash
cat > plugins/metadata/dublin_core/tests/md/custom/dc-custom-metadata.md << 'EOF'
# Dublin Core Custom Metadata Profile Test

This document is used to verify that the Dublin Core plugin respects custom metadata overrides when a custom profile is applied.

It ensures that:

- Custom Creator values override defaults
- Custom Language settings are preserved
- Explicitly provided fields are not overwritten by defaults
EOF
```

Confirm:

```bash
cat plugins/metadata/dublin_core/tests/md/custom/dc-custom-metadata.md
```

#### Complete profile test

```bash
cat > plugins/metadata/dublin_core/tests/md/complete/dc-complete-metadata.md << 'EOF'
# Dublin Core Complete Metadata Profile Test

This document is used to verify the plugin's behavior when a complete metadata set is present.

It should confirm that:

- All supported Dublin Core fields are accepted
- The plugin does not overwrite already-complete metadata
- The document body remains unchanged
EOF
```

Confirmation:

```bash
cat plugins/metadata/dublin_core/tests/md/complete/dc-complete-metadata.md
```

## Confirming our new structure

```bash
tree plugins/metadata/dublin_core/tests/md/
```

Expected output:

```text
plugins/metadata/dublin_core/tests/md/
├── complete
│   └── dc-complete-metadata.md
├── custom
│   └── dc-custom-metadata.md
├── defaults
│   └── dc-defaults-metadata.md
└── minimal
    └── dc-minimal-metadata.md

5 directories, 4 files
```

This structure is future-proof and allows new tests to be added without changing the integration workflow.

# Copy Plugin Test Files to the Test Archive

To copy all Markdown tests (preserving directory structure) into the test archive:

```bash
cp -r plugins/metadata/dublin_core/tests/md/* ../test-archive/docs/en/
```

After copying, the test archive will contain the same directory hierarchy:

```bash
tree ../test-archive/docs/en/
```

Expected output:

```
../test-archive/docs/en/
├── complete
│   └── dc-complete-metadata.md
├── custom
│   └── dc-custom-metadata.md
├── defaults
│   └── dc-defaults-metadata.md
└── minimal
    └── dc-minimal-metadata.md

5 directories, 4 files
```

## Notes

Once our testing infra is up and running as envisioned, new tests can be added under `tests/md/` and can be manually or automatically copied over to our test archive without needing to change other things.

## Applying Metadata Plugins to Test Documents

### Apply the plugin to a single test file

```bash
./cli/sat-apply-metadata ../test-archive/docs/en/minimal/dc-minimal-metadata.md
```

Output example:

```bash
Metadata updated using plugin metadata.dublin-core for ../test-archive/docs/en/minimal/dc-minimal-metadata.md
```

Confirmation

```bash
cat ../test-archive/docs/en/minimal/dc-minimal-metadata.md
```

Output example:

```bash
---
DC_Title: __REQUIRED_FIELD_MISSING__
DC_Creator: Christopher Steel
DC_Language: en
DC_License: https://creativecommons.org/licenses/by-sa/4.0/
DC_Contributor: ChatGPT-5 (OpenAI)
---

# Dublin Core Minimal Metadata Test

This document is used to verify how the Dublin Core metadata plugin behaves when no metadata front-matter is present.

It allows the plugin to demonstrate:

- Automatic insertion of required Dublin Core fields
- Proper application of defaults from config/defaults.yml
- Stable and predictable generation of YAML front-matter
- Preservation of the original Markdown body content

```

### Apply the plugin to all test files in a specific scenario

```bash
for f in ../test-archive/docs/en/minimal/*.md; do
    ./cli/sat-apply-metadata "$f"
done
```

### Apply the plugin to all Markdown test files recursively

```bash
find ../test-archive/docs/en -name '*.md' -exec ./cli/sat-apply-metadata {} \;
```

This applies the plugin to every Markdown test file, including any new ones added under the `tests/md/` directory.

# Why Integration Testing Matters

Internal plugin examples test:

- required-field behavior  
- defaults  
- transformation logic  
- plugin boundaries  

Integration tests validate:

- behavior on real document structures  
- directory-based semantics (language, PARA, etc.)  
- plugin chaining  
- metadata interactions  
- edge-case survival  

Together, these test layers ensure that the plugin behaves correctly in real-world contexts.

# License

This document, *Using a Test Archive for Dublin Core Plugin Integration Testing*, by **Christopher Steel**, with AI assistance from **ChatGPT-5 (OpenAI)**, is licensed under the Creative Commons Attribution-ShareAlike 4.0 License.

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)
