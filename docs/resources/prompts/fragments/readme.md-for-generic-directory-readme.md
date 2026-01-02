## Prompt — Generic Directory README

> Generate a **web-ready, unrendered Markdown `README.md`** for a directory.
>
> Requirements:
>
> - The filename and document title must be **`README.md`**.
> - Include a **YAML front-matter block** with:
>   - `Title: "README"`
>   - A **neutral, literal `Description`** explaining what this directory contains
>   - `Author`, `Date`, `License`, and `Sitemap` fields only
> - Do **not** encode section titles, conventions, or directory-specific rules into metadata.
>
> Content requirements:
>
> - Begin with an **H1 heading**: `README`
> - Use **H2 headings** for major sections
> - Describe:
>   - the **purpose** of the directory
>   - the **types of files** it contains
>   - any **local conventions** that apply *only* within this directory
> - If naming conventions are present:
>   - describe them explicitly
>   - include concrete examples
>   - clearly state their **scope and limits**
>
> Style constraints:
>
> - Keep language clear, precise, and neutral
> - Avoid implementation details unless the directory explicitly requires them
> - Treat conventions as **local and intentional**, not globally enforced rules
> - Prefer explanation over instruction
>
> Include a standard **CC BY-SA 4.0 license section** at the end.