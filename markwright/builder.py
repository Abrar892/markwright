"""Site builder and full-text index generator."""
import os
import json
from typing import List, Dict, Any
from markwright.parser import MarkdownParser
from markwright.templates import TemplateEngine


class SiteBuilder:
    def __init__(self, src_dir: str, out_dir: str):
        self.src_dir = os.path.abspath(src_dir)
        self.out_dir = os.path.abspath(out_dir)

    def build(self) -> int:
        os.makedirs(self.out_dir, exist_ok=True)
        md_files = []
        for root, _, files in os.walk(self.src_dir):
            for f in files:
                if f.lower().endswith((".md", ".markdown")):
                    md_files.append(os.path.join(root, f))

        nav_links = []
        parsed_pages = []

        for fpath in md_files:
            rel = os.path.relpath(fpath, self.src_dir)
            target_rel = os.path.splitext(rel)[0] + ".html"
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()

            meta, body = MarkdownParser.extract_frontmatter(content)
            title = meta.get("title", os.path.splitext(os.path.basename(fpath))[0].capitalize())
            html_body = MarkdownParser.parse_to_html(body)
            nav_links.append((title, target_rel.replace("\\", "/")))
            parsed_pages.append({
                "target_rel": target_rel,
                "title": title,
                "html_body": html_body,
                "meta": meta,
                "raw_body": body
            })

        # Render and write all HTML pages
        search_index = []
        for page in parsed_pages:
            full_html = TemplateEngine.render_page(page["title"], page["html_body"], nav_links, page["meta"])
            dest_path = os.path.join(self.out_dir, page["target_rel"])
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(full_html)

            search_index.append({
                "title": page["title"],
                "url": page["target_rel"].replace("\\", "/"),
                "text": page["raw_body"][:300]
            })

        # Write search index
        index_path = os.path.join(self.out_dir, "search_index.json")
        with open(index_path, "w", encoding="utf-8") as f:
            json.dump(search_index, f, indent=2)

        return len(parsed_pages)
