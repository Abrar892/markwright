"""Tests for markwright RSS feed and sitemap generators."""

import unittest
from datetime import datetime
from markwright.rss import RSSFeedGenerator
from markwright.sitemap import SitemapGenerator


class TestRSSAndSitemap(unittest.TestCase):
    def test_rss_generator(self):
        rss = RSSFeedGenerator(title="Dev Blog", link="https://example.com", description="Tech articles")
        rss.add_item(
            title="First Post",
            link="https://example.com/posts/1",
            description="Introduction post",
            pub_date=datetime(2026, 11, 14, 12, 0, 0),
            guid="post-1"
        )
        xml = rss.generate_xml()
        self.assertIn("<rss version=\"2.0\">", xml)
        self.assertIn("<title>Dev Blog</title>", xml)
        self.assertIn("<title>First Post</title>", xml)
        self.assertIn("<guid>post-1</guid>", xml)

    def test_sitemap_generator(self):
        sm = SitemapGenerator(base_url="https://example.com")
        sm.add_url("index.html", lastmod="2026-11-14", priority=1.0)
        sm.add_url("about.html", priority=0.5)

        xml = sm.generate_xml()
        self.assertIn("<urlset", xml)
        self.assertIn("<loc>https://example.com/index.html</loc>", xml)
        self.assertIn("<lastmod>2026-11-14</lastmod>", xml)
        self.assertIn("<priority>1.0</priority>", xml)
        self.assertIn("<loc>https://example.com/about.html</loc>", xml)


if __name__ == "__main__":
    unittest.main()
