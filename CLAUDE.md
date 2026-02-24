# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the app
python main.py

# Lint
.venv/bin/flake8 .

# Format
.venv/bin/autopep8 --in-place --recursive .

# Type check
.venv/bin/mypy .

# Install dependencies
uv sync
# or
pip install -e .
```

The project uses a `.venv` virtual environment. Always prefix tool commands with `.venv/bin/` or activate the venv first.

## Architecture

The app is a CLI tool for scraping and analyzing websites. Entry point is `main.py`, which presents a numeric menu and routes to one of five operations.

**Two-layer structure:**

- `classes/` — reusable components (parsers, downloaders, UI helpers)
- `modules/` — single-purpose orchestration functions called from `main.py`

**Key data flow for sitemap downloading (options 0 & 1):**

1. `sitemap_urls.txt` — stores known sitemap index URLs (one per line, managed by `SiteUrlsFile`)
2. `SitemapParser` — fetches and parses XML sitemaps (supports sitemap indexes that point to sub-sitemaps)
3. `HtmlDownloader` — downloads HTML pages from parsed URLs; saves them under a folder named after the domain, preserving URL path structure (e.g. `/about` → `domain/about.html`)

**Key data flow for link analysis (options 3 & 4):**

1. `fzf` is used interactively to pick a downloaded site folder from the working directory
2. `choose_html_files` recursively walks the folder and lets the user select HTML files by index/range
3. `HtmlLinksParser` parses `<a>` tags from the selected files using BeautifulSoup, building `LinkInfo` named tuples
4. Results are displayed as a `rich` table; option 4 filters to only empty/`#` hrefs

**Key classes:**

| Class | Purpose |
|---|---|
| `SitemapParser` | Fetch & parse XML sitemaps; supports index → sub-sitemap recursion |
| `HtmlDownloader` | Download URLs to disk with domain-based directory structure |
| `HtmlLinksParser` | Extract all `<a>` tags from HTML files; supports empty-href filtering |
| `HtmlSeoParser` (`HtmlParser.py`) | Extract `<title>`, meta description, og:image from HTML files |
| `Select` | Interactive selection via `fzf` (multi-select) or `simple-term-menu` |
| `SiteUrlsFile` | Read/write the `sitemap_urls.txt` file |
| `PathHelper` | Resolves paths relative to `main.py`'s directory, not CWD |
| `Menu` / `MyTable` | CLI menu display using `rich` |

**External tool dependency:** `fzf` must be installed on the system for the link analysis and SEO features (options 2, 3, 4). It is invoked via `subprocess` in `Select.select_with_fzf()`.

**`sitemap_urls.txt`** lives in the project root and stores sitemap index URLs. The app must be run from the project root so `PathHelper` resolves it correctly.

Downloaded HTML is saved to the **current working directory** under a subdirectory named after the domain (e.g. `./example.com/path/page.html`).
