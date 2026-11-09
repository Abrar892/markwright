"""HTML page templates and theme layout renderer."""
from typing import Dict, Any, List


class TemplateEngine:
    @staticmethod
    def render_page(title: str, content_html: str, nav_links: List[tuple[str, str]], meta: Dict[str, str]) -> str:
        nav_items = "".join(f'<li><a href="{href}">{name}</a></li>' for name, href in nav_links)
        author_str = f"<p class='meta'>By {meta['author']}</p>" if "author" in meta else ""
        date_str = f"<p class='meta'>Published: {meta['date']}</p>" if "date" in meta else ""

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <style>
        :root {{ --bg: #0d1117; --card: #161b22; --border: #30363d; --text: #c9d1d9; --accent: #58a6ff; }}
        body {{ font-family: -apple-system, sans-serif; background: var(--bg); color: var(--text); margin: 0; display: flex; min-height: 100vh; }}
        aside {{ width: 250px; background: var(--card); border-right: 1px solid var(--border); padding: 24px; box-sizing: border-box; }}
        aside h2 {{ font-size: 16px; color: #8b949e; text-transform: uppercase; margin-top: 0; }}
        aside ul {{ list-style: none; padding: 0; margin: 0; }}
        aside li {{ margin-bottom: 8px; }}
        aside a {{ color: var(--text); text-decoration: none; font-size: 14px; }}
        aside a:hover {{ color: var(--accent); }}
        main {{ flex: 1; padding: 40px; max-width: 800px; box-sizing: border-box; }}
        h1, h2, h3 {{ color: #f0f6fc; }}
        a {{ color: var(--accent); }}
        pre {{ background: #000; padding: 14px; border-radius: 6px; overflow-x: auto; border: 1px solid var(--border); }}
        code {{ font-family: monospace; color: #79c0ff; }}
        blockquote {{ border-left: 4px solid var(--accent); margin: 0; padding-left: 16px; color: #8b949e; }}
        .meta {{ font-size: 13px; color: #8b949e; margin-top: 4px; }}
    </style>
</head>
<body>
    <aside>
        <h2>Documentation</h2>
        <ul>{nav_items}</ul>
    </aside>
    <main>
        {author_str}
        {date_str}
        {content_html}
    </main>
</body>
</html>"""
