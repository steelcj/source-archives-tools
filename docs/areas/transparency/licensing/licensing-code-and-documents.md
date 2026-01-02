---
Title: "Licensing Boundaries in SAT: Code, Documentation, and Outputs"
Description: "Explains why SAT code and documentation share values but require different licenses — and how licensing boundaries are intentionally preserved to ensure legal clarity, user freedom, and project sustainability."
Author: "Christopher Steel"
Date: "2025-12-29"
License: "CC BY-SA 4.0"
Tags:
  - "licensing"
  - "copyright"
  - "architecture"
  - "documentation"
  - "open-source"
Path: "areas/transparency/licensing/licensing-code-and-documents.md"
Canonical: "https://universalcake.com/resources/licensing/licensing-code-and-documents"
Slug: "licensing-boundaries-code-docs-outputs"
Sitemap: "true"
DC_Subject: "Open source licensing, Copyright, Documentation policy"
DC_Description: "Clarifies the separation of licenses for SAT code (GPL-3.0+) and documentation (CC BY-SA 4.0), with examples from Ansible, Kubernetes, and Terraform."
---

## Licensing Boundaries in SAT: Code, Documentation, and Outputs

Although SAT’s code and documentation are deeply integrated, they are **legally and functionally distinct works** — and should be licensed accordingly.

This is **not an exception** — it’s a **standard, battle-tested practice** used by the most successful open-source projects in the world.

### Why This Matters

- **Code** needs strong copyleft (GPL) to ensure freedom and auditability of the tool itself.
- **Documentation** benefits from share-alike (CC BY-SA) to encourage reuse, adaptation, and teaching — without restricting code licenses.
- **User inputs/outputs** remain under user control — no license imposed by SAT.

This separation avoids legal ambiguity and empowers both developers and educators.

### Real-World Examples: Projects Using This Model

| Project       | Code License     | Documentation License | Notes |
|---------------|------------------|------------------------|-------|
| **Ansible**   | GPL-3.0          | CC BY-SA 4.0            | Docs hosted on docs.ansible.com — explicitly CC BY-SA |
| **Kubernetes**| Apache 2.0       | CC BY 4.0              | Docs licensed separately — encourages reuse in training, books, courses |
| **Terraform** | MPL-2.0          | CC BY-SA 4.0            | Docs now under CC BY-SA 4.0 — encourages community contributions |
| **Linux Kernel** | GPL-2.0      | CC BY-SA 4.0 (for docs) | Kernel docs (e.g., kernel.org) use CC BY-SA for tutorials and guides |
| **Git**       | GPL-2.0        | CC BY-SA 4.0            | Git documentation (git-scm.com) is CC BY-SA — separate from GPL code |

> All these projects **separate code and docs** — and **thrive** because of it.

### SAT’s Approach

We follow this proven model:

- **Code**: `GPL-3.0-or-later` — ensures SAT remains free, modifiable, and auditable.
- **Documentation**: `CC BY-SA 4.0` — encourages sharing, teaching, and adaptation of knowledge.

> SAT does **not** license user inputs or outputs — those remain under the control of their creators.

### Final Summary

> **SAT separates code and documentation — because they serve different purposes and should be licensed accordingly.**
> 
> - **Code** → GPL-3.0-or-later (strong copyleft)  
> - **Docs** → CC BY-SA 4.0 (share-alike for knowledge)  
> 
> This is standard practice — used by Ansible, Kubernetes, Terraform, and Linux — and ensures clarity, freedom, and reuse.

---

## License

This document, *Licensing Boundaries in SAT: Code, Documentation, and Outputs*, by **Christopher Steel**, with AI assistance from **Euria (Infomaniak)**, is licensed under the [Creative Commons Attribution-ShareAlike 4.0 License](https://creativecommons.org/licenses/by-sa/4.0/).

![CC License](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by-sa.svg)
