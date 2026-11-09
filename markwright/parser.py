"""Pure Python Markdown parser and front-matter extractor."""
import re
from typing import Tuple, Dict, Any


class MarkdownParser:
    @staticmethod
    def extract_frontmatter(content: str) -> Tuple[Dict[str, str], str]:
        metadata = {}
        body = content
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                raw_fm = parts[1]
                body = parts[2].strip()
                for line in raw_fm.splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        metadata[k.strip()] = v.strip().strip('"').strip("'")
        return metadata, body

    @classmethod
    def parse_to_html(cls, markdown: str) -> str:
        lines = markdown.splitlines()
        html_lines = []
        in_code_block = False
        in_list = False

        for line in lines:
            # Code fence
            if line.strip().startswith("```"):
                if in_code_block:
                    html_lines.append("</code></pre>")
                    in_code_block = False
                else:
                    html_lines.append("<pre><code>")
                    in_code_block = True
                continue

            if in_code_block:
                escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                html_lines.append(escaped)
                continue

            # Headings
            m_h = re.match(r"^(#{1,6})\s+(.*)$", line)
            if m_h:
                if in_list:
                    html_lines.append("</ul>")
                    in_list = False
                level = len(m_h.group(1))
                html_lines.append(f"<h{level}>{cls._inline_format(m_h.group(2))}</h{level}>")
                continue

            # Unordered lists
            m_li = re.match(r"^[-*+]\s+(.*)$", line)
            if m_li:
                if not in_list:
                    html_lines.append("<ul>")
                    in_list = True
                html_lines.append(f"<li>{cls._inline_format(m_li.group(1))}</li>")
                continue
            elif in_list and line.strip() == "":
                html_lines.append("</ul>")
                in_list = False

            # Blockquote
            if line.startswith(">"):
                quote_text = line.lstrip(">").strip()
                html_lines.append(f"<blockquote>{cls._inline_format(quote_text)}</blockquote>")
                continue

            # Paragraph
            stripped = line.strip()
            if stripped:
                html_lines.append(f"<p>{cls._inline_format(stripped)}</p>")

        if in_code_block:
            html_lines.append("</code></pre>")
        if in_list:
            html_lines.append("</ul>")

        return "\n".join(html_lines)

    @staticmethod
    def _inline_format(text: str) -> str:
        # Links: [text](url)
        text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
        # Bold: **bold** or __bold__
        text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
        # Italic: *italic* or _italic_
        text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
        # Inline code: `code`
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
        return text
