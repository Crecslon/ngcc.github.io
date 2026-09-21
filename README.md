# ngcc.dev

Source for <https://ngcc.dev>. Pages are Markdown under `content/`, rendered
by `tools/build.py` into `docs/`, which GitHub Pages serves directly (no
Jekyll). Requires Python 3 and the `markdown` package.

    make build      # content/ -> docs/
    make serve      # preview on http://localhost:8000
    git commit -a && git push   # deploy

Both `content/` and the rendered `docs/` are committed, so what is pushed is
exactly what is served. Everything in this repository is public, including
its history: commit only material that is ready to be on the site.
