# My Title

a **Mermaid chart** that reflects the **current workflow**

The **concrete, data-driven, sidecar-first document generation flow** you’ve just defined.

## Here Is Your Mermaid Chart — Tailored to Your Workflow

```mermaid
flowchart TD
    A[Document Path] --> B[Context Extractor]
    B --> C[Ingress: Dublin Core Model]
    C --> D[Augment: Compute Dynamic Fields]
    D --> E[Validate: All Fields Valid]
    E --> F[Project: Write Sidecar]
    F --> G[Human Review]
    G -->|Approve| H[Inject: Front Matter into Document]
    G -->|Reject| I[Edit Sidecar or Model]
    I --> D
    H --> J[Done]
    G -->|Skip| K[Done]

    style A fill:#e6f3ff,stroke:#0066cc
    style B fill:#e6f3ff,stroke:#0066cc
    style C fill:#e6f3ff,stroke:#0066cc
    style D fill:#e6f3ff,stroke:#0066cc
    style E fill:#e6f3ff,stroke:#0066cc
    style F fill:#e6f3ff,stroke:#0066cc
    style G fill:#fff2cc,stroke:#ff9900
    style H fill:#d9ead3,stroke:#38761d
    style I fill:#f4cccc,stroke:#cc0000
    style J fill:#d9ead3,stroke:#38761d
    style K fill:#d9ead3,stroke:#38761d
```

---

## 🧩 Legend

- 🟦 **Blue (fill:#e6f3ff)** — Automated, data-driven steps
- 🟨 **Yellow (fill:#fff2cc)** — Human decision point
- 🟩 **Green (fill:#d9ead3)** — Success / completion
- 🟥 **Red (fill:#f4cccc)** — Rejection / iteration

---

## ✅ Why This Chart Matches Your Workflow

- ✅ Starts with **Document Path** — your source of truth
- ✅ **Context Extractor** — pulls locale, domain, basename, etc.
- ✅ **Ingress** — loads `satellites/dublin-core-example.yml`
- ✅ **Augment** — computes `dc:title`, `dc:date`, etc.
- ✅ **Validate** — confirms all fields are valid (by construction)
- ✅ **Project** — writes sidecar first
- ✅ **Human Review** — you decide to inject or edit
- ✅ **Inject** — only if approved
- ✅ **Loop** — if rejected, go back to augment or edit model

---

## 📄 You’re Now SAT-Compliant

- ✅ No hardcoded values
- ✅ Title derived from filename
- ✅ Descriptions use title
- ✅ Fully data-driven
- ✅ Clean, maintainable, scalable

---

You lead — I follow.