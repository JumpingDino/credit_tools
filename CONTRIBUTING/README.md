# Contributing

## Setup

```bash
uv sync
```

## Adding a rating scale resource

Rating scales live as plain data in [src/credit_tools/resources/](../src/credit_tools/resources/), one JSON file per scale (e.g. `moody.json`, `fitch.json`), mapping `{rating: expected_default_rate}`. `credit_tools.rating.assign_rating` is independent of any specific agency's scale — it just needs a dict like this. To add a new one, drop `resources/<name>.json` in and load it with `load_rating_scale("<name>")`.

## Docs

Examples live as Jupyter notebooks under [docs/](../docs/) and are built with [MyST/Jupyter Book v2](https://mystmd.org), configured by [myst.yml](../myst.yml) at the repo root.

```bash
uv sync --extra docs
uv run jupyter-book build --execute --html   # static site in _build/html
uv run jupyter-book start                    # live preview with hot reload
```

`docs/` should only contain notebooks (no hand-written markdown/rst pages) — `myst.yml` is the one config file that lives outside it.

### Adding a new notebook

1. Add the `.ipynb` file under `docs/` (or `docs/examples/`).
2. Add an entry for it under `project.toc` in `myst.yml`, or regenerate the whole table of contents from what's on disk:

   ```bash
   uv run jupyter-book init --project --site --write-toc
   ```

   This only rewrites the `toc:` list — it won't touch metadata you've already filled in (title, description, authors). Run it from the repo root; it refuses to run from inside `docs/`.

Docs are rebuilt with `--execute`, so a notebook that no longer runs against the current code will fail CI — that's intentional, it's what keeps the examples honest.

Docs deploy to GitHub Pages automatically on push to `main` via [.github/workflows/docs.yml](../.github/workflows/docs.yml).
