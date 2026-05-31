# Harness Engineering — AGENTS.md

## Project

Open source book teaching how to build engineering-grade AI coding pipelines with OpenCode. All content is Markdown served by docsify. Currently in early writing phase — most files are TODO stubs.

## Commands

```bash
npx docsify serve ./src    # local preview (port 3000)
```

No build, test, lint, or typecheck. docsify loads JS from CDN at runtime.

## Content layout

```
src/                          # book content — docsify source root
  index.html                  # docsify entry (basePath for GitHub Pages)
  _sidebar.md                 # manual nav — keep in sync when adding/removing pages
  01-introduction/README.md   # chapter dirs: 0N-{english-name}
  ...
docs/                         # project management (NOT book content)
  plans/                      # writing plans — check before writing
  requirements/               # user stories & PRD
assets/images/                # images only
examples/                     # sample configs & skills
```

## Writing rules

- Each chapter is a directory under `src/`. Chapter dirs use zero-padded numbers: `01-introduction`, `02-core-concepts`, etc.
- Each chapter has `README.md` as index plus separate `.md` files per section.
- Update `src/_sidebar.md` when adding or renaming a page — docsify does not auto-discover.
- Images go in `assets/images/`.
- Code blocks must specify language (bash, json, jsonc, markdown, yaml).
- File names: lowercase, kebab-case.
- Content is in Chinese (zh-CN).

## Opencode config

`opencode.jsonc` enables oh-my-openagent plugin. `.opencode/oh-my-openagent.jsonc` has no custom agents yet — skeleton only.

## GitHub Pages

Deployed from `src/` directory via `.github/workflows/deploy-docsify.yml` on push to `main`. No manual Pages config needed.
