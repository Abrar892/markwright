# Markwright

Pure Python Markdown static site generator with automatic navigation, themes, and full-text index generation.

## Features
- **Built-in Markdown Parser:** Converts headings, lists, bold/italics, links, blockquotes, and code blocks to HTML without external packages.
- **Front-Matter Metadata:** Parses YAML-style header blocks (`title`, `date`, `tags`, `author`).
- **Theming & Templating:** Clean dark and light typography themes with mobile responsiveness.
- **Search Indexer:** Emits client-side JSON search index for offline static search.
- **Zero Third-Party Dependencies:** 100% Python standard library (`re`, `json`, `os`, `shutil`).

## Usage
```bash
python -m markwright.cli build docs/ --output dist/
```
