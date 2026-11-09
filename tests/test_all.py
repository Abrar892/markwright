"""Full automated test suite for markwright."""
import unittest
import tempfile
import os
from markwright.parser import MarkdownParser
from markwright.templates import TemplateEngine
from markwright.builder import SiteBuilder


class TestMarkwright(unittest.TestCase):
    def test_frontmatter_extraction(self):
        doc = """---
title: "Architecture Guide"
author: "Engineer"
---
# Welcome
Body content here.
"""
        meta, body = MarkdownParser.extract_frontmatter(doc)
        self.assertEqual(meta.get("title"), "Architecture Guide")
        self.assertEqual(meta.get("author"), "Engineer")
        self.assertIn("# Welcome", body)

    def test_markdown_to_html(self):
        md = "# Heading 1\n\nParagraph with **bold** and *italic* and `code`.\n\n- Item 1\n- Item 2\n\n> Important note"
        html = MarkdownParser.parse_to_html(md)
        self.assertIn("<h1>Heading 1</h1>", html)
        self.assertIn("<strong>bold</strong>", html)
        self.assertIn("<em>italic</em>", html)
        self.assertIn("<code>code</code>", html)
        self.assertIn("<ul>", html)
        self.assertIn("<li>Item 1</li>", html)
        self.assertIn("<blockquote>Important note</blockquote>", html)

    def test_site_builder(self):
        with tempfile.TemporaryDirectory() as src_dir, tempfile.TemporaryDirectory() as out_dir:
            doc1 = os.path.join(src_dir, "index.md")
            with open(doc1, "w", encoding="utf-8") as f:
                f.write("---\ntitle: Home\n---\n# Welcome to Markwright\n")

            doc2 = os.path.join(src_dir, "about.md")
            with open(doc2, "w", encoding="utf-8") as f:
                f.write("---\ntitle: About\n---\n# About Page\n")

            builder = SiteBuilder(src_dir, out_dir)
            count = builder.build()
            self.assertEqual(count, 2)

            self.assertTrue(os.path.exists(os.path.join(out_dir, "index.html")))
            self.assertTrue(os.path.exists(os.path.join(out_dir, "about.html")))
            self.assertTrue(os.path.exists(os.path.join(out_dir, "search_index.json")))


if __name__ == "__main__":
    unittest.main()
