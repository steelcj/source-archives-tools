# source-archive-tools

## Description

A small collection of scripts and standards for creating and managing Source Archives in development environments.  
These tools are designed to remain lightweight, portable, and easy to integrate into multilingual or multi-archive workflows.

## Installation in a Development Environment

The recommended layout places all development archives, tools, and optional shared configs under:

```
~/projets/archives/dev/
```

## Create development root directory

```bash
mkdir -p ~/projets/archives/dev
cd ~/projets/archives/dev
```

## Clone the tools repository into the tools directory

```bash
git clone git@github.com:steelcj/source-archives-tools.git tools
```

## Verify branch (optional but recommended)

```bash
cd tools
git status
```

In this case I am on the main branch

```bash
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

### Branch confirmation using branch command

```bash
git branch
```

expected output

```bash
* main
```

for sure we are on main, but I am developing

## Ensure you are on the development branch

```bash
git checkout dev
```

Output:

```bash
branch 'dev' set up to track 'origin/dev'.
Switched to a new branch 'dev'
```

## Local Repo Verification

```bash
tree ~/projets/archives/dev/tools
```

Expected output:

```bash
/home/initial/projets/archives/dev/tools
├── docs
│   └── git
│       ├── create-git-branches.md
│       ├── extended-git-workflow-for-source-archives-tools.md
│       └── minimal-git-workflow-example.md
├── README.md
├── ROADMAP.md
├── scripts
│   └── init-archive.sh
└── standards
    └── languages.yml

5 directories, 7 files
```

## Developing

### Before making changes

To keep the development branch clean and traceable, follow this minimal workflow before editing files:

1. create a feature branch  
2. make the edits  
3. commit the changes  
4. push the branch  
5. open a pull request if using GitHub

### Creating a feature branch

```bash
cd ~/projets/archives/dev/tools
git checkout -b feature/update-readme
```
## Before Testing

Your going to want to test your changes

### Ensure any scripts in the scripts directory are executable

```bash
chmod +x scripts/*.sh
```

## When your ready to commit

### Save and commit your changes

```bash
git add README.md
git commit -m "Update README with development setup instructions"
```

### Push the branch to GitHub

```bash
git push -u origin feature/update-readme
```

Output example:

```bash
Total 0 (delta 0), reused 0 (delta 0), pack-reused 0
remote: 
remote: Create a pull request for 'feature/update-readme' on GitHub by visiting:
remote:      https://github.com/steelcj/source-archives-tools/pull/new/feature/update-readme
remote: 
To github.com:steelcj/source-archives-tools.git
 * [new branch]      feature/update-readme -> feature/update-readme
branch 'feature/update-readme' set up to track 'origin/feature/update-readme'.
```
