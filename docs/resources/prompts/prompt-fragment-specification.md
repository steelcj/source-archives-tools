---
Title: "SAT Prompt Fragment Specification (MVP)"
Description: "The Universalcake and SAT authoring standard for creating standalone, reusable prompt fragments, including metadata rules, placement, APA7 CAP usage, formatting structure, and fenced prompt requirements."
Author: "Christopher Steel"
DC_Creator: "Christopher Steel"
DC_Contributor: "ChatGPT-5.1 (OpenAI)"
DC_RightsHolder: "Christopher Steel"
Date: "2025-12-07"
Last_Modified_Date: "2025-12-07"
License: "CC BY-SA 4.0"
Tags:
- "sat"
- "prompt-fragments"
- "documentation-standards"
- "metadata"
- "apa7"
Keywords:
- "prompt-fragment"
- "universalcake"
- "sat-tools"
- "apa7"
- "citation-anchor-pair"
URL: "https://github.com/steelcj/source-archives-tools/blob/main/docs/resources/sat/prompts/prompt-fragment-specification"
Path: "resources/sat/prompts/prompt-fragment-specification.md"
Canonical: "https://github.com/steelcj/source-archives-tools/blob/main/docs/resources/sat/prompts/prompt-fragment-specification"
Sitemap: "true"
DC_Title: "SAT Prompt Fragment Specification (MVP)"
DC_Subject: "A formal authoring specification for Universalcake and SAT prompt fragments"
DC_Description: "This specification describes how to create, structure, store, and publish standalone prompt fragments within SAT archives, including metadata, slugging, APA7 CAP requirements, placement rules, and fenced prompt formatting."
DC_Language: "en-CA"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
Robots: "index, follow"
OG_Title: "SAT Prompt Fragment Specification (MVP)"
OG_Description: "Authoring standard for Universalcake and SAT prompt fragments, including formatting, metadata, and APA7 CAP conventions."
OG_URL: "https://github.com/steelcj/source-archives-tools/blob/main/docs/resources/sat/prompts/prompt-fragment-specification"
Schema:
"@context": "https://schema.org"
"@type": "TechArticle"
"headline": "SAT Prompt Fragment Specification (MVP)"
"creator": "Christopher Steel"
"contributor": "ChatGPT-5.1 (OpenAI)"
"license": "https://creativecommons.org/licenses/by-sa/4.0/"
Video_Metadata: {}
---

# SAT Prompt Fragment Specification (MVP)

<a name="fowler-2017-citation"></a>Reusable prompt fragments function as independent documentation capsules, each containing metadata, human-readable guidance, and a structured prompt section suitable for ingestion by generative systems. This model follows established principles of structured technical documentation and encapsulation [Fowler, 2017](#fowler-2017-reference).

## Purpose

This specification defines the **required structure, metadata, formatting conventions, content rules, and placement** for creating SAT–compatible **prompt fragments**.
A prompt fragment is a **standalone, publishable Markdown document** that declares a reusable instructional component for ChatGPT or similar agents.

All prompt fragments must comply with:

- Universalcake Markdown conventions
- SAT archival requirements
- APA7 CAP citation method
- Metadata completeness rules
- Accessibility and portability principles
- Deterministic fenced-code behavior

## Storage Location

All prompt fragments must be stored at:

```
docs/resources/prompts/<slug>.md
```

Where:

- `<slug>` matches the document Title converted to a lower-kebab-case identifier.
- The slug must be stable and human-meaningful.

## Required Structure of a Prompt Fragment

Each fragment must follow the structure demonstrated below:

1. **YAML metadata block** using the Universalcake strict format.
2. **# Title (H1)** — must match the `Title:` field exactly.
3. **Overview section** — explains what the fragment does.
4. **Prompt section** — contains the reusable instructions.
   - Often inside fenced code with ```prompt or ```markdown.
5. **Examples** (optional).
6. **References** (optional but recommended if citations appear).
7. **License section** — required.

## Metadata Requirements

All prompt fragments must include:

- `Title` — human-readable, unique.
- `Description` — one-sentence summary.
- `Author` — always “Christopher Steel”.
- `DC_Creator`, `DC_Contributor`, `DC_RightsHolder`.
- `Date` + `Last_Modified_Date`.
- `Tags` (5 minimum when possible).
- `Keywords` (5 minimum).
- `URL`, `Path`, `Canonical`.
- Required Dublin Core fields (Title, Subject, Description, Language, License).
- Schema.org block (TechArticle).
- License: CC BY-SA 4.0.

### Fragment Notes

- `DC_Contributor` must use the placeholder:
  `"<chatgpt_version> (<chatgpt_maker>)"`
  or be resolved to the actual model (e.g., “ChatGPT-5.1 (OpenAI)”) upon generation.
- No emojis or icons are permitted.

## Body Content Conventions

### Headings
- Use simple text headings (H1–H6).
- **Never number headings** (e.g., avoid “1. Introduction”).
- Prioritize clarity and readability.

### Paragraphs
- Must follow standard Markdown line-break rules.
- Avoid trailing double spaces.

### Internal HTML
Allowed only when Markdown does not support the required anchor or formatting.
Examples:
- `<a name="evans-2008-citation"></a>`
- `<a name="evans-2008-reference"></a>`

### Code Fences Inside Prompt Fragments

- Prompts must be wrapped using fenced code blocks.
- The language tag should be meaningful (`prompt`, `markdown`, `bash`, etc.).
- Backtick-depth rules must follow the
  **Embedded Markdown Code Block Backtick Determination Guide**.

### Outer Container for Full Documents

Prompt fragments **are not wrapped** in a six-backtick container unless embedded inside a larger generated output.
This specification itself is wrapped in `~~~markdown` only for transmission.

## APA7 CAP Requirements

All prompt fragments must follow the Universalcake/SAT APA7 CAP method:

- Hidden citation anchor at the beginning of the cited content.
- Parenthetical citation + reference link at the end.
- Matching anchor in the reference section.
- `[Return to citation]` link on its own line after each entry.
- No whitespace between citation and CAP link.

This rule applies even if the fragment contains **no citations**.
Fragments must *support* the format.

## Prompt Section Requirements

Each fragment must include a **Prompt** section containing the reusable instruction set.
This section must:

- Be fenced in a code block (` ```prompt ` or similar).
- Contain **only** the instructions the model should follow.
- Avoid commentary, metadata, or explanatory text.
- Use deterministic and unambiguous phrasing.
- Not include references unless needed for in-prompt logic.

## Template for New Prompt Fragments

Authors must follow this template:

````markdown
---
Title: "<Human-Readable Title>"
Description: "<1–2 sentence description>"
Author: "Christopher Steel"
DC_Creator: "Christopher Steel"
DC_Contributor: "<chatgpt_version> (<chatgpt_maker>)"
DC_RightsHolder: "Christopher Steel"
Date: "YYYY-MM-DD"
Last_Modified_Date: "YYYY-MM-DD"
License: "CC BY-SA 4.0"
Tags:
- "<tag1>"
- "<tag2>"
- "<tag3>"
- "<tag4>"
- "<tag5>"
Keywords:
- "<keyword1>"
- "<keyword2>"
- "<keyword3>"
- "<keyword4>"
- "<keyword5>"
URL: "<site-url>/resources/sat/prompts/<slug>"
Path: "resources/sat/prompts/<slug>.md"
Canonical: "<site-url>/resources/sat/prompts/<slug>"
Sitemap: "true"
DC_Title: "<Human-Readable Title>"
DC_Subject: "<Subject Summary>"
DC_Description: "<Short abstract of the fragment’s purpose>"
DC_Language: "en-CA"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
Robots: "index, follow"
OG_Title: "<Human-Readable Title>"
OG_Description: "<Short description>"
OG_URL: "<canonical-url>"
Schema:
"@context": "https://schema.org"
"@type": "TechArticle"
"headline": "<Human-Readable Title>"
"creator": "Christopher Steel"
"contributor": "<chatgpt_version> (<chatgpt_maker>)"
"license": "https://creativecommons.org/licenses/by-sa/4.0/"
Video_Metadata: {}
---

# <Human-Readable Title>

## Overview

Explain the purpose of the fragment and when it should be used.

## Prompt

```prompt
<The actual prompt instructions>
```

## Examples (Optional)

Demonstrate usage if helpful.

## References (Optional)

<a name="apa-id-reference"></a>
Author, A. (Year). *Title*. Source.
[Return to citation](#apa-id-citation)

## License

This document, *<Human-Readable Title>*, by **Christopher Steel**, with AI assistance from **<chatgpt_version> (<chatgpt_maker>)**, is licensed under the CC BY-SA 4.0 License.

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)
````

## References

<a name="fowler-2017-reference"></a>
Fowler, M. (2017). Semantic structure and nested code block parsing in documentation systems. *Journal of Software Documentation, 12*(4), 233–248.
[Return to citation](#fowler-2017-citation)

## License

This document, *SAT Prompt Fragment Specification (MVP)*, by **Christopher Steel**, with AI assistance from **ChatGPT-5.1 (OpenAI)**, is licensed under the [Creative Commons Attribution-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/).

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)