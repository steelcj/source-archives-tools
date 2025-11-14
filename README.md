# source-archives-tools

## Tools Installation

Start with a tools-only Installation. Tools do not enforce a language and are outside of archives. tools are **canonical-language-neutral** but archives are not. So for example, in a French-first developers environment, you might do this:

```bash
PROJECTS_ROOT=~/projets/archives-sources
```

In an English developers environment perhaps this:

```bash
PROJECTS_ROOT=~/projects/source-archives
```

### Create the projects root

```bash
mkdir -p "$PROJECTS_ROOT"
cd "$PROJECTS_ROOT"
```

### Clone tools

to a French language directory **outils**

French

```bash
git clone git@github.com:<org>/sources-archive-tools.git outils
```

to an English language directory:

```bash
git clone git@github.com:<org>/sources-archive-tools.git tools
```

