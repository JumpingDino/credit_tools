# Contributing

## Setup

```bash
uv sync
```

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

## Releasing a new version

Publishing to PyPI is handled by [.github/workflows/publish.yml](../.github/workflows/publish.yml) via [Trusted Publishing](https://docs.pypi.org/trusted-publishers/) (OIDC — no API tokens stored anywhere), triggered by publishing a GitHub Release.

1. Bump `version` in [pyproject.toml](../pyproject.toml).
2. Commit and push the bump to `main`:

   ```bash
   git add pyproject.toml
   git commit -m "Bump version to X.Y.Z"
   git push
   ```
3. Create and publish a GitHub Release tagged `vX.Y.Z` (matching the version from step 1) — this is what triggers the workflow:

   ```bash
   gh release create vX.Y.Z --tißtle "vX.Y.Z" --generate-notes
   ```

   Or via the UI: [Releases → Draft a new release](https://github.com/JumpingDino/credit_tools/releases/new), type the new tag under "Choose a tag" (create it on publish), then **Publish release**.
4. Watch the run under the repo's [Actions tab](https://github.com/JumpingDino/credit_tools/actions/workflows/publish.yml) — it builds with `uv build` and publishes with `uv publish`. Once it's green, the new version is live at https://pypi.org/project/credit_tools/.

The very first release needed a one-time [pending trusted publisher](https://pypi.org/manage/account/publishing/) registered on PyPI (project name `credit_tools`, owner `JumpingDino`, repo `credit_tools`, workflow `publish.yml`, environment `pypi`) before any release existed. Subsequent releases don't need this — PyPI converts it into a normal trusted publisher after the first successful publish.
