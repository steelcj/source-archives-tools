---
Title: "Dublin Core Plugin Example Configurations"
Description: "Example configuration profiles for the Dublin Core metadata plugin, including minimal, sane defaults, custom, and full examples."
Author: "Christopher Steel"
Date: "2025-11-27"
Last_Modified_Date: "2025-11-27"
License: "CC BY-SA 4.0"
Version: "0.0.1"
Tags:
  - "metadata"
  - "dublin-core"
  - "examples"
  - "plugin"
Keywords:
  - "dublin-core"
  - "metadata"
  - "profiles"
  - "examples"
URL: "https://github.com/steelcj/source-archives-tools/blob/main/plugins/metadata/dublin-core/docs/examples-overview.md"
Path: "plugins/metadata/dublin-core/docs/examples-overview.md"
Canonical: "https://github.com/steelcj/source-archives-tools/blob/main/plugins/metadata/dublin-core/docs/examples-overview.md"
OG_URL: "https://github.com/steelcj/source-archives-tools/blob/main/plugins/metadata/dublin-core/docs/examples-overview.md"
Sitemap: "false"
DC_Title: "Dublin Core Plugin Example Configurations"
DC_Creator: "Christopher Steel"
DC_Subject: "Example configuration profiles for the Dublin Core metadata plugin"
DC_Description: "A collection of minimal, sane-default, custom, and full example metadata configurations for testing and validating the Dublin Core plugin."
DC_Language: "en"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
DC_Contributor: "ChatGPT-5 (OpenAI)"
DC_RightsHolder: "Christopher Steel"
OG_Title: "Dublin Core Plugin Example Configurations"
OG_Description: "Example configuration profiles for the Dublin Core metadata plugin."
OG_URL: "https://github.com/steelcj/source-archives-blob/main/plugins/metadata/dublin-core/docs/dublin_core-examples-overview.md"
OG_Image: ""
Schema:
  "@context": "https://schema.org"
  "@type": "TechArticle"
  "headline": "Dublin Core Plugin Example Configurations"
  "author": "Christopher Steel"
  "inLanguage": "en"
  "license": "https://creativecommons.org/licenses/by-sa/4.0/"
  "contributor": "ChatGPT-5 (OpenAI)"
Video_Metadata: ""
---

# Dublin Core Plugin Example Configurations

This document provides four example configuration profiles for use with the Dublin Core metadata plugin. These profiles support testing, validation, and reference usage.

All example files are intended to live under:

```bash
mkdir plugins/metadata/dublin_core/examples/
```

# minimal.yml

Create:

```bash
nano plugins/metadata/dublin_core/examples/minimal.yml
```

Content:

```yaml
DC_Title: "Untitled Document"
DC_Creator: "Unknown"
DC_Language: "en"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
```

# defaults.yml

Create: 

```bash
nano plugins/metadata/dublin_core/examples/defaults.yml
```

Content:

```yaml
DC_Title: "Example Document"
DC_Creator: "Christopher Steel"
DC_Language: "en"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
DC_Contributor: "ChatGPT-5 (OpenAI)"
DC_RightsHolder: "Christopher Steel"
```

# custom.yml

Create:

```bash
nano plugins/metadata/dublin_core/examples/custom.yml
```

Content:

```yaml
DC_Title: "Custom Test File"
DC_Creator: "Guest Author"
DC_Language: "fr"
DC_License: "https://creativecommons.org/licenses/by-nc-nd/4.0/"
DC_Contributor: "Documentation Team"
DC_RightsHolder: "Guest Author"
```

# complete.yml

Create:

```bash
nano plugins/metadata/dublin_core/examples/complete.yml
```

Content:

```yaml
DC_Title: "Full Dublin Core Example"
DC_Creator: "Christopher Steel"
DC_Contributor: "ChatGPT-5 (OpenAI)"
DC_Subject:
  - "metadata"
  - "testing"
  - "dublin-core"
DC_Description: "A full example of all DC fields supported by this plugin."
DC_Publisher: "Universal Cake"
DC_Date: "2025-01-01"
DC_Type: "Text"
DC_Format: "text/markdown"
DC_Identifier: "urn:uuid:123e4567-e89b-12d3-a456-426614174000"
DC_Source: "Internal Test Suite"
DC_Language: "en"
DC_Relation: []
DC_Coverage: ""
DC_Rights: "CC BY-SA 4.0"
DC_RightsHolder: "Christopher Steel"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
```

See testing again in 

## License

This document, *Dublin Core Plugin Example Configurations*, by **Christopher Steel**, with AI assistance from **ChatGPT-5 (OpenAI)**, is licensed under the Creative Commons Attribution-ShareAlike 4.0 License.

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)

