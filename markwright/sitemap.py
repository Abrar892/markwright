"""sitemap.py — Search engine sitemap.xml generator for MarkWright static sites."""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional
import html


@dataclass
class SitemapURL:
    loc: str
    lastmod: Optional[str] = None
    changefreq: str = "weekly"
    priority: float = 0.8


class SitemapGenerator:
    """Generates standard sitemap.xml according to sitemaps.org protocol."""

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")
        self.urls: List[SitemapURL] = []

    def add_url(self, path: str, lastmod: Optional[str] = None, changefreq: str = "weekly", priority: float = 0.8) -> None:
        full_url = f"{self.base_url}/{path.lstrip('/')}"
        self.urls.append(SitemapURL(loc=full_url, lastmod=lastmod, changefreq=changefreq, priority=priority))

    def generate_xml(self) -> str:
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        ]

        for u in self.urls:
            lines.extend([
                '  <url>',
                f'    <loc>{html.escape(u.loc)}</loc>',
            ])
            if u.lastmod:
                lines.append(f'    <lastmod>{html.escape(u.lastmod)}</lastmod>')
            lines.extend([
                f'    <changefreq>{html.escape(u.changefreq)}</changefreq>',
                f'    <priority>{u.priority:.1f}</priority>',
                '  </url>',
            ])

        lines.append('</urlset>')
        return "\n".join(lines)
