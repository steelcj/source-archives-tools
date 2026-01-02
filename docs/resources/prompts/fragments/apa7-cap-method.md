---
Title: "APA7 + CAP Prompt Fragment"
Description: "Minimal SAT prompt fragment describing Universalcake’s APA7 + CAP citation pattern using hidden citation anchors and paired reference links."
Author: "Christopher Steel"
Date: "2025-12-07"
Last_Modified_Date: "2025-12-07"
License: "CC BY-SA 4.0"
Tags:
- "sat"
- "prompt-fragment"
- "apa7"
- "cap"
URL: "https://github.com/steelcj/source-archives-tools/blob/main/docs/resources/sat/prompts/apa7-cap-method.md"
Path: "docs/resources/sat/prompts/apa7-cap-method.md"
Canonical: "https://github.com/steelcj/source-archives-tools/blob/main/docs/resources/sat/prompts/apa7-cap-method.md"
DC_Title: "APA7 + CAP Prompt Fragment"
DC_Creator: "Christopher Steel"
DC_Contributor: "<chatgpt_version> (<chatgpt_maker>)"
DC_RightsHolder: "Christopher Steel"
DC_Description: "A minimal, reusable SAT prompt fragment defining Universalcake’s APA7 + CAP citation method using invisible citation anchors and paired reference links."
DC_Language: "en-CA"
DC_License: "https://creativecommons.org/licenses/by-sa/4.0/"
---

# APA7 + CAP Prompt Fragment

## Overview

This document publishes the **minimal SAT prompt fragment** for Universalcake’s **APA7 + Citation Anchor Pair (CAP)** citation method.
The fragment provides the rules for:

- placing hidden citation anchors at the start of cited content,
- adding APA7 parenthetical citations paired with CAP reference links at the end of cited content,
- structuring reference entries with matching anchors and return links.

Include this fragment whenever generating Universalcake documents that must comply with APA7 and CAP standards.

## Prompt

```prompt
Use Universalcake’s APA7 + CAP (Citation Anchor Pair) method for all citations and references.

1. At the beginning of any content supported by a reference, insert a hidden citation anchor exactly like this:

```markdown
<a name="evans-2008-citation"></a>
```

2. After writing the cited content, append the APA7 parenthetical citation followed immediately (no whitespace) by a Markdown link to the matching reference anchor:

```markdown
[(Evans, 2008)](#evans-2008-reference)
```

3. The final pattern must look like:

```markdown
<a name="evans-2008-citation"></a>System 1 aligns with automatic processing [(Evans, 2008)](#evans-2008-reference).
```

4. In the reference list, create a matching anchor-entry pair followed by a “Return to citation” link:

```markdown
<a name="evans-2008-reference"></a>
Evans, J. St. B. T. (2008). Title of the article. *Journal Name, volume*(issue), pages. https://doi.org/xxx

[Return to citation](#evans-2008-citation)
```

Rules:

- The `<a name="...-citation"></a>` anchor always goes at the **start** of the cited content.
- The APA7 citation + CAP link always goes at the **end**.
- Do **not** place a space between `(Evans, 2008)` and `[#evans-2008-reference]`.
- Each in-text citation must have a matching `-reference` anchor.
- Each reference entry must include a `[Return to citation]` link pointing back to its `-citation` anchor.
```
## License

This document, *APA7 + CAP Prompt Fragment*, by **Christopher Steel**, with AI assistance from **<chatgpt_version> (<chatgpt_maker>)**, is licensed under the [Creative Commons Attribution-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/).

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)