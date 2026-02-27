# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run the app (must be run from ~/Downloads — see Runtime constraint below)
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

The app is a CLI tool for scraping and analyzing websites. Entry point is `main.py`, which presents a numeric menu (options 0–8) and routes to one of nine operations.

**Two-layer structure:**

- `classes/` — reusable components (parsers, downloaders, UI helpers)
  - `classes/menu/` — parsers specific to menu operations (`HtmlLinksParser`, `HtmlSeoParser`, `DuplicateIdsParser`)
- `modules/` — single-purpose orchestration functions called from `main.py`

**Key data flow for sitemap downloading (options 0 & 1):**

1. `sitemap_urls.txt` — stores known sitemap index URLs (one per line, managed by `SiteUrlsFile`)
2. `SitemapParser` — fetches and parses XML sitemaps (supports sitemap indexes that point to sub-sitemaps)
3. `HtmlDownloader` — downloads HTML pages from parsed URLs; saves them under a folder named after the domain, preserving URL path structure (e.g. `/about` → `domain/about.html`)

**Key data flow for HTML analysis (options 2–7):**

1. `fzf` is used interactively to pick a downloaded site folder from the working directory
2. `choose_html_files` recursively walks the folder and lets the user select HTML files by index/range
3. A parser class processes the selected files:
   - `HtmlLinksParser` — extracts `<a>` tags, builds `LinkInfo` named tuples. Has separate methods for all links, empty/`#` hrefs, WhatsApp links, and hash-links without matching IDs
   - `HtmlSeoParser` — extracts `<title>`, meta description, og:image, headings (h1-h3), noindex/nofollow
   - `DuplicateIdsParser` — finds duplicate `id` attributes (skips SVG children)
4. Results are displayed as `rich` tables/panels

**Key classes:**

| Class | Location | Purpose |
|---|---|---|
| `SitemapParser` | `classes/` | Fetch & parse XML sitemaps; supports index → sub-sitemap recursion |
| `HtmlDownloader` | `classes/` | Download URLs to disk with domain-based directory structure |
| `HtmlLinksParser` | `classes/menu/` | Extract `<a>` tags from HTML files; filtering methods for empty, WhatsApp, and hash links |
| `HtmlSeoParser` | `classes/menu/` | Extract title, meta description, og:image, headings, noindex/nofollow |
| `DuplicateIdsParser` | `classes/menu/` | Find duplicate `id` attributes in HTML (excludes SVG) |
| `Select` | `classes/` | Interactive selection via `fzf` (multi-select) or `simple-term-menu` |
| `SiteUrlsFile` | `classes/` | Read/write the `sitemap_urls.txt` file |
| `PathHelper` | `classes/` | Resolves paths relative to `main.py`'s directory, not CWD |
| `Menu` / `MyTable` | `classes/` | CLI menu display using `rich` |

**Runtime constraint:** `check_if_is_downloads_dir()` enforces that the CWD must be named `Downloads` (typically `~/Downloads`). The app exits immediately if run from elsewhere. Downloaded HTML is saved to the CWD under a subdirectory named after the domain (e.g. `~/Downloads/example.com/path/page.html`).

**`sitemap_urls.txt`** lives in the project root (resolved via `PathHelper.entry_dir`, not CWD) and stores sitemap index URLs.

**External tool dependencies:** `fzf` and `bat` must be installed on the system. `fzf` is used for folder selection; `bat` is used for file preview in `simple-term-menu`.
