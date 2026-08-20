#!/usr/bin/env python3
"""Convert each NewMaterial/Textbook/Ch*/chapter.md to chapter.html.

Tiny KaTeX HTML wrapper styled to match the lecture HTML.
Run from any directory:
    python scripts/render_chapters.py
"""
from __future__ import annotations

import html as html_mod
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TEXTBOOK_DIR = REPO_ROOT / "NewMaterial" / "Textbook"

TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} - ENGR 1050</title>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js"></script>
<style>
 body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; padding: 20px; }}
 h1 {{ color: #011F5B; border-bottom: 3px solid #990000; padding-bottom: 10px; margin-top: 30px; }}
 h2 {{ color: #011F5B; margin-top: 30px; border-bottom: 2px solid #e0e0e0; padding-bottom: 5px; }}
 h3 {{ color: #011F5B; margin-top: 20px; }}
 p {{ text-align: left; margin-bottom: 15px; }}
 code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: ui-monospace, Menlo, Consolas, monospace; }}
 pre {{ background: #f4f4f4; padding: 12px; border-radius: 6px; overflow-x: auto; }}
 blockquote {{ border-left: 4px solid #82AFD3; padding: 4px 12px; background: #f8f9fa; margin: 12px 0; }}
 a {{ color: #4a90e2; }} a:hover {{ color: #990000; }}
 .nav {{ font-size: 0.9rem; margin-bottom: 1rem; }}
</style>
</head>
<body>
<p class="nav"><a href="../../../index.html#extras">&larr; Back to Extras</a></p>
{body}
<script>
document.addEventListener("DOMContentLoaded", function() {{
  if (window.renderMathInElement) {{
    renderMathInElement(document.body, {{
      delimiters: [
        {{left: "$$", right: "$$", display: true}},
        {{left: "$", right: "$", display: false}},
      ],
    }});
  }}
}});
</script>
</body>
</html>
'''


def md_to_html(md: str) -> str:
    """Tiny markdown subset: headings, paragraphs, bullets, fenced code, blockquotes."""
    lines = md.splitlines()
    out = []
    i = 0
    in_para = []
    in_list = False  # False, True (ul), or 'ol'
    while i < len(lines):
        line = lines[i]
        if line.startswith('```'):
            if in_para:
                out.append('<p>' + ' '.join(in_para) + '</p>'); in_para = []
            if in_list:
                out.append('</ul>' if in_list is True else '</ol>'); in_list = False
            i += 1
            code = []
            while i < len(lines) and not lines[i].startswith('```'):
                code.append(html_mod.escape(lines[i]))
                i += 1
            out.append('<pre><code>' + '\n'.join(code) + '</code></pre>')
            i += 1
            continue
        m = re.match(r'^(#+)\s+(.*)$', line)
        if m:
            if in_para:
                out.append('<p>' + ' '.join(in_para) + '</p>'); in_para = []
            if in_list:
                out.append('</ul>' if in_list is True else '</ol>'); in_list = False
            level = min(len(m.group(1)), 6)
            out.append(f'<h{level}>{html_mod.escape(m.group(2))}</h{level}>')
            i += 1
            continue
        if line.startswith('> '):
            if in_para:
                out.append('<p>' + ' '.join(in_para) + '</p>'); in_para = []
            if in_list:
                out.append('</ul>' if in_list is True else '</ol>'); in_list = False
            out.append('<blockquote>' + html_mod.escape(line[2:]) + '</blockquote>')
            i += 1
            continue
        if re.match(r'^[\-*]\s+', line):
            if in_para:
                out.append('<p>' + ' '.join(in_para) + '</p>'); in_para = []
            if not in_list:
                out.append('<ul>'); in_list = True
            item = re.sub(r'^[\-*]\s+', '', line)
            out.append('<li>' + html_mod.escape(item) + '</li>')
            i += 1
            continue
        if re.match(r'^\d+\.\s+', line):
            if in_para:
                out.append('<p>' + ' '.join(in_para) + '</p>'); in_para = []
            if not in_list:
                out.append('<ol>'); in_list = 'ol'
            item = re.sub(r'^\d+\.\s+', '', line)
            out.append('<li>' + html_mod.escape(item) + '</li>')
            i += 1
            continue
        if line.strip() == '':
            if in_para:
                out.append('<p>' + ' '.join(in_para) + '</p>'); in_para = []
            if in_list:
                out.append('</ul>' if in_list is True else '</ol>'); in_list = False
            i += 1
            continue
        in_para.append(html_mod.escape(line))
        i += 1
    if in_para:
        out.append('<p>' + ' '.join(in_para) + '</p>')
    if in_list:
        out.append('</ul>' if in_list is True else '</ol>')
    return '\n'.join(out)


def main():
    if not TEXTBOOK_DIR.is_dir():
        sys.exit(f"Textbook directory not found: {TEXTBOOK_DIR}")
    n = 0
    for sub in sorted(TEXTBOOK_DIR.iterdir()):
        if not sub.is_dir():
            continue
        md_path = sub / "chapter.md"
        html_path = sub / "chapter.html"
        if not md_path.exists():
            print(f"  skip {sub.name} (no chapter.md)")
            continue
        md = md_path.read_text(encoding="utf-8")
        first = next((l for l in md.splitlines() if l.startswith('# ')), '# Chapter')
        title = first.lstrip('# ').strip()
        body = md_to_html(md)
        html_path.write_text(
            TEMPLATE.format(title=html_mod.escape(title), body=body),
            encoding="utf-8",
        )
        size = html_path.stat().st_size
        print(f"  wrote {sub.name}/chapter.html ({size} bytes)")
        n += 1
    print(f"Rendered {n} chapter file(s) under {TEXTBOOK_DIR}")


if __name__ == "__main__":
    main()
