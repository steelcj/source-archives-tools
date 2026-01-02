# Mermaid--Generate a Compliant  Flowchart Document

## Description

* replace the **subject** (e.g., “Primary Colors”, “Stoic Virtues”, “Project Phases”) and the AI will auto-structure the YAML, diagram, sections, and licensing accordingly.

### Generic Prompt: Generate SAT-Compliant Mermaid Flowchart Document (with ~~~markdown enclosure)

> You are an AI assistant following the **Source Archive Tools (SAT) Canonical Mermaid Flowchart Standard**.  
>
> Generate a complete, self-contained Markdown document illustrating **[SUBJECT]** using a top-down Mermaid flowchart (`flowchart TD`).  
>
> Replace `[SUBJECT]` with the actual topic (e.g., “Primary Colors”, “Stoic Virtues”, “Project Phases”).  
>
> The document must include:
>
> 1. **YAML Front Matter** with:
>    - `Title`: “*[SUBJECT]*”  
>    - `Description`: “A conceptual flowchart illustrating *[SUBJECT]* within SAT-style frameworks.”  
>    - `Author`: “Christopher Steel”  
>    - `Date`: Use today’s date in `YYYY-MM-DD` format  
>    - `License`: “CC BY-SA 4.0”  
>    - `Path`: `resources/[category]/[subject-slug]` — infer category (e.g., `philosophy`, `design`, `science`) from subject  
>    - `Canonical`: `https://universalcake.com/resources/[category]/[subject-slug]`  
>    - `Sitemap: "true"`  
>    - `DC_Subject`: “Topic category or domain” (e.g., “Color theory”, “Stoic philosophy”)  
>    - `DC_Description`: “Diagram showing how [SUBJECT] is structured or related.”  
>
> 2. **Main Heading**: `## [SUBJECT]`  
>
> 3. **Chart Anchor**: `<a name="[subject-slug]-chart"></a>`  
>
> 4. **Mermaid Flowchart** using:
>    - `%%{ init: { ... } }%%` theme block as defined in SAT standard (copy verbatim)  
>    - `flowchart TD`  
>    - Nodes with **quoted, multi-line labels**, properly indented  
>    - Arrows showing logical or hierarchical relationships  
>    - `click` handlers for each node linking to its section (e.g., `click A "#red"`)  
>
> 5. **Section Headers** for each major node (e.g., `### Red`, `### Blue`, etc.):
>    - Anchor link: `<a name="[node-slug]"></a>`  
>    - Brief definition and bullet points  
>    - “Return to chart” link  
>
> 6. **License Section**:
>    - Attribution: “This document, *[SUBJECT]*, by **Christopher Steel**, with AI assistance from **Euria (Infomaniak)**...”  
>    - CC BY-SA 4.0 license badge: `![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)`  
>
> !!!**CRITICAL**:  
> - Enclose the **entire document** in `~~~markdown` and `~~~` — **not** triple backticks.  
> - Do **not** use HTML tags, `<br>`, or renderer-specific syntax.  
> - Use consistent indentation inside node labels.  
> - Do **not** compress labels into single lines.  
> - Do **not** interleave node definitions with edges.  
>
> Output **only** the final formatted document — no explanations, no extra text.

---

### Example Usage:
> Generate a Primary Colors Mermaid Chart

* Will output a full SAT-compliant doc about red, blue, yellow — with flowchart, sections, anchors, and licensing — all enclosed in `~~~markdown`.

> Generate a Stoic Virtues Mermaid Chart

Absolutely! Here’s a **generic, reusable prompt** that lets you generate any SAT-compliant Mermaid flowchart document — simply replace the **subject** (e.g., “Primary Colors”, “Stoic Virtues”, “Project Phases”) — and the AI will auto-structure the YAML, diagram, sections, and licensing accordingly.

---

### Generic Prompt: Generate SAT-Compliant Mermaid Flowchart Document

> You are an AI assistant following the **Source Archive Tools (SAT) Canonical Mermaid Flowchart Standard**.  
>
> Generate a complete, self-contained Markdown document illustrating **[SUBJECT]** using a top-down Mermaid flowchart (`flowchart TD`).  
>
> Replace `[SUBJECT]` with the actual topic (e.g., “Primary Colors”, “Stoic Virtues”, “Project Phases”).  
>
> The document must include:
>
> 1. **YAML Front Matter** with:
>    - `Title`: “*[SUBJECT]*”  
>    - `Description`: “A conceptual flowchart illustrating *[SUBJECT]* within SAT-style frameworks.”  
>    - `Author`: “Christopher Steel”  
>    - `Date`: Use today’s date in `YYYY-MM-DD` format  
>    - `License`: “CC BY-SA 4.0”  
>    - `Path`: `resources/[category]/[subject-slug]` — infer category (e.g., `philosophy`, `design`, `science`) from subject  
>    - `Canonical`: `https://universalcake.com/resources/[category]/[subject-slug]`  
>    - `Sitemap: "true"`  
>    - `DC_Subject`: “Topic category or domain” (e.g., “Color theory”, “Stoic philosophy”)  
>    - `DC_Description`: “Diagram showing how [SUBJECT] is structured or related.”  
>
> 2. **Main Heading**: `## [SUBJECT]`  
>
> 3. **Chart Anchor**: `<a name="[subject-slug]-chart"></a>`  
>
> 4. **Mermaid Flowchart** using:
>    - `%%{ init: { ... } }%%` theme block as defined in SAT standard (copy verbatim)  
>    - `flowchart TD`  
>    - Nodes with **quoted, multi-line labels**, properly indented  
>    - Arrows showing logical or hierarchical relationships  
>    - `click` handlers for each node linking to its section (e.g., `click A "#red"`)  
>
> 5. **Section Headers** for each major node (e.g., `### Red`, `### Blue`, etc.):
>    - Anchor link: `<a name="[node-slug]"></a>`  
>    - Brief definition and bullet points  
>    - “Return to chart” link  
>
> 6. **License Section**:
>    - Attribution: “This document, *[SUBJECT]*, by **Christopher Steel**, with AI assistance from **Euria (Infomaniak)**...”  
>    - CC BY-SA 4.0 license badge: `![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)`  
>
> !!!**CRITICAL**:  
> - Enclose the **entire document** in `~~~markdown` and `~~~` — **not** triple backticks.  
> - Do **not** use HTML tags, `<br>`, or renderer-specific syntax.  
> - Use consistent indentation inside node labels.  
> - Do **not** compress labels into single lines.  
> - Do **not** interleave node definitions with edges.  
>
> Output **only** the final formatted document — no explanations, no extra text.

---

### Example Usage:
> Generate a Primary Colors Mermaid Chart

* Will output a full SAT-compliant doc about red, blue, yellow — with flowchart, sections, anchors, and licensing — all enclosed in `~~~markdown`.

> Generate a Stoic Virtues Mermaid Chart

* Same structure, different content.

---

## Options

Let me know if you want to add optional fields (like `Version`, `Dependencies`, or `Status`) or generate multiple variants (e.g., horizontal flowcharts, swimlanes, etc.).