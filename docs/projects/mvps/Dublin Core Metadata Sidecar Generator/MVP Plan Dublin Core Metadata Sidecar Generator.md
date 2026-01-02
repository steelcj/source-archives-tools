# MVP Plan: Dublin Core Metadata Sidecar Generator

## Goal
Generate a **SAT-compliant, data-driven Dublin Core metadata sidecar** for any Markdown document — derived from its path, filename, and config — then optionally inject into front matter.

---

## MVP Scope (Minimal Viable Product)

1. **Ingress**  
   - Load base model: `satellites/dublin-core-example.yml`  
   - Extract context from document path: `locale`, `domain`, `category`, `basename`, `relative_path`

2. **Augment**  
   - Compute dynamic fields:  
     - `dc:title` → from `basename`  
     - `dc:description` → from `title`  
     - `dc:date` → now  
     - `dc:language` → from path  
     - `dc:source` → from `base_url` + `relative_path`  
     - `dc:identifier` → UUID or hash of path

3. **Validate**  
   - All fields are valid by construction (no external validation needed)

4. **Project**  
   - Write to sidecar: `document.md.sidecar.dublin-core.yml`  
   - Do NOT modify original document

5. **Optional: Inject**  
   - If user runs with `--inject`, inject sidecar content as front matter into document  
   - Only if no front matter exists

---

## 🛠 Tools & Structure
```

bin/sat-generate-dublin-core.py satellites/dublin-core-example.yml config.yml  # base_url, author, etc.

```
yaml
---

## 🚀 Command

```bash
sat-generate-dublin-core \
  --file "archives/euria-generated/docs/en-ch/projects/information-architecture/Draft Users Manual Pipeline SKetch.md" \
  --no-changes  # dry-run, only show sidecar
  # --inject     # optional, inject into front matter
```

------

## 📁 Output

```
objectivec
Draft Users Manual Pipeline SKetch.md
Draft Users Manual Pipeline SKetch.md.sidecar.dublin-core.yml
```

------

## 🧪 Validation

- ✅ Sidecar is valid YAML
- ✅ All 15 `dc:` fields present
- ✅ `dc:title` derived from filename
- ✅ `dc:language` from path
- ✅ No hardcoded values

------

## 📄 SAT Compliance

- ✅ Human in the loop — explicit, opt-in
- ✅ No background execution
- ✅ Interpreter neutral — doesn’t change what the document means
- ✅ Plugins never replace intent — metadata is derived, not defined
- ✅ Definition is source of truth — metadata is computed from it

------

## 🎯 Next Steps (Post-MVP)

- Add `--inject` flag
- Add archive definition validation
- Add Mermaid chart for workflow
- Add CLI help / man page

