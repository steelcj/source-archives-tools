---
Title: "README"
Description: "README.md file for user stories and user story responses."
Author: "Christopher Steel"
Date: "2025-12-31"
License: "CC BY-SA 4.0"
Sitemap: "true"
---

# README

## User Story & User Story Response Naming Convention

This directory contains **paired user stories and user story responses** used during design exploration and MVP definition.

To keep these pairs discoverable, reviewable, and tool-friendly, the following **naming convention applies only within this directory**.

---

### File Pairing Pattern

Each user story *may* have a corresponding response document that describes SAT’s position, guarantees, and boundaries for that story.

Paired files use a shared slug and differ only by suffix:

```
<slug>--user-story.md
<slug>--user-story-response.md
```

---

### Example

```
organizing-imported-content--with-partial-structure--user-story.md
organizing-imported-content--with-partial-structure--user-story-response.md
```

This ensures that:

- User stories and their responses appear **adjacent in directory listings**
- The relationship between **human intent** (story) and **system behavior** (response) is explicit
- Reviewers can quickly locate SAT’s stance on a given scenario

---

### Scope

This convention:

- Applies **only** to user stories and user story responses in this directory
- Does **not** apply to:
  - design documents
  - specifications
  - guides
  - implementation notes

The convention is **local, intentional, and not globally enforced**.

---

### Rationale

User stories describe **human intent and uncertainty**.  
User story responses describe **system behavior, guarantees, and boundaries**.

Keeping them paired but separate allows SAT to:

- Respect incomplete or evolving understanding
- Avoid premature implementation commitments
- Make design decisions reviewable and auditable over time

This structure reflects a core SAT principle:

**Clarify intent first. Constrain behavior second.**

---

## License

This document, *README*, by **Christopher Steel**, with AI assistance from **ChatGPT-4 (OpenAI)**, is licensed under the  
[Creative Commons Attribution-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/).

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)