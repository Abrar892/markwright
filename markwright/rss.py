"""rss.py — RSS 2.0 XML feed generator for MarkWright static sites."""

from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import List
import html


@dataclass
class RSSItem:
    title: str
    link: str
    description: str
    pub_date: datetime
    guid: str


class RSSFeedGenerator:
    """Generates standard RSS 2.0 XML feeds."""

    def __init__(self, title: str, link: str, description: str):
        self.title = title
        self.link = link
        self.description = description
        self.items: List[RSSItem] = []

    def add_item(self, title: str, link: str, description: str, pub_date: datetime, guid: str) -> None:
        self.items.append(RSSItem(title=title, link=link, description=description, pub_date=pub_date, guid=guid))

    def generate_xml(self) -> str:
        lines = [
            '<?xml version="1.0" encoding="UTF-8" ?>',
            '<rss version="2.0">',
            '<channel>',
            f'  <title>{html.escape(self.title)}</title>',
            f'  <link>{html.escape(self.link)}</link>',
            f'  <description>{html.escape(self.description)}</description>',
        ]

        for item in self.items:
            rfc822_date = item.pub_date.strftime("%a, %d %b %Y %H:%M:%S +0000")
            lines.extend([
                '  <item>',
                f'    <title>{html.escape(item.title)}</title>',
                f'    <link>{html.escape(item.link)}</link>',
                f'    <description>{html.escape(item.description)}</description>',
                f'    <pubDate>{rfc822_date}</pubDate>',
                f'    <guid>{html.escape(item.guid)}</guid>',
                '  </item>',
            ])

        lines.extend([
            '</channel>',
            '</rss>',
        ])
        return "\n".join(lines)
