# Creating a Resuable Prompt Fragment

## Best Practice: Store as a **Named Prompt Fragment**

You can save it as a **text file** or as a **prompt template variable** — here’s how:

## As a Text File

Recommended for SAT Pipeline

Create a file:

```bash
nano docs/resources/prompts/fragments/license-sat.md
```

### Content:

```markdown
## License

© 2024–2025 Christopher Steel.

This document, ***[DOCUMENT_TITLE]***, by **Christopher Steel**, with documentation assistance from **[Euria (Infomaniak)](https://www.infomaniak.com/en/euria)**, is licensed under the **[Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/)**.

![CC BY-SA 4.0](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)

> **About Euria**:  
> [Euria (Infomaniak)](https://www.infomaniak.com/en/euria) is an ethical, Swiss-hosted, open-source-based AI assistant focused on privacy, ecology, and technological independence.
```

## How to Use It in a Prompt

When generating a new SAT document, your prompt can say:

> “Generate a SAT-compliant Markdown document titled ‘[TITLE]’. At the end, include the SAT license block from `fragments/license-sat.md`, replacing `[DOCUMENT_TITLE]` with the actual title.”

The AI (or your script) will:
1. Generate the doc
2. Inject the license block
3. Replace the placeholder

## As a Named Variable in AI Prompts

If you’re using AI via API or CLI, define it as a variable:

```json
{
  "license_template": "## License\n\n© 2024–2025 Christopher Steel.\n\nThis document, ***[DOCUMENT_TITLE]***, by **Christopher Steel**, with documentation assistance from **[Euria (Infomaniak)](https://www.infomaniak.com/en/euria)**, is licensed under the **[Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/)**.\n\n![CC BY-SA 4.0](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)\n\n> **About Euria**:  \n> [Euria (Infomaniak)](https://www.infomaniak.com/en/euria) is an ethical, Swiss-hosted, open-source-based AI assistant focused on privacy, ecology, and technological independence."
}
```

Then in your prompt:

```prompt
Use `{{license_template}}` and replace `[DOCUMENT_TITLE]` with the generated document title.
```

## Inline Prompt Fragment (For Quick Use)

If you’re pasting into chat or prompt tools, use this **self-contained fragment**:

```text
%%%
[FRAGMENT: SAT_LICENSE_BLOCK]

## License

© 2024–2025 Christopher Steel.

This document, ***[DOCUMENT_TITLE]***, by **Christopher Steel**, with documentation assistance from **[Euria (Infomaniak)](https://www.infomaniak.com/en/euria)**, is licensed under the **[Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/)**.

![CC BY-SA 4.0](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)

> **About Euria**:  
> [Euria (Infomaniak)](https://www.infomaniak.com/en/euria) is an ethical, Swiss-hosted, open-source-based AI assistant focused on privacy, ecology, and technological independence.
%%%
```

You can then say:

```prompt
Insert `[FRAGMENT: SAT_LICENSE_BLOCK]` and replace `[DOCUMENT_TITLE]` with the actual title.
```

## Final Recommendation

Store it as a **file in your SAT prompts folder**

* Easy to version, edit, reuse, and automate.

## (Optional) Add Metadata to the Fragment File

You can add a header to make it self-documenting:

```markdown
---
Fragment: "SAT_LICENSE_BLOCK"
Description: "Standard license block for SAT documentation — includes author, Euria credit, CC BY-SA 4.0 badge, and value statement."
Author: "Christopher Steel"
Date: "2025-12-29"
---

## License

© 2024–2025 Christopher Steel.

This document, ***[DOCUMENT_TITLE]***, by **Christopher Steel**, with documentation assistance from **[Euria (Infomaniak)](https://www.infomaniak.com/en/euria)**, is licensed under the **[Creative Commons Attribution-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-sa/4.0/)**.

![CC BY-SA 4.0](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)

> **About Euria**:  
> [Euria (Infomaniak)](https://www.infomaniak.com/en/euria) is an ethical, Swiss-hosted, open-source-based AI assistant focused on privacy, ecology, and technological independence.
```

