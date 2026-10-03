# MUTEX.md

A proposed standard for coordinating autonomous coding agents through one shared Markdown file: who is working, what is locked, what was asked and what happened.

It was born at a hackathon where 17 agents shared one workspace for 46 hours. It is a young text, written from one weekend of experience, and it gets better with every workspace that tries it.

- Read it: https://mutex.md/
- Raw Markdown: https://mutex.md/mutex-md-spec.md
- Source: [mutex-md-spec.md](mutex-md-spec.md), the only file you need to edit

## Your pull request is welcome

If you have run more than one agent in the same place, you know something this spec does not yet know. Send it in. Small pull requests are perfectly fine: a single sentence, one rule or one example.

Especially useful:

- **Field reports.** How many agents, which tools, what collided, and what the file looked like afterwards. Verbatim quotes from your agents beat summaries.
- **Counter-examples.** A rule that failed you, and what happened instead.
- **Rules that worked.** A convention your agents invented or you imposed, and why it held up.
- **Corrections.** Unclear wording, contradictions, typos.

Not sure whether something fits? Open a pull request anyway, or start with an [issue](https://github.com/xd-ventures/mutex-md/issues).

## How to contribute

1. Fork the repository and edit `mutex-md-spec.md`. Editing it directly on GitHub works too.
2. Keep one change per pull request. In the description, say which section it touches and what you observed.
3. Open the pull request. A check builds the site automatically, so you will see whether the Markdown renders.

Version numbers move when a MUST changes. Everything else is a patch.

Disagreements are settled in writing, in the pull request, the way the spec itself suggests.

## Preview locally (optional)

```sh
python3 -m venv .venv
.venv/bin/python -m pip install --require-hashes --only-binary=:all: -r requirements.txt
.venv/bin/python scripts/build.py
.venv/bin/python -m http.server 8000 --directory _site
```

Open http://localhost:8000/. Generated files in `_site/` are not committed.

## Repository layout

| Path | What it is |
| --- | --- |
| `mutex-md-spec.md` | The specification. |
| `scripts/build.py` | Renders the spec to HTML. |
| `site/` | Page template and stylesheet. |
| `HOSTING.md` | Maintainer notes on deployment and DNS. |

Merges to `main` are published to https://mutex.md automatically.
