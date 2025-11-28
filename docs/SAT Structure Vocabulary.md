# SAT Structure Vocabulary

Resource

## Project Root and Embedded Archives

The **project_root** is the top-level directory of a software project or repository that may contain one or more SAT archives.

A project_root:

- May contain source code, tools, tests, and other non-archive files
- May contain one or more directories that serve as SAT archive_roots
- Is not required to follow SAT’s archival directory structure

An **archive_root** may be:

- The same as the project_root, or
- A subdirectory inside the project_root

### Example: Archive Embedded in a Project

```bash
/home/initial/projects/archives/dev/tools      # project_root
/home/initial/projects/archives/dev/tools/docs # archive_root
```

In this case:

- `/home/initial/projects/archives/dev/tools` is the project_root
- `/home/initial/projects/archives/dev/tools/docs` is the archive_root for SAT documentation
- All SAT archive vocabulary (language_root, taxonomy roots, content_roots, etc.) applies starting at `docs/`

## Archive Root

* The **archive_root** is the topmost directory that contains the entire Source Archive.
* It represents the physical root of all archive content.

The archive_root:

- Has no required name.
- Exists as a physical path on disk.
- May contain any number of language roots.
- Does not impose semantics by itself.

### Definition Examples

These all describe the same archive root

#### Fixed

```bash
archive_root: /home/initial/projects/archives/dev/test-archive
```

#### Relative

As in relative to the SAT creation tools root:

```bash
archive_root: ../test-archive
```

#### Home Relative

A path that begins at the user's home directory:

```bash
archive_root: ~/projects/archives/dev/test-archive
```

## Language Roots

A **language_root** is a top-level directory inside the archive_root whose **name is a language-and-locale slug**.

Each language_root physically groups all archive content in that specific language and regional variant.

A language_root:

- Lives directly under the archive_root.
- Uses a normalized BCP-47–like slug such as `en-ca`, `fr-qc`, `es-mx`.
- Contains the physical content for that language.
- Does not yet imply taxonomy or metadata.

### Examples of language roots

```bash
archive_root/en-ca/
archive_root/fr-qc/
archive_root/es-mx/
```

Each of these directories is a **language_root**, representing a distinct localized content subtree.

## Taxonomy Roots

When a taxonomy is applied it is reflected as **directory structures** below each of the archive’s supported **language_root**'s.

So the file and path structure of the applied taxonomy:

- Lives under each language_root
- May include a defined set of child directories

### Example using a PARA Taxonomy

A PARA taxonomy describes four taxonomic root directories:

````bash
projects/
areas/
resources/
archives/
````

In an archive supporting three language locales with **English Only** PARA-based taxonomic child directories you would have something like this:

```bash
# Canadian English
archive_root/en-ca/projects/
archive_root/en-ca/areas/
archive_root/en-ca/resources/
archive_root/en-ca/archives/
# Quebec French
archive_root/fr-qc/projects/
archive_root/fr-qc/areas/
archive_root/fr-qc/resources/
archive_root/fr-qc/archives/
# Mexican Spanish
archive_root/es-mx/projects/
archive_root/es-mx/areas/
archive_root/es-mx/resources/
archive_root/es-mx/archives/
```

```bash
<archive_root>/<language_and_locale_slug><taxonomic_root_x>
```

Under this **taxonomy root**, four directories form the physical namespace:

```bash
<archive_root>/<language_slug><taxonomic_para_root_projects_translation>
<archive_root>/<language_slug><taxonomic_para_root_areas_translation>
<archive_root>/<language_slug><taxonomic_para_root_resources_translation>
<archive_root>/<language_slug><taxonomic_para_root_resources_translation><archives>
```

These directories:

- Are siblings.
- Make up the four PARA root directories

## Content Roots

A **content_root** is any directory located inside a taxonomy namespace where human-authored content may be placed.
It represents the physical location where Markdown documents, subdirectories, or other content-related files can exist within the archive.

A content_root:

- Lives under a taxonomy root such as `projects/`, `areas/`, `resources/`, or `archives/`
- May contain Markdown documents (for example: `index.md`, `overview.md`, etc.)
- May be empty or populated
- May contain child directories (branch) or may hold content directly (leaf)
- Is activated simply by the presence or possibility of content

### Shallow Content Root

If a contributor places an `index.md` directly inside a taxonomy namespace:

```bash
archive_root/en-ca/projects/index.md
```

Then:

```bash
archive_root/en-ca/projects/
```

is both a **taxonomy namespace** *and* a **content_root**, because content is located inside it.

### Deeper Content Roots

Content roots may also exist deeper in the directory structure:

```bash
archive_root/en-ca/projects/my-project/
archive_root/en-ca/projects/my-project/phase-one/
archive_root/en-ca/resources/reference-material/guides/
```

Each of these directories is considered a **content_root** because they are valid locations for content placement.

### Content Root Characteristics

- There can be many content roots across the archive.
- A content_root does not itself indicate meaning or metadata.
- A content_root can act as a parent directory for other content roots.
- The presence of a content document (such as `index.md`) is sufficient to classify a directory as a content_root.
- A taxonomy namespace becomes a content_root if content is placed directly inside it.

## Content Documents

A **content_document** is a human-authored file located inside a content_root.
It represents a single piece of content within the archive and is typically written in Markdown format.

A content_document:

- Lives inside a **content_root**
- Is a discrete file intended to be viewed or read
- May be accompanied by other content documents in the same directory
- Does not define structure, meaning, or metadata at this physical layer
- Is recognized by its file extension, most commonly `.md`

### Common Types of Content Documents

Typical content documents include files such as:

```bash
index.md
overview.md
introduction.md
chapter-01.md
notes.md
```

These filenames imply no semantics in the physical structure, even if tools may later use them in meaningful ways.

### Example: Content Documents Inside a Content Root

```bash
archive_root/en-ca/projects/my-project/index.md
archive_root/en-ca/projects/my-project/requirements.md
archive_root/en-ca/projects/my-project/todo.md
```

Here:

- `my-project/` is the content_root
- `index.md`, `requirements.md`, and `todo.md` are all **content_documents**

### Index Documents

If a directory contains a file named `index.md`:

```bash
archive_root/en-ca/areas/well-being/index.md
```

Then:

- `well-being/` is a content_root
- `index.md` is one content_document among potentially many

The presence of an index file does **not** grant special meaning at this physical vocabulary layer.
It only indicates that content is present.

### Additional Characteristics of Content Documents

- Multiple content_documents may exist in a single content_root.
- A content_document may coexist with child directories inside the same content_root.
- Content documents do not impose hierarchy; the directory structure does.
- A directory with no content_documents may still be a valid content_root if contributors intend to place content there.

## Document Assets

### Summary

#### Insight

##### Asset Handling Must Align With Document Movement

When content_documents move, their associated assets must move with them, otherwise:

- linked images break
- diagrams become disconnected
- tools cannot cleanly update references
- reorganizing content_root structures becomes risky

Because SAT archives are designed for **long-term maintainability**, every document must remain “portable” — able to be reorganized freely without manual cleanup.

This leads naturally to the pattern:

```bash
content_root/document.md
content_root/document.md.assets/
```

### Why this pattern works

#### Assets travel with their document
Moving `document.md` automatically implies moving `document.md.assets/`.

#### No naming collisions
Every document gets its own self-contained asset folder.

#### Supports multiple documents per content_root
Example:

```bash
content_root/overview.md
content_root/overview.md.assets/
content_root/details.md
content_root/details.md.assets/
```

##### Independent of taxonomy
Works the same whether the document is in:

* projects root
* a nested area

- a deep branch

##### Neutral across tools
This pattern works whether you use:

* Typora
* VS Code
* Obsidian
* static converters
* future SAT tooling

##### No generator semantics introduced

This stays purely in the physical vocabulary layer.

### Conclusion of Insight

Assets must be moved together with content_documents means:

* We should treat “document.md.assets/” as the default expected physical pattern for assets.
* We should not mandating until SAT’s asset vocabulary matures.

This gives contributors freedom while giving future tooling a predictable structure to work with.

#### Description

Assets are supporting files associated with content_documents.
They are not part of the taxonomy, and they are not considered content_documents themselves.
At this stage of the SAT vocabulary, assets are treated in a minimal and flexible manner to avoid imposing premature structure.

Assets:

- Are non-Markdown files (such as images, diagrams, PDFs, audio files, or other attachments)
- Physically reside inside a **content_root**, but outside the content_documents themselves
- May be created or organized automatically by editing tools such as Typora
- Do not define meaning or metadata at this layer
- Do not impose or require a specific directory naming convention

#### Typical Asset Placement (Tool-Driven)

Some editors and tools create asset directories automatically, using patterns such as:

```bash
content_root/document.md
content_root/document.md.assets/
```

or:

```bash
content_root/.assets/
```

So, SAT does not currently prescribe one pattern over another.
Instead, SAT recognizes that assets accompany content_documents and physically live alongside them inside the same content_root. 

### Current Working Approach to Assets

Keep the physical vocabulary flexible:

- SAT does **not** mandate a specific assets directory name
- SAT does **not** define a global assets_root
- SAT allows tools (e.g., Typora) to manage assets according to their own conventions
- SAT will formalize asset structure only when real use cases emerge

This keeps the system adaptable while still acknowledging the role of assets within content_roots.
