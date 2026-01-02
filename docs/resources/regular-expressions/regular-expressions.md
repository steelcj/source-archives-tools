# Regular Expressions

## To match a blank line followed by `---`

Use this regular expression:

```bash
(?:\r?\n)\r?\n---
```

### What this matches

- `\r?\n` → end of a line
- another `\r?\n` → a **blank line**
- `---` → the three hyphens immediately after the blank line

------

### Common variants (depending on how strict you want to be)

**Blank line that may contain spaces or tabs:**

```
\r?\n[ \t]*\r?\n---
```

**Match `---` only if it’s the first non-whitespace on the next line:**

```bash
\r?\n[ \t]*\r?\n[ \t]*---
```

**Line-based (multiline mode):**

```bash
^\s*$\r?\n^---$
```

(Enable multiline / `m` flag)

------

### Tool-specific examples

**ripgrep / grep -P**

```bash
rg -P "\r?\n[ \t]*\r?\n---"
```

**Python**

```python
re.search(r"\r?\n[ \t]*\r?\n---", text)
```