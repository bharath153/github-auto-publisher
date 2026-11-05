# GitHub Auto-Publisher

> Experimental PySide6 desktop utility for scanning local projects, generating documentation, and publishing repositories through GitHub APIs.

## Overview

This repository explores a desktop workflow that combines:
- local project scanning;
- a PySide6 GUI;
- configurable LLM-backed documentation generation;
- GitHub publishing operations;
- local configuration management.

It is a tooling experiment rather than a flagship engineering project.

## Structure

```text
github-auto-publisher/
├── src/
│   ├── main.py
│   ├── ai/
│   ├── core/
│   ├── gui/
│   └── utils/
├── requirements.txt
├── setup.py
├── setup_guide.md
└── PROJECT_README.md
```

## Run

```bash
git clone https://github.com/bharath153/github-auto-publisher.git
cd github-auto-publisher
pip install -r requirements.txt
python src/main.py
```

## Security

Do not hard-code API keys or GitHub credentials in source files. Use the application's configuration/credential mechanisms and follow the least-privilege principle for tokens.

## Scope

This repository is kept public as a software-tooling experiment. My primary engineering and research work is represented by:
- [OpenNavLab](https://github.com/bharath153/OpenNavLab)
- [Electric-Motor-Design-Surrogate-Optimization](https://github.com/bharath153/Electric-Motor-Design-Surrogate-Optimization)

For additional implementation notes, see `setup_guide.md` and `PROJECT_README.md`.
