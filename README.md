# credit_tools

Multiple out-of-the-box functionalities for credit, installable via pip/uv.

## Install

```bash
pip install credit_tools
# or
uv add credit_tools
```

## Structure

```
src/credit_tools/
    rating/       # generic borrower-rating assignment (independent of any one scale)
    resources/    # bundled rating scales as data, e.g. resources/moody.json
```

## Docs

Examples live as Jupyter notebooks in [docs/](docs/), published to GitHub Pages on every push to `main`: https://jumpingdino.github.io/credit_tools/

## Contributing

See [CONTRIBUTING/README.md](CONTRIBUTING/README.md) for dev setup, adding rating scale resources, and building/updating the docs.
